# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_designer/auth_form.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AuthForm(object):
    def setupUi(self, AuthForm):
        AuthForm.setObjectName("AuthForm")
        AuthForm.setWindowModality(QtCore.Qt.ApplicationModal)
        AuthForm.resize(300, 236)
        AuthForm.setMinimumSize(QtCore.QSize(300, 200))
        AuthForm.setFocusPolicy(QtCore.Qt.StrongFocus)
        AuthForm.setStyleSheet("#AuthForm {\n"
"    border-width: 2;\n"
"    border-radius: 5;\n"
"    border-style: solid;\n"
"    border-color: gray;\n"
"}\n"
"")
        self.gridLayout = QtWidgets.QGridLayout(AuthForm)
        self.gridLayout.setObjectName("gridLayout")
        self.forgot_password_btn = QtWidgets.QPushButton(AuthForm)
        self.forgot_password_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.forgot_password_btn.setStyleSheet("#forgot_password_btn {\n"
"    text-decoration: underline;\n"
"    color:#0000ff;\n"
"}")
        self.forgot_password_btn.setFlat(True)
        self.forgot_password_btn.setObjectName("forgot_password_btn")
        self.buttonGroup = QtWidgets.QButtonGroup(AuthForm)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.forgot_password_btn)
        self.gridLayout.addWidget(self.forgot_password_btn, 9, 1, 1, 1)
        self.show_password_chb = QtWidgets.QCheckBox(AuthForm)
        self.show_password_chb.setObjectName("show_password_chb")
        self.gridLayout.addWidget(self.show_password_chb, 8, 1, 1, 1)
        self.username_ln_edt = QtWidgets.QLineEdit(AuthForm)
        self.username_ln_edt.setText("")
        self.username_ln_edt.setObjectName("username_ln_edt")
        self.gridLayout.addWidget(self.username_ln_edt, 3, 0, 1, 3)
        self.password_ln_edt = QtWidgets.QLineEdit(AuthForm)
        self.password_ln_edt.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_ln_edt.setObjectName("password_ln_edt")
        self.gridLayout.addWidget(self.password_ln_edt, 4, 0, 1, 3)
        self.login_btn = QtWidgets.QPushButton(AuthForm)
        self.login_btn.setMinimumSize(QtCore.QSize(80, 0))
        self.login_btn.setMaximumSize(QtCore.QSize(80, 16777215))
        self.login_btn.setStyleSheet("#login_btn {\n"
"    background: #ccff66;\n"
"}\n"
"")
        self.login_btn.setDefault(True)
        self.login_btn.setObjectName("login_btn")
        self.buttonGroup.addButton(self.login_btn)
        self.gridLayout.addWidget(self.login_btn, 5, 0, 1, 1)
        self.register_btn = QtWidgets.QPushButton(AuthForm)
        self.register_btn.setMinimumSize(QtCore.QSize(110, 0))
        self.register_btn.setMaximumSize(QtCore.QSize(110, 16777215))
        self.register_btn.setStyleSheet("#register_btn {\n"
"    background: #d8d8d8;\n"
"}\n"
"")
        self.register_btn.setObjectName("register_btn")
        self.buttonGroup.addButton(self.register_btn)
        self.gridLayout.addWidget(self.register_btn, 5, 1, 1, 1)
        self.cancel_btn = QtWidgets.QPushButton(AuthForm)
        self.cancel_btn.setMinimumSize(QtCore.QSize(80, 0))
        self.cancel_btn.setMaximumSize(QtCore.QSize(80, 16777215))
        self.cancel_btn.setStyleSheet("#cancel_btn {\n"
"    background: #fe6665;\n"
"}")
        self.cancel_btn.setObjectName("cancel_btn")
        self.buttonGroup.addButton(self.cancel_btn)
        self.gridLayout.addWidget(self.cancel_btn, 5, 2, 1, 1)
        self.remember_me_chb = QtWidgets.QCheckBox(AuthForm)
        self.remember_me_chb.setObjectName("remember_me_chb")
        self.gridLayout.addWidget(self.remember_me_chb, 7, 1, 1, 1)
        self.label = QtWidgets.QLabel(AuthForm)
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
        self.gridLayout.addWidget(self.label, 2, 0, 1, 3)

        self.retranslateUi(AuthForm)
        QtCore.QMetaObject.connectSlotsByName(AuthForm)
        AuthForm.setTabOrder(self.username_ln_edt, self.password_ln_edt)
        AuthForm.setTabOrder(self.password_ln_edt, self.remember_me_chb)
        AuthForm.setTabOrder(self.remember_me_chb, self.show_password_chb)
        AuthForm.setTabOrder(self.show_password_chb, self.forgot_password_btn)
        AuthForm.setTabOrder(self.forgot_password_btn, self.login_btn)
        AuthForm.setTabOrder(self.login_btn, self.register_btn)
        AuthForm.setTabOrder(self.register_btn, self.cancel_btn)

    def retranslateUi(self, AuthForm):
        _translate = QtCore.QCoreApplication.translate
        AuthForm.setWindowTitle(_translate("AuthForm", "Вход"))
        self.forgot_password_btn.setToolTip(_translate("AuthForm", "Сбросить пароль"))
        self.forgot_password_btn.setText(_translate("AuthForm", "Забыли пароль?"))
        self.show_password_chb.setText(_translate("AuthForm", "Показать пароль"))
        self.username_ln_edt.setPlaceholderText(_translate("AuthForm", "Имя пользователя или e-mail"))
        self.password_ln_edt.setPlaceholderText(_translate("AuthForm", "Пароль"))
        self.login_btn.setText(_translate("AuthForm", "Войти"))
        self.register_btn.setText(_translate("AuthForm", "Регистрация"))
        self.cancel_btn.setText(_translate("AuthForm", "Отмена"))
        self.remember_me_chb.setText(_translate("AuthForm", "Запомнить меня"))
        self.label.setText(_translate("AuthForm", "Авторизация"))


