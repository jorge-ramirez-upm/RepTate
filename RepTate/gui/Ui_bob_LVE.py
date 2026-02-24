# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bob_LVE.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QToolButton, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(272, 474)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_11 = QLabel(Dialog)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 0, 2, 1, 1)

        self.label_9 = QLabel(Dialog)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 4, 1, 1)

        self.pb_pick_file = QToolButton(Dialog)
        self.pb_pick_file.setObjectName(u"pb_pick_file")

        self.gridLayout.addWidget(self.pb_pick_file, 0, 1, 1, 1)

        self.selected_file = QLabel(Dialog)
        self.selected_file.setObjectName(u"selected_file")

        self.gridLayout.addWidget(self.selected_file, 0, 3, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.inp_param_widget = QWidget(Dialog)
        self.inp_param_widget.setObjectName(u"inp_param_widget")
        self.verticalLayout = QVBoxLayout(self.inp_param_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(self.inp_param_widget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 222, 349))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.n_polymers = QLineEdit(self.groupBox_3)
        self.n_polymers.setObjectName(u"n_polymers")

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.n_polymers)

        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_6)

        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.n_segments = QLineEdit(self.groupBox_3)
        self.n_segments.setObjectName(u"n_segments")

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.n_segments)


        self.verticalLayout_4.addLayout(self.formLayout_4)


        self.verticalLayout_3.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.alpha = QLineEdit(self.groupBox_2)
        self.alpha.setObjectName(u"alpha")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.alpha)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(False)
        self.label.setFont(font)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label)

        self.m0 = QLineEdit(self.groupBox_2)
        self.m0.setObjectName(u"m0")
        self.m0.setFont(font)
        self.m0.setInputMethodHints(Qt.ImhDigitsOnly)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.m0)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.ne = QLineEdit(self.groupBox_2)
        self.ne.setObjectName(u"ne")
        self.ne.setFont(font)
        self.ne.setInputMethodHints(Qt.ImhDigitsOnly)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.ne)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_3)

        self.density = QLineEdit(self.groupBox_2)
        self.density.setObjectName(u"density")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.density)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_5)

        self.taue = QLineEdit(self.groupBox_2)
        self.taue.setObjectName(u"taue")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.taue)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_8)

        self.temperature = QLineEdit(self.groupBox_2)
        self.temperature.setObjectName(u"temperature")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.temperature)


        self.verticalLayout_7.addLayout(self.formLayout)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.verticalLayout_2.addWidget(self.inp_param_widget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pb_help = QPushButton(Dialog)
        self.pb_help.setObjectName(u"pb_help")

        self.horizontalLayout.addWidget(self.pb_help)

        self.pb_cancel = QPushButton(Dialog)
        self.pb_cancel.setObjectName(u"pb_cancel")

        self.horizontalLayout.addWidget(self.pb_cancel)

        self.pb_ok = QPushButton(Dialog)
        self.pb_ok.setObjectName(u"pb_ok")

        self.horizontalLayout.addWidget(self.pb_ok)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Simulation Parameters", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Selected:", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Input polyconf", None))
        self.pb_pick_file.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.selected_file.setText("")
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Memory", None))
#if QT_CONFIG(tooltip)
        self.n_polymers.setToolTip(QCoreApplication.translate("Dialog", u"Maximum number of polymer", None))
#endif // QT_CONFIG(tooltip)
        self.n_polymers.setText(QCoreApplication.translate("Dialog", u"1e4", None))
#if QT_CONFIG(tooltip)
        self.label_6.setToolTip(QCoreApplication.translate("Dialog", u"Maximum number of polymer", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Num. polymers", None))
#if QT_CONFIG(tooltip)
        self.label_7.setToolTip(QCoreApplication.translate("Dialog", u"Maximum total number of arms", None))
#endif // QT_CONFIG(tooltip)
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Num. segments", None))
#if QT_CONFIG(tooltip)
        self.n_segments.setToolTip(QCoreApplication.translate("Dialog", u"Maximum total number of arms", None))
#endif // QT_CONFIG(tooltip)
        self.n_segments.setText(QCoreApplication.translate("Dialog", u"1e5", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Parameters", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("Dialog", u"Tube dilation exponent", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Dialog", u"alpha", None))
#if QT_CONFIG(tooltip)
        self.alpha.setToolTip(QCoreApplication.translate("Dialog", u"Tube dilation exponent", None))
#endif // QT_CONFIG(tooltip)
        self.alpha.setText(QCoreApplication.translate("Dialog", u"1", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("Dialog", u"Mass of a monomer", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Dialog", u"M0 (g/mol)", None))
#if QT_CONFIG(tooltip)
        self.m0.setToolTip(QCoreApplication.translate("Dialog", u"Mass of a monomer", None))
#endif // QT_CONFIG(tooltip)
        self.m0.setText(QCoreApplication.translate("Dialog", u"28", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("Dialog", u"Number of monomers in an entanglement length", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Ne", None))
#if QT_CONFIG(tooltip)
        self.ne.setToolTip(QCoreApplication.translate("Dialog", u"Number of monomers in an entanglement length", None))
#endif // QT_CONFIG(tooltip)
        self.ne.setText(QCoreApplication.translate("Dialog", u"40", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("Dialog", u"Mass-density of the polymer (g/cc accepted)", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>density (kg/m<span style=\" vertical-align:super;\">3</span>)</p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.density.setToolTip(QCoreApplication.translate("Dialog", u"Mass-density of the polymer (g/cc accepted)", None))
#endif // QT_CONFIG(tooltip)
        self.density.setText(QCoreApplication.translate("Dialog", u"1e3", None))
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip(QCoreApplication.translate("Dialog", u"Entanglement time", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("Dialog", u"tau_e (s)", None))
#if QT_CONFIG(tooltip)
        self.taue.setToolTip(QCoreApplication.translate("Dialog", u"Entanglement time", None))
#endif // QT_CONFIG(tooltip)
        self.taue.setText(QCoreApplication.translate("Dialog", u"1e-2", None))
#if QT_CONFIG(tooltip)
        self.label_8.setToolTip(QCoreApplication.translate("Dialog", u"Temperature", None))
#endif // QT_CONFIG(tooltip)
        self.label_8.setText(QCoreApplication.translate("Dialog", u"T (K)", None))
#if QT_CONFIG(tooltip)
        self.temperature.setToolTip(QCoreApplication.translate("Dialog", u"Temperature", None))
#endif // QT_CONFIG(tooltip)
        self.temperature.setText(QCoreApplication.translate("Dialog", u"300", None))
#if QT_CONFIG(tooltip)
        self.pb_help.setToolTip(QCoreApplication.translate("Dialog", u"Show BoB documentation", None))
#endif // QT_CONFIG(tooltip)
        self.pb_help.setText(QCoreApplication.translate("Dialog", u"Help", None))
        self.pb_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.pb_ok.setText(QCoreApplication.translate("Dialog", u"OK", None))
    # retranslateUi

