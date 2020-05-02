# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# --------------------------------------------------------------------------------------------------------
#
# Authors:
#     Jorge Ramirez, jorge.ramirez@upm.es
#     Victor Boudara, victor.boudara@gmail.com
#
# Useful links:
#     http://blogs.upm.es/compsoftmatter/software/reptate/
#     https://github.com/jorge-ramirez-upm/RepTate
#     http://reptate.readthedocs.io
#
# --------------------------------------------------------------------------------------------------------
#
# Copyright (2017-2020): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
#
# This file is part of RepTate.
#
# RepTate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RepTate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RepTate.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------------------------
"""Module SplasScreen

Module that defines the GUI Splashscreen that is loaded during the startup of RepTate.

"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QSplashScreen, QApplication, QLabel
from PyQt5.QtGui import QPixmap, QFont
import RepTate.core.Version as Version

class SplashScreen(QSplashScreen):
    """Class to define a splash screen to show loading progress

    [description]
    """
    def __init__(self):
        """
        **Constructor**

        [description]
        """
        QSplashScreen.__init__(
            self,
            QPixmap(":/Images/Images/logo_with_uni_logo.png"))
        lblVersion = QLabel(self)
        lblVersion.setText("RepTate Version %s %s<br><small>\u00A9 Jorge Ramírez, Universidad Politécnica de Madrid<br>\u00A9 Victor Boudara, University of Leeds</small><br>(2017-2020)<br><a href=""https://dx.doi.org/10.1122/8.0000002"">Cite RepTate</a>" %(Version.VERSION, Version.DATE))
        font = self.font()
        font.setPixelSize(11)
        font.setWeight(QFont.Bold)
        self.setFont(font)
        lblVersion.adjustSize()
        #lblVersion.setStyleSheet("QLabel { color : white; }")
        #lblVersion.move(425 - lblVersion.width(), 195)
        QApplication.flush()

    def showMessage(self, msg):
        """Procedure to update message in splash

        [description]

        Arguments:
            - msg {[type]} -- [description]
        """
        align = Qt.Alignment(Qt.AlignBottom |
                             Qt.AlignRight |
                             Qt.AlignAbsolute)
        #color = QtGui.QColor(QtCore.Qt.White)
        color = QColor(0, 0, 0)
        QSplashScreen.showMessage(self, msg, align, color)
        QApplication.processEvents()

    def clearMessage(self):
        """[summary]

        [description]
        """
        QSplashScreen.clearMessage(self)
        QApplication.processEvents()

    def mousePressEvent(self, event):
        self.hide()
