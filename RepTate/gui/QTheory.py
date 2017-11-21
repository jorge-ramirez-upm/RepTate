# from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from Theory import *
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QFrame, QHeaderView

Ui_TheoryTab, QWidget = loadUiType('gui/theorytab.ui')

class QTheory(Ui_TheoryTab, QWidget, Theory):     
    def __init__(self, name="QTheory", parent_dataset=None, ax=None):
        super().__init__(name=name, parent_dataset=parent_dataset, ax=ax)
        self.setupUi(self)

        #build the therory widget
        self.thParamTable.setIndentation(0)
        self.thParamTable.setColumnCount(3) 
        self.thParamTable.setHeaderItem(QTreeWidgetItem(["Parameter", "Value", "Error"]))
        # self.thParamTable.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.thParamTable.header().resizeSections(QHeaderView.ResizeToContents)
        self.thParamTable.setAlternatingRowColors(True)
        self.thParamTable.setFrameShape(QFrame.NoFrame)
        self.thParamTable.setFrameShadow(QFrame.Plain)
        self.thParamTable.setEditTriggers(self.thParamTable.NoEditTriggers) 
    
        self.thTextBox.setReadOnly(True)

        connection_id = self.thParamTable.itemDoubleClicked.connect(self.onTreeWidgetItemDoubleClicked)
        connection_id = self.thParamTable.itemChanged.connect(self.handle_parameterItemChanged)


    def update_parameter_table(self):
        """Update the theory parameter table"""
        #clean table
        self.thParamTable.clear()
        #populate table
        for param in sorted(self.parameters): #parameters in alphabetic order
            p = self.parameters[param]
            if p.min_allowed: #only allowed param enter the table
                try:
                    err = "%0.3g"%p.error
                except:
                    err = "-"    
                item = QTreeWidgetItem(self.thParamTable, [p.name, "%0.3g"%p.value, err])
                if p.min_flag:
                    item.setCheckState(0,2)
                else:
                    item.setCheckState(0,0)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.thParamTable.header().resizeSections(QHeaderView.ResizeToContents)


    def onTreeWidgetItemDoubleClicked(self, item, column):
        """Start editing text when a table cell is double clicked"""
        if (column==1):
            self.thParamTable.editItem(item, column)
            # thcurrent = self.parent_dataset.TheorytabWidget.currentWidget()
            # thcurrent.editItem(item, column)

    def handle_parameterItemChanged(self, item, column):
        """Modify parameter values when 
        changed in the theory table"""
        param_changed = item.text(0)
        if column==0: #param was checked/unchecked
            self.parameters[param_changed].min_flag = item.checkState(0)==Qt.Checked
            return
        #else, assign the entered value
        val = item.text(1)
        self.set_param_value(param_changed, val)


