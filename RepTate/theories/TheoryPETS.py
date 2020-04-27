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
"""Module TheoryPETS

Module for the PETS theory for the non-linear flow of entangled polymers.

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


class FlowMode(Enum):
    """Defines the flow geometry used
    
    Parameters can be:
        - shear: Shear flow
        - uext: Uniaxial extension flow
    """
    shear = 0
    uext = 1


class TheoryPETS(CmdBase):
    """Preaveraged model for Entangled Telechelic Star polymers: This theory is intended for the prediction of non-linear transient flows of 
entangled telechelic (with sticky functional groups at the chain-ends) star polymers. 

    * **Parameters**
       - ``G`` : Plateau Modulus
       - ``tauD`` : Orientation relaxation time
       - ``tauS`` : Stretch Relxation time
       - ``tau_as`` : Typical time the sticker spends associated
       - ``tau_free`` : Typical time the sticker spends free
       - ``lmax`` : Maximum extensibility
       - ``beta`` : CCR coefficient
       - ``delta`` : CCR exponent
       - ``Z`` : Entanglement number
       - ``r_a`` : Ratio of sticker size to tube diameter
    """
    thname = "PETS"
    description = "Preaveraged model for entangled telechelic star polymers"
    citations = ["Boudara, V.A.H, and D.J. Read, J. Rheol., 61, 339-362 (2017)"]
    doi = ["http://dx.doi.org/10.1122/1.4974908"]

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
        return GUITheoryPETS(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI
                    ) else CLTheoryPETS(
                        name, parent_dataset, ax)


class BaseTheoryPETS:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/NLVE/Theory/theory.html#PETS-equation'
    single_file = False
    thname = TheoryPETS.thname
    citations = TheoryPETS.citations
    doi = TheoryPETS.doi

    def __init__(self, name="", parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.PETS
        self.has_modes = True
        EPSILON = np.finfo(float).resolution
        self.parameters["G"] = Parameter(
            name="G",
            value=1000.0,
            description="Plateau Modulus",
            type=ParameterType.real,
            opt_type=OptType.nopt,
            min_value=0)
        self.parameters["tauD"] = Parameter(
            name="tauD",
            value=100.0,
            description="Orientation relaxation time",
            type=ParameterType.real,
            opt_type=OptType.nopt,
            min_value=EPSILON)
        self.parameters["tauS"] = Parameter(
            name="tauS",
            value=1,
            description="Stretch Relxation time",
            type=ParameterType.real,
            opt_type=OptType.nopt,
            min_value=EPSILON)
        self.parameters["tau_as"] = Parameter(
            name="tau_as",
            value=1e2,
            description="Typical time the sticker spends associated",
            type=ParameterType.real,
            opt_type=OptType.nopt,
            min_value=EPSILON)
        self.parameters["tau_free"] = Parameter(
            name="tau_free",
            value=1e-2,
            description="Typical time the sticker spends free",
            type=ParameterType.real,
            opt_type=OptType.nopt,
            min_value=EPSILON)
        self.parameters["lmax"] = Parameter(
            name="lmax",
            value=10.0,
            description="Maximum extensibility",
            type=ParameterType.real,
            opt_type=OptType.const,
            display_flag=True,
            min_value=1.01)
        self.parameters["beta"] = Parameter(
            name="beta",
            value=1,
            description="CCR coefficient",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            max_value=2)
        self.parameters["delta"] = Parameter(
            name="delta",
            value=-0.5,
            description="CCR exponent",
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters["Z"] = Parameter(
            name="Z",
            value=10,
            description="Entanglement number",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=1)
        self.parameters["r_a"] = Parameter(
            name="r_a",
            value=0.01,
            description="Ratio of sticker size to tube diameter",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=EPSILON)

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
        self.init_flow_mode()

    def set_extra_data(self, extra_data):
        """Set extra data when loading project"""
        pass

    def get_extra_data(self):
        """Set extra_data when saving project"""
        pass

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
        tau = np.zeros(1)
        G = np.zeros(1)
        tau[0] = self.parameters["tauD"].value
        G[0] = self.parameters["G"].value
        return tau, G, True

    def sigmadot_shear(self, vec, t, p):
        """PETS differential equation under *shear* flow
        with stretching and finite extensibility if selected
        
        [description]
        
        Arguments:
            - sigma {array} -- vector of state variables, vec = [f, ldeq, QAxx, QAyy, QAxy, QDxx, QDyy, QDxy]
            - t {float} -- time
            - p {array} -- vector of the parameters, p = [tauD, tauS, beta, delta, gammadot]
        """
        if self.stop_theory_flag:
            raise EndComputationRequested
        f, ldeq, QAxx, QAyy, QAxy, QDxx, QDyy, QDxy = vec
        Z, r_a, lmax, tauD, tauS, tau_as, tau_free, beta, delta, gammadot = p

        # Create the vector with the time derivative of sigma

        lm2 = lmax ** 2
        trQA = QAxx + 2 * QAyy
        trQD = QDxx + 2 * QDyy
        la = ((lm2 * trQA)/ (3*lm2 - 3 + trQA))**0.5
        ld = ((lm2 * trQD)/ (3*lm2 - 3 + trQD))**0.5
        fenela = (3 * lm2 - 3 + trQA) / (3 * lm2)
        feneld = (3 * lm2 - 3 + trQD) / (3 * lm2)
        feneEq = (1 - 1/lm2) / (1 - ldeq**2 / lm2)
        
        r_freeas = 1 / tau_free
        r_asfree = 1 / tau_as * ( (1 - la**2 / lm2) / (
            1 - 1/lm2 * (la - r_a / Z)**2) * (1 - (1 - r_a / Z) / lm2) / (1 - 1 / lm2))**(-1.5 * Z * lm2 * (1 - 1/lm2))
        if r_asfree > self.RD_MAX:
            r_asfree = self.RD_MAX
        nu = 2 * (1 - f) * (
            1 - 1 / ldeq) / tauS * feneEq + f * r_asfree * 2 * (la - ld) / (
                la + ld)
        ###
        gxx = 2 * gammadot * QAxy - beta * nu * (QAxx - fenela) / la
        gyy = -beta * nu * (QAyy - fenela) / la
        gxy = gammadot * QAyy - beta * nu * QAyy / la
        trg_lm = (gxx + 2 * gyy) / (3 * lm2 - 3)

        dQAxx = gxx + trg_lm * QAxx + r_freeas * (1 - f) / f * (QDxx - QAxx)
        dQAyy = gyy + trg_lm * QAyy + r_freeas * (1 - f) / f * (QDyy - QAyy)
        dQAxy = gxy + trg_lm * QAxy + r_freeas * (1 - f) / f * (QDxy - QAxy)

        #####
        hxx = 2 * gammadot * QDxy - beta * nu * (QDxx - feneld) / ld - (
            QDxx - feneld) / tauD - 2 * (1 - 1 / ld) / tauS * feneld * QDxx
        hyy = -beta * nu * (QDyy - feneld) / ld - (
            QDyy - feneld) / tauD - 2 * (1 - 1 / ld) / tauS * feneld * QDyy
        hxy = gammadot * QDyy - beta * nu * QDxy / ld - QDxy / tauD - 2 * (
            1 - 1 / ld) / tauS * feneld * QDxy
        trh_lm = (hxx + 2 * hyy) / (3 * lm2 - 3)

        dQDxx = hxx + trh_lm * QDxx + r_asfree * f / (1 - f) * (QAxx - QDxx)
        dQDyy = hyy + trh_lm * QDyy + r_asfree * f / (1 - f) * (QAyy - QDyy)
        dQDxy = hxy + trh_lm * QDxy + r_asfree * f / (1 - f) * (QAxy - QDxy)

        ###
        dldeq = gammadot * QDxy / trQD * ldeq - (ldeq - 1)/tauS * feneEq + f * r_asfree * (la - ldeq)
        ###
        df = r_freeas * (1 - f) - r_asfree * f

        return [df, dldeq, dQAxx, dQAyy, dQAxy, dQDxx, dQDyy, dQDxy]

    def sigmadot_uext(self, vec, t, p):
        """PETS differential equation under *uext* flow
        with stretching and finite extensibility if selected
        
        [description]
        
        Arguments:
            - sigma {array} -- vector of state variables, vec = [f, ldeq, QAxx, QAyy, QDxx, QDyy]
            - t {float} -- time
            - p {array} -- vector of the parameters, p = [tauD, tauS, beta, delta, epsilon_dot]
        """
        if self.stop_theory_flag:
            raise EndComputationRequested
        f, ldeq, QAxx, QAyy, QDxx, QDyy = vec

        Z, r_a, lmax, tauD, tauS, tau_as, tau_free, beta, delta, epsilon_dot = p

        # Create the vector with the time derivative of sigma

        lm2 = lmax ** 2
        trQA = QAxx + 2 * QAyy
        trQD = QDxx + 2 * QDyy
        la = ((lm2 * trQA)/ (3*lm2 - 3 + trQA))**0.5
        ld = ((lm2 * trQD)/ (3*lm2 - 3 + trQD))**0.5
        fenela = (3 * lm2 - 3 + trQA) / (3 * lm2)
        feneld = (3 * lm2 - 3 + trQD) / (3 * lm2)
        feneEq = (1 - 1/lm2) / (1 - ldeq**2 / lm2)
        
        r_freeas = 1 / tau_free
        r_asfree = 1 / tau_as * ((1 - la**2 / lm2) / (
            1 - 1/lm2 * (la - r_a / Z)**2 * (1 - (1 - r_a / Z) / lm2) / (1 - 1 / lm2)) )**(-1.5 * Z * lm2)
        if r_asfree > self.RD_MAX:
            r_asfree = self.RD_MAX
        nu = 2 * (1 - f) * (
            1 - 1 / ldeq) / tauS * feneEq + f * r_asfree * 2 * (la - ld) / (
                la + ld)
        ###
        gxx = 2.0 * epsilon_dot * QAxx - beta * nu * (QAxx - fenela) / la
        gyy = -epsilon_dot * QAyy -beta * nu * (QAyy - fenela) / la
        trg_lm = (gxx + 2 * gyy) / (3 * lm2 - 3)

        dQAxx = gxx + trg_lm * QAxx + r_freeas * (1 - f) / f * (QDxx - QAxx)
        dQAyy = gyy + trg_lm * QAyy + r_freeas * (1 - f) / f * (QDyy - QAyy)

        #####
        hxx = 2.0 * epsilon_dot * QDxx - beta * nu * (QDxx - feneld) / ld - (
            QDxx - feneld) / tauD - 2 * (1 - 1 / ld) / tauS * feneld * QDxx
        hyy = -epsilon_dot * QDyy -beta * nu * (QDyy - feneld) / ld - (
            QDyy - feneld) / tauD - 2 * (1 - 1 / ld) / tauS * feneld * QDyy
        trh_lm = (hxx + 2 * hyy) / (3 * lm2 - 3)

        dQDxx = hxx + trh_lm * QDxx + r_asfree * f / (1 - f) * (QAxx - QDxx)
        dQDyy = hyy + trh_lm * QDyy + r_asfree * f / (1 - f) * (QAyy - QDyy)

        ###
        dldeq = epsilon_dot * (QDxx - QDyy) / trQD * ldeq - (ldeq - 1)/tauS * feneEq + f * r_asfree * (la - ldeq)
        ###
        df = r_freeas * (1 - f) - r_asfree * f
        
        # if (t< .1):
        #     print("\n time=%.3g" % t)
        #     print("f", vec[0])
        #     print("ldeq", vec[1])
        #     print("QAxx", vec[2])
        #     print("QAyy", vec[3])
        #     print("QDxx", vec[4])
        #     print("QDyy", vec[5])
        #     print("r_freeas", r_freeas)
        #     print("r_asfree", r_asfree)
        #     print("df", df)

        return [df, dldeq, dQAxx, dQAyy, dQDxx, dQDyy]

    def PETS(self, f=None):
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

        flow_rate = float(f.file_parameters["gdot"])
        delta = self.parameters["delta"].value
        beta = self.parameters["beta"].value
        tau_free = self.parameters['tau_free'].value
        tau_as = self.parameters['tau_as'].value
        tauS = self.parameters["tauS"].value
        tauD = self.parameters["tauD"].value
        lmax = self.parameters["lmax"].value
        r_a = self.parameters['r_a'].value
        Z = self.parameters['Z'].value
        self.RD_MAX = 1 / ( 0.01 * min(tau_free, min(tauS, min(tauS, 0.0001/flow_rate))))
        #flow geometry and finite extensibility
        phi0 = 1 / (1 + tau_free / tau_as)

        if self.flow_mode == FlowMode.shear:
            vec_0 = [phi0, 1.0, 1.0, 1.0, 0, 1.0, 1.0, 0]  # f, ldeq, QAxx, QAyy, QAxy QDxx, QDyy, QDxy
            pde = self.sigmadot_shear
        elif self.flow_mode == FlowMode.uext:
            vec_0 = [phi0, 1.0, 1.0, 1.0, 1.0, 1.0] # f, ldeq, QAxx, QAyy, QDxx, QDyy
            pde = self.sigmadot_uext
        else:
            return

        p = [Z, r_a, lmax, tauD, tauS, tau_as, tau_free, beta, delta, flow_rate]
        try:
            res_vec = odeint(
                pde,
                vec_0,
                t,
                args=(p, ),
                atol=abserr,
                rtol=relerr)
        except EndComputationRequested:
            pass

        G = self.parameters["G"].value
        if self.flow_mode == FlowMode.shear:
            # res_vec = [f, ldeq, QAxx, QAyy, QAxy, QDxx, QDyy, QDxy]
            f = np.delete(res_vec[:, 0], [0])
            # QAxx = np.delete(res_vec[:, 2], [0])
            # QAyy = np.delete(res_vec[:, 3], [0])
            QAxy = np.delete(res_vec[:, 4], [0])
            # QDxx = np.delete(res_vec[:, 5], [0])
            # QDyy = np.delete(res_vec[:, 6], [0])
            QDxy = np.delete(res_vec[:, 7], [0])
            # build stress array
            tt.data[:, 1] =  G * (f * QAxy + (1 - f) * QDxy)
        
        elif self.flow_mode == FlowMode.uext:
            # res_vec = [f, ldeq, QAxx, QAyy, QDxx, QDyy]
            f = np.delete(res_vec[:, 0], [0])
            QAxx = np.delete(res_vec[:, 2], [0])
            QAyy = np.delete(res_vec[:, 3], [0])
            QDxx = np.delete(res_vec[:, 4], [0])
            QDyy = np.delete(res_vec[:, 5], [0])
            # build stress array
            tt.data[:, 1] = G * (f * (QAxx - QAyy) + (1 - f) * (QDxx - QDyy))

class CLTheoryPETS(
        BaseTheoryPETS, Theory):
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


class GUITheoryPETS(
        BaseTheoryPETS, QTheory):
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

        #Show LVE button
        self.linearenvelope = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/lve-icon.png'),
            'Show Linear Envelope')
        self.linearenvelope.setCheckable(True)
        self.linearenvelope.setChecked(False)

        self.thToolsLayout.insertWidget(0, tb)

        connection_id = self.shear_flow_action.triggered.connect(
            self.select_shear_flow)
        connection_id = self.extensional_flow_action.triggered.connect(
            self.select_extensional_flow)
        connection_id = self.linearenvelope.triggered.connect(
            self.show_linear_envelope)

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
        data_table_tmp = DataTable(self.axarr)
        data_table_tmp.num_columns = 2
        data_table_tmp.num_rows = 100
        data_table_tmp.data = np.zeros((100, 2))

        times = np.logspace(-2, 3, 100)
        data_table_tmp.data[:, 0] = times
        data_table_tmp.data[:, 1] = 0
        fparamaux = {}
        fparamaux["gdot"] = 1e-8

        G = self.parameters["G"].value
        tauD = self.parameters["tauD"].value
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
