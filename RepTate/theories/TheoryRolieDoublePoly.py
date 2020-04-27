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
"""Module TheoryRolieDoublePoly

Module for the Rolie-Double-Poly theory for the non-linear flow of entangled polymers.

"""
import numpy as np
from scipy.integrate import ode, odeint
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from PyQt5.QtWidgets import QToolBar, QToolButton, QMenu, QStyle, QSpinBox, QTableWidget, QDialog, QVBoxLayout, QHBoxLayout, QDialogButtonBox, QTableWidgetItem, QMessageBox, QLabel, QLineEdit, QRadioButton, QButtonGroup, QFileDialog
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices, QDoubleValidator
from PyQt5.QtCore import Qt
from Theory_rc import *
from enum import Enum
from math import sqrt
from SpreadsheetWidget import SpreadsheetWidget
import time
import Version

import rp_blend_ctypes_helper as rpch
from Theory import EndComputationRequested
from collections import OrderedDict


class Dilution():
    def __init__(self, m, phi, taue, Me, parent_theory):
        super().__init__()
        self.parent_theory = parent_theory
        self.res = self.relax_times_from_mwd(m, phi, taue, Me)

    def find_down_indx(self, tauseff, taud):
        """Find index i such that taud[i] < tauseff < taud[i+1]
        or returns -1 if tauseff < taud[0]
        or returns n-1 if tauseff > taud[n-1] (should not happen)
        """
        n = len(taud)
        down = n - 1
        while tauseff < taud[down]:
            if down == 0:
                down = -1
                break
            down -= 1
        return down

    def find_dilution(self, phi, taud, taus, interp=True):
        """Find the dilution factor phi_dil for a chain with bare stretch relax time `taus`"""
        n = len(phi)
        temp = -1
        phi_dil = 1
        tauseff = taus / phi_dil
        #m[0] < m[1] <  ... < m[n]
        while True:
            down = self.find_down_indx(tauseff, taud)
            if down == -1:
                #case tauseff < taud[0]
                phi_dil = 1
                break
            elif down == n - 1:
                #(just in case) tauseff > taud[n-1]
                phi_dil = phi[n - 1]
                break
            else:
                #change tauseff and check if 'down' is still the same
                if (temp == down):
                    break
                temp = down
                phi_dil = 1.0
                for k in range(down):
                    phi_dil -= phi[k]
                if interp:
                    # x=0 if tauseff close to td[down], x=1 if tauseff close to td[down+1]
                    x = (tauseff - taud[down]) / (taud[down + 1] - taud[down])
                    # linear interpolation of phi_dil
                    phi_dil = phi_dil - x * phi[down]
                else:
                    phi_dil -= phi[down]
            tauseff = taus / phi_dil
        return phi_dil

    def sort_list(self, m, phi):
        """Ensure m[0] <= m[1] <=  ... <= m[n]"""
        if all(m[i] <= m[i + 1] for i in range(len(m) - 1)):
            #list aready sorted
            return m, phi
        args = np.argsort(m)
        m = list(np.array(m)[args])
        phi = list(np.array(phi)[args])
        return m, phi

    def relax_times_from_mwd(self, m, phi, taue, Me):
        """Guess relaxation times of linear rheology (taud) from molecular weight distribution.
        (i) Count short chains (M < 2*Me) as solvent
        (ii) The effective dilution at a given timescale t is equal to the sum of
        the volume fractions of all chains with relaxation time greater than t
        (iii) CLF makes use of the most diluted tube available at the CLF timescale
        """
        #m[0] < m[1] <  ... < m[n]
        m, phi = self.sort_list(m, phi)

        taus = []
        taus_short = []
        taud = []
        phi_short = []
        m_short = []
        phi_u = 0
        nshort = 0

        n = len(m)
        for i in range(n):
            z = m[i] / Me
            ts = z * z * taue
            if m[i] < 2. * Me:
                #short chains not entangled: use upper-convected Maxwell model
                nshort += 1
                phi_u += phi[i]
                taus_short.append(ts)
                phi_short.append(phi[i])
                m_short.append(m[i])
            else:
                taus.append(ts)

        #remove the short chains from the list of M and phi
        m = m[nshort:]
        phi = phi[nshort:]

        n = len(m)  # new size
        if n == 0:
            self.parent_theory.Qprint("All chains as solvent")
            return [False]
        if n == 1:
            return [True, phi, taus, [3 * z * ts,]]

        Zeff = [0] * n
        #renormalize the fraction of entangled chains
        Me /= (1 - phi_u)
        taue /= ((1 - phi_u) * (1 - phi_u))
        for i in range(n):
            phi[i] /= (1 - phi_u)
            z = m[i] / Me
            taud.append(3. * z * z * z * taue)

        vphi = []
        interp = (n>2) # true if more than two species
        for i in range(n):
            #find dilution for the entangled chains
            if i == 0:
                phi_dil = 1
            else:
                phi_dil = self.find_dilution(phi, taud, taus[i], interp=interp)
            vphi.append(phi_dil)

        for i in range(n):
            z = m[i] / Me
            if z * vphi[i] < 1 and z > 1:
                # case where long chains are effectively untentangled
                # CR-Rouse approximated as last taud having z*vphi > 1
                taud_sticky_rep = taud[i - 1]
                for j in range(i, n):
                    taud[j] = taud_sticky_rep
                    Zeff[j] = 1.0
                break
            taud[i] = taud[i] * self.parent_theory.fZ(z * vphi[i])
            Zeff[i] = z * vphi[i]
        self.parent_theory.Zeff = np.array(Zeff)

        return [True, phi, taus, taud]


class FlowMode(Enum):
    """Defines the flow geometry used
    
    Parameters can be:
        - shear: Shear flow
        - uext: Uniaxial extension flow
    """
    shear = 0
    uext = 1


class GcorrMode(Enum):
    """Primitive path fluctuations reduce the terminal modulus due to shortened tube.
    Defines if we include that correction.

    Parameters can be:
        - none: No finite extensibility
        - with_gcorr: With finite extensibility
    """
    none = 0
    with_gcorr = 1


class FeneMode(Enum):
    """Defines the finite extensibility function
    
    Parameters can be:
        - none: No finite extensibility
        - with_fene: With finite extensibility
    """
    none = 0
    with_fene = 1


class GetMwdRepate(QDialog):
    def __init__(self, parent=None, th_dict={}, title="title"):
        super().__init__(parent)

        self.setWindowTitle(title)
        layout = QVBoxLayout(self)

        validator = QDoubleValidator()
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Me"))
        self.Me_text = QLineEdit("%.3g" % parent.parameters["Me"].value)
        self.Me_text.setValidator(validator)
        hlayout.addWidget(self.Me_text)

        hlayout.addWidget(QLabel("taue"))
        self.taue_text = QLineEdit("%.3g" % parent.parameters["tau_e"].value)
        self.taue_text.setValidator(validator)
        hlayout.addWidget(self.taue_text)

        layout.addLayout(hlayout)

        self.btngrp = QButtonGroup()

        for item in th_dict.keys():
            rb = QRadioButton(item, self)
            layout.addWidget(rb)
            self.btngrp.addButton(rb)
        # default button selection
        rb = self.btngrp.buttons()[0]
        rb.setChecked(True)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


class EditMWDDialog(QDialog):
    def __init__(self, parent=None, m=None, phi=None, MAX_MODES=0):
        super().__init__(parent)

        self.setWindowTitle("Input Molecular weight distribution")
        layout = QVBoxLayout(self)

        validator = QDoubleValidator()
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Me"))
        self.Me_text = QLineEdit("%.4g" % parent.parameters["Me"].value)
        self.Me_text.setValidator(validator)
        hlayout.addWidget(self.Me_text)

        hlayout.addWidget(QLabel("taue"))
        self.taue_text = QLineEdit("%.4g" % parent.parameters["tau_e"].value)
        self.taue_text.setValidator(validator)
        hlayout.addWidget(self.taue_text)

        layout.addLayout(hlayout)
        nmodes = len(phi)

        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, MAX_MODES)  # min and max number of modes
        self.spinbox.setSuffix(" modes")
        self.spinbox.setValue(nmodes)  #initial value
        layout.addWidget(self.spinbox)

        self.table = SpreadsheetWidget()  #allows copy/paste
        self.table.setRowCount(nmodes)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["M", "phi"])
        for i in range(nmodes):
            self.table.setItem(i, 0, QTableWidgetItem("%g" % m[i]))
            self.table.setItem(i, 1, QTableWidgetItem("%g" % phi[i]))

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
            sum += float(self.table.item(i, 1).text())
        if abs(sum - 1) < 0.02:
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'phi must add up to 1')

    def handle_spinboxValueChanged(self, value):
        nrow_old = self.table.rowCount()
        self.table.setRowCount(value)
        for i in range(nrow_old, value):  #create extra rows with defaut values
            self.table.setItem(i, 0, QTableWidgetItem("0"))
            self.table.setItem(i, 1, QTableWidgetItem("1000"))


class EditModesDialog(QDialog):
    def __init__(self, parent=None, param_dic={}, MAX_MODES=0):
        super().__init__(parent)

        self.setWindowTitle("Edit volume fractions and relaxation times")
        layout = QVBoxLayout(self)
        self.nparam = len(param_dic)
        pnames = list(param_dic.keys())
        nmodes = len(param_dic[pnames[0]])

        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, MAX_MODES)  # min and max number of modes
        self.spinbox.setSuffix(" modes")
        self.spinbox.setValue(nmodes)  #initial value
        layout.addWidget(self.spinbox)

        self.table = SpreadsheetWidget()  #allows copy/paste
        self.table.setRowCount(nmodes)
        self.table.setColumnCount(self.nparam)
        self.table.setHorizontalHeaderLabels(pnames)
        for i in range(nmodes):
            for j in range(self.nparam):
                self.table.setItem(i, j,
                                   QTableWidgetItem(
                                       "%g" % param_dic[pnames[j]][i]))
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
            for j in range(self.nparam):
                self.table.setItem(i, j, QTableWidgetItem("0"))


class TheoryRolieDoublePoly(CmdBase):
    """Rolie-Double-Poly equations for the nonlinear predictions of polydisperse melts of entangled linear polymers

    * **Function**
        .. math::
            \\boldsymbol \\sigma = G_N^0 \\sum_i g(Z_{\\text{eff},i}) \\text{fene}(\\lambda_i) \\phi_i \\boldsymbol A_i

        where
            .. math::
                \\boldsymbol A_i &= \\sum_j \\phi_j \\boldsymbol A_{ij}\\\\
                \\lambda_i &= \\left( \\dfrac{\\text{Tr}  \\boldsymbol A_i}{3}  \\right)^{1/2}\\\\
                \\stackrel{\\nabla}{\\boldsymbol  A_{ij}} &=
                -\\dfrac{1}{\\tau_{\\mathrm d,i}} (\\boldsymbol A_{ij} - \\boldsymbol I)
                -\\dfrac{2}{\\tau_{\\mathrm s,i}} \\dfrac{\\lambda_i - 1}{\\lambda_i} \\boldsymbol A_{ij}
                -\\left( \\dfrac{\\beta_\\text{th}}{\\tau_{\\mathrm d,j}} 
                + \\beta_\\text{CCR}\\dfrac{2}{\\tau_{\\mathrm s,j}} \\dfrac{\\lambda_j - 1}{\\lambda_j}\\lambda_i^{2\\delta} \\right)
                (\\boldsymbol A_{ij} - \\boldsymbol I)\\\\
                \\text{fene}(\\lambda) &= \\dfrac{1-1/\\lambda_\\text{max}^2}{1-\\lambda^2/\\lambda_\\text{max}^2}
        
        with :math:`\\beta_\\text{th}` the thermal constrain release parameter, set to 1. If the "modulus correction" button
        is pressed, :math:`g(z) = 1- \\dfrac{c_1}{z^{1/2}} + \\dfrac{c_2}{z} + \\dfrac{c_3}{z^{3/2}}` is the Likhtman-McLeish
        CLF correction function to the modulus (:math:`c_1=1.69`, :math:`c_2=2`, :math:`c_3=-1.24`), :math:`g(z) = 1` otherwise;
        :math:`Z_{\\text{eff},i}=Z_i\\phi_{\\text{dil},i}` is the
        effective entanglement number of the molecular weight component :math:`i`, and :math:`\\phi_{\\text{dil},i}` the
        dilution factor (:math:`\\phi_{\\text{dil},i}\\leq \\phi_i`).

    * **Parameters**
       - ``GN0`` :math:`\\equiv G_N^0`: Plateau modulus
       - ``beta`` :math:`\\equiv\\beta_\\text{CCR}`: Rolie-Poly CCR parameter
       - ``delta`` :math:`\\equiv\\delta`: Rolie-Poly CCR exponent
       - ``phi_i`` :math:`\\equiv\\phi_i`: Volume fraction of species :math:`i`
       - ``tauD_i`` :math:`\\equiv\\tau_{\\mathrm d,i}`: Reptation time of species :math:`i` (including CLF)
       - ``tauR_i`` :math:`\\equiv\\tau_{\\mathrm s,i}`: Stretch relaxation time of species :math:`i`
       - ``lmax`` :math:`\\equiv\\lambda_\\text{max}`: Maximum stretch ratio (active only when the "fene button" is pressed)
    """
    thname = "Rolie-Double-Poly"
    description = "Rolie-Double-Poly const. eq. for polydisperse melts of entangled linear polymers"
    citations = ["Boudara V.A.H. et al., J. Rheol. 63, 71-91 (2019)"]
    doi = ["http://dx.doi.org/10.1122/1.5052320"]

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
        return GUITheoryRolieDoublePoly(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryRolieDoublePoly(
                name, parent_dataset, ax)


class BaseTheoryRolieDoublePoly:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/NLVE/Theory/theory.html#rolie-double-poly-equations'
    single_file = False
    thname = TheoryRolieDoublePoly.thname
    citations = TheoryRolieDoublePoly.citations
    doi = TheoryRolieDoublePoly.doi

    def __init__(self, name="", parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.RolieDoublePoly
        self.has_modes = True
        self.autocalculate = False
        self.parameters["beta"] = Parameter(
            name="beta",
            value=1,
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
            min_value=0)
        self.parameters["Me"] = Parameter(
            name="Me",
            value=1e4,
            description="Entanglement molecular mass",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False)
        self.parameters["tau_e"] = Parameter(
            name="tau_e",
            value=0.01,
            description="Entanglement relaxation time",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False)
        nmode = self.parameters["nmodes"].value
        for i in range(nmode):
            self.parameters["phi%02d" % i] = Parameter(
                name="phi%02d" % i,
                value=1. / nmode,
                description="Volume fraction of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.nopt,
                display_flag=False,
                min_value=0)
            self.parameters["tauD%02d" % i] = Parameter(
                name="tauD%02d" % i,
                value=100.0,
                description="Terminal time of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.nopt,
                display_flag=False,
                min_value=0)
            self.parameters["tauR%02d" % i] = Parameter(
                name="tauR%02d" % i,
                value=1,
                description="Rouse time of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.opt,
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
        self.with_gcorr = GcorrMode.none
        self.Zeff = []
        self.MWD_m = [100, 1000]
        self.MWD_phi = [0.5, 0.5]
        self.init_flow_mode()

    def set_extra_data(self, extra_data):
        """Set extra data when loading project"""
        self.MWD_m = extra_data['MWD_m']
        self.MWD_phi = extra_data['MWD_phi']
        self.Zeff = extra_data['Zeff']

        # FENE button
        self.handle_with_fene_button(extra_data['with_fene'])

        # G button
        if extra_data['with_gcorr']:
            self.with_gcorr == GcorrMode.with_gcorr
            self.with_gcorr_button.setChecked(True)

    def get_extra_data(self):
        """Set extra_data when saving project"""
        self.extra_data['MWD_m'] = self.MWD_m
        self.extra_data['MWD_phi'] = self.MWD_phi
        self.extra_data['Zeff'] = self.Zeff
        self.extra_data['with_fene'] = self.with_fene == FeneMode.with_fene
        self.extra_data['with_gcorr'] = self.with_gcorr == GcorrMode.with_gcorr

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
        self.show_theory_extras(False)
        self.ax.lines.remove(self.LVEenvelopeseries)

    def show_theory_extras(self, show=False):
        """Called when the active theory is changed
        
        [description]
        """
        if CmdBase.mode == CmdMode.GUI:
            self.Qhide_theory_extras(show)
        # self.extra_graphic_visible(show)

    def extra_graphic_visible(self, state):
        """[summary]
        
        [description]
        """
        self.view_LVEenvelope = state
        self.LVEenvelopeseries.set_visible(state)
        self.parent_dataset.parent_application.update_plot()

    def get_modes(self):
        """Get the values of Maxwell Modes from this theory"""
        nmodes = self.parameters["nmodes"].value
        tau = np.zeros(nmodes)
        G = np.zeros(nmodes)
        GN0 = self.parameters["GN0"].value
        for i in range(nmodes):
            tau[i] = self.parameters["tauD%02d" % i].value
            G[i] = GN0 * self.parameters["phi%02d" % i].value
        return tau, G, True

    def set_modes_from_mwd(self, m, phi):
        """[summary]
        
        [description]
        
        Returns:
            - [type] -- [description]
        """
        Me = self.parameters["Me"].value
        taue = self.parameters["tau_e"].value
        res = Dilution(m, phi, taue, Me, self).res
        if res[0] == False:
            self.Qprint("Could not set modes from MDW")
            return
        _, phi, taus, taud = res
        nmodes = len(phi)
        self.set_param_value("nmodes", nmodes)
        for i in range(nmodes):
            self.set_param_value("phi%02d" % i, phi[i])
            self.set_param_value("tauR%02d" % i, taus[i])
            self.set_param_value("tauD%02d" % i, taud[i])
        self.Qprint("Got %d modes from MWD" % nmodes)
        self.update_parameter_table()
        self.Qprint(
            '<font color=green><b>Press "Calculate" to update theory</b></font>'
        )

    def set_modes(self, tau, G):
        """Set the values of Maxwell Modes from another theory"""
        nmodes = len(tau)
        self.set_param_value("nmodes", nmodes)
        sum_G = G.sum()

        for i in range(nmodes):
            self.set_param_value("tauD%02d" % i, tau[i])
            self.set_param_value("phi%02d" % i, G[i] / sum_G)
        self.update_parameter_table()
        return True

    def fZ(self, z):
        """CLF correction function Likthman-McLeish (2002)"""
        return 1 - 2 * 1.69 / sqrt(z) + 4.17 / z - 1.55 / (z * sqrt(z))

    def gZ(self, z):
        """CLF correction function for modulus Likthman-McLeish (2002)"""
        return 1 - 1.69 / sqrt(z) + 2.0 / z - 1.24 / (z * sqrt(z))

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

    def calculate_fene(self, l_square, lmax):
        """calculate finite extensibility function value"""
        ilm2 = 1.0 / (lmax * lmax)  # 1/lambda_max^2
        l2_lm2 = l_square * ilm2  # (lambda/lambda_max)^2
        return (3.0 - l2_lm2) / (1.0 - l2_lm2) * (1.0 - ilm2) / (3.0 - ilm2)

    def RolieDoublePoly(self, f=None):
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
        relerr = 1.0e-8
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
        self.Qprint('Rate %.3g<br>  0%% ' % flow_rate, end='')
        try:
            sig = odeint(
                pde_stretch, sigma0, t, args=(p, ), atol=abserr, rtol=relerr)
        except EndComputationRequested:
            return
        self.Qprint(' 100%')
        # sig.shape is (len(t), 3*n^2) in shear
        if self.flow_mode == FlowMode.shear:
            c = 3
            sig = sig[1:, :]
            nt = len(sig)
            lsq = np.zeros((nt, nmodes))
            if self.with_fene == FeneMode.with_fene:
                #calculate lambda^2
                for i in range(nmodes):
                    if self.stop_theory_flag:
                        break
                    I = c * nmodes * i
                    trace_arr = np.zeros(nt)
                    for j in range(nmodes):
                        # trace_arr += phi_arr[j] * (sxx_t[:, I + j] + 2 * syy_t[:, I + j])
                        trace_arr += phi_arr[j] * (
                            sig[:, I + c * j] + 2 * sig[:, I + c * j + 1])
                    lsq[:, i] = trace_arr / 3.0  # len(t) rows and n cols

            for i in range(nmodes):
                if self.stop_theory_flag:
                    break
                I = c * nmodes * i
                sig_i = np.zeros(nt)
                for j in range(nmodes):
                    sig_i += phi_arr[j] * sig[:, I + c * j + 2]

                if self.with_fene == FeneMode.with_fene:
                    sig_i *= self.calculate_fene(lsq[:, i], lmax)
                if self.with_gcorr == GcorrMode.with_gcorr:
                    sig_i *= self.gZ(self.Zeff[i])
                tt.data[:, 1] += phi_arr[i] * sig_i
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
                    if self.stop_theory_flag:
                        break
                    I = c * nmodes * i
                    trace_arr = np.zeros(nt)
                    for j in range(nmodes):
                        trace_arr += phi_arr[j] * (
                            sig[:, I + c * j] + 2 * sig[:, I + c * j + 1])
                    lsq[:, i] = trace_arr / 3.0  # len(t) rows and n cols

            for i in range(nmodes):
                if self.stop_theory_flag:
                    break
                I = c * nmodes * i
                sig_i = np.zeros(nt)
                for j in range(nmodes):
                    sig_i += phi_arr[j] * (
                        sig[:, I + c * j] - sig[:, I + c * j + 1])

                if self.with_fene == FeneMode.with_fene:
                    sig_i *= self.calculate_fene(lsq[:, i], lmax)
                if self.with_gcorr == GcorrMode.with_gcorr:
                    sig_i *= self.gZ(self.Zeff[i])
                tt.data[:, 1] += phi_arr[i] * sig_i

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
        message, success = super(BaseTheoryRolieDoublePoly,
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
                    min_value=0)
                self.parameters["tauD%02d" % i] = Parameter(
                    name="tauD%02d" % i,
                    value=100.0,
                    description="Terminal time of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.nopt,
                    display_flag=False,
                    min_value=0)
                self.parameters["tauR%02d" % i] = Parameter(
                    name="tauR%02d" % i,
                    value=1,
                    description="Rouse time of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.opt,
                    display_flag=True,
                    min_value=0)
            if (oldn > self.parameters["nmodes"].value):
                for i in range(self.parameters["nmodes"].value, oldn):
                    del self.parameters["phi%02d" % i]
                    del self.parameters["tauD%02d" % i]
                    del self.parameters["tauR%02d" % i]
        return '', True

    def do_fit(self, line):
        """Minimisation procedure disabled in this theory"""
        self.Qprint(
            "<font color=red><b>Minimisation procedure disabled in this theory</b></font>"
        )


class CLTheoryRolieDoublePoly(BaseTheoryRolieDoublePoly, Theory):
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


class GUITheoryRolieDoublePoly(BaseTheoryRolieDoublePoly, QTheory):
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

        self.tbutmodes = QToolButton()
        self.tbutmodes.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        self.get_modes_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-broadcasting.png'),
            "Get Modes (MWD app)")
        self.get_modes_data_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-broadcasting.png'),
            "Get Modes (MWD data)")
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
        # #Show LVE button
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
        #Modulus correction button
        self.with_gcorr_button = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-circled-g-filled.png'),
            'Modulus Correction')
        self.with_gcorr_button.setCheckable(True)

        #Save to flowsolve button
        self.flowsolve_btn = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-save-flowsolve.png'),
            'Save Parameters To FlowSolve')
        self.flowsolve_btn.setCheckable(False)

        self.thToolsLayout.insertWidget(0, tb)

        connection_id = self.shear_flow_action.triggered.connect(
            self.select_shear_flow)
        connection_id = self.extensional_flow_action.triggered.connect(
            self.select_extensional_flow)
        connection_id = self.get_modes_action.triggered.connect(
            self.get_modes_reptate)
        connection_id = self.get_modes_data_action.triggered.connect(
            self.edit_mwd_modes)
        connection_id = self.edit_modes_action.triggered.connect(
            self.edit_modes_window)
        # connection_id = self.plot_modes_action.triggered.connect(
        #     self.plot_modes_graph)
        connection_id = self.linearenvelope.triggered.connect(
            self.show_linear_envelope)
        connection_id = self.save_modes_action.triggered.connect(
            self.save_modes)
        connection_id = self.with_fene_button.triggered.connect(
            self.handle_with_fene_button)
        connection_id = self.with_gcorr_button.triggered.connect(
            self.handle_with_gcorr_button)
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
            f.write('constit polydisperse\n')
            # f.write('# or multip (for pompom) or polydisperse (for polydisperse Rolie-Poly)\n')

            f.write('\n#param constitutive\n')

            n = self.parameters['nmodes'].value

            td = np.zeros(n)
            for i in range(n):
                td[i] = self.parameters["tauD%02d" % i].value
            # sort taud ascending order
            args = np.argsort(td)

            fraction = 'fraction'
            taud = 'taud'
            tauR = 'tauR'
            lmax = 'lambdaMax'
            for i, arg in enumerate(args):
                fraction += ' %.6g' % self.parameters["phi%02d" % arg].value
                taud += ' %.6g' % self.parameters["tauD%02d" % arg].value
                tauR += ' %.6g' % self.parameters["tauR%02d" % arg].value
                lmax += ' %.6g' % self.parameters["lmax"].value
            f.write('%s\n%s\n%s\n' % (taud, tauR, fraction))
            if self.with_fene == FeneMode.with_fene:  # don't output lmax at all for infinite ex
                f.write('%s\n' % lmax)
            f.write('modulus %.6g\n' % self.parameters["GN0"].value)
            f.write('beta %.6gn' % self.parameters["beta"].value)
            f.write('delta %.6g\n' % self.parameters["delta"].value)

            f.write('\n#end')

        QMessageBox.information(self, 'Success',
                                'Wrote FlowSolve parameters in \"%s\"' % fpath)

    def handle_with_gcorr_button(self, checked):
        if checked:
            if len(self.Zeff) > 0:
                # if Zeff contains something
                self.with_gcorr = GcorrMode.with_gcorr
            else:
                self.Qprint(
                    '<font color=orange><b>Modulus correction needs Z from MWD</b></font>'
                )
                self.with_gcorr_button.setChecked(False)
                return
        else:
            self.with_gcorr = GcorrMode.none
        self.Qprint(
            '<font color=green><b>Press "Calculate" to update theory</b></font>'
        )

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
        self.Qprint(
            '<font color=green><b>Press "Calculate" to update theory</b></font>'
        )

    def Qhide_theory_extras(self, show):
        """Uncheck the LVE button. Called when curent theory is changed
        
        [description]
        """
        if show:
            self.LVEenvelopeseries.set_visible(self.linearenvelope.isChecked())
        else:
            self.LVEenvelopeseries.set_visible(False)
        self.parent_dataset.actionMinimize_Error.setDisabled(show)
        self.parent_dataset.actionShow_Limits.setDisabled(show)
        self.parent_dataset.actionVertical_Limits.setDisabled(show)
        self.parent_dataset.actionHorizontal_Limits.setDisabled(show)

    def show_linear_envelope(self, state):
        self.plot_theory_stuff()
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
        apmng = self.parent_dataset.parent_application.parent_manager
        get_dict = {}
        for app in apmng.applications.values():
            app_index = apmng.ApplicationtabWidget.indexOf(app)
            app_tab_name = apmng.ApplicationtabWidget.tabText(app_index)
            for ds in app.datasets.values():
                ds_index = app.DataSettabWidget.indexOf(ds)
                ds_tab_name = app.DataSettabWidget.tabText(ds_index)
                for th in ds.theories.values():
                    th_index = ds.TheorytabWidget.indexOf(th)
                    th_tab_name = ds.TheorytabWidget.tabText(th_index)
                    if th.thname == 'Discretize MWD':
                        get_dict["%s.%s.%s" % (app_tab_name, ds_tab_name,
                                               th_tab_name)] = th.get_mwd

        if get_dict:
            d = GetMwdRepate(self, get_dict, 'Select Discretized MWD')
            if (d.exec_() and d.btngrp.checkedButton() != None):
                _, success1 = self.set_param_value("tau_e", d.taue_text.text())
                _, success2 = self.set_param_value("Me", d.Me_text.text())
                if not success1 * success2:
                    self.Qprint("Could not understand Me or taue, try again")
                    return
                item = d.btngrp.checkedButton().text()
                m, phi = get_dict[item]()

                self.MWD_m = np.copy(m)
                self.MWD_phi = np.copy(phi)
                self.set_modes_from_mwd(m, phi)
        else:
            # no theory Discretise MWD found
            QMessageBox.warning(self, 'Get MW distribution',
                                'No \"Discretize MWD\" theory found')
        # self.parent_dataset.handle_actionCalculate_Theory()

    def edit_modes_window(self):
        nmodes = self.parameters["nmodes"].value
        phi = np.zeros(nmodes)
        taud = np.zeros(nmodes)
        taur = np.zeros(nmodes)
        for i in range(nmodes):
            phi[i] = self.parameters["phi%02d" % i].value
            taud[i] = self.parameters["tauD%02d" % i].value
            taur[i] = self.parameters["tauR%02d" % i].value
        param_dic = OrderedDict()
        param_dic["phi"] = phi
        param_dic["tauD"] = taud
        param_dic["tauR"] = taur
        d = EditModesDialog(self, param_dic, self.MAX_MODES)
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

    def edit_mwd_modes(self):
        d = EditMWDDialog(self, self.MWD_m, self.MWD_phi, 200)
        if d.exec_():
            nmodes = d.table.rowCount()
            m = []
            phi = []
            _, success1 = self.set_param_value("tau_e", d.taue_text.text())
            _, success2 = self.set_param_value("Me", d.Me_text.text())
            if not success1 * success2:
                self.Qprint("Could not understand Me or taue, try again")
                return
            for i in range(nmodes):
                try:
                    m.append(float(d.table.item(i, 0).text()))
                    phi.append(float(d.table.item(i, 1).text()))
                except ValueError:
                    self.Qprint("Could not understand line %d, try again" %
                                (i + 1))
                    return
            self.MWD_m = np.copy(m)
            self.MWD_phi = np.copy(phi)
            self.set_modes_from_mwd(m, phi)

    # def plot_modes_graph(self):
    #     pass

    def plot_theory_stuff(self):
        """[summary]
        
        [description]
        """
        logtmin = np.log10(self.parent_dataset.minpositivecol(0))
        logtmax = np.log10(self.parent_dataset.maxcol(0)) + 1
        ntimes = int((logtmax - logtmin) * 20)
        data_table_tmp = DataTable(self.axarr)
        data_table_tmp.num_columns = 2
        data_table_tmp.num_rows = ntimes
        data_table_tmp.data = np.zeros((ntimes, 2))

        times = np.logspace(logtmin, logtmax, ntimes)
        data_table_tmp.data[:, 0] = times
        nmodes = self.parameters["nmodes"].value
        data_table_tmp.data[:, 1] = 0
        fparamaux = {"gdot": 1e-8}

        phi = []
        taud = []
        for i in range(nmodes):
            phi.append(self.parameters["phi%02d" % i].value)
            taud.append(self.parameters["tauD%02d" % i].value)

        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            G = self.parameters['GN0'].value
            if self.with_gcorr == GcorrMode.with_gcorr:
                G = G * self.gZ(self.Zeff[i])
            for j in range(nmodes):
                # TODO: use symetry to reduce number of loops
                tau = 1. / (1. / taud[i] + 1. / taud[j])
                data_table_tmp.data[:, 1] += G * phi[i] * phi[j] * fparamaux[
                    "gdot"] * tau * (1 - np.exp(-times / tau))
        if self.flow_mode == FlowMode.uext:
            data_table_tmp.data[:, 1] *= 3.0
        view = self.parent_dataset.parent_application.current_view
        try:
            x, y, success = view.view_proc(data_table_tmp, fparamaux)
        except TypeError as e:
            print(e)
            return
        self.LVEenvelopeseries.set_data(x[:, 0], y[:, 0])
        # remove tmp artist form ax
        for i in range(data_table_tmp.MAX_NUM_SERIES):
            for nx in range(len(self.axarr)):
                self.axarr[nx].lines.remove(data_table_tmp.series[nx][i])

