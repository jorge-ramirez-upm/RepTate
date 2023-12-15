# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fittingoptions.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTabWidget,
    QVBoxLayout, QWidget)
import Reptate_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(419, 780)
        icon = QIcon()
        icon.addFile(u":/Images/Images/new_icons/icons8-minimum-value.png", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setLayoutDirection(Qt.RightToLeft)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setLayoutDirection(Qt.LeftToRight)
        self.tabWidget.setStyleSheet(u"")
        self.tabWidget.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.ls = QWidget()
        self.ls.setObjectName(u"ls")
        self.verticalLayout_6 = QVBoxLayout(self.ls)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox = QGroupBox(self.ls)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 2, -1, 2)
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setScaledContents(False)
        self.label_4.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_4)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        font = QFont()
        font.setBold(True)
        self.label_5.setFont(font)

        self.verticalLayout_2.addWidget(self.label_5)

        self.frame_50 = QFrame(self.groupBox)
        self.frame_50.setObjectName(u"frame_50")
        self.frame_50.setFrameShape(QFrame.StyledPanel)
        self.frame_50.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_49 = QHBoxLayout(self.frame_50)
        self.horizontalLayout_49.setObjectName(u"horizontalLayout_49")
        self.horizontalLayout_49.setContentsMargins(-1, 2, -1, 2)
        self.label_3 = QLabel(self.frame_50)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_49.addWidget(self.label_3)

        self.LSmethodcomboBox = QComboBox(self.frame_50)
        self.LSmethodcomboBox.addItem("")
        self.LSmethodcomboBox.addItem("")
        self.LSmethodcomboBox.addItem("")
        self.LSmethodcomboBox.setObjectName(u"LSmethodcomboBox")

        self.horizontalLayout_49.addWidget(self.LSmethodcomboBox)


        self.verticalLayout_2.addWidget(self.frame_50)

        self.frame_29 = QFrame(self.groupBox)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setFrameShape(QFrame.StyledPanel)
        self.frame_29.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_30 = QHBoxLayout(self.frame_29)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalLayout_30.setContentsMargins(-1, 2, -1, 2)
        self.label_16 = QLabel(self.frame_29)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_30.addWidget(self.label_16)

        self.LSjaccomboBox = QComboBox(self.frame_29)
        self.LSjaccomboBox.addItem("")
        self.LSjaccomboBox.addItem("")
        self.LSjaccomboBox.addItem("")
        self.LSjaccomboBox.setObjectName(u"LSjaccomboBox")

        self.horizontalLayout_30.addWidget(self.LSjaccomboBox)


        self.verticalLayout_2.addWidget(self.frame_29)

        self.frame = QFrame(self.groupBox)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 2, -1, 2)
        self.LSftolcheckBox = QCheckBox(self.frame)
        self.LSftolcheckBox.setObjectName(u"LSftolcheckBox")
        self.LSftolcheckBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.LSftolcheckBox)

        self.LSftollineEdit = QLineEdit(self.frame)
        self.LSftollineEdit.setObjectName(u"LSftollineEdit")

        self.horizontalLayout_2.addWidget(self.LSftollineEdit)


        self.verticalLayout_2.addWidget(self.frame)

        self.frame_2 = QFrame(self.groupBox)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 2, -1, 2)
        self.LSxtolcheckBox = QCheckBox(self.frame_2)
        self.LSxtolcheckBox.setObjectName(u"LSxtolcheckBox")
        self.LSxtolcheckBox.setChecked(True)

        self.horizontalLayout_3.addWidget(self.LSxtolcheckBox)

        self.LSxtollineEdit = QLineEdit(self.frame_2)
        self.LSxtollineEdit.setObjectName(u"LSxtollineEdit")

        self.horizontalLayout_3.addWidget(self.LSxtollineEdit)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.frame_45 = QFrame(self.groupBox)
        self.frame_45.setObjectName(u"frame_45")
        self.frame_45.setFrameShape(QFrame.StyledPanel)
        self.frame_45.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_46 = QHBoxLayout(self.frame_45)
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.horizontalLayout_46.setContentsMargins(-1, 2, -1, 2)
        self.LSgtolcheckBox = QCheckBox(self.frame_45)
        self.LSgtolcheckBox.setObjectName(u"LSgtolcheckBox")
        self.LSgtolcheckBox.setChecked(True)

        self.horizontalLayout_46.addWidget(self.LSgtolcheckBox)

        self.LSgtollineEdit = QLineEdit(self.frame_45)
        self.LSgtollineEdit.setObjectName(u"LSgtollineEdit")

        self.horizontalLayout_46.addWidget(self.LSgtollineEdit)


        self.verticalLayout_2.addWidget(self.frame_45)

        self.frame_46 = QFrame(self.groupBox)
        self.frame_46.setObjectName(u"frame_46")
        self.frame_46.setFrameShape(QFrame.StyledPanel)
        self.frame_46.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_47 = QHBoxLayout(self.frame_46)
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.horizontalLayout_47.setContentsMargins(-1, 2, -1, 2)
        self.label = QLabel(self.frame_46)
        self.label.setObjectName(u"label")

        self.horizontalLayout_47.addWidget(self.label)

        self.LSlosscomboBox = QComboBox(self.frame_46)
        self.LSlosscomboBox.addItem("")
        self.LSlosscomboBox.addItem("")
        self.LSlosscomboBox.addItem("")
        self.LSlosscomboBox.addItem("")
        self.LSlosscomboBox.addItem("")
        self.LSlosscomboBox.setObjectName(u"LSlosscomboBox")

        self.horizontalLayout_47.addWidget(self.LSlosscomboBox)


        self.verticalLayout_2.addWidget(self.frame_46)

        self.frame_47 = QFrame(self.groupBox)
        self.frame_47.setObjectName(u"frame_47")
        self.frame_47.setFrameShape(QFrame.StyledPanel)
        self.frame_47.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_48 = QHBoxLayout(self.frame_47)
        self.horizontalLayout_48.setObjectName(u"horizontalLayout_48")
        self.horizontalLayout_48.setContentsMargins(-1, 2, -1, 2)
        self.label_2 = QLabel(self.frame_47)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_48.addWidget(self.label_2)

        self.LSf_scalelineEdit = QLineEdit(self.frame_47)
        self.LSf_scalelineEdit.setObjectName(u"LSf_scalelineEdit")

        self.horizontalLayout_48.addWidget(self.LSf_scalelineEdit)


        self.verticalLayout_2.addWidget(self.frame_47)

        self.frame_3 = QFrame(self.groupBox)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 2, -1, 2)
        self.LSmax_nfevcheckBox = QCheckBox(self.frame_3)
        self.LSmax_nfevcheckBox.setObjectName(u"LSmax_nfevcheckBox")

        self.horizontalLayout.addWidget(self.LSmax_nfevcheckBox)

        self.LSmax_nfevlineEdit = QLineEdit(self.frame_3)
        self.LSmax_nfevlineEdit.setObjectName(u"LSmax_nfevlineEdit")
        self.LSmax_nfevlineEdit.setEnabled(False)

        self.horizontalLayout.addWidget(self.LSmax_nfevlineEdit)


        self.verticalLayout_2.addWidget(self.frame_3)

        self.frame_48 = QFrame(self.groupBox)
        self.frame_48.setObjectName(u"frame_48")
        self.frame_48.setFrameShape(QFrame.StyledPanel)
        self.frame_48.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_50 = QHBoxLayout(self.frame_48)
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.horizontalLayout_50.setContentsMargins(-1, 2, -1, 2)
        self.LStr_solvercheckBox = QCheckBox(self.frame_48)
        self.LStr_solvercheckBox.setObjectName(u"LStr_solvercheckBox")

        self.horizontalLayout_50.addWidget(self.LStr_solvercheckBox)

        self.LStr_solvercomboBox = QComboBox(self.frame_48)
        self.LStr_solvercomboBox.addItem("")
        self.LStr_solvercomboBox.addItem("")
        self.LStr_solvercomboBox.setObjectName(u"LStr_solvercomboBox")
        self.LStr_solvercomboBox.setEnabled(False)

        self.horizontalLayout_50.addWidget(self.LStr_solvercomboBox)


        self.verticalLayout_2.addWidget(self.frame_48)


        self.verticalLayout_6.addWidget(self.groupBox)

        self.tabWidget.addTab(self.ls, "")
        self.basinhopping = QWidget()
        self.basinhopping.setObjectName(u"basinhopping")
        self.verticalLayout_10 = QVBoxLayout(self.basinhopping)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.groupBox_8 = QGroupBox(self.basinhopping)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_6 = QLabel(self.groupBox_8)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setWordWrap(True)

        self.verticalLayout_7.addWidget(self.label_6)

        self.label_7 = QLabel(self.groupBox_8)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.verticalLayout_7.addWidget(self.label_7)

        self.frame_5 = QFrame(self.groupBox_8)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_17 = QLabel(self.frame_5)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_4.addWidget(self.label_17)

        self.basinniterlineEdit = QLineEdit(self.frame_5)
        self.basinniterlineEdit.setObjectName(u"basinniterlineEdit")

        self.horizontalLayout_4.addWidget(self.basinniterlineEdit)


        self.verticalLayout_7.addWidget(self.frame_5)

        self.frame_4 = QFrame(self.groupBox_8)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_18 = QLabel(self.frame_4)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_6.addWidget(self.label_18)

        self.basinTlineEdit = QLineEdit(self.frame_4)
        self.basinTlineEdit.setObjectName(u"basinTlineEdit")

        self.horizontalLayout_6.addWidget(self.basinTlineEdit)


        self.verticalLayout_7.addWidget(self.frame_4)

        self.frame_6 = QFrame(self.groupBox_8)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_19 = QLabel(self.frame_6)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_7.addWidget(self.label_19)

        self.basinstepsizelineEdit = QLineEdit(self.frame_6)
        self.basinstepsizelineEdit.setObjectName(u"basinstepsizelineEdit")

        self.horizontalLayout_7.addWidget(self.basinstepsizelineEdit)


        self.verticalLayout_7.addWidget(self.frame_6)

        self.frame_7 = QFrame(self.groupBox_8)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_20 = QLabel(self.frame_7)
        self.label_20.setObjectName(u"label_20")

        self.horizontalLayout_8.addWidget(self.label_20)

        self.basinintervallineEdit = QLineEdit(self.frame_7)
        self.basinintervallineEdit.setObjectName(u"basinintervallineEdit")

        self.horizontalLayout_8.addWidget(self.basinintervallineEdit)


        self.verticalLayout_7.addWidget(self.frame_7)

        self.frame_8 = QFrame(self.groupBox_8)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.basinniter_successcheckBox = QCheckBox(self.frame_8)
        self.basinniter_successcheckBox.setObjectName(u"basinniter_successcheckBox")

        self.horizontalLayout_9.addWidget(self.basinniter_successcheckBox)

        self.basinniter_successlineEdit = QLineEdit(self.frame_8)
        self.basinniter_successlineEdit.setObjectName(u"basinniter_successlineEdit")
        self.basinniter_successlineEdit.setEnabled(False)

        self.horizontalLayout_9.addWidget(self.basinniter_successlineEdit)


        self.verticalLayout_7.addWidget(self.frame_8)

        self.frame_9 = QFrame(self.groupBox_8)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.basinseedcheckBox = QCheckBox(self.frame_9)
        self.basinseedcheckBox.setObjectName(u"basinseedcheckBox")

        self.horizontalLayout_10.addWidget(self.basinseedcheckBox)

        self.basinseedlineEdit = QLineEdit(self.frame_9)
        self.basinseedlineEdit.setObjectName(u"basinseedlineEdit")
        self.basinseedlineEdit.setEnabled(False)

        self.horizontalLayout_10.addWidget(self.basinseedlineEdit)


        self.verticalLayout_7.addWidget(self.frame_9)


        self.verticalLayout_10.addWidget(self.groupBox_8)

        self.tabWidget.addTab(self.basinhopping, "")
        self.dualannealing = QWidget()
        self.dualannealing.setObjectName(u"dualannealing")
        self.verticalLayout_9 = QVBoxLayout(self.dualannealing)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.groupBox_7 = QGroupBox(self.dualannealing)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(-1, 0, -1, 0)
        self.label_8 = QLabel(self.groupBox_7)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setWordWrap(True)

        self.verticalLayout_11.addWidget(self.label_8)

        self.label_9 = QLabel(self.groupBox_7)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.verticalLayout_11.addWidget(self.label_9)

        self.frame_17 = QFrame(self.groupBox_7)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_21 = QLabel(self.frame_17)
        self.label_21.setObjectName(u"label_21")

        self.horizontalLayout_11.addWidget(self.label_21)

        self.annealmaxiterlineEdit = QLineEdit(self.frame_17)
        self.annealmaxiterlineEdit.setObjectName(u"annealmaxiterlineEdit")

        self.horizontalLayout_11.addWidget(self.annealmaxiterlineEdit)


        self.verticalLayout_11.addWidget(self.frame_17)

        self.frame_16 = QFrame(self.groupBox_7)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_22 = QLabel(self.frame_16)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout_12.addWidget(self.label_22)

        self.annealinitial_templineEdit = QLineEdit(self.frame_16)
        self.annealinitial_templineEdit.setObjectName(u"annealinitial_templineEdit")

        self.horizontalLayout_12.addWidget(self.annealinitial_templineEdit)


        self.verticalLayout_11.addWidget(self.frame_16)

        self.frame_15 = QFrame(self.groupBox_7)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_23 = QLabel(self.frame_15)
        self.label_23.setObjectName(u"label_23")

        self.horizontalLayout_13.addWidget(self.label_23)

        self.annealrestart_temp_ratiolineEdit = QLineEdit(self.frame_15)
        self.annealrestart_temp_ratiolineEdit.setObjectName(u"annealrestart_temp_ratiolineEdit")

        self.horizontalLayout_13.addWidget(self.annealrestart_temp_ratiolineEdit)


        self.verticalLayout_11.addWidget(self.frame_15)

        self.frame_14 = QFrame(self.groupBox_7)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_24 = QLabel(self.frame_14)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout_14.addWidget(self.label_24)

        self.annealvisitlineEdit = QLineEdit(self.frame_14)
        self.annealvisitlineEdit.setObjectName(u"annealvisitlineEdit")

        self.horizontalLayout_14.addWidget(self.annealvisitlineEdit)


        self.verticalLayout_11.addWidget(self.frame_14)

        self.frame_13 = QFrame(self.groupBox_7)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_25 = QLabel(self.frame_13)
        self.label_25.setObjectName(u"label_25")

        self.horizontalLayout_15.addWidget(self.label_25)

        self.annealacceptlineEdit = QLineEdit(self.frame_13)
        self.annealacceptlineEdit.setObjectName(u"annealacceptlineEdit")

        self.horizontalLayout_15.addWidget(self.annealacceptlineEdit)


        self.verticalLayout_11.addWidget(self.frame_13)

        self.frame_12 = QFrame(self.groupBox_7)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_26 = QLabel(self.frame_12)
        self.label_26.setObjectName(u"label_26")

        self.horizontalLayout_16.addWidget(self.label_26)

        self.annealmaxfunlineEdit = QLineEdit(self.frame_12)
        self.annealmaxfunlineEdit.setObjectName(u"annealmaxfunlineEdit")

        self.horizontalLayout_16.addWidget(self.annealmaxfunlineEdit)


        self.verticalLayout_11.addWidget(self.frame_12)

        self.frame_11 = QFrame(self.groupBox_7)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.annealseedcheckBox = QCheckBox(self.frame_11)
        self.annealseedcheckBox.setObjectName(u"annealseedcheckBox")

        self.horizontalLayout_17.addWidget(self.annealseedcheckBox)

        self.annealseedlineEdit = QLineEdit(self.frame_11)
        self.annealseedlineEdit.setObjectName(u"annealseedlineEdit")
        self.annealseedlineEdit.setEnabled(False)

        self.horizontalLayout_17.addWidget(self.annealseedlineEdit)


        self.verticalLayout_11.addWidget(self.frame_11)

        self.frame_10 = QFrame(self.groupBox_7)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.annealno_local_searchcheckBox = QCheckBox(self.frame_10)
        self.annealno_local_searchcheckBox.setObjectName(u"annealno_local_searchcheckBox")

        self.horizontalLayout_18.addWidget(self.annealno_local_searchcheckBox)


        self.verticalLayout_11.addWidget(self.frame_10)


        self.verticalLayout_9.addWidget(self.groupBox_7)

        self.tabWidget.addTab(self.dualannealing, "")
        self.differentialevolution = QWidget()
        self.differentialevolution.setObjectName(u"differentialevolution")
        self.verticalLayout_12 = QVBoxLayout(self.differentialevolution)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.groupBox_9 = QGroupBox(self.differentialevolution)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.verticalLayout_14 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(-1, 0, -1, 0)
        self.label_10 = QLabel(self.groupBox_9)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setWordWrap(True)

        self.verticalLayout_14.addWidget(self.label_10)

        self.label_11 = QLabel(self.groupBox_9)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.verticalLayout_14.addWidget(self.label_11)

        self.frame_18 = QFrame(self.groupBox_9)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_19.setSpacing(6)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(-1, 2, -1, 2)
        self.label_27 = QLabel(self.frame_18)
        self.label_27.setObjectName(u"label_27")

        self.horizontalLayout_19.addWidget(self.label_27)

        self.diffevolstrategycomboBox = QComboBox(self.frame_18)
        self.diffevolstrategycomboBox.addItem("")
        self.diffevolstrategycomboBox.addItem("")
        self.diffevolstrategycomboBox.addItem("")
        self.diffevolstrategycomboBox.addItem("")
        self.diffevolstrategycomboBox.addItem("")
        self.diffevolstrategycomboBox.addItem("")
        self.diffevolstrategycomboBox.addItem("")
        self.diffevolstrategycomboBox.addItem("")
        self.diffevolstrategycomboBox.addItem("")
        self.diffevolstrategycomboBox.addItem("")
        self.diffevolstrategycomboBox.addItem("")
        self.diffevolstrategycomboBox.addItem("")
        self.diffevolstrategycomboBox.setObjectName(u"diffevolstrategycomboBox")

        self.horizontalLayout_19.addWidget(self.diffevolstrategycomboBox)


        self.verticalLayout_14.addWidget(self.frame_18)

        self.frame_19 = QFrame(self.groupBox_9)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_19)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(-1, 2, -1, 2)
        self.label_28 = QLabel(self.frame_19)
        self.label_28.setObjectName(u"label_28")

        self.horizontalLayout_20.addWidget(self.label_28)

        self.diffevolmaxiterlineEdit = QLineEdit(self.frame_19)
        self.diffevolmaxiterlineEdit.setObjectName(u"diffevolmaxiterlineEdit")

        self.horizontalLayout_20.addWidget(self.diffevolmaxiterlineEdit)


        self.verticalLayout_14.addWidget(self.frame_19)

        self.frame_20 = QFrame(self.groupBox_9)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setFrameShape(QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(-1, 2, -1, 2)
        self.label_29 = QLabel(self.frame_20)
        self.label_29.setObjectName(u"label_29")

        self.horizontalLayout_21.addWidget(self.label_29)

        self.diffevolpopsizelineEdit = QLineEdit(self.frame_20)
        self.diffevolpopsizelineEdit.setObjectName(u"diffevolpopsizelineEdit")

        self.horizontalLayout_21.addWidget(self.diffevolpopsizelineEdit)


        self.verticalLayout_14.addWidget(self.frame_20)

        self.frame_21 = QFrame(self.groupBox_9)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_21)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(-1, 2, -1, 2)
        self.label_30 = QLabel(self.frame_21)
        self.label_30.setObjectName(u"label_30")

        self.horizontalLayout_22.addWidget(self.label_30)

        self.diffevoltollineEdit = QLineEdit(self.frame_21)
        self.diffevoltollineEdit.setObjectName(u"diffevoltollineEdit")

        self.horizontalLayout_22.addWidget(self.diffevoltollineEdit)


        self.verticalLayout_14.addWidget(self.frame_21)

        self.frame_22 = QFrame(self.groupBox_9)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setFrameShape(QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_22)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(-1, 2, -1, 2)
        self.label_31 = QLabel(self.frame_22)
        self.label_31.setObjectName(u"label_31")

        self.horizontalLayout_23.addWidget(self.label_31)

        self.diffevolmutationAlineEdit = QLineEdit(self.frame_22)
        self.diffevolmutationAlineEdit.setObjectName(u"diffevolmutationAlineEdit")

        self.horizontalLayout_23.addWidget(self.diffevolmutationAlineEdit)

        self.diffevolmutationBlineEdit = QLineEdit(self.frame_22)
        self.diffevolmutationBlineEdit.setObjectName(u"diffevolmutationBlineEdit")

        self.horizontalLayout_23.addWidget(self.diffevolmutationBlineEdit)


        self.verticalLayout_14.addWidget(self.frame_22)

        self.frame_23 = QFrame(self.groupBox_9)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setFrameShape(QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.frame_23)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(-1, 2, -1, 2)
        self.label_32 = QLabel(self.frame_23)
        self.label_32.setObjectName(u"label_32")

        self.horizontalLayout_24.addWidget(self.label_32)

        self.diffevolrecombinationlineEdit = QLineEdit(self.frame_23)
        self.diffevolrecombinationlineEdit.setObjectName(u"diffevolrecombinationlineEdit")

        self.horizontalLayout_24.addWidget(self.diffevolrecombinationlineEdit)


        self.verticalLayout_14.addWidget(self.frame_23)

        self.frame_24 = QFrame(self.groupBox_9)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setFrameShape(QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_24)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(-1, 2, -1, 2)
        self.diffevolseedcheckBox = QCheckBox(self.frame_24)
        self.diffevolseedcheckBox.setObjectName(u"diffevolseedcheckBox")

        self.horizontalLayout_25.addWidget(self.diffevolseedcheckBox)

        self.diffevolseedlineEdit = QLineEdit(self.frame_24)
        self.diffevolseedlineEdit.setObjectName(u"diffevolseedlineEdit")
        self.diffevolseedlineEdit.setEnabled(False)

        self.horizontalLayout_25.addWidget(self.diffevolseedlineEdit)


        self.verticalLayout_14.addWidget(self.frame_24)

        self.frame_25 = QFrame(self.groupBox_9)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setFrameShape(QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_26 = QHBoxLayout(self.frame_25)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(-1, 2, -1, 2)
        self.diffevolpolishcheckBox = QCheckBox(self.frame_25)
        self.diffevolpolishcheckBox.setObjectName(u"diffevolpolishcheckBox")
        self.diffevolpolishcheckBox.setChecked(True)

        self.horizontalLayout_26.addWidget(self.diffevolpolishcheckBox)


        self.verticalLayout_14.addWidget(self.frame_25)

        self.frame_26 = QFrame(self.groupBox_9)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setFrameShape(QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.frame_26)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(-1, 2, -1, 2)
        self.label_33 = QLabel(self.frame_26)
        self.label_33.setObjectName(u"label_33")

        self.horizontalLayout_27.addWidget(self.label_33)

        self.diffevolinitcomboBox = QComboBox(self.frame_26)
        self.diffevolinitcomboBox.addItem("")
        self.diffevolinitcomboBox.addItem("")
        self.diffevolinitcomboBox.setObjectName(u"diffevolinitcomboBox")

        self.horizontalLayout_27.addWidget(self.diffevolinitcomboBox)


        self.verticalLayout_14.addWidget(self.frame_26)

        self.frame_27 = QFrame(self.groupBox_9)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setFrameShape(QFrame.StyledPanel)
        self.frame_27.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_27)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(-1, 2, -1, 2)
        self.label_34 = QLabel(self.frame_27)
        self.label_34.setObjectName(u"label_34")

        self.horizontalLayout_28.addWidget(self.label_34)

        self.diffevolatollineEdit = QLineEdit(self.frame_27)
        self.diffevolatollineEdit.setObjectName(u"diffevolatollineEdit")

        self.horizontalLayout_28.addWidget(self.diffevolatollineEdit)


        self.verticalLayout_14.addWidget(self.frame_27)

        self.frame_28 = QFrame(self.groupBox_9)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setFrameShape(QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.frame_28)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(-1, 2, -1, 2)
        self.label_35 = QLabel(self.frame_28)
        self.label_35.setObjectName(u"label_35")

        self.horizontalLayout_29.addWidget(self.label_35)

        self.diffevolupdatingcomboBox = QComboBox(self.frame_28)
        self.diffevolupdatingcomboBox.addItem("")
        self.diffevolupdatingcomboBox.addItem("")
        self.diffevolupdatingcomboBox.setObjectName(u"diffevolupdatingcomboBox")

        self.horizontalLayout_29.addWidget(self.diffevolupdatingcomboBox)


        self.verticalLayout_14.addWidget(self.frame_28)


        self.verticalLayout_12.addWidget(self.groupBox_9)

        self.tabWidget.addTab(self.differentialevolution, "")
        self.shgo = QWidget()
        self.shgo.setObjectName(u"shgo")
        self.verticalLayout_20 = QVBoxLayout(self.shgo)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.groupBox_12 = QGroupBox(self.shgo)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.verticalLayout_17 = QVBoxLayout(self.groupBox_12)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.label_12 = QLabel(self.groupBox_12)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setWordWrap(True)

        self.verticalLayout_17.addWidget(self.label_12)

        self.label_13 = QLabel(self.groupBox_12)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font)

        self.verticalLayout_17.addWidget(self.label_13)

        self.frame_30 = QFrame(self.groupBox_12)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setFrameShape(QFrame.StyledPanel)
        self.frame_30.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_31 = QHBoxLayout(self.frame_30)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setContentsMargins(-1, 2, -1, 2)
        self.label_36 = QLabel(self.frame_30)
        self.label_36.setObjectName(u"label_36")

        self.horizontalLayout_31.addWidget(self.label_36)

        self.SHGOnlineEdit = QLineEdit(self.frame_30)
        self.SHGOnlineEdit.setObjectName(u"SHGOnlineEdit")

        self.horizontalLayout_31.addWidget(self.SHGOnlineEdit)


        self.verticalLayout_17.addWidget(self.frame_30)

        self.frame_31 = QFrame(self.groupBox_12)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setFrameShape(QFrame.StyledPanel)
        self.frame_31.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_32 = QHBoxLayout(self.frame_31)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalLayout_32.setContentsMargins(-1, 2, -1, 2)
        self.label_37 = QLabel(self.frame_31)
        self.label_37.setObjectName(u"label_37")

        self.horizontalLayout_32.addWidget(self.label_37)

        self.SHGOiterslineEdit = QLineEdit(self.frame_31)
        self.SHGOiterslineEdit.setObjectName(u"SHGOiterslineEdit")

        self.horizontalLayout_32.addWidget(self.SHGOiterslineEdit)


        self.verticalLayout_17.addWidget(self.frame_31)

        self.frame_32 = QFrame(self.groupBox_12)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setFrameShape(QFrame.StyledPanel)
        self.frame_32.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_33 = QHBoxLayout(self.frame_32)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalLayout_33.setContentsMargins(-1, 2, -1, 2)
        self.SHGOmaxfevcheckBox = QCheckBox(self.frame_32)
        self.SHGOmaxfevcheckBox.setObjectName(u"SHGOmaxfevcheckBox")

        self.horizontalLayout_33.addWidget(self.SHGOmaxfevcheckBox)

        self.SHGOmaxfevlineEdit = QLineEdit(self.frame_32)
        self.SHGOmaxfevlineEdit.setObjectName(u"SHGOmaxfevlineEdit")
        self.SHGOmaxfevlineEdit.setEnabled(False)

        self.horizontalLayout_33.addWidget(self.SHGOmaxfevlineEdit)


        self.verticalLayout_17.addWidget(self.frame_32)

        self.frame_33 = QFrame(self.groupBox_12)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setFrameShape(QFrame.StyledPanel)
        self.frame_33.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_34 = QHBoxLayout(self.frame_33)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalLayout_34.setContentsMargins(-1, 2, -1, 2)
        self.SHGOf_mincheckBox = QCheckBox(self.frame_33)
        self.SHGOf_mincheckBox.setObjectName(u"SHGOf_mincheckBox")

        self.horizontalLayout_34.addWidget(self.SHGOf_mincheckBox)

        self.SHGOf_minlineEdit = QLineEdit(self.frame_33)
        self.SHGOf_minlineEdit.setObjectName(u"SHGOf_minlineEdit")
        self.SHGOf_minlineEdit.setEnabled(False)

        self.horizontalLayout_34.addWidget(self.SHGOf_minlineEdit)


        self.verticalLayout_17.addWidget(self.frame_33)

        self.frame_34 = QFrame(self.groupBox_12)
        self.frame_34.setObjectName(u"frame_34")
        self.frame_34.setFrameShape(QFrame.StyledPanel)
        self.frame_34.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_35 = QHBoxLayout(self.frame_34)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalLayout_35.setContentsMargins(-1, 2, -1, 2)
        self.label_39 = QLabel(self.frame_34)
        self.label_39.setObjectName(u"label_39")

        self.horizontalLayout_35.addWidget(self.label_39)

        self.SHGOf_tollineEdit = QLineEdit(self.frame_34)
        self.SHGOf_tollineEdit.setObjectName(u"SHGOf_tollineEdit")

        self.horizontalLayout_35.addWidget(self.SHGOf_tollineEdit)


        self.verticalLayout_17.addWidget(self.frame_34)

        self.frame_35 = QFrame(self.groupBox_12)
        self.frame_35.setObjectName(u"frame_35")
        self.frame_35.setFrameShape(QFrame.StyledPanel)
        self.frame_35.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_36 = QHBoxLayout(self.frame_35)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.horizontalLayout_36.setContentsMargins(-1, 2, -1, 2)
        self.SHGOmaxitercheckBox = QCheckBox(self.frame_35)
        self.SHGOmaxitercheckBox.setObjectName(u"SHGOmaxitercheckBox")

        self.horizontalLayout_36.addWidget(self.SHGOmaxitercheckBox)

        self.SHGOmaxiterlineEdit = QLineEdit(self.frame_35)
        self.SHGOmaxiterlineEdit.setObjectName(u"SHGOmaxiterlineEdit")
        self.SHGOmaxiterlineEdit.setEnabled(False)

        self.horizontalLayout_36.addWidget(self.SHGOmaxiterlineEdit)


        self.verticalLayout_17.addWidget(self.frame_35)

        self.frame_36 = QFrame(self.groupBox_12)
        self.frame_36.setObjectName(u"frame_36")
        self.frame_36.setFrameShape(QFrame.StyledPanel)
        self.frame_36.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_37 = QHBoxLayout(self.frame_36)
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.horizontalLayout_37.setContentsMargins(-1, 2, -1, 2)
        self.SHGOmaxevcheckBox = QCheckBox(self.frame_36)
        self.SHGOmaxevcheckBox.setObjectName(u"SHGOmaxevcheckBox")

        self.horizontalLayout_37.addWidget(self.SHGOmaxevcheckBox)

        self.SHGOmaxevlineEdit = QLineEdit(self.frame_36)
        self.SHGOmaxevlineEdit.setObjectName(u"SHGOmaxevlineEdit")
        self.SHGOmaxevlineEdit.setEnabled(False)

        self.horizontalLayout_37.addWidget(self.SHGOmaxevlineEdit)


        self.verticalLayout_17.addWidget(self.frame_36)

        self.frame_37 = QFrame(self.groupBox_12)
        self.frame_37.setObjectName(u"frame_37")
        self.frame_37.setFrameShape(QFrame.StyledPanel)
        self.frame_37.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_38 = QHBoxLayout(self.frame_37)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.horizontalLayout_38.setContentsMargins(-1, 2, -1, 2)
        self.SHGOmaxtimecheckBox = QCheckBox(self.frame_37)
        self.SHGOmaxtimecheckBox.setObjectName(u"SHGOmaxtimecheckBox")

        self.horizontalLayout_38.addWidget(self.SHGOmaxtimecheckBox)

        self.SHGOmaxtimelineEdit = QLineEdit(self.frame_37)
        self.SHGOmaxtimelineEdit.setObjectName(u"SHGOmaxtimelineEdit")
        self.SHGOmaxtimelineEdit.setEnabled(False)

        self.horizontalLayout_38.addWidget(self.SHGOmaxtimelineEdit)


        self.verticalLayout_17.addWidget(self.frame_37)

        self.frame_38 = QFrame(self.groupBox_12)
        self.frame_38.setObjectName(u"frame_38")
        self.frame_38.setFrameShape(QFrame.StyledPanel)
        self.frame_38.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_39 = QHBoxLayout(self.frame_38)
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.horizontalLayout_39.setContentsMargins(-1, 2, -1, 2)
        self.SHGOminhgrdcheckBox = QCheckBox(self.frame_38)
        self.SHGOminhgrdcheckBox.setObjectName(u"SHGOminhgrdcheckBox")

        self.horizontalLayout_39.addWidget(self.SHGOminhgrdcheckBox)

        self.SHGOminhgrdlineEdit = QLineEdit(self.frame_38)
        self.SHGOminhgrdlineEdit.setObjectName(u"SHGOminhgrdlineEdit")
        self.SHGOminhgrdlineEdit.setEnabled(False)

        self.horizontalLayout_39.addWidget(self.SHGOminhgrdlineEdit)


        self.verticalLayout_17.addWidget(self.frame_38)

        self.frame_40 = QFrame(self.groupBox_12)
        self.frame_40.setObjectName(u"frame_40")
        self.frame_40.setFrameShape(QFrame.StyledPanel)
        self.frame_40.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_41 = QHBoxLayout(self.frame_40)
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.horizontalLayout_41.setContentsMargins(-1, 2, -1, 2)
        self.SHGOminimize_every_itercheckBox = QCheckBox(self.frame_40)
        self.SHGOminimize_every_itercheckBox.setObjectName(u"SHGOminimize_every_itercheckBox")

        self.horizontalLayout_41.addWidget(self.SHGOminimize_every_itercheckBox)


        self.verticalLayout_17.addWidget(self.frame_40)

        self.frame_41 = QFrame(self.groupBox_12)
        self.frame_41.setObjectName(u"frame_41")
        self.frame_41.setFrameShape(QFrame.StyledPanel)
        self.frame_41.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_42 = QHBoxLayout(self.frame_41)
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.horizontalLayout_42.setContentsMargins(-1, 2, -1, 2)
        self.SHGOlocal_itercheckBox = QCheckBox(self.frame_41)
        self.SHGOlocal_itercheckBox.setObjectName(u"SHGOlocal_itercheckBox")

        self.horizontalLayout_42.addWidget(self.SHGOlocal_itercheckBox)


        self.verticalLayout_17.addWidget(self.frame_41)

        self.frame_42 = QFrame(self.groupBox_12)
        self.frame_42.setObjectName(u"frame_42")
        self.frame_42.setFrameShape(QFrame.StyledPanel)
        self.frame_42.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_43 = QHBoxLayout(self.frame_42)
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.horizontalLayout_43.setContentsMargins(-1, 2, -1, 2)
        self.SHGOinfty_constraintscheckBox = QCheckBox(self.frame_42)
        self.SHGOinfty_constraintscheckBox.setObjectName(u"SHGOinfty_constraintscheckBox")
        self.SHGOinfty_constraintscheckBox.setChecked(True)

        self.horizontalLayout_43.addWidget(self.SHGOinfty_constraintscheckBox)


        self.verticalLayout_17.addWidget(self.frame_42)

        self.frame_43 = QFrame(self.groupBox_12)
        self.frame_43.setObjectName(u"frame_43")
        self.frame_43.setFrameShape(QFrame.StyledPanel)
        self.frame_43.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_44 = QHBoxLayout(self.frame_43)
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.horizontalLayout_44.setContentsMargins(-1, 2, -1, 2)
        self.label_38 = QLabel(self.frame_43)
        self.label_38.setObjectName(u"label_38")

        self.horizontalLayout_44.addWidget(self.label_38)

        self.SHGOsampling_methodcomboBox = QComboBox(self.frame_43)
        self.SHGOsampling_methodcomboBox.addItem("")
        self.SHGOsampling_methodcomboBox.addItem("")
        self.SHGOsampling_methodcomboBox.setObjectName(u"SHGOsampling_methodcomboBox")

        self.horizontalLayout_44.addWidget(self.SHGOsampling_methodcomboBox)


        self.verticalLayout_17.addWidget(self.frame_43)


        self.verticalLayout_20.addWidget(self.groupBox_12)

        self.tabWidget.addTab(self.shgo, "")
        self.brute = QWidget()
        self.brute.setObjectName(u"brute")
        self.verticalLayout_5 = QVBoxLayout(self.brute)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_2 = QGroupBox(self.brute)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_14 = QLabel(self.groupBox_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_14)

        self.label_15 = QLabel(self.groupBox_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font)

        self.verticalLayout_3.addWidget(self.label_15)

        self.frame_44 = QFrame(self.groupBox_2)
        self.frame_44.setObjectName(u"frame_44")
        self.frame_44.setFrameShape(QFrame.StyledPanel)
        self.frame_44.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_45 = QHBoxLayout(self.frame_44)
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.label_40 = QLabel(self.frame_44)
        self.label_40.setObjectName(u"label_40")

        self.horizontalLayout_45.addWidget(self.label_40)

        self.BruteNslineEdit = QLineEdit(self.frame_44)
        self.BruteNslineEdit.setObjectName(u"BruteNslineEdit")

        self.horizontalLayout_45.addWidget(self.BruteNslineEdit)


        self.verticalLayout_3.addWidget(self.frame_44)


        self.verticalLayout_5.addWidget(self.groupBox_2)

        self.tabWidget.addTab(self.brute, "")

        self.verticalLayout.addWidget(self.tabWidget)

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
        self.LSftolcheckBox.toggled.connect(self.LSftollineEdit.setEnabled)
        self.LSxtolcheckBox.toggled.connect(self.LSxtollineEdit.setEnabled)
        self.LSgtolcheckBox.toggled.connect(self.LSgtollineEdit.setEnabled)
        self.LSmax_nfevcheckBox.toggled.connect(self.LSmax_nfevlineEdit.setEnabled)
        self.LStr_solvercheckBox.toggled.connect(self.LStr_solvercomboBox.setEnabled)
        self.basinniter_successcheckBox.toggled.connect(self.basinniter_successlineEdit.setEnabled)
        self.annealseedcheckBox.toggled.connect(self.annealseedlineEdit.setEnabled)
        self.diffevolseedcheckBox.toggled.connect(self.diffevolseedlineEdit.setEnabled)
        self.SHGOmaxevcheckBox.toggled.connect(self.SHGOmaxfevlineEdit.setEnabled)
        self.SHGOf_mincheckBox.toggled.connect(self.SHGOf_minlineEdit.setEnabled)
        self.SHGOmaxitercheckBox.toggled.connect(self.SHGOmaxiterlineEdit.setEnabled)
        self.SHGOmaxevcheckBox.toggled.connect(self.SHGOmaxevlineEdit.setEnabled)
        self.SHGOmaxtimecheckBox.toggled.connect(self.SHGOmaxtimelineEdit.setEnabled)
        self.SHGOminhgrdcheckBox.toggled.connect(self.SHGOminhgrdlineEdit.setEnabled)
        self.basinseedcheckBox.toggled.connect(self.basinseedlineEdit.setEnabled)
        self.SHGOmaxfevcheckBox.toggled.connect(self.SHGOmaxfevlineEdit.setEnabled)

        self.tabWidget.setCurrentIndex(5)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Fitting Options", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Least Squares Minimization", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Available methods are:\n"
"- Trust Region Reflective algorithm, particularly suitable for large sparse problems with bounds. Generally robust method (DEFAULT).\n"
"- \u2018dogbox\u2019 : dogleg algorithm with rectangular trust regions, typical use case is small problems with bounds. Not recommended for problems with rank-deficient Jacobian.\n"
"- \u2018lm\u2019 : Levenberg-Marquardt algorithm as implemented in MINPACK. Doesn\u2019t handle bounds and sparse Jacobians. Usually the most efficient method for small unconstrained problems.", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Local Method", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"method", None))
        self.LSmethodcomboBox.setItemText(0, QCoreApplication.translate("Dialog", u"trf", None))
        self.LSmethodcomboBox.setItemText(1, QCoreApplication.translate("Dialog", u"dogbox", None))
        self.LSmethodcomboBox.setItemText(2, QCoreApplication.translate("Dialog", u"lm", None))

#if QT_CONFIG(tooltip)
        self.LSmethodcomboBox.setToolTip(QCoreApplication.translate("Dialog", u"- Trust Region Reflective algorithm, particularly suitable for large sparse problems with bounds. Generally robust method (DEFAULT).\n"
"- \u2018dogbox\u2019 : dogleg algorithm with rectangular trust regions, typical use case is small problems with bounds. Not recommended for problems with rank-deficient Jacobian.\n"
"- \u2018lm\u2019 : Levenberg-Marquardt algorithm as implemented in MINPACK. Doesn\u2019t handle bounds and sparse Jacobians. Usually the most efficient method for small unconstrained problems.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_16.setToolTip(QCoreApplication.translate("Dialog", u"Finite difference scheme for numerical estimation of the Jacobian matrix: \n"
"- \u20182-point\u2019 (default)\n"
"- \u20183-point\u2019: more accurate, but requires twice as many operations as 2-point. \n"
"- \u2018cs\u2019 uses complex steps, and while potentially the most accurate, it is applicable only when fun correctly handles complex inputs and can be analytically continued to the complex plane. \n"
"Method \u2018lm\u2019 always uses the \u20182-point\u2019 scheme.", None))
#endif // QT_CONFIG(tooltip)
        self.label_16.setText(QCoreApplication.translate("Dialog", u"jac", None))
        self.LSjaccomboBox.setItemText(0, QCoreApplication.translate("Dialog", u"2-point", None))
        self.LSjaccomboBox.setItemText(1, QCoreApplication.translate("Dialog", u"3-point", None))
        self.LSjaccomboBox.setItemText(2, QCoreApplication.translate("Dialog", u"cs", None))

#if QT_CONFIG(tooltip)
        self.LSjaccomboBox.setToolTip(QCoreApplication.translate("Dialog", u"Finite difference scheme for numerical estimation of the Jacobian matrix: \n"
"- \u20182-point\u2019 (default)\n"
"- \u20183-point\u2019: more accurate, but requires twice as many operations as 2-point. \n"
"- \u2018cs\u2019 uses complex steps, and while potentially the most accurate, it is applicable only when fun correctly handles complex inputs and can be analytically continued to the complex plane. \n"
"Method \u2018lm\u2019 always uses the \u20182-point\u2019 scheme.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.LSftolcheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Tolerance for termination by the change of the cost function. Default is 1e-8. The optimization process is stopped when dF < ftol * F, and there was an adequate agreement between a local quadratic model and the true model in the last step.", None))
#endif // QT_CONFIG(tooltip)
        self.LSftolcheckBox.setText(QCoreApplication.translate("Dialog", u"ftol", None))
#if QT_CONFIG(tooltip)
        self.LSftollineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Tolerance for termination by the change of the cost function. Default is 1e-8. The optimization process is stopped when dF < ftol * F, and there was an adequate agreement between a local quadratic model and the true model in the last step.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.LSxtolcheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Tolerance for termination by the change of the independent variables. Default is 1e-8. The exact condition depends on the method used:\n"
"\n"
"For \u2018trf\u2019 and \u2018dogbox\u2019 : norm(dx) < xtol * (xtol + norm(x))\n"
"\n"
"For \u2018lm\u2019 : Delta < xtol * norm(xs), where Delta is a trust-region radius and xs is the value of x scaled according to x_scale parameter (see below).", None))
#endif // QT_CONFIG(tooltip)
        self.LSxtolcheckBox.setText(QCoreApplication.translate("Dialog", u"xtol", None))
#if QT_CONFIG(tooltip)
        self.LSxtollineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Tolerance for termination by the change of the independent variables. Default is 1e-8. The exact condition depends on the method used:\n"
"\n"
"For \u2018trf\u2019 and \u2018dogbox\u2019 : norm(dx) < xtol * (xtol + norm(x))\n"
"\n"
"For \u2018lm\u2019 : Delta < xtol * norm(xs), where Delta is a trust-region radius and xs is the value of x scaled according to x_scale parameter (see below).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.LSgtolcheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Tolerance for termination by the norm of the gradient. Default is 1e-8. The exact condition depends on a method used:\n"
"\n"
"For \u2018trf\u2019 : norm(g_scaled, ord=np.inf) < gtol, where g_scaled is the value of the gradient scaled to account for the presence of the bounds [STIR].\n"
"\n"
"For \u2018dogbox\u2019 : norm(g_free, ord=np.inf) < gtol, where g_free is the gradient with respect to the variables which are not in the optimal state on the boundary.\n"
"\n"
"For \u2018lm\u2019 : the maximum absolute value of the cosine of angles between columns of the Jacobian and the residual vector is less than gtol, or the residual vector is zero.", None))
#endif // QT_CONFIG(tooltip)
        self.LSgtolcheckBox.setText(QCoreApplication.translate("Dialog", u"gtol", None))
#if QT_CONFIG(tooltip)
        self.LSgtollineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Tolerance for termination by the norm of the gradient. Default is 1e-8. The exact condition depends on a method used:\n"
"\n"
"For \u2018trf\u2019 : norm(g_scaled, ord=np.inf) < gtol, where g_scaled is the value of the gradient scaled to account for the presence of the bounds [STIR].\n"
"\n"
"For \u2018dogbox\u2019 : norm(g_free, ord=np.inf) < gtol, where g_free is the gradient with respect to the variables which are not in the optimal state on the boundary.\n"
"\n"
"For \u2018lm\u2019 : the maximum absolute value of the cosine of angles between columns of the Jacobian and the residual vector is less than gtol, or the residual vector is zero.", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Dialog", u"loss", None))
        self.LSlosscomboBox.setItemText(0, QCoreApplication.translate("Dialog", u"linear", None))
        self.LSlosscomboBox.setItemText(1, QCoreApplication.translate("Dialog", u"soft_l1", None))
        self.LSlosscomboBox.setItemText(2, QCoreApplication.translate("Dialog", u"huber", None))
        self.LSlosscomboBox.setItemText(3, QCoreApplication.translate("Dialog", u"cauchy", None))
        self.LSlosscomboBox.setItemText(4, QCoreApplication.translate("Dialog", u"arctan", None))

#if QT_CONFIG(tooltip)
        self.LSlosscomboBox.setToolTip(QCoreApplication.translate("Dialog", u"Determines the loss function. The following keyword values are allowed:\n"
"- \u2018linear\u2019 (default) : rho(z) = z. Gives a standard least-squares problem.\n"
"- \u2018soft_l1\u2019 : rho(z) = 2 * ((1 + z)**0.5 - 1). The smooth approximation of l1 (absolute value) loss. Usually a good choice for robust least squares.\n"
"- \u2018huber\u2019 : rho(z) = z if z <= 1 else 2*z^0.5 - 1. Works similarly to \u2018soft_l1\u2019. \n"
"- \u2018cauchy\u2019 : rho(z) = ln(1 + z). Severely weakens outliers influence, but may cause difficulties in optimization process.\n"
"- \u2018arctan\u2019 : rho(z) = arctan(z). Limits a maximum loss on a single residual, has properties similar to \u2018cauchy\u2019.\n"
" Method \u2018lm\u2019 supports only \u2018linear\u2019 loss.", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Dialog", u"f_scale", None))
#if QT_CONFIG(tooltip)
        self.LSf_scalelineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Value of soft margin between inlier and outlier residuals, default is 1.0. The loss function is evaluated as follows rho_(f**2) = C**2 * rho(f**2 / C**2), where C is f_scale, and rho is determined by loss parameter. This parameter has no effect with loss='linear', but for other loss values it is of crucial importance.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.LSmax_nfevcheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Maximum number of function evaluations before the termination. If None (default), the value is chosen automatically:\n"
"\n"
"For \u2018trf\u2019 and \u2018dogbox\u2019 : 100 * n.\n"
"\n"
"For \u2018lm\u2019 : 100 * n if jac is callable and 100 * n * (n + 1) otherwise (because \u2018lm\u2019 counts function calls in Jacobian estimation).", None))
#endif // QT_CONFIG(tooltip)
        self.LSmax_nfevcheckBox.setText(QCoreApplication.translate("Dialog", u"max_nfev", None))
#if QT_CONFIG(tooltip)
        self.LSmax_nfevlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Maximum number of function evaluations before the termination. If None (default), the value is chosen automatically:\n"
"\n"
"For \u2018trf\u2019 and \u2018dogbox\u2019 : 100 * n.\n"
"\n"
"For \u2018lm\u2019 : 100 * n if jac is callable and 100 * n * (n + 1) otherwise (because \u2018lm\u2019 counts function calls in Jacobian estimation).", None))
#endif // QT_CONFIG(tooltip)
        self.LStr_solvercheckBox.setText(QCoreApplication.translate("Dialog", u"tr_solver", None))
        self.LStr_solvercomboBox.setItemText(0, QCoreApplication.translate("Dialog", u"exact", None))
        self.LStr_solvercomboBox.setItemText(1, QCoreApplication.translate("Dialog", u"lsmr", None))

#if QT_CONFIG(tooltip)
        self.LStr_solvercomboBox.setToolTip(QCoreApplication.translate("Dialog", u"Method for solving trust-region subproblems, relevant only for \u2018trf\u2019 and \u2018dogbox\u2019 methods.\n"
"\n"
"\u2018exact\u2019 is suitable for not very large problems with dense Jacobian matrices. The computational complexity per iteration is comparable to a singular value decomposition of the Jacobian matrix.\n"
"\n"
"\u2018lsmr\u2019 is suitable for problems with sparse and large Jacobian matrices. It uses the iterative procedure scipy.sparse.linalg.lsmr for finding a solution of a linear least-squares problem and only requires matrix-vector product evaluations.\n"
"\n"
"If None (default) the solver is chosen based on the type of Jacobian returned on the first iteration.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ls), QCoreApplication.translate("Dialog", u"LS", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Dialog", u"Basin Hopping", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Basin-hopping is a two-phase method that combines a global stepping algorithm with local minimization at each step.", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Global Method", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"niter", None))
#if QT_CONFIG(tooltip)
        self.basinniterlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"number of basin-hopping iterations", None))
#endif // QT_CONFIG(tooltip)
        self.label_18.setText(QCoreApplication.translate("Dialog", u"T", None))
#if QT_CONFIG(tooltip)
        self.basinTlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"\u201ctemperature\u201d parameter for the accept or reject criterion", None))
#endif // QT_CONFIG(tooltip)
        self.label_19.setText(QCoreApplication.translate("Dialog", u"stepsize", None))
#if QT_CONFIG(tooltip)
        self.basinstepsizelineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Maximum step size for use in the random displacement", None))
#endif // QT_CONFIG(tooltip)
        self.label_20.setText(QCoreApplication.translate("Dialog", u"interval", None))
#if QT_CONFIG(tooltip)
        self.basinintervallineEdit.setToolTip(QCoreApplication.translate("Dialog", u"interval for how often to update the stepsize", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.basinniter_successcheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Stop the run if the global minimum candidate remains the same for this number of iterations", None))
#endif // QT_CONFIG(tooltip)
        self.basinniter_successcheckBox.setText(QCoreApplication.translate("Dialog", u"niter_success", None))
#if QT_CONFIG(tooltip)
        self.basinniter_successlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Stop the run if the global minimum candidate remains the same for this number of iterations", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.basinseedcheckBox.setToolTip(QCoreApplication.translate("Dialog", u"seed for random numbers", None))
#endif // QT_CONFIG(tooltip)
        self.basinseedcheckBox.setText(QCoreApplication.translate("Dialog", u"seed", None))
#if QT_CONFIG(tooltip)
        self.basinseedlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"seed for random numbers", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.basinhopping), QCoreApplication.translate("Dialog", u"Basin", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Dialog", u"Dual Annealing", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Find the global minimum of a function using Dual Annealing.\n"
"\n"
"", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Global Method", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"maxiter", None))
#if QT_CONFIG(tooltip)
        self.annealmaxiterlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"The maximum number of global search iterations. Default value is 1000", None))
#endif // QT_CONFIG(tooltip)
        self.label_22.setText(QCoreApplication.translate("Dialog", u"initial_temp", None))
#if QT_CONFIG(tooltip)
        self.annealinitial_templineEdit.setToolTip(QCoreApplication.translate("Dialog", u"initial temperature, use higher values to facilitates a wider search of the energy landscape, allowing dual_annealing to escape local minima that it is trapped in. Default value is 5230. Range is (0.01, 5.e4]", None))
#endif // QT_CONFIG(tooltip)
        self.label_23.setText(QCoreApplication.translate("Dialog", u"restart_temp_ratio", None))
#if QT_CONFIG(tooltip)
        self.annealrestart_temp_ratiolineEdit.setToolTip(QCoreApplication.translate("Dialog", u"During the annealing process, temperature is decreasing, when it reaches initial_temp * restart_temp_ratio, the reannealing process is triggered. Default value of the ratio is 2e-5. Range is (0, 1).", None))
#endif // QT_CONFIG(tooltip)
        self.label_24.setText(QCoreApplication.translate("Dialog", u"visit", None))
#if QT_CONFIG(tooltip)
        self.annealvisitlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Parameter for visiting distribution. Default value is 2.62. Higher values give the visiting distribution a heavier tail, this makes the algorithm jump to a more distant region. The value range is (0, 3].", None))
#endif // QT_CONFIG(tooltip)
        self.label_25.setText(QCoreApplication.translate("Dialog", u"accept", None))
#if QT_CONFIG(tooltip)
        self.annealacceptlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Parameter for acceptance distribution. It is used to control the probability of acceptance. The lower the acceptance parameter, the smaller the probability of acceptance. Default value is -5.0 with a range (-1e4, -5].", None))
#endif // QT_CONFIG(tooltip)
        self.label_26.setText(QCoreApplication.translate("Dialog", u"maxfun", None))
#if QT_CONFIG(tooltip)
        self.annealmaxfunlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Soft limit for the number of objective function calls. If the algorithm is in the middle of a local search, this number will be exceeded, the algorithm will stop just after the local search is done. Default value is 1e7.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.annealseedcheckBox.setToolTip(QCoreApplication.translate("Dialog", u"seed for random numbers", None))
#endif // QT_CONFIG(tooltip)
        self.annealseedcheckBox.setText(QCoreApplication.translate("Dialog", u"seed", None))
#if QT_CONFIG(tooltip)
        self.annealseedlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"seed for random numbers", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.annealno_local_searchcheckBox.setToolTip(QCoreApplication.translate("Dialog", u"a traditional Generalized Simulated Annealing will be performed with no local search strategy applied", None))
#endif // QT_CONFIG(tooltip)
        self.annealno_local_searchcheckBox.setText(QCoreApplication.translate("Dialog", u"no_local_search", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dualannealing), QCoreApplication.translate("Dialog", u"Annealing", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("Dialog", u"Differential Evolution", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Stochastic method to find the minimum, and can search large areas of candidate space, but often requires larger numbers of function evaluations than conventional gradient based techniques.", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Global Method", None))
        self.label_27.setText(QCoreApplication.translate("Dialog", u"strategy", None))
        self.diffevolstrategycomboBox.setItemText(0, QCoreApplication.translate("Dialog", u"best1bin", None))
        self.diffevolstrategycomboBox.setItemText(1, QCoreApplication.translate("Dialog", u"best1exp", None))
        self.diffevolstrategycomboBox.setItemText(2, QCoreApplication.translate("Dialog", u"rand1exp", None))
        self.diffevolstrategycomboBox.setItemText(3, QCoreApplication.translate("Dialog", u"randtobest1exp", None))
        self.diffevolstrategycomboBox.setItemText(4, QCoreApplication.translate("Dialog", u"currenttobest1exp", None))
        self.diffevolstrategycomboBox.setItemText(5, QCoreApplication.translate("Dialog", u"best2exp", None))
        self.diffevolstrategycomboBox.setItemText(6, QCoreApplication.translate("Dialog", u"rand2exp", None))
        self.diffevolstrategycomboBox.setItemText(7, QCoreApplication.translate("Dialog", u"randtobest1bin", None))
        self.diffevolstrategycomboBox.setItemText(8, QCoreApplication.translate("Dialog", u"currenttobest1bin", None))
        self.diffevolstrategycomboBox.setItemText(9, QCoreApplication.translate("Dialog", u"best2bin", None))
        self.diffevolstrategycomboBox.setItemText(10, QCoreApplication.translate("Dialog", u"rand2bin", None))
        self.diffevolstrategycomboBox.setItemText(11, QCoreApplication.translate("Dialog", u"rand1bin", None))

#if QT_CONFIG(tooltip)
        self.diffevolstrategycomboBox.setToolTip(QCoreApplication.translate("Dialog", u"The differential evolution strategy to use. The default is \u2018best1bin\u2019.", None))
#endif // QT_CONFIG(tooltip)
        self.label_28.setText(QCoreApplication.translate("Dialog", u"maxiter", None))
#if QT_CONFIG(tooltip)
        self.diffevolmaxiterlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"The maximum number of generations over which the entire population is evolved. The maximum number of function evaluations (with no polishing) is: (maxiter + 1) * popsize * len(x)", None))
#endif // QT_CONFIG(tooltip)
        self.label_29.setText(QCoreApplication.translate("Dialog", u"popsize", None))
#if QT_CONFIG(tooltip)
        self.diffevolpopsizelineEdit.setToolTip(QCoreApplication.translate("Dialog", u"A multiplier for setting the total population size. The population has popsize * len(x) individuals", None))
#endif // QT_CONFIG(tooltip)
        self.label_30.setText(QCoreApplication.translate("Dialog", u"tol", None))
#if QT_CONFIG(tooltip)
        self.diffevoltollineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Relative tolerance for convergence, the solving stops when np.std(pop) <= atol + tol * np.abs(np.mean(population_energies)), where and atol and tol are the absolute and relative tolerance respectively.", None))
#endif // QT_CONFIG(tooltip)
        self.label_31.setText(QCoreApplication.translate("Dialog", u"mutation", None))
#if QT_CONFIG(tooltip)
        self.diffevolmutationAlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"The mutation constant, also known as differential weight.If specified as a tuple (min, max) dithering is employed. Dithering randomly changes the mutation constant on a generation by generation basis. The mutation constant for that generation is taken from U[min, max). Dithering can help speed convergence significantly. Increasing the mutation constant increases the search radius, but will slow down convergence.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.diffevolmutationBlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"The mutation constant, also known as differential weight.If specified as a tuple (min, max) dithering is employed. Dithering randomly changes the mutation constant on a generation by generation basis. The mutation constant for that generation is taken from U[min, max). Dithering can help speed convergence significantly. Increasing the mutation constant increases the search radius, but will slow down convergence.", None))
#endif // QT_CONFIG(tooltip)
        self.label_32.setText(QCoreApplication.translate("Dialog", u"recombination", None))
#if QT_CONFIG(tooltip)
        self.diffevolrecombinationlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"The recombination constant, also known as the crossover probability, in the range [0, 1]. Increasing this value allows a larger number of mutants to progress into the next generation, but at the risk of population stability.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.diffevolseedcheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Seed for random numbers", None))
#endif // QT_CONFIG(tooltip)
        self.diffevolseedcheckBox.setText(QCoreApplication.translate("Dialog", u"seed", None))
#if QT_CONFIG(tooltip)
        self.diffevolseedlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Seed for random numbers", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.diffevolpolishcheckBox.setToolTip(QCoreApplication.translate("Dialog", u"If True (default), then scipy.optimize.minimize with the L-BFGS-B method is used to polish the best population member at the end, which can improve the minimization slightly. If a constrained problem is being studied then the trust-constr method is used instead.", None))
#endif // QT_CONFIG(tooltip)
        self.diffevolpolishcheckBox.setText(QCoreApplication.translate("Dialog", u"polish", None))
        self.label_33.setText(QCoreApplication.translate("Dialog", u"init", None))
        self.diffevolinitcomboBox.setItemText(0, QCoreApplication.translate("Dialog", u"latinhypercube", None))
        self.diffevolinitcomboBox.setItemText(1, QCoreApplication.translate("Dialog", u"random", None))

#if QT_CONFIG(tooltip)
        self.diffevolinitcomboBox.setToolTip(QCoreApplication.translate("Dialog", u"Specify which type of population initialization is performed. The default is \u2018latinhypercube\u2019. Latin Hypercube sampling tries to maximize coverage of the available parameter space. \u2018random\u2019 initializes the population randomly - this has the drawback that clustering can occur, preventing the whole of parameter space being covered.", None))
#endif // QT_CONFIG(tooltip)
        self.label_34.setText(QCoreApplication.translate("Dialog", u"atol", None))
#if QT_CONFIG(tooltip)
        self.diffevolatollineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Absolute tolerance for convergence, the solving stops when np.std(pop) <= atol + tol * np.abs(np.mean(population_energies)), where and atol and tol are the absolute and relative tolerance respectively.", None))
#endif // QT_CONFIG(tooltip)
        self.label_35.setText(QCoreApplication.translate("Dialog", u"updating", None))
        self.diffevolupdatingcomboBox.setItemText(0, QCoreApplication.translate("Dialog", u"immediate", None))
        self.diffevolupdatingcomboBox.setItemText(1, QCoreApplication.translate("Dialog", u"deferred", None))

#if QT_CONFIG(tooltip)
        self.diffevolupdatingcomboBox.setToolTip(QCoreApplication.translate("Dialog", u"If 'immediate', the best solution vector is continuously updated within a single generation. This can lead to faster convergence as trial vectors can take advantage of continuous improvements in the best solution. With 'deferred', the best solution vector is updated once per generation.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.differentialevolution), QCoreApplication.translate("Dialog", u"Evolution", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("Dialog", u"SHGO", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Finds the global minimum of a function using simplicial homology global optimization.", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Global Method", None))
        self.label_36.setText(QCoreApplication.translate("Dialog", u"n", None))
#if QT_CONFIG(tooltip)
        self.SHGOnlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Number of sampling points used in the construction of the simplicial complex. Note that this argument is only used for sobol", None))
#endif // QT_CONFIG(tooltip)
        self.label_37.setText(QCoreApplication.translate("Dialog", u"iters", None))
#if QT_CONFIG(tooltip)
        self.SHGOiterslineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Number of iterations used in the construction of the simplicial complex.", None))
#endif // QT_CONFIG(tooltip)
        self.SHGOmaxfevcheckBox.setText(QCoreApplication.translate("Dialog", u"maxfev", None))
#if QT_CONFIG(tooltip)
        self.SHGOmaxfevlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Maximum number of function evaluations in the feasible domain.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.SHGOf_mincheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Specify the minimum objective function value, if it is known.", None))
#endif // QT_CONFIG(tooltip)
        self.SHGOf_mincheckBox.setText(QCoreApplication.translate("Dialog", u"f_min", None))
#if QT_CONFIG(tooltip)
        self.SHGOf_minlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Specify the minimum objective function value, if it is known.", None))
#endif // QT_CONFIG(tooltip)
        self.label_39.setText(QCoreApplication.translate("Dialog", u"f_tol", None))
#if QT_CONFIG(tooltip)
        self.SHGOf_tollineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Precision goal for the value of f in the stopping criterion. Note that the global routine will also terminate if a sampling point in the global routine is within this tolerance.\n"
"\n"
"", None))
#endif // QT_CONFIG(tooltip)
        self.SHGOmaxitercheckBox.setText(QCoreApplication.translate("Dialog", u"maxiter", None))
#if QT_CONFIG(tooltip)
        self.SHGOmaxiterlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Maximum number of iterations to perform.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.SHGOmaxevcheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Maximum number of sampling evaluations to perform (includes searching in infeasible points).", None))
#endif // QT_CONFIG(tooltip)
        self.SHGOmaxevcheckBox.setText(QCoreApplication.translate("Dialog", u"maxev", None))
#if QT_CONFIG(tooltip)
        self.SHGOmaxevlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Maximum number of sampling evaluations to perform (includes searching in infeasible points).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.SHGOmaxtimecheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Maximum processing runtime allowed", None))
#endif // QT_CONFIG(tooltip)
        self.SHGOmaxtimecheckBox.setText(QCoreApplication.translate("Dialog", u"maxtime", None))
#if QT_CONFIG(tooltip)
        self.SHGOmaxtimelineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Maximum processing runtime allowed", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.SHGOminhgrdcheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Minimum homology group rank differential. The homology group of the objective function is calculated (approximately) during every iteration. The rank of this group has a one-to-one correspondence with the number of locally convex subdomains in the objective function (after adequate sampling points each of these subdomains contain a unique global minimum). If the difference in the hgr is 0 between iterations for maxhgrd specified iterations the algorithm will terminate.", None))
#endif // QT_CONFIG(tooltip)
        self.SHGOminhgrdcheckBox.setText(QCoreApplication.translate("Dialog", u"minhgrd", None))
#if QT_CONFIG(tooltip)
        self.SHGOminhgrdlineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Minimum homology group rank differential. The homology group of the objective function is calculated (approximately) during every iteration. The rank of this group has a one-to-one correspondence with the number of locally convex subdomains in the objective function (after adequate sampling points each of these subdomains contain a unique global minimum). If the difference in the hgr is 0 between iterations for maxhgrd specified iterations the algorithm will terminate.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.SHGOminimize_every_itercheckBox.setToolTip(QCoreApplication.translate("Dialog", u"If True then promising global sampling points will be passed to a local minimisation routine every iteration. If False then only the final minimiser pool will be run.", None))
#endif // QT_CONFIG(tooltip)
        self.SHGOminimize_every_itercheckBox.setText(QCoreApplication.translate("Dialog", u"minimize_every_iter", None))
#if QT_CONFIG(tooltip)
        self.SHGOlocal_itercheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Only evaluate a few of the best minimiser pool candidates every iteration. If False all potential points are passed to the local minimisation routine.", None))
#endif // QT_CONFIG(tooltip)
        self.SHGOlocal_itercheckBox.setText(QCoreApplication.translate("Dialog", u"local_iter", None))
#if QT_CONFIG(tooltip)
        self.SHGOinfty_constraintscheckBox.setToolTip(QCoreApplication.translate("Dialog", u"If True then any sampling points generated which are outside will the feasible domain will be saved and given an objective function value of inf. If False then these points will be discarded. Using this functionality could lead to higher performance with respect to function evaluations before the global minimum is found, specifying False will use less memory at the cost of a slight decrease in performance. Defaults to True.", None))
#endif // QT_CONFIG(tooltip)
        self.SHGOinfty_constraintscheckBox.setText(QCoreApplication.translate("Dialog", u"infty_constraints", None))
        self.label_38.setText(QCoreApplication.translate("Dialog", u"sampling_method", None))
        self.SHGOsampling_methodcomboBox.setItemText(0, QCoreApplication.translate("Dialog", u"simplicial", None))
        self.SHGOsampling_methodcomboBox.setItemText(1, QCoreApplication.translate("Dialog", u"sobol", None))

#if QT_CONFIG(tooltip)
        self.SHGOsampling_methodcomboBox.setToolTip(QCoreApplication.translate("Dialog", u"The default simplicial uses less memory and provides the theoretical guarantee of convergence to the global minimum in finite time. The sobol method is faster in terms of sampling point generation at the cost of higher memory resources and the loss of guaranteed convergence. It is more appropriate for most \u201ceasier\u201d problems where the convergence is relatively fast. ", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.shgo), QCoreApplication.translate("Dialog", u"SHGO", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Brute Force", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Minimize a function over a given range by brute force, i.e. it computes the function\u2019s value at each point of a multidimensional grid of points, to find the global minimum of the function. It is inefficient because the number of grid points increases exponentially - the number of grid points to evaluate is Ns ** len(x). Consequently, even with coarse grid spacing, even moderately sized problems can take a long time to run, and/or run into memory limitations.\n"
"\n"
"The program finds the gridpoint at which the lowest value of the objective function occurs. When the global minimum occurs within (or not very far outside) the grid\u2019s boundaries, and the grid is fine enough, that point will be in the neighborhood of the global minimum.", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Global Method", None))
        self.label_40.setText(QCoreApplication.translate("Dialog", u"Ns", None))
#if QT_CONFIG(tooltip)
        self.BruteNslineEdit.setToolTip(QCoreApplication.translate("Dialog", u"Number of grid points along the axes", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.brute), QCoreApplication.translate("Dialog", u"Brute", None))
        self.pushCancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.pushOK.setText(QCoreApplication.translate("Dialog", u"OK", None))
    # retranslateUi

