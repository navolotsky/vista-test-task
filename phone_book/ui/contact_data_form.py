# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_designer/contact_data_form.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ContactDataForm(object):
    def setupUi(self, ContactDataForm):
        ContactDataForm.setObjectName("ContactDataForm")
        ContactDataForm.setWindowModality(QtCore.Qt.ApplicationModal)
        ContactDataForm.resize(300, 200)
        ContactDataForm.setMinimumSize(QtCore.QSize(300, 200))
        ContactDataForm.setStyleSheet("#ContactDataForm {\n"
"    border-width: 2;\n"
"    border-radius: 5;\n"
"    border-style: solid;\n"
"    border-color: gray;\n"
"}\n"
"")
        self.gridLayout = QtWidgets.QGridLayout(ContactDataForm)
        self.gridLayout.setObjectName("gridLayout")
        self.button_box = QtWidgets.QDialogButtonBox(ContactDataForm)
        self.button_box.setStyleSheet("QDialogButtonBox *[text=\"OK\"] {\n"
"    background: #ccff66;\n"
"}\n"
"\n"
"QDialogButtonBox *[text=\"Cancel\"] { \n"
"    background: #fe6665;\n"
"}")
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.setObjectName("button_box")
        self.gridLayout.addWidget(self.button_box, 5, 0, 1, 1)
        self.label = QtWidgets.QLabel(ContactDataForm)
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
        self.phone_number_ln_edt = QtWidgets.QLineEdit(ContactDataForm)
        self.phone_number_ln_edt.setText("")
        self.phone_number_ln_edt.setObjectName("phone_number_ln_edt")
        self.gridLayout.addWidget(self.phone_number_ln_edt, 2, 0, 1, 1)
        self.name_ln_edt = QtWidgets.QLineEdit(ContactDataForm)
        self.name_ln_edt.setText("")
        self.name_ln_edt.setObjectName("name_ln_edt")
        self.gridLayout.addWidget(self.name_ln_edt, 1, 0, 1, 1)
        self.birth_date_dt_edt = QtWidgets.QDateEdit(ContactDataForm)
        self.birth_date_dt_edt.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.birth_date_dt_edt.setCalendarPopup(True)
        self.birth_date_dt_edt.setObjectName("birth_date_dt_edt")
        self.gridLayout.addWidget(self.birth_date_dt_edt, 4, 0, 1, 1)

        self.retranslateUi(ContactDataForm)
        QtCore.QMetaObject.connectSlotsByName(ContactDataForm)
        ContactDataForm.setTabOrder(self.name_ln_edt, self.phone_number_ln_edt)
        ContactDataForm.setTabOrder(self.phone_number_ln_edt, self.birth_date_dt_edt)

    def retranslateUi(self, ContactDataForm):
        _translate = QtCore.QCoreApplication.translate
        ContactDataForm.setWindowTitle(_translate("ContactDataForm", "Добавить/Изменить контакт"))
        self.label.setText(_translate("ContactDataForm", "Данные контакта"))
        self.phone_number_ln_edt.setPlaceholderText(_translate("ContactDataForm", "Телефон"))
        self.name_ln_edt.setPlaceholderText(_translate("ContactDataForm", "Имя"))
        self.birth_date_dt_edt.setToolTip(_translate("ContactDataForm", "Дата рождения"))


