from PyQt5 import QtCore
from PyQt5.QtWidgets import QHeaderView

from . import contact_data_form, contacts_page, register_form
from .auth_form import Ui_AuthForm
from .contact_data_form import Ui_ContactDataForm
from .main_window import Ui_MainWindow


class Ui_RegisterForm(register_form.Ui_RegisterForm):
    def setupUi(self, RegisterForm):
        super().setupUi(RegisterForm)
        self.birth_date_dt_edt.setMaximumDate(QtCore.QDate.currentDate().addYears(-16))
        self.username_ln_edt.setFocus()


class Ui_ContactDataForm(contact_data_form.Ui_ContactDataForm):
    def setupUi(self, ContactDataForm):
        super().setupUi(ContactDataForm)
        self.name_ln_edt.setFocus()


class Ui_ContactsPage(contacts_page.Ui_ContactsPage):
    def setupUi(self, ContactsPage):
        super().setupUi(ContactsPage)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
