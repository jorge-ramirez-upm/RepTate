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
"""Module QApplicationManager

Module for the main Graphical User Interface of RepTate. It is the GUI counterpart of
ApplicationManager.

"""
#import logging
import os
from os.path import dirname, join, abspath
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QIcon, QDesktopServices, QTextCursor
from PyQt5.QtCore import QUrl, Qt, QSize
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QInputDialog, QLineEdit, QMenu, QAction, QToolBar, QToolButton, QMessageBox, QFileDialog, QPlainTextEdit, QTextBrowser

from RepTate.core.CmdBase import CmdBase, CmdMode, CalcMode
from RepTate.gui.QApplicationWindow import QApplicationWindow
from RepTate.core.ApplicationManager import ApplicationManager
from RepTate.core.File import File
from RepTate.gui.QAboutReptate import AboutWindow
from collections import OrderedDict
import numpy as np
import time
import RepTate.core.Version as Version
import logging

PATH = dirname(abspath(__file__))
Ui_MainWindow, QMainWindow = loadUiType(join(PATH, 'ReptateMainWindow.ui'))

class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        #self.widget = QPlainTextEdit(parent)
        self.widget = QTextBrowser(parent)
        self.widget.setReadOnly(True)
        self.widget.setStyleSheet("background-color: rgb(255, 255, 222);")


    def emit(self, record):
        msg = self.format(record)
        #self.widget.appendPlainText(msg)

        self.widget.moveCursor(QTextCursor.End)
        self.widget.insertHtml(msg+'<br>')
        self.widget.verticalScrollBar().setValue(
            self.widget.verticalScrollBar().maximum())
        self.widget.moveCursor(QTextCursor.End)


class QApplicationManager(ApplicationManager, QMainWindow, Ui_MainWindow):
    """Main Reptate window and application manager

    [description]
    """
    help_file = 'http://reptate.readthedocs.io/index.html'

    def __init__(self, parent=None, loglevel=logging.INFO):
        """
        **Constructor**

        Keyword Arguments:
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(loglevel=loglevel)
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        CmdBase.mode = CmdMode.GUI  #set GUI mode
        self.setupUi(self)

        if CmdBase.calcmode == CalcMode.singlethread:
            self.setWindowTitle('RepTate v' + self.version + ' ' + self.date +
                                ' - SINGLE THREAD!!')
        else:
            self.setWindowTitle('RepTate v' + self.version + ' ' + self.date)

        # Add Apps
        self.toolBarApps.addAction(self.actionMWD)
        tbut = QToolButton()
        tbut.setPopupMode(QToolButton.MenuButtonPopup)
        tbut.setDefaultAction(self.actionTTS)
        menu = QMenu()
        menu.addAction(self.actionTTSFactors)
        tbut.setMenu(menu)
        self.toolBarApps.addWidget(tbut)
        self.toolBarApps.addAction(self.actionLVE)
        self.toolBarApps.addAction(self.actionNLVE)
        self.toolBarApps.addAction(self.actionCrystal)
        self.toolBarApps.addAction(self.actionGt)
        self.toolBarApps.addAction(self.actionCreep)
        self.toolBarApps.addAction(self.actionSANS)
        self.toolBarApps.addAction(self.actionReact)
        self.toolBarApps.addAction(self.actionDielectric)
        # self.toolBarApps.addAction(self.actionDynamicStructureFactor)
        self.toolBarApps.addAction(self.actionLAOS)

        #help button
        icon = QIcon(':/Icon8/Images/new_icons/icons8-user-manual.png')
        #self.show_reptate_help = QAction(icon, 'RepTate Manual', self)
        #self.show_app_help = QAction(icon, 'Application Manual', self)
        #self.show_th_help = QAction(icon, 'Theory Manual', self)
        tbut = QToolButton()
        tbut.setPopupMode(QToolButton.MenuButtonPopup)
        tbut.setDefaultAction(self.actionShow_reptate_help)
        menu = QMenu()
        menu.addAction(self.actionShow_app_help)
        menu.addAction(self.actionShow_th_help)
        menu.addAction(self.actionShow_offline_help)
        tbut.setMenu(menu)
        #self.toolBarHelpAbout.insertWidget(self.actionAbout_Qt, tbut)
        self.toolBarHelpAbout.addWidget(tbut)
        self.toolBarHelpAbout.addSeparator()

        self.toolBarHelpAbout.addAction(self.actionShow_Logger)

        tbut = QToolButton()
        tbut.setPopupMode(QToolButton.MenuButtonPopup)
        tbut.setDefaultAction(self.actionAbout)
        menu = QMenu()
        menu.addAction(self.actionAbout_Qt)
        menu.addAction(self.actionAboutMatplotlib)
        menu.addAction(self.actionAboutNumpy)
        menu.addAction(self.actionAboutScipy)
        menu.addSeparator()
        menu.addAction(self.actionCite_RepTate)
        menu.addAction(self.actionCheckRepTateVersion)
        tbut.setMenu(menu)
        self.toolBarHelpAbout.addWidget(tbut)

        self.toolBarHelpAbout.insertSeparator(self.actionAbout_Qt)
        #self.toolBar.insertSeparator(self.actionQuit)
        self.toolBarProject.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolBarApps.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolBarHelpAbout.setContextMenuPolicy(Qt.PreventContextMenu)

        # # ApplicationXY button
        # #choose the button icon
        # icon = QIcon(':/Icon8/Images/new_icons/XY.png')
        # tool_tip = 'XY'  # text that appear on hover
        # self.actionXY = QAction(icon, tool_tip, self)
        # #insert the new button before the "MWD" button
        # self.toolBarApps.insertAction(self.actionMWD, self.actionXY)
        # #connect button
        # self.actionXY.triggered.connect(lambda: self.handle_new_app('XY'))

        # App tabs behaviour
        self.ApplicationtabWidget.setMovable(True)
        self.ApplicationtabWidget.setTabsClosable(True)
        self.ApplicationtabWidget.setUsesScrollButtons(True)

        # Connect actions
        self.actionOpenProject.triggered.connect(self.launch_open_dialog)
        self.actionSaveProject.triggered.connect(self.launch_save_dialog)

        # Generate action buttons from dict of available applications
        self.actionMWD.triggered.connect(lambda: self.handle_new_app('MWD'))
        self.actionTTS.triggered.connect(lambda: self.handle_new_app('TTS'))
        self.actionTTSFactors.triggered.connect(lambda: self.handle_new_app('TTSF'))
        self.actionLVE.triggered.connect(lambda: self.handle_new_app('LVE'))
        self.actionNLVE.triggered.connect(lambda: self.handle_new_app('NLVE'))
        self.actionCrystal.triggered.connect(lambda: self.handle_new_app('Crystal'))
        self.actionGt.triggered.connect(lambda: self.handle_new_app('Gt'))
        self.actionCreep.triggered.connect(lambda: self.handle_new_app('Creep'))
        self.actionSANS.triggered.connect(lambda: self.handle_new_app('SANS'))
        self.actionReact.triggered.connect(lambda: self.handle_new_app('React'))
        self.actionDielectric.triggered.connect(lambda: self.handle_new_app('Dielectric'))
        self.actionLAOS.triggered.connect(lambda: self.handle_new_app('LAOS'))
        # self.actionLAOS.triggered.connect(lambda: self.handle_app_coming_soon('LAOS'))
        # self.actionDynamicStructureFactor.triggered.connect(lambda: self.handle_app_coming_soon('DynamicStructureFactor'))

        self.ApplicationtabWidget.tabCloseRequested.connect(self.close_app_tab)
        self.ApplicationtabWidget.currentChanged.connect(self.tab_changed)

        self.actionAbout_Qt.triggered.connect(QApplication.aboutQt)
        self.actionAbout.triggered.connect(self.show_about)

        connection_id = self.ApplicationtabWidget.tabBarDoubleClicked.connect(
            self.handle_doubleClickTab)
        # help buttons
        self.actionShow_reptate_help.triggered.connect(self.handle_show_reptate_help)
        self.actionShow_app_help.triggered.connect(self.handle_show_app_help)
        self.actionShow_th_help.triggered.connect(self.handle_show_th_help)
        self.actionShow_offline_help.triggered.connect(self.handle_actionShow_offline_help)

        # additional about buttons
        self.actionAboutMatplotlib.triggered.connect(self.handle_about_matplotlib)
        self.actionAboutNumpy.triggered.connect(self.handle_about_numpy)
        self.actionAboutScipy.triggered.connect(self.handle_about_scipy)
        self.actionCite_RepTate.triggered.connect(self.handle_cite_RepTate)
        self.actionCheckRepTateVersion.triggered.connect(self.handle_check_RepTate_version)

        connection_id = self.LoggerdockWidget.visibilityChanged.connect(self.handle_loggerVisibilityChanged)
        connection_id = self.actionShow_Logger.triggered.connect(self.showLogger)

        tb = QToolBar()
        tb.setIconSize(QSize(24,24))
        tb.setOrientation(Qt.Vertical)

        self.tbutlog = QToolButton()
        self.tbutlog.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        menu.addAction(self.actionLogNotSet)
        menu.addAction(self.actionLogDebug)
        menu.addAction(self.actionLogInfo)
        menu.addAction(self.actionLogWarning)
        menu.addAction(self.actionLogError)
        menu.addAction(self.actionLogCritical)
        if loglevel==logging.NOTSET:
            self.tbutlog.setDefaultAction(self.actionLogNotSet)
        elif loglevel==logging.DEBUG:
            self.tbutlog.setDefaultAction(self.actionLogDebug)
        elif loglevel==logging.INFO:
            self.tbutlog.setDefaultAction(self.actionLogInfo)
        elif loglevel==logging.WARNING:
            self.tbutlog.setDefaultAction(self.actionLogWarning)
        elif loglevel==logging.ERROR:
            self.tbutlog.setDefaultAction(self.actionLogError)
        elif loglevel==logging.CRITICAL:
            self.tbutlog.setDefaultAction(self.actionLogCritical)
        self.tbutlog.setMenu(menu)
        tb.addWidget(self.tbutlog)

        tb.addAction(self.actionCopyLogText)
        self.LoggerdochorizontalLayout.addWidget(tb)

        self.logTextBox = QTextEditLogger(self)
        formatter = logging.Formatter('<font color=blue>%(asctime)s</font> <b>%(name)s <font color=red>%(levelname)s</font></b>: %(message)s',
                                "%Y%m%d %H%M%S")
        self.logTextBox.setFormatter(formatter)
        logging.getLogger('RepTate').addHandler(self.logTextBox)
        logging.getLogger('RepTate').setLevel(loglevel)
        import matplotlib
        matplotlib._log.addHandler(self.logTextBox)
        self.logTextBox.setLevel(loglevel)
        self.LoggerdochorizontalLayout.addWidget(self.logTextBox.widget)

        connection_id = self.actionLogNotSet.triggered.connect(self.logNotSet)
        connection_id = self.actionLogDebug.triggered.connect(self.logDebug)
        connection_id = self.actionLogInfo.triggered.connect(self.logInfo)
        connection_id = self.actionLogWarning.triggered.connect(self.logWarning)
        connection_id = self.actionLogError.triggered.connect(self.logError)
        connection_id = self.actionLogCritical.triggered.connect(self.logCritical)
        connection_id = self.actionCopyLogText.triggered.connect(self.copyLogText)

        #self.add_save_load_buttons()
        self.REPTATE_PROJ_JSON = 'reptate_project.json' # json filename inside zip
        self.load_path = None

        # CONSOLE WINDOW (need to integrate it with cmd commands)
        #self.text_edit = Console(self)
        #this is how you pass in locals to the interpreter
        #self.text_edit.initInterpreter(locals())
        #self.verticalLayout.addWidget(self.text_edit)

        # Hide Logger Window
        self.LoggerdockWidget.hide()

    def showLogger(self, checked):
        """Handle show Log window"""
        if checked:
            self.LoggerdockWidget.show()
        else:
            self.LoggerdockWidget.hide()

    def handle_loggerVisibilityChanged(self, visible):
        """Handle the hide/show event of the logger window"""
        self.actionShow_Logger.setChecked(visible)

    def logNotSet(self):
        logging.getLogger('RepTate').setLevel(logging.NOTSET)
        self.logTextBox.setLevel(logging.NOTSET)
        self.tbutlog.setDefaultAction(self.actionLogNotSet)

    def logDebug(self):
        logging.getLogger('RepTate').setLevel(logging.DEBUG)
        self.logTextBox.setLevel(logging.DEBUG)
        self.tbutlog.setDefaultAction(self.actionLogDebug)

    def logInfo(self):
        logging.getLogger('RepTate').setLevel(logging.INFO)
        self.logTextBox.setLevel(logging.INFO)
        self.tbutlog.setDefaultAction(self.actionLogInfo)

    def logWarning(self):
        logging.getLogger('RepTate').setLevel(logging.WARNING)
        self.logTextBox.setLevel(logging.WARNING)
        self.tbutlog.setDefaultAction(self.actionLogWarning)

    def logError(self):
        logging.getLogger('RepTate').setLevel(logging.ERROR)
        self.logTextBox.setLevel(logging.ERROR)
        self.tbutlog.setDefaultAction(self.actionLogError)

    def logCritical(self):
        logging.getLogger('RepTate').setLevel(logging.CRITICAL)
        self.logTextBox.setLevel(logging.CRITICAL)
        self.tbutlog.setDefaultAction(self.actionLogCritical)

    def copyLogText(self):
        self.logTextBox.widget.selectAll()
        self.logTextBox.widget.copy()

    def handle_show_reptate_help(self):
        """Show RepTate documentation"""
        try:
            help_file = self.help_file
        except AttributeError as e:
            print('in "handle_show_help":', e)
            return
        QDesktopServices.openUrl(QUrl.fromUserInput((help_file)))

    def handle_show_app_help(self):
        """Show RepTate current application (if any) manual, or all applications"""
        try:
            help_file = self.ApplicationtabWidget.currentWidget().help_file
        except AttributeError as e:
            print('in "handle_show_help":', e)
            help_file = 'http://reptate.readthedocs.io/manual/Applications/applications.html'
        QDesktopServices.openUrl(QUrl.fromUserInput((help_file)))

    def handle_show_th_help(self):
        """Show RepTate current theory (if any) manual, or all theories"""
        try:
            app = self.ApplicationtabWidget.currentWidget()
            ds = app.DataSettabWidget.currentWidget()
            th = ds.theories[ds.current_theory]
            help_file = th.help_file
        except Exception as e:
            print('in "handle_show_help":', e)
            help_file = 'http://reptate.readthedocs.io/manual/All_Theories/All_Theories.html'
        QDesktopServices.openUrl(QUrl.fromUserInput((help_file)))

    def handle_actionShow_offline_help(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile('docs/build/html/index.html'))

    def handle_about_matplotlib(self):
        """Show matplotlib web site"""
        QDesktopServices.openUrl(QUrl.fromUserInput(('https://matplotlib.org/index.html')))

    def handle_about_numpy(self):
        """Show numpy web site"""
        QDesktopServices.openUrl(QUrl.fromUserInput(('http://www.numpy.org/')))

    def handle_about_scipy(self):
        """Show scipy web site"""
        QDesktopServices.openUrl(QUrl.fromUserInput(('https://scipy.org/')))

    def handle_cite_RepTate(self):
        """Visit the web site of the RepTatepaper"""
        QDesktopServices.openUrl(QUrl.fromUserInput(('https://dx.doi.org/10.1122/8.0000002')))

    def handle_check_RepTate_version(self):
        """Query Github for the latest RepTate release"""
        newversion, version_github, version_current = self.check_version()
        if newversion:
            ans = QMessageBox.question(self, 'New RepTate version found',
                "The version of RepTate on Github (%s) is more recent than the one you are running (%s).Do you want to check the new features?"%(version_github, version_current),
                QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
            if ans == QMessageBox.Yes:
                QDesktopServices.openUrl(QUrl.fromUserInput(('https://github.com/jorge-ramirez-upm/RepTate/releases')))
        else:
            QMessageBox.information(self, 'You are running the latest version of RepTate',
                "The version of RepTate you are running (%s) is up to date with respect to the version on Github (%s)"%(version_current, version_github))

    def list_theories_Maxwell(self, th_exclude=None):
        """Redefinition for the GUI mode that lists the tab names.
        List the theories in the current RepTate instance that provide and need
        Maxwell modes

        [description]

        Returns:
            - [type] -- [description]
        """
        get_dict = {}
        set_dict = {}
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
                        get_dict["%s.%s.%s" % (app_tab_name, ds_tab_name,
                                               th_tab_name)] = th.get_modes
                        set_dict["%s.%s.%s" % (app_tab_name, ds_tab_name,
                                               th_tab_name)] = th.set_modes
        return get_dict, set_dict

    def handle_doubleClickTab(self, index):
        """Edit Application name, tab only, the dictinary key remains unchanged

        [description]

        Arguments:
            - index {[type]} -- [description]
        """
        old_name = self.ApplicationtabWidget.tabText(index)
        dlg = QInputDialog(self)
        dlg.setWindowTitle("Change Application Name")
        dlg.setLabelText("New Application Name:")
        dlg.setTextValue(old_name)
        dlg.resize(400, 100)
        success = dlg.exec()
        new_tab_name = dlg.textValue()
        if (success and new_tab_name != ""):
            self.ApplicationtabWidget.setTabText(index, new_tab_name)
            # self.applications[old_name].name = new_tab_name
            # self.applications[new_tab_name] = self.applications.pop(old_name)

    def show_about(self):
        """Show about window

        [description]
        """
        #dlg = AboutWindow(self, self.version + ' ' + self.date)
        dlg = AboutWindow(self, "%s %s<br><small>\u00A9 Jorge Ramírez, Universidad Politécnica de Madrid<br>\u00A9 Victor Boudara, University of Leeds</small><br>(2017-2020)<br><a href=""https://dx.doi.org/10.1122/8.0000002"">Cite RepTate</a>" %(Version.VERSION, Version.DATE))
        dlg.show()

    def tab_changed(self, index):
        """Capture when the active application has changed

        [description]

        Arguments:
            - index {[type]} -- [description]
        """
        #appname = self.ApplicationtabWidget.widget(index).windowTitle
        #items = self.Projecttree.findItems(appname, Qt.MatchContains)
        #self.Projecttree.setCurrentItem(items[0])
        pass

    def close_app_tab(self, index):
        """[summary]

        [description]

        Arguments:
            - index {[type]} -- [description]
        """
        app = self.ApplicationtabWidget.widget(index)
        ds_name_list = [key for key in app.datasets]
        for ds_name in ds_name_list:
            app.delete(ds_name) #call theory destructor
        self.ApplicationtabWidget.removeTab(index)
        self.delete(app.name)

    def Qopen_app(self, app_name, icon):
        """[summary]

        [description]

        Arguments:
            - app_name {[type]} -- [description]
            - icon {[type]} -- [description]
        """
        newapp = self.new(app_name)
        newapp.createNew_Empty_Dataset(
        )  #populate with empty dataset at app opening
        app_tabname = "%s%d" % (app_name, self.application_counter)
        ind = self.ApplicationtabWidget.addTab(newapp, QIcon(icon), app_tabname)
        self.ApplicationtabWidget.setCurrentIndex(ind)
        self.ApplicationtabWidget.setTabToolTip(ind, app_name + " app")
        return newapp

    def handle_new_app(self, app_name=''):
        """
        Open a new application window from name
        """
        self.Qopen_app(app_name,
                       ':/Icons/Images/new_icons/%s.png' % app_name)


    def handle_app_coming_soon(self, appname=''):
        """Show message"""
        QMessageBox.warning(self, "new %s application"% appname, "%s coming soon..." % appname)



############################
#SAVE/LOAD REPTATE SESSION
############################


    def closeEvent(self, event):
        """Ask if we want to save project before closing RepTate (uncomment the rest)"""
        pass
        # btns = (QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        # msg = 'Do you want to save your project before exiting RepTate?'
        # title = 'Quit'
        # ans = QMessageBox.question(self, title , msg, buttons=btns)
        # if ans == QMessageBox.No:
        #     event.accept()
        # elif ans == QMessageBox.Yes:
        #     success = self.launch_save_dialog()
        #     if not success:
        #         event.ignore()
        # elif ans == QMessageBox.Cancel:
        #     event.ignore()

    def launch_open_dialog(self):
        """Get filename of RepTate project to open"""
        if self.load_path:
            fpath, _ = QFileDialog.getOpenFileName(self,
                "Open RepTate Project", self.load_path, "RepTate Project (*.rept)")
        else:
            fpath, _ = QFileDialog.getOpenFileName(self,
                "Open RepTate Project", "data/", "RepTate Project (*.rept)")
        if fpath == '':
            return
        self.open_project(fpath)

    def launch_save_dialog(self):
        """Get filename of RepTate project to save"""
        if self.load_path:
            fpath, _ = QFileDialog.getSaveFileName(self,
                "Save RepTate Project", self.load_path, "RepTate Project (*.rept)")
        else:
            fpath, _ = QFileDialog.getSaveFileName(self,
                "Save RepTate Project", "data/", "RepTate Project (*.rept)")
        if fpath == '':
            return False
        self.save_reptate(fpath)
        return True

    def save_reptate(self, fpath):
        """Save RepTate project to 'fpath'"""
        self.load_path = fpath
        apps_dic = OrderedDict()
        napps = self.ApplicationtabWidget.count()
        nth_saved = 0
        nfile_saved = 0
        ntool_saved = 0
        for i in range(napps):
            app = self.ApplicationtabWidget.widget(i)

            # Save DataSets in application
            datasets_dic = OrderedDict()
            ndatasets = app.DataSettabWidget.count()
            for j in range(ndatasets):
                ds = app.DataSettabWidget.widget(j)
                files_dic = OrderedDict()
                for f in ds.files:
                    nfile_saved += 1
                    param_dic = OrderedDict([ (pname, f.file_parameters[pname]) for pname in f.file_parameters])

                    file_dic = OrderedDict(
                        [
                            ('fname', os.path.basename(f.file_full_path)),
                            ('is_active', f.active),
                            ('fparam', param_dic),
                            ('ftable', f.data_table.data.tolist()),
                            ('with_extra_x', int(f.with_extra_x)),
                            ('theory_xmin', f.theory_xmin),
                            ('theory_xmax', f.theory_xmax),
                            ('theory_logspace', int(f.theory_logspace)),
                            ('th_num_pts', f.th_num_pts),
                            ('nextramin', f.nextramin),
                            ('nextramax', f.nextramax),
                        ]
                    )
                    files_dic[f.file_name_short] = file_dic

                # Save theories in DataSet
                theories_dic = OrderedDict()
                ntheories = ds.TheorytabWidget.count()
                for k in range(ntheories):
                    nth_saved += 1
                    th = ds.TheorytabWidget.widget(k)
                    param_dic = OrderedDict([(pname, th.parameters[pname].value) for pname in th.parameters])
                    th_table_dic = OrderedDict(
                        [ (f.file_name_short, th.tables[f.file_name_short].data.tolist()) for f in ds.files]
                    )
                    # save extra_tables
                    th_extra_table_dic = OrderedDict()
                    for f in ds.files:
                        dic_copy = {}
                        # loop over extra table and convert np.array to list
                        for et_key in th.tables[f.file_name_short].extra_tables:
                            val = th.tables[f.file_name_short].extra_tables[et_key]
                            if type(val) is np.ndarray:
                                dic_copy[et_key] = val.tolist()
                            else:
                                dic_copy[et_key] = val
                        th_extra_table_dic[f.file_name_short] = dic_copy

                    th.get_extra_data()
                    e_dic = th.extra_data
                    e_dic_copy = {}
                    # convert numpy arrays into lists
                    for key in e_dic:
                        val = e_dic[key]
                        if type(val) is np.ndarray:
                            e_dic_copy[key] = val.tolist()
                        else:
                            e_dic_copy[key] = val

                    th_dic = OrderedDict(
                        [
                            ('th_tabname', ds.TheorytabWidget.tabText(k)),
                            ('thname', th.thname),
                            ('th_param', param_dic),
                            ('th_textbox', str(th.thTextBox.toHtml()) + '<br><i>Saved at %s on %s<i><br>' % (time.strftime("%X"), time.strftime("%a %b %d, %Y") )),
                            ('th_tables', th_table_dic),
                            ('th_extra_table_dic', th_extra_table_dic),
                            ('extra_data', e_dic_copy)
                        ]
                    )
                    theories_dic[th.name] = th_dic

                # Save figure markers
                ds_markers = OrderedDict(
                    [
                        ('marker_size', ds.marker_size),
                        ('line_width', ds.line_width),
                        ('colormode', ds.colormode),
                        ('color1', ds.color1),
                        ('color2', ds.color2),
                        ('th_line_mode', ds.th_line_mode),
                        ('th_color', ds.th_color),
                        ('palette_name', ds.palette_name),
                        ('symbolmode', ds.symbolmode),
                        ('symbol1', ds.symbol1),
                        ('symbol1_name', ds.symbol1_name),
                        ('th_linestyle', ds.th_linestyle),
                        ('th_line_width', ds.th_line_width)
                    ]
                )
                # Save full DataSet
                ds_dict = OrderedDict(
                    [
                        ('ds_tabname', app.DataSettabWidget.tabText(j)),
                        ('files', files_dic),
                        ('current_th_indx', ds.TheorytabWidget.currentIndex()),
                        ('theories', theories_dic),
                        ('ds_markers', ds_markers)
                    ]
                )
                datasets_dic[ds.name] = ds_dict

            # Save Tools
            tools_dic = OrderedDict() # contain all the tools
            for tool in app.tools:
                ntool_saved += 1
                param_dic = OrderedDict()
                for pname in tool.parameters:
                    param_dic[pname] = tool.parameters[pname].value
                tool_dic = OrderedDict(
                    [
                        ('tool_name', tool.toolname), # what tool
                        ('tool_tab_name', app.TooltabWidget.tabText(app.TooltabWidget.indexOf(tool))),
                        ('tool_to_th', int(tool.actionApplyToTheory.isChecked())),
                        ('tool_active', int(tool.actionActive.isChecked())),
                        ('tool_param', param_dic),
                        ('tool_txtbox', str(tool.toolTextBox.toHtml() + '<br><i>Saved at %s on %s<i><br>' % (time.strftime("%X"), time.strftime("%a %b %d, %Y"))))
                    ]
                )
                #add to global tools dic
                tools_dic[tool.name] = tool_dic

            # all tools plus extra
            tools = {
                'tools_dic': tools_dic,
                'cur_tab_index': app.TooltabWidget.currentIndex()
            }

            # annotations
            ann_dict = OrderedDict()
            for k, ann in enumerate(app.graphicnotes):
                ann_opts = {}
                ann_text = ann.get_text()
                ann_x, ann_y = ann.get_position()
                ann_opts["color"] = ann.get_color()
                ann_opts["rotation"] = ann.get_rotation()
                ann_opts["horizontalalignment"] = ann.get_horizontalalignment()
                ann_opts["verticalalignment"] = ann.get_verticalalignment()
                ann_opts["fontweight"] = ann.get_fontweight()
                ann_opts["style"] = ann.get_fontstyle()
                ann_opts["fontsize"] = ann.get_fontsize()
                ann_opts["alpha"] = ann.get_alpha()
                ann_opts["family"] = ann.get_fontfamily()[0]
                ann_opts["zorder"] = ann.get_zorder()

                ann_dict["annotation_%02d" % (k + 1)] = {
                    "ann_text": ann_text,
                    "ann_x": ann_x,
                    "ann_y": ann_y,
                    "ann_opts": ann_opts
                    }

            # collect all app info
            app_dic = OrderedDict(
                [
                    ('app_tabname', self.ApplicationtabWidget.tabText(i)),
                    ('app_indx', i),
                    ('appname', app.appname),
                    ('current_view_names', [v.name for v in app.multiviews]),
                    ('current_ds_indx', app.DataSettabWidget.currentIndex()),
                    ('datasets', datasets_dic),
                    ('tools', tools),
                    ('show_inspector', int(app.DataInspectordockWidget.isVisible())),
                    ('annotations', ann_dict),
                    ('axis_options', app.ax_opts),
                    ('legend_opts', app.legend_opts)
                ]
            )

            apps_dic[app.name] = app_dic

        current_app_indx = self.ApplicationtabWidget.currentIndex()
        out = OrderedDict(
            [
                ('RepTate_version', Version.VERSION + '_' + Version.DATE),
                ('project_saved_at', '%s on %s' % (time.strftime("%X"), time.strftime("%a %b %d, %Y"))),
                ('napp_saved', napps), ('nfile_saved', nfile_saved),
                ('nth_saved', nth_saved),
                ('ntool_saved', ntool_saved),
                ('current_app_indx', current_app_indx), ('apps', apps_dic)
                ]
            )

        # zip output file
        import json, zipfile, tempfile
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmp = os.path.join(tmpdirname, 'tmp')
            json.dump(out, open(tmp, 'w'), indent=4)
            with zipfile.ZipFile(fpath, 'w', compression=zipfile.ZIP_DEFLATED) as z:
                z.write(tmp, self.REPTATE_PROJ_JSON)

        if napps > 1:
            txtapp = 'Applications'
        else:
            txtapp = 'Application'
        if nth_saved > 1:
            txtth = 'theories'
        else:
            txtth = 'theory'
        if nfile_saved > 1:
            txtfiles = 'files'
        else:
            txtfiles = 'file'
        if ntool_saved > 1:
            txttool = 'tools'
        else:
            txttool = 'tool'
        QMessageBox.information(self, 'Save RepTate Project', 'Saved %d %s, %d %s, %d %s, and %d %s to \"%s\"' % (napps, txtapp, nth_saved, txtth, nfile_saved, txtfiles, ntool_saved, txttool, fpath))

    # load RepTate session
############################

    def restore_app(self, app_name, app_tabname):
        """Open new application"""
        newapp = self.new(app_name)
        icon = QIcon(':/Icons/Images/new_icons/%s.png' % app_name)
        ind = self.ApplicationtabWidget.addTab(newapp, icon, app_tabname)
        # self.ApplicationtabWidget.setCurrentIndex(ind)
        self.ApplicationtabWidget.setTabToolTip(ind, app_name + " app")
        return self.ApplicationtabWidget.widget(ind), ind

    def restore_files(self, ds, files):
        """Open data files"""
        for file_dic in files.values():
            fname = file_dic['fname']
            is_active = file_dic['is_active']
            fparams = file_dic['fparam'] # dict
            ftable = np.asarray(file_dic['ftable'])


            f_ext = fname.split('.')[-1]
            ft = ds.parent_application.filetypes[f_ext]
            f = File(fname, ft, ds, ds.parent_application.axarr)
            f.data_table.num_rows, f.data_table.num_columns = ftable.shape
            f.data_table.data = ftable

            ds.files.append(f)
            ds.current_file = f
            f.active = is_active
            for pname in fparams:
                f.file_parameters[pname] = fparams[pname]
            try:
                f.with_extra_x = bool(file_dic['with_extra_x'])
                f.theory_xmin = file_dic['theory_xmin']
                f.theory_xmax = file_dic['theory_xmax']
                f.theory_logspace = bool(file_dic['theory_logspace'])
                f.th_num_pts = file_dic['th_num_pts']
                f.nextramin = file_dic['nextramin']
                f.nextramax = file_dic['nextramax']
            except KeyError:
                pass # backward compatibility

            ds.parent_application.addTableToCurrentDataSet(f, f_ext)
            ds.do_plot()
            ds.parent_application.update_Qplot()
            ds.set_table_icons(ds.table_icon_list)

    def restore_theories(self, ds, theories):
        """Open theories"""
        for th_dic in theories.values():
            th_tabname = th_dic['th_tabname']
            thname = th_dic['thname']
            th_param = th_dic['th_param']
            th_textbox = th_dic['th_textbox']
            th_tables = th_dic['th_tables']
            extra_data = th_dic['extra_data']
            try:
                extra_table_dic = th_dic['th_extra_table_dic']
            except KeyError:
                # backward compatibility
                extra_table_dic = {}

            for key in extra_data:
                val = extra_data[key]
                if type(val) == list:
                    extra_data[key] = np.asarray(val)

            if thname == 'SCCR':
                thname = 'GLaMM' # backward compatibility
            new_th = ds.new_theory(thname, th_tabname, calculate=False, show=False)
            autocal = new_th.autocalculate
            new_th.autocalculate = False
            for pname in th_param:
                new_th.set_param_value(pname, th_param[pname])
            for fname in th_tables:
                tt = new_th.tables[fname]
                tt.data = np.asarray(th_tables[fname])
                try:
                    tt.num_rows, tt.num_columns = tt.data.shape
                except ValueError:
                    tt.num_rows, tt.num_columns = (0, 0)
            for fname in extra_table_dic:
                tt_dic = new_th.tables[fname].extra_tables
                for key in extra_table_dic[fname]:
                    tt_dic[key] = np.asarray(extra_table_dic[fname][key])
            new_th.set_extra_data(extra_data)
            new_th.update_parameter_table()
            new_th.thTextBox.insertHtml(th_textbox)
            new_th.autocalculate = autocal

    def restore_marker_settings(self, ds, marker_dic):
        """Restore the dataset marker settings"""
        ds.marker_size = marker_dic['marker_size']
        ds.line_width = marker_dic['line_width']
        ds.colormode = marker_dic['colormode']
        ds.color1 = marker_dic['color1']
        ds.color2 = marker_dic['color2']
        ds.th_line_mode = marker_dic['th_line_mode']
        ds.th_color = marker_dic['th_color']
        ds.palette_name = marker_dic['palette_name']
        ds.symbolmode = marker_dic['symbolmode']
        ds.symbol1 = marker_dic['symbol1']
        ds.symbol1_name = marker_dic['symbol1_name']
        ds.th_linestyle = marker_dic['th_linestyle']
        ds.th_line_width = marker_dic['th_line_width']

    def restore_tools(self, app, tools):
        """Restore the tools"""
        for tdic in tools['tools_dic'].values():
            toolname = tdic['tool_name']
            tool_tab_name = tdic['tool_tab_name']
            tool_to_th = tdic['tool_to_th']
            tool_active = tdic['tool_active']
            tool_param = tdic['tool_param']
            tool_txtbox = tdic['tool_txtbox']

            # create new tool and set state
            to = app.new_tool(toolname, tool_tab_name)
            to.handle_actionApplyToTheorypressed(bool(tool_to_th))
            to.handle_actionActivepressed(bool(tool_active))
            to.toolTextBox.insertHtml(tool_txtbox)
            for pname in tool_param:
                to.set_param_value(pname, tool_param[pname])
        app.TooltabWidget.setCurrentIndex(tools['cur_tab_index'])

    def restore_annotations(self, app, annotations):
        """Restore the annotations"""
        for ann in annotations.values():
            ann_text = ann["ann_text"]
            ann_x = ann["ann_x"]
            ann_y = ann["ann_y"]
            ann_opts = ann["ann_opts"]
            app.add_annotation(text=ann_text, x=ann_x, y=ann_y, annotation_opts=ann_opts)

    def open_project(self, project_path):
        """Open file and load project"""
        import json, zipfile, tempfile
        if not os.path.isfile(project_path):
            return
        self.load_path = project_path
        try:
            with tempfile.TemporaryDirectory() as tmpdirname:
                with zipfile.ZipFile(project_path) as z:
                    z.extract(self.REPTATE_PROJ_JSON, tmpdirname)
                    data = json.load(open(os.path.join(tmpdirname, self.REPTATE_PROJ_JSON)), object_pairs_hook=OrderedDict)
        except:
            print("File \"%s\" seems to be corrupted" % project_path)
            return
        try:
            app_indx_now = current_app_indx = data['current_app_indx']
            apps_dic = data['apps']
        except KeyError:
            print("Could not find data in \"%s\"" % project_path)
            return
        calc_mode_tmp = CmdBase.calcmode
        CmdBase.calcmode = CalcMode.singlethread
        napps = int(data['napp_saved'])
        nth_saved = int(data['nth_saved'])
        nfile_saved = int(data['nfile_saved'])
        ntool_saved = int(data['ntool_saved'])
        if napps > 1:
            txtapp = 'Applications'
        else:
            txtapp = 'Application'
        if nth_saved > 1:
            txtth = 'theories'
        else:
            txtth = 'theory'
        if nfile_saved > 1:
            txtfiles = 'files'
        else:
            txtfiles = 'file'
        if ntool_saved > 1:
            txttool = 'tools'
        else:
            txttool = 'tool'
        ans = QMessageBox.question(self, 'Load Project',
            'Will load %d %s, %d %s, %d %s, and %d %s.\nDo you want to continue?' % (napps,
            txtapp, nth_saved, txtth, nfile_saved, txtfiles, ntool_saved, txttool),
            QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
        if ans != QMessageBox.Yes:
            return
        for app_dic in apps_dic.values():
            app_tabname = app_dic['app_tabname']
            app_indx = app_dic['app_indx']
            appname = app_dic['appname']
            current_view_names = app_dic['current_view_names']
            current_ds_indx = app_dic['current_ds_indx']
            datasets = app_dic['datasets']
            tools = app_dic['tools']
            show_inspector = bool(app_dic['show_inspector'])
            annotations = app_dic['annotations']

            new_app_tab, ind = self.restore_app(appname, app_tabname)

            try:
                new_app_tab.ax_opts = app_dic['axis_options']
            except:
                #backward compatibility
                pass

            try:
                new_app_tab.legend_opts = app_dic['legend_opts']
            except:
                #backward compatibility
                pass

            if app_indx == current_app_indx:
                # to be safe in case some apps are open before restore
                app_indx_now = ind

            for ds_dic in datasets.values():
                ds_tabname = ds_dic['ds_tabname']
                files = ds_dic['files']
                current_th_indx = ds_dic['current_th_indx']
                theories = ds_dic['theories']
                ds_markers = ds_dic['ds_markers']

                new_ds_tab = new_app_tab.createNew_Empty_Dataset(tabname=ds_tabname)
                self.restore_files(new_ds_tab, files)
                self.restore_theories(new_ds_tab, theories)
                new_ds_tab.TheorytabWidget.setCurrentIndex(current_th_indx)
                self.restore_marker_settings(new_ds_tab, ds_markers)
            self.restore_tools(new_app_tab, tools)
            new_app_tab.DataInspectordockWidget.setVisible(show_inspector)

            # restore annotations
            self.restore_annotations(new_app_tab, annotations)

            # set app views
            new_app_tab.multiviews = [new_app_tab.views[v] for v in current_view_names]
            new_app_tab.viewComboBox.setCurrentText(current_view_names[0])
            new_app_tab.change_view()
            #set current ds_tab index
            new_app_tab.DataSettabWidget.setCurrentIndex(current_ds_indx)
            # new_app_tab.update_all_ds_plots() # not needed ?

            QApplication.processEvents()

        self.ApplicationtabWidget.setCurrentIndex(app_indx_now)
        CmdBase.calcmode = calc_mode_tmp
#################
