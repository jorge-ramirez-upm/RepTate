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
"""Module QAboutReptate

Module that defines the About window.

""" 
from os.path import dirname, join, abspath
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUiType

PATH = dirname(abspath(__file__))
Ui_AboutReptateWindow, QDialog = loadUiType(join(PATH,'AboutDialog.ui'))

class AboutWindow(QDialog, Ui_AboutReptateWindow):
    """About window in the GUI
    
    [description]
    """
    def __init__(self, parent, version):
        """
        **Constructor**
        
        Arguments:
            - parent {[type]} -- [description]
            - version {[type]} -- [description]
        """
        super(AboutWindow, self).__init__(parent)
        self.setupUi(self)
        self.label.setText('RepTate v'+version)
    
