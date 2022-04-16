import logging.handlers
import os.path
import sys
from types import SimpleNamespace
from typing import Dict, Tuple

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
        self.ui.button_box.rejected.connect(self.reject)
        self.ui.button_box.accepted.connect(self.handle_ok_btn_clicked)

        self.result = SimpleNamespace(code=None, username=None, password=None)

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
            self.result.code, self.result.username, self.result.password = res_code, username, password
            if res_code is db.RegisterResult.SUCCESS:
                self.accept()
                # TODO: send a password by an email
                ans = QMessageBox.question(
                    self, "Телефонная книжка",
                    "Регистрация успешна.\n"
                    "Ваш пароль выслан [! не реализовано] на указанную почту.\n"
                    "Скопировать в буфер обмена?")
                if ans == QMessageBox.Yes:
                    QApplication.clipboard().setText(password)
            elif res_code is db.RegisterResult.USERNAME_EXISTS:
                self.ui.username_ln_edt.setFocus()
                QMessageBox.warning(self, "Телефонная книжка", "Пользователь с таким именем уже существует.")
            elif res_code is db.RegisterResult.EMAIL_EXISTS:
                self.ui.email_ln_edt.setFocus()
                QMessageBox.warning(self, "Телефонная книжка", "Пользователь с таким e-mail уже существует.")
            elif res_code is db.RegisterResult.UNKNOWN_ERROR:
                QMessageBox.critical(self, "Телефонная книжка", "Возникла непредвиденная ошибка.")
                self.close()
            else:
                raise RuntimeError("unknown member: {}".format(res_code))
        finally:
            self.ui.button_box.button(QDialogButtonBox.Ok).setEnabled(True)


class AuthForm(QDialog):
    def __init__(self, remember_me=False, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint)
        self.ui = Ui_AuthForm()
        self.ui.setupUi(self)
        self.ui.login_btn.clicked.connect(self.handle_login_btn_clicked)
        self.ui.register_btn.clicked.connect(self.handle_register_button_clicked)
        self.ui.cancel_btn.clicked.connect(self.reject)
        self.ui.show_password_chb.clicked.connect(self.handle_show_password_chb_clicked)
        self.ui.remember_me_chb.clicked.connect(self.handle_remember_me_chb_clicked)
        self.ui.forgot_password_btn.clicked.connect(lambda: show_not_implemented_msg(self))

        self.result = SimpleNamespace(session_key=None, username=None, remember_me=remember_me)

        self.ui.remember_me_chb.setChecked(self.result.remember_me)

    def handle_login_btn_clicked(self):
        uname_or_email = self.ui.username_ln_edt.text()
        password = self.ui.password_ln_edt.text()
        # TODO: some input validaton
        try:
            self.ui.login_btn.setDisabled(True)
            session_key = db.log_in(uname_or_email, password)
            self.result.username, _ = db.get_user_info(session_key)
        except db.DatabaseConnectionError:
            show_db_conn_err_msg(self)
            self.close()
        else:
            if session_key:
                self.result.session_key = session_key
                self.accept()
            else:
                self.ui.password_ln_edt.setFocus()
                QMessageBox.warning(self, "Телефонная книжка",
                                    "Не удалось войти. Такая комбинация учетных данных не найдена.")
        finally:
            self.ui.login_btn.setEnabled(True)

    def on_register_form_finished(self, form: RegisterForm, r: QDialog.DialogCode):
        if r == QDialog.Accepted:
            try:
                session_key = db.log_in(form.result.username, form.result.password)
                self.result.username = form.result.username
            except db.DatabaseConnectionError:
                show_db_conn_err_msg(self.parent())
                self.close()
            else:
                if session_key:
                    self.result.session_key = session_key
                    self.accept()
                else:
                    self.close()
                    QMessageBox.warning(self.parent(), "Телефонная книжка", "Автоматический вход не удался.")
        else:
            # TODO: process a case when register form closed due to db connection error
            self.show()

    def handle_register_button_clicked(self):
        form = RegisterForm(parent=self.parent())
        self.hide()
        form.finished.connect(lambda r: self.on_register_form_finished(form, r))
        form.open()

    def handle_show_password_chb_clicked(self, chb_active):
        if chb_active:
            self.ui.password_ln_edt.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.password_ln_edt.setFocus()
        else:
            self.ui.password_ln_edt.setEchoMode(QLineEdit.EchoMode.Password)

    def handle_remember_me_chb_clicked(self, chb_active):
        self.result.remember_me = chb_active


class ContactsPage(QWidget):
    contact_selected = pyqtSignal()

    def __init__(self, model: db.ContactsReadWriteModel, parent=None):
        super().__init__(parent)
        self.ui = Ui_ContactsPage()
        self.ui.setupUi(self)
        self.ui.tableView.clicked.connect(self.contact_selected.emit)

        self.model = model
        self.view.setModel(model)
        self.is_data_fetched = False

    @property
    def view(self):
        return self.ui.tableView

    def refresh_data(self, session_key):
        self.model.refresh(session_key)
        self.view.hideColumn(0)

    def fetch_data_first_time(self, session_key):
        self.refresh_data(session_key)
        self.is_data_fetched = True

    def clear_data(self):
        self.model.clear()
        self.is_data_fetched = False


class ContactDataForm(QDialog):
    def __init__(self, session_key, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint)
        self.ui = Ui_ContactDataForm()
        self.ui.setupUi(self)
        self.ui.button_box.rejected.connect(self.reject)

        self.session_key = session_key


class AddContactForm(ContactDataForm):
    def __init__(self, session_key, parent=None):
        super().__init__(session_key, parent)
        self.ui.button_box.accepted.connect(self.handle_ok_btn_clicked)

        self.result = SimpleNamespace(code=None, contact_id=None, contact_name=None)

    def handle_ok_btn_clicked(self):
        name = self.ui.name_ln_edt.text()
        phone_number = self.ui.phone_number_ln_edt.text()
        birth_date = self.ui.birth_date_dt_edt.dateTime().toString("yyyy.MM.dd")
        # TODO: some input validaton
        try:
            self.ui.button_box.button(QDialogButtonBox.Ok).setDisabled(True)
            self.result.code, self.result.contact_id = db.add_contact(self.session_key, name, phone_number, birth_date)
        except db.DatabaseConnectionError:
            show_db_conn_err_msg(self)
            self.close()
        else:
            self.result.contact_name = name
            self.accept()
        finally:
            self.ui.button_box.button(QDialogButtonBox.Ok).setEnabled(True)


class MainWindow(QMainWindow):
    auth_status_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.log_in_out_btn.clicked.connect(self.handle_log_in_out_btn_clicked)
        self.ui.settings_btn.clicked.connect(lambda: show_not_implemented_msg(self))
        self.ui.contacts_tab_widget.currentChanged.connect(self.handle_tab_changed)
        self.ui.add_contact_btn.clicked.connect(self.handle_add_contact_btn_clicked)

        self.auth_status_changed.connect(self.handle_auth_status_changed)

        self.settings, self.default_settings = self.get_settings()

        self.session_key = self.read_session_key_from_storage()
        self.username = None

        self.remember_me = False if self.session_key is None else True
        self.is_authenticated = False if self.session_key is None else None

        self.letter_sets = ("АБ", "ВГ", "ДЕЁ", "ЖЗИЙ", "КЛ", "МН", "ОП", "РС", "ТУ", "ФХ", "ЦЧШЩ", "ЪЫЬЭ", "ЮЯ")
        self.rest_contacts_page_name = "Другое"
        self.full_letter_set = ''.join(self.letter_sets)
        self.letter_set_to_contacts_page: Dict[str, ContactsPage] = {}
        self.setup_tabs()

    @staticmethod
    def get_settings():
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "vista", "phone_book")
        def_settings_path = os.path.join(os.path.dirname(__file__), "phone_book_defaults.ini")
        default_settings = QSettings(def_settings_path, QSettings.IniFormat)
        return settings, default_settings

    def setup_tabs(self):
        for letter_set in self.letter_sets + (self.rest_contacts_page_name,):
            model = db.ContactsReadWriteModel(
                self,
                letter_set=letter_set if letter_set != self.rest_contacts_page_name else self.full_letter_set,
                exclude=letter_set == self.rest_contacts_page_name)
            tab = ContactsPage(model)
            tab.contact_selected.connect(self.handle_contacts_table_row_clicked)
            self.letter_set_to_contacts_page[letter_set] = tab
            self.ui.contacts_tab_widget.addTab(tab, letter_set)

    def read_session_key_from_storage(self):
        return self.settings.value("session_key")

    def write_session_key_to_storage(self):
        self.settings.setValue("session_key", self.session_key)
        self.settings.sync()

    def erase_session_key_from_storage(self):
        self.settings.remove("session_key")
        self.settings.sync()

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

    def on_auth_form_finished(self, form: AuthForm, r: QDialog.DialogCode):
        if r == QDialog.Accepted and form.result.session_key:
            self.session_key = form.result.session_key
            self.remember_me = form.result.remember_me
            self.username = form.result.username
            self.is_authenticated = True
            self.auth_status_changed.emit()

            if self.remember_me:
                self.write_session_key_to_storage()

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

        form = AuthForm(self.remember_me, parent=self)
        form.finished.connect(lambda r: self.on_auth_form_finished(form, r))
        form.open()

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
            self.ui.contacts_tab_widget.currentWidget().refresh_data(self.session_key)
        else:
            self.ui.label.setText("Вход не выполнен")
            self.ui.log_in_out_btn.setText("Войти")
            self.ui.add_contact_btn.setDisabled(True)
            self.clear_contacts_pages()

    def clear_contacts_pages(self):
        tab_widget = self.ui.contacts_tab_widget
        for idx in range(tab_widget.count()):
            page: ContactsPage = tab_widget.widget(idx)
            page.clear_data()

    def handle_tab_changed(self, idx):
        self.ui.edit_contact_btn.setDisabled(True)
        self.ui.delete_contact_btn.setDisabled(True)

        page: ContactsPage = self.ui.contacts_tab_widget.widget(idx)
        if self.is_authenticated and not page.is_data_fetched:
            page.fetch_data_first_time(self.session_key)

    def detect_page_where_contact_located(self, contact_name: str) -> Tuple[str, ContactsPage]:
        first_letter = contact_name[0].upper()
        page_name = self.rest_contacts_page_name
        for letter_set in self.letter_sets:
            if first_letter in letter_set.upper():
                page_name = letter_set
                break
        page = self.letter_set_to_contacts_page[page_name]
        return page_name, page

    def on_add_contact_form_finished(self, form: AddContactForm, r: QDialog.DialogCode):
        if r == QDialog.Rejected:
            return

        res_code, contact_name = form.result.code, form.result.contact_name

        if res_code is db.AddContactResult.SUCCESS:
            page_name, tab = self.detect_page_where_contact_located(contact_name)
            tab.refresh_data(self.session_key)

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

    def handle_add_contact_btn_clicked(self):
        form = AddContactForm(self.session_key, parent=self)
        form.finished.connect(lambda r: self.on_add_contact_form_finished(form, r))
        form.open()

    def handle_contacts_table_row_clicked(self):
        self.ui.edit_contact_btn.setEnabled(True)
        self.ui.delete_contact_btn.setEnabled(True)


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
