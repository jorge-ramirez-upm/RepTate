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
# Copyright (2017-2020): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module QTheory

Module that defines the GUI counterpart of the class Theory.

"""
#from PyQt5.QtCore import *
import sys
from PyQt5.uic import loadUiType
from RepTate.core.CmdBase import CmdBase, CalcMode
from RepTate.core.Theory import Theory, MinimizationMethod, ErrorCalculationMethod
from os.path import dirname, join, abspath
from PyQt5.QtWidgets import QWidget, QTabWidget, QTreeWidget, QTreeWidgetItem, QFrame, QHeaderView, QMessageBox, QDialog, QVBoxLayout, QRadioButton, QDialogButtonBox, QButtonGroup, QFormLayout, QLineEdit, QComboBox, QLabel, QFileDialog, QApplication, QTextBrowser, QSplitter, QMenu
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QCursor
from RepTate.core.Parameter import OptType, ParameterType
from math import ceil, floor
import RepTate.core.Version as Version
import time
import ast
PATH = dirname(abspath(__file__))
Ui_TheoryTab, QWidget = loadUiType(join(PATH, 'theorytab.ui'))
from fittingoptions import Ui_Dialog
import errorcalculationoptions

# def trap_exc_during_debug(*args):
#     # when app raises uncaught exception, print info
#     print(args)

# # install exception hook: without this, uncaught exception would cause application to exit
# sys.excepthook = trap_exc_during_debug


class EditThParametersDialog(QDialog):
    """Create the form that is used to modify the theorys parameters"""

    def __init__(self, parent, p_name):
        super().__init__(parent)
        self.parent_theory = parent
        self.tabs = QTabWidget()
        self.all_pattr = {}
        for pname in self.parent_theory.parameters:
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
        self.setWindowTitle("Theory Parameters")

    def create_param_tab(self, p_name):
        """Create a form to set the new values of the file parameters"""
        tab = QWidget()
        layout = QFormLayout()

        p = self.parent_theory.parameters[p_name]
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


class GetModesDialog(QDialog):
    def __init__(self, parent=None, th_dict={}):
        super(GetModesDialog, self).__init__(parent)

        self.setWindowTitle("Get Maxwell modes")
        layout = QVBoxLayout(self)

        self.btngrp = QButtonGroup()

        for item in th_dict.keys():
            rb = QRadioButton(item, self)
            layout.addWidget(rb)
            self.btngrp.addButton(rb)

        #select first button by default
        rb = self.btngrp.buttons()[0]
        rb.setChecked(True)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


class QTheory(Ui_TheoryTab, QWidget, Theory):
    """[summary]

    [description]
    """

    def __init__(self, name="QTheory", parent_dataset=None, axarr=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {"QTheory"})
            - parent_dataset {[type]} -- [description] (default: {None})
            - axarr {[type]} -- [description] (default: {None})
        """
        super().__init__(name=name, parent_dataset=parent_dataset, axarr=axarr)
        self.setupUi(self)

        #build the therory widget
        self.thParamTable.setIndentation(0)
        self.thParamTable.setColumnCount(3)
        self.thParamTable.setHeaderItem(
            QTreeWidgetItem(["Parameter", "Value", "Error"]))
        # self.thParamTable.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.thParamTable.header().resizeSections(QHeaderView.ResizeToContents)
        self.thParamTable.setAlternatingRowColors(True)
        self.thParamTable.setFrameShape(QFrame.NoFrame)
        self.thParamTable.setFrameShadow(QFrame.Plain)
        self.thParamTable.setEditTriggers(self.thParamTable.NoEditTriggers)

        self.thTextBox.setReadOnly(True)
        self.thTextBox.setOpenExternalLinks(True)
        self.thTextBox.setContextMenuPolicy(Qt.CustomContextMenu)
        self.thTextBox.customContextMenuRequested.connect(self.thtextbox_context_menu)

        self.thread_calc_busy = False
        self.thread_fit_busy = False

        # Setup Theory Parameters Dialog
        self.fittingoptionsdialog = QDialog()
        self.fittingoptionsdialog.ui = Ui_Dialog()
        self.fittingoptionsdialog.ui.setupUi(self.fittingoptionsdialog)
        self.populate_default_minimization_options()

        # Setup Error Calculation Options
        self.errorcalculationdialog = QDialog()
        self.errorcalculationdialog.ui = errorcalculationoptions.Ui_Dialog()
        self.errorcalculationdialog.ui.setupUi(self.errorcalculationdialog)
        self.populate_default_error_calculation_options()

        connection_id = self.thParamTable.itemDoubleClicked.connect(
            self.onTreeWidgetItemDoubleClicked)
        connection_id = self.thParamTable.itemChanged.connect(
            self.handle_parameterItemChanged)

    def populate_default_minimization_options(self):
        dvalidator = QDoubleValidator()
        ivalidator = QIntValidator()
        # LEAST-SQUARES LOCAL MIN
        self.fittingoptionsdialog.ui.LSftollineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.LSxtollineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.LSgtollineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.LSf_scalelineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.LSmax_nfevlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.LSmethodcomboBox.setCurrentIndex(self.fittingoptionsdialog.ui.LSmethodcomboBox.findText(self.LSmethod))
        self.fittingoptionsdialog.ui.LSjaccomboBox.setCurrentIndex(self.fittingoptionsdialog.ui.LSjaccomboBox.findText(self.LSjac))
        self.fittingoptionsdialog.ui.LSftollineEdit.setText('%g'%self.LSftol)
        self.fittingoptionsdialog.ui.LSxtollineEdit.setText('%g'%self.LSxtol)
        self.fittingoptionsdialog.ui.LSgtollineEdit.setText('%g'%self.LSgtol)
        self.fittingoptionsdialog.ui.LSlosscomboBox.setCurrentIndex(self.fittingoptionsdialog.ui.LSlosscomboBox.findText(self.LSloss))
        self.fittingoptionsdialog.ui.LSf_scalelineEdit.setText('%g'%self.LSf_scale)
        self.fittingoptionsdialog.ui.LSmax_nfevlineEdit.setText('100')
        # BASIN HOPPING
        self.fittingoptionsdialog.ui.basinniterlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.basinTlineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.basinstepsizelineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.basinintervallineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.basinniter_successlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.basinseedlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.basinniterlineEdit.setText('%d'%self.basinniter)
        self.fittingoptionsdialog.ui.basinTlineEdit.setText('%g'%self.basinT)
        self.fittingoptionsdialog.ui.basinstepsizelineEdit.setText('%g'%self.basinstepsize)
        self.fittingoptionsdialog.ui.basinintervallineEdit.setText('%d'%self.basininterval)
        self.fittingoptionsdialog.ui.basinniter_successlineEdit.setText('30')
        self.fittingoptionsdialog.ui.basinseedlineEdit.setText('4398495')
        # DUAL ANNEALING
        self.fittingoptionsdialog.ui.annealmaxiterlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.annealinitial_templineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.annealrestart_temp_ratiolineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.annealvisitlineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.annealacceptlineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.annealmaxfunlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.annealseedlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.annealmaxiterlineEdit.setText('%d'%self.annealmaxiter)
        self.fittingoptionsdialog.ui.annealinitial_templineEdit.setText('%g'%self.annealinitial_temp)
        self.fittingoptionsdialog.ui.annealrestart_temp_ratiolineEdit.setText('%g'%self.annealrestart_temp_ratio)
        self.fittingoptionsdialog.ui.annealvisitlineEdit.setText('%g'%self.annealvisit)
        self.fittingoptionsdialog.ui.annealacceptlineEdit.setText('%g'%self.annealaccept)
        self.fittingoptionsdialog.ui.annealmaxfunlineEdit.setText('%d'%self.annealmaxfun)
        self.fittingoptionsdialog.ui.annealseedlineEdit.setText('4389439')
        # DIFFERENTIAL EVOLUTION
        self.fittingoptionsdialog.ui.diffevolmaxiterlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.diffevolpopsizelineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.diffevoltollineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.diffevolmutationAlineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.diffevolmutationBlineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.diffevolrecombinationlineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.diffevolseedlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.diffevolatollineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.diffevolstrategycomboBox.setCurrentIndex(self.fittingoptionsdialog.ui.diffevolstrategycomboBox.findText(self.diffevolstrategy))
        self.fittingoptionsdialog.ui.diffevolmaxiterlineEdit.setText('%d'%self.diffevolmaxiter)
        self.fittingoptionsdialog.ui.diffevolpopsizelineEdit.setText('%d'%self.diffevolpopsize)
        self.fittingoptionsdialog.ui.diffevoltollineEdit.setText('%g'%self.diffevoltol)
        self.fittingoptionsdialog.ui.diffevolmutationAlineEdit.setText('%g'%self.diffevolmutation[0])
        self.fittingoptionsdialog.ui.diffevolmutationBlineEdit.setText('%g'%self.diffevolmutation[1])
        self.fittingoptionsdialog.ui.diffevolrecombinationlineEdit.setText('%g'%self.diffevolrecombination)
        self.fittingoptionsdialog.ui.diffevolseedlineEdit.setText('4389439')
        self.fittingoptionsdialog.ui.diffevolinitcomboBox.setCurrentIndex(self.fittingoptionsdialog.ui.diffevolinitcomboBox.findText(self.diffevolinit))
        self.fittingoptionsdialog.ui.diffevolatollineEdit.setText('%g'%self.diffevolatol)
        # SHGO
        self.fittingoptionsdialog.ui.SHGOnlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.SHGOiterslineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.SHGOmaxfevlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.SHGOf_minlineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.SHGOf_tollineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.SHGOmaxiterlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.SHGOmaxevlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.SHGOmaxtimelineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.SHGOminhgrdlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.SHGOnlineEdit.setText('%d'%self.SHGOn)
        self.fittingoptionsdialog.ui.SHGOiterslineEdit.setText('%d'%self.SHGOiters)
        self.fittingoptionsdialog.ui.SHGOf_tollineEdit.setText('%g'%self.SHGOf_tol)
        # Brute Force
        self.fittingoptionsdialog.ui.BruteNslineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.BruteNslineEdit.setText('%d'%self.BruteNs)

    def populate_default_error_calculation_options(self):
        # ERROR CALCULATION METHOD
        if self.errormethod == ErrorCalculationMethod.View1:
            self.errorcalculationdialog.ui.View1radioButton.setChecked(True)
        elif self.errormethod == ErrorCalculationMethod.RawData:
            self.errorcalculationdialog.ui.RawDataradioButton.setChecked(True)
        elif self.errormethod == ErrorCalculationMethod.AllViews:
            self.errorcalculationdialog.ui.AllViewsradioButton.setChecked(True)
        self.errorcalculationdialog.ui.NormalizecheckBox.setChecked(self.normalizebydata)

    def thtextbox_context_menu(self):
        """Custom contextual menu for the theory textbox"""
        menu = self.thTextBox.createStandardContextMenu()
        menu.addSeparator()
        menu.addAction("Increase Font Size", lambda: self.change_thtextbox_fontsize(1.25))
        menu.addAction("Deacrease Font Size", lambda: self.change_thtextbox_fontsize(0.8))
        menu.addAction("Clear Text", self.thTextBox.clear)
        menu.exec_(QCursor.pos())

    def change_thtextbox_fontsize(self, factor):
        """Change the thTextBox font size by a factor `factor` """
        font = self.thTextBox.currentFont()
        if factor < 1:
            font_size = ceil(font.pointSize() * factor)
        else:
            font_size = floor(font.pointSize() * factor)
        font.setPointSize(font_size)
        self.thTextBox.document().setDefaultFont(font)

    def set_extra_data(self, extra_data):
        """set the extra data dict at loading, redefined in Child class if needed"""
        self.extra_data = extra_data

    def get_extra_data(self):
        """get the extra data dict before saving (defined in Child class if needed)"""
        pass

    def theory_buttons_disabled(self, state):
        """Disable theory button inside the theory"""
        pass

    def handle_actionCalculate_Theory(self):
        if self.thread_calc_busy:
            return
        self.thread_calc_busy = True
        #disable buttons
        self.parent_dataset.actionNew_Theory.setDisabled(True) #only needed for theories using shared libraries
        self.theory_buttons_disabled(True)

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

    def end_thread_calc(self):
        if CmdBase.calcmode == CalcMode.multithread:
            try:
                self.thread_calc.quit()
            except:
                pass
        else:
            self.update_parameter_table()
            for file in self.theory_files(
            ):  #copy theory data to the plot series
                tt = self.tables[file.file_name_short]
                for nx in range(self.parent_dataset.nplots):
                    view = self.parent_dataset.parent_application.multiviews[
                        nx]
                    x, y, success = view.view_proc(tt, file.file_parameters)
                    for i in range(tt.MAX_NUM_SERIES):
                        if (i < view.n):
                            tt.series[nx][i].set_data(x[:, i], y[:, i])

            self.parent_dataset.parent_application.update_Qplot()
        self.thread_calc_busy = False
        #enable buttons
        self.parent_dataset.actionNew_Theory.setDisabled(False)
        self.theory_buttons_disabled(False)
        self.parent_dataset.end_of_computation(self.name)

    def handle_actionMinimize_Error(self):
        """Minimize the error

        [description]
        """
        if self.thread_fit_busy:
            return
        self.thread_fit_busy = True
        #disable buttons
        self.parent_dataset.actionNew_Theory.setDisabled(True) #only needed for theories using shared libraries
        self.theory_buttons_disabled(True)

        if CmdBase.calcmode == CalcMode.multithread:
            self.worker = CalculationThread(
                self.do_fit,
                "",
            )
            self.worker.sig_done.connect(self.end_thread_fit)
            self.thread_fit = QThread()
            self.worker.moveToThread(self.thread_fit)
            self.thread_fit.started.connect(self.worker.work)
            self.thread_fit.start()
        elif CmdBase.calcmode == CalcMode.singlethread:
            self.do_fit("")
            self.end_thread_fit()

    def end_thread_fit(self):
        if CmdBase.calcmode == CalcMode.multithread:
            try:
                self.thread_fit.quit()
            except:
                pass
        self.update_parameter_table()
        self.parent_dataset.parent_application.update_Qplot()
        self.thread_fit_busy = False
        #enable buttons
        self.parent_dataset.actionNew_Theory.setDisabled(False)
        self.theory_buttons_disabled(False)
        self.parent_dataset.end_of_computation(self.name)

    def copy_parameters(self):
        text = ""
        for param in self.parameters:
            p = self.parameters[param]
            text += "%s\t%g\n"%(p.name,p.value)
        QApplication.clipboard().setText(text)

    def paste_parameters(self):
        text = QApplication.clipboard().text()
        if text == '':
            return
        rows = text.splitlines() # split on newlines
        for i in range(len(rows)):
            cols = rows[i].split() # split on whitespaces
            if (len(cols)==2):
                if (cols[0] in self.parameters):
                    message, success = self.set_param_value(cols[0], cols[1])
        self.update_parameter_table()
        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()

    def update_parameter_table(self):
        """Update the theory parameter table

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
                item.setToolTip(0, p.description)
        self.thParamTable.header().resizeSections(QHeaderView.ResizeToContents)

    def onTreeWidgetItemDoubleClicked(self, item, column):
        """Start editing text when a table cell is double clicked
        Or edit all parameters fittingoptionsdialog if parameter name is double clicked

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
            # thcurrent = self.parent_dataset.TheorytabWidget.currentWidget()
            # thcurrent.editItem(item, column)

    def handle_parameterItemChanged(self, item, column):
        """Modify parameter values when changed in the theory table

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
        else:
            self.update_parameter_table()
            if self.autocalculate:
                self.parent_dataset.handle_actionCalculate_Theory()

    def Qcopy_modes(self):
        """[summary]

        [description]
        """
        apmng = self.parent_dataset.parent_application.parent_manager
        G, S = apmng.list_theories_Maxwell(th_exclude=self)
        if G:
            d = GetModesDialog(self, G)
            if (d.exec_() and d.btngrp.checkedButton() != None):
                item = d.btngrp.checkedButton().text()
                tau, G0 = G[item]()
                tauinds = (-tau).argsort()
                tau = tau[tauinds]
                G0 = G0[tauinds]
                success = self.set_modes(tau, G0)
                if not success:
                    self.logger.warning("Could not set modes successfully")
                    return
                self.update_parameter_table()
                self.parent_dataset.handle_actionCalculate_Theory()
        else:
            QMessageBox.information(self, 'Import Modes', 'Found no opened theory to import modes from')


    def save_modes(self):
        """Save Maxwell modes to a text file"""
        fpath, _ = QFileDialog.getSaveFileName(self,
                                               "Save Maxwell modes to a text file",
                                               "data/", "Text (*.txt)")
        if fpath == '':
            return

        with open(fpath, 'w') as f:
            times, G, success = self.get_modes()
            if not success:
                self.logger.warning("Could not get modes correctly")
                return

            header = '# Maxwell modes\n'
            header += '# Generated with RepTate v%s %s\n' % (Version.VERSION,
                                                             Version.DATE)
            header += '# At %s on %s\n' % (time.strftime("%X"),
                                           time.strftime("%a %b %d, %Y"))
            f.write(header)

            f.write('\n#number of modes\n')
            n = len(times)
            f.write('%d\n'%n)
            f.write('\n#%4s\t%15s\t%15s\n'%('i','tau_i','G_i'))

            for i in range(n):
                f.write('%5d\t%15g\t%15g\n'%(i+1,times[i],G[i]))

            f.write('\n#end')

        QMessageBox.information(self, 'Success',
                                'Wrote Maxwell modes \"%s\"' % fpath)
