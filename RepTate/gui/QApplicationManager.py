"""Module QApplicationManager

RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
http://blogs.upm.es/compsoftmatter/software/reptate/
https://github.com/jorge-ramirez-upm/RepTate
http://reptate.readthedocs.io
Jorge Ramirez, jorge.ramirez@upm.es
Victor Boudara, mmvahb@leeds.ac.uk

Module for the main Graphical User Interface of RepTate. It is the GUI counterpart of
ApplicationManager.

Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
This software is distributed under the GNU General Public License. 
""" 
import os
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QInputDialog

from QApplicationWindow import *
from ApplicationManager import *
from QAboutReptate import *

path = os.path.dirname(os.path.abspath(__file__))
Ui_MainWindow, QMainWindow = loadUiType(os.path.join(path,'ReptateMainWindow.ui'))

class QApplicationManager(ApplicationManager, QMainWindow, Ui_MainWindow):
    """ Main Reptate window and application manager"""    
    # count = 0
    reptatelogger = logging.getLogger('ReptateLogger')
    reptatelogger.setLevel(logging.DEBUG)

    def __init__(self, parent=None):
        super().__init__()
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        CmdBase.mode = CmdMode.GUI #set GUI mode
        self.setupUi(self)

        # App tabs behaviour
        self.ApplicationtabWidget.setMovable(True)
        self.ApplicationtabWidget.setTabsClosable(True)
        self.ApplicationtabWidget.setUsesScrollButtons(True)

        # log file
        log_file_name = 'Qreptate.log'
        handler = logging.handlers.RotatingFileHandler(
            log_file_name, maxBytes=20000, backupCount=2)
        self.reptatelogger.addHandler(handler)
        

        # Connect actions
        # Generate action buttons from dict of available applications
        self.actionMWD.triggered.connect(self.new_mwd_window)
        self.actionTTS.triggered.connect(self.new_tts_window)
        self.actionLVE.triggered.connect(self.new_lve_window)
        #self.actionNLVE.triggered.connect(self.new_nlve_window)
        self.actionGt.triggered.connect(self.new_gt_window)
        #self.actionCreep.triggered.connect(self.new_creep_window)
        #self.actionSANS.triggered.connect(self.new_sans_window)
        self.ApplicationtabWidget.tabCloseRequested.connect(self.close_app_tab)        
        self.ApplicationtabWidget.currentChanged.connect(self.tab_changed)
        #self.Projecttree.itemSelectionChanged.connect(self.treeChanged)
        
        self.actionAbout_Qt.triggered.connect(QApplication.aboutQt)
        self.actionAbout.triggered.connect(self.show_about)
        

        connection_id = self.ApplicationtabWidget.tabBarDoubleClicked.connect(self.handle_doubleClickTab)

        # CONSOLE WINDOW (need to integrate it with cmd commands)
        #self.text_edit = Console(self)
        #this is how you pass in locals to the interpreter
        #self.text_edit.initInterpreter(locals()) 
        #self.verticalLayout.addWidget(self.text_edit)

    def handle_doubleClickTab(self, index):
        """Edit DataSet-tab name"""
        old_name = self.ApplicationtabWidget.tabText(index)
        new_tab_name, success = QInputDialog.getText (
            self, "Change Name",
            "Insert New Tab Name",
            QLineEdit.Normal,
            old_name)
        if (success and new_tab_name!=""):    
            self.ApplicationtabWidget.setTabText(index, new_tab_name)

    def show_about(self):
        """ Show about window"""
        dlg = AboutWindow(self, self.version + ' ' + self.date)
        dlg.show()        

    def tab_changed(self, index):
        """Capture when the active application has changed"""
        #appname = self.ApplicationtabWidget.widget(index).windowTitle
        #items = self.Projecttree.findItems(appname, Qt.MatchContains)
        #self.Projecttree.setCurrentItem(items[0])
        pass

    def close_app_tab(self, index):    
        app_name = self.ApplicationtabWidget.widget(index).name
        self.ApplicationtabWidget.removeTab(index)
        self.delete(app_name)

    def Qopen_app(self, app_name, icon):
        newapp = self.new(app_name)
        newapp.createNew_Empty_Dataset() #populate with empty dataset at app opening
        app_id = "%s%d"%(app_name, self.application_counter)
        ind = self.ApplicationtabWidget.addTab(newapp, QIcon(icon), app_id)
        self.ApplicationtabWidget.setCurrentIndex(ind)


    def new_mwd_window(self):
        """ Open a new MWD application window"""
        app_name = 'MWD'
        self.Qopen_app(app_name, ':/Icons/Images/new_icons/icons8-MWD.png')


    def new_tts_window(self):
        """ Open a new TTS application window"""
        app_name = "TTS"
        self.Qopen_app(app_name, ':/Icons/Images/new_icons/icons8-TTS.png')

    def new_lve_window(self):
        """ Open a new LVE application window"""
        app_name = "LVE"
        self.Qopen_app(app_name, ':/Icons/Images/new_icons/icons8-LVE.png')

    def new_gt_window(self):
        """ Open a new Gt application window"""
        app_name = "Gt"
        self.Qopen_app(app_name, ':/Icons/Images/new_icons/icons8-Gt.png')

    def new_nlve_window(self):
        """ Open a new NLVE application window"""
        app_name = "NLVE"
        self.Qopen_app(app_name, ':/Icons/Images/new_icons/icons8-NLVE.png')
    
    def new_creep_window(self):
        """ Open a new Creep application window"""
        app_name = "Creep"
        self.Qopen_app(app_name, ':/Icons/Images/new_icons/icons8-Creep.png')

    def new_sans_window(self):
        """ Open a new SANS application window"""
        app_name = "SANS"
        self.Qopen_app(app_name, ':/Icons/Images/new_icons/icons8-SANS.png')
            