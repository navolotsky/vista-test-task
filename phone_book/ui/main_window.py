# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_designer/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/icon128.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QtCore.QSize(48, 48))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_contact_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_contact_btn.setEnabled(False)
        self.add_contact_btn.setObjectName("add_contact_btn")
        self.horizontalLayout.addWidget(self.add_contact_btn)
        self.edit_contact_btn = QtWidgets.QPushButton(self.centralwidget)
        self.edit_contact_btn.setEnabled(False)
        self.edit_contact_btn.setObjectName("edit_contact_btn")
        self.horizontalLayout.addWidget(self.edit_contact_btn)
        self.delete_contact_btn = QtWidgets.QPushButton(self.centralwidget)
        self.delete_contact_btn.setEnabled(False)
        self.delete_contact_btn.setObjectName("delete_contact_btn")
        self.horizontalLayout.addWidget(self.delete_contact_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.log_in_out_btn = QtWidgets.QPushButton(self.centralwidget)
        self.log_in_out_btn.setObjectName("log_in_out_btn")
        self.horizontalLayout.addWidget(self.log_in_out_btn)
        self.settings_btn = QtWidgets.QPushButton(self.centralwidget)
        self.settings_btn.setObjectName("settings_btn")
        self.horizontalLayout.addWidget(self.settings_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.contacts_tab_widget = QtWidgets.QTabWidget(self.centralwidget)
        self.contacts_tab_widget.setTabPosition(QtWidgets.QTabWidget.West)
        self.contacts_tab_widget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.contacts_tab_widget.setObjectName("contacts_tab_widget")
        self.verticalLayout.addWidget(self.contacts_tab_widget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.contacts_tab_widget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Телефонная книжка"))
        self.add_contact_btn.setText(_translate("MainWindow", "Добавить"))
        self.edit_contact_btn.setText(_translate("MainWindow", "Изменить"))
        self.delete_contact_btn.setText(_translate("MainWindow", "Удалить"))
        self.label.setText(_translate("MainWindow", "Вход не выполнен"))
        self.log_in_out_btn.setText(_translate("MainWindow", "Войти"))
        self.settings_btn.setText(_translate("MainWindow", "Настройки"))


from . import images_rc
