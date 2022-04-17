# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_designer/upcoming_birthdays_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UpcomingBirthdaysDialog(object):
    def setupUi(self, UpcomingBirthdaysDialog):
        UpcomingBirthdaysDialog.setObjectName("UpcomingBirthdaysDialog")
        UpcomingBirthdaysDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        UpcomingBirthdaysDialog.resize(320, 299)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UpcomingBirthdaysDialog.sizePolicy().hasHeightForWidth())
        UpcomingBirthdaysDialog.setSizePolicy(sizePolicy)
        UpcomingBirthdaysDialog.setMinimumSize(QtCore.QSize(200, 100))
        UpcomingBirthdaysDialog.setStyleSheet("#UpcomingBirthdaysDialog {\n"
"    border-width: 2;\n"
"    border-radius: 5;\n"
"    border-style: solid;\n"
"    border-color: gray;\n"
"}\n"
"")
        self.gridLayout = QtWidgets.QGridLayout(UpcomingBirthdaysDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.button_box = QtWidgets.QDialogButtonBox(UpcomingBirthdaysDialog)
        self.button_box.setStyleSheet("QDialogButtonBox *[text=\"OK\"] {\n"
"    background: #ccff66;\n"
"}\n"
"\n"
"QDialogButtonBox *[text=\"Cancel\"] { \n"
"    background: #fe6665;\n"
"}")
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.setObjectName("button_box")
        self.gridLayout.addWidget(self.button_box, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(UpcomingBirthdaysDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.tableView = QtWidgets.QTableView(UpcomingBirthdaysDialog)
        self.tableView.setTabKeyNavigation(False)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 1)

        self.retranslateUi(UpcomingBirthdaysDialog)
        QtCore.QMetaObject.connectSlotsByName(UpcomingBirthdaysDialog)

    def retranslateUi(self, UpcomingBirthdaysDialog):
        _translate = QtCore.QCoreApplication.translate
        UpcomingBirthdaysDialog.setWindowTitle(_translate("UpcomingBirthdaysDialog", "Телефонная книжка"))
        self.label.setText(_translate("UpcomingBirthdaysDialog", "Предстоящие дни рождения"))


