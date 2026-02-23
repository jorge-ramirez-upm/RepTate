# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_excel_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QToolButton, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(604, 603)
        Dialog.setAcceptDrops(True)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_4 = QGroupBox(Dialog)
        self.groupBox_4.setObjectName(u"groupBox_4")
        font = QFont()
        font.setBold(False)
        self.groupBox_4.setFont(font)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.selected_file_label = QLabel(self.groupBox_4)
        self.selected_file_label.setObjectName(u"selected_file_label")

        self.gridLayout_2.addWidget(self.selected_file_label, 1, 1, 1, 1)

        self.select_file_tb = QToolButton(self.groupBox_4)
        self.select_file_tb.setObjectName(u"select_file_tb")

        self.gridLayout_2.addWidget(self.select_file_tb, 1, 0, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_2)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.file_param_grid = QGridLayout()
        self.file_param_grid.setObjectName(u"file_param_grid")
        self.file_param_txt = QLineEdit(self.groupBox_2)
        self.file_param_txt.setObjectName(u"file_param_txt")

        self.file_param_grid.addWidget(self.file_param_txt, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.file_param_grid.addItem(self.horizontalSpacer_2, 0, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.file_param_grid)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.select_cols_layout = QGridLayout()
        self.select_cols_layout.setObjectName(u"select_cols_layout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.select_cols_layout.addWidget(self.label, 1, 0, 1, 1)

        self.col2 = QLabel(self.groupBox)
        self.col2.setObjectName(u"col2")

        self.select_cols_layout.addWidget(self.col2, 3, 0, 1, 1)

        self.col1 = QLabel(self.groupBox)
        self.col1.setObjectName(u"col1")

        self.select_cols_layout.addWidget(self.col1, 2, 0, 1, 1)

        self.skip_sb = QSpinBox(self.groupBox)
        self.skip_sb.setObjectName(u"skip_sb")

        self.select_cols_layout.addWidget(self.skip_sb, 1, 1, 1, 1)

        self.col1_cb = QComboBox(self.groupBox)
        self.col1_cb.setObjectName(u"col1_cb")

        self.select_cols_layout.addWidget(self.col1_cb, 2, 1, 1, 1)

        self.col3 = QLabel(self.groupBox)
        self.col3.setObjectName(u"col3")

        self.select_cols_layout.addWidget(self.col3, 4, 0, 1, 1)

        self.col2_cb = QComboBox(self.groupBox)
        self.col2_cb.setObjectName(u"col2_cb")

        self.select_cols_layout.addWidget(self.col2_cb, 3, 1, 1, 1)

        self.col3_cb = QComboBox(self.groupBox)
        self.col3_cb.setObjectName(u"col3_cb")

        self.select_cols_layout.addWidget(self.col3_cb, 4, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.select_cols_layout.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        self.cbInterpolate = QCheckBox(self.groupBox)
        self.cbInterpolate.setObjectName(u"cbInterpolate")

        self.select_cols_layout.addWidget(self.cbInterpolate, 2, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.select_cols_layout)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(Dialog)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.qtabs = QTabWidget(self.groupBox_3)
        self.qtabs.setObjectName(u"qtabs")

        self.verticalLayout_5.addWidget(self.qtabs)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.qtabs.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Import Data From Excel", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"Select Excel File", None))
        self.selected_file_label.setText("")
        self.select_file_tb.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Enter File Parameters", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Select Data", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Header rows to skip", None))
        self.col2.setText(QCoreApplication.translate("Dialog", u"Val2", None))
        self.col1.setText(QCoreApplication.translate("Dialog", u"Val1", None))
        self.col3.setText(QCoreApplication.translate("Dialog", u"Val3", None))
#if QT_CONFIG(tooltip)
        self.cbInterpolate.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>If ncol&gt;2 and columns 2 and 3 don't share the same x values, the data is interpolated</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cbInterpolate.setText(QCoreApplication.translate("Dialog", u"Interpolate Data", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Data Preview", None))
    # retranslateUi

