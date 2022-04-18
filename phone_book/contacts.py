from types import SimpleNamespace
from typing import Callable

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QStyle, QWidget

from . import database as db
from .msg_dialogs import show_db_conn_err_msg
from .ui import Ui_ContactDataForm, Ui_ContactsPage, Ui_DeleteContactDialog, Ui_UpcomingBirthdaysDialog


class ContactsPage(QWidget):
    contact_selection_changed = pyqtSignal()

    def __init__(self, model: db.ContactsPageReadWriteModel, parent=None):
        super().__init__(parent)
        self.ui = Ui_ContactsPage()
        self.ui.setupUi(self)

        self.model = model
        self.view.setModel(model)
        self.view.selectionModel().selectionChanged.connect(self.contact_selection_changed.emit)
        self.is_data_fetched = False

    @property
    def view(self):
        return self.ui.tableView

    def is_selection_empty(self):
        return not self.view.selectionModel().hasSelection()

    def refresh_data(self, session_key):
        self.view.selectionModel().clearSelection()
        self.model.refresh(session_key)
        self.view.hideColumn(0)

    def fetch_data_first_time(self, session_key):
        self.refresh_data(session_key)
        self.is_data_fetched = True

    def clear_data(self):
        self.view.selectionModel().clearSelection()
        self.model.clear()
        self.is_data_fetched = False


class ContactDataForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint)
        self.ui = Ui_ContactDataForm()
        self.ui.setupUi(self)
        self.ui.button_box.rejected.connect(self.reject)


class AddContactForm(ContactDataForm):
    def __init__(self, add_contact_cb: Callable, parent=None):
        super().__init__(parent)
        self.ui.button_box.accepted.connect(self.handle_ok_btn_clicked)

        self.add_contact_cb = add_contact_cb
        self.result = SimpleNamespace(code=None, contact_id=None, contact_name=None)

    def handle_ok_btn_clicked(self):
        name = self.ui.name_ln_edt.text()
        phone_number = self.ui.phone_number_ln_edt.text()
        birth_date = self.ui.birth_date_dt_edt.date().toString("yyyy.MM.dd")
        # TODO: some input validation
        try:
            self.ui.button_box.button(QDialogButtonBox.Ok).setDisabled(True)
            self.result.code, self.result.contact_id = self.add_contact_cb(name, phone_number, birth_date)
        except db.DatabaseConnectionError as exc:
            show_db_conn_err_msg(details=str(exc), parent=self)
            self.close()
        else:
            self.result.contact_name = name
            self.accept()
        finally:
            self.ui.button_box.button(QDialogButtonBox.Ok).setEnabled(True)


class EditContactForm(ContactDataForm):
    def __init__(self, edit_contact_cb: Callable, name, phone_number, birth_date, parent=None):
        super().__init__(parent)
        self.ui.button_box.accepted.connect(self.handle_ok_btn_clicked)
        self.ui.name_ln_edt.setText(name)
        self.ui.phone_number_ln_edt.setText(phone_number)
        self.ui.birth_date_dt_edt.setDate(birth_date)

        self.original_input_data = name, phone_number, birth_date
        self.edit_contact_cb = edit_contact_cb
        self.result = SimpleNamespace(code=None, contact_new_name=None, same_data_contact_id=None)

    def handle_ok_btn_clicked(self):
        # TODO: some input validation
        name = self.ui.name_ln_edt.text()
        phone_number = self.ui.phone_number_ln_edt.text()
        birth_date = self.ui.birth_date_dt_edt.date()

        if (name, phone_number, birth_date) == self.original_input_data:
            self.reject()  # data didn't change so let's interpret Ok as a synonym for Cancel at this case
            return

        birth_date = birth_date.toString("yyyy.MM.dd")
        try:
            self.ui.button_box.button(QDialogButtonBox.Ok).setDisabled(True)
            self.result.code, self.result.same_data_contact_id = self.edit_contact_cb(name, phone_number, birth_date)
        except db.DatabaseConnectionError as exc:
            show_db_conn_err_msg(details=str(exc), parent=self)
            self.close()  # Unfortunately, a user will have to fill a form again
        else:
            self.result.contact_new_name = name
            self.accept()
        finally:
            self.ui.button_box.button(QDialogButtonBox.Ok).setEnabled(True)


class DeleteContactDialog(QDialog):
    def __init__(self, delete_contact_cb: Callable, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint)
        self.ui = Ui_DeleteContactDialog()
        self.ui.setupUi(self)
        self.ui.button_box.rejected.connect(self.reject)
        self.ui.button_box.accepted.connect(self.handle_ok_btn_clicked)

        self.delete_contact_cb = delete_contact_cb
        self.result = SimpleNamespace(code=None)

    def handle_ok_btn_clicked(self):
        try:
            self.ui.button_box.button(QDialogButtonBox.Ok).setDisabled(True)
            self.result.code = self.delete_contact_cb()
        except db.DatabaseConnectionError as exc:
            show_db_conn_err_msg(details=str(exc), parent=self)
            self.close()
        else:
            self.accept()
        finally:
            self.ui.button_box.button(QDialogButtonBox.Ok).setEnabled(True)


class UpcomingBirthdaysDialog(QDialog):
    def __init__(self, model: db.UpcomingBirthdaysReadModel, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint)
        self.ui = Ui_UpcomingBirthdaysDialog()
        self.ui.setupUi(self)
        self.ui.button_box.rejected.connect(self.reject)
        self.ui.button_box.accepted.connect(self.accept)

        self.model = model
        self.view.setModel(model)

    def resizeWindowToColumns(self):
        """adopted from https://stackoverflow.com/a/26960463"""
        margins = self.layout().contentsMargins()
        self.resize((
                margins.left() + margins.right() +
                self.view.frameWidth() * 2 +
                self.view.verticalHeader().width() +
                self.view.horizontalHeader().length() +
                self.view.style().pixelMetric(QStyle.PM_ScrollBarExtent)
        ), self.height())

    @property
    def view(self):
        return self.ui.tableView

    def refresh_data(self, session_key):
        self.model.refresh(session_key)
        self.view.hideColumn(0)
