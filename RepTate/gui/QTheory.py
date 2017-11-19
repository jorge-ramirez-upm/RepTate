# from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Theory import *
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QFrame

class QTheory(QTreeWidget, Theory):     
    def __init__(self, name="QTheory", parent_dataset=None, ax=None):
        print("QTheory.__init__() called")
        super(QTheory, self).__init__(name=name, parent_dataset=parent_dataset, ax=ax)
        print("QTheory.__init__() ended")

        #build the therory widget
        self.setIndentation(0)
        self.setHeaderItem(QTreeWidgetItem(["Parameter", "Value"]))
        self.setAlternatingRowColors(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.setEditTriggers(self.NoEditTriggers) 
        self.setColumnCount(2) 

        connection_id = self.itemDoubleClicked.connect(self.onTreeWidgetItemDoubleClicked)
        connection_id = self.itemChanged.connect(self.handle_parameterItemChanged)

        
    
    def update_parameter_table(self):
        """Update the theory parameter table"""
        #clean and resize table
        self.clear()
        #populate table
        for param in self.parameters.values():
            item = QTreeWidgetItem(self, [param.name, "%g"%param.value])
            item.setWhatsThis(2, param.description)
            if param.min_flag:
                item.setCheckState(0,2)
            else:
                item.setCheckState(0,0)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
  
    def onTreeWidgetItemDoubleClicked(self, item, column):
        """Start editing text when a table cell is double clicked"""
        if (column==1):
            thcurrent = self.parent_dataset.TheorytabWidget.currentWidget()
            thcurrent.editItem(item, column)

    def handle_parameterItemChanged(self, item, column):
        """Modify parameter values when 
        changed in the theory table"""
        param_changed = item.text(0)
        if column==0: #param was checked/unchecked
            self.parameters[param_changed].min_flag = item.checkState(0)==Qt.Checked
            return
        #else, find the type of parameter (real, integer, ...)
        #and assign the entered value
        val = item.text(1)
        ptype = self.parameters[param_changed].type
        if (ptype==ParameterType.real):
            value = float(val)
        elif (ptype==ParameterType.integer):
            value = int(val)
        else:
            print("type not supported")
            return 
        self.parameters[param_changed].value = value