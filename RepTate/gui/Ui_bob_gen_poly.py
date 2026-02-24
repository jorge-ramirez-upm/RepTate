# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bob_gen_poly.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QSplitter, QTabWidget, QTextBrowser,
    QToolButton, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(360, 658)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_8 = QLabel(Dialog)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout.addWidget(self.label_8)

        self.pb_pick_file = QToolButton(Dialog)
        self.pb_pick_file.setObjectName(u"pb_pick_file")

        self.horizontalLayout.addWidget(self.pb_pick_file)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_9.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_9 = QLabel(Dialog)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_2.addWidget(self.label_9)

        self.selected_file = QLabel(Dialog)
        self.selected_file.setObjectName(u"selected_file")

        self.horizontalLayout_2.addWidget(self.selected_file)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_9.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addLayout(self.verticalLayout_9)

        self.inp_param_widget = QWidget(Dialog)
        self.inp_param_widget.setObjectName(u"inp_param_widget")
        self.verticalLayout_13 = QVBoxLayout(self.inp_param_widget)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.tabWidget = QTabWidget(self.inp_param_widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.Chemistry = QWidget()
        self.Chemistry.setObjectName(u"Chemistry")
        self.verticalLayout_8 = QVBoxLayout(self.Chemistry)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.scrollArea = QScrollArea(self.Chemistry)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 277, 423))
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(False)
        self.label.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.m0 = QLineEdit(self.groupBox_2)
        self.m0.setObjectName(u"m0")
        self.m0.setFont(font)
        self.m0.setInputMethodHints(Qt.ImhDigitsOnly)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.m0)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.ne = QLineEdit(self.groupBox_2)
        self.ne.setObjectName(u"ne")
        self.ne.setFont(font)
        self.ne.setInputMethodHints(Qt.ImhDigitsOnly)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.ne)


        self.verticalLayout_7.addLayout(self.formLayout)


        self.verticalLayout_6.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.component = QFormLayout()
        self.component.setObjectName(u"component")
        self.component.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")

        self.component.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.ratio = QLineEdit(self.groupBox_3)
        self.ratio.setObjectName(u"ratio")
        self.ratio.setFont(font)
        self.ratio.setInputMethodHints(Qt.ImhDigitsOnly)

        self.component.setWidget(0, QFormLayout.FieldRole, self.ratio)

        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")

        self.component.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.cb_type = QComboBox(self.groupBox_3)
        self.cb_type.setObjectName(u"cb_type")
        self.cb_type.setFont(font)

        self.component.setWidget(1, QFormLayout.FieldRole, self.cb_type)

        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setWordWrap(True)

        self.component.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.number = QLineEdit(self.groupBox_3)
        self.number.setObjectName(u"number")
        self.number.setFont(font)
        self.number.setInputMethodHints(Qt.ImhDigitsOnly)

        self.component.setWidget(2, QFormLayout.FieldRole, self.number)

        self.ngeneration_label = QLabel(self.groupBox_3)
        self.ngeneration_label.setObjectName(u"ngeneration_label")
        self.ngeneration_label.setEnabled(False)

        self.component.setWidget(3, QFormLayout.LabelRole, self.ngeneration_label)

        self.sb_ngeneration = QSpinBox(self.groupBox_3)
        self.sb_ngeneration.setObjectName(u"sb_ngeneration")
        self.sb_ngeneration.setEnabled(False)
        self.sb_ngeneration.setMinimum(0)
        self.sb_ngeneration.setValue(2)

        self.component.setWidget(3, QFormLayout.FieldRole, self.sb_ngeneration)


        self.verticalLayout_2.addLayout(self.component)

        self.add_button = QPushButton(self.groupBox_3)
        self.add_button.setObjectName(u"add_button")

        self.verticalLayout_2.addWidget(self.add_button)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout_6.addWidget(self.groupBox_3)

        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.polymer_tab = QTabWidget(self.groupBox)
        self.polymer_tab.setObjectName(u"polymer_tab")
        self.polymer_tab.setFont(font)
        self.polymer_tab.setUsesScrollButtons(True)
        self.polymer_tab.setTabsClosable(True)

        self.verticalLayout_4.addWidget(self.polymer_tab)


        self.verticalLayout_6.addWidget(self.groupBox)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_8.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.Chemistry, "")
        self.Memory = QWidget()
        self.Memory.setObjectName(u"Memory")
        self.verticalLayout_5 = QVBoxLayout(self.Memory)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.label_6 = QLabel(self.Memory)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)
        self.label_6.setWordWrap(False)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_6)

        self.n_polymers = QLineEdit(self.Memory)
        self.n_polymers.setObjectName(u"n_polymers")
        self.n_polymers.setFont(font)
        self.n_polymers.setInputMethodHints(Qt.ImhDigitsOnly)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.n_polymers)

        self.label_7 = QLabel(self.Memory)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)
        self.label_7.setWordWrap(False)

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.n_segments = QLineEdit(self.Memory)
        self.n_segments.setObjectName(u"n_segments")
        self.n_segments.setFont(font)
        self.n_segments.setInputMethodHints(Qt.ImhDigitsOnly)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.n_segments)


        self.verticalLayout_5.addLayout(self.formLayout_2)

        self.tabWidget.addTab(self.Memory, "")
        self.Result = QWidget()
        self.Result.setObjectName(u"Result")
        self.verticalLayout_12 = QVBoxLayout(self.Result)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.splitter = QSplitter(self.Result)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.text_box = QTextBrowser(self.splitter)
        self.text_box.setObjectName(u"text_box")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.text_box.sizePolicy().hasHeightForWidth())
        self.text_box.setSizePolicy(sizePolicy)
        self.text_box.setAcceptRichText(False)
        self.splitter.addWidget(self.text_box)
        self.proto_widget = QWidget(self.splitter)
        self.proto_widget.setObjectName(u"proto_widget")
        self.proto_widget.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(2)
        sizePolicy1.setHeightForWidth(self.proto_widget.sizePolicy().hasHeightForWidth())
        self.proto_widget.setSizePolicy(sizePolicy1)
        self.verticalLayout_11 = QVBoxLayout(self.proto_widget)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.proto_label = QLabel(self.proto_widget)
        self.proto_label.setObjectName(u"proto_label")
        self.proto_label.setEnabled(False)

        self.verticalLayout_10.addWidget(self.proto_label)

        self.proto_text = QTextBrowser(self.proto_widget)
        self.proto_text.setObjectName(u"proto_text")
        self.proto_text.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(2)
        sizePolicy2.setHeightForWidth(self.proto_text.sizePolicy().hasHeightForWidth())
        self.proto_text.setSizePolicy(sizePolicy2)
        self.proto_text.setReadOnly(False)
        self.proto_text.setAcceptRichText(False)

        self.verticalLayout_10.addWidget(self.proto_text)


        self.verticalLayout_11.addLayout(self.verticalLayout_10)

        self.splitter.addWidget(self.proto_widget)

        self.verticalLayout_12.addWidget(self.splitter)

        self.tabWidget.addTab(self.Result, "")

        self.verticalLayout_13.addWidget(self.tabWidget)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pb_help = QPushButton(self.inp_param_widget)
        self.pb_help.setObjectName(u"pb_help")

        self.horizontalLayout_3.addWidget(self.pb_help)

        self.pb_apply = QPushButton(self.inp_param_widget)
        self.pb_apply.setObjectName(u"pb_apply")

        self.horizontalLayout_3.addWidget(self.pb_apply)

        self.pb_ok = QPushButton(self.inp_param_widget)
        self.pb_ok.setObjectName(u"pb_ok")

        self.horizontalLayout_3.addWidget(self.pb_ok)

        self.pb_cancel = QPushButton(self.inp_param_widget)
        self.pb_cancel.setObjectName(u"pb_cancel")

        self.horizontalLayout_3.addWidget(self.pb_cancel)


        self.verticalLayout_13.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addWidget(self.inp_param_widget)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)
        self.polymer_tab.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Create Polymer Configuration", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Pick Output Polyconf File", None))
#if QT_CONFIG(tooltip)
        self.pb_pick_file.setToolTip(QCoreApplication.translate("Dialog", u"Select File...", None))
#endif // QT_CONFIG(tooltip)
        self.pb_pick_file.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Selected file:", None))
        self.selected_file.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Polymer", None))
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
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Add Component", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("Dialog", u"Ratio weight fraction occupied by component", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Ratio", None))
#if QT_CONFIG(tooltip)
        self.ratio.setToolTip(QCoreApplication.translate("Dialog", u"Ratio weight fraction occupied by component", None))
#endif // QT_CONFIG(tooltip)
        self.ratio.setText(QCoreApplication.translate("Dialog", u"1", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("Dialog", u"Polymer architecture type", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Architecture", None))
#if QT_CONFIG(tooltip)
        self.cb_type.setToolTip(QCoreApplication.translate("Dialog", u"Polymer architecture type", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip(QCoreApplication.translate("Dialog", u"Number of polymers in current type", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Num. of polymers", None))
#if QT_CONFIG(tooltip)
        self.number.setToolTip(QCoreApplication.translate("Dialog", u"Number of polymers in current type", None))
#endif // QT_CONFIG(tooltip)
        self.number.setText(QCoreApplication.translate("Dialog", u"1000", None))
#if QT_CONFIG(tooltip)
        self.ngeneration_label.setToolTip(QCoreApplication.translate("Dialog", u"Number of generations (Cayley type only)", None))
#endif // QT_CONFIG(tooltip)
        self.ngeneration_label.setText(QCoreApplication.translate("Dialog", u"Num. generations", None))
#if QT_CONFIG(tooltip)
        self.sb_ngeneration.setToolTip(QCoreApplication.translate("Dialog", u"Number of generations (Cayley type only)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.add_button.setToolTip(QCoreApplication.translate("Dialog", u"Add component to mix", None))
#endif // QT_CONFIG(tooltip)
        self.add_button.setText(QCoreApplication.translate("Dialog", u"Add", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Components", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Chemistry), QCoreApplication.translate("Dialog", u"Chemistry", None))
#if QT_CONFIG(tooltip)
        self.label_6.setToolTip(QCoreApplication.translate("Dialog", u"Maximum number of polymer", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Max. num. of polymers", None))
#if QT_CONFIG(tooltip)
        self.n_polymers.setToolTip(QCoreApplication.translate("Dialog", u"Maximum number of polymer", None))
#endif // QT_CONFIG(tooltip)
        self.n_polymers.setText(QCoreApplication.translate("Dialog", u"1e4", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Max. num. of segments", None))
#if QT_CONFIG(tooltip)
        self.n_segments.setToolTip(QCoreApplication.translate("Dialog", u"Maximum total number of arms", None))
#endif // QT_CONFIG(tooltip)
        self.n_segments.setText(QCoreApplication.translate("Dialog", u"1e5", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Memory), QCoreApplication.translate("Dialog", u"Memory", None))
        self.proto_label.setText(QCoreApplication.translate("Dialog", u"Enter Polymer Prototype:", None))
        self.proto_text.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'.SF NS Text'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Result), QCoreApplication.translate("Dialog", u"Result", None))
        self.pb_help.setText(QCoreApplication.translate("Dialog", u"Help", None))
        self.pb_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pb_ok.setText(QCoreApplication.translate("Dialog", u"OK", None))
        self.pb_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

