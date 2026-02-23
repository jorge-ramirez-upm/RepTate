# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dummyfilesDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QComboBox,
    QDialog, QDialogButtonBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QSizePolicy, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(450, 384)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")
        font = QFont()
        font.setBold(True)
        self.label_6.setFont(font)

        self.verticalLayout.addWidget(self.label_6)

        self.parameterTreeWidget = QTreeWidget(Dialog)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(4, Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter);
        __qtreewidgetitem.setFont(4, font);
        __qtreewidgetitem.setTextAlignment(3, Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter);
        __qtreewidgetitem.setFont(3, font);
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter);
        __qtreewidgetitem.setFont(2, font);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter);
        __qtreewidgetitem.setFont(1, font);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter);
        __qtreewidgetitem.setFont(0, font);
        self.parameterTreeWidget.setHeaderItem(__qtreewidgetitem)
        self.parameterTreeWidget.setObjectName(u"parameterTreeWidget")
        font1 = QFont()
        font1.setBold(False)
        self.parameterTreeWidget.setFont(font1)
        self.parameterTreeWidget.setLayoutDirection(Qt.LeftToRight)
        self.parameterTreeWidget.setFrameShape(QFrame.StyledPanel)
        self.parameterTreeWidget.setFrameShadow(QFrame.Plain)
        self.parameterTreeWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.parameterTreeWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.parameterTreeWidget.setTabKeyNavigation(False)
        self.parameterTreeWidget.setProperty("showDropIndicator", False)
        self.parameterTreeWidget.setAlternatingRowColors(True)
        self.parameterTreeWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.parameterTreeWidget.setRootIsDecorated(False)
        self.parameterTreeWidget.setUniformRowHeights(True)
        self.parameterTreeWidget.setItemsExpandable(False)
        self.parameterTreeWidget.setAnimated(False)
        self.parameterTreeWidget.setHeaderHidden(False)
        self.parameterTreeWidget.setExpandsOnDoubleClick(False)
        self.parameterTreeWidget.header().setVisible(True)
        self.parameterTreeWidget.header().setDefaultSectionSize(70)
        self.parameterTreeWidget.header().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.parameterTreeWidget)

        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font)
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.xminLineEdit = QLineEdit(self.groupBox)
        self.xminLineEdit.setObjectName(u"xminLineEdit")
        self.xminLineEdit.setFont(font1)

        self.gridLayout.addWidget(self.xminLineEdit, 0, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.xmaxLineEdit = QLineEdit(self.groupBox)
        self.xmaxLineEdit.setObjectName(u"xmaxLineEdit")
        self.xmaxLineEdit.setFont(font1)

        self.gridLayout.addWidget(self.xmaxLineEdit, 0, 3, 1, 1)

        self.npointsLineEdit = QLineEdit(self.groupBox)
        self.npointsLineEdit.setObjectName(u"npointsLineEdit")
        self.npointsLineEdit.setFont(font1)

        self.gridLayout.addWidget(self.npointsLineEdit, 1, 1, 1, 1)

        self.scaleComboBox = QComboBox(self.groupBox)
        self.scaleComboBox.addItem("")
        self.scaleComboBox.addItem("")
        self.scaleComboBox.setObjectName(u"scaleComboBox")
        self.scaleComboBox.setFont(font1)

        self.gridLayout.addWidget(self.scaleComboBox, 1, 3, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.horizontalLayout.addWidget(self.label_5)

        self.yvaluesLineEdit = QLineEdit(self.frame)
        self.yvaluesLineEdit.setObjectName(u"yvaluesLineEdit")

        self.horizontalLayout.addWidget(self.yvaluesLineEdit)


        self.verticalLayout.addWidget(self.frame)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_7 = QLabel(self.frame_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_7)

        self.chemLineEdit = QLineEdit(self.frame_2)
        self.chemLineEdit.setObjectName(u"chemLineEdit")

        self.horizontalLayout_2.addWidget(self.chemLineEdit)


        self.verticalLayout.addWidget(self.frame_2)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Help|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"New Dummy File(s)", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Select the file parameters that you want to modify and set the range: ", None))
        ___qtreewidgetitem = self.parameterTreeWidget.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("Dialog", u"Scale", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Dialog", u"# Points", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Max", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Value/Min", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Name", None));
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"X range in dummy files", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"# Points", None))
        self.xminLineEdit.setText(QCoreApplication.translate("Dialog", u"0.001", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Max", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Min", None))
        self.xmaxLineEdit.setText(QCoreApplication.translate("Dialog", u"1000", None))
        self.npointsLineEdit.setText(QCoreApplication.translate("Dialog", u"100", None))
        self.scaleComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"Log", None))
        self.scaleComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Linear", None))

        self.label_4.setText(QCoreApplication.translate("Dialog", u"Scale", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Default y values", None))
        self.yvaluesLineEdit.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Chemistry", None))
        self.chemLineEdit.setText(QCoreApplication.translate("Dialog", u"None", None))
    # retranslateUi

