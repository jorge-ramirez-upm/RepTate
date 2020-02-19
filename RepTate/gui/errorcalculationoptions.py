# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'errorcalculationoptions.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(275, 213)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/Images/new_icons/icons8-abacus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.View1radioButton = QtWidgets.QRadioButton(self.groupBox_3)
        self.View1radioButton.setObjectName("View1radioButton")
        self.verticalLayout_2.addWidget(self.View1radioButton)
        self.AllViewsradioButton = QtWidgets.QRadioButton(self.groupBox_3)
        self.AllViewsradioButton.setCheckable(False)
        self.AllViewsradioButton.setObjectName("AllViewsradioButton")
        self.verticalLayout_2.addWidget(self.AllViewsradioButton)
        self.RawDataradioButton = QtWidgets.QRadioButton(self.groupBox_3)
        self.RawDataradioButton.setCheckable(False)
        self.RawDataradioButton.setObjectName("RawDataradioButton")
        self.verticalLayout_2.addWidget(self.RawDataradioButton)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.NormalizecheckBox = QtWidgets.QCheckBox(Dialog)
        self.NormalizecheckBox.setObjectName("NormalizecheckBox")
        self.verticalLayout.addWidget(self.NormalizecheckBox)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushCancel = QtWidgets.QPushButton(Dialog)
        self.pushCancel.setObjectName("pushCancel")
        self.horizontalLayout_5.addWidget(self.pushCancel)
        self.pushOK = QtWidgets.QPushButton(Dialog)
        self.pushOK.setObjectName("pushOK")
        self.horizontalLayout_5.addWidget(self.pushOK)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Dialog)
        self.pushOK.clicked.connect(Dialog.accept)
        self.pushCancel.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Error Calculation Options"))
        self.groupBox_3.setTitle(_translate("Dialog", "Calculate error with respect to"))
        self.View1radioButton.setText(_translate("Dialog", "View number 1"))
        self.AllViewsradioButton.setText(_translate("Dialog", "All active views"))
        self.RawDataradioButton.setText(_translate("Dialog", "Raw data table"))
        self.NormalizecheckBox.setText(_translate("Dialog", "Normalize by experimental data"))
        self.pushCancel.setText(_translate("Dialog", "Cancel"))
        self.pushOK.setText(_translate("Dialog", "OK"))
import Reptate_rc
