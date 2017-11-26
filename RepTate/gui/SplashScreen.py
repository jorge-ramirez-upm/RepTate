# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module SplasScreen

Module that defines the GUI Splashscreen that is loaded during the startup of RepTate.

""" 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

class SplashScreen(QSplashScreen):
    """Class to define a splash screen to show loading progress
    
    [description]
    """
    def __init__(self):
        """[summary]
        
        [description]
        """
        QtWidgets.QSplashScreen.__init__(
            self,
            QtGui.QPixmap("gui/Images/logo.jpg"))
        QtWidgets.QApplication.flush()

    def showMessage(self, msg):
        """Procedure to update message in splash
        
        [description]
        
        Arguments:
            msg {[type]} -- [description]
        """
        align = QtCore.Qt.Alignment(QtCore.Qt.AlignBottom |
                                    QtCore.Qt.AlignRight |
                                    QtCore.Qt.AlignAbsolute)
        #color = QtGui.QColor(QtCore.Qt.White)
        color = QtGui.QColor(0, 0, 0)
        QSplashScreen.showMessage(self, msg, align, color)
        QApplication.processEvents()

    def clearMessage(self):
        """[summary]
        
        [description]
        """
        QSplashScreen.clearMessage(self)
        QApplication.processEvents()
