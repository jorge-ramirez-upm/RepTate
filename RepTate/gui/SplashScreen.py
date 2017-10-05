from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap


class SplashScreen(QSplashScreen):
    """Class to define a splash screen to show loading progress"""
    def __init__(self):
        QtWidgets.QSplashScreen.__init__(
            self,
            QtGui.QPixmap("gui/Images/logo.jpg"))
        QtWidgets.QApplication.flush()

    def showMessage(self, msg):
        """Procedure to update message in splash"""
        align = QtCore.Qt.Alignment(QtCore.Qt.AlignBottom |
                                    QtCore.Qt.AlignRight |
                                    QtCore.Qt.AlignAbsolute)
        #color = QtGui.QColor(QtCore.Qt.White)
        color = QtGui.QColor(0, 0, 0)
        QSplashScreen.showMessage(self, msg, align, color)
        QApplication.processEvents()

    def clearMessage(self):
        QSplashScreen.clearMessage(self)
        QApplication.processEvents()

        