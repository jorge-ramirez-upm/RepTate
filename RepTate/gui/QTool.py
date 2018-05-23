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

# def trap_exc_during_debug(*args):
#     # when app raises uncaught exception, print info
#     print(args)

# # install exception hook: without this, uncaught exception would cause application to exit
# sys.excepthook = trap_exc_during_debug


class EditThParametersDialog(QDialog):
    """Create the form that is used to modify the Tools parameters"""

    def __init__(self, parent, p_name):
        super().__init__(parent)
        self.parent_Tool = parent
        self.tabs = QTabWidget()
        self.all_pattr = {}
        for pname in self.parent_Tool.parameters:
            tab = self.create_param_tab(pname)
            self.tabs.addTab(tab, pname)
            if pname == p_name:
                index = self.tabs.indexOf(tab)
        self.tabs.setCurrentIndex(index)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok
                                     | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tabs)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("Tool Parameters")

    def create_param_tab(self, p_name):
        """Create a form to set the new values of the file parameters"""
        tab = QWidget()
        layout = QFormLayout()

        p = self.parent_Tool.parameters[p_name]
        p_attributes = p.__dict__
        attr_dict = {}
        a_new = []
        i = 0
        for attr_name in p_attributes:  #loop over the Parameters attributes
            if attr_name == 'type':
                cb = QComboBox()
                cb.addItem('real')
                cb.addItem('integer')
                cb.addItem('discrete_real')
                cb.addItem('discrete_integer')
                cb.addItem('boolean')
                # cb.setCurrentText('%s'.split(".")[-1] % p_attributes[attr_name])
                s = '%s' % p_attributes[attr_name]
                cb.setCurrentText(s.split(".")[-1])
                a_new.append(cb)
            elif attr_name == 'opt_type':
                cb = QComboBox()
                cb.addItem('opt')
                cb.addItem('nopt')
                cb.addItem('const')
                # cb.setCurrentText('%s'.split(".")[-1] % p_attributes[attr_name])
                s = '%s' % p_attributes[attr_name]
                cb.setCurrentText(s.split(".")[-1])
                a_new.append(cb)
            elif attr_name == 'min_shift_type':
                cb = QComboBox()
                cb.addItem('linear')
                cb.addItem('log')
                s = '%s' % p_attributes[attr_name]
                cb.setCurrentText(s.split(".")[-1])
                a_new.append(cb)
            elif attr_name == 'bracketed':
                cb = QComboBox()
                cb.addItem('True')
                cb.addItem('False')
                cb.setCurrentText('%s' % p_attributes[attr_name])
                a_new.append(cb)
            elif attr_name == 'display_flag':
                cb = QComboBox()
                cb.addItem('True')
                cb.addItem('False')
                cb.setCurrentText('%s' % p_attributes[attr_name])
                a_new.append(cb)
            elif attr_name in ['value', 'error']:
                continue
            else:
                qline = QLineEdit()
                if attr_name in ['name', 'description']:
                    qline.setReadOnly(True)
                a_new.append(qline)
                a_new[i].setText("%s" % p_attributes[attr_name])
            layout.addRow("%s:" % attr_name, a_new[i])
            attr_dict[attr_name] = a_new[i]
            i += 1
        tab.setLayout(layout)
        self.all_pattr[p_name] = attr_dict
        return tab


class CalculationThread(QObject):
    sig_done = pyqtSignal()

    def __init__(self, fthread, *args):
        super().__init__()
        self.args = args
        self.function = fthread

    def work(self):
        self.function(*self.args)
        self.sig_done.emit()


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

        connection_id = self.thParamTable.itemDoubleClicked.connect(
            self.onTreeWidgetItemDoubleClicked)
        connection_id = self.thParamTable.itemChanged.connect(
            self.handle_parameterItemChanged)

    def handle_actionCalculate_Tool(self):
        if self.thread_calc_busy:
            return
        self.thread_calc_busy = True
        #disable buttons
        self.parent_dataset.actionCalculate_Tool.setDisabled(True)
        self.parent_dataset.actionNew_Tool.setDisabled(True)
        try:
            self.Tool_buttons_disabled(
                True)  # TODO: Add that function to all theories
        except AttributeError:  #the function is not defined in the current Tool
            pass
        if CmdBase.calcmode == CalcMode.multithread:
            self.worker = CalculationThread(
                self.do_calculate,
                "",
            )
            self.worker.sig_done.connect(self.end_thread_calc)
            self.thread_calc = QThread()
            self.worker.moveToThread(self.thread_calc)
            self.thread_calc.started.connect(self.worker.work)
            self.thread_calc.start()
        elif CmdBase.calcmode == CalcMode.singlethread:
            self.do_calculate("")
            self.end_thread_calc()

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

    def onTreeWidgetItemDoubleClicked(self, item, column):
        """Start editing text when a table cell is double clicked
        Or edit all parameters dialog if parameter name is double clicked
        
        [description]
        
        Arguments:
            - - item {[type]} -- [description]
            - - column {[type]} -- [description]
        """
        if column == 0:
            p_name = item.text(0)
            d = EditThParametersDialog(self, p_name)
            if d.exec_():
                for pname in self.parameters:
                    p = self.parameters[pname]
                    attr_dict = d.all_pattr[pname]
                    for attr_name in attr_dict:
                        if attr_name == 'type':
                            val = attr_dict[attr_name].currentText()
                            setattr(p, attr_name, ParameterType[val])
                        elif attr_name == 'opt_type':
                            val = attr_dict[attr_name].currentText()
                            setattr(p, attr_name, OptType[val])
                        elif attr_name == 'min_shift_type':
                            val = attr_dict[attr_name].currentText()
                            setattr(p, attr_name, ShiftType[val])
                        elif attr_name == 'bracketed':
                            val = ast.literal_eval(
                                attr_dict[attr_name].currentText())  # bool
                            setattr(p, attr_name, val)
                        elif attr_name == 'display_flag':
                            val = ast.literal_eval(
                                attr_dict[attr_name].currentText())  # bool
                            setattr(p, attr_name, val)
                        elif attr_name == 'discrete_values':
                            val = attr_dict[attr_name].text()
                            l = ast.literal_eval(val)
                            if isinstance(l, list):
                                setattr(p, attr_name, l)
                        elif attr_name in ['name', 'description']:
                            continue
                        else:
                            val = float(attr_dict[attr_name].text())
                            setattr(p, attr_name, val)
                self.update_parameter_table()

        elif column == 1:
            self.thParamTable.editItem(item, column)
            # thcurrent = self.parent_dataset.TooltabWidget.currentWidget()
            # thcurrent.editItem(item, column)

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

    def actionActivepressed(self):
        self.active = self.actionActive.isChecked()
        self.parent_application.update_all_ds_plots()

    def actionApplyToTheorypressed(self):
        self.applytotheory = self.actionApplyToTheory.isChecked()
        self.parent_application.update_all_ds_plots()
