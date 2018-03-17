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
"""Module TheoryBlendRoliePoly

Module for the Rolie-Poly theory for the non-linear flow of entangled polymers.

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

import rp_blend_ctypes_helper as rpch


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
    def __init__(self,
                 parent=None,
                 phi=None,
                 taud=None,
                 taur=None,
                 MAX_MODES=0):
        super(EditModesDialog, self).__init__(parent)

        self.setWindowTitle("Edit volume fractions and relaxation times")
        layout = QVBoxLayout(self)
        nmodes = len(phi)

        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, MAX_MODES)  # min and max number of modes
        self.spinbox.setSuffix(" modes")
        self.spinbox.setValue(nmodes)  #initial value
        layout.addWidget(self.spinbox)

        self.table = SpreadsheetWidget()  #allows copy/paste
        self.table.setRowCount(nmodes)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["phi", "tauD", "tauR"])
        for i in range(nmodes):
            self.table.setItem(i, 0, QTableWidgetItem("%g" % phi[i]))
            self.table.setItem(i, 1, QTableWidgetItem("%g" % taud[i]))
            self.table.setItem(i, 2, QTableWidgetItem("%g" % taur[i]))

        layout.addWidget(self.table)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept_)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged)

    def accept_(self):
        sum = 0
        for i in range(self.table.rowCount()):
            sum += float(self.table.item(i, 0).text())
        if abs(sum - 1) < 0.02:
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'phi must add up to 1')

    def handle_spinboxValueChanged(self, value):
        nrow_old = self.table.rowCount()
        self.table.setRowCount(value)
        for i in range(nrow_old, value):  #create extra rows with defaut values
            self.table.setItem(i, 0, QTableWidgetItem("0"))
            self.table.setItem(i, 1, QTableWidgetItem("100"))
            self.table.setItem(i, 2, QTableWidgetItem("1"))


class TheoryBlendRoliePoly(CmdBase):
    """Blend of Rolie-Poly equations for the nonlinear predictions of polydisperse melts

    * **Function**
        .. math::
            \\boldsymbol \\sigma = G_N^0 \\sum_i \\text{fene}(\\lambda_i) \\phi_i \\boldsymbol A_i

        where
            .. math::
                \\boldsymbol A_i &= \\sum_j \\phi_j \\boldsymbol A_{ij}\\\\
                \\lambda_i &= \\left( \\dfrac{\\text{Tr}  \\boldsymbol A_i}{3}  \\right)^{1/2}\\\\
                \\stackrel{\\nabla}{\\boldsymbol  A_{ij}} &=
                -\\dfrac{1}{2\\tau_{\\mathrm d,i}} (\\boldsymbol A_{ij} - \\boldsymbol I)
                -\\dfrac{2}{\\tau_{\\mathrm s,i}} \\dfrac{\\lambda_i - 1}{\\lambda_i} \\boldsymbol A_{ij}
                -\\left( \\dfrac{\\beta_\\text{th}}{2\\tau_{\\mathrm d,j}} 
                + \\beta_\\text{CCR}\\dfrac{2}{\\tau_{\\mathrm s,j}} \\dfrac{\\lambda_j - 1}{\\lambda_j}\\lambda_i^{2\\delta} \\right)
                (\\boldsymbol A_{ij} - \\boldsymbol I)

    * **Parameters**
       - ``GN0`` :math:`\\equiv G_N^0`: Plateau modulus
       - ``beta`` :math:`\\equiv\\beta_\\text{CCR}`: Rolie-Poly CCR parameter
       - ``delta`` :math:`\\equiv\\delta`: Rolie-Poly CCR exponent
       - ``phi_i`` :math:`\\equiv\\phi_i`: Volume fraction of species :math:`i`
       - ``tauD_i`` :math:`\\equiv\\tau_{\\mathrm d,i}`: Maxwell relaxation times for the stress of species :math:`i` (includes both reptation and constraint release mechamisms)
       - ``tauR_i`` :math:`\\equiv\\tau_{\\mathrm s,i}`: Stretch relaxation time of species :math:`i`
    """
    thname = "BlendRoliePoly"
    description = "BlendRoliePoly"
    citations = ""

    def __new__(cls, name="ThBlendRoliePoly", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUITheoryBlendRoliePoly(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryBlendRoliePoly(
                name, parent_dataset, ax)


class BaseTheoryBlendRoliePoly:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/en/latest/manual/Applications/NLVE/Theory/theory.html#rolie-poly-blend-equations'
    single_file = False

    def __init__(self,
                 name="ThBlendRoliePoly",
                 parent_dataset=None,
                 axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"ThBlendRoliePoly"})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.BlendRoliePoly
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
        self.parameters["GN0"] = Parameter(
            name="GN0",
            value=1000.0,
            description="Plateau modulus",
            type=ParameterType.real,
            opt_type=OptType.const,
            bracketed=True,
            min_value=0)
        nmode = self.parameters["nmodes"].value
        for i in range(nmode):
            self.parameters["phi%02d" % i] = Parameter(
                name="phi%02d" % i,
                value=1. / nmode,
                description="Volume fraction of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.nopt,
                display_flag=False,
                bracketed=True,
                min_value=0)
            self.parameters["tauD%02d" % i] = Parameter(
                name="tauD%02d" % i,
                value=100.0,
                description="Terminal time of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.nopt,
                display_flag=False,
                bracketed=True,
                min_value=0)
            self.parameters["tauR%02d" % i] = Parameter(
                name="tauR%02d" % i,
                value=1,
                description="Rouse time of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.opt,
                bracketed=True,
                min_value=0)

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
        """Called when the theory tab is closed
        
        [description]
        """
        self.extra_graphic_visible(False)
        self.ax.lines.remove(self.LVEenvelopeseries)

    def show_theory_extras(self, show=False):
        """Called when the active theory is changed
        
        [description]
        """
        if CmdBase.mode == CmdMode.GUI:
            self.Qhide_theory_extras(show)
        self.extra_graphic_visible(show)

    def extra_graphic_visible(self, state):
        """[summary]
        
        [description]
        """
        self.LVEenvelopeseries.set_visible(state)
        self.parent_dataset.parent_application.update_plot()

    def get_modes(self):
        """[summary]
        
        [description]
        
        Returns:
            - [type] -- [description]
        """
        pass
        # nmodes = self.parameters["nmodes"].value
        # tau = np.zeros(nmodes)
        # G = np.zeros(nmodes)
        # for i in range(nmodes):
        #     tau[i] = self.parameters["tauD%02d" % i].value
        #     G[i] = self.parameters["G%02d" % i].value
        # return tau, G

    def set_modes(self, tau, G):
        """[summary]
        
        [description]
        
        Arguments:
            - - tau {[type]} -- [description]
            - - G {[type]} -- [description]
        """
        nmodes = len(tau)
        self.set_param_value("nmodes", nmodes)
        sum_G = G.sum()

        for i in range(nmodes):
            self.set_param_value("tauD%02d" % i, tau[i])
            self.set_param_value("phi%02d" % i, G[i] / sum_G)

    def sigmadot_shear(self, sigma, t, p):
        """Rolie-Poly differential equation under *shear* flow
        with stretching and finite extensibility if selected
        
        [description]
        
        Arguments:
            - sigma {array} -- vector of state variables, sigma = [sxx, syy, sxy]
            - t {float} -- time
            - p {array} -- vector of the parameters, p = [tauD, tauR, beta, delta, gammadot]
        """
        tmax = p[-1]
        if t >= tmax * self.count:
            self.Qprint("--", end='')
            self.count += 0.2

        # Calling C function:
        if self.with_fene == FeneMode.with_fene:
            wfene = 1
        else:
            wfene = 0
        return rpch.compute_derivs_shear(sigma, p, t, wfene)

        # With Python:
        # n, lmax, phi, taud, taus, beta, delta, gamma_dot, tmax = p
        # c = 3 # number of components in sigma (xx, yy, xy)
        # deriv = np.zeros(n * n * c)
        # # Create the vector with the time derivative of sigma
        # stretch = np.zeros(n)
        # for i in range(n):
        #     I = c * n * i
        #     trace = 0
        #     for j in range(n):
        #         sjxx = sigma[I + c * j]
        #         sjyy = sigma[I + c * j + 1]
        #         trace += phi[j] * (sjxx + 2 * sjyy)
        #     stretch[i] = sqrt(trace / 3.0)

        # for i in range(n):
        #     I = c * n * i
        #     tdi = taud[i]
        #     tsi = taus[i]
        #     li = stretch[i]
        #     ret = 2.0 * (1.0 - 1.0 / li) / tsi
        #     if self.with_fene == FeneMode.with_fene:
        #         fene = self.calculate_fene(li * li, lmax)
        #         ret *= fene

        #     for j in range(n):
        #         tdj = taud[j]
        #         tsj = taus[j]
        #         sxx = sigma[I + c * j]
        #         syy = sigma[I + c * j + 1]
        #         sxy = sigma[I + c * j + 2]
        #         lj = stretch[j]
        #         rep = 1 / (2 * tdi) + 1 / (2 * tdj) # assumes beta_thermal = 1

        #         auxj = 2.0 * beta * (1.0 - 1.0 / lj) / tsj
        #         if self.with_fene == FeneMode.with_fene:
        #             fene = self.calculate_fene(lj * lj, lmax)
        #             auxj *= fene
        #         rccr = auxj * li**(2*delta)

        #         dsxx = 2 * gamma_dot * sxy - rep * (sxx - 1.0) - ret * sxx - rccr * (sxx - 1.0)
        #         dsyy = - rep * (syy - 1.0) - ret * syy - rccr * (syy - 1.0)
        #         dsxy = gamma_dot * syy - rep * sxy - ret * sxy - rccr * sxy

        #         deriv[I + c * j] = dsxx
        #         deriv[I + c * j + 1] = dsyy
        #         deriv[I + c * j + 2] = dsxy
        # return deriv

    def sigmadot_uext(self, sigma, t, p):
        """Rolie-Poly differential equation under *uniaxial elongational* flow
        with stretching and finite extensibility if selecter

        [description]

        Arguments:
            - sigma {array} -- vector of state variables, sigma = [sxx, syy]
            - t {float} -- time
            - p {array} -- vector of the parameters, p = [tauD, tauR, beta, delta, gammadot]
        """
        tmax = p[-1]
        if t >= tmax * self.count:
            self.Qprint("--", end='')
            # self.Qprint("%4d%% done" % (self.count*100))
            self.count += 0.2

        # Calling C function:
        if self.with_fene == FeneMode.with_fene:
            wfene = 1
        else:
            wfene = 0
        return rpch.compute_derivs_uext(sigma, p, t, wfene)

        # With Python:
        # n, lmax, phi, taud, taus, beta, delta, epsilon_dot, tmax = p
        # c = 2 # number of components in sigma (xx, yy, xy)
        # deriv = np.zeros(n * n * c)
        # # Create the vector with the time derivative of sigma
        # stretch = np.zeros(n)
        # for i in range(n):
        #     I = c * n * i
        #     trace = 0
        #     for j in range(n):
        #         sjxx = sigma[I + c * j]
        #         sjyy = sigma[I + c * j + 1]
        #         trace += phi[j] * (sjxx + 2 * sjyy)
        #     stretch[i] = sqrt(trace / 3.0)

        # for i in range(n):
        #     I = c * n * i
        #     tdi = taud[i]
        #     tsi = taus[i]
        #     li = stretch[i]
        #     ret = 2.0 * (1.0 - 1.0 / li) / tsi
        #     if self.with_fene == FeneMode.with_fene:
        #         fene = self.calculate_fene(li * li, lmax)
        #         ret *= fene

        #     for j in range(n):
        #         tdj = taud[j]
        #         tsj = taus[j]
        #         sxx = sigma[I + c * j]
        #         syy = sigma[I + c * j + 1]
        #         lj = stretch[j]
        #         rep = 1.0 / (2 * tdi) + 1.0 / (2 * tdj) # assumes beta_thermal = 1

        #         auxj = 2.0 * beta * (1.0 - 1.0 / lj) / tsj
        #         if self.with_fene == FeneMode.with_fene:
        #             fene = self.calculate_fene(lj * lj, lmax)
        #             auxj *= fene
        #         rccr = auxj * li**(2*delta)

        #         dsxx =  2.0 * epsilon_dot * sxx - rep * (sxx - 1.0) - ret * sxx - rccr * (sxx - 1.0)
        #         dsyy = -epsilon_dot * syy - rep * (syy - 1.0) - ret * syy - rccr * (syy - 1.0)

        #         deriv[I + c * j] = dsxx
        #         deriv[I + c * j + 1] = dsyy
        # return deriv

    def calculate_fene(self, l_square, lmax):
        """calculate finite extensibility function value"""
        ilm2 = 1.0 / (lmax * lmax)  # 1/lambda_max^2
        l2_lm2 = l_square * ilm2  # (lambda/lambda_max)^2
        return (3.0 - l2_lm2) / (1.0 - l2_lm2) * (1.0 - ilm2) / (3.0 - ilm2)

    def BlendRoliePoly(self, f=None):
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

        #flow geometry
        if self.flow_mode == FlowMode.shear:
            sigma0 = ([1.0, 1.0, 0.0] *
                      (nmodes * nmodes))  # sxx_ij, syy_ij, sxy_ij
            pde_stretch = self.sigmadot_shear
        elif self.flow_mode == FlowMode.uext:
            sigma0 = ([1.0, 1.0] * (nmodes * nmodes))  # sxx_ij, syy_ij
            pde_stretch = self.sigmadot_uext
        else:
            return

        taud_arr = []
        taus_arr = []
        phi_arr = []
        for i in range(nmodes):
            taud_arr.append(self.parameters["tauD%02d" % i].value)
            taus_arr.append(self.parameters["tauR%02d" % i].value)
            phi_arr.append(self.parameters["phi%02d" % i].value)
        tmax = t[-1]
        p = [
            nmodes, lmax, phi_arr, taud_arr, taus_arr, beta, delta, flow_rate,
            tmax
        ]
        self.count = 0.2
        self.Qprint('Rate %.3g\n  0%% ' % flow_rate, end='')
        sig = odeint(
            pde_stretch, sigma0, t, args=(p, ), atol=abserr, rtol=relerr)
        self.Qprint(' 100%')
        # sig.shape is (len(t), 3*n^2) in shear
        if self.flow_mode == FlowMode.shear:
            # every 3 component we find xx, yy, xy, starting at 0, 1, or 2; and remove t=0
            # sxx_t = sig[1:, 0::3] # len(t) - 1 rows and n^2 cols
            # syy_t = sig[1:, 1::3] # len(t) - 1 rows and n^2 cols
            # sxy_t = sig[1:, 2::3] # len(t) - 1 rows and n^2 cols
            # nt = len(sxx_t)
            c = 3
            sig = sig[1:, :]
            nt = len(sig)
            lsq = np.zeros((nt, nmodes))
            if self.with_fene == FeneMode.with_fene:
                for i in range(nmodes):
                    I = c * nmodes * i
                    trace_arr = np.zeros(nt)
                    for j in range(nmodes):
                        # trace_arr += phi_arr[j] * (sxx_t[:, I + j] + 2 * syy_t[:, I + j])
                        trace_arr += phi_arr[j] * (
                            sig[:, I + c * j] + 2 * sig[:, I + c * j + 1])
                    lsq[:, i] = trace_arr / 3.0  # len(t) rows and n cols

            for i in range(nmodes):
                I = c * nmodes * i
                temp_arr = np.zeros(nt)
                for j in range(nmodes):
                    temp_arr += phi_arr[j] * sig[:, I + c * j + 2]
                if self.with_fene == FeneMode.with_fene:
                    tt.data[:, 1] += phi_arr[i] * self.calculate_fene(
                        lsq[:, i], lmax) * temp_arr
                else:
                    tt.data[:, 1] += phi_arr[i] * temp_arr
            tt.data[:, 1] *= self.parameters["GN0"].value

        if self.flow_mode == FlowMode.uext:
            # every 2 component we find xx, yy, starting at 0, or 1; and remove t=0
            # sxx_t = sig[1:, 0::2] # len(t) - 1 rows and n^2 cols
            # syy_t = sig[1:, 1::2] # len(t) - 1 rows and n^2 cols

            # nt = len(sxx_t)
            c = 2
            sig = sig[1:, :]
            nt = len(sig)
            lsq = np.zeros((nt, nmodes))
            if self.with_fene == FeneMode.with_fene:
                for i in range(nmodes):
                    I = c * nmodes * i
                    trace_arr = np.zeros(nt)
                    for j in range(nmodes):
                        trace_arr += phi_arr[j] * (
                            sig[:, I + c * j] + 2 * sig[:, I + c * j + 1])
                    lsq[:, i] = trace_arr / 3.0  # len(t) rows and n cols

            for i in range(nmodes):
                I = c * nmodes * i
                temp_arr = np.zeros(nt)
                for j in range(nmodes):
                    temp_arr += phi_arr[j] * (
                        sig[:, I + c * j] - sig[:, I + c * j + 1])
                if self.with_fene == FeneMode.with_fene:
                    tt.data[:, 1] += phi_arr[i] * self.calculate_fene(
                        lsq[:, i], lmax) * temp_arr
                else:
                    tt.data[:, 1] += phi_arr[i] * temp_arr
            tt.data[:, 1] *= self.parameters["GN0"].value

    def set_param_value(self, name, value):
        """[summary]
        
        [description]
        
        Arguments:
            - name {[type]} -- [description]
            - value {[type]} -- [description]
        """
        if (name == "nmodes"):
            oldn = self.parameters["nmodes"].value
            # self.spinbox.setMaximum(int(value))
        message, success = super(BaseTheoryBlendRoliePoly,
                                 self).set_param_value(name, value)
        if not success:
            return message, success
        if (name == "nmodes"):
            for i in range(self.parameters["nmodes"].value):
                self.parameters["phi%02d" % i] = Parameter(
                    name="phi%02d" % i,
                    value=0.0,
                    description="Volume fraction of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.nopt,
                    display_flag=False,
                    bracketed=True,
                    min_value=0)
                self.parameters["tauD%02d" % i] = Parameter(
                    name="tauD%02d" % i,
                    value=100.0,
                    description="Terminal time of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.nopt,
                    display_flag=False,
                    bracketed=True,
                    min_value=0)
                self.parameters["tauR%02d" % i] = Parameter(
                    name="tauR%02d" % i,
                    value=1,
                    description="Rouse time of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.opt,
                    display_flag=True,
                    bracketed=True,
                    min_value=0)
            if (oldn > self.parameters["nmodes"].value):
                for i in range(self.parameters["nmodes"].value, oldn):
                    del self.parameters["phi%02d" % i]
                    del self.parameters["tauD%02d" % i]
                    del self.parameters["tauR%02d" % i]
        return '', True


class CLTheoryBlendRoliePoly(BaseTheoryBlendRoliePoly, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name="ThBlendRoliePoly", parent_dataset=None, ax=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)


class GUITheoryBlendRoliePoly(BaseTheoryBlendRoliePoly, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self, name="ThBlendRoliePoly", parent_dataset=None, ax=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))

        self.tbutflow = QToolButton()
        self.tbutflow.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        self.shear_flow_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-garden-shears.png'),
            "Shear Flow")
        self.extensional_flow_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-socks.png'),
            "Extensional Flow")
        if self.flow_mode == FlowMode.shear:
            self.tbutflow.setDefaultAction(self.shear_flow_action)
        else:
            self.tbutflow.setDefaultAction(self.extensional_flow_action)
        self.tbutflow.setMenu(menu)
        tb.addWidget(self.tbutflow)

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
        self.tbutmodes.setDefaultAction(self.get_modes_action)
        self.tbutmodes.setMenu(menu)
        tb.addWidget(self.tbutmodes)
        #Show LVE button
        self.linearenvelope = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-visible.png'),
            'Show Linear Envelope')
        self.linearenvelope.setCheckable(True)
        self.linearenvelope.setChecked(False)
        #Finite extensibility button
        self.with_fene_button = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-infinite.png'),
            'Finite Extensibility')
        self.with_fene_button.setCheckable(True)
        # #SpinBox "nmodes"
        # self.spinbox = QSpinBox()
        # self.spinbox.setRange(0, self.parameters["nmodes"].value)  # min and max number of modes
        # self.spinbox.setSuffix(" stretch")
        # self.spinbox.setToolTip("Number of stretching modes")
        # self.spinbox.setValue(self.parameters["nmodes"].value)  #initial value
        # tb.addWidget(self.spinbox)

        self.thToolsLayout.insertWidget(0, tb)

        connection_id = self.shear_flow_action.triggered.connect(
            self.select_shear_flow)
        connection_id = self.extensional_flow_action.triggered.connect(
            self.select_extensional_flow)
        connection_id = self.get_modes_action.triggered.connect(
            self.get_modes_reptate)
        connection_id = self.edit_modes_action.triggered.connect(
            self.edit_modes_window)
        connection_id = self.plot_modes_action.triggered.connect(
            self.plot_modes_graph)
        connection_id = self.linearenvelope.triggered.connect(
            self.show_linear_envelope)
        # connection_id = self.spinbox.valueChanged.connect(
        #     self.handle_spinboxValueChanged)
        connection_id = self.with_fene_button.triggered.connect(
            self.handle_with_fene_button)

    def handle_with_fene_button(self, checked):
        if checked:
            self.with_fene = FeneMode.with_fene
            self.with_fene_button.setIcon(
                QIcon(':/Icon8/Images/new_icons/icons8-facebook-f.png'))
            self.parameters["lmax"].display_flag = True
            self.parameters["lmax"].opt_type = OptType.nopt
        else:
            self.with_fene = FeneMode.none
            self.with_fene_button.setIcon(
                QIcon(':/Icon8/Images/new_icons/icons8-infinite.png'))
            self.parameters["lmax"].display_flag = False
            self.parameters["lmax"].opt_type = OptType.const
        self.parent_dataset.handle_actionCalculate_Theory()

    # def handle_spinboxValueChanged(self, value):
    #     nmodes = self.parameters["nmodes"].value
    #     self.set_param_value("nstretch", min(nmodes, value))
    #     self.handle_actionCalculate_Theory()

    def Qhide_theory_extras(self, state):
        """Uncheck the LVE button. Called when curent theory is changed
        
        [description]
        """
        self.linearenvelope.setChecked(state)

    def show_linear_envelope(self, state):
        self.extra_graphic_visible(state)
        # self.LVEenvelopeseries.set_visible(self.linearenvelope.isChecked())
        # self.plot_theory_stuff()
        # self.parent_dataset.parent_application.update_plot()

    def select_shear_flow(self):
        self.flow_mode = FlowMode.shear
        self.tbutflow.setDefaultAction(self.shear_flow_action)

    def select_extensional_flow(self):
        self.flow_mode = FlowMode.uext
        self.tbutflow.setDefaultAction(self.extensional_flow_action)

    def get_modes_reptate(self):
        self.Qcopy_modes()
        self.parent_dataset.handle_actionCalculate_Theory()

    def edit_modes_window(self):
        nmodes = self.parameters["nmodes"].value
        phi = np.zeros(nmodes)
        taud = np.zeros(nmodes)
        taur = np.zeros(nmodes)
        for i in range(nmodes):
            phi[i] = self.parameters["phi%02d" % i].value
            taud[i] = self.parameters["tauD%02d" % i].value
            taur[i] = self.parameters["tauR%02d" % i].value
        d = EditModesDialog(self, phi, taud, taur, self.MAX_MODES)
        if d.exec_():
            nmodes = d.table.rowCount()
            self.set_param_value("nmodes", nmodes)
            # self.set_param_value("nstretch", nmodes)
            success = True
            for i in range(nmodes):
                msg, success1 = self.set_param_value("phi%02d" % i,
                                                     d.table.item(i, 0).text())
                msg, success2 = self.set_param_value("tauD%02d" % i,
                                                     d.table.item(i, 1).text())
                msg, success3 = self.set_param_value("tauR%02d" % i,
                                                     d.table.item(i, 2).text())
                success *= success1 * success2 * success3
            if not success:
                QMessageBox.warning(
                    self, 'Error',
                    'Some parameter(s) could not be updated.\nPlease try again.'
                )
            else:
                self.handle_actionCalculate_Theory()

    def plot_modes_graph(self):
        pass
