import os.path
from typing import Dict, Tuple

from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox

from . import database as db
from .contacts import AddContactForm, ContactsPage
from .msg_dialogs import show_db_conn_err_msg, show_not_implemented_msg
from .reg_auth import AuthForm
from .ui import Ui_MainWindow


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
