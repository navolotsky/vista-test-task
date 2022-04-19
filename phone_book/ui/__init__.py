from PyQt5.QtCore import QDate, QRegularExpression
from PyQt5.QtGui import QIntValidator, QPalette, QRegularExpressionValidator
from PyQt5.QtWidgets import QHeaderView

from . import auth_form, contact_data_form, contacts_page, register_form, settings_dialog, upcoming_birthdays_dialog
from .delete_contact_dialog import Ui_DeleteContactDialog
from .main_window import Ui_MainWindow
from ..input_validation import InputValidationHighlighterMixin


class Ui_AuthForm(auth_form.Ui_AuthForm, InputValidationHighlighterMixin):
    def setupUi(self, AuthForm):
        super().setupUi(AuthForm)

        # Just forbid an empty string:
        rx = QRegularExpression(".{1,}")
        if not rx.isValid():
            raise ValueError(rx.errorString())
        self.username_ln_edt.setValidator(QRegularExpressionValidator(rx, self.username_ln_edt))
        self.password_ln_edt.setValidator(QRegularExpressionValidator(rx, self.password_ln_edt))

        self.setup_highlighting()


class Ui_RegisterForm(register_form.Ui_RegisterForm, InputValidationHighlighterMixin):
    def setupUi(self, RegisterForm):
        super().setupUi(RegisterForm)
        self.birth_date_dt_edt.setMaximumDate(QDate.currentDate().addYears(-16))
        self.username_ln_edt.setFocus()

        rx = QRegularExpression(".{1,255}")
        if not rx.isValid():
            raise ValueError(rx.errorString())
        self.username_ln_edt.setValidator(QRegularExpressionValidator(rx, self.username_ln_edt))
        self.username_ln_edt.setToolTip("Любая строка от 1 до 255 символов.")

        # adopted from https://emailregex.com
        rx = QRegularExpression(
            r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
        )
        if not rx.isValid():
            raise ValueError(rx.errorString())
        self.email_ln_edt.setValidator(QRegularExpressionValidator(rx, self.email_ln_edt))

        self.setup_highlighting()


class Ui_ContactDataForm(contact_data_form.Ui_ContactDataForm, InputValidationHighlighterMixin):
    def setupUi(self, ContactDataForm):
        super().setupUi(ContactDataForm)
        self.birth_date_dt_edt.setMaximumDate(QDate.currentDate())
        self.name_ln_edt.setFocus()

        rx = QRegularExpression(".{1,255}")
        if not rx.isValid():
            raise ValueError(rx.errorString())
        self.name_ln_edt.setValidator(QRegularExpressionValidator(rx, self.name_ln_edt))
        self.name_ln_edt.setToolTip("Любая строка от 1 до 255 символов.")

        # adopted (Russia version) from https://phoneregex.com
        rx = QRegularExpression(r"^((\+7|7|8)+([0-9]){10})$")
        if not rx.isValid():
            raise ValueError(rx.errorString())
        self.phone_number_ln_edt.setValidator(QRegularExpressionValidator(rx, self.phone_number_ln_edt))

        self.setup_highlighting()


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


class Ui_SettingsDialog(settings_dialog.Ui_SettingsDialog, InputValidationHighlighterMixin):
    def setupUi(self, ContactsPage):
        super().setupUi(ContactsPage)

        rx = QRegularExpression(".{1,}")
        if not rx.isValid():
            raise ValueError(rx.errorString())
        self.host_name_ln_edt.setValidator(QRegularExpressionValidator(rx, self.host_name_ln_edt))
        self.database_name_ln_edt.setValidator(QRegularExpressionValidator(rx, self.database_name_ln_edt))
        self.username_ln_edt.setValidator(QRegularExpressionValidator(rx, self.username_ln_edt))
        self.password_ln_edt.setValidator(QRegularExpressionValidator(rx, self.password_ln_edt))

        min_, max_ = 0, 2 ** 16 - 1
        self.port_ln_edt.setValidator(QIntValidator(min_, max_, self.port_ln_edt))
        self.port_ln_edt.setToolTip("Целое число от {} до {}.".format(min_, max_))

        self.setup_highlighting()
