# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module QTheory

Module that defines the GUI counterpart of the class Theory.

""" 
#from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from Theory import Theory
from os.path import dirname, join, abspath
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QFrame, QHeaderView, QMessageBox, QDialog, QVBoxLayout, QRadioButton, QDialogButtonBox, QButtonGroup
from PyQt5.QtCore import Qt

PATH = dirname(abspath(__file__))
Ui_TheoryTab, QWidget = loadUiType(join(PATH,'theorytab.ui'))

class GetModesDialog(QDialog):
    def __init__(self, parent = None, th_dict = {}):
        super(GetModesDialog, self).__init__(parent)

        self.setWindowTitle("Get Maxwell modes")
        layout = QVBoxLayout(self)
        
        self.btngrp = QButtonGroup()

        for item in th_dict.keys():
            rb = QRadioButton(item, self)
            layout.addWidget(rb)
            self.btngrp.addButton(rb)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)    
        
    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getMaxwellModesProvider(self, parent = None, th_dict = {}):
        dialog = GetModesDialog(parent, th_dict)
        result = dialog.exec_()
        return (self.btngrp.checkedButton().text(), result == QDialog.Accepted)

class QTheory(Ui_TheoryTab, QWidget, Theory):
    """[summary]
    
    [description]
    """
    def __init__(self, name="QTheory", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"QTheory"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
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
        """Update the theory parameter table
        
        [description]
        """
        #clean table
        self.thParamTable.clear()
        #populate table
        for param in sorted(self.parameters): #parameters in alphabetic order
            p = self.parameters[param]
            if p.display_flag: #only allowed param enter the table
                try:
                    err = "%0.3g"%p.error
                except:
                    err = "-"    
                item = QTreeWidgetItem(self.thParamTable, [p.name, "%0.3g"%p.value, err])
                if p.min_flag:
                    item.setCheckState(0, Qt.Checked)
                else:
                    item.setCheckState(0, Qt.PartiallyChecked)
                    item.setFlags(item.flags() & ~Qt.ItemIsUserCheckable)
                    
                item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.thParamTable.header().resizeSections(QHeaderView.ResizeToContents)


    def onTreeWidgetItemDoubleClicked(self, item, column):
        """Start editing text when a table cell is double clicked
        
        [description]
        
        Arguments:
            item {[type]} -- [description]
            column {[type]} -- [description]
        """
        if (column==1):
            self.thParamTable.editItem(item, column)
            # thcurrent = self.parent_dataset.TheorytabWidget.currentWidget()
            # thcurrent.editItem(item, column)

    def handle_parameterItemChanged(self, item, column):
        """Modify parameter values when changed in the theory table
        
        [description]
        
        Arguments:
            item {[type]} -- [description]
            column {[type]} -- [description]
        """
        param_changed = item.text(0)
        if column==0: #param was checked/unchecked
            self.parameters[param_changed].min_flag = item.checkState(0)==Qt.Checked
            return
        #else, assign the entered value
        val = item.text(1)
        success = self.set_param_value(param_changed, val)
        if (not success):
            msg = QMessageBox()
            msg.setWindowTitle("Not a valid value")
            msg.setText("Allowed values are: \n"+", ".join(str(x) for x in self.parameters[param_changed].discrete_values))
            msg.exec_()
            item.setText(1, str(self.parameters[param_changed].value))

    def Qcopy_modes(self):
        """[summary]
        
        [description]
        """
        apmng=self.parent_dataset.parent_application.parent_manager
        G, S=apmng.list_theories_Maxwell()
        for item in G.keys():
            if self.name in item:
                del G[item]
                break
        if G:
            d = GetModesDialog(self, G)
            if d.exec_():
                item = d.btngrp.checkedButton().text()
                tau, G0 = G[item]()
                self.set_modes(tau,G0)
            
            #item, success = GetModesDialog.getMaxwellModesProvider(parent=self, th_dict=G)
            #print(item)
            
            #d = QDialog(self, )
            #layout = QVBoxLayout(d)
            #d.setLayout(layout)
            #for item in G.keys():
            #    rb = QRadioButton(item, d)
            #    layout.addWidget(rb)
            #d.setWindowTitle("Select provider of Maxwell modes:")
            #d.setWindowModality(Qt.ApplicationModal)
            #d.exec_()