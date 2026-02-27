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
# Copyright (2017-2026): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSplashScreen, QApplication, QLabel
from PySide6.QtGui import QPixmap, QFont, QColor
import RepTate
try:
    import RepTate.gui.About_rc
except ImportError:
    import logging
    import sys
    l = logging.getLogger("RepTate.gui.SplashScreen")
    l.fatal("Error importing RepTate.gui.About_rc. Please, run ""python scripts/build_ui.py"" or contact the developers.")
    sys.exit(1)


class SplashScreen(QSplashScreen):
    """Class to define a splash screen to show loading progress"""

    def __init__(self):
        """**Constructor**"""
        QSplashScreen.__init__(self, QPixmap(":/Images/Images/logo_with_uni_logo.png"))
        lblVersion = QLabel(self)

        # verdata = RepTate._version.get_versions()
        # version = verdata["version"].split("+")[0]
        # date = verdata["date"].split("T")[0]
        # build = verdata["version"]

        version = RepTate.__version__.split("+")[0]
        date = ""
        try:
            build = RepTate.__version__.split("+")[1]
        except IndexError:
            build = ""

        lblVersion.setText(
            'RepTate %s %s (build %s)<br><small>\u00a9 Jorge Ramírez, Universidad Politécnica de Madrid<br>\u00a9 Victor Boudara, University of Leeds</small><br>(2017-2026)<br><a href="https://dx.doi.org/10.1122/8.0000002">Cite RepTate</a>'
            % (version, date, build)
        )
        font = self.font()
        font.setPixelSize(11)
        font.setWeight(QFont.Bold)
        self.setFont(font)
        lblVersion.adjustSize()
        # lblVersion.setStyleSheet("QLabel { color : white; }")
        # lblVersion.move(425 - lblVersion.width(), 195)
        # QApplication.flush()

    def showMessage(self, msg):
        """Procedure to update message in splash"""
        align = Qt.Alignment(Qt.AlignBottom | Qt.AlignRight | Qt.AlignAbsolute)
        # color = QtGui.QColor(QtCore.Qt.White)
        color = QColor(0, 0, 0)
        QSplashScreen.showMessage(self, msg, align, color)
        QApplication.processEvents()

    def clearMessage(self):
        """Clear message in Splash"""
        QSplashScreen.clearMessage(self)
        QApplication.processEvents()

    def mousePressEvent(self, event):
        self.hide()
