import os
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication

from Application import *

path = os.path.dirname(os.path.abspath(__file__))
Ui_AppWindow, QApplicationWindow = loadUiType(os.path.join(path,'ApplicationWindow.ui'))

class QApplication(QApplicationWindow, Ui_AppWindow, Application):
    """ Abstract Reptate Application window"""    
    def __init__(self, parent=None):
        super(QApplication, self).__init__(parent)
        self.setupUi(self)

        
