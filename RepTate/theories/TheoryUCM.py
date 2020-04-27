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
"""Module TheoryUCM

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
from ApplicationLAOS import CLApplicationLAOS, GUIApplicationLAOS

class FlowMode(Enum):
    """Defines the flow geometry used
    
    Parameters can be:
        - shear: Shear flow
        - uext: Uniaxial extension flow
    """
    shear = 0
    uext = 1


class EditModesDialog(QDialog):
    def __init__(self, parent=None, times=None, G=None, MAX_MODES=0):
        super(EditModesDialog, self).__init__(parent)

        self.setWindowTitle("Edit Maxwell modes")
        layout = QVBoxLayout(self)
        nmodes = len(times)

        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, MAX_MODES)  # min and max number of modes
        self.spinbox.setSuffix(" modes")
        self.spinbox.setValue(nmodes)  #initial value
        layout.addWidget(self.spinbox)

        self.table = SpreadsheetWidget()  #allows copy/paste
        self.table.setRowCount(nmodes)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["tauD", "G"])
        for i in range(nmodes):
            tau = "%g" % times[i]
            mod = "%g" % G[i]
            self.table.setItem(i, 0, QTableWidgetItem(tau))
            self.table.setItem(i, 1, QTableWidgetItem(mod))

        layout.addWidget(self.table)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged)

    def handle_spinboxValueChanged(self, value):
        nrow_old = self.table.rowCount()
        self.table.setRowCount(value)
        for i in range(nrow_old, value):  #create extra rows with defaut values
            self.table.setItem(i, 0, QTableWidgetItem("10"))
            self.table.setItem(i, 1, QTableWidgetItem("1000"))


class TheoryUCM(CmdBase):
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
    citations = ["Oldroyd J.G., Proc. Roy. Soc. 1950, 200, 523-541"]
    doi = ["http://dx.doi.org/10.1098/rspa.1950.0035"]

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
        return GUITheoryUCM(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryUCM(
                name, parent_dataset, ax)


class BaseTheoryUCM:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/NLVE/Theory/theory.html#multi-mode-upper-convected-maxwell-model'
    single_file = False
    thname = TheoryUCM.thname
    citations = TheoryUCM.citations
    doi = TheoryUCM.doi 

    def __init__(self, name="", parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate_UCM
        self.has_modes = True
        self.parameters["nmodes"] = Parameter(
            name="nmodes",
            value=2,
            description="Number of modes",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False)

        for i in range(self.parameters["nmodes"].value):
            self.parameters["G%02d" % i] = Parameter(
                name="G%02d" % i,
                value=1000.0,
                description="Modulus of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.nopt,
                display_flag=False,
                min_value=0)
            self.parameters["tauD%02d" % i] = Parameter(
                name="tauD%02d" % i,
                value=10.0,
                description="Terminal time of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.nopt,
                display_flag=False,
                min_value=0)

        self.MAX_MODES = 40
        self.init_flow_mode()

    def init_flow_mode(self):
        """Find if data files are shear or extension"""
        try:
            f = self.theory_files()[0]
            if f.file_type.extension == 'shear':
                self.flow_mode = FlowMode.shear
            else:
                self.flow_mode = FlowMode.uext
        except Exception as e:
            print("in UCM init:", e)
            self.flow_mode = FlowMode.shear  #default mode: shear

    def get_modes(self):
        """Get the values of Maxwell Modes from this theory"""
        nmodes = self.parameters["nmodes"].value
        tau = np.zeros(nmodes)
        G = np.zeros(nmodes)
        for i in range(nmodes):
            tau[i] = self.parameters["tauD%02d" % i].value
            G[i] = self.parameters["G%02d" % i].value
        return tau, G, True

    def set_modes(self, tau, G):
        """Set the values of Maxwell Modes from another theory"""
        nmodes = len(tau)
        self.set_param_value("nmodes", nmodes)
        for i in range(nmodes):
            self.set_param_value("tauD%02d" % i, tau[i])
            self.set_param_value("G%02d" % i, G[i])
        return True

    def sigma_xy_shear(self, p, times):
        """Upper Convected Maxwell model in shear.
        Returns XY component of stress tensor
        
        [description]
        
        Arguments:
            - p {array} -- p = [G, tauD, gamma_dot] 
            - times {array} -- time
        """
        G, tauD, gd = p

        return G * gd * tauD * (1 - np.exp(-times / tauD))

    def n1_uext(self, p, times):
        """Upper Convected Maxwell model in uniaxial extension.
        Returns N1 = (XX -YY) component of stress tensor
        
        [description]
        
        Arguments:
            - p {array} -- p = [G, tauD, epsilon_dot] 
            - times {array} -- time
        """
        G, tauD, ed = p
        w = tauD * ed
        sxx = (1 - 2 * w * np.exp(-(1 - 2 * w) * times / tauD)) / (1 - 2 * w)
        syy = (1 + w * np.exp(-(1 + w) * times / tauD)) / (1 + w)

        return G * (sxx - syy)

    def calculate_UCM(self, f=None):
        """[summary]
        
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
        times = ft.data[:, 0]

        tt.data[:, 0] = times

        flow_rate = float(f.file_parameters["gdot"])
        nmodes = self.parameters["nmodes"].value
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            G = self.parameters["G%02d" % i].value
            tauD = self.parameters["tauD%02d" % i].value

            p = [G, tauD, flow_rate]

            if self.flow_mode == FlowMode.shear:
                tt.data[:, 1] += self.sigma_xy_shear(p, times)
            elif self.flow_mode == FlowMode.uext:
                tt.data[:, 1] += self.n1_uext(p, times)

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

    def set_param_value(self, name, value):
        """[summary]
        
        [description]
        
        Arguments:
            - name {[type]} -- [description]
            - value {[type]} -- [description]
        """
        if (name == "nmodes"):
            oldn = self.parameters["nmodes"].value
        message, success = super(BaseTheoryUCM, self).set_param_value(
            name, value)
        if not success:
            return message, success
        if (name == "nmodes"):
            for i in range(self.parameters["nmodes"].value):
                self.parameters["G%02d" % i] = Parameter(
                    name="G%02d" % i,
                    value=1000.0,
                    description="Modulus of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.nopt,
                    display_flag=False,
                    min_value=0)
                self.parameters["tauD%02d" % i] = Parameter(
                    name="tauD%02d" % i,
                    value=10.0,
                    description="Terminal time of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.nopt,
                    display_flag=False,
                    min_value=0)

            if (oldn > self.parameters["nmodes"].value):
                for i in range(self.parameters["nmodes"].value, oldn):
                    del self.parameters["G%02d" % i]
                    del self.parameters["tauD%02d" % i]
        return '', True


class CLTheoryUCM(BaseTheoryUCM, Theory):
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
        if isinstance(parent_dataset.parent_application, CLApplicationLAOS):
            self.function = self.calculate_UCMLAOS

class GUITheoryUCM(BaseTheoryUCM, QTheory):
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

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))

        if not isinstance(parent_dataset.parent_application, GUIApplicationLAOS):
            self.tbutflow = QToolButton()
            self.tbutflow.setPopupMode(QToolButton.MenuButtonPopup)
            menu = QMenu()
            self.shear_flow_action = menu.addAction(
                QIcon(':/Icon8/Images/new_icons/icon-shear.png'),
                "Shear Flow")
            self.extensional_flow_action = menu.addAction(
                QIcon(':/Icon8/Images/new_icons/icon-uext.png'),
                "Extensional Flow")
            if self.flow_mode == FlowMode.shear:
                self.tbutflow.setDefaultAction(self.shear_flow_action)
            else:
                self.tbutflow.setDefaultAction(self.extensional_flow_action)
            self.tbutflow.setMenu(menu)
            tb.addWidget(self.tbutflow)

            connection_id = self.shear_flow_action.triggered.connect(
                self.select_shear_flow)
            connection_id = self.extensional_flow_action.triggered.connect(
                self.select_extensional_flow)
        else:
            self.function = self.calculate_UCMLAOS

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

        self.thToolsLayout.insertWidget(0, tb)

        connection_id = self.get_modes_action.triggered.connect(
            self.get_modes_reptate)
        connection_id = self.edit_modes_action.triggered.connect(
            self.edit_modes_window)
        connection_id = self.plot_modes_action.triggered.connect(
            self.plot_modes_graph)
        connection_id = self.save_modes_action.triggered.connect(
            self.save_modes)

    def select_shear_flow(self):
        self.flow_mode = FlowMode.shear
        self.tbutflow.setDefaultAction(self.shear_flow_action)

    def select_extensional_flow(self):
        self.flow_mode = FlowMode.uext
        self.tbutflow.setDefaultAction(self.extensional_flow_action)

    def get_modes_reptate(self):
        self.Qcopy_modes()

    def edit_modes_window(self):
        times, G, success = self.get_modes()
        if not success:
            self.logger.warning("Could not get modes successfully")
            return
        d = EditModesDialog(self, times, G, self.MAX_MODES)
        if d.exec_():
            nmodes = d.table.rowCount()
            self.set_param_value("nmodes", nmodes)
            success = True
            for i in range(nmodes):
                msg, success1 = self.set_param_value("tauD%02d" % i,
                                                     d.table.item(i, 0).text())
                msg, success2 = self.set_param_value("G%02d" % i,
                                                     d.table.item(i, 1).text())
                success *= success1 * success2
            if not success:
                QMessageBox.warning(
                    self, 'Error',
                    'Some parameter(s) could not be updated.\nPlease try again.'
                )
            else:
                self.handle_actionCalculate_Theory()

    def plot_modes_graph(self):
        pass
