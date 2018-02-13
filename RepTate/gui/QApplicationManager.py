# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module QApplicationManager

Module for the main Graphical User Interface of RepTate. It is the GUI counterpart of
ApplicationManager.

""" 
import logging
from os.path import dirname, join, abspath
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QInputDialog,QLineEdit

from CmdBase import CmdBase, CmdMode, CalcMode
from QApplicationWindow import QApplicationWindow
from ApplicationManager import ApplicationManager
from QAboutReptate import AboutWindow

PATH = dirname(abspath(__file__))
Ui_MainWindow, QMainWindow = loadUiType(join(PATH,'ReptateMainWindow.ui'))

class QApplicationManager(ApplicationManager, QMainWindow, Ui_MainWindow):
    """Main Reptate window and application manager
    
    [description]
    """
    # count = 0
    reptatelogger = logging.getLogger('ReptateLogger')
    reptatelogger.setLevel(logging.DEBUG)

    def __init__(self, parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            parent {[type]} -- [description] (default: {None})
        """
        super().__init__()
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        CmdBase.mode = CmdMode.GUI #set GUI mode
        self.setupUi(self)

        if CmdBase.calcmode == CalcMode.singlethread:
            self.setWindowTitle('RepTate v' + self.version + ' ' + self.date + ' - SINGLE THREAD!!');
        else:
            self.setWindowTitle('RepTate v' + self.version + ' ' + self.date);

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
        self.actionNLVE.triggered.connect(self.new_nlve_window)
        self.actionGt.triggered.connect(self.new_gt_window)
        #self.actionCreep.triggered.connect(self.new_creep_window)
        #self.actionSANS.triggered.connect(self.new_sans_window)
        self.actionReact.triggered.connect(self.new_React_window)
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

    def list_theories_Maxwell(self, th_exclude=None):
        """Redefinition for the GUI mode that lists the tab names.
        List the theories in the current RepTate instance that provide and need
        Maxwell modes
        
        [description]
        
        Returns:
            [type] -- [description]
        """
        get_dict={}
        set_dict={}
        for app in self.applications.values():
            app_index = self.ApplicationtabWidget.indexOf(app)
            app_tab_name = self.ApplicationtabWidget.tabText(app_index)
            for ds in app.datasets.values():
                ds_index = app.DataSettabWidget.indexOf(ds)
                ds_tab_name = app.DataSettabWidget.tabText(ds_index)
                for th in ds.theories.values():
                    th_index = ds.TheorytabWidget.indexOf(th)
                    th_tab_name = ds.TheorytabWidget.tabText(th_index)
                    if th.has_modes and th != th_exclude:
                        get_dict["%s.%s.%s"%(app_tab_name, ds_tab_name, th_tab_name)] = th.get_modes
                        set_dict["%s.%s.%s"%(app_tab_name, ds_tab_name, th_tab_name)] = th.set_modes
        return get_dict, set_dict

    def handle_doubleClickTab(self, index):
        """Edit Application name, tab only, the dictinary key remains unchanged
        
        [description]
        
        Arguments:
            index {[type]} -- [description]
        """
        old_name = self.ApplicationtabWidget.tabText(index)
        dlg = QInputDialog(self)
        dlg.setWindowTitle("Change Application Name")
        dlg.setLabelText("New Application Name:")
        dlg.setTextValue(old_name)
        dlg.resize(400,100)
        success = dlg.exec()
        new_tab_name = dlg.textValue()
        if (success and new_tab_name!=""):    
            self.ApplicationtabWidget.setTabText(index, new_tab_name)
            # self.applications[old_name].name = new_tab_name
            # self.applications[new_tab_name] = self.applications.pop(old_name)
            

    def show_about(self):
        """Show about window
        
        [description]
        """
        dlg = AboutWindow(self, self.version + ' ' + self.date)
        dlg.show()        

    def tab_changed(self, index):
        """Capture when the active application has changed
        
        [description]
        
        Arguments:
            index {[type]} -- [description]
        """
        #appname = self.ApplicationtabWidget.widget(index).windowTitle
        #items = self.Projecttree.findItems(appname, Qt.MatchContains)
        #self.Projecttree.setCurrentItem(items[0])
        pass

    def close_app_tab(self, index):
        """[summary]
        
        [description]
        
        Arguments:
            index {[type]} -- [description]
        """
        app_name = self.ApplicationtabWidget.widget(index).name
        self.ApplicationtabWidget.removeTab(index)
        self.delete(app_name)

    def Qopen_app(self, app_name, icon):
        """[summary]
        
        [description]
        
        Arguments:
            app_name {[type]} -- [description]
            icon {[type]} -- [description]
        """
        newapp = self.new(app_name)
        newapp.createNew_Empty_Dataset() #populate with empty dataset at app opening
        app_id = "%s%d"%(app_name, self.application_counter)
        ind = self.ApplicationtabWidget.addTab(newapp, QIcon(icon), app_id)
        self.ApplicationtabWidget.setCurrentIndex(ind)
        self.ApplicationtabWidget.setTabToolTip(ind, app_name + " app")
        return newapp

    def new_app_from_name(self, app_name):
        """
        Open a new application window from name
        """
        self.Qopen_app(app_name, ':/Icons/Images/new_icons/icons8-%s.png'%app_name)
        

    def new_mwd_window(self):
        """Open a new MWD application window
        
        [description]
        """
        app_name = 'MWD'
        self.Qopen_app(app_name, ':/Icons/Images/new_icons/icons8-MWD.png')


    def new_tts_window(self):
        """Open a new TTS application window
        
        [description]
        """
        app_name = "TTS"
        self.Qopen_app(app_name, ':/Icons/Images/new_icons/icons8-TTS.png')

    def new_lve_window(self):
        """Open a new LVE application window
        
        [description]
        """
        app_name = "LVE"
        self.Qopen_app(app_name, ':/Icons/Images/new_icons/icons8-LVE.png')

    def new_gt_window(self):
        """Open a new Gt application window
        
        [description]
        """
        app_name = "Gt"
        self.Qopen_app(app_name, ':/Icons/Images/new_icons/icons8-Gt.png')

    def new_nlve_window(self):
        """Open a new NLVE application window
        
        [description]
        """
        app_name = "NLVE"
        self.Qopen_app(app_name, ':/Icons/Images/new_icons/icons8-NLVE.png')
    
    def new_creep_window(self):
        """Open a new Creep application window
        
        [description]
        """
        app_name = "Creep"
        self.Qopen_app(app_name, ':/Icons/Images/new_icons/icons8-Creep.png')

    def new_sans_window(self):
        """Open a new SANS application window
        
        [description]
        """
        app_name = "SANS"
        self.Qopen_app(app_name, ':/Icons/Images/new_icons/icons8-SANS.png')

    def new_React_window(self):
        """Open a new React application window
        
        [description]
        """
        app_name = "React"
        return self.Qopen_app(app_name, ':/Icons/Images/new_icons/icons8-test-tube.png')
