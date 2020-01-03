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
"""Module TheoryShanbhagMaxwellModes

Module that defines theories related to Maxwell modes, in the frequency and time domains 
based on the codes pyRespect-time (10.1002/mats.201900005) and pyRespect-frequency (10.3933/ApplRheol-23-24628)

"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from DataTable import DataTable
from Parameter import Parameter, ParameterType, ShiftType, OptType
from Theory import Theory
from QTheory import QTheory
from PyQt5.QtWidgets import QWidget, QToolBar, QComboBox, QSpinBox, QAction, QStyle
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from DraggableArtists import DragType, DraggableModesSeries
from scipy.optimize import nnls, minimize, least_squares
from scipy.interpolate import interp1d
from scipy.integrate import cumtrapz, quad
import time

class TheoryShanbhagMaxwellModesFrequency(CmdBase):
    """Extract continuous and discrete relaxation spectra from complex modulus G*(w)
        
    * **Parameters**
       - plateau : is there a residual plateau in the data (default False).
       - lamC : Specify lambda_C instead of using the one inferred from the L-curve (default 0, use the L-curve).
       - SmFacLam = Smoothing Factor.
       - MaxNumModes = Max Number of Modes (default 0, automatically determine the optimal number of modes).
       - lam_min = lower limit of lambda for lcurve calculation (default 1e-10).
       - lam_max = higher limit of lambda for lcurve calculation (default 1e3).
       - lamDensity = lambda density per decade (default 3, use 2 or more).
       - rho_cutoff = Threshold to avoid picking too small lambda for L-curve without (default 0).
       - deltaBaseWeightDist = how finely to sample BaseWeightDist (default 0.2).
       - minTauSpacing = how close do successive modes (tau2/tau1) have to be before we try to mege them (default 1.25).
    
    """
    thname = "Shanbhag Maxwell Modes"
    description = "Shanbhag Maxwell modes, frequency dependent"
    citations = "Takeh, A. and Shanbhag, S., Appl. Rheol. 2013, 23, 24628"
    doi = 'http://dx.doi.org/10.3933/ApplRheol-23-24628'
    
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
        return GUITheoryShanbhagMaxwellModesFrequency(name, parent_dataset, ax) if (
            CmdBase.mode == CmdMode.GUI) else CLTheoryShanbhagMaxwellModesFrequency(
                name, parent_dataset, ax)


class BaseTheoryShanbhagMaxwellModesFrequency:
    """[summary] 
        
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/LVE/Theory/theory.html#shanbhag-maxwell-modes'
    single_file = True
    thname = TheoryShanbhagMaxwellModesFrequency.thname
    citations = TheoryShanbhagMaxwellModesFrequency.citations
    doi = TheoryShanbhagMaxwellModesFrequency.doi 

    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**
                
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.ShanBhagMaxwellModesFrequency
        self.has_modes = True
        self.MAX_MODES = 40
        self.view_modes = True
        wmin = self.parent_dataset.minpositivecol(0)
        wmax = self.parent_dataset.maxcol(0)
        nmodes = int(np.round(np.log10(wmax / wmin)))

        self.parameters["plateau"] = Parameter(
            "plateau",
            False,
            "is there a residual plateau?",
            ParameterType.boolean,
            opt_type=OptType.const)
        self.parameters["ns"] = Parameter(
            "ns",
            100,
            "Number of grid points to represent the continuous spectrum (typical 50-100)",
            ParameterType.integer,
            opt_type=OptType.const)
        self.parameters["lamC"] = Parameter(
            "lamC",
            0,
            "Specify lambda_C",
            ParameterType.real,
            opt_type=OptType.nopt)
        self.parameters["SmFacLam"] = Parameter(
            name="SmFacLam",
            value=0,
            description="Smoothing Factor (between -1 and 1)",
            type=ParameterType.discrete_integer,
            opt_type=OptType.const,
            discrete_values=[-1,0,1])
        self.parameters["MaxNumModes"] = Parameter(
            "MaxNumModes",
            0,
            "Max Number of Modes",
            ParameterType.integer,
            opt_type=OptType.opt)
        self.parameters["lam_min"] = Parameter(
            "lam_min",
            1e-10,
            "lower limit of lambda for lcurve calculation",
            ParameterType.real,
            opt_type=OptType.nopt)
        self.parameters["lam_max"] = Parameter(
            "lam_max",
            1e3,
            "higher limit of lambda for lcurve calculation",
            ParameterType.real,
            opt_type=OptType.nopt)
        self.parameters["lamDensity"] = Parameter(
            "lamDensity",
            3,
            "lambda density per decade",
            ParameterType.integer,
            opt_type=OptType.nopt)
        self.parameters["rho_cutoff"] = Parameter(
            "rho_cutoff",
            0,
            "Threshold to avoid picking too small lambda",
            ParameterType.real,
            opt_type=OptType.nopt)
        self.parameters["deltaBaseWeightDist"] = Parameter(
            "deltaBaseWeightDist",
            0.2,
            "how finely to sample BaseWeightDist",
            ParameterType.real,
            opt_type=OptType.nopt)
        self.parameters["minTauSpacing"] = Parameter(
            "minTauSpacing",
            1.25,
            "how close modes (tau2/tau1) for merge",
            ParameterType.real,
            opt_type=OptType.nopt)

        self.autocalculate = False

        # GRAPHIC MODES
        self.graphicmodes = []
        self.spectrum = []
        ns = self.parameters['ns'].value
        self.scont = np.zeros(ns)
        self.Hcont = np.zeros(ns)
        self.sdisc = np.zeros(ns)
        self.Hdisc = np.zeros(ns)
        self.setup_graphic_modes()

    # def drag_mode(self, dx, dy):
    #     """[summary]
        
    #     [description]
        
    #     Arguments:
    #         - dx {[type]} -- [description]
    #         - dy {[type]} -- [description]
    #     """
    #     nmodes = self.parameters["nmodes"].value
    #     if self.parent_dataset.parent_application.current_view.log_x:
    #         self.set_param_value("logwmin", np.log10(dx[0]))
    #         self.set_param_value("logwmax", np.log10(dx[nmodes - 1]))
    #     else:
    #         self.set_param_value("logwmin", dx[0])
    #         self.set_param_value("logwmax", dx[nmodes - 1])

    #     if self.parent_dataset.parent_application.current_view.log_y:
    #         for i in range(nmodes):
    #             self.set_param_value("logG%02d" % i, np.log10(dy[i]))
    #     else:
    #         for i in range(nmodes):
    #             self.set_param_value("logG%02d" % i, dy[i])

    #     self.do_calculate("")
    #     self.update_parameter_table()

    def setup_graphic_modes(self):
        """[summary]
        
        [description]
        """
        self.contspectrum = self.ax.plot([], [])[0]
        self.contspectrum.set_marker('*')
        self.contspectrum.set_linestyle('--')
        self.contspectrum.set_visible(self.view_modes)
        self.contspectrum.set_color('green')
        self.contspectrum.set_linewidth(5)
        self.contspectrum.set_label('')
        #self.contspectrum.set_markerfacecolor('yellow')
        self.contspectrum.set_markeredgecolor('black')
        self.contspectrum.set_markeredgewidth(3)
        self.contspectrum.set_markersize(6)
        self.contspectrum.set_alpha(0.5)

        self.discspectrum = self.ax.plot([], [])[0]
        self.discspectrum.set_marker('D')
        self.discspectrum.set_visible(self.view_modes)
        self.discspectrum.set_label('')
        self.discspectrum.set_markerfacecolor('yellow')
        self.discspectrum.set_markeredgecolor('black')
        self.discspectrum.set_markeredgewidth(3)
        self.discspectrum.set_markersize(8)
        self.discspectrum.set_alpha(0.5)

        self.plot_theory_stuff()

    def destructor(self):
        """Called when the theory tab is closed
        
        [description]
        """
        self.graphicmodes_visible(False)
        self.ax.lines.remove(self.contspectrum)
        self.ax.lines.remove(self.discspectrum)

    def show_theory_extras(self, show=False):
        """Called when the active theory is changed
        
        [description]
        """
        if CmdBase.mode == CmdMode.GUI:
            self.Qhide_theory_extras(show)
        self.graphicmodes_visible(show)

    def graphicmodes_visible(self, state):
        """[summary]
        
        [description]
        """
        self.view_modes = state
        self.contspectrum.set_visible(self.view_modes)
        self.discspectrum.set_visible(self.view_modes)
        # if self.view_modes:
        #     self.artistmodes.connect()
        # else:
        #     self.artistmodes.disconnect()
        # self.do_calculate("")
        self.parent_dataset.parent_application.update_plot()

    def get_modes(self):
        """[summary]
        
        [description]
        
        Returns:
            - [type] -- [description]
        """
        nmodes = self.parameters["nmodes"].value
        freq = np.logspace(self.parameters["logwmin"].value,
                           self.parameters["logwmax"].value, nmodes)
        tau = 1.0 / freq
        G = np.zeros(nmodes)
        for i in range(nmodes):
            G[i] = np.power(10, self.parameters["logG%02d" % i].value)
        return tau, G

    def set_modes(self, tau, G):
        """[summary]
        
        [description]
        
        Arguments:
            - tau {[type]} -- [description]
            - G {[type]} -- [description]
        """
        print("set_modes not allowed in this theory (%s)" % self.name)

    def kernel_prestore(self, H, kernMat, *argv):
        """
            turbocharging kernel function evaluation by prestoring kernel matrix
            Date    : 8/17/2018
            Function: kernel_prestore(input) returns K*h, where h = exp(H)
            
            Same as kernel, except prestoring hs, S, and W to improve speed 3x.
            
            outputs the 2n*1 dimensional vector K(H)(w) which is comparable to G* = [G'|G"]'
            3/11/2019: returning Kh + G0
                    
            Input: H = substituted CRS,
                    kernMat = 2n*ns matrix [(ws^2/1+ws^2) | (ws/1+ws)]'*hs
                        
        """
        if len(argv) > 0:
            n = int(kernMat.shape[0]/2)
            G0v = np.zeros(2*n)
            G0v[:n] = argv[0]
        else:
            G0v = 0.
        
        return np.dot(kernMat, np.exp(H)) + G0v

    def residualLM(self, H, lam, Gexp, kernMat):
        """
        %
        % HELPER FUNCTION: Gets Residuals r
        %"""

        n   = int(kernMat.shape[0]/2)
        ns  = kernMat.shape[1]
        
        nl  = ns - 2
        r   = np.zeros(2*n + nl)

        # if plateau then unfurl G0
        if len(H) > ns:
            G0       = H[-1]
            H        = H[:-1]
            r[0:2*n] = (1. - self.kernel_prestore(H, kernMat, G0)/Gexp)
        else:
            r[0:2*n] = (1. - self.kernel_prestore(H,kernMat)/Gexp)
        
        # the curvature constraint is not affected by G0	
        r[2*n:2*n+nl] = np.sqrt(lam) * np.diff(H, n=2)  # second derivative
        
        return r
        
    def jacobianLM(self, H, lam, Gexp, kernMat):
        """
        
        HELPER FUNCTION: Gets Jacobian J
            returns a (n+nl * ns) matrix Jr; (ns + 1) if G0 is also supplied.
            
            Jr_(i, j) = dr_i/dH_j
            
            It uses kernelD, which approximates dK_i/dH_j, where K is the kernel	
        
        """
        
        n   = int(kernMat.shape[0]/2)
        ns  = kernMat.shape[1]
        nl  = ns - 2

        # L is a nl*ns tridiagonal matrix with 1 -2 and 1 on its diagonal.
        L  = np.diag(np.ones(ns-1), 1) + np.diag(np.ones(ns-1),-1) + np.diag(-2. * np.ones(ns))	     
        L  = L[1:nl+1,:]


        Jr  = np.zeros((2*n + nl,ns))	
            
        #
        # Furnish the Jacobian Jr - (2n+nl)*ns matrix
        # Kmatrix is 2*n * ns matrix
        #
        Kmatrix = np.dot((1./Gexp).reshape(2*n,1), np.ones((1,ns)))

        if len(H) > ns:

            G0     = H[-1]
            H      = H[:-1]

            Jr  = np.zeros((2*n + nl,ns+1))	
            
            Jr[0:2*n, 0:ns]   = -self.kernelD(H, kernMat) * Kmatrix;
            Jr[0:n, ns]       = -1./Gexp[:n]						# nonzero dr_i/dG0 only for G'


            Jr[2*n:2*n+nl,0:ns] = np.sqrt(lam) * L;
            Jr[2*n:2*n+nl, ns]  = np.zeros(nl)						# column for dr_i/dG0 = 0
            
        else:

            Jr  = np.zeros((2*n + nl,ns))	

            Jr[0:2*n, 0:ns]     = -self.kernelD(H, kernMat) * Kmatrix;
            Jr[2*n:2*n+nl,0:ns] = np.sqrt(lam) * L;
        
        return	Jr

    def kernelD(self, H, kernMat):
        """
        Function: kernelD(input)
            
        outputs the 2n*ns dimensional vector DK(H)(w)
        It approximates dK_i/dH_j = K * e(H_j):
            
        Input: H       = substituted CRS,
                kernMat = matrix for faster kernel evaluation
        Output: DK     = Jacobian of H
            
        """

        n   = int(kernMat.shape[0]/2)
        ns  = kernMat.shape[1]
            
        Hsuper  = np.dot(np.ones((2*n,1)), np.exp(H).reshape(1, ns))       
        DK      = kernMat * Hsuper
        
        return DK


    def getKernMat(self, s, w):
        """furnish kerMat() which helps faster kernel evaluation, given s, w
        Generates a 2n*ns matrix [(ws^2/1+ws^2) | (ws/1+ws)]'*hs, which can be 
        multiplied with exp(H) to get predicted G*"""
        
        ns          = len(s)
        hsv         = np.zeros(ns)

        hsv[0]      = 0.5 * np.log(s[1]/s[0])
        hsv[ns-1]   = 0.5 * np.log(s[ns-1]/s[ns-2])
        hsv[1:ns-1] = 0.5 * (np.log(s[2:ns]) - np.log(s[0:ns-2]))

        S, W        = np.meshgrid(s, w)
        ws          = S*W
        ws2         = ws**2
        
        return np.vstack((ws2/(1+ws2), ws/(1+ws2))) *hsv

    def getH(self, lam, Gexp, H, kernMat, G0=0):
        """
        minimize_H  V(lambda) := ||Gexp - kernel(H)||^2 +  lambda * ||L H||^2

        Input  : lambda  = regularization parameter ,
                Gexp    = experimental data,
                H       = guessed H,
                kernMat = matrix for faster kernel evaluation
                G0      = optional
        
        Output : H_lam, [G0]
                Default uses Trust-Region Method with Jacobian supplied by jacobianLM
        """
        # send Hplus = [H, G0], on return unpack H and G0
        if G0>0:
            Hplus= np.append(H, G0)
            res_lsq = least_squares(self.residualLM, Hplus, jac=self.jacobianLM, args=(lam, Gexp, kernMat))
            return res_lsq.x[:-1], res_lsq.x[-1]
            
        # send normal H, and collect optimized H back
        else:
            res_lsq = least_squares(self.residualLM, H, jac=self.jacobianLM, args=(lam, Gexp, kernMat))			
            return res_lsq.x


    def InitializeH(self, Gexp, s, kernMat,  G0=0):
        """
        Function: InitializeH(input)
            
        Input:  Gexp    = 2n*1 vector [G';G"],
                s       = relaxation modes,
                kernMat = matrix for faster kernel evaluation
                G0      = optional; if plateau is nonzero	
            
        Output: H = guessed H
                G0 = optional guess if *argv is nonempty	
        """
        
        #
        # To guess spectrum, pick a negative Hgs and a large value of lambda to get a
        # solution that is most determined by the regularization
        # March 2019; a single guess is good enough now, because going from large lambda to small
        #             lambda in lcurve.

        H    = -5.0 * np.ones(len(s)) + np.sin(np.pi * s)
        lam  = 1e0
        
        if G0>0:
            G0       = argv[0]
            Hlam, G0 = self.getH(lam, Gexp, H, kernMat, G0)		
            return Hlam, G0
        else:
            Hlam     = self.getH(lam, Gexp, H, kernMat)
            return Hlam

    def getAmatrix(self, ns):
        """Generate symmetric matrix A = L' * L required for error analysis:
        helper function for lcurve in error determination"""
        # L is a ns*ns tridiagonal matrix with 1 -2 and 1 on its diagonal;
        nl = ns - 2
        L  = np.diag(np.ones(ns-1), 1) + np.diag(np.ones(ns-1),-1) + np.diag(-2. * np.ones(ns))
        L  = L[1:nl+1,:]
                
        return np.dot(L.T, L)

    def getBmatrix(self, H, kernMat, Gexp, *argv):
        """get the Bmatrix required for error analysis; helper for lcurve()
        not explicitly accounting for G0 in Jr because otherwise I get underflow problems"""
        n   = int(len(Gexp)/2)
        ns  = len(H)
        nl  = ns - 2
        r   = np.zeros(n)   	  # vector of size (n);

        # furnish relevant portion of Jacobian and residual
        Kmatrix = np.dot((1./Gexp).reshape(2*n,1), np.ones((1,ns)))
        Jr      = -self.kernelD(H, kernMat) * Kmatrix;    

        # if plateau then unfurl G0
        if len(argv) > 0:
            G0 = argv[0]
            r  = (1. - self.kernel_prestore(H, kernMat, G0)/Gexp)
        else:
            r = (1. - self.kernel_prestore(H, kernMat)/Gexp)
        
        B = np.dot(Jr.T, Jr) + np.diag(np.dot(r.T, Jr))

        return B

    def oldLamC(self, lam, rho, eta):

        #
        # 8/1/2018: Making newer strategy more accurate and robust: dividing by minimum rho/eta
        # which is not as sensitive to lam_min, lam_max. This makes lamC robust to range of lam explored
        #
        #er = rho/np.amin(rho) + eta/np.amin(eta);
        er    = rho/np.amin(rho) + eta/(np.sqrt(np.amax(eta)*np.amin(eta)))

        #
        # Since rho v/s lambda is smooth, we can interpolate the coarse mesh to find minimum
        #
        # change 3/20/2019: Scipy 0.17 has a bug with extrapolation: so making lami tad smaller 
        lami = np.logspace(np.log10(min(lam)+1e-15), np.log10(max(lam)-1e-15), 1000)
        erri = np.exp(interp1d(np.log(lam), np.log(er), kind='cubic', bounds_error=False,
                        fill_value=(np.log(er[0]), np.log(er[-1])))(np.log(lami)))


        ermin = np.amin(erri)
        eridx = np.argmin(erri)	
        lamC  = lami[eridx]
            
        #
        # 2/2: Copying 12/18 edit from pyReSpect-time;
        #      for rough data have cutoff at rho = rho_cutoff?
        #
        rhoF  = interp1d(lam, rho, bounds_error=False, fill_value=(rho[0], rho[-1]))

        if  rhoF(lamC) <= self.parameters['rho_cutoff'].value:
            try:
                eridx = (np.abs(rhoF(lami) - self.parameters['rho_cutoff'].value)).argmin()
                if lami[eridx] > lamC:
                    lamC = lami[eridx]				
            except:
                pass

        return lamC


    def lcurve(self, Gexp, Hgs, kernMat, *argv):
        """
        Function: lcurve(input)
        
        Input: Gexp    = 2n*1 vector [Gt],
                Hgs     = guessed H,
                kernMat = matrix for faster kernel evaluation
                G0      = optionally
                
        
        Output: lamC and 3 vectors of size npoints*1 contains a range of lambda, rho
                and eta. "Elbow"  = lamC is estimated using a *NEW* heuristic AND by Hansen method

        
            March 2019: starting from large lambda to small cuts calculation time by a lot
                    also gives an error estimate 
        """

        plateau = self.parameters['plateau'].value
        if plateau:
            G0 = argv[0]

        lamDensity = self.parameters['lamDensity'].value
        lam_max = self.parameters['lam_max'].value
        lam_min = self.parameters['lam_min'].value
        npoints = int(lamDensity * (np.log10(lam_max) - np.log10(lam_min)))
        hlam    = (lam_max/lam_min)**(1./(npoints-1.))	
        lam     = lam_min * hlam**np.arange(npoints)
        eta     = np.zeros(npoints)
        rho     = np.zeros(npoints)
        logP    = np.zeros(npoints)
        H       = Hgs.copy()
        n       = len(Gexp)
        ns      = len(H)
        nl      = ns - 2
        logPmax = -np.inf					# so nothing surprises me!
        Hlambda = np.zeros((ns, npoints))

        # Error Analysis: Furnish A_matrix
        Amat       = self.getAmatrix(len(H))
        _, LogDetN = np.linalg.slogdet(Amat)
                
        #
        # This is the costliest step
        #
        for i in reversed(range(len(lam))):
            
            lamb    = lam[i]
            
            if plateau:
                H, G0   = self.getH(lamb, Gexp, H, kernMat, G0)			
                rho[i]  = np.linalg.norm((1. - self.kernel_prestore(H, kernMat, G0)/Gexp))
                Bmat    = self.getBmatrix(H, kernMat, Gexp, G0)			
            else:
                H       = self.getH(lamb, Gexp, H, kernMat)
                rho[i]  = np.linalg.norm((1. - self.kernel_prestore(H,kernMat)/Gexp))
                Bmat    = self.getBmatrix(H, kernMat, Gexp)

            eta[i]       = np.linalg.norm(np.diff(H, n=2))
            Hlambda[:,i] = H

            _, LogDetC = np.linalg.slogdet(lamb*Amat + Bmat)
            V          =  rho[i]**2 + lamb * eta[i]**2		
                        
            # this assumes a prior exp(-lam)
            logP[i]    = -V + 0.5 * (LogDetN + ns*np.log(lamb) - LogDetC) - lamb
            
            if(logP[i] > logPmax):
                logPmax = logP[i]
            elif(logP[i] < logPmax - 18):
                break		

        # truncate all to significant lambda
        lam  = lam[i:]
        logP = logP[i:]
        eta  = eta[i:]
        rho  = rho[i:]
        logP = logP - max(logP)

        Hlambda = Hlambda[:,i:]

        #
        # currently using both schemes to get optimal lamC
        # new lamM works better with actual experimental data  
        #
        lamC = self.oldLamC(lam, rho, eta)
        plam = np.exp(logP); plam = plam/np.sum(plam)
        lamM = np.exp(np.sum(plam*np.log(lam)))

        #
        # Dialling in the Smoothness Factor
        #
        SmFacLam = self.parameters['SmFacLam'].value
        if SmFacLam > 0:
            lamM = np.exp(np.log(lamM) + SmFacLam*(max(np.log(lam)) - np.log(lamM)))
        elif SmFacLam < 0:
            lamM = np.exp(np.log(lamM) + SmFacLam*(np.log(lamM) - min(np.log(lam))))

        #
        # printing this here for now because storing lamC for sometime only
        #
        # if par['plotting']:
        #     plt.clf()
        #     plt.axvline(x=lamC, c='k', label=r'$\lambda_c$')
        #     plt.axvline(x=lamM, c='gray', label=r'$\lambda_m$')
        #     plt.ylim(-20,1)
        #     plt.plot(lam, logP, 'o-')
        #     plt.xscale('log')
        #     plt.xlabel(r'$\lambda$')
        #     plt.ylabel(r'$\log\,p(\lambda)$')
        #     plt.legend(loc='upper left')
        #     plt.tight_layout()
        #     plt.savefig('output/logP.pdf')

        return lamM, lam, rho, eta, logP, Hlambda

    def MaxwellModes(self, z, w, Gexp, isPlateau):
        """
        
        Function: MaxwellModes(input)
        
        Solves the linear least squares problem to obtain the DRS
        
        Input: z = points distributed according to the density,
                t    = n*1 vector contains times,
                Gexp = 2n*1 vector contains Gp and Gpp
                isPlateau = True if G0 \neq 0	
        
        Output: g, tau = spectrum  (array)
                error = relative error between the input data and the G(t) inferred from the DRS
                condKp = condition number
        
        """

        N      = len(z)
        tau    = np.exp(z)
        n      = len(w)

        #
        # Prune small -ve weights g(i)
        #
        g, error, condKp = self.nnLLS(w, tau, Gexp, isPlateau)

        # first remove runaway modes outside window with potentially large weight
        izero = np.where(np.logical_or(max(w)*min(tau) < 0.02, min(w)*max(tau) > 50.))
        tau   = np.delete(tau, izero)
        g     = np.delete(g, izero)

        # search for small weights (gi) 
        if isPlateau:
            izero = np.where(g[:-1]/np.max(g[:-1]) < 1e-8)
        else:
            izero = np.where(g/np.max(g) < 1e-8)

        tau   = np.delete(tau, izero);
        g     = np.delete(g, izero)
            
        return g, tau, error, condKp

    def nnLLS(self, w, tau, Gexp, isPlateau):
        """
        #
        # Helper subfunction which does the actual LLS problem
        # helps MaxwellModes
        #
        """	
        n       = int(len(Gexp)/2)
        ntau    = len(tau)
        S, W    = np.meshgrid(tau, w)
        ws      = S*W
        ws2     = ws**2
        K       = np.vstack((ws2/(1+ws2), ws/(1+ws2)))   # 2n * nmodes

        # K is n*ns [or ns+1]
        if isPlateau:
            K   = np.hstack(( K, np.ones((len(Gexp), 1)) ))  # G' needs some G0
            K[n:, ntau] = 0.								 # G" doesn't have G0 contrib
        #
        # gets (Gst/GstE - 1)^2, instead of  (Gst -  GstE)^2
        #
        Kp      = np.dot(np.diag((1./Gexp)), K)
        condKp  = np.linalg.cond(Kp)
        g       = nnls(Kp, np.ones(len(Gexp)))[0]
            
        GstM   	= np.dot(K, g)
        error 	= np.sum((GstM/Gexp - 1.)**2)

        return g, error, condKp

    def GetWeights(self, H, w, s, wb):

        """
        %
        % Function: GetWeights(input)
        %
        % Finds the weight of "each" mode by taking a weighted average of its contribution
        % to Gp and Gpp, mixed with an even distribution given by `wb`
        %
        % Input: H = CRS (ns * 1)
        %        w = n*1 vector contains times
        %        s = relaxation modes (ns * 1)
        %       wb = weightBaseDist
        %
        % Output: wt = weight of each mode
        %
        """
    
        ns         = len(s)
        n          = len(w)

        hs         = np.zeros(ns)
        wt         = hs
        
        hs[0]      = 0.5 * np.log(s[1]/s[0])
        hs[ns-1]   = 0.5 * np.log(s[ns-1]/s[ns-2])
        hs[1:ns-1] = 0.5 * (np.log(s[2:ns]) - np.log(s[0:ns-2]))

        S, W       = np.meshgrid(s, w)
        ws         = S*W
        ws2        = ws**2

        kern       = np.vstack((ws2/(1+ws2), ws/(1+ws2)))
        wij        = np.dot(kern, np.diag(hs * np.exp(H)))  # 2n * ns
        K          = np.dot(kern, hs * np.exp(H)) # 2n * 1, comparable with Gexp

        for i in np.arange(n):
            wij[i,:] = wij[i,:]/K[i]

        for j in np.arange(ns):
            wt[j] = np.sum(wij[:,j])

        wt  = wt/np.trapz(wt, np.log(s))
        wt  = (1. - wb) * wt + (wb * np.mean(wt)) * np.ones(len(wt))

        return wt

    def GridDensity(self, x, px, N):

        """#
        #  PROGRAM: GridDensity(input)
        #
        #	Takes in a PDF or density function, and spits out a bunch of points in
        #       accordance with the PDF
        #
        #  Input:
        #       x  = vector of points. It need *not* be equispaced,
        #       px = vector of same size as x: probability distribution or
        #            density function. It need not be normalized but has to be positive.
        #  	    N  = Number of points >= 3. The end points of "x" are included
        #  	     necessarily,
        # 
        #  Output:
        #       z  = Points distributed according to the density
        #       hz = width of the "intervals" - useful to apportion domain to points
        #            if you are doing quadrature with the results, for example.
        #
        #  (c) Sachin Shanbhag, November 11, 2015
        #"""

        npts = 100;                              # can potentially change
        xi   = np.linspace(min(x),max(x),npts)   # reinterpolate on equi-spaced axis
        fint = interp1d(x,px,'cubic')	         # smoothen using cubic splines
        pint = fint(xi)        					 # interpolation
        ci   = cumtrapz(pint, xi, initial=0)                
        pint = pint/ci[npts-1]
        ci   = ci/ci[npts-1]                     # normalize ci

        alfa = 1./(N-1)                          # alfa/2 + (N-1)*alfa + alfa/2
        zij  = np.zeros(N+1)                     # quadrature interval end marker
        z    = np.zeros(N)                       # quadrature point

        z[0]    = min(x);  
        z[N-1]  = max(x); 

        #
        # ci(Z_j,j+1) = (j - 0.5) * alfa
        #
        beta       = np.arange(0.5, N-0.5) * alfa
        zij[0]     = z[0]
        zij[N]     = z[N-1]
        fint       = interp1d(ci, xi, 'cubic')
        zij[1:N]   = fint(beta)
        h          = np.diff(zij)

        #
        # Quadrature points are not the centroids, but rather the center of masses
        # of the quadrature intervals
        #

        beta     = np.arange(1, N-1) * alfa
        z[1:N-1] = fint(beta)

        return z, h

    def mergeModes_magic(self, g, tau, imode):
        """merge modes imode and imode+1 into a single mode
        return gp and taup corresponding to this new mode
        used only when magic = True"""

        iniGuess = [g[imode] + g[imode+1], 0.5*(tau[imode] + tau[imode+1])]
        res = minimize(costFcn_magic, iniGuess, args=(g, tau, imode))

        newtau        = np.delete(tau, imode+1)
        newtau[imode] = res.x[1]

        newg          = np.delete(g, imode+1)
        newg[imode]   = res.x[0]
            
        return newg, newtau
            
    def normKern_magic(self, w, gn, taun, g1, tau1, g2, tau2):
        """helper function: for costFcn and mergeModes
        used only when magic = True"""
        wt   = w*taun
        Gnp  = gn * (wt**2)/(1. + wt**2)
        Gnpp = gn *  wt/(1. + wt**2)

        wt   = w*tau1
        Gop  = g1 * (wt**2)/(1. + wt**2)
        Gopp = g1 *  wt/(1. + wt**2)
        
        wt    = w*tau2
        Gop  += g2 * (wt**2)/(1. + wt**2)
        Gopp += g2 *  wt/(1. + wt**2)
        
        return (Gnp/Gop - 1.)**2 + (Gnpp/Gopp - 1.)**2

    def costFcn_magic(self, par, g, tau, imode):
        """"helper function for mergeModes; establishes cost function to minimize
            used only when magic = True"""

        gn   = par[0]
        taun = par[1]

        g1   = g[imode]
        g2   = g[imode+1]
        tau1 = tau[imode]
        tau2 = tau[imode+1]

        wmin = min(1./tau1, 1./tau2)/10.
        wmax = max(1./tau1, 1./tau2)*10.

        return quad(self.normKern_magic, wmin, wmax, args=(gn, taun, g1, tau1, g2, tau2))[0]

    def FineTuneSolution(self, tau, w, Gexp, isPlateau):
        """Given a spacing of modes tau, tries to do NLLS to fine tune it further
        If it fails, then it returns the old tau back	   
        Uses helper function: res_wG which computes residuals
        """	   

        success   = False
        initError = np.linalg.norm(self.res_wG(tau, w, Gexp, isPlateau))

        try:
            res     = least_squares(self.res_wG, tau, bounds=(0.02/max(w), 50/min(w)),
                                args=(w, Gexp, isPlateau))		
            tau     = res.x		
            tau0    = tau.copy()
            success = True
        except:
            pass

        g, tau, _, _ = self.MaxwellModes(np.log(tau), w, Gexp, isPlateau)   # Get g_i, taui
        finalError   = np.linalg.norm(self.res_wG(tau, w, Gexp, isPlateau))

        # keep fine tuned solution, only if it improves things
        if finalError > initError:
            success = False

        return success, g, tau

    def res_wG(self, tau, wexp, Gexp, isPlateau):
        """
            Helper function for final optimization problem
        """
        g, _, _ = self.nnLLS(wexp, tau, Gexp, isPlateau)
        Gmodel  = np.zeros(len(Gexp))

            
        S, W    = np.meshgrid(tau, wexp)
        ws      = S*W
        ws2     = ws**2
        K       = np.vstack((ws2/(1+ws2), ws/(1+ws2)))   # 2n * nmodes

        # add G0
        if isPlateau:
            Gmodel 	= np.dot(K, g[:-1])
            n = int(len(Gexp)/2)
            Gmodel[:n] += g[-1]	
        else:
            Gmodel 	= np.dot(K, g)
                    
        residual = Gmodel/Gexp - 1.
            
        return residual


    def ShanBhagMaxwellModesFrequency(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        # CALCULATE THE CONTINUOUS SPECTRUM FIRST
        w = ft.data[:, 0]
        Gexp =  np.append(ft.data[:, 1], ft.data[:, 2])  # % Gp followed by Gpp (2n*1)

        n = ft.num_rows
        ns = self.parameters['ns'].value
        wmin = ft.data[0, 0]
        wmax = ft.data[n-1, 0]

    	# determine frequency window
        #if FreqEnd == 1:
        #    smin = np.exp(-np.pi/2)/wmax; smax = np.exp(np.pi/2)/wmin		
        #elif FreqEnd == 2:
        smin = 1./wmax; smax = 1./wmin				
        #elif FreqEnd == 3:
        #    smin = np.exp(+np.pi/2)/wmax; smax = np.exp(-np.pi/2)/wmin

        hs   = (smax/smin)**(1./(ns-1))
        s    = smin * hs**np.arange(ns)

        kernMat = self.getKernMat(s, w)

        tic  = time.time()
        plateau = self.parameters["plateau"].value
        if plateau:
            Hgs, G0  = self.InitializeH(Gexp, s, kernMat, np.min(Gexp))
        else:
            Hgs      = self.InitializeH(Gexp, s, kernMat)


        te   = time.time() - tic
        self.Qprint('Initial Set up...({0:.1f} s)'.format(te))
        tic  = time.time()

        # Find Optimum Lambda with 'lcurve'
        lamC = self.parameters['lamC'].value
        if lamC == 0:
            if plateau:
                lamC, lam, rho, eta, logP, Hlam = self.lcurve(Gexp, Hgs, kernMat, G0)
            else:
                lamC, lam, rho, eta, logP, Hlam = self.lcurve(Gexp, Hgs, kernMat)

        te = time.time() - tic
        self.Qprint('Building the L-curve...({0:.1f} s)'.format(te))
        tic = time.time()
        self.Qprint('lamC = {0:0.3e}'.format(lamC))

        # Get the best spectrum	
        if plateau:
            H, G0  = self.getH(lamC, Gexp, Hgs, kernMat, G0)
            self.Qprint('G0 = {0:0.3e} ...'.format(G0))
        else:
            H  = self.getH(lamC, Gexp, Hgs, kernMat)

        te = time.time() - tic
        self.Qprint('Extracting CRS...done ({0:.1f} s)'.format(te))

		# Save inferred H(s) and Gw
        if lamC != 0:
            if plateau:
                K   = self.kernel_prestore(H, kernMat, G0);	
                #np.savetxt('output/H.dat', np.c_[s, H], fmt='%e', header='G0 = {0:0.3e}'.format(G0))
            else:
                K   = self.kernel_prestore(H, kernMat)
                #np.savetxt('output/H.dat', np.c_[s, H], fmt='%e')
             
            #np.savetxt('output/Gfit.dat', np.c_[w, K[:n], K[n:]], fmt='%e')
            tt.data[:, 1] = K[:n]
            tt.data[:, 2] = K[n:]

        # Spectrum
        self.scont = s
        self.Hcont = H

        # GET DISCRETE SPECTRUM

        # range of N scanned
        Nmax  = min(np.floor(3.0 * np.log10(max(w)/min(w))),n/4); # maximum N
        Nmin  = max(np.floor(0.5 * np.log10(max(w)/min(w))),3);   # minimum N
        Nv    = np.arange(Nmin, Nmax + 1).astype(int)

        Cerror  = 1./(np.std(K/Gexp - 1.))  #	Cerror = 1.?
        npts = len(Nv)

        # range of wtBaseDist scanned
        deltaBaseWeightDist = self.parameters['deltaBaseWeightDist'].value
        wtBase = deltaBaseWeightDist * np.arange(1, int(1./deltaBaseWeightDist))
        AICbst = np.zeros(len(wtBase))
        Nbst   = np.zeros(len(wtBase))  # nominal number of modes
        nzNbst = np.zeros(len(wtBase))  # actual number of nonzero modes

        # main loop over wtBaseDist
        for ib, wb in enumerate(wtBase):
            
            # Find the distribution of nodes you need
            wt  = self.GetWeights(H, w, s, wb)

            # Scan the range of number of Maxwell modes N = (Nmin, Nmax) 
            ev    = np.zeros(npts)
            nzNv  = np.zeros(npts)  # number of nonzero modes 

            for i, N in enumerate(Nv):
                z, hz  = self.GridDensity(np.log(s), wt, N)         # select "tau" Points
                g, tau, ev[i], _ = self.MaxwellModes(z, w, Gexp, plateau)    # get g_i
                nzNv[i]                 = len(g)

            # store the best solution for this particular wb
            AIC        = 2. * Nv + 2. * Cerror * ev

            AICbst[ib] = min(AIC)
            Nbst[ib]   = Nv[np.argmin(AIC)]
            nzNbst[ib] = nzNv[np.argmin(AIC)]

        # global best settings of wb and Nopt; note this is nominal Nopt (!= len(g) due to NNLS)
        Nopt  = int(Nbst[np.argmin(AICbst)])
        wbopt = wtBase[np.argmin(AICbst)]

        #
        # Recompute the best data-set stats
        #
        wt                   = self.GetWeights(H, w, s, wbopt)
        z, hz                = self.GridDensity(np.log(s), wt, Nopt)             # Select "tau" Points
        g, tau, error, cKp   = self.MaxwellModes(z, w, Gexp, plateau)     # Get g_i, taui	
        succ, gf, tauf       = self.FineTuneSolution(tau, w, Gexp, plateau)
        if succ:
            g   = gf.copy(); tau = tauf.copy()
        
        #
        # Check if modes are close enough to merge
        #
        indx       = np.argsort(tau)
        tau        = tau[indx]
        tauSpacing = tau[1:]/tau[:-1]
        itry       = 0

        if plateau:
            g[:-1] = g[indx]
        else:
            g      = g[indx]

        minTauSpacing = self.parameters['minTauSpacing'].value
        while min(tauSpacing) < minTauSpacing and itry < 3:
            self.Qprint("Tau Spacing < minTauSpacing")
            
            imode      = np.argmin(tauSpacing)      # merge modes imode and imode + 1
            g, tau     = self.mergeModes_magic(g, tau, imode)

            succ, g, tau  = self.FineTuneSolution(tau, w, Gexp, plateau)		
            if succ:
                g   = gf.copy(); tau = tauf.copy()

                    
            tauSpacing = tau[1:]/tau[:-1]
            itry      += 1

        if plateau:
            G0 = g[-1]
            g  = g[:-1]

        self.Qprint('Number of optimum nodes = {0:d}'.format(len(g)))

        # Spectrum
        self.sdisc = tau
        self.Hdisc = g

        # TODO: DECIDE IF WE PLOT THE CONTINUOUS OR DISCRETE FIT TO G*(omega)


    def plot_theory_stuff(self):
        """[summary]
        
        [description]
        """
        if not self.view_modes:
             return

        # PLOT CONTINUOUS SPECTRUM
        view = self.parent_dataset.parent_application.current_view
        data_table_tmp = DataTable(self.axarr)
        data_table_tmp.num_columns = 3
        ns = self.parameters['ns'].value
        data_table_tmp.num_rows = ns
        data_table_tmp.data = np.zeros((ns, 3))
        data_table_tmp.data[:, 0] = np.reciprocal(self.scont)
        data_table_tmp.data[:, 1] = np.exp(self.Hcont)
        try:
            x, y, success = view.view_proc(data_table_tmp, None)
        except TypeError as e:
            print(e)
            return
        self.contspectrum.set_data(x, y)

        data_table_tmp.num_columns = 3
        nmodes = len(self.sdisc)
        data_table_tmp.num_rows = nmodes
        data_table_tmp.data = np.zeros((nmodes, 3))
        data_table_tmp.data[:, 0] = np.reciprocal(self.sdisc)
        data_table_tmp.data[:, 1] = self.Hdisc
        try:
            x, y, success = view.view_proc(data_table_tmp, None)
        except TypeError as e:
            print(e)
            return
        self.discspectrum.set_data(x, y)


class CLTheoryShanbhagMaxwellModesFrequency(BaseTheoryShanbhagMaxwellModesFrequency, Theory):
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


class GUITheoryShanbhagMaxwellModesFrequency(BaseTheoryShanbhagMaxwellModesFrequency, QTheory):
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
        #self.spinbox = QSpinBox()
        #self.spinbox.setRange(1, self.MAX_MODES)  # min and max number of modes
        #self.spinbox.setSuffix(" modes")
        #self.spinbox.setValue(self.parameters["nmodes"].value)  #initial value
        #tb.addWidget(self.spinbox)
        self.modesaction = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-visible.png'), 'View modes')
        self.save_modes_action = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-save-Maxwell.png'),
            "Save Modes")            
        self.modesaction.setCheckable(True)
        self.modesaction.setChecked(True)
        self.thToolsLayout.insertWidget(0, tb)

        #connection_id = self.spinbox.valueChanged.connect(
        #    self.handle_spinboxValueChanged)
        #connection_id = self.modesaction.triggered.connect(
        #    self.modesaction_change)
        #connection_id = self.save_modes_action.triggered.connect(
        #    self.save_modes)

    def Qhide_theory_extras(self, state):
        """Uncheck the modeaction button. Called when curent theory is changed
        
        [description]
        """
        self.modesaction.setChecked(state)

    def modesaction_change(self, checked):
        """[summary]
        
        [description]
        """
        self.graphicmodes_visible(checked)
        # self.view_modes = self.modesaction.isChecked()
        # self.graphicmodes.set_visible(self.view_modes)
        # self.do_calculate("")

    def handle_spinboxValueChanged(self, value):
        """[summary]
        
        [description]
        
        Arguments:
            - value {[type]} -- [description]
        """
        """Handle a change of the parameter 'nmodes'"""
        self.set_param_value('nmodes', value)
        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()
        self.update_parameter_table()


##################################################################################
#   MAXWELL MODES TIME
##################################################################################


class TheoryShanbhagMaxwellModesTime(CmdBase):
    """Fit a generalized Maxwell model to a time dependent relaxation function. 
    
    * **Function**
        .. math::
            \\begin{eqnarray}
            G(t) & = & \\sum_{i=1}^{n_{modes}} G_i \\exp (-t/\\tau_i)
            \\end{eqnarray}
    
    * **Parameters**
       - :math:`n_{modes}`: number of Maxwell modes equally distributed in logarithmic scale between :math:`\\omega_{min}` and :math:`\\omega_{max}`.
       - logtmin = :math:`\\log(t_{min})`: decimal logarithm of the minimum time.
       - logtmax = :math:`\\log(t_{max})`: decimal logarithm of the maximum time.
       - logGi = :math:`\\log(G_{i})`: decimal logarithm of the amplitude of Maxwell mode :math:`i`.
    
    """
    thname = "Maxwell Modes"
    description = "Maxwell modes, time dependent"
    citations = ""

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
        return GUITheoryShanbhagMaxwellModesTime(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryShanbhagMaxwellModesTime(
                name, parent_dataset, ax)


class BaseTheoryShanbhagMaxwellModesTime:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/Gt/Theory/theory.html#maxwell-modes'
    single_file = True
    thname = TheoryShanbhagMaxwellModesTime.thname
    citations = TheoryShanbhagMaxwellModesTime.citations

    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.MaxwellModesTime
        self.has_modes = True
        self.MAX_MODES = 40
        self.view_modes = True
        tmin = self.parent_dataset.minpositivecol(0)
        tmax = self.parent_dataset.maxcol(0)
        nmodes = int(np.round(np.log10(tmax / tmin)))

        self.parameters["logtmin"] = Parameter(
            "logtmin",
            np.log10(tmin),
            "Log of time range minimum",
            ParameterType.real,
            opt_type=OptType.opt)
        self.parameters["logtmax"] = Parameter(
            "logtmax",
            np.log10(tmax),
            "Log of time range maximum",
            ParameterType.real,
            opt_type=OptType.opt)
        self.parameters["nmodes"] = Parameter(
            name="nmodes",
            value=nmodes,
            description="Number of Maxwell modes",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False)
        # Interpolate modes from data
        tau = np.logspace(np.log10(tmin), np.log10(tmax), nmodes)
        G = np.abs(
            np.interp(tau, self.parent_dataset.files[0].data_table.data[:, 0],
                      self.parent_dataset.files[0].data_table.data[:, 1]))
        for i in range(self.parameters["nmodes"].value):
            self.parameters["logG%02d" % i] = Parameter(
                "logG%02d" % i,
                np.log10(G[i]),
                "Log of Mode %d amplitude" % i,
                ParameterType.real,
                opt_type=OptType.opt)

        # GRAPHIC MODES
        self.graphicmodes = None
        self.artistmodes = None
        self.setup_graphic_modes()

    def set_param_value(self, name, value):
        """Change other parameters when nmodes is changed, else call parent function"""
        if name == 'nmodes':
            nmodesold = self.parameters["nmodes"].value
            tminold = self.parameters["logtmin"].value
            tmaxold = self.parameters["logtmax"].value
            tauold = np.logspace(tminold, tmaxold, nmodesold)
            Gold = np.zeros(nmodesold)
            for i in range(nmodesold):
                Gold[i] = self.parameters["logG%02d" % i].value
                del self.parameters["logG%02d" % i]

            nmodesnew = value
            message, success = super().set_param_value("nmodes", nmodesnew)
            taunew = np.logspace(tminold, tmaxold, nmodesnew)

            Gnew = np.interp(taunew, tauold, Gold)

            for i in range(nmodesnew):
                self.parameters["logG%02d" % i] = Parameter(
                    "logG%02d" % i,
                    Gnew[i],
                    "Log of Mode %d amplitude" % i,
                    ParameterType.real,
                    opt_type=OptType.opt)
            if CmdBase.mode == CmdMode.GUI:
                self.spinbox.setValue(value)
        else:
            message, success = super().set_param_value(name, value)
        
        return message, success

    def drag_mode(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        nmodes = self.parameters["nmodes"].value
        self.set_param_value("logtmin", dx[0])
        self.set_param_value("logtmax", dx[nmodes - 1])
        for i in range(nmodes):
            self.set_param_value("logG%02d" % i, dy[i])
        self.do_calculate("")
        self.update_parameter_table()

    def update_modes(self):
        """[summary]
        
        [description]
        """
        pass

    def setup_graphic_modes(self):
        """[summary]
        
        [description]
        """
        nmodes = self.parameters["nmodes"].value
        tau = np.logspace(self.parameters["logtmin"].value,
                          self.parameters["logtmax"].value, nmodes)
        G = np.zeros(nmodes)
        for i in range(nmodes):
            G[i] = np.power(10, self.parameters["logG%02d" % i].value)

        self.graphicmodes = self.ax.plot(tau, G)[0]
        self.graphicmodes.set_marker('D')
        self.graphicmodes.set_linestyle('')
        self.graphicmodes.set_visible(self.view_modes)
        self.graphicmodes.set_markerfacecolor('yellow')
        self.graphicmodes.set_markeredgecolor('black')
        self.graphicmodes.set_markeredgewidth(3)
        self.graphicmodes.set_markersize(8)
        self.graphicmodes.set_alpha(0.5)
        self.artistmodes = DraggableModesSeries(
            self.graphicmodes, DragType.special,
            self.parent_dataset.parent_application, self.drag_mode)
        self.plot_theory_stuff()

    def destructor(self):
        """Called when the theory tab is closed
        
        [description]
        """
        self.graphicmodes_visible(False)
        self.ax.lines.remove(self.graphicmodes)

    def show_theory_extras(self, show=False):
        """Called when the active theory is changed
        
        [description]
        """
        if CmdBase.mode == CmdMode.GUI:
            self.Qhide_theory_extras(show)
        self.graphicmodes_visible(show)

    def graphicmodes_visible(self, state):
        """[summary]
        
        [description]
        """
        self.view_modes = state
        self.contspectrum.set_visible(self.view_modes)
        # if self.view_modes:
        #     self.artistmodes.connect()
        # else:
        #     self.artistmodes.disconnect()
        # self.do_calculate("")
        self.parent_dataset.parent_application.update_plot()

    def get_modes(self):
        """[summary]
        
        [description]
        
        Returns:
            - [type] -- [description]
        """
        nmodes = self.parameters["nmodes"].value
        tau = np.logspace(self.parameters["logtmin"].value,
                          self.parameters["logtmax"].value, nmodes)
        G = np.zeros(nmodes)
        for i in range(nmodes):
            G[i] = np.power(10, self.parameters["logG%02d" % i].value)
        return tau, G

    def set_modes(self, tau, G):
        """[summary]
        
        [description]
        
        Arguments:
            - tau {[type]} -- [description]
            - G {[type]} -- [description]
        """
        print("set_modes not allowed in this theory (%s)" % self.name)

    def MaxwellModesTime(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        try:
            gamma = float(f.file_parameters["gamma"])
            if (gamma==0):
                gamma=1
        except:
            gamma = 1

        nmodes = self.parameters["nmodes"].value
        tau = np.logspace(self.parameters["logtmin"].value,
                          self.parameters["logtmax"].value, nmodes)

        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            expT_tau = np.exp(-tt.data[:, 0] / tau[i])
            G = np.power(10, self.parameters["logG%02d" % i].value)
            tt.data[:, 1] += G * expT_tau * gamma

    def plot_theory_stuff(self):
        """[summary]
        
        [description]
        """
        if not self.view_modes:
            return
        data_table_tmp = DataTable(self.axarr)
        data_table_tmp.num_columns = 2
        nmodes = self.parameters["nmodes"].value
        data_table_tmp.num_rows = nmodes
        data_table_tmp.data = np.zeros((nmodes, 2))
        tau = np.logspace(self.parameters["logtmin"].value,
                          self.parameters["logtmax"].value, nmodes)
        data_table_tmp.data[:, 0] = tau
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            data_table_tmp.data[i, 1] = np.power(
                10, self.parameters["logG%02d" % i].value)
        view = self.parent_dataset.parent_application.current_view
        try:
            x, y, success = view.view_proc(data_table_tmp, None)
        except TypeError as e:
            print(e)
            return
        self.graphicmodes.set_data(x, y)
        for i in range(data_table_tmp.MAX_NUM_SERIES):
            for nx in range(len(self.axarr)):
                self.axarr[nx].lines.remove(data_table_tmp.series[nx][i])


class CLTheoryShanbhagMaxwellModesTime(BaseTheoryShanbhagMaxwellModesTime, Theory):
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


class GUITheoryShanbhagMaxwellModesTime(BaseTheoryShanbhagMaxwellModesTime, QTheory):
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
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, self.MAX_MODES)  # min and max number of modes
        self.spinbox.setSuffix(" modes")
        self.spinbox.setValue(self.parameters["nmodes"].value)  #initial value
        tb.addWidget(self.spinbox)
        self.modesaction = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-visible.png'), 'View modes')
        self.save_modes_action = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-save-Maxwell.png'),
            "Save Modes")            
        self.modesaction.setCheckable(True)
        self.modesaction.setChecked(True)
        self.thToolsLayout.insertWidget(0, tb)

        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged)
        connection_id = self.modesaction.triggered.connect(
            self.modesaction_change)
        connection_id = self.save_modes_action.triggered.connect(
            self.save_modes)

    def Qhide_theory_extras(self, state):
        """Uncheck the modeaction button. Called when curent theory is changed
        
        [description]
        """
        self.modesaction.setChecked(state)

    def modesaction_change(self, checked):
        """[summary]
        
        [description]
        """
        self.graphicmodes_visible(checked)
        # self.view_modes = self.modesaction.isChecked()
        # self.graphicmodes.set_visible(self.view_modes)
        # if self.view_modes:
        #     self.artistmodes.connect()
        # else:
        #     self.artistmodes.disconnect()
        # self.do_calculate("")

    def handle_spinboxValueChanged(self, value):
        """Handle a change of the parameter 'nmodes'
        
        Arguments:
            - value {[type]} -- [description]
        """
        self.set_param_value('nmodes', value)
        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()
        self.update_parameter_table()
