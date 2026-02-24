# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'markerSettings.ui'
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
    QDoubleSpinBox, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QToolButton, QVBoxLayout, QWidget)
from . import Reptate_rc
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(451, 582)
        icon = QIcon()
        icon.addFile(u":/Images/Images/new_icons/icons8-color-wheel-2.png", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setLayoutDirection(Qt.RightToLeft)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        font = QFont()
        font.setBold(True)
        self.tabWidget.setFont(font)
        self.tabWidget.setLayoutDirection(Qt.LeftToRight)
        self.data = QWidget()
        self.data.setObjectName(u"data")
        self.verticalLayout_6 = QVBoxLayout(self.data)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox = QGroupBox(self.data)
        self.groupBox.setObjectName(u"groupBox")
        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(True)
        self.groupBox.setFont(font1)
        self.groupBox.setLayoutDirection(Qt.LeftToRight)
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox_3 = QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.cbSymbolType = QComboBox(self.groupBox_3)
        self.cbSymbolType.setObjectName(u"cbSymbolType")
        self.cbSymbolType.setEnabled(True)
        font2 = QFont()
        font2.setBold(False)
        self.cbSymbolType.setFont(font2)

        self.verticalLayout_2.addWidget(self.cbSymbolType)

        self.rbFixedSymbol = QRadioButton(self.groupBox_3)
        self.rbFixedSymbol.setObjectName(u"rbFixedSymbol")
        self.rbFixedSymbol.setFont(font2)
        self.rbFixedSymbol.setChecked(True)

        self.verticalLayout_2.addWidget(self.rbFixedSymbol)

        self.rbVariableSymbol = QRadioButton(self.groupBox_3)
        self.rbVariableSymbol.setObjectName(u"rbVariableSymbol")
        self.rbVariableSymbol.setFont(font2)
        self.rbVariableSymbol.setChecked(False)

        self.verticalLayout_2.addWidget(self.rbVariableSymbol)

        self.spinBoxLineW = QDoubleSpinBox(self.groupBox_3)
        self.spinBoxLineW.setObjectName(u"spinBoxLineW")
        font3 = QFont()
        font3.setPointSize(13)
        font3.setBold(False)
        self.spinBoxLineW.setFont(font3)
        self.spinBoxLineW.setDecimals(1)
        self.spinBoxLineW.setMinimum(0.100000000000000)
        self.spinBoxLineW.setMaximum(10.000000000000000)
        self.spinBoxLineW.setSingleStep(0.100000000000000)
        self.spinBoxLineW.setValue(1.000000000000000)

        self.verticalLayout_2.addWidget(self.spinBoxLineW)


        self.horizontalLayout.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.spinBox = QSpinBox(self.groupBox_4)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setFont(font2)
        self.spinBox.setMaximum(40)
        self.spinBox.setSingleStep(3)
        self.spinBox.setValue(12)

        self.verticalLayout_3.addWidget(self.spinBox)

        self.rbEmpty = QRadioButton(self.groupBox_4)
        self.rbEmpty.setObjectName(u"rbEmpty")
        self.rbEmpty.setFont(font2)
        self.rbEmpty.setChecked(True)

        self.verticalLayout_3.addWidget(self.rbEmpty)

        self.rbFilled = QRadioButton(self.groupBox_4)
        self.rbFilled.setObjectName(u"rbFilled")
        self.rbFilled.setFont(font2)

        self.verticalLayout_3.addWidget(self.rbFilled)


        self.horizontalLayout.addWidget(self.groupBox_4)


        self.verticalLayout_6.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.data)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font1)
        self.groupBox_2.setLayoutDirection(Qt.LeftToRight)
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBox_5 = QGroupBox(self.groupBox_2)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.rbFixedColor = QRadioButton(self.groupBox_5)
        self.rbFixedColor.setObjectName(u"rbFixedColor")
        self.rbFixedColor.setFont(font2)

        self.verticalLayout_5.addWidget(self.rbFixedColor)

        self.rbGradientColor = QRadioButton(self.groupBox_5)
        self.rbGradientColor.setObjectName(u"rbGradientColor")
        self.rbGradientColor.setFont(font2)

        self.verticalLayout_5.addWidget(self.rbGradientColor)

        self.rbPalette = QRadioButton(self.groupBox_5)
        self.rbPalette.setObjectName(u"rbPalette")
        self.rbPalette.setFont(font2)
        self.rbPalette.setChecked(True)

        self.verticalLayout_5.addWidget(self.rbPalette)


        self.horizontalLayout_3.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(self.groupBox_2)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pickColor1 = QToolButton(self.groupBox_6)
        self.pickColor1.setObjectName(u"pickColor1")
        self.pickColor1.setEnabled(False)

        self.gridLayout.addWidget(self.pickColor1, 0, 2, 1, 1)

        self.labelPickedColor1 = QLabel(self.groupBox_6)
        self.labelPickedColor1.setObjectName(u"labelPickedColor1")
        self.labelPickedColor1.setEnabled(False)
        self.labelPickedColor1.setFont(font2)

        self.gridLayout.addWidget(self.labelPickedColor1, 0, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_6)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setEnabled(False)
        self.label_4.setFont(font2)

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_5 = QLabel(self.groupBox_6)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setEnabled(False)
        self.label_5.setFont(font2)

        self.horizontalLayout_4.addWidget(self.label_5)

        self.labelPickedColor2 = QLabel(self.groupBox_6)
        self.labelPickedColor2.setObjectName(u"labelPickedColor2")
        self.labelPickedColor2.setEnabled(False)
        self.labelPickedColor2.setFont(font2)

        self.horizontalLayout_4.addWidget(self.labelPickedColor2)

        self.pickColor2 = QToolButton(self.groupBox_6)
        self.pickColor2.setObjectName(u"pickColor2")
        self.pickColor2.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.pickColor2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.cbPalette = QComboBox(self.groupBox_6)
        self.cbPalette.setObjectName(u"cbPalette")
        self.cbPalette.setFont(font2)

        self.verticalLayout_4.addWidget(self.cbPalette)


        self.horizontalLayout_3.addWidget(self.groupBox_6)


        self.verticalLayout_6.addWidget(self.groupBox_2)

        self.tabWidget.addTab(self.data, "")
        self.theory = QWidget()
        self.theory.setObjectName(u"theory")
        self.verticalLayout_10 = QVBoxLayout(self.theory)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.groupBox_8 = QGroupBox(self.theory)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.cbTheoryLine = QComboBox(self.groupBox_8)
        self.cbTheoryLine.setObjectName(u"cbTheoryLine")
        self.cbTheoryLine.setFont(font2)

        self.verticalLayout_7.addWidget(self.cbTheoryLine)

        self.sbThLineWidth = QDoubleSpinBox(self.groupBox_8)
        self.sbThLineWidth.setObjectName(u"sbThLineWidth")
        self.sbThLineWidth.setFont(font3)
        self.sbThLineWidth.setDecimals(1)
        self.sbThLineWidth.setMinimum(0.100000000000000)
        self.sbThLineWidth.setMaximum(10.000000000000000)
        self.sbThLineWidth.setSingleStep(0.100000000000000)
        self.sbThLineWidth.setValue(1.000000000000000)

        self.verticalLayout_7.addWidget(self.sbThLineWidth)


        self.verticalLayout_10.addWidget(self.groupBox_8)

        self.groupBox_10 = QGroupBox(self.theory)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.verticalLayout_13 = QVBoxLayout(self.groupBox_10)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.rbThSameColor = QRadioButton(self.groupBox_10)
        self.rbThSameColor.setObjectName(u"rbThSameColor")
        self.rbThSameColor.setFont(font3)

        self.verticalLayout_8.addWidget(self.rbThSameColor)

        self.rbThFixedColor = QRadioButton(self.groupBox_10)
        self.rbThFixedColor.setObjectName(u"rbThFixedColor")
        self.rbThFixedColor.setFont(font3)

        self.verticalLayout_8.addWidget(self.rbThFixedColor)


        self.verticalLayout_13.addLayout(self.verticalLayout_8)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.labelThcol = QLabel(self.groupBox_10)
        self.labelThcol.setObjectName(u"labelThcol")

        self.horizontalLayout_6.addWidget(self.labelThcol)

        self.labelThPickedColor = QLabel(self.groupBox_10)
        self.labelThPickedColor.setObjectName(u"labelThPickedColor")

        self.horizontalLayout_6.addWidget(self.labelThPickedColor)

        self.pickThColor = QToolButton(self.groupBox_10)
        self.pickThColor.setObjectName(u"pickThColor")

        self.horizontalLayout_6.addWidget(self.pickThColor)


        self.verticalLayout_13.addLayout(self.horizontalLayout_6)


        self.verticalLayout_10.addWidget(self.groupBox_10)

        self.tabWidget.addTab(self.theory, "")
        self.legend = QWidget()
        self.legend.setObjectName(u"legend")
        self.verticalLayout_9 = QVBoxLayout(self.legend)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.cb_show_legend = QCheckBox(self.legend)
        self.cb_show_legend.setObjectName(u"cb_show_legend")
        self.cb_show_legend.setChecked(False)
        self.cb_show_legend.setTristate(False)

        self.verticalLayout_9.addWidget(self.cb_show_legend)

        self.groupBox_7 = QGroupBox(self.legend)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(-1, 0, -1, 0)
        self.frameLocation = QFrame(self.groupBox_7)
        self.frameLocation.setObjectName(u"frameLocation")
        self.frameLocation.setFrameShape(QFrame.NoFrame)
        self.frameLocation.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frameLocation)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frameLocation)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.locationComboBox = QComboBox(self.frameLocation)
        self.locationComboBox.addItem("")
        self.locationComboBox.addItem("")
        self.locationComboBox.addItem("")
        self.locationComboBox.addItem("")
        self.locationComboBox.addItem("")
        self.locationComboBox.addItem("")
        self.locationComboBox.addItem("")
        self.locationComboBox.addItem("")
        self.locationComboBox.addItem("")
        self.locationComboBox.addItem("")
        self.locationComboBox.addItem("")
        self.locationComboBox.setObjectName(u"locationComboBox")
        self.locationComboBox.setFont(font2)

        self.horizontalLayout_2.addWidget(self.locationComboBox)


        self.verticalLayout_11.addWidget(self.frameLocation)

        self.frameColumns = QFrame(self.groupBox_7)
        self.frameColumns.setObjectName(u"frameColumns")
        self.frameColumns.setFrameShape(QFrame.NoFrame)
        self.frameColumns.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frameColumns)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frameColumns)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_7.addWidget(self.label_2)

        self.colSpinBox = QSpinBox(self.frameColumns)
        self.colSpinBox.setObjectName(u"colSpinBox")
        self.colSpinBox.setFont(font2)
        self.colSpinBox.setMinimum(1)
        self.colSpinBox.setMaximum(10)

        self.horizontalLayout_7.addWidget(self.colSpinBox)


        self.verticalLayout_11.addWidget(self.frameColumns)

        self.frameFont = QFrame(self.groupBox_7)
        self.frameFont.setObjectName(u"frameFont")
        self.frameFont.setFrameShape(QFrame.NoFrame)
        self.frameFont.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frameFont)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.frameFont)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_8.addWidget(self.label_3)

        self.fontsizeSpinBox = QSpinBox(self.frameFont)
        self.fontsizeSpinBox.setObjectName(u"fontsizeSpinBox")
        self.fontsizeSpinBox.setFont(font2)
        self.fontsizeSpinBox.setMinimum(1)

        self.horizontalLayout_8.addWidget(self.fontsizeSpinBox)


        self.verticalLayout_11.addWidget(self.frameFont)

        self.frameBoolean = QFrame(self.groupBox_7)
        self.frameBoolean.setObjectName(u"frameBoolean")
        self.frameBoolean.setFrameShape(QFrame.NoFrame)
        self.frameBoolean.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frameBoolean)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.fancyboxCheckBox = QCheckBox(self.frameBoolean)
        self.fancyboxCheckBox.setObjectName(u"fancyboxCheckBox")

        self.gridLayout_2.addWidget(self.fancyboxCheckBox, 2, 0, 1, 1)

        self.markerfirstCheckBox = QCheckBox(self.frameBoolean)
        self.markerfirstCheckBox.setObjectName(u"markerfirstCheckBox")

        self.gridLayout_2.addWidget(self.markerfirstCheckBox, 0, 0, 1, 1)

        self.modeCheckBox = QCheckBox(self.frameBoolean)
        self.modeCheckBox.setObjectName(u"modeCheckBox")

        self.gridLayout_2.addWidget(self.modeCheckBox, 9, 0, 1, 1)

        self.shadowCheckBox = QCheckBox(self.frameBoolean)
        self.shadowCheckBox.setObjectName(u"shadowCheckBox")

        self.gridLayout_2.addWidget(self.shadowCheckBox, 3, 0, 1, 1)

        self.frameColors = QFrame(self.frameBoolean)
        self.frameColors.setObjectName(u"frameColors")
        self.frameColors.setFrameShape(QFrame.NoFrame)
        self.frameColors.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frameColors)
        self.horizontalLayout_10.setSpacing(20)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.facecolorCheckBox = QCheckBox(self.frameColors)
        self.facecolorCheckBox.setObjectName(u"facecolorCheckBox")

        self.horizontalLayout_17.addWidget(self.facecolorCheckBox)

        self.labelFaceColor = QLabel(self.frameColors)
        self.labelFaceColor.setObjectName(u"labelFaceColor")
        self.labelFaceColor.setEnabled(False)
        self.labelFaceColor.setFont(font2)

        self.horizontalLayout_17.addWidget(self.labelFaceColor)

        self.pickFaceColor = QToolButton(self.frameColors)
        self.pickFaceColor.setObjectName(u"pickFaceColor")
        self.pickFaceColor.setEnabled(False)

        self.horizontalLayout_17.addWidget(self.pickFaceColor)


        self.horizontalLayout_10.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.edgecolorCheckBox = QCheckBox(self.frameColors)
        self.edgecolorCheckBox.setObjectName(u"edgecolorCheckBox")

        self.horizontalLayout_18.addWidget(self.edgecolorCheckBox)

        self.labelEdgeColor = QLabel(self.frameColors)
        self.labelEdgeColor.setObjectName(u"labelEdgeColor")
        self.labelEdgeColor.setEnabled(False)
        self.labelEdgeColor.setFont(font2)

        self.horizontalLayout_18.addWidget(self.labelEdgeColor)

        self.pickEdgeColor = QToolButton(self.frameColors)
        self.pickEdgeColor.setObjectName(u"pickEdgeColor")
        self.pickEdgeColor.setEnabled(False)

        self.horizontalLayout_18.addWidget(self.pickEdgeColor)


        self.horizontalLayout_10.addLayout(self.horizontalLayout_18)


        self.gridLayout_2.addWidget(self.frameColors, 7, 0, 1, 1)

        self.frameTransparency = QFrame(self.frameBoolean)
        self.frameTransparency.setObjectName(u"frameTransparency")
        self.frameTransparency.setFrameShape(QFrame.NoFrame)
        self.frameTransparency.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frameTransparency)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.framealphaCheckBox = QCheckBox(self.frameTransparency)
        self.framealphaCheckBox.setObjectName(u"framealphaCheckBox")

        self.horizontalLayout_9.addWidget(self.framealphaCheckBox)

        self.framealphaSpinBox = QDoubleSpinBox(self.frameTransparency)
        self.framealphaSpinBox.setObjectName(u"framealphaSpinBox")
        self.framealphaSpinBox.setEnabled(False)
        self.framealphaSpinBox.setFont(font2)
        self.framealphaSpinBox.setMaximum(1.000000000000000)
        self.framealphaSpinBox.setSingleStep(0.050000000000000)

        self.horizontalLayout_9.addWidget(self.framealphaSpinBox)


        self.gridLayout_2.addWidget(self.frameTransparency, 4, 0, 1, 1)

        self.frameonCheckBox = QCheckBox(self.frameBoolean)
        self.frameonCheckBox.setObjectName(u"frameonCheckBox")

        self.gridLayout_2.addWidget(self.frameonCheckBox, 1, 0, 1, 1)


        self.verticalLayout_11.addWidget(self.frameBoolean)

        self.frameTitle = QFrame(self.groupBox_7)
        self.frameTitle.setObjectName(u"frameTitle")
        self.frameTitle.setFrameShape(QFrame.NoFrame)
        self.frameTitle.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frameTitle)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.legendtitleCheckBox = QCheckBox(self.frameTitle)
        self.legendtitleCheckBox.setObjectName(u"legendtitleCheckBox")

        self.horizontalLayout_11.addWidget(self.legendtitleCheckBox)

        self.legendtitleStr = QLineEdit(self.frameTitle)
        self.legendtitleStr.setObjectName(u"legendtitleStr")
        self.legendtitleStr.setEnabled(False)

        self.horizontalLayout_11.addWidget(self.legendtitleStr)


        self.verticalLayout_11.addWidget(self.frameTitle)

        self.borderpadframe = QFrame(self.groupBox_7)
        self.borderpadframe.setObjectName(u"borderpadframe")
        self.borderpadframe.setFrameShape(QFrame.NoFrame)
        self.borderpadframe.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.borderpadframe)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.borderpadCheckBox = QCheckBox(self.borderpadframe)
        self.borderpadCheckBox.setObjectName(u"borderpadCheckBox")

        self.horizontalLayout_13.addWidget(self.borderpadCheckBox)

        self.borderpadSpinBox = QDoubleSpinBox(self.borderpadframe)
        self.borderpadSpinBox.setObjectName(u"borderpadSpinBox")
        self.borderpadSpinBox.setEnabled(False)
        self.borderpadSpinBox.setFont(font2)
        self.borderpadSpinBox.setMaximum(1.000000000000000)
        self.borderpadSpinBox.setSingleStep(0.050000000000000)

        self.horizontalLayout_13.addWidget(self.borderpadSpinBox)


        self.verticalLayout_11.addWidget(self.borderpadframe)

        self.frame = QFrame(self.groupBox_7)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.labelspacingCheckBox = QCheckBox(self.frame)
        self.labelspacingCheckBox.setObjectName(u"labelspacingCheckBox")

        self.horizontalLayout_14.addWidget(self.labelspacingCheckBox)

        self.labelspacingSpinBox = QDoubleSpinBox(self.frame)
        self.labelspacingSpinBox.setObjectName(u"labelspacingSpinBox")
        self.labelspacingSpinBox.setEnabled(False)
        self.labelspacingSpinBox.setFont(font2)
        self.labelspacingSpinBox.setMaximum(2.000000000000000)
        self.labelspacingSpinBox.setSingleStep(0.100000000000000)

        self.horizontalLayout_14.addWidget(self.labelspacingSpinBox)


        self.verticalLayout_11.addWidget(self.frame)

        self.frame_2 = QFrame(self.groupBox_7)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.handletextpadCheckBox = QCheckBox(self.frame_2)
        self.handletextpadCheckBox.setObjectName(u"handletextpadCheckBox")

        self.horizontalLayout_15.addWidget(self.handletextpadCheckBox)

        self.handletextpadSpinBox = QDoubleSpinBox(self.frame_2)
        self.handletextpadSpinBox.setObjectName(u"handletextpadSpinBox")
        self.handletextpadSpinBox.setEnabled(False)
        self.handletextpadSpinBox.setFont(font2)
        self.handletextpadSpinBox.setMaximum(4.000000000000000)
        self.handletextpadSpinBox.setSingleStep(0.100000000000000)

        self.horizontalLayout_15.addWidget(self.handletextpadSpinBox)


        self.verticalLayout_11.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.groupBox_7)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.columnspacingCheckBox = QCheckBox(self.frame_3)
        self.columnspacingCheckBox.setObjectName(u"columnspacingCheckBox")

        self.horizontalLayout_16.addWidget(self.columnspacingCheckBox)

        self.columnspacingSpinBox = QDoubleSpinBox(self.frame_3)
        self.columnspacingSpinBox.setObjectName(u"columnspacingSpinBox")
        self.columnspacingSpinBox.setEnabled(False)
        self.columnspacingSpinBox.setFont(font2)
        self.columnspacingSpinBox.setMaximum(10.000000000000000)
        self.columnspacingSpinBox.setSingleStep(0.250000000000000)

        self.horizontalLayout_16.addWidget(self.columnspacingSpinBox)


        self.verticalLayout_11.addWidget(self.frame_3)

        self.frameLabelString = QFrame(self.groupBox_7)
        self.frameLabelString.setObjectName(u"frameLabelString")
        self.frameLabelString.setFrameShape(QFrame.NoFrame)
        self.frameLabelString.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frameLabelString)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.legendlabelCheckBox = QCheckBox(self.frameLabelString)
        self.legendlabelCheckBox.setObjectName(u"legendlabelCheckBox")

        self.horizontalLayout_12.addWidget(self.legendlabelCheckBox)

        self.legendlabelStr = QLineEdit(self.frameLabelString)
        self.legendlabelStr.setObjectName(u"legendlabelStr")
        self.legendlabelStr.setEnabled(False)
        self.legendlabelStr.setFont(font2)

        self.horizontalLayout_12.addWidget(self.legendlabelStr)


        self.verticalLayout_11.addWidget(self.frameLabelString)

        self.draggableCheckBox = QCheckBox(self.groupBox_7)
        self.draggableCheckBox.setObjectName(u"draggableCheckBox")

        self.verticalLayout_11.addWidget(self.draggableCheckBox)


        self.verticalLayout_9.addWidget(self.groupBox_7)

        self.tabWidget.addTab(self.legend, "")
        self.annotations = QWidget()
        self.annotations.setObjectName(u"annotations")
        self.verticalLayout_12 = QVBoxLayout(self.annotations)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.groupBox_9 = QGroupBox(self.annotations)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.verticalLayout_14 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(-1, 0, -1, 0)
        self.frame_5 = QFrame(self.groupBox_9)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.frame_5)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.frame_7 = QFrame(self.frame_5)
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
        self.rotationSpinBox.setFont(font2)
        self.rotationSpinBox.setDecimals(1)
        self.rotationSpinBox.setMaximum(360.000000000000000)

        self.horizontalLayout_21.addWidget(self.rotationSpinBox)


        self.verticalLayout_15.addWidget(self.frame_7)


        self.verticalLayout_14.addWidget(self.frame_5)

        self.frame_8 = QFrame(self.groupBox_9)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_8)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.label_11 = QLabel(self.frame_8)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_16.addWidget(self.label_11)

        self.frame_9 = QFrame(self.frame_8)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.label_12 = QLabel(self.frame_9)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_22.addWidget(self.label_12)

        self.hacomboBox = QComboBox(self.frame_9)
        self.hacomboBox.addItem("")
        self.hacomboBox.addItem("")
        self.hacomboBox.addItem("")
        self.hacomboBox.setObjectName(u"hacomboBox")
        self.hacomboBox.setFont(font2)

        self.horizontalLayout_22.addWidget(self.hacomboBox)

        self.label_13 = QLabel(self.frame_9)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_22.addWidget(self.label_13)

        self.vacomboBox = QComboBox(self.frame_9)
        self.vacomboBox.addItem("")
        self.vacomboBox.addItem("")
        self.vacomboBox.addItem("")
        self.vacomboBox.addItem("")
        self.vacomboBox.setObjectName(u"vacomboBox")
        self.vacomboBox.setFont(font2)

        self.horizontalLayout_22.addWidget(self.vacomboBox)


        self.verticalLayout_16.addWidget(self.frame_9)


        self.verticalLayout_14.addWidget(self.frame_8)

        self.frame_10 = QFrame(self.groupBox_9)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setSpacing(0)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.label_7 = QLabel(self.frame_10)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_23.addWidget(self.label_7)

        self.labelFontColor = QLabel(self.frame_10)
        self.labelFontColor.setObjectName(u"labelFontColor")
        self.labelFontColor.setEnabled(False)
        self.labelFontColor.setFont(font2)

        self.horizontalLayout_23.addWidget(self.labelFontColor)

        self.pickFontColor = QToolButton(self.frame_10)
        self.pickFontColor.setObjectName(u"pickFontColor")
        self.pickFontColor.setEnabled(True)

        self.horizontalLayout_23.addWidget(self.pickFontColor)


        self.horizontalLayout_25.addLayout(self.horizontalLayout_23)


        self.verticalLayout_14.addWidget(self.frame_10)

        self.frame_11 = QFrame(self.groupBox_9)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_26 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.label_14 = QLabel(self.frame_11)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_26.addWidget(self.label_14)

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
        self.fontweightComboBox.setFont(font2)

        self.horizontalLayout_26.addWidget(self.fontweightComboBox)

        self.label_15 = QLabel(self.frame_11)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_26.addWidget(self.label_15)

        self.fontstyleComboBox = QComboBox(self.frame_11)
        self.fontstyleComboBox.addItem("")
        self.fontstyleComboBox.addItem("")
        self.fontstyleComboBox.addItem("")
        self.fontstyleComboBox.setObjectName(u"fontstyleComboBox")
        self.fontstyleComboBox.setFont(font2)

        self.horizontalLayout_26.addWidget(self.fontstyleComboBox)


        self.verticalLayout_14.addWidget(self.frame_11)

        self.frame_12 = QFrame(self.groupBox_9)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.label_16 = QLabel(self.frame_12)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_27.addWidget(self.label_16)

        self.fontsizeannotationSpinBox = QSpinBox(self.frame_12)
        self.fontsizeannotationSpinBox.setObjectName(u"fontsizeannotationSpinBox")
        self.fontsizeannotationSpinBox.setFont(font2)
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
        self.framealphaannotationSpinBox.setFont(font2)
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
        self.label_17 = QLabel(self.frame_14)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_29.addWidget(self.label_17)

        self.fontfamilyComboBox = QComboBox(self.frame_14)
        self.fontfamilyComboBox.addItem("")
        self.fontfamilyComboBox.addItem("")
        self.fontfamilyComboBox.addItem("")
        self.fontfamilyComboBox.addItem("")
        self.fontfamilyComboBox.addItem("")
        self.fontfamilyComboBox.setObjectName(u"fontfamilyComboBox")
        self.fontfamilyComboBox.setFont(font2)

        self.horizontalLayout_29.addWidget(self.fontfamilyComboBox)


        self.verticalLayout_14.addWidget(self.frame_14)


        self.verticalLayout_12.addWidget(self.groupBox_9)

        self.tabWidget.addTab(self.annotations, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_20 = QVBoxLayout(self.tab)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.groupBox_12 = QGroupBox(self.tab)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.verticalLayout_17 = QVBoxLayout(self.groupBox_12)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.labelFontColor_label = QLabel(self.groupBox_12)
        self.labelFontColor_label.setObjectName(u"labelFontColor_label")

        self.gridLayout_3.addWidget(self.labelFontColor_label, 0, 1, 1, 1)

        self.pickFontColor_label = QToolButton(self.groupBox_12)
        self.pickFontColor_label.setObjectName(u"pickFontColor_label")
        self.pickFontColor_label.setEnabled(True)

        self.gridLayout_3.addWidget(self.pickFontColor_label, 0, 2, 1, 1)

        self.label_22 = QLabel(self.groupBox_12)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_3.addWidget(self.label_22, 1, 0, 1, 1)

        self.fontweightComboBox_ax = QComboBox(self.groupBox_12)
        self.fontweightComboBox_ax.addItem("")
        self.fontweightComboBox_ax.addItem("")
        self.fontweightComboBox_ax.addItem("")
        self.fontweightComboBox_ax.addItem("")
        self.fontweightComboBox_ax.addItem("")
        self.fontweightComboBox_ax.addItem("")
        self.fontweightComboBox_ax.addItem("")
        self.fontweightComboBox_ax.addItem("")
        self.fontweightComboBox_ax.addItem("")
        self.fontweightComboBox_ax.addItem("")
        self.fontweightComboBox_ax.addItem("")
        self.fontweightComboBox_ax.addItem("")
        self.fontweightComboBox_ax.addItem("")
        self.fontweightComboBox_ax.addItem("")
        self.fontweightComboBox_ax.setObjectName(u"fontweightComboBox_ax")
        self.fontweightComboBox_ax.setFont(font2)

        self.gridLayout_3.addWidget(self.fontweightComboBox_ax, 1, 1, 1, 1)

        self.label_25 = QLabel(self.groupBox_12)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_3.addWidget(self.label_25, 4, 0, 1, 1)

        self.fontsizeSpinBox_ax = QSpinBox(self.groupBox_12)
        self.fontsizeSpinBox_ax.setObjectName(u"fontsizeSpinBox_ax")
        self.fontsizeSpinBox_ax.setEnabled(False)
        self.fontsizeSpinBox_ax.setFont(font2)
        self.fontsizeSpinBox_ax.setMinimum(1)

        self.gridLayout_3.addWidget(self.fontsizeSpinBox_ax, 3, 1, 1, 1)

        self.label_23 = QLabel(self.groupBox_12)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_3.addWidget(self.label_23, 2, 0, 1, 1)

        self.label_8 = QLabel(self.groupBox_12)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)

        self.fontstyleComboBox_ax = QComboBox(self.groupBox_12)
        self.fontstyleComboBox_ax.addItem("")
        self.fontstyleComboBox_ax.addItem("")
        self.fontstyleComboBox_ax.addItem("")
        self.fontstyleComboBox_ax.setObjectName(u"fontstyleComboBox_ax")
        self.fontstyleComboBox_ax.setFont(font2)

        self.gridLayout_3.addWidget(self.fontstyleComboBox_ax, 2, 1, 1, 1)

        self.label_size_auto_cb = QCheckBox(self.groupBox_12)
        self.label_size_auto_cb.setObjectName(u"label_size_auto_cb")
        self.label_size_auto_cb.setChecked(True)

        self.gridLayout_3.addWidget(self.label_size_auto_cb, 3, 0, 1, 1)

        self.fontfamilyComboBox_ax = QComboBox(self.groupBox_12)
        self.fontfamilyComboBox_ax.addItem("")
        self.fontfamilyComboBox_ax.addItem("")
        self.fontfamilyComboBox_ax.addItem("")
        self.fontfamilyComboBox_ax.addItem("")
        self.fontfamilyComboBox_ax.addItem("")
        self.fontfamilyComboBox_ax.setObjectName(u"fontfamilyComboBox_ax")
        self.fontfamilyComboBox_ax.setFont(font2)

        self.gridLayout_3.addWidget(self.fontfamilyComboBox_ax, 4, 1, 1, 1)


        self.verticalLayout_17.addLayout(self.gridLayout_3)


        self.verticalLayout_20.addWidget(self.groupBox_12)

        self.groupBox_11 = QGroupBox(self.tab)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.verticalLayout_18 = QVBoxLayout(self.groupBox_11)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pickFontColor_ax = QToolButton(self.groupBox_11)
        self.pickFontColor_ax.setObjectName(u"pickFontColor_ax")

        self.gridLayout_4.addWidget(self.pickFontColor_ax, 2, 2, 1, 1)

        self.label_20 = QLabel(self.groupBox_11)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_4.addWidget(self.label_20, 1, 0, 1, 1)

        self.grid_cb = QCheckBox(self.groupBox_11)
        self.grid_cb.setObjectName(u"grid_cb")

        self.gridLayout_4.addWidget(self.grid_cb, 3, 0, 1, 1)

        self.label_9 = QLabel(self.groupBox_11)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_4.addWidget(self.label_9, 2, 0, 1, 1)

        self.axis_thickness_cb = QDoubleSpinBox(self.groupBox_11)
        self.axis_thickness_cb.setObjectName(u"axis_thickness_cb")
        self.axis_thickness_cb.setFont(font2)
        self.axis_thickness_cb.setDecimals(1)
        self.axis_thickness_cb.setSingleStep(0.500000000000000)
        self.axis_thickness_cb.setValue(1.000000000000000)

        self.gridLayout_4.addWidget(self.axis_thickness_cb, 1, 1, 1, 1)

        self.labelFontColor_ax = QLabel(self.groupBox_11)
        self.labelFontColor_ax.setObjectName(u"labelFontColor_ax")

        self.gridLayout_4.addWidget(self.labelFontColor_ax, 2, 1, 1, 1)

        self.tick_label_size_cb = QSpinBox(self.groupBox_11)
        self.tick_label_size_cb.setObjectName(u"tick_label_size_cb")
        self.tick_label_size_cb.setEnabled(False)
        self.tick_label_size_cb.setFont(font2)

        self.gridLayout_4.addWidget(self.tick_label_size_cb, 0, 1, 1, 1)

        self.tick_label_size_auto_cb = QCheckBox(self.groupBox_11)
        self.tick_label_size_auto_cb.setObjectName(u"tick_label_size_auto_cb")
        self.tick_label_size_auto_cb.setChecked(True)

        self.gridLayout_4.addWidget(self.tick_label_size_auto_cb, 0, 0, 1, 1)


        self.verticalLayout_18.addLayout(self.gridLayout_4)


        self.verticalLayout_20.addWidget(self.groupBox_11)

        self.reset_all_pb = QPushButton(self.tab)
        self.reset_all_pb.setObjectName(u"reset_all_pb")

        self.verticalLayout_20.addWidget(self.reset_all_pb)

        self.tabWidget.addTab(self.tab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushOK = QPushButton(Dialog)
        self.pushOK.setObjectName(u"pushOK")

        self.horizontalLayout_5.addWidget(self.pushOK)

        self.pushCancel = QPushButton(Dialog)
        self.pushCancel.setObjectName(u"pushCancel")

        self.horizontalLayout_5.addWidget(self.pushCancel)

        self.pushApply = QPushButton(Dialog)
        self.pushApply.setObjectName(u"pushApply")

        self.horizontalLayout_5.addWidget(self.pushApply)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.retranslateUi(Dialog)
        self.pushOK.clicked.connect(Dialog.accept)
        self.pushCancel.clicked.connect(Dialog.reject)
        self.rbThFixedColor.clicked["bool"].connect(self.pickThColor.setEnabled)
        self.rbFixedSymbol.clicked["bool"].connect(self.cbSymbolType.setEnabled)
        self.rbGradientColor.clicked["bool"].connect(self.cbPalette.setDisabled)
        self.rbPalette.clicked["bool"].connect(self.pickColor1.setDisabled)
        self.rbPalette.clicked["bool"].connect(self.pickColor2.setDisabled)
        self.rbThFixedColor.clicked["bool"].connect(self.labelThcol.setEnabled)
        self.rbThSameColor.clicked["bool"].connect(self.labelThcol.setDisabled)
        self.rbPalette.clicked["bool"].connect(self.label_5.setDisabled)
        self.rbThFixedColor.clicked["bool"].connect(self.labelThPickedColor.setEnabled)
        self.rbThSameColor.clicked["bool"].connect(self.pickThColor.setDisabled)
        self.rbVariableSymbol.clicked["bool"].connect(self.cbSymbolType.setDisabled)
        self.rbThSameColor.clicked["bool"].connect(self.labelThPickedColor.setDisabled)
        self.rbFixedColor.clicked["bool"].connect(self.pickColor2.setDisabled)
        self.rbFixedColor.clicked["bool"].connect(self.cbPalette.setDisabled)
        self.rbFixedColor.clicked["bool"].connect(self.pickColor1.setEnabled)
        self.rbGradientColor.clicked["bool"].connect(self.pickColor1.setEnabled)
        self.rbFixedColor.clicked["bool"].connect(self.labelPickedColor2.setDisabled)
        self.rbGradientColor.clicked["bool"].connect(self.pickColor2.setEnabled)
        self.rbGradientColor.clicked["bool"].connect(self.labelPickedColor2.setEnabled)
        self.rbGradientColor.clicked["bool"].connect(self.labelPickedColor1.setEnabled)
        self.rbGradientColor.clicked["bool"].connect(self.label_4.setEnabled)
        self.rbPalette.clicked["bool"].connect(self.label_4.setDisabled)
        self.rbPalette.clicked["bool"].connect(self.labelPickedColor1.setDisabled)
        self.rbFixedColor.clicked["bool"].connect(self.label_4.setEnabled)
        self.rbPalette.clicked["bool"].connect(self.cbPalette.setEnabled)
        self.rbFixedColor.clicked["bool"].connect(self.label_5.setDisabled)
        self.rbPalette.clicked["bool"].connect(self.labelPickedColor2.setDisabled)
        self.rbGradientColor.clicked["bool"].connect(self.label_5.setEnabled)
        self.rbFixedColor.clicked["bool"].connect(self.labelPickedColor1.setEnabled)
        self.facecolorCheckBox.clicked["bool"].connect(self.labelFaceColor.setEnabled)
        self.facecolorCheckBox.clicked["bool"].connect(self.pickFaceColor.setEnabled)
        self.edgecolorCheckBox.clicked["bool"].connect(self.labelEdgeColor.setEnabled)
        self.edgecolorCheckBox.clicked["bool"].connect(self.pickEdgeColor.setEnabled)
        self.framealphaCheckBox.clicked["bool"].connect(self.framealphaSpinBox.setEnabled)
        self.borderpadCheckBox.clicked["bool"].connect(self.borderpadSpinBox.setEnabled)
        self.labelspacingCheckBox.clicked["bool"].connect(self.labelspacingSpinBox.setEnabled)
        self.handletextpadCheckBox.clicked["bool"].connect(self.handletextpadSpinBox.setEnabled)
        self.columnspacingCheckBox.clicked["bool"].connect(self.columnspacingSpinBox.setEnabled)
        self.legendtitleCheckBox.clicked["bool"].connect(self.legendtitleStr.setEnabled)
        self.legendlabelCheckBox.clicked["bool"].connect(self.legendlabelStr.setEnabled)
        self.label_size_auto_cb.toggled.connect(self.fontsizeSpinBox_ax.setDisabled)
        self.tick_label_size_auto_cb.toggled.connect(self.tick_label_size_cb.setDisabled)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Plot Style", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Symbol", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Type", None))
#if QT_CONFIG(tooltip)
        self.cbSymbolType.setToolTip(QCoreApplication.translate("Dialog", u"Empty symbol", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.rbFixedSymbol.setToolTip(QCoreApplication.translate("Dialog", u"Fixed symbol shape", None))
#endif // QT_CONFIG(tooltip)
        self.rbFixedSymbol.setText(QCoreApplication.translate("Dialog", u"Fixed", None))
#if QT_CONFIG(tooltip)
        self.rbVariableSymbol.setToolTip(QCoreApplication.translate("Dialog", u"Variable symbol shape", None))
#endif // QT_CONFIG(tooltip)
        self.rbVariableSymbol.setText(QCoreApplication.translate("Dialog", u"Variable", None))
        self.spinBoxLineW.setPrefix(QCoreApplication.translate("Dialog", u"Line width: ", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"Size", None))
        self.rbEmpty.setText(QCoreApplication.translate("Dialog", u"Empty", None))
#if QT_CONFIG(tooltip)
        self.rbFilled.setToolTip(QCoreApplication.translate("Dialog", u"Filled symbol", None))
#endif // QT_CONFIG(tooltip)
        self.rbFilled.setText(QCoreApplication.translate("Dialog", u"Filled", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Color", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Dialog", u"Type", None))
#if QT_CONFIG(tooltip)
        self.rbFixedColor.setToolTip(QCoreApplication.translate("Dialog", u"Fixed color", None))
#endif // QT_CONFIG(tooltip)
        self.rbFixedColor.setText(QCoreApplication.translate("Dialog", u"Fixed", None))
#if QT_CONFIG(tooltip)
        self.rbGradientColor.setToolTip(QCoreApplication.translate("Dialog", u"Gradient color between Color1 and Color2", None))
#endif // QT_CONFIG(tooltip)
        self.rbGradientColor.setText(QCoreApplication.translate("Dialog", u"Gradient", None))
        self.rbPalette.setText(QCoreApplication.translate("Dialog", u"Palette", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Dialog", u"Selection", None))
        self.pickColor1.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.labelPickedColor1.setText("")
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Color 1", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Color 2", None))
        self.labelPickedColor2.setText("")
        self.pickColor2.setText(QCoreApplication.translate("Dialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.cbPalette.setToolTip(QCoreApplication.translate("Dialog", u"Choose color palette", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.data), QCoreApplication.translate("Dialog", u"Data", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Dialog", u"Line Type", None))
        self.sbThLineWidth.setPrefix(QCoreApplication.translate("Dialog", u"Line width: ", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("Dialog", u"Color", None))
#if QT_CONFIG(tooltip)
        self.rbThSameColor.setToolTip(QCoreApplication.translate("Dialog", u"Same color as the data points", None))
#endif // QT_CONFIG(tooltip)
        self.rbThSameColor.setText(QCoreApplication.translate("Dialog", u"Same as Data", None))
#if QT_CONFIG(tooltip)
        self.rbThFixedColor.setToolTip(QCoreApplication.translate("Dialog", u"Theory in fixed color", None))
#endif // QT_CONFIG(tooltip)
        self.rbThFixedColor.setText(QCoreApplication.translate("Dialog", u"Fixed", None))
        self.labelThcol.setText(QCoreApplication.translate("Dialog", u"Color", None))
        self.labelThPickedColor.setText("")
        self.pickThColor.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.theory), QCoreApplication.translate("Dialog", u"Theory", None))
#if QT_CONFIG(tooltip)
        self.cb_show_legend.setToolTip(QCoreApplication.translate("Dialog", u"Show Legend on Figure", None))
#endif // QT_CONFIG(tooltip)
        self.cb_show_legend.setText(QCoreApplication.translate("Dialog", u"Show Legend", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Dialog", u"Legend Properties", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("Dialog", u"The location of the legend", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Dialog", u"Location", None))
        self.locationComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"best", None))
        self.locationComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"upper right", None))
        self.locationComboBox.setItemText(2, QCoreApplication.translate("Dialog", u"upper left", None))
        self.locationComboBox.setItemText(3, QCoreApplication.translate("Dialog", u"lower left", None))
        self.locationComboBox.setItemText(4, QCoreApplication.translate("Dialog", u"lower right", None))
        self.locationComboBox.setItemText(5, QCoreApplication.translate("Dialog", u"right", None))
        self.locationComboBox.setItemText(6, QCoreApplication.translate("Dialog", u"center left", None))
        self.locationComboBox.setItemText(7, QCoreApplication.translate("Dialog", u"center right", None))
        self.locationComboBox.setItemText(8, QCoreApplication.translate("Dialog", u"lower center", None))
        self.locationComboBox.setItemText(9, QCoreApplication.translate("Dialog", u"upper center", None))
        self.locationComboBox.setItemText(10, QCoreApplication.translate("Dialog", u"center", None))

#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("Dialog", u"Number of columns in the legend", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Number of columns", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("Dialog", u"Legend font size", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Font Size", None))
#if QT_CONFIG(tooltip)
        self.fancyboxCheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Draw legend frame with round edges", None))
#endif // QT_CONFIG(tooltip)
        self.fancyboxCheckBox.setText(QCoreApplication.translate("Dialog", u"Fancy Box", None))
#if QT_CONFIG(tooltip)
        self.markerfirstCheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Place legend marker to the left of the legend label", None))
#endif // QT_CONFIG(tooltip)
        self.markerfirstCheckBox.setText(QCoreApplication.translate("Dialog", u"Marker First", None))
#if QT_CONFIG(tooltip)
        self.modeCheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Expand the legend horizontally to fill the axes area", None))
#endif // QT_CONFIG(tooltip)
        self.modeCheckBox.setText(QCoreApplication.translate("Dialog", u"Expand Mode", None))
#if QT_CONFIG(tooltip)
        self.shadowCheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Draw a shadow behind the legend", None))
#endif // QT_CONFIG(tooltip)
        self.shadowCheckBox.setText(QCoreApplication.translate("Dialog", u"Shadow", None))
#if QT_CONFIG(tooltip)
        self.facecolorCheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Legend\u2019s background color", None))
#endif // QT_CONFIG(tooltip)
        self.facecolorCheckBox.setText(QCoreApplication.translate("Dialog", u"Face Color", None))
        self.labelFaceColor.setText("")
        self.pickFaceColor.setText(QCoreApplication.translate("Dialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.edgecolorCheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Legend\u2019s background patch edge color", None))
#endif // QT_CONFIG(tooltip)
        self.edgecolorCheckBox.setText(QCoreApplication.translate("Dialog", u"Edge Color", None))
        self.labelEdgeColor.setText("")
        self.pickEdgeColor.setText(QCoreApplication.translate("Dialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.framealphaCheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Alpha transparency of the legend\u2019s background", None))
#endif // QT_CONFIG(tooltip)
        self.framealphaCheckBox.setText(QCoreApplication.translate("Dialog", u"Transparency", None))
#if QT_CONFIG(tooltip)
        self.frameonCheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Draw the legend inside a patch (frame)", None))
#endif // QT_CONFIG(tooltip)
        self.frameonCheckBox.setText(QCoreApplication.translate("Dialog", u"Draw Frame", None))
#if QT_CONFIG(tooltip)
        self.legendtitleCheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Set Legend Title (default None)", None))
#endif // QT_CONFIG(tooltip)
        self.legendtitleCheckBox.setText(QCoreApplication.translate("Dialog", u"Legend Title", None))
#if QT_CONFIG(tooltip)
        self.legendtitleStr.setToolTip(QCoreApplication.translate("Dialog", u"Legend\u2019s title (none if left empty)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.borderpadCheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Fractional whitespace inside the legend border", None))
#endif // QT_CONFIG(tooltip)
        self.borderpadCheckBox.setText(QCoreApplication.translate("Dialog", u"Legend Border Pad", None))
        self.labelspacingCheckBox.setText(QCoreApplication.translate("Dialog", u"Space Between Entries", None))
        self.handletextpadCheckBox.setText(QCoreApplication.translate("Dialog", u"Space Handle-Label", None))
        self.columnspacingCheckBox.setText(QCoreApplication.translate("Dialog", u"Space Between Columns", None))
#if QT_CONFIG(tooltip)
        self.legendlabelCheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Set Legend label (default = all basic file parameters with values)", None))
#endif // QT_CONFIG(tooltip)
        self.legendlabelCheckBox.setText(QCoreApplication.translate("Dialog", u"Legend Labels", None))
#if QT_CONFIG(tooltip)
        self.legendlabelStr.setToolTip(QCoreApplication.translate("Dialog", u"default = all basic file parameters with values", None))
#endif // QT_CONFIG(tooltip)
        self.legendlabelStr.setText(QCoreApplication.translate("Dialog", u"default", None))
#if QT_CONFIG(tooltip)
        self.draggableCheckBox.setToolTip(QCoreApplication.translate("Dialog", u"Can the user move the legend with the mouse", None))
#endif // QT_CONFIG(tooltip)
        self.draggableCheckBox.setText(QCoreApplication.translate("Dialog", u"Draggable Legend", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.legend), QCoreApplication.translate("Dialog", u"Legend", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("Dialog", u"Default Annotation Properties", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Rotation", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Alignment", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Horizontal", None))
        self.hacomboBox.setItemText(0, QCoreApplication.translate("Dialog", u"center", None))
        self.hacomboBox.setItemText(1, QCoreApplication.translate("Dialog", u"right", None))
        self.hacomboBox.setItemText(2, QCoreApplication.translate("Dialog", u"left", None))

        self.label_13.setText(QCoreApplication.translate("Dialog", u"Vertical", None))
        self.vacomboBox.setItemText(0, QCoreApplication.translate("Dialog", u"center", None))
        self.vacomboBox.setItemText(1, QCoreApplication.translate("Dialog", u"top", None))
        self.vacomboBox.setItemText(2, QCoreApplication.translate("Dialog", u"bottom", None))
        self.vacomboBox.setItemText(3, QCoreApplication.translate("Dialog", u"baseline", None))

        self.label_7.setText(QCoreApplication.translate("Dialog", u"Font Color", None))
        self.labelFontColor.setText("")
        self.pickFontColor.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Font weight", None))
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

        self.label_15.setText(QCoreApplication.translate("Dialog", u"Font Style", None))
        self.fontstyleComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"normal", None))
        self.fontstyleComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"italic", None))
        self.fontstyleComboBox.setItemText(2, QCoreApplication.translate("Dialog", u"oblique", None))

#if QT_CONFIG(tooltip)
        self.label_16.setToolTip(QCoreApplication.translate("Dialog", u"Legend font size", None))
#endif // QT_CONFIG(tooltip)
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Font Size", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Opacity", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Font Family", None))
        self.fontfamilyComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"serif", None))
        self.fontfamilyComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"sans-serif", None))
        self.fontfamilyComboBox.setItemText(2, QCoreApplication.translate("Dialog", u"cursive", None))
        self.fontfamilyComboBox.setItemText(3, QCoreApplication.translate("Dialog", u"fantasy", None))
        self.fontfamilyComboBox.setItemText(4, QCoreApplication.translate("Dialog", u"monospace", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.annotations), QCoreApplication.translate("Dialog", u"Annotations", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("Dialog", u"Labels", None))
        self.labelFontColor_label.setText("")
        self.pickFontColor_label.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Font Weight", None))
        self.fontweightComboBox_ax.setItemText(0, QCoreApplication.translate("Dialog", u"ultralight", None))
        self.fontweightComboBox_ax.setItemText(1, QCoreApplication.translate("Dialog", u"light", None))
        self.fontweightComboBox_ax.setItemText(2, QCoreApplication.translate("Dialog", u"normal", None))
        self.fontweightComboBox_ax.setItemText(3, QCoreApplication.translate("Dialog", u"regular", None))
        self.fontweightComboBox_ax.setItemText(4, QCoreApplication.translate("Dialog", u"book", None))
        self.fontweightComboBox_ax.setItemText(5, QCoreApplication.translate("Dialog", u"medium", None))
        self.fontweightComboBox_ax.setItemText(6, QCoreApplication.translate("Dialog", u"roman", None))
        self.fontweightComboBox_ax.setItemText(7, QCoreApplication.translate("Dialog", u"semibold", None))
        self.fontweightComboBox_ax.setItemText(8, QCoreApplication.translate("Dialog", u"demibold", None))
        self.fontweightComboBox_ax.setItemText(9, QCoreApplication.translate("Dialog", u"demi", None))
        self.fontweightComboBox_ax.setItemText(10, QCoreApplication.translate("Dialog", u"bold", None))
        self.fontweightComboBox_ax.setItemText(11, QCoreApplication.translate("Dialog", u"heavy", None))
        self.fontweightComboBox_ax.setItemText(12, QCoreApplication.translate("Dialog", u"extra bold", None))
        self.fontweightComboBox_ax.setItemText(13, QCoreApplication.translate("Dialog", u"black", None))

        self.label_25.setText(QCoreApplication.translate("Dialog", u"Font Family", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Font Style", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Font Color", None))
        self.fontstyleComboBox_ax.setItemText(0, QCoreApplication.translate("Dialog", u"normal", None))
        self.fontstyleComboBox_ax.setItemText(1, QCoreApplication.translate("Dialog", u"italic", None))
        self.fontstyleComboBox_ax.setItemText(2, QCoreApplication.translate("Dialog", u"oblique", None))

        self.label_size_auto_cb.setText(QCoreApplication.translate("Dialog", u"Autoscale Label Size", None))
        self.fontfamilyComboBox_ax.setItemText(0, QCoreApplication.translate("Dialog", u"serif", None))
        self.fontfamilyComboBox_ax.setItemText(1, QCoreApplication.translate("Dialog", u"sans-serif", None))
        self.fontfamilyComboBox_ax.setItemText(2, QCoreApplication.translate("Dialog", u"cursive", None))
        self.fontfamilyComboBox_ax.setItemText(3, QCoreApplication.translate("Dialog", u"fantasy", None))
        self.fontfamilyComboBox_ax.setItemText(4, QCoreApplication.translate("Dialog", u"monospace", None))

        self.groupBox_11.setTitle(QCoreApplication.translate("Dialog", u"Axes", None))
        self.pickFontColor_ax.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Axes Thickness", None))
        self.grid_cb.setText(QCoreApplication.translate("Dialog", u"Grid", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Color", None))
        self.labelFontColor_ax.setText("")
        self.tick_label_size_auto_cb.setText(QCoreApplication.translate("Dialog", u"Autoscale Tick Label Size", None))
        self.reset_all_pb.setText(QCoreApplication.translate("Dialog", u"Default", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Axes", None))
        self.pushOK.setText(QCoreApplication.translate("Dialog", u"OK", None))
        self.pushCancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.pushApply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
    # retranslateUi

