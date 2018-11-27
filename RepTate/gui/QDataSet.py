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
"""Module QDataSet

Module that defines the GUI counterpart of Dataset.

"""
from os.path import dirname, join, abspath
import os
from PyQt5.QtGui import QPixmap, QColor, QPainter, QIcon, QIntValidator, QDoubleValidator, QStandardItem
from PyQt5.uic import loadUiType
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QTabWidget, QHeaderView, QToolBar, QComboBox, QMessageBox, QInputDialog, QFrame, QToolButton, QMenu, QAction, QAbstractItemView, QTableWidgetItem, QDialog, QVBoxLayout, QTableWidget, QDialogButtonBox, QGroupBox, QFormLayout, QLineEdit, QLabel, QFileDialog, QCheckBox
from DataSet import DataSet
from DataTable import DataTable
from QTheory import QTheory
from DataSetWidget import DataSetWidget
import threading
import matplotlib.patheffects as pe

PATH = dirname(abspath(__file__))
Ui_DataSet, QWidget = loadUiType(join(PATH, 'DataSet.ui'))


class EditFileParametersDialog(QDialog):
    """Create the form that is used to modify the file parameters"""

    def __init__(self, parent, file):
        super().__init__(parent)
        self.createFormGroupBox(file)
        self.createFormGroupBoxTheory(file)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok
                                     | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        tab_widget = QTabWidget()
        tab_widget.addTab(self.formGroupBox, 'File Parameters')
        tab_widget.addTab(self.formGroupBoxTheory, 'Theory Parameters')
        mainLayout.addWidget(tab_widget)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("Edit")

    def createFormGroupBox(self, file):
        """Create a form to set the new values of the file parameters"""
        self.formGroupBox = QGroupBox(
            "Parameters of \"%s\"" % file.file_name_short)
        layout = QFormLayout()

        parameters = file.file_parameters
        self.param_dict = {}
        self.p_new = []
        for i, pname in enumerate(parameters):  #loop over the Parameters
            self.p_new.append(QLineEdit())
            if isinstance(parameters[pname], str):  #the parameter is a string
                self.p_new[i].setText("%s" % parameters[pname])
            else:  #parameter is a number:
                self.p_new[i].setValidator(
                    QDoubleValidator())  #prevent letters
                self.p_new[i].setText("%.4g" % parameters[pname])
            layout.addRow("%s:" % pname, self.p_new[i])
            self.param_dict[pname] = self.p_new[i]
        self.formGroupBox.setLayout(layout)

    def createFormGroupBoxTheory(self, file):
        self.formGroupBoxTheory = QGroupBox(
            "Extend theory x-range of \"%s\"" % file.file_name_short)
        layout = QFormLayout()
        self.with_extra_x = QCheckBox()
        self.with_extra_x.setChecked(file.with_extra_x)
        layout.addRow('Extra theory xrange?', self.with_extra_x)
        self.with_extra_x.toggled.connect(self.activate_th_widgets)
        # theory xmin/max
        self.th_xmin = QLineEdit()
        self.th_xmax = QLineEdit()
        self.th_linear = QCheckBox()
        self.th_xmin.setText('%s' % file.theory_xmin)
        self.th_xmax.setText('%s' % file.theory_xmax)
        layout.addRow('xmin theory', self.th_xmin)
        layout.addRow('xmax theory', self.th_xmax)
        # Npoints
        self.th_num_pts = QLineEdit()
        intvalidator = QIntValidator()
        intvalidator.setBottom(2)
        self.th_num_pts.setValidator(QIntValidator())
        self.th_num_pts.setText('%s' % file.th_num_pts)
        layout.addRow('Num. of extra point', self.th_num_pts)
        # logspace
        self.th_logspace = QCheckBox()
        self.th_logspace.setChecked(file.theory_logspace)
        layout.addRow('logspace', self.th_logspace)
        # set layout
        self.formGroupBoxTheory.setLayout(layout)
        self.activate_th_widgets()
    
    def activate_th_widgets(self):
        checked = self.with_extra_x.isChecked()
        self.th_xmin.setDisabled(not checked)
        self.th_xmax.setDisabled(not checked)
        self.th_num_pts.setDisabled(not checked)
        self.th_logspace.setDisabled(not checked)


class QDataSet(DataSet, QWidget, Ui_DataSet):
    """[summary]
    
    [description]
    """

    def __init__(self, name="QDataSet", parent=None):
        """
        **Constructor**
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"QDataSet"})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name=name, parent=parent)
        QWidget.__init__(self)
        Ui_DataSet.__init__(self)

        self.setupUi(self)

        self.DataSettreeWidget = DataSetWidget(self)
        self.splitter.insertWidget(0, self.DataSettreeWidget)

        self.DataSettreeWidget.setIndentation(0)
        self.DataSettreeWidget.setHeaderItem(QTreeWidgetItem([""]))
        self.DataSettreeWidget.setSelectionMode(
            1)  #QAbstractItemView::SingleSelection
        hd = self.DataSettreeWidget.header()
        hd.setSectionsMovable(False)
        w = self.DataSettreeWidget.width()
        w /= hd.count()
        for i in range(hd.count()):
            hd.resizeSection(0, w)

        # Theory Toolbar
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        tb.addAction(self.actionNew_Theory)
        self.cbtheory = QComboBox()
        model = self.cbtheory.model()
        self.cbtheory.setToolTip("Choose a Theory")

        item = QStandardItem('Select:')
        item.setForeground(QColor('grey'))
        model.appendRow(item)
        i = 1
        for th_name in self.parent_application.theories:
            if th_name not in self.parent_application.common_theories:
                item = QStandardItem(th_name)
                item.setToolTip(self.parent_application.theories[th_name].description)
                model.appendRow(item)
        flag_first = True
        for th_name in self.parent_application.theories:
            if th_name in self.parent_application.common_theories:
                if flag_first:
                    # add separator if al least one common theories is added
                    self.cbtheory.insertSeparator(self.cbtheory.count())
                    flag_first = False
                item = QStandardItem(th_name)
                item.setToolTip(self.parent_application.theories[th_name].description)
                model.appendRow(item)
        self.cbtheory.setCurrentIndex(0)

        ###

        self.cbtheory.setMaximumWidth(115)
        self.cbtheory.setMinimumWidth(50)
        tb.addWidget(self.cbtheory)
        tb.addAction(self.actionCalculate_Theory)
        tb.addAction(self.actionMinimize_Error)
        #Buttons not wired yet
        # tb.addAction(self.actionTheory_Options)
        # self.actionTheory_Options.setDisabled(True)
        tbut = QToolButton()
        tbut.setPopupMode(QToolButton.MenuButtonPopup)
        tbut.setDefaultAction(self.actionShow_Limits)
        menu = QMenu()
        menu.addAction(self.actionVertical_Limits)
        menu.addAction(self.actionHorizontal_Limits)
        tbut.setMenu(menu)
        tb.addWidget(tbut)
        tbut2 = QToolButton()
        tbut2.setPopupMode(QToolButton.MenuButtonPopup)
        self.action_save_theory_data = QAction(QIcon(':/Icon8/Images/new_icons/icons8-save_TH.png'), "Save Theory Data", self)
        tbut2.setDefaultAction(self.action_save_theory_data)
        menu2 = QMenu()
        menu2.addAction(self.actionCopy_Parameters)
        menu2.addAction(self.actionPaste_Parameters)
        tbut2.setMenu(menu2)
        tb.addWidget(tbut2)
        
        self.TheoryLayout.insertWidget(0, tb)
        self.splitter.setSizes((1000, 3000))

        #desactive buttons when no theory tab
        self.theory_actions_disabled(True)

        connection_id = self.actionNew_Theory.triggered.connect(
            self.handle_actionNew_Theory)
        connection_id = self.DataSettreeWidget.itemChanged.connect(
            self.handle_itemChanged)
        #connection_id = self.DataSettreeWidget.itemClicked.connect(self.handle_itemClicked)
        connection_id = self.DataSettreeWidget.itemDoubleClicked.connect(
            self.handle_itemDoubleClicked)
        connection_id = self.DataSettreeWidget.header(
        ).sortIndicatorChanged.connect(self.handle_sortIndicatorChanged)
        connection_id = self.DataSettreeWidget.itemSelectionChanged.connect(
            self.handle_itemSelectionChanged)
        # connection_id = self.DataSettreeWidget.currentItemChanged.connect(self.handle_currentItemChanged)

        connection_id = self.TheorytabWidget.tabCloseRequested.connect(
            self.handle_thTabCloseRequested)
        connection_id = self.TheorytabWidget.tabBarDoubleClicked.connect(
            self.handle_thTabBarDoubleClicked)
        connection_id = self.TheorytabWidget.currentChanged.connect(
            self.handle_thCurrentChanged)
        connection_id = self.actionMinimize_Error.triggered.connect(
            self.handle_actionMinimize_Error)
        connection_id = self.actionCalculate_Theory.triggered.connect(
            self.handle_actionCalculate_Theory)
        connection_id = self.action_save_theory_data.triggered.connect(
            self.handle_action_save_theory_data)
        connection_id = self.actionCopy_Parameters.triggered.connect(
            self.copy_parameters)
        connection_id = self.actionPaste_Parameters.triggered.connect(
            self.paste_parameters)
            

        connection_id = self.actionVertical_Limits.triggered.connect(
            self.toggle_vertical_limits)
        connection_id = self.actionHorizontal_Limits.triggered.connect(
            self.toggle_horizontal_limits)

    def copy_parameters(self):
        """Copy the parameters of the currently active theory to the clipboard"""
        th = self.current_theory
        if th:
            self.theories[th].copy_parameters()

    def paste_parameters(self):
        """Paste the parameters from the clipboard to the currently active theory"""
        th = self.current_theory
        if th:
            self.theories[th].paste_parameters()
            
    def handle_action_save_theory_data(self):
        """Save theory data of current theory"""
        th = self.current_theory
        if th:
            # file browser window
            dir_start = "data/"
            dilogue_name = "Select Folder"
            folder = QFileDialog.getExistingDirectory(self, dilogue_name, dir_start)
            if os.path.isdir(folder):
                dialog = QInputDialog(self)
                dialog.setWindowTitle('Add label to filename(s)?')
                dialog.setLabelText('Add the following text to each saved theory filename(s):')
                dialog.setTextValue('')
                dialog.setCancelButtonText('None')
                if dialog.exec():
                    txt = dialog.textValue()
                    if txt != '':
                        txt = '_' + txt
                else:
                    txt = ''
                self.theories[th].do_save(folder, txt)

    def set_table_icons(self, table_icon_list):
        """The list 'table_icon_list' contains tuples (file_name_short, marker_name, face, color)
        
        [description]
        
        Arguments:
            - table_icon_list {[type]} -- [description]
        """
        self.DataSettreeWidget.blockSignals(
            True
        )  #avoid triggering 'itemChanged' signal that causes a call to do_plot()

        for fname, marker_name, face, color in table_icon_list:
            item = self.DataSettreeWidget.findItems(
                fname, Qt.MatchCaseSensitive,
                column=0)  #returns list of items matching file name
            if item:
                #paint icon
                folder = ':/Markers/Images/Matplotlib_markers/'
                if face == 'none':  #empty symbol
                    marker_path = folder + 'marker_%s' % marker_name
                else:  #filled symbol
                    marker_path = folder + 'marker_filled_%s' % marker_name
                qp = QPixmap(marker_path)
                mask = qp.createMaskFromColor(QColor(0, 0, 0), Qt.MaskOutColor)
                qpainter = QPainter()
                qpainter.begin(qp)
                qpainter.setPen(
                    QColor(
                        int(255 * color[0]), int(255 * color[1]),
                        int(255 * color[2]), 255))
                qpainter.drawPixmap(qp.rect(), mask, qp.rect())
                qpainter.end()
                item[0].setIcon(0, QIcon(qp))

        self.DataSettreeWidget.blockSignals(False)

    def theory_actions_disabled(self, state):
        """Disable theory buttons if no theory tab is open
        
        [description]
        
        Arguments:
            - state {[type]} -- [description]
        """
        self.actionCalculate_Theory.setDisabled(state)
        self.actionMinimize_Error.setDisabled(state)
        # self.actionTheory_Options.setDisabled(state)
        self.actionShow_Limits.setDisabled(state)
        self.actionVertical_Limits.setDisabled(state)
        self.actionHorizontal_Limits.setDisabled(state)
        self.action_save_theory_data.setDisabled(state)

    def set_limit_icon(self):
        """[summary]
        
        [description]
        """
        if self.current_theory:
            th = self.theories[self.current_theory]
        vlim = th.is_xrange_visible
        hlim = th.is_yrange_visible
        if hlim and vlim:
            img = "Line Chart Both Limits"
        elif vlim:
            img = "Line Chart Vertical Limits"
        elif hlim:
            img = "Line Chart Horizontal Limits"
        else:
            img = "Line Chart"
        self.actionShow_Limits.setIcon(QIcon(':/Images/Images/%s.png' % img))

    def set_no_limits(self, th_name):
        """Turn the x and yrange selectors off
        
        [description]
        
        Arguments:
            - th_name {[type]} -- [description]
        """
        if th_name in self.theories:
            self.theories[self.current_theory].set_xy_limits_visible(
                False, False)  #hide xrange and yrange

    def toggle_vertical_limits(self, checked):
        """Show/Hide the xrange selector for fit
        
        [description]
        """
        if self.current_theory:
            th = self.theories[self.current_theory]
            th.do_xrange("", checked)
            th.is_xrange_visible = checked
            self.set_limit_icon()

    def toggle_horizontal_limits(self, checked):
        """Show/Hide the yrange selector for fit
        
        [description]
        """
        if self.current_theory:
            th = self.theories[self.current_theory]
            th.do_yrange("", checked)
            th.is_yrange_visible = checked
            self.set_limit_icon()
    
    def end_of_computation(self, th_name):
        """Action when theory has finished computations"""
        try:
            th = self.theories[th_name]
            th.stop_theory_flag = False
        except KeyError:
            pass
        if self.current_theory == th_name:
            self.icon_calculate_is_stop(False)
            self.icon_fit_is_stop(False)

    def handle_actionCalculate_Theory(self):
        if self.current_theory and self.files:
            th = self.theories[self.current_theory]
            if th.thread_calc_busy: # request stop if in do_calculate
                th.request_stop_computations()
                return
            elif th.is_fitting or th.thread_fit_busy:  #do nothing if already busy in do_fit
                th.Qprint("Busy minimising theory...")
                return
            if th.single_file and (
                    len(self.files) - len(self.inactive_files)) > 1:
                header = "Calculate"
                message = "<p>Too many active files: \"%s\" uses only one data file.</p>\
                    <p>The theory will be applied to the highlighted file if any or to the first active file.</p>" % th.thname
                QMessageBox.warning(self, header, message)
            self.icon_calculate_is_stop(True)
            th.handle_actionCalculate_Theory()

    def handle_actionMinimize_Error(self):
        """Minimize the error
        
        [description]
        """
        if self.current_theory and self.files:
            th = self.theories[self.current_theory]
            if th.is_fitting or th.thread_fit_busy: # request stop if in do_fit
                th.request_stop_computations()
                return
            elif th.calculate_is_busy or th.thread_calc_busy:  #do nothing if already busy in do_calculate
                th.Qprint("Busy calculating theory...")
                return
            if th.single_file and (
                    len(self.files) - len(self.inactive_files)) > 1:
                header = "Minimization"
                message = "<p>Too many active files: \"%s\" uses only one data file.</p>\
                    <p>The theory will be applied to the highlighted file if any or to the first active file.</p>" % th.thname
                QMessageBox.warning(self, header, message)
            self.icon_fit_is_stop(True)
            th.handle_actionMinimize_Error()

    def icon_calculate_is_stop(self, ans):
        """Change the "calculate" button to "stop" button"""
        if ans:
            self.actionCalculate_Theory.setIcon(QIcon(":/Icon8/Images/new_icons/icons8-stop-sign.png"))
            self.actionCalculate_Theory.setToolTip("Stop current calculations")
        else:
            self.actionCalculate_Theory.setIcon(QIcon(":/Icon8/Images/new_icons/icons8-abacus.png"))
            self.actionCalculate_Theory.setToolTip("Calculate Theory (ALT + C)")

    def icon_fit_is_stop(self, ans):
        """Change the "fit" button to "stop" button"""
        if ans:
            self.actionMinimize_Error.setIcon(QIcon(":/Icon8/Images/new_icons/icons8-stop-sign.png"))
            self.actionCalculate_Theory.setToolTip("Stop current calculations")
        else:
            self.actionMinimize_Error.setIcon(QIcon(":/Icon8/Images/new_icons/icons8-minimum-value.png"))
            self.actionCalculate_Theory.setToolTip("Minimize error (ALT + M)")

    def handle_thCurrentChanged(self, index):
        """Change figure when the active theory tab is changed
        
        [description]
        
        Arguments:
            - index {[type]} -- [description]
        """
        self.icon_calculate_is_stop(False)
        self.icon_fit_is_stop(False)
        th = self.TheorytabWidget.widget(index)
        if th:
            self.current_theory = th.name
            ntab = self.TheorytabWidget.count()
            #hide all theory curves
            for i in range(ntab):
                if i != index:
                    th_to_hide = self.TheorytabWidget.widget(i)
                    th_to_hide.do_hide()
            th.do_show()  #must be called last, after hiding other theories

            if th.thread_calc_busy or th.thread_fit_busy:
                self.icon_calculate_is_stop(th.thread_calc_busy)
                self.icon_fit_is_stop(th.thread_fit_busy)
                return
        else:
            self.current_theory = None
            self.theory_actions_disabled(True)
        self.parent_application.update_plot()
        self.parent_application.update_Qplot()

    def handle_thTabBarDoubleClicked(self, index):
        """Edit Theory name
        
        Edit the theory tab name, leave 'theories' dictionary keys unchanged.
        Two tabs can share the same name

        Arguments:
            - index {[type]} -- [description]
        """
        old_name = self.TheorytabWidget.tabText(index)
        dlg = QInputDialog(self)
        dlg.setWindowTitle("Change Theory Name")
        dlg.setLabelText("New Theory Name:")
        dlg.setTextValue(old_name)
        dlg.resize(400, 100)
        success = dlg.exec()
        new_tab_name = dlg.textValue()
        if (success and new_tab_name != ""):
            self.TheorytabWidget.setTabText(index, new_tab_name)
            # self.theories[old_name].name = new_tab_name
            # self.theories[new_tab_name] = self.theories.pop(old_name)
            # self.current_theory = new_tab_name

    def handle_thTabCloseRequested(self, index):
        """Delete a theory tab from the current dataset
        
        [description]
        
        Arguments:
            - index {[type]} -- [description]
        """
        th_name = self.TheorytabWidget.widget(index).name
        th = self.theories[th_name]
        th.Qprint("Close theory tab requested")
        th.request_stop_computations()
        self.set_no_limits(th_name)
        self.do_theory_delete(th_name)  #call DataSet.do_theory_delete
        self.TheorytabWidget.removeTab(index)

    def handle_itemSelectionChanged(self):
        """Define actions for when a file table is selected
        
        [description]
        """
        selection = self.DataSettreeWidget.selectedItems()
        if selection == []:
            self.selected_file = None
            self.highlight_series()
            return
        for f in self.files:
            if f.file_name_short == selection[0].text(0):
                self.parent_application.disconnect_curve_drag()
                self.selected_file = f
                self.highlight_series()
                self.populate_inspector()
                self.parent_application.handle_actionShiftTriggered()


    def highlight_series(self):
        """Highligh the data series of the selected file
        
        [description]
        """
        self.do_plot()  #remove current series highlight
        file = self.selected_file
        thname = self.current_theory
        if thname:
            th = self.theories[thname]
        else:
            th = None
        if file is not None:
            dt = file.data_table
            if th:
                tt = th.tables[file.file_name_short]
            for i in range(dt.MAX_NUM_SERIES):
                for nx in range(self.nplots):
                    view = self.parent_application.multiviews[nx]
                    if (i < view.n and file.active):
                        dt.series[nx][i].set_marker('.')
                        # dt.series[nx][i].set_linestyle(":")
                        dt.series[nx][i].set_markerfacecolor(dt.series[nx][i].get_markeredgecolor())
                        dt.series[nx][i].set_markeredgecolor('peachpuff')
                        dt.series[nx][i].set_markersize(self.marker_size+3)
                        dt.series[nx][i].set_markeredgewidth(2)
                        dt.series[nx][i].set_zorder(
                            self.parent_application.zorder)  #put series on top
                        if th:
                            if th.active:
                                tt.series[nx][i].set_color('k')
                                tt.series[nx][i].set_path_effects([pe.Stroke(linewidth=self.th_line_width+3, foreground='chartreuse'), pe.Normal()])
                                tt.series[nx][i].set_zorder(
                                    self.parent_application.zorder)

            self.parent_application.zorder += 1
        self.parent_application.update_plot()

    def populate_inspector(self):
        """[summary]
        
        [description]
        """
        file = self.selected_file
        if not file:
            self.parent_application.inspector_table.setRowCount(0)
            self.parent_application.DataInspectordockWidget.setWindowTitle(
                "File:")
            return
        if self.parent_application.DataInspectordockWidget.isHidden():
            return
        dt = file.data_table
        nrow = dt.num_rows
        ncol = dt.num_columns
        inspec_tab = self.parent_application.inspector_table
        inspec_tab.setRowCount(nrow)
        inspec_tab.setColumnCount(ncol)
        for i in range(nrow):
            for j in range(ncol):
                x = "%.3e" % dt.data[i, j]
                inspec_tab.setItem(
                    i, j, QTableWidgetItem(x))  # dt.setItem(row, column, item)
        ds_index = self.parent_application.DataSettabWidget.currentIndex()
        self.parent_application.DataInspectordockWidget.setWindowTitle(
            "File: \"%s\" in %s" %
            (file.file_name_short,
             self.parent_application.DataSettabWidget.tabText(ds_index)))
        inspec_tab.resizeColumnsToContents()
        inspec_tab.resizeRowsToContents()
        # Update shift factors
        for i in range(DataTable.MAX_NUM_SERIES):
            self.parent_application.update_shifts(0, 0, i)
             
    def handle_itemChanged(self, item, column):
        """[summary]
        
        [description]
        
        Arguments:
            - item {[type]} -- [description]
            - column {[type]} -- [description]
        """
        if column == 0:
            self.change_file_visibility(
                item.text(0),
                item.checkState(column) == Qt.Checked)

    def handle_sortIndicatorChanged(self, column, order):
        """Sort files according to the selected parameter (column) and replot
        
        [description]
        
        Arguments:
            - column {[type]} -- [description]
            - order {[type]} -- [description]
        """
        # if column == 0: #do not sort file name
        #     return
        if self.DataSettreeWidget.topLevelItemCount() > 0:
            # sort iff there are some files in the dataset
            sort_param = self.DataSettreeWidget.headerItem().text(column)
            rev = True if order == Qt.AscendingOrder else False
            if rev:
                sort_param = sort_param + ",reverse"
            self.do_sort(sort_param)
            self.do_plot()
            self.set_table_icons(self.table_icon_list)

    def Qshow_all(self):
        """Show all the files in this dataset, except those previously hiden
        
        [description]
        """
        self.do_show_all()
        for i in range(self.DataSettreeWidget.topLevelItemCount()):
            file_name = self.DataSettreeWidget.topLevelItem(i).text(0)
            if file_name in self.inactive_files:
                self.DataSettreeWidget.topLevelItem(i).setCheckState(0, 0)
            else:
                self.DataSettreeWidget.topLevelItem(i).setCheckState(0, 2)

    def resizeEvent(self, evt=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - evt {[type]} -- [description] (default: {None})
        """
        hd = self.DataSettreeWidget.header()
        w = self.DataSettreeWidget.width()
        w /= hd.count()
        for i in range(hd.count()):
            hd.resizeSection(i, w)
            #hd.setTextAlignment(i, Qt.AlignHCenter)

    def handle_itemDoubleClicked(self, item, column):
        """Edit item entry upon double click
        
        [description]
        
        Arguments:
            - item {[type]} -- [description]
            - column {[type]} -- [description]
        """
        # if column>0:
        #     param = self.DataSettreeWidget.headerItem().text(column) #retrive parameter name
        #     file_name_short = item.text(0) #retrive file name
        #     header = "Edit Parameter"
        #     message = "Do you want to edit %s of \"%s\"?"%(param, file_name_short)
        #     answer = QMessageBox.question(self, header, message)
        #     if answer == QMessageBox.Yes:
        #         old_value = item.text(column) #old parameter value
        #         message = "New value of %s"%param
        #         new_value, success = QInputDialog.getDouble(self, header, message, float(old_value))
        #         if success:
        #             for file in self.files:
        #                 if file.file_name_short == file_name_short:
        #                     file.file_parameters[param] = new_value #change value in DataSet
        #             self.DataSettreeWidget.blockSignals(True) #avoid triggering 'itemChanged' signal that causes a false checkbox change
        #             item.setText(column, str(new_value)) #change table label
        #             self.DataSettreeWidget.blockSignals(False)
        # else:
        file_name_short = item.text(0)
        for file in self.files:
            if file.file_name_short == file_name_short:
                d = EditFileParametersDialog(self, file)
                if d.exec_():
                    for p in d.param_dict:
                        if isinstance(file.file_parameters[p], str):
                            file.file_parameters[p] = d.param_dict[p].text()
                        else:
                            try:
                                file.file_parameters[p] = float(
                                    d.param_dict[p].text())
                            except Exception as e:
                                print(e)
                        for i in range(self.DataSettreeWidget.columnCount()):
                            if p == self.DataSettreeWidget.headerItem().text(
                                    i):
                                item.setText(i, str(file.file_parameters[p]))
                    # theory xmin/max
                    try:
                        file.theory_xmin = float(d.th_xmin.text())
                    except ValueError:
                        file.theory_xmin = "None"
                    try:
                        file.theory_xmax = float(d.th_xmax.text())
                    except ValueError:
                        file.theory_xmax = "None"
                    # theory logspace and Npoints
                    try:
                        file.th_num_pts = float(d.th_num_pts.text())
                    except ValueError:
                        pass 
                    try:
                        file.th_num_pts = max(int(d.th_num_pts.text()), 2)
                    except ValueError:
                        pass
                    file.theory_logspace = d.th_logspace.isChecked()
                    file.with_extra_x = d.with_extra_x.isChecked()
                    

    def handle_actionNew_Theory(self):
        """Create new theory and do fit
        
        [description]
        """
        self.actionNew_Theory.setDisabled(True)
        if self.cbtheory.currentIndex() == 0:
            # by default, open first theory in the list
            th_name = self.cbtheory.itemText(1) 
        else:
            th_name = self.cbtheory.currentText()
        self.cbtheory.setCurrentIndex(0) # reset the combobox selection
        if th_name != '':
            self.new_theory(th_name)
        self.actionNew_Theory.setDisabled(False)

    def new_theory(self, th_name, th_tab_id="", calculate=True, show=True):
        """[summary]
        
        [description]
        
        Arguments:
            - th_name {[type]} -- [description]
        """
        if not self.files:
            return
        if self.current_theory:
            self.set_no_limits(
                self.current_theory)  #remove the xy-range limits
        self.theory_actions_disabled(False)  #enable theory buttons
        newth = self.do_theory_new(th_name, calculate)

        # add new theory tab
        if th_tab_id == "":
            th_tab_id = newth.name
            th_tab_id = ''.join(
                c for c in th_tab_id
                if c.isupper())  #get the upper case letters of th_name
            th_tab_id = "%s%d" % (th_tab_id, self.num_theories)  #append number

        #hide all theory curves
        ntab = self.TheorytabWidget.count()
        for i in range(ntab):
            th_to_hide = self.TheorytabWidget.widget(i)
            th_to_hide.do_hide()
        #add theory tab
        self.TheorytabWidget.blockSignals(
            True)  #avoid trigger handle_thCurrentChanged()
        index = self.TheorytabWidget.addTab(newth, th_tab_id)
        self.TheorytabWidget.setCurrentIndex(
            index)  #set new theory tab as curent tab
        self.TheorytabWidget.setTabToolTip(index,
                                           th_name)  #set new-tab tool tip
        self.TheorytabWidget.blockSignals(False)
        if show:
            newth.update_parameter_table()
            newth.do_show("")
        return newth
