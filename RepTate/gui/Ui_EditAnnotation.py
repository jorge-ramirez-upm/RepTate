# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'annotationedit.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QDoubleSpinBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpinBox, QToolButton, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(334, 567)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_9 = QGroupBox(Dialog)
        self.groupBox_9.setObjectName(u"groupBox_9")
        font = QFont()
        font.setBold(True)
        self.groupBox_9.setFont(font)
        self.verticalLayout_14 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_14.setSpacing(9)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(-1, 9, -1, 9)
        self.frame = QFrame(self.groupBox_9)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_11 = QLabel(self.frame)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout.addWidget(self.label_11)

        self.textLineEdit = QLineEdit(self.frame)
        self.textLineEdit.setObjectName(u"textLineEdit")
        font1 = QFont()
        font1.setBold(False)
        self.textLineEdit.setFont(font1)

        self.horizontalLayout.addWidget(self.textLineEdit)


        self.verticalLayout_14.addWidget(self.frame)

        self.frame_2 = QFrame(self.groupBox_9)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.xLineEdit = QLineEdit(self.frame_2)
        self.xLineEdit.setObjectName(u"xLineEdit")

        self.gridLayout.addWidget(self.xLineEdit, 1, 1, 1, 1)

        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)

        self.yLineEdit = QLineEdit(self.frame_2)
        self.yLineEdit.setObjectName(u"yLineEdit")

        self.gridLayout.addWidget(self.yLineEdit, 1, 3, 1, 1)


        self.verticalLayout_14.addWidget(self.frame_2)

        self.frame_7 = QFrame(self.groupBox_9)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_10 = QLabel(self.frame_7)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_21.addWidget(self.label_10)

        self.rotationSpinBox = QDoubleSpinBox(self.frame_7)
        self.rotationSpinBox.setObjectName(u"rotationSpinBox")
        self.rotationSpinBox.setFont(font1)
        self.rotationSpinBox.setDecimals(1)
        self.rotationSpinBox.setMaximum(360.000000000000000)

        self.horizontalLayout_21.addWidget(self.rotationSpinBox)


        self.verticalLayout_14.addWidget(self.frame_7)

        self.frame_8 = QFrame(self.groupBox_9)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_8)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.label_12 = QLabel(self.frame_8)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout_16.addWidget(self.label_12)

        self.frame_9 = QFrame(self.frame_8)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.label_13 = QLabel(self.frame_9)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_22.addWidget(self.label_13)

        self.hacomboBox = QComboBox(self.frame_9)
        self.hacomboBox.addItem("")
        self.hacomboBox.addItem("")
        self.hacomboBox.addItem("")
        self.hacomboBox.setObjectName(u"hacomboBox")
        self.hacomboBox.setFont(font1)

        self.horizontalLayout_22.addWidget(self.hacomboBox)

        self.label_14 = QLabel(self.frame_9)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_22.addWidget(self.label_14)

        self.vacomboBox = QComboBox(self.frame_9)
        self.vacomboBox.addItem("")
        self.vacomboBox.addItem("")
        self.vacomboBox.addItem("")
        self.vacomboBox.addItem("")
        self.vacomboBox.setObjectName(u"vacomboBox")
        self.vacomboBox.setFont(font1)

        self.horizontalLayout_22.addWidget(self.vacomboBox)


        self.verticalLayout_16.addWidget(self.frame_9)


        self.verticalLayout_14.addWidget(self.frame_8)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setSpacing(9)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(9, 9, 9, 9)
        self.label_7 = QLabel(self.groupBox_9)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_23.addWidget(self.label_7)

        self.labelFontColor = QLabel(self.groupBox_9)
        self.labelFontColor.setObjectName(u"labelFontColor")
        self.labelFontColor.setEnabled(False)
        self.labelFontColor.setFont(font1)

        self.horizontalLayout_23.addWidget(self.labelFontColor)

        self.pickFontColor = QToolButton(self.groupBox_9)
        self.pickFontColor.setObjectName(u"pickFontColor")
        self.pickFontColor.setEnabled(True)
        self.pickFontColor.setFont(font1)

        self.horizontalLayout_23.addWidget(self.pickFontColor)


        self.verticalLayout_14.addLayout(self.horizontalLayout_23)

        self.frame_11 = QFrame(self.groupBox_9)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_26 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.label_15 = QLabel(self.frame_11)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_26.addWidget(self.label_15)

        self.fontweightComboBox = QComboBox(self.frame_11)
        self.fontweightComboBox.addItem("")
        self.fontweightComboBox.addItem("")
        self.fontweightComboBox.addItem("")
        self.fontweightComboBox.addItem("")
        self.fontweightComboBox.addItem("")
        self.fontweightComboBox.addItem("")
        self.fontweightComboBox.addItem("")
        self.fontweightComboBox.addItem("")
        self.fontweightComboBox.addItem("")
        self.fontweightComboBox.addItem("")
        self.fontweightComboBox.addItem("")
        self.fontweightComboBox.addItem("")
        self.fontweightComboBox.addItem("")
        self.fontweightComboBox.addItem("")
        self.fontweightComboBox.setObjectName(u"fontweightComboBox")
        self.fontweightComboBox.setFont(font1)

        self.horizontalLayout_26.addWidget(self.fontweightComboBox)

        self.label_16 = QLabel(self.frame_11)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_26.addWidget(self.label_16)

        self.fontstyleComboBox = QComboBox(self.frame_11)
        self.fontstyleComboBox.addItem("")
        self.fontstyleComboBox.addItem("")
        self.fontstyleComboBox.addItem("")
        self.fontstyleComboBox.setObjectName(u"fontstyleComboBox")
        self.fontstyleComboBox.setFont(font1)

        self.horizontalLayout_26.addWidget(self.fontstyleComboBox)


        self.verticalLayout_14.addWidget(self.frame_11)

        self.frame_12 = QFrame(self.groupBox_9)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.label_17 = QLabel(self.frame_12)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_27.addWidget(self.label_17)

        self.fontsizeannotationSpinBox = QSpinBox(self.frame_12)
        self.fontsizeannotationSpinBox.setObjectName(u"fontsizeannotationSpinBox")
        self.fontsizeannotationSpinBox.setFont(font1)
        self.fontsizeannotationSpinBox.setMinimum(1)

        self.horizontalLayout_27.addWidget(self.fontsizeannotationSpinBox)


        self.verticalLayout_14.addWidget(self.frame_12)

        self.frame_13 = QFrame(self.groupBox_9)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_6 = QLabel(self.frame_13)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_28.addWidget(self.label_6)

        self.framealphaannotationSpinBox = QDoubleSpinBox(self.frame_13)
        self.framealphaannotationSpinBox.setObjectName(u"framealphaannotationSpinBox")
        self.framealphaannotationSpinBox.setEnabled(True)
        self.framealphaannotationSpinBox.setFont(font1)
        self.framealphaannotationSpinBox.setMaximum(1.000000000000000)
        self.framealphaannotationSpinBox.setSingleStep(0.050000000000000)

        self.horizontalLayout_28.addWidget(self.framealphaannotationSpinBox)


        self.verticalLayout_14.addWidget(self.frame_13)

        self.frame_14 = QFrame(self.groupBox_9)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.label_18 = QLabel(self.frame_14)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_29.addWidget(self.label_18)

        self.fontfamilyComboBox = QComboBox(self.frame_14)
        self.fontfamilyComboBox.addItem("")
        self.fontfamilyComboBox.addItem("")
        self.fontfamilyComboBox.addItem("")
        self.fontfamilyComboBox.addItem("")
        self.fontfamilyComboBox.addItem("")
        self.fontfamilyComboBox.setObjectName(u"fontfamilyComboBox")
        self.fontfamilyComboBox.setFont(font1)

        self.horizontalLayout_29.addWidget(self.fontfamilyComboBox)


        self.verticalLayout_14.addWidget(self.frame_14)


        self.verticalLayout.addWidget(self.groupBox_9)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushApply = QPushButton(Dialog)
        self.pushApply.setObjectName(u"pushApply")

        self.horizontalLayout_2.addWidget(self.pushApply)

        self.pushCancel = QPushButton(Dialog)
        self.pushCancel.setObjectName(u"pushCancel")

        self.horizontalLayout_2.addWidget(self.pushCancel)

        self.pushDelete = QPushButton(Dialog)
        self.pushDelete.setObjectName(u"pushDelete")

        self.horizontalLayout_2.addWidget(self.pushDelete)

        self.pushOK = QPushButton(Dialog)
        self.pushOK.setObjectName(u"pushOK")

        self.horizontalLayout_2.addWidget(self.pushOK)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Dialog)
        self.pushOK.clicked.connect(Dialog.accept)
        self.pushCancel.clicked.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"View/Edit Annotation Settings", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("Dialog", u"Annotation Properties", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Text", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Position", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"x", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"y", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Rotation", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Alignment", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Horizontal", None))
        self.hacomboBox.setItemText(0, QCoreApplication.translate("Dialog", u"center", None))
        self.hacomboBox.setItemText(1, QCoreApplication.translate("Dialog", u"right", None))
        self.hacomboBox.setItemText(2, QCoreApplication.translate("Dialog", u"left", None))

        self.label_14.setText(QCoreApplication.translate("Dialog", u"Vertical", None))
        self.vacomboBox.setItemText(0, QCoreApplication.translate("Dialog", u"center", None))
        self.vacomboBox.setItemText(1, QCoreApplication.translate("Dialog", u"top", None))
        self.vacomboBox.setItemText(2, QCoreApplication.translate("Dialog", u"bottom", None))
        self.vacomboBox.setItemText(3, QCoreApplication.translate("Dialog", u"baseline", None))

        self.label_7.setText(QCoreApplication.translate("Dialog", u"Font Color", None))
        self.labelFontColor.setText("")
        self.pickFontColor.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Font weight", None))
        self.fontweightComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"ultralight", None))
        self.fontweightComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"light", None))
        self.fontweightComboBox.setItemText(2, QCoreApplication.translate("Dialog", u"normal", None))
        self.fontweightComboBox.setItemText(3, QCoreApplication.translate("Dialog", u"regular", None))
        self.fontweightComboBox.setItemText(4, QCoreApplication.translate("Dialog", u"book", None))
        self.fontweightComboBox.setItemText(5, QCoreApplication.translate("Dialog", u"medium", None))
        self.fontweightComboBox.setItemText(6, QCoreApplication.translate("Dialog", u"roman", None))
        self.fontweightComboBox.setItemText(7, QCoreApplication.translate("Dialog", u"semibold", None))
        self.fontweightComboBox.setItemText(8, QCoreApplication.translate("Dialog", u"demibold", None))
        self.fontweightComboBox.setItemText(9, QCoreApplication.translate("Dialog", u"demi", None))
        self.fontweightComboBox.setItemText(10, QCoreApplication.translate("Dialog", u"bold", None))
        self.fontweightComboBox.setItemText(11, QCoreApplication.translate("Dialog", u"heavy", None))
        self.fontweightComboBox.setItemText(12, QCoreApplication.translate("Dialog", u"extra bold", None))
        self.fontweightComboBox.setItemText(13, QCoreApplication.translate("Dialog", u"black", None))

        self.label_16.setText(QCoreApplication.translate("Dialog", u"Font Style", None))
        self.fontstyleComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"normal", None))
        self.fontstyleComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"italic", None))
        self.fontstyleComboBox.setItemText(2, QCoreApplication.translate("Dialog", u"oblique", None))

#if QT_CONFIG(tooltip)
        self.label_17.setToolTip(QCoreApplication.translate("Dialog", u"Legend font size", None))
#endif // QT_CONFIG(tooltip)
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Font Size", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Transparency", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Font Family", None))
        self.fontfamilyComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"serif", None))
        self.fontfamilyComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"sans-serif", None))
        self.fontfamilyComboBox.setItemText(2, QCoreApplication.translate("Dialog", u"cursive", None))
        self.fontfamilyComboBox.setItemText(3, QCoreApplication.translate("Dialog", u"fantasy", None))
        self.fontfamilyComboBox.setItemText(4, QCoreApplication.translate("Dialog", u"monospace", None))

        self.pushApply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushCancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.pushDelete.setText(QCoreApplication.translate("Dialog", u"Delete", None))
        self.pushOK.setText(QCoreApplication.translate("Dialog", u"OK", None))
    # retranslateUi

