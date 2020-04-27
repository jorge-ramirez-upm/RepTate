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
"""Module TheoryGiesekus

Module for the Giesekus model for the non-linear flow of entangled polymers.

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
from Theory import EndComputationRequested
from ApplicationLAOS import GUIApplicationLAOS, CLApplicationLAOS

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


class TheoryGiesekus(CmdBase):
    """Multi-mode Giesekus Model (see Chapter 6 of :cite:`NLVE-Larson1988`):
    
    .. math::
        \\boldsymbol \\sigma &= \\sum_{i=1}^n G_i \\boldsymbol  {A_i},\\\\
        \\dfrac {\\mathrm D \\boldsymbol  A_i} {\\mathrm D t} &=  \\boldsymbol \\kappa \\cdot \\boldsymbol A_i
        + \\boldsymbol A_i\\cdot \\boldsymbol \\kappa ^T 
        - \dfrac {1} {\\tau_i}  (\\boldsymbol A_i - \\boldsymbol I)
        -  \dfrac {\\alpha_i} {\\tau_i} (\\boldsymbol A_i - \\boldsymbol I)^2,

    where for each mode :math:`i`:
        - :math:`G_i`: weight of mode :math:`i`
        - :math:`\\tau_i`: relaxation time of mode :math:`i`
        - :math:`\\alpha_i`: constant of proportionality mode :math:`i`
   
   * **Parameters**
        - ``alpha_i`` :math:`\\equiv \\alpha_i`

    """
    thname = "Giesekus"
    description = "Giesekus constitutive equation"
    citations = ["Giesekus H., Rheol. Acta 1966, 5, 29"]
    doi = ["http://dx.doi.org/10.1007/BF01973575"]

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
        return GUITheoryGiesekus(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryGiesekus(
                name, parent_dataset, ax)


class BaseTheoryGiesekus:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/NLVE/Theory/theory.html#multi-mode-giesekus-model'
    single_file = False
    thname = TheoryGiesekus.thname
    citations = TheoryGiesekus.citations
    doi = TheoryGiesekus.doi

    def __init__(self, name="", parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate_giesekus
        self.has_modes = True
        self.parameters["nmodes"] = Parameter(
            name="nmodes",
            value=2,
            description="Number of modes",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False)
        self.parameters["nstretch"] = Parameter(
            name="nstretch",
            value=2,
            description="Number of strecthing modes",
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
            self.parameters["alpha%02d" % i] = Parameter(
                name="alpha%02d" % i,
                value=0.5,
                description="Dimensionless mobility factor of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.opt,
                min_value=0,
                max_value=1)

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
            tau[i] = self.parameters["tauD%02d" % i].value
            G[i] = self.parameters["G%02d" % i].value
        return tau, G, True

    def set_modes(self, tau, G):
        """Set the values of Maxwell Modes from another theory"""
        nmodes = len(tau)
        self.set_param_value("nmodes", nmodes)
        self.set_param_value("nstretch", nmodes)

        for i in range(nmodes):
            self.set_param_value("tauD%02d" % i, tau[i])
            self.set_param_value("G%02d" % i, G[i])
        return True

    def n1_uext(self, p, times):
        """Upper Convected Maxwell model in uniaxial extension.
        Returns N1 = (XX -YY) component of stress tensor
        
        [description]
        
        Arguments:
            - p {array} -- p = [G, tauD, epsilon_dot] 
            - times {array} -- time
        """
        _, G, tauD, ed = p
        w = tauD * ed
        sxx = (1 - 2 * w * np.exp(-(1 - 2 * w) * times / tauD)) / (1 - 2 * w)
        syy = (1 + w * np.exp(-(1 + w) * times / tauD)) / (1 + w)

        return G * (sxx - syy)

    def sigma_xy_shear(self, p, times):
        """Upper Convected Maxwell model in shear.
        Returns XY component of stress tensor
        
        [description]
        
        Arguments:
            - p {array} -- p = [G, tauD, gamma_dot] 
            - times {array} -- time
        """
        _, G, tauD, gd = p

        return G * gd * tauD * (1 - np.exp(-times / tauD))

    def sigma_xy_shearLAOS(self, p, times):
        _, G, tauD, g0, w = p
        eta = G*tauD

        return eta*g0*w*(tauD*w*np.sin(w*times)
                        -np.exp(-times/tauD)
                        +np.cos(w*times))/(1+w**2*tauD**2)

    def sigmadot_shear(self, sigma, times, p):
        """Giesekus model in shear"""
        if self.stop_theory_flag:
            raise EndComputationRequested
        alpha, _, tau, gdot = p
        sxx, syy, sxy = sigma

        dsxx = 2 * gdot * sxy + (alpha - 1) * (sxx - 1) / tau - alpha / tau * (
            sxx * sxx + sxy * sxy - sxx)

        dsyy = (alpha - 1) * (syy - 1) / tau - alpha / tau * (
            sxy * sxy + syy * syy - syy)

        dsxy = gdot * syy + (alpha - 1) * sxy / tau - alpha / tau * (
            sxx * sxy + sxy * syy - sxy)

        return [dsxx, dsyy, dsxy]

    def sigmadot_uext(self, sigma, times, p):
        """Giesekus model in uniaxial extension"""
        if self.stop_theory_flag:
            raise EndComputationRequested
        alpha, _, tau, edot = p
        sxx, syy = sigma

        dsxx = 2 * edot * sxx + (alpha - 1) * (sxx - 1) / tau - alpha / tau * (
            sxx * sxx - sxx)

        dsyy = -edot * syy + (alpha - 1) * (syy - 1) / tau - alpha / tau * (
            syy * syy - syy)

        return [dsxx, dsyy]

    # def sigmadot_uext(self, sigma, times, p):
    #     """Giesekus model in uniaxial extension"""
    #     alpha, _, tau, gdot = p
    #     sxx, syy = sigma

    #     dsxx = 2 * gdot * sxx - (sxx - 1) / tau - alpha / tau * sxx * (sxx - 1)
    #     dsyy = -gdot * syy - (syy - 1) / tau - alpha / tau * syy * (syy - 1)
    #     return [dsxx, dsyy]

    def sigmadot_shearLAOS(self, sigma, times, p):
        """Giesekus model in shear"""
        if self.stop_theory_flag:
            raise EndComputationRequested
        alpha, _, tau, g0, w = p
        sxx, syy, sxy = sigma
        gdot = g0*w*np.cos(w*times)

        dsxx = 2 * gdot * sxy + (alpha - 1) * (sxx - 1) / tau - alpha / tau * (
            sxx * sxx + sxy * sxy - sxx)

        dsyy = (alpha - 1) * (syy - 1) / tau - alpha / tau * (
            sxy * sxy + syy * syy - syy)

        dsxy = gdot * syy + (alpha - 1) * sxy / tau - alpha / tau * (
            sxx * sxy + sxy * syy - sxy)

        return [dsxx, dsyy, dsxy]

    def calculate_giesekus(self, f=None):
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
            sigma0 = [1.0, 1.0, 0.0]  # sxx, syy, sxy
            pde_stretch = self.sigmadot_shear
        elif self.flow_mode == FlowMode.uext:
            sigma0 = [1.0, 1.0]  # sxx, syy
            pde_stretch = self.sigmadot_uext
        else:
            return

        # ODE solver parameters
        abserr = 1.0e-8
        relerr = 1.0e-6
        t = ft.data[:, 0]
        t = np.concatenate([[0], t])
        # sigma0 = [1.0, 1.0, 0.0]  # sxx, syy, sxy
        flow_rate = float(f.file_parameters["gdot"])
        nmodes = self.parameters["nmodes"].value
        nstretch = self.parameters["nstretch"].value
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            G = self.parameters["G%02d" % i].value
            tauD = self.parameters["tauD%02d" % i].value
            alpha = self.parameters["alpha%02d" % i].value
            p = [alpha, G, tauD, flow_rate]
            if i < nstretch:
                try:
                    sig = odeint(
                        pde_stretch,
                        sigma0,
                        t,
                        args=(p, ),
                        atol=abserr,
                        rtol=relerr)
                except EndComputationRequested:
                    break
                if self.flow_mode == FlowMode.shear:
                    sxy = np.delete(sig[:, 2], [0])
                    tt.data[:, 1] += G * sxy
                elif self.flow_mode == FlowMode.uext:
                    sxx = np.delete(sig[:, 0], [0])
                    syy = np.delete(sig[:, 1], [0])
                    tt.data[:, 1] += G * (sxx - syy)
            else:
                # use UCM for non stretching modes
                if self.flow_mode == FlowMode.shear:
                    tt.data[:, 1] += self.sigma_xy_shear(p, ft.data[:, 0])
                elif self.flow_mode == FlowMode.uext:
                    tt.data[:, 1] += self.n1_uext(p, ft.data[:, 0])

    def calculate_giesekusLAOS(self, f=None):
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

        sigma0 = [1.0, 1.0, 0.0]  # sxx, syy, sxy
        pde_stretchLAOS = self.sigmadot_shearLAOS

        # ODE solver parameters
        abserr = 1.0e-8
        relerr = 1.0e-6
        g0 = float(f.file_parameters["gamma"])
        w = float(f.file_parameters["omega"])
        nmodes = self.parameters["nmodes"].value
        nstretch = self.parameters["nstretch"].value
        t = ft.data[:, 0]
        tt.data[:, 1] = g0*np.sin(w*t)
        t = np.concatenate([[0], t])
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            G = self.parameters["G%02d" % i].value
            tauD = self.parameters["tauD%02d" % i].value
            alpha = self.parameters["alpha%02d" % i].value
            p = [alpha, G, tauD, g0, w]
            if i < nstretch:
                try:
                    sig = odeint(
                        pde_stretchLAOS,
                        sigma0,
                        t,
                        args=(p, ),
                        atol=abserr,
                        rtol=relerr)
                except EndComputationRequested:
                    break
                sxy = np.delete(sig[:, 2], [0])
                tt.data[:, 2] += G * sxy
            else:
                # use UCM for non stretching modes
                tt.data[:, 1] += self.sigma_xy_shearLAOS(p, ft.data[:, 0])
 
    def set_param_value(self, name, value):
        """[summary]
        
        [description]
        
        Arguments:
            - name {[type]} -- [description]
            - value {[type]} -- [description]
        """
        if (name == "nmodes"):
            oldn = self.parameters["nmodes"].value
            if CmdBase.mode==CmdMode.GUI:
                self.spinbox.setMaximum(int(value))
        message, success = super(BaseTheoryGiesekus, self).set_param_value(
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
                self.parameters["alpha%02d" % i] = Parameter(
                    name="alpha%02d" % i,
                    value=0.5,
                    description="Constant of proportionality of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.opt,
                    display_flag=True,
                    min_value=0,
                    max_value=1)
            if (oldn > self.parameters["nmodes"].value):
                for i in range(self.parameters["nmodes"].value, oldn):
                    del self.parameters["G%02d" % i]
                    del self.parameters["tauD%02d" % i]
                    del self.parameters["alpha%02d" % i]
        return '', True


class CLTheoryGiesekus(BaseTheoryGiesekus, Theory):
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
            self.function = self.calculate_giesekusLAOS


class GUITheoryGiesekus(BaseTheoryGiesekus, QTheory):
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
            self.function = self.calculate_giesekusLAOS

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

        #SpinBox "n-stretch modes"
        self.spinbox = QSpinBox()
        self.spinbox.setRange(
            0, self.parameters["nmodes"].value)  # min and max number of modes
        self.spinbox.setSuffix(" stretch")
        self.spinbox.setToolTip("Number of stretching modes")
        self.spinbox.setValue(self.parameters["nmodes"].value)  #initial value
        tb.addWidget(self.spinbox)

        self.thToolsLayout.insertWidget(0, tb)

        connection_id = self.get_modes_action.triggered.connect(
            self.get_modes_reptate)
        connection_id = self.edit_modes_action.triggered.connect(
            self.edit_modes_window)
        connection_id = self.plot_modes_action.triggered.connect(
            self.plot_modes_graph)
        connection_id = self.save_modes_action.triggered.connect(
            self.save_modes)
        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged)

    def handle_spinboxValueChanged(self, value):
        nmodes = self.parameters["nmodes"].value
        self.set_param_value("nstretch", min(nmodes, value))
        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()

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
            self.set_param_value("nstretch", nmodes)
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
