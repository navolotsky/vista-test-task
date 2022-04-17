from PyQt5 import QtCore
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QHeaderView

from . import contact_data_form, contacts_page, register_form, upcoming_birthdays_dialog
from .auth_form import Ui_AuthForm
from .contact_data_form import Ui_ContactDataForm
from .delete_contact_dialog import Ui_DeleteContactDialog
from .main_window import Ui_MainWindow


class Ui_RegisterForm(register_form.Ui_RegisterForm):
    def setupUi(self, RegisterForm):
        super().setupUi(RegisterForm)
        self.birth_date_dt_edt.setMaximumDate(QtCore.QDate.currentDate().addYears(-16))
        self.username_ln_edt.setFocus()


class Ui_ContactDataForm(contact_data_form.Ui_ContactDataForm):
    def setupUi(self, ContactDataForm):
        super().setupUi(ContactDataForm)
        self.birth_date_dt_edt.setMaximumDate(QtCore.QDate.currentDate())
        self.name_ln_edt.setFocus()


class Ui_ContactsPage(contacts_page.Ui_ContactsPage):
    def setupUi(self, ContactsPage):
        super().setupUi(ContactsPage)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        pal = self.tableView.palette()
        pal.setColor(QPalette.Inactive, QPalette.Highlight, pal.color(QPalette.Active, QPalette.Highlight))
        pal.setColor(QPalette.Inactive, QPalette.HighlightedText, pal.color(QPalette.Active, QPalette.HighlightedText))
        self.tableView.setPalette(pal)


class Ui_UpcomingBirthdaysDialog(upcoming_birthdays_dialog.Ui_UpcomingBirthdaysDialog):
    def setupUi(self, ContactsPage):
        super().setupUi(ContactsPage)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
