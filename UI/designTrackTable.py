# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designTrackTable.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(815, 300)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setObjectName("tableView")
        self.horizontalLayout_2.addWidget(self.tableView)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_humanEditors = QtWidgets.QGroupBox(Dialog)
        self.groupBox_humanEditors.setMaximumSize(QtCore.QSize(120, 16777215))
        self.groupBox_humanEditors.setObjectName("groupBox_humanEditors")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_humanEditors)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_addRow = QtWidgets.QPushButton(self.groupBox_humanEditors)
        self.pushButton_addRow.setObjectName("pushButton_addRow")
        self.verticalLayout.addWidget(self.pushButton_addRow)
        self.pushButton_deletRow = QtWidgets.QPushButton(self.groupBox_humanEditors)
        self.pushButton_deletRow.setObjectName("pushButton_deletRow")
        self.verticalLayout.addWidget(self.pushButton_deletRow)
        self.verticalLayout_3.addWidget(self.groupBox_humanEditors)
        self.groupBox_ExcelEditor = QtWidgets.QGroupBox(Dialog)
        self.groupBox_ExcelEditor.setMaximumSize(QtCore.QSize(120, 16777215))
        self.groupBox_ExcelEditor.setObjectName("groupBox_ExcelEditor")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_ExcelEditor)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_openExcel = QtWidgets.QPushButton(self.groupBox_ExcelEditor)
        self.pushButton_openExcel.setObjectName("pushButton_openExcel")
        self.verticalLayout_2.addWidget(self.pushButton_openExcel)
        self.pushButton_loadChange = QtWidgets.QPushButton(self.groupBox_ExcelEditor)
        self.pushButton_loadChange.setObjectName("pushButton_loadChange")
        self.verticalLayout_2.addWidget(self.pushButton_loadChange)
        self.verticalLayout_3.addWidget(self.groupBox_ExcelEditor)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_OK = QtWidgets.QPushButton(Dialog)
        self.pushButton_OK.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.horizontalLayout.addWidget(self.pushButton_OK)
        self.pushButton_Cancel = QtWidgets.QPushButton(Dialog)
        self.pushButton_Cancel.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.horizontalLayout.addWidget(self.pushButton_Cancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox_humanEditors.setTitle(_translate("Dialog", "人工编辑"))
        self.pushButton_addRow.setText(_translate("Dialog", "增加一行"))
        self.pushButton_deletRow.setText(_translate("Dialog", "删除一行"))
        self.groupBox_ExcelEditor.setTitle(_translate("Dialog", "Excel编辑"))
        self.pushButton_openExcel.setText(_translate("Dialog", "打开表格"))
        self.pushButton_loadChange.setText(_translate("Dialog", "载入更改"))
        self.pushButton_OK.setText(_translate("Dialog", "确认"))
        self.pushButton_Cancel.setText(_translate("Dialog", "取消"))

