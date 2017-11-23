from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import itertools
import Symbols_rc
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTabWidget, QHeaderView, QToolBar, QComboBox, QMessageBox, QInputDialog, QFrame, QToolButton, QMenu, QAction, QAbstractItemView, QTableWidgetItem
from DataSet import *
from QTheory import *
from SubQTreeWidget import *

Ui_DataSet, QWidget = loadUiType('gui/DataSet.ui')

class QDataSet(DataSet, QWidget, Ui_DataSet): 
    def __init__(self, name="QDataSet", parent=None):
        "Constructor"
        super().__init__(name=name, parent=parent)
        QWidget.__init__(self)
        Ui_DataSet.__init__(self)

        self.setupUi(self)
        self.selected_file = None

        self.DataSettreeWidget = SubQTreeWidget(self)
        self.splitter.insertWidget(0, self.DataSettreeWidget)
        

        self.DataSettreeWidget.setIndentation(0)
        self.DataSettreeWidget.setHeaderItem(QTreeWidgetItem([""]))   
        self.DataSettreeWidget.setSelectionMode(1) #QAbstractItemView::SingleSelection
        hd = self.DataSettreeWidget.header()
        hd.setSectionsMovable(False)
        w = self.DataSettreeWidget.width()
        w /= hd.count()
        for i in range(hd.count()):
            hd.resizeSection(0, w)
        


        # Theory Toolbar
        tb = QToolBar()
        tb.setIconSize(QSize(24,24))
        tb.addAction(self.actionNew_Theory)
        self.cbtheory = QComboBox()
        self.cbtheory.setToolTip("Choose a Theory")
        self.cbtheory.addItem("Select Theory")
        self.cbtheory.model().item(0).setEnabled(False)

        for th_name in self.parent_application.theories:
             self.cbtheory.addItem(th_name)
        # self.cbtheory.addItem("MaxwellModesFrequency") 
        # self.cbtheory.addItem("MWDiscr") 
        
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
        self.TheoryLayout.insertWidget(0, tb)

        #desactive buttons when no theory tab
        self.theory_actions_disabled(True)

        connection_id = self.actionNew_Theory.triggered.connect(self.handle_actionNew_Theory)
        connection_id = self.DataSettreeWidget.itemChanged.connect(self.handle_itemChanged)
        connection_id = self.DataSettreeWidget.itemDoubleClicked.connect(self.handle_itemDoubleClicked)
        #connection_id = self.DataSettreeWidget.itemClicked.connect(self.handle_itemClicked)
        connection_id = self.DataSettreeWidget.header().sortIndicatorChanged.connect(self.handle_sortIndicatorChanged)
        connection_id = self.DataSettreeWidget.itemSelectionChanged.connect(self.handle_itemSelectionChanged)

        connection_id = self.TheorytabWidget.tabCloseRequested.connect(self.handle_thTabCloseRequested)
        connection_id = self.TheorytabWidget.tabBarDoubleClicked.connect(self.handle_thTabBarDoubleClicked)
        connection_id = self.TheorytabWidget.currentChanged.connect(self.handle_thCurrentChanged)
        connection_id = self.actionMinimize_Error.triggered.connect(self.handle_actionMinimize_Error)
        connection_id = self.actionCalculate_Theory.triggered.connect(self.handle_actionCalculate_Theory)

        connection_id = self.actionVertical_Limits.triggered.connect(self.toggle_vertical_limits)
        connection_id = self.actionHorizontal_Limits.triggered.connect(self.toggle_horizontal_limits)


    def theory_actions_disabled(self, state):
        """Disable theory buttons if no theory tab is open"""
        self.actionCalculate_Theory.setDisabled(state)
        self.actionMinimize_Error.setDisabled(state)
        # self.actionTheory_Options.setDisabled(state)
        self.actionShow_Limits.setDisabled(state)
        self.actionVertical_Limits.setDisabled(state)
        self.actionHorizontal_Limits.setDisabled(state)

    def set_limit_icon(self):
        hlim = self.actionHorizontal_Limits.isChecked()
        vlim = self.actionVertical_Limits.isChecked()
        if hlim and vlim:
            img = "Line Chart Both Limits"
        elif vlim:
            img = "Line Chart Vertical Limits"
        elif hlim:
            img = "Line Chart Horizontal Limits"
        else:
            img = "Line Chart"
        self.actionShow_Limits.setIcon(QIcon(':/Images/Images/%s'%img))

    def set_no_limits(self, th_name):
        """Turn the x and yrange selectors off"""
        if th_name in self.theories:
            th = self.theories[self.current_theory]
            th.xrange.set_visible(False) 
            th.xminline.set_visible(False) 
            th.xmaxline.set_visible(False) 

            th.yrange.set_visible(False) 
            th.yminline.set_visible(False) 
            th.ymaxline.set_visible(False) 

            self.actionHorizontal_Limits.setChecked(False)
            self.actionVertical_Limits.setChecked(False)
            self.set_limit_icon()

    def toggle_vertical_limits(self):
        """Show/Hide the xrange selector for fit"""
        if self.current_theory:
            self.theories[self.current_theory].do_xrange("")
            self.set_limit_icon()
 
    def toggle_horizontal_limits(self):
        """Show/Hide the yrange selector for fit"""
        if self.current_theory:        
            self.theories[self.current_theory].do_yrange("")
            self.set_limit_icon()

    def handle_actionCalculate_Theory(self):
        """Calculate the theory"""
        if self.current_theory and self.files!=[]:
            self.theories[self.current_theory].do_calculate("")
            self.theories[self.current_theory].update_parameter_table()

    def handle_actionMinimize_Error(self):
        """Minimize the error"""
        if self.current_theory and self.files!=[]:
            self.theories[self.current_theory].do_fit("")
            self.theories[self.current_theory].update_parameter_table()

    def handle_thCurrentChanged(self, index):
        """Change figure when the active theory tab is changed"""
        th = self.TheorytabWidget.widget(index)
        if th:
            th.do_show()
            self.current_theory = th.name
            ntab = self.TheorytabWidget.count()
            #hide all theory curves
            for i in range(ntab):   
                if i != index:
                    th_to_hide = self.TheorytabWidget.widget(i)
                    th_to_hide.do_hide()
        else:
            self.current_theory = None
            self.theory_actions_disabled(True)
        self.parent_application.update_plot()
        self.parent_application.update_Qplot()

    def Qshow_all(self):
        """Show all the files in this dataset, except those previously hiden"""
        self.do_show_all()
        for i in range(self.DataSettreeWidget.topLevelItemCount()):
            file_name = self.DataSettreeWidget.topLevelItem(i).text(0)
            if file_name in self.inactive_files:
                self.DataSettreeWidget.topLevelItem(i).setCheckState(0, 0)
            else:
                self.DataSettreeWidget.topLevelItem(i).setCheckState(0, 2)


    def handle_thTabBarDoubleClicked(self, index):
        """Edit theory tab name"""
        pass

    def handle_thTabCloseRequested(self, index):
        """Delete a theory tab from the current dataset"""
        th_name = self.TheorytabWidget.widget(index).name
        self.set_no_limits(th_name)
        self.do_theory_delete(th_name) #call DataSet.do_theory_delete 
        self.TheorytabWidget.removeTab(index)


    def handle_itemSelectionChanged(self):
        """Define actions for when a file table is selected"""
        selection = self.DataSettreeWidget.selectedItems()
        if selection==[]:
            self.selected_file = None
            self.highlight_series()
            return
        for f in self.files:
            if f.file_name_short==selection[0].text(0):  
                self.parent_application.disconnect_curve_drag()  
                self.selected_file = f
                self.highlight_series()
                self.populate_inspector()

    def highlight_series(self):
        """Highligh the data series of the selected file"""
        self.do_plot() #remove current series highlight
        file = self.selected_file
        if file is not None:
            view = self.parent_application.current_view
            for i in range(file.data_table.MAX_NUM_SERIES):
                    if (i<view.n and file.active):
                        file.data_table.series[i].set_marker('.')
                        # file.data_table.series[i].set_linestyle(":")
                        file.data_table.series[i].set_markerfacecolor("black")
                        file.data_table.series[i].set_markeredgecolor("black")
                        file.data_table.series[i].set_zorder(self.parent_application.zorder) #put series on top
            self.parent_application.zorder += 1
        self.parent_application.update_plot()

    def populate_inspector(self):
        file = self.selected_file
        if not file: 
            self.parent_application.tableWidget.setRowCount(0)
            self.parent_application.DataInspectordockWidget.setWindowTitle("File:")
            return
        if self.parent_application.DataInspectordockWidget.isHidden():
            return
        dt = file.data_table
        nrow = dt.num_rows
        ncol = dt.num_columns
        inspec_tab = self.parent_application.tableWidget
        inspec_tab.setRowCount(nrow)
        inspec_tab.setColumnCount(ncol)
        for i in range(nrow):
            for j in range(ncol):
                x = "%.3e" %dt.data[i, j]
                inspec_tab.setItem(i, j, QTableWidgetItem(x)) # dt.setItem(row, column, item)
        ds_index = self.parent_application.DataSettabWidget.currentIndex()
        self.parent_application.DataInspectordockWidget.setWindowTitle(
            "File: \"%s\" in %s"%(file.file_name_short, self.parent_application.DataSettabWidget.tabText(ds_index)))
        
    def handle_itemChanged(self, item, column):
        self.change_file_visibility(item.text(0), item.checkState(column)==Qt.Checked)
            
    def handle_sortIndicatorChanged(self, column, order):
        """Sort files according to the selected parameter (column) and replot"""
        # if column == 0: #do not sort file name
        #     return
        sort_param = self.DataSettreeWidget.headerItem().text(column)
        rev = True if order==Qt.AscendingOrder else False
        if rev:
            sort_param = sort_param + ",reverse"
        self.do_sort(sort_param)
        self.do_plot()

    def Qshow_all(self):
        """Show all the files in this dataset, except those previously hiden"""
        self.do_show_all()
        for i in range(self.DataSettreeWidget.topLevelItemCount()):
            file_name = self.DataSettreeWidget.topLevelItem(i).text(0)
            if file_name in self.inactive_files:
                self.DataSettreeWidget.topLevelItem(i).setCheckState(0, 0)
            else:
                self.DataSettreeWidget.topLevelItem(i).setCheckState(0, 2)

    def resizeEvent(self, evt=None):
        hd=self.DataSettreeWidget.header()
        w=self.DataSettreeWidget.width()
        w/=hd.count()
        for i in range(hd.count()):
            hd.resizeSection(i, w)        
            #hd.setTextAlignment(i, Qt.AlignHCenter)

    def handle_itemDoubleClicked(self, item, column):
        """Edit item entry upon double click"""
        if column>0:
            param = self.DataSettreeWidget.headerItem().text(column) #retrive parameter name
            file_name_short = item.text(0) #retrive file name
            header = "Edit Parameter"
            message = "Do you want to edit %s of \"%s\"?"%(param, file_name_short)
            answer = QMessageBox.question(self, header, message)
            if answer == QMessageBox.Yes:
                old_value = item.text(column) #old parameter value       
                message = "New value of %s"%param
                new_value, success = QInputDialog.getDouble(self, header, message, float(old_value))
                if success:
                    for file in self.files:
                        if file.file_name_short == file_name_short:
                            file.file_parameters[param] = new_value #change value in DataSet
                    self.DataSettreeWidget.blockSignals(True) #avoid triggering 'itemChanged' signal that causes a false checkbox change
                    item.setText(column, str(new_value)) #change table label
                    self.DataSettreeWidget.blockSignals(False)

    def handle_actionNew_Theory(self):
        """Create new theory and do fit"""
        if self.cbtheory.currentIndex() == 0:
            return
        th_name = self.cbtheory.currentText()
        self.cbtheory.setCurrentIndex(0) # reset the combobox selection
        self.new_theory(th_name)

    def new_theory(self, th_name, th_tab_id=""):    
        if not self.files:
            return
        if self.parent_application.theories[th_name].single_file and len(self.files)>1: 
            header = "New Theory"
            message = "Theory \"%s\" cannot be applied to multiple data files"%th_name
            QMessageBox.warning(self, header, message)
            return
        if self.current_theory:
            self.set_no_limits(self.current_theory) #remove the xy-range limits
        newth = self.do_theory_new(th_name)

        # add new theory tab
        if th_tab_id == "": 
            th_name_short = ''.join(c for c in th_name if c.isupper()) #get the upper case letters of th_name
            th_tab_id = "%s%d"%(th_name_short, self.num_theories) #append number
        index = self.TheorytabWidget.addTab(newth, th_tab_id) #add theory tab
        self.TheorytabWidget.setCurrentIndex(index) #set new theory tab as curent tab
        #self.handle_thCurrentChanged(index)
        newth.update_parameter_table()
        self.theory_actions_disabled(False)
