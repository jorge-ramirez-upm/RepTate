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
        #self.actionTest.triggered.connect(self.new_test_window)
        #self.actionReact.triggered.connect(self.new_react_window)
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

    def tree_changed(self):
        """Capture when the active application has changed in the application navigator"""
        #print("HELLO")
        #appname = self.Projecttree.currentItem.text(0)
        #print(index, appname)
        pass

    def close_app_tab(self, index):    
        app_name = self.ApplicationtabWidget.widget(index).name
        self.ApplicationtabWidget.removeTab(index)
        self.delete(app_name)

    def new_tts_window(self):
        """ Open a new TTS application window"""
        app_name = "TTS"
        self.Qopen_app(app_name)

    def new_lve_window(self):
        """ Open a new LVE application window"""
        app_name = "LVE"
        self.Qopen_app(app_name)

    def new_gt_window(self):
        """ Open a new Gt application window"""
        app_name = "Gt"
        self.Qopen_app(app_name)

    def Qopen_app(self, app_name):
        newapp = self.new(app_name)
        newapp.createNew_Empty_Dataset() #populate with empty dataset at app opening
        app_id = "%s%d"%(app_name, self.application_counter)
        ind = self.ApplicationtabWidget.addTab(newapp, QIcon(':/Icons/Images/LVE.ico'), app_id)
        self.ApplicationtabWidget.setCurrentIndex(ind)
        #self.ApplicationtabWidget.currentItem().appname = app_name
        # newapp.new_tables_from_files(["data/PI_LINEAR/PI_94.9k_T-35.tts"])
        # root = QTreeWidgetItem(self.Projecttree, [app_name])
        # root.setIcon(0, QIcon(':/Icons/Images/LVE.ico'))


    def new_mwd_window(self):
        """ Open a new MWD application window"""
        app_name = 'MWD'
        self.Qopen_app(app_name)

        # self.count = self.count + 1
        # sub = ApplicationMWD(parent=self)
        # appname = sub.name + str(self.count)
        # sub.windowTitle = appname
        # ind = self.ApplicationtabWidget.addTab(sub, QIcon(':/Icons/Images/MWD.ico'), appname)
        # self.ApplicationtabWidget.setCurrentIndex(ind)

        # root = QTreeWidgetItem(self.Projecttree, [appname])
        # root.setIcon(0, QIcon(':/Icons/Images/MWD.ico'))

    def new_nlve_window(self):
        """ Open a new NLVE application window"""
        app_name = "NLVE"
        self.Qopen_app(app_name)
        # app_id = 'NLVE'
        # self.count = self.count + 1
        # sub = ApplicationNLVE(parent=self)
        # appname = sub.name + str(self.count)
        # sub.windowTitle = appname
        # ind = self.ApplicationtabWidget.addTab(sub, QIcon(':/Icons/Images/NLVE.ico'), appname)
        # self.ApplicationtabWidget.setCurrentIndex(ind)

        # root = QTreeWidgetItem(self.Projecttree, [appname])
        # root.setIcon(0, QIcon(':/Icons/Images/NLVE.ico'))

        # """ Open a new LVE application window"""
        # sub = ApplicationLVE()
        # #appname = sub.name
        # appname = 'TESTLVE'
        # #+ '%d'%MainWindow.count
        # #sub.windowTitle=appname
        
        # ind = self.ApplicationtabWidget.addTab(sub, QIcon(':Images/LVE.ico'), appname)
        # self.ApplicationtabWidget.setCurrentIndex(ind)        
        
        # #root = QTreeWidgetItem(self.Projecttree, [appname])
        # #root.setIcon(0, QIcon(':Icons/Images/Clip.ico'))
        # #sub.treeEntry = root
    