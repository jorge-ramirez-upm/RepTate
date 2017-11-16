from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import itertools
import Symbols_rc
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTabWidget, QHeaderView, QToolBar, QComboBox, QMessageBox, QInputDialog, QFrame, QToolButton, QMenu, QAction, QAbstractItemView, QTableWidgetItem
from QFile import *
from DataSet import *

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
        self.num_theory_tab = 0
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
        
        self.cbtheory = QComboBox()
        self.cbtheory.setToolTip("Choose a Theory")
        self.cbtheory.addItem("Select Theory")
        self.cbtheory.model().item(0).setEnabled(False)
        for th in self.parent_application.theories:
            self.cbtheory.addItem(th)
        self.cbtheory.setMaximumWidth(115)
        self.cbtheory.setMinimumWidth(50)
        tb.addWidget(self.cbtheory)
        
        tb.addAction(self.actionNew_Theory)
   
        tb.addAction(self.actionCalculate_Theory)
        tb.addAction(self.actionMinimize_Error)
        tb.addAction(self.actionTheory_Options)
        self.TheoryLayout.insertWidget(0, tb)


        connection_id = self.actionNew_Theory.triggered.connect(self.NewTheory)
        connection_id = self.DataSettreeWidget.itemChanged.connect(self.handle_itemChanged)
        connection_id = self.DataSettreeWidget.itemDoubleClicked.connect(self.handle_itemDoubleClicked)
        #connection_id = self.DataSettreeWidget.itemClicked.connect(self.handle_itemClicked)
        connection_id = self.DataSettreeWidget.header().sortIndicatorChanged.connect(self.handle_sortIndicatorChanged)
        connection_id = self.DataSettreeWidget.itemSelectionChanged.connect(self.handle_itemSelectionChanged)
        connection_id = self.DataSettreeWidget.itemDoubleClicked.connect(self.handle_itemSelectionChanged)
    

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
                    file.data_table.series[i].set_marker("X")
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
        if self.cbtheory.currentIndex() == 0:
            return
        thname = self.cbtheory.currentText()
        self.cbtheory.setCurrentIndex(0)
        
        obj=QTreeWidget()
        obj.setIndentation(0)
        obj.setHeaderItem(QTreeWidgetItem(["Parameter", "Value"]))
        obj.setAlternatingRowColors(True)
        obj.setFrameShape(QFrame.NoFrame)
        obj.setFrameShadow(QFrame.Plain)
        #obj.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        obj.setEditTriggers(obj.NoEditTriggers) 
        connection_id = obj.itemDoubleClicked.connect(self.onTreeWidgetItemDoubleClicked)
        #self.actionNew_Theory.triggered.connect(self.NewTheory)
        #obj.setStyleSheet(QStyle("QTreeWidget::item { border: 0.5px ; border-style: solid ; border-color: lightgray ;}"))
        ##obj.styleSheet="QTreeWidget::item { border: 0.5px ; border-style: solid ; border-color: lightgray ;}\n"
        
        self.num_theory_tab += 1
        index = self.TheorytabWidget.addTab(obj, thname+'%d'%self.num_theory_tab)
        self.TheorytabWidget.setCurrentIndex(index)
        item = QTreeWidgetItem(obj, ['Param1', "%g"%4.345])
        item.setCheckState(0,2)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        item = QTreeWidgetItem(obj, ['Param2', "%g"%2.365])
        item.setCheckState(0,2)
        item.setFlags(item.flags() | Qt.ItemIsEditable)

    def onTreeWidgetItemDoubleClicked(self, item, column):
        if (column==1):
            thcurrent = self.TheorytabWidget.currentWidget()
            thcurrent.editItem(item, column)

