from PyQt5 import QtCore

from . import contact_data_form, register_form
from .auth_form import Ui_AuthForm
from .contact_data_form import Ui_ContactDataForm
from .contacts_page import Ui_ContactsPage
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
