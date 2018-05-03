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
# Copyright (2017): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
import logging
import os
from os.path import dirname, join, abspath
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QInputDialog, QLineEdit, QMenu, QAction, QToolButton, QMessageBox, QFileDialog

from CmdBase import CmdBase, CmdMode, CalcMode
from QApplicationWindow import QApplicationWindow
from ApplicationManager import ApplicationManager
from File import File
from QAboutReptate import AboutWindow
from collections import OrderedDict
import numpy as np

PATH = dirname(abspath(__file__))
Ui_MainWindow, QMainWindow = loadUiType(join(PATH, 'ReptateMainWindow.ui'))


class QApplicationManager(ApplicationManager, QMainWindow, Ui_MainWindow):
    """Main Reptate window and application manager
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/en/latest/index.html'
    reptatelogger = logging.getLogger('ReptateLogger')
    reptatelogger.setLevel(logging.DEBUG)

    def __init__(self, parent=None):
        """
        **Constructor**

        Keyword Arguments:
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__()
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        CmdBase.mode = CmdMode.GUI  #set GUI mode
        self.setupUi(self)

        if CmdBase.calcmode == CalcMode.singlethread:
            self.setWindowTitle('RepTate v' + self.version + ' ' + self.date +
                                ' - SINGLE THREAD!!')
        else:
            self.setWindowTitle('RepTate v' + self.version + ' ' + self.date)

        #help button
        icon = QIcon(':/Icon8/Images/new_icons/icons8-user-manual.png')
        self.show_reptate_help = QAction(icon, 'RepTate Manual', self)
        self.show_app_help = QAction(icon, 'Application Manual', self)
        self.show_th_help = QAction(icon, 'Theory Manual', self)
        tbut = QToolButton()
        tbut.setPopupMode(QToolButton.MenuButtonPopup)
        tbut.setDefaultAction(self.show_reptate_help)
        menu = QMenu()
        menu.addAction(self.show_app_help)
        menu.addAction(self.show_th_help)
        tbut.setMenu(menu)
        self.toolBarHelp.insertWidget(self.actionAbout_Qt, tbut)
        self.toolBarHelp.insertSeparator(self.actionAbout_Qt)
        #self.toolBar.insertSeparator(self.actionQuit)
        self.toolBarApps.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolBarHelp.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolBarTools.setContextMenuPolicy(Qt.PreventContextMenu)
        
        # # ApplicationXY button
        # #choose the button icon
        # icon = QIcon(':/Icon8/Images/new_icons/icons8-scatter-plot.png')
        # tool_tip = 'XY'  # text that appear on hover
        # self.actionXY = QAction(icon, tool_tip, self)
        # #insert the new button before the "MWD" button
        # self.toolBar.insertAction(self.actionMWD, self.actionXY)
        # #connect button
        # self.actionXY.triggered.connect(self.new_xy_window)

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
        self.actionMWD.triggered.connect(lambda: self.handle_new_app('MWD'))
        self.actionTTS.triggered.connect(lambda: self.handle_new_app('TTS'))
        self.actionLVE.triggered.connect(lambda: self.handle_new_app('LVE'))
        self.actionNLVE.triggered.connect(lambda: self.handle_new_app('NLVE'))
        self.actionGt.triggered.connect(lambda: self.handle_new_app('Gt'))
        self.actionCreep.triggered.connect(lambda: self.handle_new_app('Creep'))
        self.actionSANS.triggered.connect(lambda: self.handle_new_app('SANS'))
        self.actionReact.triggered.connect(lambda: self.handle_new_app('React'))
        self.actionDielectric.triggered.connect(lambda: self.handle_new_app('Dielectric'))
        self.actionDynamicStructureFactor.triggered.connect(lambda: self.handle_app_coming_soon('DynamicStructureFactor'))

        self.ApplicationtabWidget.tabCloseRequested.connect(self.close_app_tab)
        self.ApplicationtabWidget.currentChanged.connect(self.tab_changed)
        #self.Projecttree.itemSelectionChanged.connect(self.treeChanged)

        self.actionAbout_Qt.triggered.connect(QApplication.aboutQt)
        self.actionAbout.triggered.connect(self.show_about)

        connection_id = self.ApplicationtabWidget.tabBarDoubleClicked.connect(
            self.handle_doubleClickTab)
        # help buttons
        self.show_reptate_help.triggered.connect(self.handle_show_reptate_help)
        self.show_app_help.triggered.connect(self.handle_show_app_help)
        self.show_th_help.triggered.connect(self.handle_show_th_help)

        self.add_save_load_buttons()
        self.REPTATE_PROJ_JSON = 'reptate_project.json' # json filename inside zip

        # CONSOLE WINDOW (need to integrate it with cmd commands)
        #self.text_edit = Console(self)
        #this is how you pass in locals to the interpreter
        #self.text_edit.initInterpreter(locals())
        #self.verticalLayout.addWidget(self.text_edit)


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
            help_file = 'http://reptate.readthedocs.io/en/latest/manual/Applications/applications.html'
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
            help_file = 'http://reptate.readthedocs.io/en/latest/manual/All_Theories/All_Theories.html'
        QDesktopServices.openUrl(QUrl.fromUserInput((help_file)))

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
        dlg = AboutWindow(self, self.version + ' ' + self.date)
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
        app_name = self.ApplicationtabWidget.widget(index).name
        self.ApplicationtabWidget.removeTab(index)
        self.delete(app_name)

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
        QMessageBox.warning(self, "new %s application"% appname, "Coming soon..." )



############################
#SAVE/LOAD REPTATE SESSION
############################

    def add_save_load_buttons(self):
        """Add "save" and "open" project buttons"""
        icon = QIcon(':/Icons/Images/new_icons/icons8-save.png')
        self.save_button = QAction(icon, 'Save Project', self)
        self.save_button.triggered.connect(self.launch_save_dialog)

        icon = QIcon(':/Icons/Images/new_icons/icons8-open.png')
        self.open_button = QAction(icon, 'Open Project', self)
        self.open_button.triggered.connect(self.launch_open_dialog)
        
        self.toolBarTools.addAction(self.save_button)
        self.toolBarTools.addAction(self.open_button)


    def closeEvent(self, event):
        """Ask if we want to save project before closing RepTate"""
        btns = (QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        msg = 'Do you want to save your project before exiting RepTate?'
        title = 'Quit'
        ans = QMessageBox.question(self, title , msg, buttons=btns)
        if ans == QMessageBox.No:
            event.accept()
        elif ans == QMessageBox.Yes:
            success = self.launch_save_dialog()
            if not success:
                event.ignore()
        elif ans == QMessageBox.Cancel:
            event.ignore()

    def launch_open_dialog(self):
        """Get filename of RepTate project to open"""
        fpath, _ = QFileDialog.getOpenFileName(self,
            "Open RepTate Project", "data/", "RepTate Project (*.rept)")
        if fpath == '':
            return
        self.open_project(fpath)

    def launch_save_dialog(self):
        """Get filename of RepTate project to save"""
        fpath, _ = QFileDialog.getSaveFileName(self,
            "Save RepTate Project", "data/", "RepTate Project (*.rept)")
        if fpath == '':
            return False
        self.save_reptate(fpath)
        return True

    def save_reptate(self, fpath):
        """Save RepTate project to 'fpath'"""
        apps_dic = OrderedDict()
        napps = self.ApplicationtabWidget.count()
        for i in range(napps):
            app = self.ApplicationtabWidget.widget(i)
            datasets_dic = {}
            ndatasets = app.DataSettabWidget.count()
            for j in range(ndatasets):
                ds = app.DataSettabWidget.widget(j)
                files_dic = {}
                for f in ds.files:
                    param_dic = dict([ (pname, f.file_parameters[pname]) for pname in f.file_parameters])
                    file_dic = dict(
                        [
                            ('fname', os.path.basename(f.file_full_path)),
                            ('is_active', f.active),
                            ('fparam', param_dic),
                            ('ftable', f.data_table.data.tolist())
                        ]
                    )
                    files_dic[f.file_name_short] = file_dic

                theories_dic = {}
                ntheories = ds.TheorytabWidget.count()
                for k in range(ntheories):
                    th = ds.TheorytabWidget.widget(k)
                    param_dic = OrderedDict([(pname, th.parameters[pname].value) for pname in th.parameters])
                    th_table_dic = dict( 
                        [ (f.file_name_short, th.tables[f.file_name_short].data.tolist()) for f in ds.files]
                    )
                    
                    th_dic = dict(
                        [
                            ('th_tabname', ds.TheorytabWidget.tabText(k)),
                            ('thname', th.thname),
                            ('th_param', param_dic),
                            ('th_textbox', str(th.thTextBox.toPlainText())),
                            ('th_tables', th_table_dic)
                        ]
                    )
                    theories_dic[th.name] = th_dic
                
                ds_dict = dict(
                    [
                        ('ds_tabname', app.DataSettabWidget.tabText(j)),
                        ('files', files_dic),
                        ('current_th_indx', ds.TheorytabWidget.currentIndex()),
                        ('theories', theories_dic)
                    ]
                )
                datasets_dic[ds.name] = ds_dict


            app_dic = OrderedDict(
                [
                    ('app_tabname', self.ApplicationtabWidget.tabText(i)),
                    ('app_indx', i),
                    ('appname', app.appname), 
                    ('current_view_names', [v.name for v in app.multiviews]), 
                    ('current_ds_indx', app.DataSettabWidget.currentIndex()),
                    ('datasets', datasets_dic)
                ]
            )

            apps_dic[app.name] = app_dic

        current_app_indx = self.ApplicationtabWidget.currentIndex()
        out = OrderedDict([('current_app_indx', current_app_indx), ('apps', apps_dic)])

        # zip output file
        import json, zipfile, tempfile
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmp = os.path.join(tmpdirname, 'tmp')
            json.dump(out, open(tmp, 'w'), indent=4)
            with zipfile.ZipFile(fpath, 'w', compression=zipfile.ZIP_DEFLATED) as z:
                z.write(tmp, self.REPTATE_PROJ_JSON)


    # load RepTate session
############################

    def restore_app(self, app_name, app_tabname):
        """Open new application"""
        newapp = self.new(app_name)
        icon = QIcon(':/Icons/Images/new_icons/%s.png' % app_name)
        ind = self.ApplicationtabWidget.addTab(newapp, icon, app_tabname)
        self.ApplicationtabWidget.setCurrentIndex(ind)
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

            new_th = ds.new_theory(thname, th_tabname, calculate=False)
            for pname in th_param:
                new_th.set_param_value(pname, th_param[pname])
            for fname in th_tables:
                tt = new_th.tables[fname]
                tt.data = np.asarray(th_tables[fname])
                tt.num_rows, tt.num_columns = tt.data.shape
            new_th.update_parameter_table()
            new_th.thTextBox.insertPlainText(th_textbox)

    def open_project(self, project_path):
        """Open file and load project"""
        import json, zipfile, tempfile
        if not os.path.isfile(project_path):
            return
        try:
            with tempfile.TemporaryDirectory() as tmpdirname:
                with zipfile.ZipFile(project_path) as z:
                    z.extract(self.REPTATE_PROJ_JSON, tmpdirname)
                    data = json.load(open(os.path.join(tmpdirname, self.REPTATE_PROJ_JSON)))
        except:
            print("File \"%s\" seems to be corrupted" % project_path)
            return
        try:
            app_indx_now = current_app_indx = data['current_app_indx']
            apps_dic = data['apps']
        except KeyError:
            print("Could not find data in \"%s\"" % project_path)
            return

        for app_dic in apps_dic.values():
            app_tabname = app_dic['app_tabname']
            app_indx = app_dic['app_indx'] 
            appname = app_dic['appname']
            current_view_names = app_dic['current_view_names']
            current_ds_indx = app_dic['current_ds_indx']
            datasets = app_dic['datasets']

            new_app_tab, ind = self.restore_app(appname, app_tabname)
            if app_indx == current_app_indx:
                # to be safe in case some apps are open before restore
                app_indx_now = ind

            for ds_dic in datasets.values():
                ds_tabname = ds_dic['ds_tabname']
                files = ds_dic['files']
                current_th_indx = ds_dic['current_th_indx']
                theories = ds_dic['theories']

                new_ds_tab = new_app_tab.createNew_Empty_Dataset(tabname=ds_tabname)
                self.restore_files(new_ds_tab, files)
                self.restore_theories(new_ds_tab, theories)
                new_ds_tab.TheorytabWidget.setCurrentIndex(current_th_indx)

            #set app views
            new_app_tab.multiviews = [new_app_tab.views[v] for v in current_view_names]
            new_app_tab.viewComboBox.setCurrentText(current_view_names[0])
            new_app_tab.change_view()
            #set current ds_tab index
            new_app_tab.DataSettabWidget.setCurrentIndex(current_ds_indx)
            # new_app_tab.update_all_ds_plots() # not needed ?
    
        self.ApplicationtabWidget.setCurrentIndex(app_indx_now)

#################