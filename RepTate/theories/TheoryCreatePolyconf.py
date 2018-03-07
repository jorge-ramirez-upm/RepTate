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
import numpy as np
from CmdBase import CmdBase, CmdMode
from enum import Enum
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from collections import OrderedDict

import bob_gen_poly
from PyQt5.QtWidgets import QDialog, QFormLayout, QWidget, QLineEdit, QLabel, QComboBox
from PyQt5.QtGui import QIntValidator, QDoubleValidator


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
        self.parameters['param1'] = Parameter(
            name='param1',
            value=1,
            description='parameter 1',
            type=ParameterType.real,
            opt_type=OptType.const)

    def get_modes(self):
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

    # def do_calculate(self, line=''):
    #     """Redefinition of 'do_calculate()' """
    #     if self.dialog.exec_():
    #         print("SUCCESS")
    #     print("DONE")
    
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
        # connect button
        self.d.add_button.clicked.connect(self.handle_add_component)
        # connect combobox architecture type
        self.d.cb_type.currentTextChanged.connect(self.handle_architecture_type_changed)
        # fill combobox
        for e in ArchitectureType:
            self.d.cb_type.addItem(e.name)

    def handle_architecture_type_changed(self, current_name):
        """Called when the combobox 'Architecture' is changed"""
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
        lines = []

        val_double = QDoubleValidator()
        val_double.setBottom(0)  #set smalled double allowed in the form

        e1 = QLineEdit()
        e1.setValidator(val_double)
        e1.setMaxLength(6)
        e1.setText(self.d.ratio.text())
        layout.addRow(QLabel("Ratio"), e1)
        lines.append(e1)
        
        e2 = QLineEdit()
        e2.setValidator(val_double)
        e2.setText(self.d.number.text())
        layout.addRow(QLabel("Num. of polymers"), e2)
        lines.append(e2)
        
        self.set_extra_lines(pol_type, layout, lines)
        self.dict_component[pol_id] = lines

        widget.setLayout(layout)
        return widget

    def set_extra_lines(self, pol_type, layout, lines):
        """Extra parameters related to the polymer architecture"""

        pol_attr = ArchitectureType[pol_type].value # return a list with the expected input parameters
        for attr in pol_attr[1:]: 
            if "generation" in attr:
                ngen = self.d.sb_ngeneration.value()
                for i in range(ngen + 1):
                    self.add_new_qline("Mw gen%d (g/mol)" % i, "1e4", layout, lines)
                    self.add_new_qline("PDI gen%d" % i, "1.2", layout, lines)
                    self.add_cb_distribution("Dist gen%d" % i, layout, lines)
                break
            elif "arm" in attr:
                if pol_attr[0] in [4, 6]:
                    # comb Poisson distribution (double)
                    self.add_new_qline(attr, "4.2", layout, lines)
                else:
                    #star or comb with fixed number of arms (integer)
                    self.add_new_qline(attr, "3", layout, lines, QIntValidator())
            if "Mw" in attr:
                # add Mw line
                self.add_new_qline(attr, "1e4", layout, lines)
            elif "PDI" in attr:
                #add PDI line
                self.add_new_qline(attr, "1.2", layout, lines)
            elif "Dist" in attr:
                # add distribution combobox
                self.add_cb_distribution(attr, layout, lines)
            elif "/mol" in attr:
                # add branch/molecule line
                self.add_new_qline(attr, "0.1", layout, lines)
            elif "proba" in attr:
                # add branching proba line
                self.add_new_qline(attr, "0.2", layout, lines)
            elif attr == '':
                continue


    def add_new_qline(self, name, default_val, layout, lines, validator=QDoubleValidator()):
        """Add a new line with a QLabel in form"""
        validator.setBottom(0)  #set smalled double allowed in the form
        e = QLineEdit()
        e.setValidator(validator)
        e.setText("%s" % default_val)
        layout.addRow(QLabel(name), e)
        lines.append(e)


    def add_cb_distribution(self, name, layout, lines):
        """Add a new line with a QComboBox in form"""
        cb = QComboBox()
        for dtype in DistributionType: # list the distribution names
            cb.addItem(dtype.name)
        cb.setCurrentIndex(2) # log-normal by default
        layout.addRow(QLabel(name), cb)
        lines.append(cb)
    
    def handle_close_polymer_tab(self, index):
        """Close a tab and delete dictionary entry"""
        name = self.d.polymer_tab.tabText(index)
        ind = int(''.join(c for c in name if c.isdigit())) #get the number
        del self.dict_component[name]
        self.d.polymer_tab.removeTab(index)
        self.trash_indices.append(ind)

    def handle_actionCalculate_Theory(self):
        """Overides QTheory method to avoid multithread"""
        if self.dialog.exec_():
            print("SUCCESS")
        