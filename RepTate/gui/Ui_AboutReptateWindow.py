# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AboutDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QSizePolicy, QTextBrowser,
    QVBoxLayout, QWidget)
from . import About_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(771, 449)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QSize(771, 449))
        icon = QIcon()
        icon.addFile(u":/Images/Images/RepTate_logo_100.png", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setModal(True)
        self.horizontalLayout = QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(353, 447))
        self.label.setMaximumSize(QSize(353, 447))
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet(u"background-image: url(:/Images/Images/logo_with_uni_logo.png);")
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label.setMargin(0)
        self.label.setIndent(0)
        self.label.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.frame)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(402, 449))
        self.frame_2.setMaximumSize(QSize(402, 449))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAutoFillBackground(False)
        self.label_2.setFrameShape(QFrame.NoFrame)
        self.label_2.setPixmap(QPixmap(u":/Images/Images/alexei.png"))
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setMargin(-3)

        self.verticalLayout.addWidget(self.label_2)

        self.textBrowser = QTextBrowser(self.frame_2)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setAutoFillBackground(True)
        self.textBrowser.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.textBrowser)


        self.horizontalLayout.addWidget(self.frame_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText("")
        self.label_2.setText("")
        self.textBrowser.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:2px; margin-right:2px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'.SF NS Text'; font-size:8pt; font-weight:600;\">RepTate</span><span style=\" font-family:'.SF NS Text'; font-size:8pt;\"> (</span><span style=\" font-family:'.SF NS Text'; font-size:8pt; font-weight:600;\">R</span><span style=\" font-family:'.SF NS Text'; font-size:8pt;\">heology of </span><span style=\" font-family:'.SF NS Text'; font-size:8pt; font-weight:600;\">E</span><span style=\" font-family:'.SF NS Text'; font-size:8pt;\">ntangled </span><span style=\" font-family:'.SF NS Text'; font-"
                        "size:8pt; font-weight:600;\">P</span><span style=\" font-family:'.SF NS Text'; font-size:8pt;\">olymers: </span><span style=\" font-family:'.SF NS Text'; font-size:8pt; font-weight:600;\">T</span><span style=\" font-family:'.SF NS Text'; font-size:8pt;\">oolkit for the </span><span style=\" font-family:'.SF NS Text'; font-size:8pt; font-weight:600;\">A</span><span style=\" font-family:'.SF NS Text'; font-size:8pt;\">nalysis of </span><span style=\" font-family:'.SF NS Text'; font-size:8pt; font-weight:600;\">T</span><span style=\" font-family:'.SF NS Text'; font-size:8pt;\">heory and </span><span style=\" font-family:'.SF NS Text'; font-size:8pt; font-weight:600;\">E</span><span style=\" font-family:'.SF NS Text'; font-size:8pt;\">xperiment), was originally created in Delphi by Jorge Ram\u00edrez and Alexei Likhtman at the </span><a href=\"http://www.leeds.ac.uk/\"><span style=\" font-family:'.SF NS Text'; font-size:8pt; text-decoration: underline; color:#0068da;\">University of Leeds</span></a><span style=\" "
                        "font-family:'.SF NS Text'; font-size:8pt;\"> and the </span><a href=\"http://www.reading.ac.uk/\"><span style=\" font-family:'.SF NS Text'; font-size:8pt; text-decoration: underline; color:#0068da;\">University of Reading</span></a><span style=\" font-family:'.SF NS Text'; font-size:8pt;\">, as part of the muPP2 project, funded by the EPSRC. This new version is a port (and enhancement) of the original RepTate code to Python 3, using PySide6 and Matplotlib for the visuals, and NumPy and SciPy for numerical calculations. It is developed by </span><a href=\"mailto: jorge.ramirez@upm.es\"><span style=\" font-family:'.SF NS Text'; font-size:8pt; text-decoration: underline; color:#0068da;\">Jorge Ram\u00edrez</span></a><span style=\" font-family:'.SF NS Text'; font-size:8pt;\"> (</span><a href=\"http://www.upm.es\"><span style=\" font-family:'.SF NS Text'; font-size:8pt; text-decoration: underline; color:#0068da;\">Universidad Polit\u00e9cnica de Madrid</span></a><span style=\" font-family:'.SF NS Text'; font-size:8"
                        "pt;\">) and Victor Boudara (</span><a href=\"http://www.leeds.ac.uk\"><span style=\" font-family:'.SF NS Text'; font-size:8pt; text-decoration: underline; color:#0068da;\">University of Leeds</span></a><span style=\" font-family:'.SF NS Text'; font-size:8pt;\">). The program and source code are released under the </span><a href=\"https://www.gnu.org/licenses/gpl-3.0.en.html\"><span style=\" font-family:'.SF NS Text'; font-size:8pt; text-decoration: underline; color:#0068da;\">GPLv3+ license</span></a><span style=\" font-family:'.SF NS Text'; font-size:8pt;\">.</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'.SF NS Text'; font-size:8pt;\">This project is dedicated to the memory of our great friend and collaborator Alexei.<br />Project page: </span><a href=\"https://github.com/jorge-ramirez-upm/RepTate\"><span style=\" font-family:'.SF NS Text'; font-size:8pt; text-decoration: un"
                        "derline; color:#0068da;\">https://github.com/jorge-ramirez-upm/RepTate</span></a><span style=\" font-family:'.SF NS Text'; font-size:8pt;\"><br />Documentation: </span><a href=\"https://reptate.readthedocs.io/\"><span style=\" font-family:'.SF NS Text'; font-size:8pt; text-decoration: underline; color:#0068da;\">http://reptate.readthedocs.io/</span></a><span style=\" font-family:'.SF NS Text'; font-size:8pt;\"><br />OLD web site: </span><a href=\"http://www.reptate.com\"><span style=\" font-family:'.SF NS Text'; font-size:8pt; text-decoration: underline; color:#0068da;\">https://www.reptate.com</span></a><span style=\" font-family:'.SF NS Text'; font-size:8pt;\"><br />Icons: </span><a href=\"https://icons8.com/\"><span style=\" font-family:'.SF NS Text'; font-size:8pt; text-decoration: underline; color:#0068da;\">https://icons8.com/</span></a></p></body></html>", None))
    # retranslateUi

