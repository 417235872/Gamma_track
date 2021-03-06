# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\projectFileChooseDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 577)
        Dialog.setMinimumSize(QtCore.QSize(500, 0))
        Dialog.setMaximumSize(QtCore.QSize(500, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/70-basic-icons/SVGs/70 Basic Icons-all-19.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_topTip = QtWidgets.QLabel(Dialog)
        self.label_topTip.setObjectName("label_topTip")
        self.horizontalLayout.addWidget(self.label_topTip)
        self.back_toolButton = QtWidgets.QToolButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/feather-v1.1/svg-single/arrow-left.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back_toolButton.setIcon(icon1)
        self.back_toolButton.setObjectName("back_toolButton")
        self.horizontalLayout.addWidget(self.back_toolButton)
        self.disk_toolButton = QtWidgets.QToolButton(Dialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/feather-v1.1/svg-single/globe.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.disk_toolButton.setIcon(icon2)
        self.disk_toolButton.setObjectName("disk_toolButton")
        self.horizontalLayout.addWidget(self.disk_toolButton)
        self.desktop_toolButton = QtWidgets.QToolButton(Dialog)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/feather-v1.1/svg-single/monitor.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.desktop_toolButton.setIcon(icon3)
        self.desktop_toolButton.setObjectName("desktop_toolButton")
        self.horizontalLayout.addWidget(self.desktop_toolButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.lineEdit_currentChoose = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_currentChoose.setReadOnly(False)
        self.lineEdit_currentChoose.setObjectName("lineEdit_currentChoose")
        self.horizontalLayout_3.addWidget(self.lineEdit_currentChoose)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.treeView = NewTreeView(Dialog)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(268, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_OK = QtWidgets.QPushButton(Dialog)
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.horizontalLayout_2.addWidget(self.pushButton_OK)
        self.pushButton_cancel = QtWidgets.QPushButton(Dialog)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout_2.addWidget(self.pushButton_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_topTip.setText(_translate("Dialog", "TextLabel"))
        self.back_toolButton.setToolTip(_translate("Dialog", "后退"))
        self.back_toolButton.setText(_translate("Dialog", "..."))
        self.disk_toolButton.setToolTip(_translate("Dialog", "从所有磁盘"))
        self.disk_toolButton.setText(_translate("Dialog", "..."))
        self.desktop_toolButton.setToolTip(_translate("Dialog", "转到桌面"))
        self.desktop_toolButton.setText(_translate("Dialog", "..."))
        self.label.setText(_translate("Dialog", "当前选择："))
        self.pushButton_OK.setText(_translate("Dialog", "确认"))
        self.pushButton_cancel.setText(_translate("Dialog", "取消"))

from myWidget import NewTreeView

