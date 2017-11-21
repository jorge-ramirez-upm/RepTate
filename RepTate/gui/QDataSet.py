from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import itertools
import Symbols_rc
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTabWidget, QHeaderView, QToolBar, QComboBox, QMessageBox, QInputDialog, QFrame, QToolButton, QMenu, QAction, QAbstractItemView, QTableWidgetItem
from QFile import *
from DataSet import *
from QTheory import *

Ui_DataSet, QWidget = loadUiType('gui/DataSet.ui')

class QDataSet(DataSet, QWidget, Ui_DataSet): 
    def __init__(self, name="QDataSet", parent=None):
        "Constructor"
        print("QDataSet.__init__(self) called")
        super(QDataSet, self).__init__(name=name, parent=parent)
        QWidget.__init__(self)
        Ui_DataSet.__init__(self)
        print("QDataSet.__init__(self) ended")

        self.setupUi(self)
        self.selected_file = None


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
        tb.addAction(self.actionTheory_Options)

        tbut = QToolButton()
        tbut.setPopupMode(QToolButton.MenuButtonPopup)
        tbut.setDefaultAction(self.actionShow_Limits)
        menu=QMenu()
        menu.addAction(self.actionNo_Limits)
        menu.addAction(self.actionVertical_Limits)
        menu.addAction(self.actionHorizontal_Limits)
        menu.addAction(self.actionBoth_Limits)
        tbut.setMenu(menu)
        
        tb.addWidget(tbut)

        self.TheoryLayout.insertWidget(0, tb)

        #Buttons not wired yet
        self.actionShow_Limits.setDisabled(True)
        self.actionTheory_Options.setDisabled(True)

        # # Theory text display
        # self.ThText.setReadOnly(True)
        # self.ThText.setHtml("""
        # <head>
        #     <title>Some HTML text</title>
        # </head>
            
        # <body>
        #  <center>
        #     <p> <b>Hello</b> <i>Qt!</i></p>
        #  </center>
        #     <hr />
        #     <p>This is some HTML text</p>
        #       <p>An image: <img src="gui/Images/logo.jpg"> </p>
        # </body>
            
        # </html>
        # """)
        connection_id = self.actionNew_Theory.triggered.connect(self.NewTheory)
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

        connection_id = self.actionNo_Limits.triggered.connect(self.No_Limits)
        connection_id = self.actionVertical_Limits.triggered.connect(self.Vertical_Limits)
        connection_id = self.actionHorizontal_Limits.triggered.connect(self.Horizontal_Limits)
        connection_id = self.actionBoth_Limits.triggered.connect(self.Both_Limits)


    def No_Limits(self):
        self.actionShow_Limits.setIcon(self.actionNo_Limits.icon())

    def Vertical_Limits(self):
        self.actionShow_Limits.setIcon(self.actionVertical_Limits.icon())

    def Horizontal_Limits(self):
        self.actionShow_Limits.setIcon(self.actionHorizontal_Limits.icon())

    def Both_Limits(self):
        self.actionShow_Limits.setIcon(self.actionBoth_Limits.icon())
        
    def handle_actionCalculate_Theory(self):
        """Calculate the theory"""
        if self.current_theory:
            self.theories[self.current_theory].do_calculate("")
            self.theories[self.current_theory].update_parameter_table()

            
    def handle_actionMinimize_Error(self):
        """Minimize the error"""
        if self.current_theory:
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
                    th = self.TheorytabWidget.widget(i)
                    th.do_hide()
        else:
            self.current_theory = None
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
        self.do_theory_delete(th_name) #call DataSet.do_theory_delete 
        self.TheorytabWidget.removeTab(index)


    def handle_itemSelectionChanged(self):
        """Define actions for when a file table is selected"""
        selection = self.DataSettreeWidget.selectedItems()
        if selection==[]:
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
        if not file:
            return
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

    def NewTheory(self):
        """Create new theory and do fit"""
        if self.cbtheory.currentIndex() == 0:
            return
        th_name = self.cbtheory.currentText()
        self.cbtheory.setCurrentIndex(0) # reset the combobox selection
        if not self.files:
            return
        if self.parent_application.theories[th_name].single_file and len(self.files)>1: 
            header = "New Theory"
            message = "Theory \"%s\" cannot be applied to multiple data files"%th_name
            QMessageBox.warning(self, header, message)
            return
        newth = self.do_theory_new(th_name)

        # add new theory tab
        th_name_short = ''.join(c for c in th_name if c.isupper()) #get the upper case letters of th_name
        th_tab_id = "%s%d"%(th_name_short, self.num_theories) #append number
        index = self.TheorytabWidget.addTab(newth, th_tab_id) #add theory tab
        self.TheorytabWidget.setCurrentIndex(index) #set new theory tab as curent tab

        newth.update_parameter_table()
