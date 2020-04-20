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
"""Module TheorySCCROLD

Module for the SCCROLD theory for the non-linear flow of entangled polymers.

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
from theory_helpers import FlowMode

class TheorySCCROLD(CmdBase):
    """SCCROLD
    
    [description]
    """
    thname = "SCCROLD"
    description = "SCCROLD theory for linear entangled polymers"
    citations = "Graham, R.S., Likhtman, A.E., McLeish, T.C.B. & Milner, S.T., J. Rheo., 2003, 47, 1171-1200"
    doi = "http://dx.doi.org/10.1122/1.1595099"

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
        return GUITheorySCCROLD(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheorySCCROLD(
                name, parent_dataset, ax)


class BaseTheorySCCROLD:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/NLVE/Theory/theory.html#SCCROLD'
    single_file = False
    thname = TheorySCCROLD.thname
    citations = TheorySCCROLD.citations
    doi = TheorySCCROLD.doi

    def __init__(self, name="", parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.SCCROLD
        self.has_modes = False

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
        self.parameters["N"] = Parameter(
            name="N",
            value=1,
            description="npoints=N*Z Precision of SCCROLD (odd number)",
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


    def init_flow_mode(self):
        """Find if data files are shear or extension"""
        try:
            f = self.theory_files()[0]
            if f.file_type.extension == 'shear':
                self.flow_mode = FlowMode.shear
            else:
                self.flow_mode = FlowMode.uext
        except Exception as e:
            print("in SCCROLD init:", e)
            self.flow_mode = FlowMode.shear  #default mode: shear

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

    def sigmadot_uext_nostretch(self, sigma, t, p):
        """Rolie-Poly differential equation under elongation flow, wihtout stretching
        
        [description]
        
        Arguments:
            - sigma {array} -- vector of state variables, sigma = [sxx, syy]
            - t {float} -- time
            - p {array} -- vector of the parameters, p = [tauD, tauR, beta, delta, epsilon_dot]
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

    def d1(self, s):
        """ 
        1D diffusion coefficient (reptation + CLF)
        With cut-off for maximum D=a^2/6/tau_e
        """
        ad = 1.15
        w=0
        waux=1.0/np.pi/np.pi/3.0*(np.pi*np.pi/2.0-1.0/self.Z)
        s*=self.Z/self.N
        if (s==0):
            w = waux
        elif (s<ad*np.sqrt(self.Z)):
            w=1.0/np.pi/np.pi/3.0*(ad*ad/s/s-1.0/self.Z);
        if (w>waux):
            w = waux
        return w

    def d(self, i, j):
        """
        1D diffusion coefficient (reptation + CLF)
        """
        sm=min(i, j, self.N-i, self.N-j)
        return 1.0/3.0/np.pi/np.pi/self.Z+self.d1(sm);

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

    def get_im(self, i,j):
        im=i;
        imin=i;
        if(j<imin):
            im=j
            imin=j
        if(self.N-i<imin):
            im=i
            imin=self.N-i
        if(self.N-j<imin):
            im=j
        return im


    def pde_shear(self, y, t, p):
        """    [description]
        """    
        if (t>self.prevt):
            self.dt=t-self.prevt
            self.prevt=t
            if(np.log10(t)-np.log10(self.prevtlog)>1):
                self.Qprint("t=%g"%(t*self.taue))
                self.prevtlog=t
        gdot = p[0]
        Rs = 2.0

        # Instantaneous number of entanglements (normalized arc length of primitive path)
        # And norm of f
        normf = [y[self.ind(0,j,j)] + 2*y[self.ind(2,j,j)] for j in range(self.N+1)]
        zstar=(1+sum(np.sqrt(normf[i]) for i in range(1,self.N)))*self.Z/self.N;

        dy = np.zeros(3*self.SIZE)
        if self.stop_theory_flag:
            return dy

        for k in range(3):
            for i in range(1, self.N):
                mm = max(self.N-i,i)
                for j in range(mm, self.N):

                    im=self.get_im(i,j)

                    fkij = self.ind(k,i,j)
                    fkip1jp1 = self.ind(k,i+1,j+1)
                    fkim1jm1 = self.ind(k,i-1,j-1)
                    fkip1j = self.ind(k,i+1,j)
                    fkim1j = self.ind(k,i-1,j)
                    fkijp1 = self.ind(k,i,j+1)
                    fkijm1 = self.ind(k,i,j-1)

                    dy[fkij]+=1.0/2.0/np.pi/np.pi*self.N/self.Z*self.N/self.Z*Rs* \
					        ((y[fkip1j]-y[fkim1j])/2.0*  # Retr (s)
					        (np.log(normf[i+1])-np.log(normf[i-1]))/2.0 
                            +y[fkij]*(np.log(normf[i+1])+np.log(normf[i-1])-2.0*np.log(normf[i])))

                    dy[fkij]+=1.0/2.0/np.pi/np.pi*self.N/self.Z*self.N/self.Z*Rs* \
					        ((y[fkijp1]-y[fkijm1])/2.0*   # Retr (s')
					        (np.log(normf[j+1])-np.log(normf[j-1]))/2.0
					        +y[fkij]*(np.log(normf[j+1])+np.log(normf[j-1])-2.0*np.log(normf[j])))
            
                    # Chain rule applied to Rept+CLF term
                    dy[fkij]+=self.N/self.Z*self.N/self.Z/np.sqrt(normf[im])*(
					        (self.d(i+1,j+1)-self.d(i-1,j-1))/2.0*(y[fkip1jp1]-y[fkim1jm1])/2.0/np.sqrt(normf[im])	# CLF
					        +self.d(i,j)*(y[fkip1jp1]-y[fkim1jm1])/2.0*
					        (1.0/np.sqrt(normf[im+1])-1.0/np.sqrt(normf[im-1]))/2.0
					        +self.d(i,j)/np.sqrt(normf[im])*(y[fkip1jp1]+y[fkim1jm1]-2.0*y[fkij])
					        )
    
        # Get partially updated y to calculate retraction rate
        yn = y + dy*self.dt
        normfn = [yn[self.ind(0,j,j)] + 2*yn[self.ind(2,j,j)] for j in range(self.N+1)]
        lam=0
        if (self.dt>0):
            for i in range (1,self.N):
                lam-=(normfn[i]-normf[i])/self.N/2.0/self.dt/np.sqrt(normf[i])
    
        for k in range(3):
            for i in range(1, self.N):
                mm = max(self.N-i,i)
                for j in range(mm, self.N):

                    fkij = self.ind(k,i,j)
                    fkip1jp1 = self.ind(k,i+1,j+1)
                    fkim1jm1 = self.ind(k,i-1,j-1)
                    fkip1j = self.ind(k,i+1,j)
                    fkim1j = self.ind(k,i-1,j)
                    fkijp1 = self.ind(k,i,j+1)
                    fkijm1 = self.ind(k,i,j-1)

                    dy[fkij]+=self.N/self.Z*self.N/self.Z*1.5*(lam+1.0/3.0/self.beta_rcr/self.Z/self.Z/self.Z)*self.cnu*(self.Z/zstar) \
                        *((y[fkip1j]+y[fkim1j]-2.0*y[fkij]-self.yeq[fkip1j]-self.yeq[fkim1j]+2.0*self.yeq[fkij])  # CCR
                        /np.sqrt(normf[i])
                        +(y[fkip1j]-y[fkim1j]-self.yeq[fkip1j]+self.yeq[fkim1j])/2.0
                        *(1.0/np.sqrt(normf[i+1])-1.0/np.sqrt(normf[i-1]))/2.0
                
                        +(y[fkijp1]+y[fkijm1]-2.0*y[fkij]-self.yeq[fkijp1]-self.yeq[fkijm1]+2.0*self.yeq[fkij]) # CCR
                        /np.sqrt(normf[j])
                        +(y[fkijp1]-y[fkijm1]-self.yeq[fkijp1]+self.yeq[fkijm1])/2.0
                        *(1.0/np.sqrt(normf[j+1])-1.0/np.sqrt(normf[j-1]))/2.0)
                        
        for i in range(1, self.N):
            mm = max(self.N-i,i)
            for j in range(mm, self.N):
                f0ij = self.ind(0,i,j)
                f1ij = self.ind(1,i,j)
                f2ij = self.ind(2,i,j)
                # Shear Flow
                dy[f0ij]+=2*gdot*y[f1ij]
                dy[f1ij]+=gdot*y[f2ij]
        return dy


    def SCCROLD(self, f=None):
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
        Mw = float(f.file_parameters["Mw"])
        gdot = float(f.file_parameters["gdot"])
        gdot=gdot*self.taue

        self.Z = int(np.round(Mw / Me))
        if (self.Z < 1):
            # self.Qprint("WARNING: Mw of %s is too small"%(f.file_name_short))
            self.Z = 1
        if self.parameters["recommendedN"].value:
            self.N = self.Get_Recommended_N(self.cnu, self.Z)
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

        # Initialize the equilibrium function yeq    
        t = ft.data[:, 0]/self.taue
        #t = np.concatenate([[0], t])
        self.set_yeq()
        p = [gdot]
        dt0 = (self.Z/self.N)**2.5
        
        ## SOLUTION WITH SCIPY.ODEINT   
        self.Qprint("<b>SCCROLD</b> - File: %s"%f.file_name_short)
        try:
            sig = odeint(self.pde_shear, self.yeq, t, args=(p, ), full_output = 1, h0=dt0, rtol=self.relerr)
        except EndComputationRequested:
            pass
        self.Qprint("<b>Done</b>")
        self.Qprint("")

        Sint=np.linspace(0,self.Z,self.N+1)
        Fint=np.zeros(self.N+1)
        #Gxy=np.zeros(len(t)-1)
        Gxy=np.zeros(len(t))
        #for i in range(1, len(t)):
        for i in range(len(t)):
            # Stress from tube theory
            Fint = [sig[0][i][self.ind(1,j,j)] for j in range(self.N+1)]
            stressTube = np.trapz(Fint,Sint)*3.0/self.Z #*3.0/self.N

            # Fast modes inside the tube
            stressRouse=0
            for j in range(self.Z,self.NMAXROUSE*self.Z+1):
                stressRouse+=self.Z*self.Z/2.0/j/j*(1-np.exp(-2.0*j*j*t[i]/self.Z/self.Z))/self.Z*gdot

            tt.data[i,1]=(stressTube*4.0/5.0+stressRouse)*Ge

class CLTheorySCCROLD(BaseTheorySCCROLD, Theory):
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


class GUITheorySCCROLD(BaseTheorySCCROLD, QTheory):
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
        self.spinbox.setToolTip("Precision of SCCROLD Calculation")
        self.spinbox.setValue(self.parameters["N"].value)
        self.spinbox.setSingleStep(2)
        tb.addWidget(self.spinbox)

        self.recommendedN = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-infinite.png'),
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




