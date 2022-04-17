# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_designer/delete_contact_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DeleteContactDialog(object):
    def setupUi(self, DeleteContactDialog):
        DeleteContactDialog.setObjectName("DeleteContactDialog")
        DeleteContactDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        DeleteContactDialog.resize(303, 104)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DeleteContactDialog.sizePolicy().hasHeightForWidth())
        DeleteContactDialog.setSizePolicy(sizePolicy)
        DeleteContactDialog.setMinimumSize(QtCore.QSize(200, 100))
        DeleteContactDialog.setStyleSheet("#DeleteContactDialog {\n"
"    border-width: 2;\n"
"    border-radius: 5;\n"
"    border-style: solid;\n"
"    border-color: gray;\n"
"}\n"
"")
        self.gridLayout = QtWidgets.QGridLayout(DeleteContactDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(DeleteContactDialog)
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
        self.button_box = QtWidgets.QDialogButtonBox(DeleteContactDialog)
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
        self.gridLayout.addWidget(self.button_box, 2, 0, 1, 1)

        self.retranslateUi(DeleteContactDialog)
        QtCore.QMetaObject.connectSlotsByName(DeleteContactDialog)

    def retranslateUi(self, DeleteContactDialog):
        _translate = QtCore.QCoreApplication.translate
        DeleteContactDialog.setWindowTitle(_translate("DeleteContactDialog", "Телефонная книжка"))
        self.label.setText(_translate("DeleteContactDialog", "Подтвердить удаление"))


