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
"""Module TheoryUCMLaos

Module for the Upper Convected Maxwell model

"""
import numpy as np
from scipy.integrate import ode, odeint
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from PyQt5.QtWidgets import QToolBar, QToolButton, QMenu, QStyle, QSpinBox, QTableWidget, QDialog, QVBoxLayout, QDialogButtonBox, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import Qt
from Theory_rc import *
from enum import Enum
from math import sqrt
from SpreadsheetWidget import SpreadsheetWidget

from TheoryUCM import CLTheoryUCM, GUITheoryUCM


class TheoryUCMLAOS(CmdBase):
    """Multi-mode Upper Convected Maxwell model (see Chapter 1 of :cite:`NLVE-Larson1988`):
    
    .. math::
        \\boldsymbol \\sigma &= \\sum_{i=1}^n G_i \\boldsymbol A_i\\\\
        \\dfrac {\\mathrm D \\boldsymbol  A_i} {\\mathrm D t} &=  \\boldsymbol \\kappa \\cdot \\boldsymbol A_i
        + \\boldsymbol A_i\\cdot \\boldsymbol \\kappa ^T 
         - \dfrac 1 {\\tau_i} (\\boldsymbol A_i - \\boldsymbol I)
    
    * **Functions**
        - Analytical solution in shear
        
          .. math::
            \\eta^+(t) = \\sum_{i=1}^n G_i \\tau_i (1 - \\exp(-t/\\tau_i))
        
        - Analytical solution in uniaxial extension
        
          .. math::
            \\eta^+_\\mathrm E (t) = \\dfrac 1 {\\dot\\varepsilon}
            \\sum_{i=1}^n G_i (A_{xx, i}(t) - A_{yy, i}(t))
        
          with

            .. math::
                A_{xx, i}(t) &= \\dfrac{ 1 - 2 \\dot\\varepsilon\\tau_i 
                \\exp(-(1 - 2 \\dot\\varepsilon\\tau_i) t / \\tau_i) } {1 - 2 \\dot\\varepsilon\\tau_i }\\\\
                A_{yy, i}(t) &= \\dfrac{ 1 + \\dot\\varepsilon\\tau_i 
                \\exp(-(1 + \\dot\\varepsilon\\tau_i)t/\\tau_i) } { 1+ \\dot\\varepsilon\\tau_i}

        where for each mode :math:`i`:
            - :math:`G_i`: weight of mode :math:`i`
            - :math:`\\tau_i`: relaxation time of mode :math:`i`

    * **Parameters**
        [none]

    """
    thname = "UCM"
    description = "Upper-convected Maxwell constitutive equation"
    citations = "Oldroyd J.G., Proc. Roy. Soc. 1950, 200, 523-541"
    doi = "http://dx.doi.org/10.1098/rspa.1950.0035"

    def __new__(cls, name="", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUITheoryUCMLAOS(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryUCMLAOS(
                name, parent_dataset, ax)


class BaseTheoryUCMLAOS:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/NLVE/Theory/theory.html#multi-mode-upper-convected-maxwell-model'
    single_file = False
    thname = TheoryUCMLAOS.thname
    citations = TheoryUCMLAOS.citations
    doi = TheoryUCMLAOS.doi 

    def __init__(self, name="", parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate_UCMLAOS
    
    def calculate_UCMLAOS(self, f=None):
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        times = ft.data[:, 0]

        g0 = float(f.file_parameters["gamma"])
        w = float(f.file_parameters["omega"])
        tt.data[:, 0] = times
        tt.data[:, 1] = g0*np.sin(w*times)

        nmodes = self.parameters["nmodes"].value
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            G = self.parameters["G%02d" % i].value
            tauD = self.parameters["tauD%02d" % i].value
            eta = G*tauD
            tt.data[:, 2] += eta*g0*w*(
                                tauD*w*np.sin(w*times)
                                -np.exp(-times/tauD)
                                +np.cos(w*times))/(1+w**2*tauD**2)


class CLTheoryUCMLAOS(BaseTheoryUCMLAOS, CLTheoryUCM):
    """[summary]
    
    [description]
    """

    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)


class GUITheoryUCMLAOS(BaseTheoryUCMLAOS, GUITheoryUCM):
    """[summary]
    
    [description]
    """

    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        # clear toolbar of elements from GUITheoryUCM
        tb = self.thToolsLayout.itemAt(0).widget()
        tb.clear()

        self.tbutmodes = QToolButton()
        self.tbutmodes.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        self.get_modes_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-broadcasting.png'),
            "Get Modes")
        self.edit_modes_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-edit-file.png'),
            "Edit Modes")
        self.plot_modes_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-scatter-plot.png'),
            "Plot Modes")
        self.save_modes_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-save-Maxwell.png'),
            "Save Modes")
        self.tbutmodes.setDefaultAction(self.get_modes_action)
        self.tbutmodes.setMenu(menu)
        tb.addWidget(self.tbutmodes)

        connection_id = self.get_modes_action.triggered.connect(
            self.get_modes_reptate)
        connection_id = self.edit_modes_action.triggered.connect(
            self.edit_modes_window)
        connection_id = self.plot_modes_action.triggered.connect(
            self.plot_modes_graph)
        connection_id = self.save_modes_action.triggered.connect(
            self.save_modes)