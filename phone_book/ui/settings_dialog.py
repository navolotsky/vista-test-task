# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_designer/settings_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        SettingsDialog.resize(303, 384)
        SettingsDialog.setMinimumSize(QtCore.QSize(200, 200))
        SettingsDialog.setStyleSheet("#SettingsDialog {\n"
"    border-width: 2;\n"
"    border-radius: 5;\n"
"    border-style: solid;\n"
"    border-color: gray;\n"
"}\n"
"")
        self.gridLayout = QtWidgets.QGridLayout(SettingsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.database_connection_gb = QtWidgets.QGroupBox(SettingsDialog)
        self.database_connection_gb.setObjectName("database_connection_gb")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.database_connection_gb)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.host_name_ln_edt = QtWidgets.QLineEdit(self.database_connection_gb)
        self.host_name_ln_edt.setObjectName("host_name_ln_edt")
        self.verticalLayout_3.addWidget(self.host_name_ln_edt)
        self.port_ln_edt = QtWidgets.QLineEdit(self.database_connection_gb)
        self.port_ln_edt.setObjectName("port_ln_edt")
        self.verticalLayout_3.addWidget(self.port_ln_edt)
        self.database_name_ln_edt = QtWidgets.QLineEdit(self.database_connection_gb)
        self.database_name_ln_edt.setReadOnly(False)
        self.database_name_ln_edt.setObjectName("database_name_ln_edt")
        self.verticalLayout_3.addWidget(self.database_name_ln_edt)
        self.username_ln_edt = QtWidgets.QLineEdit(self.database_connection_gb)
        self.username_ln_edt.setObjectName("username_ln_edt")
        self.verticalLayout_3.addWidget(self.username_ln_edt)
        self.password_ln_edt = QtWidgets.QLineEdit(self.database_connection_gb)
        self.password_ln_edt.setObjectName("password_ln_edt")
        self.verticalLayout_3.addWidget(self.password_ln_edt)
        self.qsql_driver_ln_edt = QtWidgets.QLineEdit(self.database_connection_gb)
        self.qsql_driver_ln_edt.setReadOnly(True)
        self.qsql_driver_ln_edt.setObjectName("qsql_driver_ln_edt")
        self.verticalLayout_3.addWidget(self.qsql_driver_ln_edt)
        self.check_connection_btn = QtWidgets.QPushButton(self.database_connection_gb)
        self.check_connection_btn.setObjectName("check_connection_btn")
        self.verticalLayout_3.addWidget(self.check_connection_btn)
        self.gridLayout.addWidget(self.database_connection_gb, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(SettingsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.button_box = QtWidgets.QDialogButtonBox(SettingsDialog)
        self.button_box.setStyleSheet("QDialogButtonBox *[text=\"OK\"] {\n"
"    background: #ccff66;\n"
"}\n"
"\n"
"QDialogButtonBox *[text=\"Cancel\"] { \n"
"    background: #fe6665;\n"
"}\n"
"\n"
"QDialogButtonBox *[text=\"Restore Defaults\"]  {\n"
"    background: #d8d8d8;\n"
"}\n"
"")
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.button_box.setCenterButtons(False)
        self.button_box.setObjectName("button_box")
        self.gridLayout.addWidget(self.button_box, 5, 0, 1, 1)
        self.notifications_gb = QtWidgets.QGroupBox(SettingsDialog)
        self.notifications_gb.setObjectName("notifications_gb")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.notifications_gb)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.birthdays_notification_chb = QtWidgets.QCheckBox(self.notifications_gb)
        self.birthdays_notification_chb.setChecked(True)
        self.birthdays_notification_chb.setObjectName("birthdays_notification_chb")
        self.horizontalLayout.addWidget(self.birthdays_notification_chb)
        self.birthdays_notification_range_value_sb = QtWidgets.QSpinBox(self.notifications_gb)
        self.birthdays_notification_range_value_sb.setMinimum(1)
        self.birthdays_notification_range_value_sb.setMaximum(365)
        self.birthdays_notification_range_value_sb.setObjectName("birthdays_notification_range_value_sb")
        self.horizontalLayout.addWidget(self.birthdays_notification_range_value_sb)
        self.gridLayout.addWidget(self.notifications_gb, 2, 0, 1, 1)

        self.retranslateUi(SettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)
        SettingsDialog.setTabOrder(self.host_name_ln_edt, self.port_ln_edt)
        SettingsDialog.setTabOrder(self.port_ln_edt, self.database_name_ln_edt)
        SettingsDialog.setTabOrder(self.database_name_ln_edt, self.username_ln_edt)
        SettingsDialog.setTabOrder(self.username_ln_edt, self.password_ln_edt)
        SettingsDialog.setTabOrder(self.password_ln_edt, self.check_connection_btn)
        SettingsDialog.setTabOrder(self.check_connection_btn, self.birthdays_notification_chb)
        SettingsDialog.setTabOrder(self.birthdays_notification_chb, self.birthdays_notification_range_value_sb)
        SettingsDialog.setTabOrder(self.birthdays_notification_range_value_sb, self.qsql_driver_ln_edt)

    def retranslateUi(self, SettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Телефонная книжка — Настройки"))
        self.database_connection_gb.setTitle(_translate("SettingsDialog", "Подключение к базе данных"))
        self.host_name_ln_edt.setPlaceholderText(_translate("SettingsDialog", "Имя хоста"))
        self.port_ln_edt.setPlaceholderText(_translate("SettingsDialog", "Порт"))
        self.database_name_ln_edt.setPlaceholderText(_translate("SettingsDialog", "Имя базы данных"))
        self.username_ln_edt.setPlaceholderText(_translate("SettingsDialog", "Имя пользователя"))
        self.password_ln_edt.setPlaceholderText(_translate("SettingsDialog", "Пароль"))
        self.qsql_driver_ln_edt.setToolTip(_translate("SettingsDialog", "Измение запрещено, приводится для справки"))
        self.qsql_driver_ln_edt.setPlaceholderText(_translate("SettingsDialog", "Драйвер"))
        self.check_connection_btn.setText(_translate("SettingsDialog", "Проверить соединение"))
        self.label.setText(_translate("SettingsDialog", "Настройки"))
        self.notifications_gb.setTitle(_translate("SettingsDialog", "Уведомления"))
        self.birthdays_notification_chb.setText(_translate("SettingsDialog", "Уведомлять о днях рождения за"))
        self.birthdays_notification_range_value_sb.setSuffix(_translate("SettingsDialog", " дней"))


