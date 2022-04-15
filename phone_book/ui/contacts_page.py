# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_designer/contacts_page.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ContactsPage(object):
    def setupUi(self, ContactsPage):
        ContactsPage.setObjectName("ContactsPage")
        ContactsPage.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(ContactsPage)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QtWidgets.QTableView(ContactsPage)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.tableView.setTabKeyNavigation(False)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 1)

        self.retranslateUi(ContactsPage)
        QtCore.QMetaObject.connectSlotsByName(ContactsPage)

    def retranslateUi(self, ContactsPage):
        _translate = QtCore.QCoreApplication.translate
        ContactsPage.setWindowTitle(_translate("ContactsPage", "Form"))


