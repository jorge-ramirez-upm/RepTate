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
"""Module TheorySCCR

Module for the SCCR theory for the non-linear flow of entangled polymers.

"""
import numpy as np
from scipy.integrate import ode, odeint
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from PyQt5.QtWidgets import QToolBar, QToolButton, QMenu, QStyle, QSpinBox, QTableWidget, QDialog, QVBoxLayout, QDialogButtonBox, QTableWidgetItem, QMessageBox, QFileDialog, QInputDialog
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
import sccr_ctypes_helper as sch
from ctypes import c_int, c_double
from math import exp
from PyQt5.QtCore import pyqtSignal

class FlowMode(Enum):
    """Defines the flow geometry used
    
    Parameters can be:
        - shear: Shear flow
        - uext: Uniaxial extension flow
    """
    shear = 0
    uext = 1

class TheorySCCR(CmdBase):
    """Full SCCR theory for the Non-linear transient flow of linear entangled polymers.
        
    * **Parameters**
       - ``tau_e`` : Rouse time of one entanglement segment (of length :math:`M_e`.
       - ``Ge`` : Entanglement modulus.
       - ``Me`` : Entanglement molecular weight.
       - ``c_nu`` : Constraint release parameter.
    """
    thname = "GLaMM"
    description = "SCCR theory for linear entangled polymers"
    citations = ["Graham, R.S. et al., J. Rheol., 2003, 47, 1171-1200"]
    doi = ["http://dx.doi.org/10.1122/1.1595099"]

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
        return GUITheorySCCR(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheorySCCR(
                name, parent_dataset, ax)


class BaseTheorySCCR:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/NLVE/Theory/theory.html#sccr-theory'
    single_file = False
    thname = TheorySCCR.thname
    citations = TheorySCCR.citations
    doi = TheorySCCR.doi

    signal_get_MW = pyqtSignal(object)

    def __init__(self, name="", parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.SCCR
        self.has_modes = False
        self.signal_get_MW.connect(self.launch_get_MW_dialog)

        self.parameters["tau_e"] = Parameter(
            "tau_e",
            1,
            "Rouse time of one Entanglement",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0.0,
            max_value=np.inf)
        self.parameters["Ge"] = Parameter(
            "Ge",
            1,
            "Entanglement modulus",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0.0,
            max_value=np.inf)
        self.parameters["Me"] = Parameter(
            "Me",
            1,
            "Entanglement molecular weight",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0.0,
            max_value=np.inf)
        self.parameters["c_nu"] = Parameter(
            name="c_nu",
            value=0.1,
            description="Constraint Release parameter",
            type=ParameterType.discrete_real,
            opt_type=OptType.const,
            discrete_values=[0, 0.01, 0.03, 0.1, 0.3, 1, 3, 10])
        self.parameters["Rs"] = Parameter(
            name="Rs",
            value=2.0,
            description="Retraction rate parameter",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0.0,
            max_value=4.0)
        self.parameters["N"] = Parameter(
            name="N",
            value=1,
            description="npoints=N*Z Precision of SCCR (odd number)",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False)
        self.parameters["recommendedN"] = Parameter(
            name="recommendedN",
            value=False,
            description="Get Optimal value of N, depending on Z",
            type=ParameterType.boolean,
            opt_type=OptType.const,
            display_flag=False)

        self.init_flow_mode()
        self.get_material_parameters()
        self.autocalculate = False

    def launch_get_MW_dialog(self):
        title = 'Missing "Mw" value'
        msg = 'Set "Mw" value for file \"%s\"' % self.fname_missing_mw
        def_val = 10
        min_val = 0
        val, success = QInputDialog.getDouble(self, title, msg, def_val, min_val)
        self.success_MW = success
        self.new_MW_val = val

    def init_flow_mode(self):
        """Find if data files are shear or extension"""
        try:
            f = self.theory_files()[0]
            if f.file_type.extension == 'shear':
                self.flow_mode = FlowMode.shear
            else:
                self.flow_mode = FlowMode.uext
        except Exception as e:
            print("in SCCR init:", e)
            self.flow_mode = FlowMode.shear  #default mode: shear

    def do_fit(self, line):
        """Minimisation procedure disabled in this theory"""
        self.Qprint(
            "<font color=red><b>Minimisation procedure disabled in this theory</b></font>"
        )

    def show_theory_extras(self, show=False):
        """Called when the active theory is changed
        
        [description]
        """
        pass

    def extra_graphic_visible(self, state):
        """[summary]
        
        [description]
        """
        pass

    def Get_Recommended_N(self, cnu, z):
        n=0
        if (cnu>0.1):
            if (z<5): 
                n=5*z
            elif (z<10):
               n=3*z
            else:
                n=z
        elif (cnu>0.03):
            if (z<5):
                n=5*z
            elif (z<13):
               n=3*z
            else:
               n=z
        elif (cnu>0.01):
            if (z<5):
               n=5*z
            elif (z<20):
               n=3*z
            else:
               n=z
        else:
            if (z<5):
               n=5*z
            elif (z<25):
               n=3*z
            else:
               n=z
        return n

    def Set_beta_rcr(self, z, cnu):
        beta_rcr=1
        if (cnu>0):
            logcnu = np.log10(cnu)
            Zeq = z*(1.0923-0.38008*logcnu-0.041605*logcnu*logcnu)
            fZ = 0.65237-0.4223/np.sqrt(Zeq)+2.1586/Zeq-17.581/np.power(Zeq,1.5)+25.071/Zeq/Zeq
            gcnu = 1.2065+0.65493*logcnu+0.073027*logcnu*logcnu
            beta_rcr = fZ*gcnu
        return beta_rcr

    def ind(self, k, i, j):
        """
        Convert k,i,j (3D array) indices to ind (1D array), considering the symmetry of the problem
         \  1 /  (j=i diagonal)
          \  /
         2 \/ 4
           /\
          /  \
         /  3 \ (j=self.N-i diagonal)
        """
        if (j>=i and j>=(self.N-i)): # 1st Quadrant
            ind0 = k*self.SIZE
            if (i<=self.N/2):
                return ind0 + i*(i+3)//2+j-self.N
            else:
                if (self.N % 2 == 0):
                    return ind0 - i*i//2+(2*self.N+1)*i//2 + j - self.N*(2+self.N)//4
                else:
                    return ind0 - i*i//2+(2*self.N+1)*i//2 + j - ((self.N+1)//2)**2
        elif (j>=i and j<(self.N-i)): # 2nd Quadrant
            # Reflection of point on J=self.N-I line
            auxi=self.N-j
            auxj=self.N-i
            return self.ind(k, auxi, auxj)
        elif (j<i and j<(self.N-i)): # 3rd Quadrant
            # INVERSION OF THE POINT WITH RESPECT TO THE POINT (self.N/2, self.N/2)
            auxi=self.N-i
            auxj=self.N-j
            return self.ind(k, auxi, auxj)
        elif (j<i and j>=(self.N-i)): # 4th Quadrant
            # Reflection of point on K=I line
            auxi=j
            auxj=i
            return self.ind(k, auxi, auxj)

    def set_yeq(self):
        aux = self.N/self.Z/2.0
        ind=0
        for k in range(3):
            for i in range(self.N+1):
                mm = max(self.N-i,i)
                for j in range(mm,self.N+1):
                    if ((k!=1) and (abs(i-j)<aux)):
                        self.yeq[ind]=1.0/3.0
                    ind+=1

    def pde_shear(self, y, t):
        if self.stop_theory_flag:
            raise EndComputationRequested
        if t >= self.tmax * self.count:
            self.Qprint("-", end='')
            self.count += 0.1
        n = len(y)
        y_arr = (c_double * n)(*y[:])
        dy_arr = (c_double * n)(*np.zeros(n))
        sch.sccr_dy(y_arr, dy_arr, c_double(t))
        return dy_arr[:]

    def SCCR(self, f=None):
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

        self.taue = self.parameters["tau_e"].value
        Ge = self.parameters["Ge"].value
        Me = self.parameters["Me"].value
        self.cnu = self.parameters["c_nu"].value
        self.Rs = self.parameters["Rs"].value
        try:
            Mw = float(f.file_parameters["Mw"])
        except KeyError:
            self.success_MW = None
            self.fname_missing_mw = f.file_name_short
            self.signal_get_MW.emit(self)
            while self.success_MW is None:
                time.sleep(0.5)
            if self.success_MW:
                f.file_parameters["Mw"] = self.new_MW_val
                Mw = self.new_MW_val
            else:
                self.Qprint('<big><font color=red><b>Mw value is missing in file \"%s\"</b></font></big>' % f.file_name_short)
                return
        gdot = float(f.file_parameters["gdot"])
        gdot=gdot*self.taue

        self.Z = int(np.round(Mw / Me))
        if (self.Z < 1):
            # self.Qprint("WARNING: Mw of %s is too small"%(f.file_name_short))
            self.Z = 1
        if self.parameters["recommendedN"].value:
            self.N = self.Get_Recommended_N(self.cnu, self.Z)
            self.Qprint("recommend N=%d" % self.N)
        else:
            self.N=self.Z*self.parameters["N"].value

        # Setup stuff
        if self.N % 2 == 0:
            self.SIZE = ((self.N+1)*(self.N+3)+1)//4
        else:
            self.SIZE = (self.N+1)*(self.N+3)//4
        
        self.yeq = np.zeros(3*self.SIZE) # Integer division (NEED TO STORE 3 COMPONENTS f(0)=fxx f(1)=fxy f(2)=fyy)
        self.beta_rcr=self.Set_beta_rcr(self.Z,self.cnu)
        self.prevt=0
        self.prevtlog=1e-12
        self.dt=0
        self.NMAXROUSE=50 # To calculate fast Rouse modes inside the tube
        self.relerr = 1.0e-3

        # send value of N, Z, and SIZE to C code
        is_shear = c_int(self.flow_mode == FlowMode.shear)
        sch.set_static_int(c_int(self.N), c_int(self.Z), c_int(self.SIZE), is_shear)
        # initialise gdot, prevt, dt, beta_rcr, and cnu in C code
        sch.set_static_double(c_double(gdot), c_double(self.prevt), c_double(self.dt), c_double(self.beta_rcr), c_double(self.cnu), c_double(self.Rs))

        # Initialize the equilibrium function yeq    
        t = ft.data[:, 0]/self.taue
        t = np.concatenate([[0], t]) # integration starts at t=0
        self.set_yeq()
        sch.set_yeq_static(self.yeq)
        # p = [] # parameters are static in the C code
        dt0 = (self.Z/self.N)**2.5
        
        ## SOLUTION WITH SCIPY.ODEINT   
        self.Qprint("<b>SCCR</b> - File: %s"%f.file_name_short)
        self.tmax = t[-1]
        self.count = 0.1
        self.Qprint('Rate %.3g<br>  0%% ' % gdot, end='')
        try:
            sig = odeint(self.pde_shear, self.yeq, t, args=( ), full_output = 1, h0=dt0, rtol=self.relerr)
        except EndComputationRequested:
            return
        else:
            self.Qprint('&nbsp;100%')
        Sint=np.linspace(0,self.Z,self.N+1)
        Fint=np.zeros(self.N+1)
        t = t[1:]
        sigma = sig[0][1:] 
        if self.flow_mode == FlowMode.shear:
            tmp = self.Z * self.Z / 2.0
            for i in range(len(t)):
                # Stress from tube theory
                Fint = [sigma[i][self.ind(1, j, j)] for j in range(self.N + 1)]
                stressTube = np.trapz(Fint, Sint) * 3.0 / self.Z #*3.0/self.N
                # Fast modes inside the tube
                stressRouse = 0
                for j in range(self.Z, self.NMAXROUSE*self.Z + 1):
                    jsq = j * j
                    # stressRouse+=self.Z*self.Z/2.0/j/j*(1-np.exp(-2.0*j*j*t[i]/self.Z/self.Z))/self.Z*gdot
                    stressRouse += (1 - exp(-jsq * t[i] / tmp)) / jsq 
                tt.data[i, 1] = (stressTube * 4.0 / 5.0 + stressRouse * tmp / self.Z * gdot) * Ge
        else:
            # extensional flow
            Zsq = self.Z * self.Z
            for i in range(len(t)):
                # Stress from tube theory
                Fint = [(sigma[i][self.ind(0, j, j)] - sigma[i][self.ind(2, j, j)]) for j in range(self.N + 1)]
                stressTube = np.trapz(Fint, Sint) * 3.0 / self.Z
                tt.data[i, 1] = stressTube * 4.0 / 5.0 * Ge

class CLTheorySCCR(BaseTheorySCCR, Theory):
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


class GUITheorySCCR(BaseTheorySCCR, QTheory):
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

        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, 5)  # min and max number of modes
        self.spinbox.setPrefix("N=")
        self.spinbox.setSuffix("*Z")
        self.spinbox.setToolTip("Precision of SCCR Calculation")
        self.spinbox.setValue(self.parameters["N"].value)
        self.spinbox.setSingleStep(2)
        tb.addWidget(self.spinbox)

        self.recommendedN = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-light-on-N.png'),
            'Recommended N value')
        self.recommendedN.setCheckable(True)  

        self.thToolsLayout.insertWidget(0, tb)

        connection_id = self.shear_flow_action.triggered.connect(
            self.select_shear_flow)
        connection_id = self.extensional_flow_action.triggered.connect(
            self.select_extensional_flow)                     
        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged)
        connection_id = self.recommendedN.triggered.connect(
            self.handle_recommendedN)

    def select_shear_flow(self):
        self.flow_mode = FlowMode.shear
        self.tbutflow.setDefaultAction(self.shear_flow_action)

    def select_extensional_flow(self):
        self.flow_mode = FlowMode.uext
        self.tbutflow.setDefaultAction(self.extensional_flow_action)

    def handle_recommendedN(self, checked):
        self.spinbox.setEnabled(not checked)
        self.set_param_value("recommendedN", checked)

    def handle_spinboxValueChanged(self, value):
        self.set_param_value("N", value)

    def set_extra_data(self, extra_data):
        """Set extra data when loading project"""
        self.spinbox.setValue(self.parameters["N"].value)
        self.recommendedN.setChecked(self.parameters["recommendedN"].value)
        self.handle_recommendedN(self.parameters["recommendedN"].value)
