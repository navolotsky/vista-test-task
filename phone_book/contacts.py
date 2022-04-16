from types import SimpleNamespace

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QWidget

from . import database as db
from .msg_dialogs import show_db_conn_err_msg
from .ui import Ui_ContactDataForm, Ui_ContactsPage


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
