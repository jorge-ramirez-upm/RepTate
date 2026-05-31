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
"""Module QAboutReptate

Module that defines the About window.

"""

from PySide6.QtWidgets import QDialog, QLabel, QWidget

# PATH = dirname(abspath(__file__))
from RepTate.gui.Ui_AboutDialog import Ui_Dialog as Ui_AboutRepTateWindow


class AboutWindow(QDialog, Ui_AboutRepTateWindow):
    """About window in the GUI"""

    label: QLabel

    def __init__(self, parent: QWidget | None, version: str, text: str) -> None:
        """**Constructor**"""
        super(AboutWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(version)
        self.label.setText(text)
