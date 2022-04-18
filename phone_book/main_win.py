import os.path
from functools import partial
from typing import Dict, Tuple

from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox

from . import database as db
from .contacts import AddContactForm, ContactsPage, DeleteContactDialog, EditContactForm, UpcomingBirthdaysDialog
from .msg_dialogs import show_db_conn_err_msg
from .reg_auth import AuthForm
from .settings_dialog import SettingsDialog, SettingsDialogFieldValues
from .ui import Ui_MainWindow


class MainWindow(QMainWindow):
    auth_status_changed = pyqtSignal()
    database_settings_changed = pyqtSignal()
    contact_edited = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.log_in_out_btn.clicked.connect(self.handle_log_in_out_btn_clicked)
        self.ui.settings_btn.clicked.connect(self.handle_settings_btn_clicked)
        self.ui.contacts_tab_widget.currentChanged.connect(self.handle_tab_changed)
        self.ui.add_contact_btn.clicked.connect(self.handle_add_contact_btn_clicked)
        self.ui.edit_contact_btn.clicked.connect(self.handle_edit_contact_btn_clicked)
        self.ui.delete_contact_btn.clicked.connect(self.handle_delete_contact_btn_clicked)

        self.auth_status_changed.connect(self.handle_auth_status_changed)
        self.database_settings_changed.connect(self.handle_database_settings_changed)

        self.settings, self.default_settings = self.get_settings()
        if self.settings is self.default_settings:
            raise RuntimeError

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

    def handle_contact_selection_changed(self, page_where_changed: ContactsPage):
        if page_where_changed is self.ui.contacts_tab_widget.currentWidget():
            is_selection_empty = page_where_changed.is_selection_empty()
            self.ui.edit_contact_btn.setDisabled(is_selection_empty)
            self.ui.delete_contact_btn.setDisabled(is_selection_empty)

    def setup_tabs(self):
        for letter_set in self.letter_sets + (self.rest_contacts_page_name,):
            model = db.ContactsPageReadWriteModel(
                letter_set=letter_set if letter_set != self.rest_contacts_page_name else self.full_letter_set,
                exclude=letter_set == self.rest_contacts_page_name, parent=self)
            tab = ContactsPage(model)
            tab.contact_selection_changed.connect(partial(self.handle_contact_selection_changed, tab))
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

    def welcome_if_first_run(self):
        key = "first_run"
        type_ = bool
        def_val = self.default_settings.value(key, True, type_)
        is_first_run = self.settings.value(key, def_val, type_)
        is_show_settings = False
        if is_first_run:
            r = QMessageBox.question(self, "Телефонная книжка",
                                     "Добро пожаловать!\n\nХотите проверить настройки перед началом работы?")
            self.settings.setValue(key, False)
            if r == QMessageBox.Yes:
                is_show_settings = True
        return is_show_settings

    def show(self):
        super().show()
        self.setup_db()
        if self.welcome_if_first_run():
            self.show_settings_dialog(self.restore_session_or_log_in)
        else:
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
        except db.DatabaseConnectionError as exc:
            show_db_conn_err_msg(details=str(exc), parent=self)
            return

        form = AuthForm(self.remember_me, parent=self)
        form.finished.connect(partial(self.on_auth_form_finished, form))
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
            self.show_birthdays_if_any()
            self.ui.add_contact_btn.setEnabled(True)
            self.ui.contacts_tab_widget.currentWidget().refresh_data(self.session_key)
        else:
            self.ui.label.setText("Вход не выполнен")
            self.ui.log_in_out_btn.setText("Войти")
            self.ui.add_contact_btn.setDisabled(True)
            self.clear_contacts_pages()

    def handle_database_settings_changed(self):
        if self.is_authenticated:
            self.log_out()
            QMessageBox.information(self, "Телефонная книжка", "Настройки подключения к базе данных изменены.\n"
                                                               "Вам придется войти заново.")
        self.setup_db()

    def clear_contacts_pages(self):
        tab_widget = self.ui.contacts_tab_widget
        for idx in range(tab_widget.count()):
            page: ContactsPage = tab_widget.widget(idx)
            page.clear_data()

    def handle_tab_changed(self, idx):
        page: ContactsPage = self.ui.contacts_tab_widget.widget(idx)

        is_selection_empty = page.is_selection_empty()
        self.ui.edit_contact_btn.setDisabled(is_selection_empty)
        self.ui.delete_contact_btn.setDisabled(is_selection_empty)

        if self.is_authenticated and not page.is_data_fetched:
            try:
                page.fetch_data_first_time(self.session_key)
            except db.DatabaseConnectionError as exc:
                show_db_conn_err_msg(details=str(exc), parent=self)
                self.close()

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
        page: ContactsPage = self.ui.contacts_tab_widget.currentWidget()
        cb = partial(page.model.add_contact, self.session_key)
        form = AddContactForm(cb, parent=self)
        form.finished.connect(partial(self.on_add_contact_form_finished, form))
        form.open()

    def on_edit_contact_form_finished(self, form: EditContactForm, r: QDialog.DialogCode):
        if r == QDialog.Rejected:
            return

        res_code, contact_new_name = form.result.code, form.result.contact_new_name

        if res_code is db.EditContactResult.SUCCESS:
            page_name, page = self.detect_page_where_contact_located(contact_new_name)
            current_page = self.ui.contacts_tab_widget.currentWidget()
            current_page.refresh_data(self.session_key)
            if current_page is not page:
                page.refresh_data(self.session_key)

            if page is current_page:
                QMessageBox.information(self, "Телефонная книжка", "Контакт отредактирован.")
            else:
                ans = QMessageBox.question(
                    self, "Телефонная книжка",
                    "Контакт отредактирован и перенесен на страницу {}. Хотите перейти на неё?".format(page_name))
                if ans == QMessageBox.Yes:
                    self.ui.contacts_tab_widget.setCurrentWidget(page)

        elif res_code is db.EditContactResult.SAME_DATA_CONTACT_EXISTS:
            page_name, page = self.detect_page_where_contact_located(contact_new_name)
            current_page = self.ui.contacts_tab_widget.currentWidget()

            if page is current_page:
                QMessageBox.warning(self, "Телефонная книжка",
                                    "Контакт с такими данными уже существует.\nОн находится на текущей странице.")
            else:
                ans = QMessageBox.warning(
                    self, "Телефонная книжка",
                    "Контакт с такими данными уже существует.\n"
                    "Он расположен на странице {}. ".format(page_name) + "Хотите перейти на неё?",
                    buttons=QMessageBox.Yes | QMessageBox.No)
                if ans == QMessageBox.Yes:
                    self.ui.contacts_tab_widget.setCurrentWidget(page)

        elif res_code is db.EditContactResult.CONTACT_DOESNT_EXIST:
            QMessageBox.warning(self, "Телефонная книжка", "Не удалось отредактировать: контакт не существует.")
        elif res_code is db.EditContactResult.NO_AUTHORITY_TO_EDIT_CONTACT:
            QMessageBox.warning(self, "Телефонная книжка", "У вас нет прав на редактирование данного контакта.")
        elif res_code is db.EditContactResult.INVALID_SESSION:
            QMessageBox.warning(self, "Телефонная книжка", "Сессия истекла. Вам нужно войти заново.")
            self.log_out()
        elif res_code is db.EditContactResult.UNKNOWN_ERROR:
            QMessageBox.critical(self, "Телефонная книжка", "Возникла непредвиденная ошибка.")
        else:
            raise RuntimeError("unknown member: {}".format(res_code))

    def _get_contacts_page_selected_row_idx(self, page: ContactsPage) -> int:
        rows = set(idx.row() for idx in page.view.selectedIndexes())
        if len(rows) > 1:
            raise RuntimeError(
                "for `page.view` expected: "
                "1) `selectionMode` property to be `QTableView.SingleSelection`; "
                "2) `selectionBehavior` property to be `QTableView.SelectRows`")
        elif len(rows) == 0:
            raise RuntimeError("no rows selected")
        return rows.pop()

    def handle_edit_contact_btn_clicked(self):
        page: ContactsPage = self.ui.contacts_tab_widget.currentWidget()
        contact_row_idx = self._get_contacts_page_selected_row_idx(page)
        data = page.model.get_contact_data(contact_row_idx)
        cb = partial(page.model.edit_contact, self.session_key, contact_row_idx)
        form = EditContactForm(cb, data.name, data.phone_number, data.birth_date, parent=self)
        form.finished.connect(partial(self.on_edit_contact_form_finished, form))
        form.open()

    def on_delete_contact_form_finished(self, form: DeleteContactDialog, r: QDialog.DialogCode):
        if r == QDialog.Rejected:
            return

        res_code = form.result.code

        if res_code is db.DeleteContactResult.SUCCESS:
            current_page = self.ui.contacts_tab_widget.currentWidget()
            current_page.refresh_data(self.session_key)
            QMessageBox.information(self, "Телефонная книжка", "Контакт успешно удален.")
        elif res_code is db.DeleteContactResult.CONTACT_DOESNT_EXIST:
            QMessageBox.warning(self, "Телефонная книжка", "Не удалось удалить: контакт уже не существует.")
        elif res_code is db.DeleteContactResult.NO_AUTHORITY_TO_DELETE_CONTACT:
            QMessageBox.warning(self, "Телефонная книжка", "У вас нет прав на удаление данного контакта.")
        elif res_code is db.DeleteContactResult.INVALID_SESSION:
            QMessageBox.warning(self, "Телефонная книжка", "Сессия истекла. Вам нужно войти заново.")
            self.log_out()
        elif res_code is db.DeleteContactResult.UNKNOWN_ERROR:
            QMessageBox.critical(self, "Телефонная книжка", "Возникла непредвиденная ошибка.")
        else:
            raise RuntimeError("unknown member: {}".format(res_code))

    def handle_delete_contact_btn_clicked(self):
        page: ContactsPage = self.ui.contacts_tab_widget.currentWidget()
        contact_row_idx = self._get_contacts_page_selected_row_idx(page)
        cb = partial(page.model.delete_contact, self.session_key, contact_row_idx)
        form = DeleteContactDialog(cb, parent=self)
        form.finished.connect(partial(self.on_delete_contact_form_finished, form))
        form.open()

    def show_birthdays_if_any(self):
        key = "notifications/birthdays/turned_on"
        type_ = bool
        def_val = self.default_settings.value(key, True, type_)
        if not self.settings.value(key, def_val, type_):
            return

        key = "notifications/birthdays/range/type"
        type_ = str
        def_val = self.default_settings.value(key, "day", type_)
        range_type = self.settings.value(key, def_val, type_)

        key = "notifications/birthdays/range/value"
        type_ = int
        def_val = self.default_settings.value(key, 7, type_)
        range_value = self.settings.value(key, def_val, type_)

        model = db.UpcomingBirthdaysReadModel(range_type, range_value, parent=self)
        dialog = UpcomingBirthdaysDialog(model, parent=self)
        dialog.refresh_data(self.session_key)
        if dialog.model.rowCount() > 0:
            dialog.view.resizeColumnsToContents()

            # dialog.adjustSize() <- this doesn't work although sizePolicy is set to Expanding,
            # so have to use a kludge adopted from SO:
            dialog.resizeWindowToColumns()

            dialog.show()

    def _get_settings_dialog_fields_values(self, defaults=False) -> SettingsDialogFieldValues:
        result = {}
        self.settings.beginGroup("database")
        self.default_settings.beginGroup("database")
        try:
            for key in ("host_name", "port", "database_name", "username", "password", "qsql_driver"):
                type_ = int if key == "port" else str
                def_val = self.default_settings.value(key, type=type_)
                result[key] = self.settings.value(key, def_val, type_) if not defaults else def_val
        finally:
            self.settings.endGroup()
            self.default_settings.endGroup()

        key = "notifications/birthdays/turned_on"
        type_ = bool
        def_val = self.default_settings.value(key, True, type_)
        result[key.replace("/", "_")] = self.settings.value(key, def_val, type_) if not defaults else def_val

        key = "notifications/birthdays/range/value"
        type_ = int
        def_val = self.default_settings.value(key, 7, type_)
        result[key.replace("/", "_")] = self.settings.value(key, def_val, type_) if not defaults else def_val

        return SettingsDialogFieldValues(**result)

    def set_settings(self, values: SettingsDialogFieldValues):
        is_db_settings_changed = False
        is_settings_changed = False
        new_settings = values._asdict()

        try:
            self.settings.beginGroup("database")
            self.default_settings.beginGroup("database")
            try:
                for key in ("host_name", "port", "database_name", "username", "password", "qsql_driver"):
                    type_ = int if key == "port" else str
                    new_val = new_settings[key]
                    def_val = self.default_settings.value(key, type=type_)
                    cur_val = self.settings.value(key, def_val, type_)
                    if new_val != cur_val:
                        is_settings_changed = is_db_settings_changed = True
                        if new_val != def_val:
                            self.settings.setValue(key, new_val)
                        else:
                            self.settings.remove(key)
            finally:
                self.settings.endGroup()
                self.default_settings.endGroup()

            for key, type_ in (("notifications/birthdays/turned_on", bool),
                               ("notifications/birthdays/range/value", int)):
                new_val = new_settings[key.replace("/", "_")]
                def_val = self.default_settings.value(key, True, type_)
                cur_val = self.settings.value(key, def_val, type_)
                if new_val != cur_val:
                    is_settings_changed = True
                    if new_val != def_val:
                        self.settings.setValue(key, new_val)
                    else:
                        self.settings.remove(key)
        finally:
            if is_settings_changed:
                self.settings.sync()
            if is_db_settings_changed:
                self.database_settings_changed.emit()

    def on_settings_dialog_finished(self, initial_values, dialog: SettingsDialog, r: QDialog.DialogCode):
        if r == QDialog.Rejected or not dialog.result.changed_settings_saving_requested:
            return
        if dialog.result.field_values != initial_values:
            self.set_settings(dialog.result.field_values)

    @staticmethod
    def _setting_dialog_check_db_connection_cb(settings_values: SettingsDialogFieldValues):
        filtered = dict([(key, value) for (key, value) in settings_values._asdict().items() if
                         key in ("host_name", "port", "database_name", "username", "password", "qsql_driver")])
        return db.check_db_connection_settings(**filtered)

    def _setup_settings_dialog(self):
        initial_values = self._get_settings_dialog_fields_values()
        dialog = SettingsDialog(initial_field_values=initial_values,
                                get_defaults_cb=partial(self._get_settings_dialog_fields_values, defaults=True),
                                check_db_connection_cb=self._setting_dialog_check_db_connection_cb,
                                parent=self)
        dialog.finished.connect(partial(self.on_settings_dialog_finished, initial_values, dialog))
        return dialog

    def show_settings_dialog(self, on_finished_cb=None):
        dialog = self._setup_settings_dialog()
        if on_finished_cb is not None:
            dialog.finished.connect(on_finished_cb)
        dialog.open()

    def handle_settings_btn_clicked(self):
        self._setup_settings_dialog().open()
