# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'errorcalculationoptions.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QGroupBox,
    QHBoxLayout, QPushButton, QRadioButton, QSizePolicy,
    QVBoxLayout, QWidget)
from . import Reptate_rc
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(275, 213)
        icon = QIcon()
        icon.addFile(u":/Images/Images/new_icons/icons8-abacus.png", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setLayoutDirection(Qt.RightToLeft)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_3 = QGroupBox(Dialog)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.View1radioButton = QRadioButton(self.groupBox_3)
        self.View1radioButton.setObjectName(u"View1radioButton")

        self.verticalLayout_2.addWidget(self.View1radioButton)

        self.AllViewsradioButton = QRadioButton(self.groupBox_3)
        self.AllViewsradioButton.setObjectName(u"AllViewsradioButton")
        self.AllViewsradioButton.setCheckable(False)

        self.verticalLayout_2.addWidget(self.AllViewsradioButton)

        self.RawDataradioButton = QRadioButton(self.groupBox_3)
        self.RawDataradioButton.setObjectName(u"RawDataradioButton")
        self.RawDataradioButton.setCheckable(False)

        self.verticalLayout_2.addWidget(self.RawDataradioButton)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.NormalizecheckBox = QCheckBox(Dialog)
        self.NormalizecheckBox.setObjectName(u"NormalizecheckBox")

        self.verticalLayout.addWidget(self.NormalizecheckBox)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushCancel = QPushButton(Dialog)
        self.pushCancel.setObjectName(u"pushCancel")

        self.horizontalLayout_5.addWidget(self.pushCancel)

        self.pushOK = QPushButton(Dialog)
        self.pushOK.setObjectName(u"pushOK")

        self.horizontalLayout_5.addWidget(self.pushOK)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.retranslateUi(Dialog)
        self.pushOK.clicked.connect(Dialog.accept)
        self.pushCancel.clicked.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Error Calculation Options", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Calculate error with respect to", None))
        self.View1radioButton.setText(QCoreApplication.translate("Dialog", u"View number 1", None))
        self.AllViewsradioButton.setText(QCoreApplication.translate("Dialog", u"All active views", None))
        self.RawDataradioButton.setText(QCoreApplication.translate("Dialog", u"Raw data table", None))
        self.NormalizecheckBox.setText(QCoreApplication.translate("Dialog", u"Normalize by experimental data", None))
        self.pushCancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.pushOK.setText(QCoreApplication.translate("Dialog", u"OK", None))
    # retranslateUi

