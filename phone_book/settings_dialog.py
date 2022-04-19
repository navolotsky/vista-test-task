from types import SimpleNamespace
from typing import Callable, NamedTuple, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QMessageBox

from .msg_dialogs import show_db_conn_err_msg, show_invalid_input_warning
from .ui import Ui_SettingsDialog


class SettingsDialogFieldValues(NamedTuple):
    host_name: str
    port: int
    database_name: str
    username: str
    password: str
    qsql_driver: str
    notifications_birthdays_turned_on: bool
    notifications_birthdays_range_value: int


class SettingsDialog(QDialog):
    # TODO: some input validation
    def __init__(self, initial_field_values: SettingsDialogFieldValues,
                 get_defaults_cb: Callable[[], SettingsDialogFieldValues],
                 check_db_connection_cb: Callable[[SettingsDialogFieldValues], Tuple[bool, str]],
                 parent=None):
        super().__init__(parent, Qt.FramelessWindowHint)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.ui.check_connection_btn.clicked.connect(self.handle_check_connection_btn_clicked)
        self.ui.birthdays_notification_chb.stateChanged.connect(self.handle_birthdays_notification_chb_state_changed)
        self.ui.button_box.clicked.connect(self.handle_button_box_btn_clicked)
        self.ui.button_box.accepted.connect(self.handle_button_box_accepted)
        self.ui.button_box.rejected.connect(self.handle_button_box_rejected)

        self.initial_field_values = initial_field_values
        self.get_defaults_cb = get_defaults_cb
        self.check_db_connection_cb = check_db_connection_cb
        self.result = SimpleNamespace(changed_settings_saving_requested=False, field_values=None)

        self._set_field_values(self.initial_field_values)

    def _set_field_values(self, values: SettingsDialogFieldValues):
        for line_edt, value in zip((self.ui.host_name_ln_edt, self.ui.port_ln_edt, self.ui.database_name_ln_edt,
                                    self.ui.username_ln_edt, self.ui.password_ln_edt, self.ui.qsql_driver_ln_edt),
                                   values):
            line_edt.setText(str(value))
        self.ui.birthdays_notification_chb.setChecked(values.notifications_birthdays_turned_on)
        self.ui.birthdays_notification_range_value_sb.setValue(values.notifications_birthdays_range_value)

    def _get_field_values(self):
        str_to_int_fields = (self.ui.port_ln_edt,)
        values = []
        for line_edt in (self.ui.host_name_ln_edt, self.ui.port_ln_edt, self.ui.database_name_ln_edt,
                         self.ui.username_ln_edt, self.ui.password_ln_edt, self.ui.qsql_driver_ln_edt):
            value = line_edt.text()
            if line_edt in str_to_int_fields:
                try:
                    value = int(value)
                except ValueError:
                    pass
            values.append(value)
        values.append(self.ui.birthdays_notification_chb.isChecked())
        values.append(self.ui.birthdays_notification_range_value_sb.value())
        return SettingsDialogFieldValues(*values)

    def handle_check_connection_btn_clicked(self):
        invalid_input_fields = self.ui.validate_and_highlight_all()
        if invalid_input_fields:
            show_invalid_input_warning(invalid_input_fields, highlighted=True, parent=self)
            return
        self.ui.check_connection_btn.setDisabled(True)
        QApplication.processEvents()
        try:
            conn_check = self.check_db_connection_cb(self._get_field_values())
            if not conn_check.is_error:
                QMessageBox.information(self, "Телефонная книжка", "Соединение установлено успешно.")
            else:
                msg_text = "Ошибка конфигурации." if conn_check.is_critical else "Не удалось соединиться."
                show_db_conn_err_msg(msg_text, details=conn_check.message, critical=conn_check.is_critical, parent=self)
        finally:
            self.ui.check_connection_btn.setEnabled(True)

    def handle_birthdays_notification_chb_state_changed(self, chb_active):
        self.ui.birthdays_notification_range_value_sb.setEnabled(chb_active)

    def handle_button_box_btn_clicked(self, button):
        if button == self.ui.button_box.button(QDialogButtonBox.RestoreDefaults):
            r = QMessageBox.question(self, "Телефонная книжка",
                                     "Вы уверены, что хотите установить настройки по умолчанию?")
            if r == QMessageBox.Yes:
                self._set_field_values(self.get_defaults_cb())
                self.ui.validate_and_highlight_all()

    def handle_button_box_accepted(self):
        invalid_input_fields = self.ui.validate_and_highlight_all()
        if invalid_input_fields:
            show_invalid_input_warning(invalid_input_fields, highlighted=True, parent=self)
            return

        self.result.field_values = values = self._get_field_values()
        self.result.changed_settings_saving_requested = values != self.initial_field_values
        self.accept()

    def handle_button_box_rejected(self):
        self.result.field_values = values = self._get_field_values()
        if values != self.initial_field_values:
            r = QMessageBox.question(self, "Телефонная книжка", "Сохранить изменения?",
                                     buttons=QMessageBox.Cancel | QMessageBox.Yes | QMessageBox.No)
            if r == QMessageBox.Yes:
                invalid_input_fields = self.ui.validate_and_highlight_all()
                if invalid_input_fields:
                    show_invalid_input_warning(invalid_input_fields, highlighted=True, parent=self)
                    return

                self.result.changed_settings_saving_requested = values != self.initial_field_values
                self.accept()
            elif r == QMessageBox.No:
                self.result.changed_settings_saving_requested = False
                self.reject()
        else:
            self.reject()
