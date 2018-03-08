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
# Copyright (2017): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module TheoryCreatePolyconf

CreatePolyconf file for creating a polymer configuration file using BoB
"""
import os
import numpy as np
from CmdBase import CmdBase, CmdMode
from enum import Enum
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from collections import OrderedDict
import time

import bob_gen_poly # dialog
import bob_ctypes_helper as bch
from PyQt5.QtWidgets import QDialog, QFormLayout, QWidget, QLineEdit, QLabel, QComboBox, QDialogButtonBox, QFileDialog
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QDesktopServices
from PyQt5.QtCore import QUrl, pyqtSignal


class DistributionType(Enum):
    """Type of molecular weight distribution"""
    Monodisperse = 0
    Gaussian = 1
    Log_normal = 2
    Poisson = 3
    Flory = 4

class ArchitectureType(Enum):
    """Type of polymer architecture and expected parameters as input for BoB"""
    
    Linear = [0, 'Dist', 'Mw (g/mol)', 'PDI']
    Star = [1, 'Dist', 'Mw (g/mol)', 'PDI', '', 'Num. arm']
    Asym_Star = [2, 'Dist long', 'Mw long (g/mol)', 'PDI long', '','Dist short', 'Mw short', 'PDI short']
    H = [3,  'Dist side', 'Mw side (g/mol)', 'PDI side', '','Dist cross', 'Mw cross', 'PDI cross']
    Combs_Poisson = [4, 'Dist backbone', 'Mw backbone (g/mol)', 'PDI backbone', '','Dist side', 'Mw side (g/mol)', 'PDI side', '', 'Num. arm']
    Combs_fixed = [5, 'Dist backbone', 'Mw backbone (g/mol)', 'PDI backbone', '','Dist side', 'Mw side (g/mol)', 'PDI side', '', 'Num. arm']
    Combs_coupled = [6, 'Dist backbone', 'Mw backbone (g/mol)', 'PDI backbone', '','Dist side', 'Mw side (g/mol)', 'PDI side', '', 'Num. arm']
    Cayley_tree = [10, 'Num. generation', '', 'Dist gen0', 'Mw gen0 (g/mol)', 'PDI gen0']
    Cayley_lin = [11, 'Num. generation', '', 'Dist gen0', 'Mw gen0 (g/mol)', 'PDI gen0']
    Cayley_star4 = [12, 'Num. generation', '', 'Dist gen0', 'Mw gen0 (g/mol)', 'PDI gen0']
    MPE_numav = [20, 'Mw (g/mol)', 'Branch/molecule']
    MPE_wtav = [21, 'Mw (g/mol)', 'Branch/molecule']
    GEL_wtav = [25, 'Mn (g/mol)', 'Up Branch. proba.']
    # Prototype = [40,]
    # From_file = [60, 'file name']

class TheoryCreatePolyconf(CmdBase):
    """[summary]
    
    [description]
    """
    thname = 'CreatePolyconfTheory'
    description = 'CreatePolyconf Theory'
    citations = ''

    def __new__(cls, name='ThCreatePolyconf', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'ThCreatePolyconf'})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUITheoryCreatePolyconf(name, parent_dataset, axarr) if (
            CmdBase.mode == CmdMode.GUI) else CLTheoryCreatePolyconf(
                name, parent_dataset, axarr)


class BaseTheoryCreatePolyconf:
    """[summary]
    
    [description]
    """
    #help_file = ''
    single_file = False  # False if the theory can be applied to multiple files simultaneously
    signal_param_dialog = pyqtSignal(object)

    def __init__(self,
                 name='ThCreatePolyconf',
                 parent_dataset=None,
                 axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'ThCreatePolyconf'})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate  # main theory function
        self.has_modes = False  # True if the theory has modes
        self.signal_param_dialog.connect(self.launch_param_dialog)

    def get_modes(self):
        """[summary]
        
        [description]
        
        Returns:
            - [type] -- [description]
        """
        pass

    def do_error(self, line=""):
        """[summary]
        
        [description]
        
        Returns:
            - [type] -- [description]
        """
        pass

    def set_modes(self):
        """[summary]
        
        [description]
        
        Arguments:

        """
        pass

    def destructor(self):
        """[summary]
        
        [description]
        
        Arguments:

        """
        pass

    def calculate(self, f=None):
        """CreatePolyconf function that returns the square of y
        
        [description]
        
        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        #show form
        self.success_dialog = None
        self.signal_param_dialog.emit(self)
        while self.success_dialog is None:  # wait for the end of QDialog
            time.sleep(
                0.5
            )  # TODO: find a better way to wait for the dialog thread to finish
        if not self.success_dialog:
            self.Qprint('Operation canceled')
            return



class CLTheoryCreatePolyconf(BaseTheoryCreatePolyconf, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self,
                 name='ThCreatePolyconf',
                 parent_dataset=None,
                 axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'ThCreatePolyconf'})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # This class usually stays empty


class GUITheoryCreatePolyconf(BaseTheoryCreatePolyconf, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self,
                 name='ThCreatePolyconf',
                 parent_dataset=None,
                 axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'ThCreatePolyconf'})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.ncomponent = 1
        self.trash_indices = []
        self.dict_component = OrderedDict()
        self.setup_dialog()

    def setup_dialog(self):
        """Create the dialog to setup the polymer configuration"""
        # create form
        self.dialog = QDialog(self)
        self.dialog.ui = bob_gen_poly.Ui_Dialog()
        self.dialog.ui.setupUi(self.dialog)
        self.d = self.dialog.ui
        self.d.polymer_tab.setTabsClosable(True)
        # connect close tab
        self.d.polymer_tab.tabCloseRequested.connect(self.handle_close_polymer_tab)
        # connect button Apply
        self.d.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.handle_apply_button)
        # connect button Help
        self.d.buttonBox.button(QDialogButtonBox.Help).clicked.connect(self.handle_help_button)
        # connect button OK
        # self.d.buttonBox.accepted.connect(self.accept_)
        # connect button Add component
        self.d.add_button.clicked.connect(self.handle_add_component)
        # connect combobox architecture type
        self.d.cb_type.currentTextChanged.connect(self.handle_architecture_type_changed)
        # fill combobox
        for e in ArchitectureType:
            self.d.cb_type.addItem(e.name)

    def handle_apply_button(self):
        """When Apply button of dialog box is clicked"""
        tb = self.d.text_box
        # remove all current text
        tb.clear()
        #1 memory line
        tb.append("%s %s" % (self.d.n_polymers.text(), self.d.n_segments.text()))
        #2 alpha (not used)
        tb.append("1.0")
        #3 "1" for BoB 'compatibility'
        tb.append("1")
        #4 M0, Ne, (density not used)
        tb.append("%s %s 0" % (self.d.m0.text(), self.d.ne.text()))
        #5 tau_e, T (not used)
        tb.append("0 0")
        #6 number of component(s) in blend
        tb.append("%s" % len(self.dict_component))
        
        #7.. the rest of the lines is specific to the architecture
        tot_ratio = self.sum_ratios() # summ all components ratios to define weights

        for pol_dict in self.dict_component.values():
            pol_type_list = ArchitectureType[pol_dict["type"]].value  # architecture type value
            #8.. weight
            try:
                w = float(pol_dict["Ratio"].text()) / tot_ratio
            except:
                w = "ERROR"
            tb.append("%s" % w)
            #9.. num. polymer and type
            npol = pol_dict["Num. of polymers"].text()
            type_number = pol_type_list[0]
            tb.append("%s %s" % (npol, type_number))

            if type_number in [10, 11, 12]:  # Cayley tree: handle varible number of generations
                ngen = pol_dict["Num. generation"]
                text = "%s\n" % ngen
                for i in range(ngen + 1):
                    text += self.poly_param_text(pol_dict, "Dist gen%d" % i)
                    text += self.poly_param_text(pol_dict, "Mw gen%d (g/mol)" % i)
                    text += self.poly_param_text(pol_dict, "PDI gen%d" % i).rstrip()  # remove whitespace on right side
                    if i < ngen:
                        text += "\n"
            else:
                text = ""
                for attr in pol_type_list[1:]:  # go over all attributes of the architecture type
                    text += self.poly_param_text(pol_dict, attr)

            tb.append(text.rstrip())  # remove whitespace on right side
        
        # set current tab to the Text box "result"
        self.d.tabWidget.setCurrentIndex(2)

    def poly_param_text(self, pol_dict, attr):
        if attr == "":
            text = "\n"
        else:
            try:
                val =  pol_dict[attr].text()  # for QLineEdit (Mw, PDI, narm)
            except:
                val =  DistributionType[pol_dict[attr].currentText()].value  # for Dist QComboBox
            text = "%s " % val
        return text

    def sum_ratios(self):
        s = 0.0
        for pol_dict in self.dict_component.values():
            try: 
                s += float(pol_dict["Ratio"].text())
            except ValueError:
                print("ERROR in Ratio conversion")
        if s == 0.0:
            s = 1.0
        return s


    def handle_help_button(self):
        """When Help button of dialog box is clicked"""
        bob_manual_pdf = 'docs%ssource%smanual%sApplications%sReact%sbob2.3.pdf' % ((os.sep,) * 5)
        QDesktopServices.openUrl(QUrl.fromLocalFile(bob_manual_pdf))

    # def accept_(self):
    #     """When OK button of dialog box is clicked"""
    #     pass

    def handle_architecture_type_changed(self, current_name):
        """Activate/Desactivate the ngeneration widgets.
        Called when the combobox 'Architecture' is changed"""
        is_cayley = "Cayley" in current_name
        self.d.ngeneration_label.setDisabled(not is_cayley)
        self.d.sb_ngeneration.setDisabled(not is_cayley)

    def handle_add_component(self):
        """Add a tab with new polymer component"""
        pol_type = self.d.cb_type.currentText()
        # re-use numbering of closed tabs (if any)
        if self.trash_indices:
            ind = min(self.trash_indices)
            self.trash_indices.remove(ind)
            pol_id = "%s%s" % (pol_type, ind)
        else:
            pol_id = "%s%s" % (pol_type, self.ncomponent)
            self.ncomponent += 1
        # define a new tab widget
        tab_widget = self.create_new_tab(pol_id, pol_type) 
        index = self.d.polymer_tab.addTab(tab_widget, pol_id)
        # set new tab as active one
        self.d.polymer_tab.setCurrentIndex(index)  

    def create_new_tab(self, pol_id, pol_type):
        """Create a form to set the new values of the BoB binning parameters"""
        widget = QWidget(self)
        layout = QFormLayout()
        pol_dict = OrderedDict([("type", pol_type),])  # Arch. type number

        val_double = QDoubleValidator()
        val_double.setBottom(0)  #set smalled double allowed in the form

        e1 = QLineEdit()
        e1.setValidator(val_double)
        e1.setMaxLength(6)
        e1.setText(self.d.ratio.text())
        layout.addRow(QLabel("Ratio"), e1)
        pol_dict["Ratio"] = e1
        
        e2 = QLineEdit()
        e2.setValidator(val_double)
        e2.setText(self.d.number.text())
        layout.addRow(QLabel("Num. of polymers"), e2)
        pol_dict["Num. of polymers"] = e2
        
        self.set_extra_lines(pol_type, layout, pol_dict)
        self.dict_component[pol_id] = pol_dict

        widget.setLayout(layout)
        return widget

    def set_extra_lines(self, pol_type, layout, pol_dict):
        """Extra parameters related to the polymer architecture"""

        pol_attr = ArchitectureType[pol_type].value # return a list with the expected input parameters
        for attr in pol_attr[1:]: 
            if "Num. generation" in attr:
                ngen = self.d.sb_ngeneration.value()
                pol_dict["Num. generation"] = ngen
                for i in range(ngen + 1):
                    self.add_new_qline("Mw gen%d (g/mol)" % i, "1e4", layout, pol_dict)
                    self.add_new_qline("PDI gen%d" % i, "1.2", layout, pol_dict)
                    self.add_cb_distribution("Dist gen%d" % i, layout, pol_dict)
                break
            elif "arm" in attr:
                if pol_attr[0] in [4, 6]:
                    # comb Poisson distribution (double)
                    self.add_new_qline(attr, "4.2", layout, pol_dict)
                else:
                    #star or comb with fixed number of arms (integer)
                    self.add_new_qline(attr, "3", layout, pol_dict, QIntValidator())
            if "Mw" in attr:
                # add Mw line
                self.add_new_qline(attr, "1e4", layout, pol_dict)
            elif "PDI" in attr:
                #add PDI line
                self.add_new_qline(attr, "1.2", layout, pol_dict)
            elif "Dist" in attr:
                # add distribution combobox
                self.add_cb_distribution(attr, layout, pol_dict)
            elif "/mol" in attr:
                # add branch/molecule line
                self.add_new_qline(attr, "0.1", layout, pol_dict)
            elif "proba" in attr:
                # add branching proba line
                self.add_new_qline(attr, "0.2", layout, pol_dict)
            elif attr == '':
                continue


    def add_new_qline(self, name, default_val, layout, pol_dict, validator=QDoubleValidator()):
        """Add a new line with a QLabel in form"""
        validator.setBottom(0)  #set smalled double allowed in the form
        e = QLineEdit()
        e.setValidator(validator)
        e.setText("%s" % default_val)
        layout.addRow(QLabel(name), e)
        pol_dict[name] = e

    def add_cb_distribution(self, name, layout, pol_dict):
        """Add a new line with a QComboBox in form"""
        cb = QComboBox()
        for dtype in DistributionType: # list the distribution names
            cb.addItem(dtype.name)
        cb.setCurrentIndex(2) # log-normal by default
        layout.addRow(QLabel(name), cb)
        pol_dict[name] = cb
    
    def handle_close_polymer_tab(self, index):
        """Close a tab and delete dictionary entry"""
        name = self.d.polymer_tab.tabText(index)
        ind = int(''.join(c for c in name if c.isdigit())) #get the number
        del self.dict_component[name]
        self.d.polymer_tab.removeTab(index)
        self.trash_indices.append(ind)

    def launch_param_dialog(self):
        """Overides QTheory method to avoid multithread"""
        if self.dialog.exec_():
            self.handle_apply_button()
            
            # create temporary file for BoB input
            # get the directory path of current file
            dir_path = os.path.dirname(os.path.realpath(__file__))
            temp_dir = dir_path + '%stemp%s' % ((os.sep,)*2)
            #create temp folder if does not exist
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            temp_file = temp_dir + 'bob_inp.dat'
            self.create_input_param_file(temp_file)
            
            # ask where to save the polymer config file
            polyconf_file_out = self.get_file_name()
            if polyconf_file_out is not None:
                # run BoB main
                argv = ["./bob", "-i", temp_file, "-c", polyconf_file_out]
                bch.run_bob_main(argv)

                self.Qprint("Polymer configuration written in %s" % polyconf_file_out)
                self.success_dialog = True
                return

        self.success_dialog = False

    def create_input_param_file(self, temp_file):
        with open(temp_file, 'w') as tmp:
            tmp.write(str(self.d.text_box.toPlainText()))

        
    def get_file_name(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_start = "data/React/"
        dilogue_name = "Save BoB Polymer Configuration"
        ext_filter = "Data Files (*.dat)"
        out_file = QFileDialog.getSaveFileName(
            self, dilogue_name, dir_start, options=options)
        if out_file[0] == "":
            self.Qprint('Invalid filename')
            return None
        else:
            return out_file[0]
