# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Tooltab.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QSizePolicy,
    QSplitter, QTextBrowser, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)
import Tool_rc

class Ui_ToolTab(object):
    def setupUi(self, ToolTab):
        if not ToolTab.objectName():
            ToolTab.setObjectName(u"ToolTab")
        ToolTab.resize(224, 409)
        self.actionActive = QAction(ToolTab)
        self.actionActive.setObjectName(u"actionActive")
        self.actionActive.setCheckable(True)
        icon = QIcon()
        icon.addFile(u":/Icon8/Images/new_icons/icons8-toggle-on.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionActive.setIcon(icon)
        self.actionApplyToTheory = QAction(ToolTab)
        self.actionApplyToTheory.setObjectName(u"actionApplyToTheory")
        self.actionApplyToTheory.setCheckable(True)
        icon1 = QIcon()
        icon1.addFile(u":/Icon8/Images/new_icons/icons8-einstein-yes.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionApplyToTheory.setIcon(icon1)
        self.verticalLayout = QVBoxLayout(ToolTab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.toolToolsLayout = QHBoxLayout()
        self.toolToolsLayout.setObjectName(u"toolToolsLayout")

        self.verticalLayout.addLayout(self.toolToolsLayout)

        self.splitter = QSplitter(ToolTab)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setLineWidth(1)
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.setHandleWidth(3)
        self.toolParamTable = QTreeWidget(self.splitter)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.toolParamTable.setHeaderItem(__qtreewidgetitem)
        self.toolParamTable.setObjectName(u"toolParamTable")
        self.splitter.addWidget(self.toolParamTable)
        self.toolTextBox = QTextBrowser(self.splitter)
        self.toolTextBox.setObjectName(u"toolTextBox")
        font = QFont()
        font.setFamilies([u"Courier"])
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        self.toolTextBox.setFont(font)
        self.toolTextBox.viewport().setProperty("cursor", QCursor(Qt.IBeamCursor))
        self.toolTextBox.setStyleSheet(u"background-color: rgb(217, 255, 217);\n"
"font: 8pt \"Courier\";\n"
";")
        self.splitter.addWidget(self.toolTextBox)

        self.verticalLayout.addWidget(self.splitter)


        self.retranslateUi(ToolTab)

        QMetaObject.connectSlotsByName(ToolTab)
    # setupUi

    def retranslateUi(self, ToolTab):
        ToolTab.setWindowTitle(QCoreApplication.translate("ToolTab", u"Form", None))
        self.actionActive.setText(QCoreApplication.translate("ToolTab", u"Active", None))
#if QT_CONFIG(tooltip)
        self.actionActive.setToolTip(QCoreApplication.translate("ToolTab", u"Active Tool?", None))
#endif // QT_CONFIG(tooltip)
        self.actionApplyToTheory.setText(QCoreApplication.translate("ToolTab", u"Apply to Theory", None))
#if QT_CONFIG(tooltip)
        self.actionApplyToTheory.setToolTip(QCoreApplication.translate("ToolTab", u"Apply Tool to Theory", None))
#endif // QT_CONFIG(tooltip)
        self.toolTextBox.setHtml(QCoreApplication.translate("ToolTab", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Courier'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
    # retranslateUi

