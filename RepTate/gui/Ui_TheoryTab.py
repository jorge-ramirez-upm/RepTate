# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'theorytab.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QSizePolicy,
    QSplitter, QTextBrowser, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_TheoryTab(object):
    def setupUi(self, TheoryTab):
        if not TheoryTab.objectName():
            TheoryTab.setObjectName(u"TheoryTab")
        TheoryTab.resize(224, 409)
        self.verticalLayout_2 = QVBoxLayout(TheoryTab)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.thToolsLayout = QHBoxLayout()
        self.thToolsLayout.setObjectName(u"thToolsLayout")

        self.verticalLayout_2.addLayout(self.thToolsLayout)

        self.splitter = QSplitter(TheoryTab)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setLineWidth(1)
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.setHandleWidth(3)
        self.thParamTable = QTreeWidget(self.splitter)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.thParamTable.setHeaderItem(__qtreewidgetitem)
        self.thParamTable.setObjectName(u"thParamTable")
        self.splitter.addWidget(self.thParamTable)
        self.thTextBox = QTextBrowser(self.splitter)
        self.thTextBox.setObjectName(u"thTextBox")
        font = QFont()
        font.setFamilies([u"Courier"])
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        self.thTextBox.setFont(font)
        self.thTextBox.viewport().setProperty("cursor", QCursor(Qt.IBeamCursor))
        self.thTextBox.setStyleSheet(u"background-color: rgb(217, 255, 255);\n"
"font: 8pt \"Courier\";\n"
";")
        self.splitter.addWidget(self.thTextBox)

        self.verticalLayout_2.addWidget(self.splitter)


        self.retranslateUi(TheoryTab)

        QMetaObject.connectSlotsByName(TheoryTab)
    # setupUi

    def retranslateUi(self, TheoryTab):
        TheoryTab.setWindowTitle(QCoreApplication.translate("TheoryTab", u"Form", None))
        self.thTextBox.setHtml(QCoreApplication.translate("TheoryTab", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Courier'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
    # retranslateUi

