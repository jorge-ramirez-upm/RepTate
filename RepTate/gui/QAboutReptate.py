# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module QAboutReptate

Module that defines the About window.

""" 
from os.path import dirname, join, abspath
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUiType

path = dirname(abspath(__file__))
Ui_AboutReptateWindow, QDialog = loadUiType(join(path,'AboutDialog.ui'))

class AboutWindow(QDialog, Ui_AboutReptateWindow):
    """About window in the GUI
    
    [description]
    """
    def __init__(self, parent, version):
        """[summary]
        
        [description]
        
        Arguments:
            parent {[type]} -- [description]
            version {[type]} -- [description]
        """
        super(AboutWindow, self).__init__(parent)
        self.setupUi(self)
        self.label_Version.setText('RepTate v'+version)
    
