import logging.handlers
import os.path
import sys

from PyQt5.QtCore import QSettings, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLineEdit, QMainWindow, QMessageBox, QWidget

from . import database as db
from .ui import Ui_AuthForm, Ui_ContactDataForm, Ui_ContactsPage, Ui_MainWindow, Ui_RegisterForm

logger = logging.getLogger("phone_book.__main__")


def show_db_conn_err_msg(parent):
    QMessageBox.critical(parent, "Телефонная книжка",
                         "Не удалось соединиться с базой данных. Попробуйте позже или проверьте настройки.")


def show_not_implemented_msg(parent):
    QMessageBox.information(parent, "Телефонная книжка", "Очень жаль, но пока не реализовано.")


class RegisterForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint)
        self.ui = Ui_RegisterForm()
        self.ui.setupUi(self)

        self.register_result = None, None, None
        self.ui.button_box.accepted.connect(self.handle_ok_btn_clicked)
        self.ui.button_box.rejected.connect(self.reject)

    def handle_ok_btn_clicked(self):
        username = self.ui.username_ln_edt.text()
        email = self.ui.email_ln_edt.text()
        birth_date = self.ui.birth_date_dt_edt.dateTime().toString("yyyy.MM.dd")
        # TODO: some input validaton
        try:
            self.ui.button_box.button(QDialogButtonBox.Ok).setDisabled(True)
            res_code, password = db.register(username, email, birth_date)
        except db.DatabaseConnectionError:
            show_db_conn_err_msg(self)
            self.close()
        else:
            self.register_result = (res_code, username, password)
            if res_code is db.RegisterResult.SUCCESS:
                self.accept()
                # TODO: send a password by an email
                ans = QMessageBox.question(
                    self.parent(), "Телефонная книжка",
                    "Регистрация успешна.\n"
                    "Ваш пароль выслан [! не реализовано] на указанную почту.\n"
                    "Скопировать в буфер обмена?")
                if ans == QMessageBox.Yes:
                    QApplication.clipboard().setText(password)
            elif res_code is db.RegisterResult.USERNAME_EXISTS:
                self.ui.username_ln_edt.setFocus()
                QMessageBox.warning(self.parent(), "Телефонная книжка", "Пользователь с таким именем уже существует.")
            elif res_code is db.RegisterResult.EMAIL_EXISTS:
                self.ui.email_ln_edt.setFocus()
                QMessageBox.warning(self.parent(), "Телефонная книжка", "Пользователь с таким e-mail уже существует.")
            elif res_code is db.RegisterResult.UNKNOWN_ERROR:
                QMessageBox.critical(self.parent(), "Телефонная книжка", "Возникла непредвиденная ошибка.")
                self.close()
            else:
                raise RuntimeError("unknown member: {}".format(res_code))
        finally:
            self.ui.button_box.button(QDialogButtonBox.Ok).setEnabled(True)


class AuthForm(QDialog):
    def __init__(self, parent=None, remember_me=False):
        super().__init__(parent, Qt.FramelessWindowHint)
        self.ui = Ui_AuthForm()
        self.ui.setupUi(self)

        self.session_key = None
        self.username = None
        self.remember_me = remember_me

        self.ui.remember_me_chb.setChecked(self.remember_me)

        self.ui.login_btn.clicked.connect(self.handle_login_btn_clicked)
        self.ui.register_btn.clicked.connect(self.handle_register_button_clicked)
        self.ui.cancel_btn.clicked.connect(self.reject)
        self.ui.show_password_chb.clicked.connect(self.handle_show_password_chb_clicked)
        self.ui.remember_me_chb.clicked.connect(self.handle_remember_me_chb_clicked)
        self.ui.forgot_password_btn.clicked.connect(lambda: show_not_implemented_msg(self))

    def handle_login_btn_clicked(self):
        uname_or_email = self.ui.username_ln_edt.text()
        password = self.ui.password_ln_edt.text()
        # TODO: some input validaton
        try:
            self.ui.login_btn.setDisabled(True)
            session_key = db.log_in(uname_or_email, password)
            self.username, _ = db.get_user_info(session_key)
        except db.DatabaseConnectionError:
            show_db_conn_err_msg(self)
            self.close()
        else:
            if session_key:
                self.session_key = session_key
                self.accept()
            else:
                self.ui.password_ln_edt.setFocus()
                QMessageBox.warning(self, "Телефонная книжка",
                                    "Не удалось войти. Такая комбинация учетных данных не найдена.")
        finally:
            self.ui.login_btn.setEnabled(True)

    def handle_register_button_clicked(self):
        register_form = RegisterForm(parent=self.parent())
        self.hide()
        res = register_form.exec()
        if res == QDialog.Accepted:
            try:
                _, username, password = register_form.register_result
                session_key = db.log_in(username, password)
                self.username = username
            except db.DatabaseConnectionError:
                show_db_conn_err_msg(self.parent())
                self.close()
            else:
                if session_key:
                    self.session_key = session_key
                    self.accept()
                else:
                    self.close()
                    QMessageBox.warning(self.parent(), "Телефонная книжка", "Автоматический вход не удался.")
        else:
            # TODO: process a case when register form closed due to db connection error
            self.show()

    def handle_show_password_chb_clicked(self, chb_active):
        if chb_active:
            self.ui.password_ln_edt.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.password_ln_edt.setFocus()
        else:
            self.ui.password_ln_edt.setEchoMode(QLineEdit.EchoMode.Password)

    def handle_remember_me_chb_clicked(self, chb_active):
        self.remember_me = chb_active


class ContactsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ContactsPage()
        self.ui.setupUi(self)


class ContactDataForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint)
        self.ui = Ui_ContactDataForm()
        self.ui.setupUi(self)

        self.ui.button_box.rejected.connect(self.reject)

    @property
    def session_key(self):
        return self.parent().session_key


class AddContactForm(ContactDataForm):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.name = None
        self.add_result = None, None
        self.ui.button_box.accepted.connect(self.handle_ok_btn_clicked)

    def handle_ok_btn_clicked(self):
        name = self.ui.name_ln_edt.text()
        phone_number = self.ui.phone_number_ln_edt.text()
        birth_date = self.ui.birth_date_dt_edt.dateTime().toString("yyyy.MM.dd")
        # TODO: some input validaton

        try:
            self.ui.button_box.button(QDialogButtonBox.Ok).setDisabled(True)
            res_code, contact_id = db.add_contact(self.session_key, name, phone_number, birth_date)
        except db.DatabaseConnectionError:
            show_db_conn_err_msg(self)
            self.close()
        else:
            self.name = name
            self.add_result = (res_code, contact_id)
            self.accept()
        finally:
            self.ui.button_box.button(QDialogButtonBox.Ok).setEnabled(True)


class MainWindow(QMainWindow):
    auth_status_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.settings, self.default_settings = self.get_settings()

        self.session_key = self.read_session_key_from_storage()
        self.username = None
        self.contacts_model = None

        self.remember_me = False if self.session_key is None else True
        self.is_authenticated = False if self.session_key is None else None

        self.letter_sets = ("АБ", "ВГ", "ДЕЁ", "ЖЗИЙ", "КЛ", "МН", "ОП", "РС", "ТУ", "ФХ", "ЦЧШЩ", "ЪЫЬЭ", "ЮЯ")
        self.rest_contacts_page_name = "Другое"
        self.full_set = ''.join(self.letter_sets)
        self.contacts_model_view_tab_tab_visited = {}
        self.setup_tabs()

        self.ui.log_in_out_btn.clicked.connect(self.handle_log_in_out_btn_clicked)
        self.ui.settings_btn.clicked.connect(lambda: show_not_implemented_msg(self))
        self.auth_status_changed.connect(self.handle_auth_status_changed)
        self.ui.contacts_tab_widget.currentChanged.connect(self.handle_tab_changed)
        self.ui.add_contact_btn.clicked.connect(self.handle_add_contact_btn_clicked)

    @staticmethod
    def get_settings():
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "vista", "phone_book")
        def_settings_path = os.path.join(os.path.dirname(__file__), "phone_book_defaults.ini")
        default_settings = QSettings(def_settings_path, QSettings.IniFormat)
        return settings, default_settings

    def setup_tabs(self):
        tab_visited = False
        for letter_set in self.letter_sets + (self.rest_contacts_page_name,):
            tab = ContactsPage()
            view = tab.ui.tableView
            model = db.ContactsReadWriteModel(
                self,
                letter_set=letter_set if letter_set != self.rest_contacts_page_name else self.full_set,
                exclude=letter_set == self.rest_contacts_page_name)
            self.contacts_model_view_tab_tab_visited[letter_set] = (model, view, tab, tab_visited)
            view.setModel(model)
            view.hideColumn(0)
            self.ui.contacts_tab_widget.addTab(tab, letter_set)

    def read_session_key_from_storage(self):
        return self.settings.value("session_key")

    def write_session_key_to_storage(self):
        self.settings.setValue("session_key", self.session_key)
        self.settings.sync()

    def erase_session_key_from_storage(self):
        self.settings.remove("session_key")
        self.settings.sync()

    def restore_session_or_log_in(self):
        try:
            if self.session_key and db.check_session_exists(self.session_key):
                self.username, _ = db.get_user_info(self.session_key)
                self.is_authenticated = True
                self.auth_status_changed.emit()
                return
        except db.DatabaseConnectionError:
            show_db_conn_err_msg(self)
            return

        auth_form = AuthForm(parent=self, remember_me=self.remember_me)

        def on_finished(res):
            if res == QDialog.Accepted and auth_form.session_key:
                self.session_key = auth_form.session_key
                self.remember_me = auth_form.remember_me
                self.username = auth_form.username
                self.is_authenticated = True
                self.auth_status_changed.emit()

                if self.remember_me:
                    logger.debug("Requested to be remembered")
                    self.write_session_key_to_storage()

        auth_form.finished.connect(on_finished)
        auth_form.open()

    def log_out(self):
        self.erase_session_key_from_storage()
        self.session_key = None
        self.is_authenticated = False
        self.auth_status_changed.emit()
        try:
            db.log_out(self.session_key)
        except db.DatabaseConnectionError:
            # Not critical because a session_key is erased &
            # a database can delete it later on its own when it expires
            pass

    def refresh_contacts_page(self, tab_or_tab_idx):
        if isinstance(tab_or_tab_idx, int):
            idx = tab_or_tab_idx
        else:
            idx = self.ui.contacts_tab_widget.indexOf(tab_or_tab_idx)
        text = self.ui.contacts_tab_widget.tabText(idx)
        model, view, *_ = self.contacts_model_view_tab_tab_visited[text]
        model.refresh(self.session_key)
        view.hideColumn(0)
        # from PyQt5.QtWidgets import QTableView, QHeaderView
        # # view: QTableView
        # view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def clear_contacts_pages(self):
        for model, *_ in self.contacts_model_view_tab_tab_visited.values():
            model.clear()

    def handle_log_in_out_btn_clicked(self):
        if self.is_authenticated:
            self.log_out()
        else:
            self.restore_session_or_log_in()

    def handle_auth_status_changed(self):
        if self.is_authenticated:
            self.ui.label.setText("Вы вошли" + ("" if self.username is None else " как {}".format(self.username)))
            self.ui.log_in_out_btn.setText("Выйти")
            self.ui.add_contact_btn.setEnabled(True)
            self.refresh_contacts_page(self.ui.contacts_tab_widget.currentWidget())
        else:
            self.ui.label.setText("Вход не выполнен")
            self.ui.log_in_out_btn.setText("Войти")
            self.ui.add_contact_btn.setDisabled(True)
            self.clear_contacts_pages()

    def handle_tab_changed(self, idx):
        text = self.ui.contacts_tab_widget.tabText(idx)
        model, view, _, tab_visited = self.contacts_model_view_tab_tab_visited[text]
        if not tab_visited:
            model.refresh(self.session_key)
            view.hideColumn(0)

    def detect_page_where_contact_located(self, contact_name):
        first_letter = contact_name[0].upper()
        page_name = self.rest_contacts_page_name
        for letter_set in self.letter_sets:
            if first_letter in letter_set.upper():
                page_name = letter_set
                break
        *_, page, _ = self.contacts_model_view_tab_tab_visited[page_name]
        return page_name, page

    def handle_add_contact_btn_clicked(self):
        form = AddContactForm(self)

        def on_finished(res):
            if res == QDialog.Rejected:
                return

            contact_name = form.name
            res_code, _ = form.add_result

            if res_code is db.AddContactResult.SUCCESS:
                page_name, tab = self.detect_page_where_contact_located(contact_name)
                self.refresh_contacts_page(tab)

                if tab is self.ui.contacts_tab_widget.currentWidget():
                    QMessageBox.information(self, "Телефонная книжка", "Контакт успешно добавлен на текущую страницу.")
                else:
                    ans = QMessageBox.question(
                        self, "Телефонная книжка",
                        "Контакт добавлен успешно на страницу {}. Хотите перейти на неё?".format(page_name))
                    if ans == QMessageBox.Yes:
                        self.ui.contacts_tab_widget.setCurrentWidget(tab)

            elif res_code is db.AddContactResult.CONTACT_EXISTS:
                page_name, tab = self.detect_page_where_contact_located(contact_name)

                if tab is self.ui.contacts_tab_widget.currentWidget():
                    QMessageBox.warning(self, "Телефонная книжка",
                                        "Контакт уже существует. Он находится на текущей странице.")
                else:
                    ans = QMessageBox.warning(
                        self, "Телефонная книжка",
                        "Такой контакт уже существует. Он расположен на странице {}. ".format(page_name) +
                        "Хотите перейти на неё?",
                        buttons=QMessageBox.Yes | QMessageBox.No)
                    if ans == QMessageBox.Yes:
                        self.ui.contacts_tab_widget.setCurrentWidget(tab)

            elif res_code is db.AddContactResult.INVALID_SESSION:
                QMessageBox.warning(self, "Телефонная книжка", "Сессия истекла. Вам нужно войти заново.")
                self.log_out()
            elif res_code is db.AddContactResult.UNKNOWN_ERROR:
                QMessageBox.critical(self, "Телефонная книжка", "Возникла непредвиденная ошибка.")
            else:
                raise RuntimeError("unknown member: {}".format(res_code))

        form.finished.connect(on_finished)
        form.open()

    def setup_db(self):
        db.setup_db(self.settings, self.default_settings)

    def show(self):
        super().show()
        self.setup_db()
        self.restore_session_or_log_in()

    def closeEvent(self, event):
        self.hide()
        if not self.remember_me and self.is_authenticated:
            self.log_out()
        event.accept()


if __name__ == "__main__":
    # TODO: parse args to set a logger config for debug purposes
    logging.basicConfig()
    parent_logger = logging.getLogger("phone_book")
    parent_logger.setLevel(logging.DEBUG)
    file_handler = logging.handlers.RotatingFileHandler("log.txt", maxBytes=2 ** 19, backupCount=1)
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    parent_logger.addHandler(file_handler)

    sys._original_excepthook = sys.excepthook


    def exception_hook(exctype, value, traceback):
        logger.exception("Unexpected error", exc_info=value)
        sys._original_excepthook(exctype, value, traceback)
        msg_box = QMessageBox(QMessageBox.Critical, "Телефонная книжка",
                              "Неожиданная ошибка. Приложение будет закрыто.")
        msg_box.setDetailedText(str(value))
        msg_box.exec()
        sys.exit(1)

    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
