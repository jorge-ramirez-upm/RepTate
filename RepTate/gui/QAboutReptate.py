import os
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

path = os.path.dirname(os.path.abspath(__file__))
Ui_AboutReptateWindow, QDialog = loadUiType(os.path.join(path,'AboutDialog.ui'))

class AboutWindow(QDialog, Ui_AboutReptateWindow):
    """About window in the GUI"""    
    def __init__(self, parent, version):
        super(AboutWindow, self).__init__(parent)
        self.setupUi(self)
        self.label_Version.setText('RepTate v'+version)
    
