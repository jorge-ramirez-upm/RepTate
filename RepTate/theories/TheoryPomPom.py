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
"""Module TheoryPomPom

Module for the Pom-Pom model for the non-linear flow of entangled polymers.

"""
import numpy as np
from math import exp  # faster than np for scalar
from scipy.integrate import ode, odeint
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from PyQt5.QtWidgets import QToolBar, QToolButton, QMenu, QStyle, QSpinBox, QTableWidget, QDialog, QVBoxLayout, QDialogButtonBox, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import Qt
from Theory_rc import *
from enum import Enum
from math import sqrt
from SpreadsheetWidget import SpreadsheetWidget
from Theory import EndComputationRequested
from ApplicationLAOS import GUIApplicationLAOS, CLApplicationLAOS
import Version
import time

class FlowMode(Enum):
    """Defines the flow geometry used
    
    Parameters can be:
        - shear: Shear flow
        - uext: Uniaxial extension flow
    """
    shear = 0
    uext = 1


class EditModesDialog(QDialog):
    def __init__(self, parent=None, times=0, G=0, MAX_MODES=0):
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
        self.table.setHorizontalHeaderLabels(["tauB", "G"])
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


class TheoryPomPom(CmdBase):
    """Multi-mode PomPom Model based on :cite:`NLVE-Blackwell2000`:
    
    .. math::
        \\boldsymbol \\sigma &= 3 \\sum_{i=1}^n G_i  \\lambda_i^2(t) \\boldsymbol S_i (t),\\\\
        \\boldsymbol S_i &= \\dfrac{\\boldsymbol A_i } {\\mathrm{Tr} \\boldsymbol A_i}\\\\
        \\dfrac {\\mathrm D \\boldsymbol A_i} {\\mathrm D t} &= \\boldsymbol \\kappa \\cdot \\boldsymbol A_i
        + \\boldsymbol A_i\\cdot \\boldsymbol \\kappa ^T 
        - \\dfrac {1} {\\tau_{\\mathrm b, i}}  (\\boldsymbol A_i - \\boldsymbol I), \\\\
        \\dfrac {\\mathrm D  \\lambda_i} {\\mathrm D t} &=
        \\lambda_i (\\boldsymbol \\kappa : \\boldsymbol S_i)
        - \\dfrac {1} {\\tau_{\\mathrm s, i}}  (\\lambda_i - 1)
        \\exp\\left( \\nu^* (\\lambda_i - 1) \\right),
        
    where, for each mode :math:`i`:
        - :math:`G_i`: weight of mode :math:`i`
        - :math:`\\tau_{\\mathrm b, i}`: backbone orientation relaxation time of mode :math:`i`
        - :math:`\\tau_{\\mathrm s, i}`: backbone stretch relaxation time of mode :math:`i`
        - :math:`\\nu_i^* = \\dfrac{2}{q_i - 1}`
        - :math:`q_i`: the number of dangling arms of each mode

   * **Parameters**
            - ``q_i`` :math:`\\equiv q_i`: the number of dangling arms of each mode
            - ``ratio_i`` :math:`\\equiv \\dfrac{\\tau_{\\mathrm b, i}}{\\tau_{\\mathrm s, i}}`:
            the ratio of orientation to stretch relaxation times of each mode

    """
    thname = "Pom-Pom"
    description = "Pom-Pom constitutive equation"
    citations = ["McLeish T.C.B. and Larson R.G., J. Rheol. 1998, 42, 81-110"]
    doi = ["http://dx.doi.org/10.1122/1.550933"]

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
        return GUITheoryPomPom(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryPomPom(
                name, parent_dataset, ax)


class BaseTheoryPomPom:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/NLVE/Theory/theory.html#multi-mode-pom-pom-model'
    single_file = False
    thname = TheoryPomPom.thname
    citations = TheoryPomPom.citations
    doi = TheoryPomPom.doi

    def __init__(self, name="", parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate_PomPom
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
            self.parameters["tauB%02d" % i] = Parameter(
                name="tauB%02d" % i,
                value=10.0,
                description="Backbone relaxation time of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.nopt,
                display_flag=False,
                min_value=0)
            self.parameters["q%02d" % i] = Parameter(
                name="q%02d" % i,
                value=1,
                description="Number of dangling arms of mode %02d" % i,
                type=ParameterType.integer,
                opt_type=OptType.opt,
                min_value=1,
                max_value=100)
            self.parameters["ratio%02d" % i] = Parameter(
                name="ratio%02d" % i,
                value=2,
                description=
                "Ratio of orientation to stretch relaxation times of mode %02d"
                % i,
                type=ParameterType.real,
                opt_type=OptType.const,
                min_value=1,
                max_value=5)

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
            print("in RP init:", e)
            self.flow_mode = FlowMode.shear  #default mode: shear

    def get_modes(self):
        """Get the values of Maxwell Modes from this theory"""
        nmodes = self.parameters["nmodes"].value
        tau = np.zeros(nmodes)
        G = np.zeros(nmodes)
        for i in range(nmodes):
            tau[i] = self.parameters["tauB%02d" % i].value
            G[i] = self.parameters["G%02d" % i].value
        return tau, G, True

    def set_modes(self, tau, G):
        """Set the values of Maxwell Modes from another theory"""
        nmodes = len(tau)
        self.set_param_value("nmodes", nmodes)
        for i in range(nmodes):
            self.set_param_value("tauB%02d" % i, tau[i])
            self.set_param_value("G%02d" % i, G[i])
        return True

    def sigmadot_shear(self, l, t, p):
        """PomPom model in shear"""
        if self.stop_theory_flag:
            raise EndComputationRequested
        q, tauB, tauS, gdot = p
        if (l >= q) or (q == 1):
            l = q
            dydx = 0
        elif l < 1:
            l = 1
            dydx = 0
        else:
            nustar = 2.0 / (q - 1)
            Axy = gdot * tauB * (1 - exp(-t / tauB))
            Axx = 2 * gdot * gdot * tauB * tauB * (1 - exp(
                -t / tauB)) + 1 - 2 * gdot * gdot * tauB * t * exp(-t / tauB)
            Trace = Axx + 2
            #For very fast modes, avoid integrating
            aux = tauS / exp(nustar * (l - 1))
            if (aux * gdot < 1e-3):
                dydx = 0
            else:
                dydx = l * gdot * Axy / Trace - (
                    l - 1) / tauS * exp(nustar * (l - 1))
        return dydx

    def sigmadot_uext(self, l, t, p):
        """PomPom model in uniaxial extension"""
        if self.stop_theory_flag:
            raise EndComputationRequested
        q, tauB, tauS, edot = p

        if (l >= q) or (q == 1):
            l = q
            dydx = 0
        else:
            nustar = 2.0 / (q - 1.0)
            Axx = (1 - 2 * edot * tauB * exp(
                (2 * edot * tauB - 1) * t / tauB)) / (1 - 2 * edot * tauB)
            Ayy = (1 + edot * tauB * exp(-(1 + edot * tauB) * t / tauB)) / (
                1 + edot * tauB)
            Trace = Axx + 2 * Ayy
            #For very fast modes, avoid integrating
            aux = tauS / exp(nustar * (l - 1))
            if Axx > 1E240:  # To avoid floating point overflow
                firstterm = l * edot
            else:
                firstterm = l * edot * (Axx - Ayy) / Trace

            if aux * edot < 1e-3:
                dydx = 0
            else:
                dydx = firstterm - (l - 1) / tauS * exp(nustar * (l - 1))
        return dydx

    def sigmadot_shearLAOS(self, l, t, p):
        """PomPom model in shear LAOS"""
        if self.stop_theory_flag:
            raise EndComputationRequested
        q, tauB, tauS, g0, w = p
        gdot = g0*w*np.cos(w*t)
        if (l >= q) or (q == 1):
            l = q
            dydx = 0
        elif l < 1:
            l = 1
            dydx = 0
        else:
            nustar = 2.0 / (q - 1)
            Axy = tauB*g0*w*(tauB*w*np.sin(w*t)-np.exp(-t/tauB)+np.cos(w*t))/(1+w**2*tauB**2)
            Axx = 1-tauB*g0**2*w*(2*np.cos(2*w*t)*tauB**3*w**3 + 2*np.exp(-t/tauB)*tauB**3*w**3 + 8*np.exp(-t/tauB)*tauB**2*w**2*np.sin(w*t) - 4*tauB**3*w**3 - 3*np.sin(2*w*t)*tauB**2*w**2 - np.cos(2*w*t)*tauB*w + 2*tauB*np.exp(-t/tauB)*w + 2*np.exp(-t/tauB)*np.sin(w*t) - tauB*w)/(4*tauB**4*w**4 + 5*tauB**2*w**2 + 1)
            Trace = Axx + 2
            #For very fast modes, avoid integrating
            aux = tauS / exp(nustar * (l - 1))
            if (aux * gdot < 1e-3):
                dydx = 0
            else:
                dydx = l * gdot * Axy / Trace - (
                    l - 1) / tauS * exp(nustar * (l - 1))
        return dydx

    def calculate_PomPom(self, f=None):
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
        tt.data[:, 0] = ft.data[:, 0]

        #flow geometry
        if self.flow_mode == FlowMode.shear:
            pde_stretch = self.sigmadot_shear
        elif self.flow_mode == FlowMode.uext:
            pde_stretch = self.sigmadot_uext
        else:
            return

        # ODE solver parameters
        abserr = 1.0e-8
        relerr = 1.0e-6
        times = ft.data[:, 0]
        times = np.concatenate([[0], times])

        #create parameters list
        flow_rate = float(f.file_parameters["gdot"])
        nmodes = self.parameters["nmodes"].value
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            G = self.parameters["G%02d" % i].value
            q = self.parameters["q%02d" % i].value
            tauB = self.parameters["tauB%02d" % i].value
            tauS = tauB / self.parameters["ratio%02d" % i].value
            p = [q, tauB, tauS, flow_rate]

            #solve ODEs
            stretch_ini = 1
            try:
                l = odeint(
                    pde_stretch,
                    stretch_ini,
                    times,
                    args=(p, ),
                    atol=abserr,
                    rtol=relerr)
            except EndComputationRequested:
                break
            # write results in table
            l = np.delete(l, [0])  # delete the t=0 value
            t = np.delete(times, [0])  # delete the t=0 value
            if self.flow_mode == FlowMode.shear:
                Axy_arr = flow_rate * tauB * (1 - np.exp(-t / tauB))
                Axx_arr = 2 * flow_rate * flow_rate * tauB * tauB * (
                    1 - np.exp(-t / tauB)
                ) + 1 - 2 * flow_rate * flow_rate * tauB * t * np.exp(
                    -t / tauB)
                tt.data[:, 1] += 3 * G * l * l * Axy_arr / (Axx_arr + 2.0)

            elif self.flow_mode == FlowMode.uext:
                Axx_arr = (1 - 2 * flow_rate * tauB * np.exp(
                    (2 * flow_rate * tauB - 1) * t / tauB)) / (
                        1 - 2 * flow_rate * tauB)
                Ayy_arr = (1 + flow_rate * tauB * np.exp(
                    -(1 + flow_rate * tauB) * t / tauB)) / (
                        1 + flow_rate * tauB)

                k = np.ones(len(t))
                k[Axx_arr < 1e240] = (Axx_arr - Ayy_arr) / (
                    Axx_arr + 2 * Ayy_arr)  # k=1 if Axx > 1e240

                tt.data[:, 1] += 3 * G * l * l * k

    def calculate_PomPomLAOS(self, f=None):
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        pde_stretchLAOS = self.sigmadot_shearLAOS

        # ODE solver parameters
        abserr = 1.0e-8
        relerr = 1.0e-6

        #create parameters list
        g0 = float(f.file_parameters["gamma"])
        w = float(f.file_parameters["omega"])
        nmodes = self.parameters["nmodes"].value
        times = ft.data[:, 0]
        tt.data[:, 1] = g0*np.sin(w*times)
        times = np.concatenate([[0], times])
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            G = self.parameters["G%02d" % i].value
            q = self.parameters["q%02d" % i].value
            tauB = self.parameters["tauB%02d" % i].value
            tauS = tauB / self.parameters["ratio%02d" % i].value
            p = [q, tauB, tauS, g0, w]

            #solve ODEs
            stretch_ini = 1
            try:
                l = odeint(
                    pde_stretchLAOS,
                    stretch_ini,
                    times,
                    args=(p, ),
                    atol=abserr,
                    rtol=relerr)
            except EndComputationRequested:
                break
            # write results in table
            l = np.delete(l, [0])  # delete the t=0 value
            t = np.delete(times, [0])  # delete the t=0 value
            Axy_arr = tauB*g0*w*(tauB*w*np.sin(w*t)-np.exp(-t/tauB)+np.cos(w*t))/(1+w**2*tauB**2)
            Axx_arr = 1-tauB*g0**2*w*(2*np.cos(2*w*t)*tauB**3*w**3 + 2*np.exp(-t/tauB)*tauB**3*w**3 + 8*np.exp(-t/tauB)*tauB**2*w**2*np.sin(w*t) - 4*tauB**3*w**3 - 3*np.sin(2*w*t)*tauB**2*w**2 - np.cos(2*w*t)*tauB*w + 2*tauB*np.exp(-t/tauB)*w + 2*np.exp(-t/tauB)*np.sin(w*t) - tauB*w)/(4*tauB**4*w**4 + 5*tauB**2*w**2 + 1)
            tt.data[:, 2] += 3 * G * l * l * Axy_arr / (Axx_arr + 2.0)            

    def set_param_value(self, name, value):
        """[summary]
        
        [description]
        
        Arguments:
            - name {[type]} -- [description]
            - value {[type]} -- [description]
        """
        if (name == "nmodes"):
            oldn = self.parameters["nmodes"].value
        message, success = super(BaseTheoryPomPom, self).set_param_value(
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
                self.parameters["tauB%02d" % i] = Parameter(
                    name="tauB%02d" % i,
                    value=10.0,
                    description="Backbone relaxation time of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.nopt,
                    display_flag=False,
                    min_value=0)
                self.parameters["q%02d" % i] = Parameter(
                    name="q%02d" % i,
                    value=1,
                    description="Number of dangling arms of mode %02d" % i,
                    type=ParameterType.integer,
                    opt_type=OptType.opt,
                    min_value=1,
                    max_value=100)
                self.parameters["ratio%02d" % i] = Parameter(
                    name="ratio%02d" % i,
                    value=2,
                    description=
                    "Ratio of orientation to stretch relaxation times of mode %02d"
                    % i,
                    type=ParameterType.real,
                    opt_type=OptType.const,
                    min_value=1,
                    max_value=5)
            if (oldn > self.parameters["nmodes"].value):
                for i in range(self.parameters["nmodes"].value, oldn):
                    del self.parameters["G%02d" % i]
                    del self.parameters["tauB%02d" % i]
                    del self.parameters["ratio%02d" % i]
                    del self.parameters["q%02d" % i]
        return '', True


class CLTheoryPomPom(BaseTheoryPomPom, Theory):
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
            self.function = self.calculate_PomPomLAOS


class GUITheoryPomPom(BaseTheoryPomPom, QTheory):
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
            self.function = self.calculate_PomPomLAOS

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

        #Save to flowsolve button
        self.flowsolve_btn = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-save-flowsolve.png'),
            'Save Parameters To FlowSolve')
        self.flowsolve_btn.setCheckable(False)

        self.thToolsLayout.insertWidget(0, tb)

        connection_id = self.get_modes_action.triggered.connect(
            self.get_modes_reptate)
        connection_id = self.edit_modes_action.triggered.connect(
            self.edit_modes_window)
        connection_id = self.plot_modes_action.triggered.connect(
            self.plot_modes_graph)
        connection_id = self.save_modes_action.triggered.connect(
            self.save_modes)
        connection_id = self.flowsolve_btn.triggered.connect(
            self.handle_flowsolve_btn)

    def handle_flowsolve_btn(self):
        """Save theory parameters in FlowSolve format"""

        #Get filename of RepTate project to open
        fpath, _ = QFileDialog.getSaveFileName(self,
            "Save Parameters to FowSolve", "data/", "FlowSolve (*.fsrep)")
        if fpath == '':
            return
        
        with open(fpath, 'w') as f:
            header = '#flowGen input\n'
            header += '# Generated with RepTate v%s %s\n' % (Version.VERSION, Version.DATE)
            header += '# At %s on %s\n' % (time.strftime("%X"), time.strftime("%a %b %d, %Y"))
            f.write(header)

            f.write('\n#param global\n')
            f.write('constit multip\n')
            # f.write('# or multip (for pompom) or polydisperse (for polydisperse Rolie-Poly)\n')

            f.write('\n#param constitutive\n')
            
            n = self.parameters['nmodes'].value
            td = np.zeros(n)
            for i in range(n):
                td[i] = self.parameters["tauB%02d" % i].value
            # sort taud ascending order
            args = np.argsort(td)

            modulus = 'modulus'
            taub = 'taub'
            ratio = 'ratio'
            qarms = 'qarms'
            for i, arg in enumerate(args):
                modulus += ' %.6g' % self.parameters["G%02d" % arg].value
                taub += ' %.6g' % self.parameters["tauB%02d" % arg].value
                ratio += ' %.6g' % self.parameters["ratio%02d" % arg].value
                qarms += ' %.6g' % self.parameters["q%02d" % arg].value
            f.write('%s\n%s\n%s\n%s\n' % (modulus, taub, ratio, qarms))
            
            f.write('nustar 2\n')

            f.write('\n#end')
        
        QMessageBox.information(self, 'Success', 'Wrote FlowSolve parameters in \"%s\"' % fpath)

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
                msg, success1 = self.set_param_value("tauB%02d" % i,
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
