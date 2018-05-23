# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Tool and Experiments
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
# Copyright (2018): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module QTool

Module that defines the GUI counterpart of the class Tool.

"""
#from PyQt5.QtCore import *
import sys
from PyQt5.uic import loadUiType
from CmdBase import CmdBase, CalcMode
from Tool import Tool
from os.path import dirname, join, abspath
from PyQt5.QtWidgets import QWidget, QTabWidget, QTreeWidget, QTreeWidgetItem, QFrame, QHeaderView, QMessageBox, QDialog, QVBoxLayout, QRadioButton, QDialogButtonBox, QButtonGroup, QFormLayout, QLineEdit, QComboBox, QLabel, QToolBar
from PyQt5.QtCore import Qt, QObject, QThread, QSize, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QDoubleValidator
from Parameter import OptType, ParameterType, ShiftType
import ast
PATH = dirname(abspath(__file__))
Ui_ToolTab, QWidget = loadUiType(join(PATH, 'Tooltab.ui'))

class QTool(Ui_ToolTab, QWidget, Tool):
    """[summary]
    
    [description]
    """

    def __init__(self, name="QTool", parent_app=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"QTool"})
            - parent_dataset {[type]} -- [description] (default: {None})
            - axarr {[type]} -- [description] (default: {None})
        """
        super().__init__(name=name, parent_app=parent_app)
        self.setupUi(self)

        tb = QToolBar()
        tb.setIconSize(QSize(24,24))
        self.actionActive.setChecked(True)
        self.actionApplyToTheory.setChecked(True)
        tb.addAction(self.actionActive)
        tb.addAction(self.actionApplyToTheory)
        self.verticalLayout_2.insertWidget(0, tb)

        #build the therory widget
        self.thParamTable.setIndentation(0)
        self.thParamTable.setColumnCount(2)
        self.thParamTable.setHeaderItem(QTreeWidgetItem(["Parameter", "Value"]))
        self.thParamTable.header().resizeSections(QHeaderView.ResizeToContents)
        self.thParamTable.setAlternatingRowColors(True)
        self.thParamTable.setFrameShape(QFrame.NoFrame)
        self.thParamTable.setFrameShadow(QFrame.Plain)
        self.thParamTable.setEditTriggers(self.thParamTable.NoEditTriggers)

        self.thTextBox.setReadOnly(True)

        connection_id = self.actionActive.triggered.connect(self.actionActivepressed)
        connection_id = self.actionApplyToTheory.triggered.connect(self.actionApplyToTheorypressed)

        connection_id = self.thParamTable.itemChanged.connect(
            self.handle_parameterItemChanged)

    def update_parameter_table(self):
        """Update the Tool parameter table
        
        [description]
        """
        #clean table
        self.thParamTable.clear()

        #populate table
        for param in self.parameters:
            p = self.parameters[param]
            if p.display_flag:  #only allowed param enter the table
                if p.opt_type == OptType.const:
                    item = QTreeWidgetItem(
                        self.thParamTable,
                        [p.name, "%0.3g" % p.value, "N/A"])
                    item.setCheckState(0, Qt.PartiallyChecked)
                    item.setFlags(item.flags() & ~Qt.ItemIsUserCheckable)
                else:
                    try:
                        err = "%0.3g" % p.error
                    except:
                        err = "-"
                    item = QTreeWidgetItem(
                        self.thParamTable,
                        [p.name, "%0.3g" % p.value, err])
                    if p.opt_type == OptType.opt:
                        item.setCheckState(0, Qt.Checked)
                    elif p.opt_type == OptType.nopt:
                        item.setCheckState(0, Qt.Unchecked)

                item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.thParamTable.header().resizeSections(QHeaderView.ResizeToContents)

    def handle_parameterItemChanged(self, item, column):
        """Modify parameter values when changed in the Tool table
        
        [description]
        
        Arguments:
            - item {[type]} -- [description]
            - column {[type]} -- [description]
        """
        param_changed = item.text(0)
        if column == 0:  #param was checked/unchecked
            if item.checkState(0) == Qt.Checked:
                self.parameters[param_changed].opt_type = OptType.opt
            elif item.checkState(0) == Qt.Unchecked:
                self.parameters[param_changed].opt_type = OptType.nopt
            return
        #else, assign the entered value
        new_value = item.text(1)
        message, success = self.set_param_value(param_changed, new_value)
        if (not success):
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            if message != '':
                msg.setText("Not a valid value\n" + message)
            else:
                msg.setText("Not a valid value")
            msg.exec_()
            item.setText(1, str(self.parameters[param_changed].value))
        self.parent_application.update_all_ds_plots()

    def actionActivepressed(self):
        self.active = self.actionActive.isChecked()
        self.parent_application.update_all_ds_plots()

    def actionApplyToTheorypressed(self):
        self.applytotheory = self.actionApplyToTheory.isChecked()
        self.parent_application.update_all_ds_plots()
