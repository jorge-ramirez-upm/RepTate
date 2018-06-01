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
from PyQt5.QtGui import QPixmap, QColor, QPainter, QIcon, QIntValidator, QDoubleValidator
from PyQt5.uic import loadUiType
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QTabWidget, QHeaderView, QToolBar, QComboBox, QMessageBox, QInputDialog, QFrame, QToolButton, QMenu, QAction, QAbstractItemView, QTableWidgetItem, QDialog, QVBoxLayout, QTableWidget, QDialogButtonBox, QGroupBox, QFormLayout, QLineEdit, QLabel, QFileDialog
from DataSet import DataSet
from QTheory import QTheory
from DataSetWidget import DataSetWidget
import threading

PATH = dirname(abspath(__file__))
Ui_DataSet, QWidget = loadUiType(join(PATH, 'DataSet.ui'))


class EditFileParametersDialog(QDialog):
    """Create the form that is used to modify the file parameters"""

    def __init__(self, parent, file):
        super().__init__(parent)
        self.createFormGroupBox(file)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok
                                     | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
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
        # layout.addRow(QLabel("Number of bins for Bob:"), self.e1)
        self.formGroupBox.setLayout(layout)


class EditFileParametersDialog_(QDialog):
    def __init__(
            self,
            parent=None,
            file=None,
    ):
        super(EditFileParametersDialog, self).__init__(parent)

        self.setWindowTitle("Parameters - %s" % file.file_name_short)
        layout = QVBoxLayout(self)

        self.parameters = file.file_parameters
        self.table = QTableWidget()
        self.table.setRowCount(len(self.parameters))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Parameter", "Value"])
        k = list(self.parameters.keys())
        k.sort()
        for i, p in enumerate(k):
            self.table.setItem(i, 0, QTableWidgetItem(p))
            item = self.table.item(i, 0)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if isinstance(self.parameters[p], str):
                self.table.setItem(i, 1, QTableWidgetItem(self.parameters[p]))
            else:
                self.table.setItem(i, 1,
                                   QTableWidgetItem(str(self.parameters[p])))

        layout.addWidget(self.table)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


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
        self.cbtheory.setToolTip("Choose a Theory")

        for th_name in self.parent_application.theories:
            if th_name not in self.parent_application.common_theories:
                self.cbtheory.addItem(th_name)
        flag_first = True
        for th_name in self.parent_application.theories:
            if th_name in self.parent_application.common_theories:
                if flag_first:
                    # add separator if common theories are added
                    self.cbtheory.insertSeparator(self.cbtheory.count())
                    flag_first = False
                self.cbtheory.addItem(th_name)
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
                print('saving')
                self.theories[th].do_save(folder)


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

    def toggle_vertical_limits(self, bool):
        """Show/Hide the xrange selector for fit
        
        [description]
        """
        if self.current_theory:
            th = self.theories[self.current_theory]
            th.do_xrange("")
            th.is_xrange_visible = self.actionVertical_Limits.isChecked()
            self.set_limit_icon()

    def toggle_horizontal_limits(self):
        """Show/Hide the yrange selector for fit
        
        [description]
        """
        if self.current_theory:
            th = self.theories[self.current_theory]
            th.do_yrange("")
            th.is_yrange_visible = self.actionHorizontal_Limits.isChecked()
            self.set_limit_icon()

    def handle_actionCalculate_Theory(self):
        if self.current_theory and self.files:
            th = self.theories[self.current_theory]
            if th.calculate_is_busy or th.is_fitting or th.thread_calc_busy or th.thread_fit_busy:  #do nothing if already busy in do_calculate or do_fit
                return
            if th.single_file and (
                    len(self.files) - len(self.inactive_files)) > 1:
                header = "Calculate"
                message = "<p>Too many active files: \"%s\" uses only one data file.</p>\
                    <p>The theory will be applied to the highlighted file if any or to the first active file.</p>" % th.thname
                QMessageBox.warning(self, header, message)
            th.handle_actionCalculate_Theory()

    def handle_actionMinimize_Error(self):
        """Minimize the error
        
        [description]
        """
        if self.current_theory and self.files:
            th = self.theories[self.current_theory]
            if th.calculate_is_busy or th.is_fitting or th.thread_calc_busy or th.thread_fit_busy:  #do nothing if already busy in do_calculate or do_fit
                return
            if th.single_file and (
                    len(self.files) - len(self.inactive_files)) > 1:
                header = "Minimization"
                message = "<p>Too many active files: \"%s\" uses only one data file.</p>\
                    <p>The theory will be applied to the highlighted file if any or to the first active file.</p>" % th.thname
                QMessageBox.warning(self, header, message)
            th.handle_actionMinimize_Error()

    def handle_thCurrentChanged(self, index):
        """Change figure when the active theory tab is changed
        
        [description]
        
        Arguments:
            - index {[type]} -- [description]
        """
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
        th.stop_theory_calc_flag = True
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

    def highlight_series(self):
        """Highligh the data series of the selected file
        
        [description]
        """
        self.do_plot()  #remove current series highlight
        file = self.selected_file
        if file is not None:
            dt = file.data_table
            for i in range(dt.MAX_NUM_SERIES):
                for nx in range(self.nplots):
                    view = self.parent_application.multiviews[nx]
                    if (i < view.n and file.active):
                        dt.series[nx][i].set_marker('.')
                        # dt.series[nx][i].set_linestyle(":")
                        dt.series[nx][i].set_markerfacecolor("black")
                        dt.series[nx][i].set_markeredgecolor("black")
                        dt.series[nx][i].set_zorder(
                            self.parent_application.zorder)  #put series on top
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

    def handle_actionNew_Theory(self):
        """Create new theory and do fit
        
        [description]
        """
        #if self.cbtheory.currentIndex() == 0:
        #    return
        self.actionNew_Theory.setDisabled(True)
        th_name = self.cbtheory.currentText()
        #self.cbtheory.setCurrentIndex(0) # reset the combobox selection
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
