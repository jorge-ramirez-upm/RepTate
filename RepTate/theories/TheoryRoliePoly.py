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
"""Module TheoryRoliePoly

Module for the Rolie-Poly theory for the non-linear flow of entangled polymers.

"""
import numpy as np
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
import Version
import time
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


class FeneMode(Enum):
    """Defines the finite extensibility function
    
    Parameters can be:
        - none: No finite extensibility
        - with_fene: With finite extensibility
    """
    none = 0
    with_fene = 1


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

class TheoryRoliePoly(CmdBase):
    """Rolie-Poly
    
    [description]
    """
    thname = "Rolie-Poly"
    description = "Rolie-Poly constitutive equation"
    citations = ["Likhtman, A.E. & Graham, R.S., J. Non-Newtonian Fluid Mech., 2003, 114, 1-12"]
    doi = ["http://dx.doi.org/10.1016/S0377-0257(03)00114-9"]

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
        return GUITheoryRoliePoly(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryRoliePoly(
                name, parent_dataset, ax)


class BaseTheoryRoliePoly:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/NLVE/Theory/theory.html#rolie-poly-equation'
    single_file = False
    thname = TheoryRoliePoly.thname
    citations = TheoryRoliePoly.citations
    doi = TheoryRoliePoly.doi

    def __init__(self, name="", parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.RoliePoly
        self.has_modes = True
        self.parameters["beta"] = Parameter(
            name="beta",
            value=0.5,
            description="CCR coefficient",
            type=ParameterType.real,
            opt_type=OptType.nopt)
        self.parameters["delta"] = Parameter(
            name="delta",
            value=-0.5,
            description="CCR exponent",
            type=ParameterType.real,
            opt_type=OptType.nopt)
        self.parameters["lmax"] = Parameter(
            name="lmax",
            value=10.0,
            description="Maximum extensibility",
            type=ParameterType.real,
            opt_type=OptType.nopt,
            display_flag=False,
            min_value=1.01)
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
            self.parameters["tauR%02d" % i] = Parameter(
                name="tauR%02d" % i,
                value=0.5,
                description="Rouse time of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.opt,
                min_value=1e-12)

        self.view_LVEenvelope = False
        auxseries = self.ax.plot([], [], label='')
        self.LVEenvelopeseries = auxseries[0]
        self.LVEenvelopeseries.set_marker('')
        self.LVEenvelopeseries.set_linestyle('--')
        self.LVEenvelopeseries.set_visible(self.view_LVEenvelope)
        self.LVEenvelopeseries.set_color('green')
        self.LVEenvelopeseries.set_linewidth(5)
        self.LVEenvelopeseries.set_label('')

        self.MAX_MODES = 40
        self.with_fene = FeneMode.none
        self.init_flow_mode()

    def set_extra_data(self, extra_data):
        """Set extra data when loading project"""
        self.handle_with_fene_button(extra_data['with_fene'])
        self.spinbox.setValue(self.parameters["nstretch"].value)

    def get_extra_data(self):
        """Set extra_data when saving project"""
        self.extra_data['with_fene'] = self.with_fene == FeneMode.with_fene

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

    def destructor(self):
        """Called when the theory tab is closed"""
        self.extra_graphic_visible(False)
        self.ax.lines.remove(self.LVEenvelopeseries)

    def show_theory_extras(self, show=False):
        """Called when the active theory is changed
        
        [description]
        """
        if CmdBase.mode == CmdMode.GUI:
            self.Qhide_theory_extras(show)
        # self.extra_graphic_visible(self.linearenvelope.isChecked())

    def extra_graphic_visible(self, state):
        """[summary]
        
        [description]
        """
        self.LVEenvelopeseries.set_visible(state)
        self.parent_dataset.parent_application.update_plot()

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

    def sigmadot_shear(self, sigma, t, p):
        """Rolie-Poly differential equation under *shear* flow
        with stretching and finite extensibility if selected
        
        [description]
        
        Arguments:
            - sigma {array} -- vector of state variables, sigma = [sxx, syy, sxy]
            - t {float} -- time
            - p {array} -- vector of the parameters, p = [tauD, tauR, beta, delta, gammadot]
        """
        if self.stop_theory_flag:
            raise EndComputationRequested
        sxx, syy, sxy = sigma
        lmax, tauD, tauR, beta, delta, gammadot = p

        # Create the vector with the time derivative of sigma
        trace_sigma = sxx + 2 * syy
        l_sq = trace_sigma / 3.0  # stretch^2
        if self.with_fene == FeneMode.with_fene:
            fene = self.calculate_fene(l_sq, lmax)
            aux1 = 2.0 * (1.0 - 1.0 / sqrt(l_sq)) / tauR * fene
        else:
            aux1 = 2.0 * (1.0 - 1.0 / sqrt(l_sq)) / tauR
        aux2 = beta * (l_sq**delta)

        return [
            2 * gammadot * sxy - (sxx - 1.) / tauD - aux1 * (sxx + aux2 *
                                                             (sxx - 1.)),
            -1.0 * (syy - 1.) / tauD - aux1 * (syy + aux2 * (syy - 1.)),
            gammadot * syy - sxy / tauD - aux1 * (sxy + aux2 * sxy)
        ]

    def sigmadot_shear_nostretch(self, sigma, t, p):
        """Rolie-Poly differential equation under shear flow, without stretching
        
        [description]
        
        Arguments:
            - sigma {array} -- vector of state variables, sigma = [sxx, syy, sxy]
            - t {float} -- time
            - p {array} -- vector of the parameters, p = [tauD, tauR, beta, delta, gammadot]
        """
        if self.stop_theory_flag:
            raise EndComputationRequested
        sxx, syy, sxy = sigma
        _, tauD, _, beta, _, gammadot = p

        # Create the vector with the time derivative of sigma
        return [
            2.0 * gammadot * sxy -
            (sxx - 1.0) / tauD - 2.0 / 3.0 * gammadot * sxy * (sxx + beta *
                                                               (sxx - 1)),
            -(syy - 1.0) / tauD - 2.0 / 3.0 * gammadot * sxy * (syy + beta *
                                                                (syy - 1)),
            gammadot * syy - sxy / tauD - 2.0 / 3.0 * gammadot * sxy *
            (sxy + beta * sxy)
        ]

    def sigmadot_uext(self, sigma, t, p):
        """Rolie-Poly differential equation under *uniaxial elongational* flow
        with stretching and finite extensibility if selecter

        [description]

        Arguments:
            - sigma {array} -- vector of state variables, sigma = [sxx, syy]
            - t {float} -- time
            - p {array} -- vector of the parameters, p = [tauD, tauR, beta, delta, gammadot]
        """
        if self.stop_theory_flag:
            raise EndComputationRequested
        sxx, syy = sigma
        lmax, tauD, tauR, beta, delta, epsilon_dot = p

        # Create the vector with the time derivative of sigma
        trace_sigma = sxx + 2 * syy
        l_sq = trace_sigma / 3.0  # stretch^2
        if self.with_fene == FeneMode.with_fene:
            fene = self.calculate_fene(l_sq, lmax)
            aux1 = 2.0 * (1.0 - 1.0 / sqrt(l_sq)) / tauR * fene
        else:
            aux1 = 2.0 * (1.0 - 1.0 / sqrt(l_sq)) / tauR
        aux2 = beta * (l_sq**delta)

        dsxx = 2.0 * epsilon_dot * sxx - (sxx - 1.0) / tauD - aux1 * (
            sxx + aux2 * (sxx - 1.0))
        dsyy = -epsilon_dot * syy - (syy - 1.0) / tauD - aux1 * (syy + aux2 *
                                                                 (syy - 1.0))
        return [dsxx, dsyy]

    def sigmadot_uext_nostretch(self, sigma, t, p):
        """Rolie-Poly differential equation under elongation flow, wihtout stretching
        
        [description]
        
        Arguments:
            - sigma {array} -- vector of state variables, sigma = [sxx, syy]
            - t {float} -- time
            - p {array} -- vector of the parameters, p = [tauD, tauR, beta, delta, epsilon_dot]
        """
        if self.stop_theory_flag:
            raise EndComputationRequested
        sxx, syy = sigma
        _, tauD, tauR, beta, delta, epsilon_dot = p

        # Create the vector with the time derivative of sigma
        trace_k_sigma = epsilon_dot * (sxx - syy)
        aux1 = 2.0 / 3.0 * trace_k_sigma
        return [
            2.0 * epsilon_dot * sxx - (sxx - 1.0) / tauD - aux1 *
            (sxx + beta * (sxx - 1.0)), -epsilon_dot * syy -
            (syy - 1.0) / tauD - aux1 * (syy + beta * (syy - 1.0))
        ]

    def sigmadot_shearLAOS(self, sigma, t, p):
        """Rolie-Poly differential equation under *shear* flow
        with stretching and finite extensibility if selected
        
        [description]
        
        Arguments:
            - sigma {array} -- vector of state variables, sigma = [sxx, syy, sxy]
            - t {float} -- time
            - p {array} -- vector of the parameters, p = [lmax, tauD, tauR, beta, delta, g0, w]
        """
        if self.stop_theory_flag:
            raise EndComputationRequested
        sxx, syy, sxy = sigma
        lmax, tauD, tauR, beta, delta, g0, w = p
        gammadot = g0*w*np.cos(w*t)

        # Create the vector with the time derivative of sigma
        trace_sigma = sxx + 2 * syy
        l_sq = trace_sigma / 3.0  # stretch^2
        if self.with_fene == FeneMode.with_fene:
            fene = self.calculate_fene(l_sq, lmax)
            aux1 = 2.0 * (1.0 - 1.0 / sqrt(l_sq)) / tauR * fene
        else:
            aux1 = 2.0 * (1.0 - 1.0 / sqrt(l_sq)) / tauR
        aux2 = beta * (l_sq**delta)

        return [
            2 * gammadot * sxy - (sxx - 1.) / tauD - aux1 * (sxx + aux2 *
                                                             (sxx - 1.)),
            -1.0 * (syy - 1.) / tauD - aux1 * (syy + aux2 * (syy - 1.)),
            gammadot * syy - sxy / tauD - aux1 * (sxy + aux2 * sxy)
        ]

    def sigmadot_shear_nostretchLAOS(self, sigma, t, p):
        """Rolie-Poly differential equation under shear flow, without stretching
        
        [description]
        
        Arguments:
            - sigma {array} -- vector of state variables, sigma = [sxx, syy, sxy]
            - t {float} -- time
            - p {array} -- vector of the parameters, p = [lmax, tauD, tauR, beta, delta, g0, w]
        """
        if self.stop_theory_flag:
            raise EndComputationRequested
        sxx, syy, sxy = sigma
        _, tauD, _, beta, _, g0, w = p
        gammadot = g0*w*np.cos(w*t)

        # Create the vector with the time derivative of sigma
        return [
            2.0 * gammadot * sxy -
            (sxx - 1.0) / tauD - 2.0 / 3.0 * gammadot * sxy * (sxx + beta *
                                                               (sxx - 1)),
            -(syy - 1.0) / tauD - 2.0 / 3.0 * gammadot * sxy * (syy + beta *
                                                                (syy - 1)),
            gammadot * syy - sxy / tauD - 2.0 / 3.0 * gammadot * sxy *
            (sxy + beta * sxy)
        ]
    def calculate_fene(self, l_square, lmax):
        """calculate finite extensibility function value"""
        ilm2 = 1.0 / (lmax * lmax)  # 1/lambda_max^2
        l2_lm2 = l_square * ilm2  # (lambda/lambda_max)^2
        return (3.0 - l2_lm2) / (1.0 - l2_lm2) * (1.0 - ilm2) / (3.0 - ilm2)

    def RoliePoly(self, f=None):
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

        #flow geometry and finite extensibility
        if self.flow_mode == FlowMode.shear:
            sigma0 = [1.0, 1.0, 0.0]  # sxx, syy, sxy
            pde_nostretch = self.sigmadot_shear_nostretch
            pde_stretch = self.sigmadot_shear
        elif self.flow_mode == FlowMode.uext:
            sigma0 = [1.0, 1.0]  # sxx, syy
            pde_nostretch = self.sigmadot_uext_nostretch
            pde_stretch = self.sigmadot_uext
        else:
            return

        # ODE solver parameters
        abserr = 1.0e-8
        relerr = 1.0e-6
        t = ft.data[:, 0]
        t = np.concatenate([[0], t])
        # sigma0 = [1.0, 1.0, 0.0]  # sxx, syy, sxy
        beta = self.parameters["beta"].value
        delta = self.parameters["delta"].value
        lmax = self.parameters["lmax"].value
        flow_rate = float(f.file_parameters["gdot"])
        nmodes = self.parameters["nmodes"].value
        nstretch = self.parameters["nstretch"].value
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            tauD = self.parameters["tauD%02d" % i].value
            tauR = self.parameters["tauR%02d" % i].value
            p = [lmax, tauD, tauR, beta, delta, flow_rate]
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
            else:
                try:
                    sig = odeint(
                        pde_nostretch,
                        sigma0,
                        t,
                        args=(p, ),
                        atol=abserr,
                        rtol=relerr)
                except EndComputationRequested:
                    break

            sxx = np.delete(sig[:, 0], [0])
            syy = np.delete(sig[:, 1], [0])
            if self.flow_mode == FlowMode.shear:
                sxy = np.delete(sig[:, 2], [0])
                tt.data[:, 1] += self.parameters["G%02d" % i].value * sxy
            elif self.flow_mode == FlowMode.uext:
                tt.data[:, 1] += self.parameters["G%02d" % i].value * (
                    sxx - syy)

            if self.with_fene == FeneMode.with_fene:
                ilm2 = 1.0 / (lmax * lmax)  # 1/lambda_max^2
                l_sq_arr = (sxx + 2.0 * syy) / 3.0  # array lambda^2
                l2_lm2_arr = l_sq_arr * ilm2  # array (lambda/lambda_max)^2
                fene_arr = (3.0 - l2_lm2_arr) / (1.0 - l2_lm2_arr) * (
                    1.0 - ilm2) / (3.0 - ilm2)  # fene array
                tt.data[:, 1] *= fene_arr

    def RoliePolyLAOS(self, f=None):
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        #flow geometry and finite extensibility
        sigma0 = [1.0, 1.0, 0.0]  # sxx, syy, sxy
        pde_nostretchLAOS = self.sigmadot_shear_nostretchLAOS
        pde_stretchLAOS = self.sigmadot_shearLAOS

        # ODE solver parameters
        abserr = 1.0e-8
        relerr = 1.0e-6
        beta = self.parameters["beta"].value
        delta = self.parameters["delta"].value
        lmax = self.parameters["lmax"].value
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
            tauD = self.parameters["tauD%02d" % i].value
            tauR = self.parameters["tauR%02d" % i].value
            p = [lmax, tauD, tauR, beta, delta, g0, w]
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
            else:
                try:
                    sig = odeint(
                        pde_nostretchLAOS,
                        sigma0,
                        t,
                        args=(p, ),
                        atol=abserr,
                        rtol=relerr)
                except EndComputationRequested:
                    break

            sxx = np.delete(sig[:, 0], [0])
            syy = np.delete(sig[:, 1], [0])
            sxy = np.delete(sig[:, 2], [0])
            tt.data[:, 2] += self.parameters["G%02d" % i].value * sxy

            if self.with_fene == FeneMode.with_fene:
                ilm2 = 1.0 / (lmax * lmax)  # 1/lambda_max^2
                l_sq_arr = (sxx + 2.0 * syy) / 3.0  # array lambda^2
                l2_lm2_arr = l_sq_arr * ilm2  # array (lambda/lambda_max)^2
                fene_arr = (3.0 - l2_lm2_arr) / (1.0 - l2_lm2_arr) * (
                    1.0 - ilm2) / (3.0 - ilm2)  # fene array
                tt.data[:, 2] *= fene_arr

    def set_param_value(self, name, value):
        """[summary]
        
        [description]
        
        Arguments:
            - name {[type]} -- [description]
            - value {[type]} -- [description]
        """
        if (name == "nmodes"):
            oldn = self.parameters["nmodes"].value
            if CmdBase.mode == CmdMode.GUI:
                self.spinbox.setMaximum(int(value))
        message, success = super(BaseTheoryRoliePoly, self).set_param_value(
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
                self.parameters["tauR%02d" % i] = Parameter(
                    name="tauR%02d" % i,
                    value=0.5,
                    description="Rouse time of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.opt,
                    display_flag=True,
                    min_value=0)
            if (oldn > self.parameters["nmodes"].value):
                for i in range(self.parameters["nmodes"].value, oldn):
                    del self.parameters["G%02d" % i]
                    del self.parameters["tauD%02d" % i]
                    del self.parameters["tauR%02d" % i]
        return '', True


class CLTheoryRoliePoly(BaseTheoryRoliePoly, Theory):
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
            self.function = self.RoliePolyLAOS


class GUITheoryRoliePoly(BaseTheoryRoliePoly, QTheory):
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
                QIcon(':/Icon8/Images/new_icons/icon-shear.png'), "Shear Flow")
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
            self.function = self.RoliePolyLAOS

        self.tbutmodes = QToolButton()
        self.tbutmodes.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        self.get_modes_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-broadcasting.png'),
            "Get Modes")
        self.edit_modes_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-edit-file.png'),
            "Edit Modes")
        # self.plot_modes_action = menu.addAction(
        #     QIcon(':/Icon8/Images/new_icons/icons8-scatter-plot.png'),
        #     "Plot Modes")
        self.save_modes_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-save-Maxwell.png'),
            "Save Modes")
        self.tbutmodes.setDefaultAction(self.get_modes_action)
        self.tbutmodes.setMenu(menu)
        tb.addWidget(self.tbutmodes)
        #Show LVE button
        self.linearenvelope = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/lve-icon.png'),
            'Show Linear Envelope')
        self.linearenvelope.setCheckable(True)
        self.linearenvelope.setChecked(False)
        #Finite extensibility button
        self.with_fene_button = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-infinite.png'),
            'Finite Extensibility')
        self.with_fene_button.setCheckable(True)
        #SpinBox "nmodes"
        self.spinbox = QSpinBox()
        self.spinbox.setRange(
            0, self.parameters["nmodes"].value)  # min and max number of modes
        self.spinbox.setSuffix(" stretch")
        self.spinbox.setToolTip("Number of stretching modes")
        self.spinbox.setValue(self.parameters["nmodes"].value)  #initial value
        tb.addWidget(self.spinbox)

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
        # connection_id = self.plot_modes_action.triggered.connect(
        #     self.plot_modes_graph)
        connection_id = self.save_modes_action.triggered.connect(
            self.save_modes)
        connection_id = self.linearenvelope.triggered.connect(
            self.show_linear_envelope)
        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged)
        connection_id = self.with_fene_button.triggered.connect(
            self.handle_with_fene_button)
        connection_id = self.flowsolve_btn.triggered.connect(
            self.handle_flowsolve_btn)
            
            
    def handle_flowsolve_btn(self):
        """Save theory parameters in FlowSolve format"""

        #Get filename of RepTate project to open
        fpath, _ = QFileDialog.getSaveFileName(self,
                                               "Save Parameters to FowSolve",
                                               "data/", "FlowSolve (*.fsrep)")
        if fpath == '':
            return

        with open(fpath, 'w') as f:
            header = '#flowGen input\n'
            header += '# Generated with RepTate v%s %s\n' % (Version.VERSION,
                                                             Version.DATE)
            header += '# At %s on %s\n' % (time.strftime("%X"),
                                           time.strftime("%a %b %d, %Y"))
            f.write(header)

            f.write('\n#param global\n')
            f.write('constit roliepoly\n')
            # f.write('# or multip (for pompom) or polydisperse (for polydisperse Rolie-Poly)\n')

            f.write('\n#param constitutive\n')
            n = self.parameters['nmodes'].value
            nR = self.parameters['nstretch'].value

            # sort taud ascending order
            td = np.zeros(n)
            for i in range(n):
                td[i] = self.parameters["tauD%02d" % i].value
            args = np.argsort(td)

            modulus = 'modulus'
            taud = 'taud'
            tauR = 'tauR'
            lmax = 'lambdaMax'
            for i, arg in enumerate(args):
                modulus += ' %.6g' % self.parameters["G%02d" % arg].value
                taud += ' %.6g' % self.parameters["tauD%02d" % arg].value
                if n - i <= nR:
                    tauR += ' %.6g' % self.parameters["tauR%02d" % arg].value
                    lmax += ' %.6g' % self.parameters["lmax"].value
            f.write('%s\n%s\n%s\n' % (modulus, taud, tauR))
            if self.with_fene == FeneMode.with_fene:  # don't output lmax at all for infinite ex
                f.write('%s\n' % lmax)
            f.write('beta %.6g\n' % self.parameters["beta"].value)
            f.write('delta %.6g\n' % self.parameters["delta"].value)
            f.write('firstStretch %d\n' %
                    (1 + n - nR))  # +1 as flowsolve uses 1-n index not 0-n-1

            f.write('\n#end')

        QMessageBox.information(self, 'Success',
                                'Wrote FlowSolve parameters in \"%s\"' % fpath)

    def handle_with_fene_button(self, checked):
        if checked:
            self.with_fene = FeneMode.with_fene
            self.with_fene_button.setChecked(True)
            self.with_fene_button.setIcon(
                QIcon(':/Icon8/Images/new_icons/icons8-facebook-f.png'))
            self.parameters["lmax"].display_flag = True
            self.parameters["lmax"].opt_type = OptType.nopt
        else:
            self.with_fene = FeneMode.none
            self.with_fene_button.setChecked(False)
            self.with_fene_button.setIcon(
                QIcon(':/Icon8/Images/new_icons/icons8-infinite.png'))
            self.parameters["lmax"].display_flag = False
            self.parameters["lmax"].opt_type = OptType.const
        self.update_parameter_table()
        self.parent_dataset.handle_actionCalculate_Theory()

    def handle_spinboxValueChanged(self, value):
        nmodes = self.parameters["nmodes"].value
        self.set_param_value("nstretch", min(nmodes, value))
        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()

    def Qhide_theory_extras(self, show):
        """Uncheck the LVE button. Called when curent theory is changed
        
        [description]
        """
        if show:
            self.LVEenvelopeseries.set_visible(self.linearenvelope.isChecked())
        else:
            self.LVEenvelopeseries.set_visible(False)

    def show_linear_envelope(self, state):
        self.extra_graphic_visible(state)
        # self.LVEenvelopeseries.set_visible(self.linearenvelope.isChecked())
        # self.plot_theory_stuff()
        # self.parent_dataset.parent_application.update_plot()

    def plot_theory_stuff(self):
        """[summary]
        
        [description]
        """
        if not isinstance(self.parent_dataset.parent_application, GUIApplicationLAOS):
            data_table_tmp = DataTable(self.axarr)
            data_table_tmp.num_columns = 2
            data_table_tmp.num_rows = 100
            data_table_tmp.data = np.zeros((100, 2))

            times = np.logspace(-2, 3, 100)
            data_table_tmp.data[:, 0] = times
            nmodes = self.parameters["nmodes"].value
            data_table_tmp.data[:, 1] = 0
            fparamaux = {}
            fparamaux["gdot"] = 1e-8
            for i in range(nmodes):
                if self.stop_theory_flag:
                    break
                G = self.parameters["G%02d" % i].value
                tauD = self.parameters["tauD%02d" % i].value
                data_table_tmp.data[:, 1] += G * fparamaux["gdot"] * tauD * (
                    1 - np.exp(-times / tauD))
            if self.flow_mode == FlowMode.uext:
                data_table_tmp.data[:, 1] *= 3.0
            view = self.parent_dataset.parent_application.current_view
            try:
                x, y, success = view.view_proc(data_table_tmp, fparamaux)
            except TypeError as e:
                print(e)
                return
            self.LVEenvelopeseries.set_data(x[:, 0], y[:, 0])

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

    # def plot_modes_graph(self):
    #     pass
