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
from RepTate.core.CmdBase import CmdBase, CalcMode
from RepTate.core.Tool import Tool
from os.path import dirname, join, abspath
from PyQt5.QtWidgets import QWidget, QTabWidget, QTreeWidget, QTreeWidgetItem, QFrame, QHeaderView, QMessageBox, QDialog, QVBoxLayout, QRadioButton, QDialogButtonBox, QButtonGroup, QFormLayout, QLineEdit, QComboBox, QLabel, QToolBar
from PyQt5.QtCore import Qt, QObject, QThread, QSize, pyqtSignal, pyqtSlot, QEvent
from PyQt5.QtGui import QDoubleValidator, QIcon, QCursor
from RepTate.core.Parameter import OptType, ParameterType
from math import ceil, floor
import ast
PATH = dirname(abspath(__file__))
sys.path.append(PATH)
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

        self.tb = QToolBar()
        self.tb.setIconSize(QSize(24,24))
        self.actionActive.setChecked(True)
        self.actionApplyToTheory.setChecked(True)
        self.tb.addAction(self.actionActive)
        self.tb.addAction(self.actionApplyToTheory)
        self.verticalLayout.insertWidget(0, self.tb)

        #build the tool widget
        self.toolParamTable.setIndentation(0)
        self.toolParamTable.setColumnCount(2)
        self.toolParamTable.setHeaderItem(QTreeWidgetItem(["Parameter", "Value"]))
        self.toolParamTable.header().resizeSections(QHeaderView.ResizeToContents)
        self.toolParamTable.setAlternatingRowColors(True)
        self.toolParamTable.setFrameShape(QFrame.NoFrame)
        self.toolParamTable.setFrameShadow(QFrame.Plain)
        self.toolParamTable.setEditTriggers(self.toolParamTable.NoEditTriggers)

        self.toolTextBox.setReadOnly(True)
        self.toolTextBox.setContextMenuPolicy(Qt.CustomContextMenu)
        self.toolTextBox.customContextMenuRequested.connect(self.toolTextBox_context_menu)

        connection_id = self.actionActive.triggered.connect(self.handle_actionActivepressed)
        connection_id = self.actionApplyToTheory.triggered.connect(self.handle_actionApplyToTheorypressed)

        connection_id = self.toolParamTable.itemDoubleClicked.connect(self.onTreeWidgetItemDoubleClicked)
        connection_id = self.toolParamTable.itemChanged.connect(self.handle_parameterItemChanged)
        self.toolParamTable.setEditTriggers(QTreeWidget.EditKeyPressed)

    def toolTextBox_context_menu(self):
        """Custom contextual menu for the theory textbox"""
        menu = self.toolTextBox.createStandardContextMenu()
        menu.addSeparator()
        menu.addAction("Increase Font Size", lambda: self.change_toolTextBox_fontsize(1.25))
        menu.addAction("Deacrease Font Size", lambda: self.change_toolTextBox_fontsize(0.8))
        menu.addAction("Clear Text", self.toolTextBox.clear)
        menu.exec_(QCursor.pos())

    def change_toolTextBox_fontsize(self, factor):
        """Change the toolTextBox font size by a factor `factor` """
        font = self.toolTextBox.currentFont()
        if factor < 1:
            font_size = ceil(font.pointSize() * factor)
        else:
            font_size = floor(font.pointSize() * factor)
        font.setPointSize(font_size)
        self.toolTextBox.document().setDefaultFont(font)

    def editItem(self, item, column):
        print(column)

    def update_parameter_table(self):
        """Update the Tool parameter table

        [description]
        """
        #clean table
        self.toolParamTable.clear()

        #populate table
        for param in self.parameters:
            p = self.parameters[param]
            if p.display_flag:  #only allowed param enter the table
                if (p.type == ParameterType.string):
                    item = QTreeWidgetItem(self.toolParamTable, [p.name, p.value])
                else:
                    item = QTreeWidgetItem(self.toolParamTable, [p.name, "%0.4g" % p.value])
                item.setToolTip(0, p.description)

                item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.toolParamTable.header().resizeSections(QHeaderView.ResizeToContents)

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

    def handle_actionActivepressed(self, checked):
        if checked:
            self.actionActive.setIcon(
                QIcon(':/Icon8/Images/new_icons/icons8-toggle-on.png'))
        else:
            self.actionActive.setIcon(
                QIcon(':/Icon8/Images/new_icons/icons8-toggle-off.png'))
        self.actionActive.setChecked(checked)
        self.active = checked
        self.parent_application.update_all_ds_plots()

    # def actionActivepressed(self):
    #     self.active = self.actionActive.isChecked()
    #     self.parent_application.update_all_ds_plots()

    def handle_actionApplyToTheorypressed(self, checked):
        if checked:
            self.actionApplyToTheory.setIcon(
                QIcon(':/Icon8/Images/new_icons/icons8-einstein-yes.png'))
        else:
            self.actionApplyToTheory.setIcon(
                QIcon(':/Icon8/Images/new_icons/icons8-einstein-no.png'))
        self.actionApplyToTheory.setChecked(checked)
        self.applytotheory = checked
        self.parent_application.update_all_ds_plots()

    def onTreeWidgetItemDoubleClicked(self, item, column):
        """Start editing text when a table cell is double clicked
        """
        if column == 1:
            self.toolParamTable.editItem(item, column)
