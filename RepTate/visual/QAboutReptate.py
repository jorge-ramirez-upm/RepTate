from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

Ui_AboutReptateWindow, QDialog = loadUiType('gui/AboutDialog.ui')

class AboutWindow(QDialog, Ui_AboutReptateWindow):
        def __init__(self, parent):
            super(AboutWindow, self).__init__(parent)
            self.setupUi(self)

