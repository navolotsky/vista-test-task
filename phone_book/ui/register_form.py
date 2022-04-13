# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_designer/register_form.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RegisterForm(object):
    def setupUi(self, RegisterForm):
        RegisterForm.setObjectName("RegisterForm")
        RegisterForm.setWindowModality(QtCore.Qt.ApplicationModal)
        RegisterForm.resize(300, 200)
        RegisterForm.setMinimumSize(QtCore.QSize(300, 200))
        RegisterForm.setStyleSheet("#RegisterForm {\n"
"    border-width: 2;\n"
"    border-radius: 5;\n"
"    border-style: solid;\n"
"    border-color: gray;\n"
"}\n"
"")
        self.gridLayout = QtWidgets.QGridLayout(RegisterForm)
        self.gridLayout.setObjectName("gridLayout")
        self.button_box = QtWidgets.QDialogButtonBox(RegisterForm)
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
        self.label = QtWidgets.QLabel(RegisterForm)
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
        self.email_ln_edt = QtWidgets.QLineEdit(RegisterForm)
        self.email_ln_edt.setText("")
        self.email_ln_edt.setObjectName("email_ln_edt")
        self.gridLayout.addWidget(self.email_ln_edt, 2, 0, 1, 1)
        self.username_ln_edt = QtWidgets.QLineEdit(RegisterForm)
        self.username_ln_edt.setText("")
        self.username_ln_edt.setObjectName("username_ln_edt")
        self.gridLayout.addWidget(self.username_ln_edt, 1, 0, 1, 1)
        self.birth_date_dt_edt = QtWidgets.QDateEdit(RegisterForm)
        self.birth_date_dt_edt.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.birth_date_dt_edt.setCalendarPopup(True)
        self.birth_date_dt_edt.setObjectName("birth_date_dt_edt")
        self.gridLayout.addWidget(self.birth_date_dt_edt, 4, 0, 1, 1)

        self.retranslateUi(RegisterForm)
        QtCore.QMetaObject.connectSlotsByName(RegisterForm)
        RegisterForm.setTabOrder(self.username_ln_edt, self.email_ln_edt)
        RegisterForm.setTabOrder(self.email_ln_edt, self.birth_date_dt_edt)

    def retranslateUi(self, RegisterForm):
        _translate = QtCore.QCoreApplication.translate
        RegisterForm.setWindowTitle(_translate("RegisterForm", "Регистрация"))
        self.label.setText(_translate("RegisterForm", "Регистрация"))
        self.email_ln_edt.setPlaceholderText(_translate("RegisterForm", "E-mail"))
        self.username_ln_edt.setPlaceholderText(_translate("RegisterForm", "Имя пользователя"))
        self.birth_date_dt_edt.setToolTip(_translate("RegisterForm", "Дата рождения"))


