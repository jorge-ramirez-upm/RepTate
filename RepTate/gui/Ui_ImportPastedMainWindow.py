# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_from_pasted_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QGroupBox, QLabel, QLineEdit,
    QSizePolicy, QTextBrowser, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(501, 362)
        Dialog.setAcceptDrops(True)
        self.verticalLayout_5 = QVBoxLayout(Dialog)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.file_name_label = QLineEdit(self.groupBox_2)
        self.file_name_label.setObjectName(u"file_name_label")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.file_name_label)


        self.verticalLayout_3.addLayout(self.formLayout)


        self.verticalLayout_5.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_columns = QLabel(self.groupBox)
        self.label_columns.setObjectName(u"label_columns")
        font = QFont()
        font.setBold(False)
        self.label_columns.setFont(font)
        self.label_columns.setTextFormat(Qt.RichText)
        self.label_columns.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_columns)

        self.paste_box = QTextBrowser(self.groupBox)
        self.paste_box.setObjectName(u"paste_box")
        self.paste_box.setUndoRedoEnabled(True)
        self.paste_box.setReadOnly(False)
        self.paste_box.setAcceptRichText(False)
        self.paste_box.setOpenLinks(False)

        self.verticalLayout_2.addWidget(self.paste_box)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_5.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_5.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Import Pasted Data", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Filename", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Set filename to:", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Data", None))
        self.label_columns.setText(QCoreApplication.translate("Dialog", u"w, G', G''", None))
        self.paste_box.setPlaceholderText(QCoreApplication.translate("Dialog", u"Paste TAB or SPACE separated data", None))
    # retranslateUi

