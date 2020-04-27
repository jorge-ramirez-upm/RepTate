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
import sys
import numpy as np
from CmdBase import CmdBase, CmdMode
from DataTable import DataTable
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from PyQt5.QtWidgets import QWidget, QToolBar, QToolButton, QMenu, QComboBox, QSpinBox, QAction, QStyle, QMessageBox, QFileDialog
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from DraggableArtists import DragType, DraggableModesSeries
from scipy.optimize import nnls, minimize, least_squares
from scipy.interpolate import interp1d
from scipy.integrate import cumtrapz, quad
from enum import Enum
import Version
import time

class PredictionMode(Enum):
    """Define which prediction we want to see
    
    Parameters can be:
        - cont: Prediction from Continuous spectrum
        - disc: Prediction from Discrete spectrum
    """
    cont = 0
    disc = 1


class TheoryShanbhagMaxwellModesFrequency(CmdBase):
    """Extract continuous and discrete relaxation spectra from complex modulus G*(w)
        
    * **Parameters**
       - plateau : is there a residual plateau in the data (default False).
       - ns : Number of grid points to represent the continuous spectrum (typical 50-100)
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
    thname = "ReSpect"
    description = "Relaxation spectra from dynamic moduli"
    citations = ["Takeh, A. and Shanbhag, S., Appl. Rheol. 2013, 23, 24628"]
    doi = ['http://dx.doi.org/10.3933/ApplRheol-23-24628']
    
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
        self.view_modes = True
        wmin = self.parent_dataset.minpositivecol(0)
        wmax = self.parent_dataset.maxcol(0)
        nmodes = int(np.round(np.log10(wmax / wmin)))

        self.parameters["plateau"] = Parameter(
            "plateau",
            False,
            "is there a residual plateau?",
            ParameterType.boolean,
            opt_type=OptType.const,
            display_flag=False)
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
        self.parameters["FreqEnd"] = Parameter(
            name="FreqEnd",
            value=1,
            description="Treatment of Frequency Window ends (1, 2 or 3)",
            type=ParameterType.discrete_integer,
            opt_type=OptType.const,
            discrete_values=[1,2,3])
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

        self.prediction_mode = PredictionMode.cont 

        self.GstM = None
        self.K = None
        self.n = 0

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
        """Called when the theory tab is closed"""
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
        self.parent_dataset.parent_application.update_plot()

    def get_modes(self):
        """Get the values of Maxwell Modes from this theory"""
        nmodes = len(self.sdisc)
        tau = self.sdisc
        G = self.Hdisc
        return tau, G, True

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
            
            self.Qprint(".", end='')
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
        res = minimize(self.costFcn_magic, iniGuess, args=(g, tau, imode))

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

        # CALCULATE THE CONTINUOUS SPECTRUM FIRST
        self.Qprint("<b>CONTINUOUS SPECTRUM</b>")
        w = ft.data[:, 0]
        Gp = ft.data[:, 1]
        Gpp = ft.data[:, 2]

        # Remove points with w<=0
        filt=w>0
        w=w[filt]
        Gp=Gp[filt]
        Gpp=Gpp[filt]

        # Sanitize the input: remove repeated values and space data homogeneously. Using linear interpolation
        w, indices = np.unique(w, return_index = True)	
        Gp         = Gp[indices]
        Gpp        = Gpp[indices]
        fp  =  interp1d(w, Gp, fill_value="extrapolate")
        fpp =  interp1d(w, Gpp, fill_value="extrapolate")
        w  =  np.logspace(np.log10(np.min(w)), np.log10(np.max(w)), max(len(w),200))
        Gp =  fp(w)
        Gpp = fpp(w)
        Gexp = np.append(Gp, Gpp)

        n = len(w)
        self.n = n
        self.wfit = np.copy(w)
        tt.num_rows = len(w)
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = w

        ns = self.parameters['ns'].value
        wmin = w[0]
        wmax = w[n-1]

    	# determine frequency window
        if self.parameters['FreqEnd'].value == 1:
            smin = np.exp(-np.pi/2)/wmax; smax = np.exp(np.pi/2)/wmin		
        elif self.parameters['FreqEnd'].value == 2:
            smin = 1./wmax; smax = 1./wmin				
        elif self.parameters['FreqEnd'].value == 3:
            smin = np.exp(+np.pi/2)/wmax; smax = np.exp(-np.pi/2)/wmin

        hs   = (smax/smin)**(1./(ns-1))
        s    = smin * hs**np.arange(ns)

        kernMat = self.getKernMat(s, w)

        self.Qprint('Initial Set up...',end='')
        tic  = time.time()
        plateau = self.parameters["plateau"].value
        if plateau:
            Hgs, G0  = self.InitializeH(Gexp, s, kernMat, np.min(Gexp))
        else:
            Hgs      = self.InitializeH(Gexp, s, kernMat)


        te   = time.time() - tic
        self.Qprint('({0:.1f} s)'.format(te))
        tic  = time.time()

        # Find Optimum Lambda with 'lcurve'
        self.Qprint('Building the L-curve ...',end='')
        if self.parameters['lamC'].value == 0:
            if plateau:
                lamC, lam, rho, eta, logP, Hlam = self.lcurve(Gexp, Hgs, kernMat, G0)
            else:
                lamC, lam, rho, eta, logP, Hlam = self.lcurve(Gexp, Hgs, kernMat)
        else:
            lamC = self.parameters['lamC'].value

        te = time.time() - tic
        self.Qprint('({0:.1f} s)'.format(te))
        tic = time.time()
        self.Qprint('lamC = {0:0.3e}'.format(lamC))

        # Get the best spectrum	
        self.Qprint('Extracting CRS...',end='')
        if plateau:
            H, G0  = self.getH(lamC, Gexp, Hgs, kernMat, G0)
            self.Qprint('G0 = {0:0.3e} ...'.format(G0))
        else:
            H  = self.getH(lamC, Gexp, Hgs, kernMat)

        te = time.time() - tic
        self.Qprint('done ({0:.1f} s)'.format(te))

		# Save inferred H(s) and Gw
        if self.parameters['lamC'].value != 0:
            if plateau:
                self.K   = self.kernel_prestore(H, kernMat, G0);	
                #np.savetxt('output/H.dat', np.c_[s, H], fmt='%e', header='G0 = {0:0.3e}'.format(G0))
            else:
                self.K   = self.kernel_prestore(H, kernMat)
                #np.savetxt('output/H.dat', np.c_[s, H], fmt='%e')
             
        else:
            plam = np.exp(logP); plam = plam/np.sum(plam)			
            Hm   = np.zeros(len(s))
            Hm2  = np.zeros(len(s))
            cnt  = 0
            for i in range(len(lam)):	
                #~ Hm   += plam[i]*Hlam[:,i]
                #~ Hm2  += plam[i]*Hlam[:,i]**2
                # count all spectra within a threshold
                if plam[i] > 0.1:
                    Hm   += Hlam[:,i]
                    Hm2  += Hlam[:,i]**2
                    cnt  += 1

            Hm = Hm/cnt
            dH = np.sqrt(Hm2/cnt - Hm**2)

            if plateau:
                self.K   = self.kernel_prestore(Hm, kernMat, G0);	
            else:
                self.K   = self.kernel_prestore(Hm, kernMat);	

        #np.savetxt('output/Gfit.dat', np.c_[w, K[:n], K[n:]], fmt='%e')
        if self.prediction_mode == PredictionMode.cont:
            tt.data[:, 1] = self.K[:n]
            tt.data[:, 2] = self.K[n:]

        # Spectrum
        self.scont = s
        self.Hcont = H

        # GET DISCRETE SPECTRUM
        self.Qprint("<b>DISCRETE SPECTRUM</b>")

        # range of N scanned
        MaxNumModes=self.parameters['MaxNumModes'].value
        if(MaxNumModes == 0):
            Nmax  = min(np.floor(3.0 * np.log10(max(w)/min(w))),n/4); # maximum N
            Nmin  = max(np.floor(0.5 * np.log10(max(w)/min(w))),3);   # minimum N
            Nv    = np.arange(Nmin, Nmax + 1).astype(int)
        else:
            Nv    = np.arange(MaxNumModes, MaxNumModes + 1).astype(int)

        Cerror  = 1./(np.std(self.K/Gexp - 1.))  #	Cerror = 1.?
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
        g, tau, error, cKp = self.MaxwellModes(z, w, Gexp, plateau)   # Get g_i, taui
        succ, gf, tauf = self.FineTuneSolution(tau, w, Gexp, plateau)
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

            succ, g, tau = self.FineTuneSolution(tau, w, Gexp, plateau)
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

        S, W    = np.meshgrid(tau, w)
        ws		= S*W
        ws2     = ws**2
        K = np.vstack((ws2/(1+ws2), ws/(1+ws2)))
        self.GstM   	= np.dot(K, g)

        if plateau:
            self.GstM[:n] += G0

        # TODO: DECIDE IF WE PLOT THE CONTINUOUS OR DISCRETE FIT TO G*(omega)
        if self.prediction_mode == PredictionMode.disc:
            tt.data[:, 1] = self.GstM[:n]
            tt.data[:, 2] = self.GstM[n:]
            self.Qprint('<b>Fit from discrete spectrum</b>')
        else:
            self.Qprint('<b>Fit from continuous spectrum</b>')

    def do_fit(self, line=''):
        self.Qprint("Fitting not allowed in this theory")

    def do_error(self, line):
        total_error = 0
        npoints = 0
        view = self.parent_dataset.parent_application.current_view
        tools = self.parent_dataset.parent_application.tools       
        # table='''<table border="1" width="100%">'''
        # table+='''<tr><th>File</th><th>Error (RSS)</th><th># Pts</th></tr>'''
        tab_data = [['%-18s' % 'File', '%-18s' % 'Error (RSS)', '%-18s' % '# Pts'],]
        for f in self.theory_files():
            if self.stop_theory_flag:
                break
            xexp, yexp, success = view.view_proc(f.data_table,
                                                 f.file_parameters)
            tmp_dt = self.get_non_extended_th_table(f)
            xth, yth, success = view.view_proc(tmp_dt,
                                               f.file_parameters)

            yth2=np.copy(yexp)
            for i in range(xexp.shape[1]):
                fint = interp1d(xth[:,i],yth[:,i],'linear') # Get the theory at the same points as the data
                yth2[:,i] = np.copy(fint(xexp[:,i]))
            xth = np.copy(xexp)
            yth = np.copy(yth2)

            if (self.xrange.get_visible()):
                conditionx = (xexp > self.xmin) * (xexp < self.xmax)
            else:
                conditionx = np.ones_like(xexp, dtype=np.bool)
            if (self.yrange.get_visible()):
                conditiony = (yexp > self.ymin) * (yexp < self.ymax)
            else:
                conditiony = np.ones_like(yexp, dtype=np.bool)
            conditionnaninf = (~np.isnan(xexp)) * (~np.isnan(yexp)) * (
                ~np.isnan(xth)) * (~np.isnan(yth)) * (~np.isinf(xexp)) * (
                    ~np.isinf(yexp)) * (~np.isinf(xth)) * (~np.isinf(yth))
            yexp = np.extract(conditionx * conditiony * conditionnaninf, yexp)
            yth = np.extract(conditionx * conditiony * conditionnaninf, yth)
            f_error = np.mean((yth - yexp)**2)
            npt = len(yth)
            total_error += f_error * npt
            npoints += npt
            # table+= '''<tr><td>%-18s</td><td>%-18.4g</td><td>%-18d</td></tr>'''% (f.file_name_short, f_error, npt)
            tab_data.append(['%-18s'% f.file_name_short, '%-18.4g' % f_error, '%-18d' %npt])
        # table+='''</table><br>'''
        # self.Qprint(table)
        self.Qprint(tab_data)

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
        data_table_tmp.data[:, 2] = np.exp(self.Hcont)
        try:
            x, y, success = view.view_proc(data_table_tmp, None)
        except TypeError as e:
            print(e)
            return
        self.contspectrum.set_data(x[:,0], y[:,0])

        data_table_tmp.num_columns = 3
        nmodes = len(self.sdisc)
        data_table_tmp.num_rows = nmodes
        data_table_tmp.data = np.zeros((nmodes, 3))
        data_table_tmp.data[:, 0] = np.reciprocal(self.sdisc)
        data_table_tmp.data[:, 1] = self.Hdisc
        data_table_tmp.data[:, 2] = self.Hdisc
        try:
            x, y, success = view.view_proc(data_table_tmp, None)
        except TypeError as e:
            print(e)
            return
        self.discspectrum.set_data(x[:,0], y[:,0])


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

        self.tbutpredmode = QToolButton()
        self.tbutpredmode.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        self.cont_pred_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-minimum-value.png'),
            "Fit from Spectrum")
        self.disc_pred_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-scatter-plot.png'),
            "Fit from Discrete")
        if self.prediction_mode == PredictionMode.cont:
            self.tbutpredmode.setDefaultAction(self.cont_pred_action)
        else:
            self.tbutpredmode.setDefaultAction(self.disc_pred_action)
        self.tbutpredmode.setMenu(menu)
        tb.addWidget(self.tbutpredmode)

        self.modesaction = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-visible.png'), 'View modes/spectrum')
        self.plateauaction = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-flat-tire-80.png'), 'is there a residual plateau?')
        self.save_modes_action = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-save-Maxwell.png'),
            "Save Modes")            
        self.save_spectrum_action = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-save_Ht.png'),
            "Save Spectrum")                      
        self.modesaction.setCheckable(True)
        self.modesaction.setChecked(True)
        self.plateauaction.setCheckable(True)
        self.plateauaction.setChecked(False)
        self.thToolsLayout.insertWidget(0, tb)

        connection_id = self.modesaction.triggered.connect(
            self.modesaction_change)
        connection_id = self.plateauaction.triggered.connect(
            self.plateauaction_change)
        connection_id = self.save_modes_action.triggered.connect(
            self.save_modes)
        connection_id = self.save_spectrum_action.triggered.connect(
            self.save_spectrum)
        connection_id = self.cont_pred_action.triggered.connect(
            self.select_cont_pred)
        connection_id = self.disc_pred_action.triggered.connect(
            self.select_disc_pred)

    def select_cont_pred(self):
        self.prediction_mode = PredictionMode.cont
        self.tbutpredmode.setDefaultAction(self.cont_pred_action)

        if self.n > 0:
            th_files = self.theory_files()
            for f in self.parent_dataset.files:
                if f in th_files:
                    tt = self.tables[f.file_name_short]
                    tt.data[:, 1] = self.K[:self.n]
                    tt.data[:, 2] = self.K[self.n:]

            self.Qprint('<b>Fit from continuous spectrum</b>')
            self.do_error('')
            self.do_plot('')

    def select_disc_pred(self):
        self.prediction_mode = PredictionMode.disc
        self.tbutpredmode.setDefaultAction(self.disc_pred_action)

        if self.n > 0:
            th_files = self.theory_files()
            for f in self.parent_dataset.files:
                if f in th_files:
                    tt = self.tables[f.file_name_short]
                    tt.data[:, 1] = self.GstM[:self.n]
                    tt.data[:, 2] = self.GstM[self.n:]

            self.Qprint('<b>Fit from discrete spectrum</b>')
            self.do_error('')
            self.do_plot('')


    def save_spectrum(self):
        """Save Spectrum to a text file"""
        fpath, _ = QFileDialog.getSaveFileName(self,
                                               "Save spectrum to a text file",
                                               "data/", "Text (*.txt)")
        if fpath == '':
            return
            
        with open(fpath, 'w') as f:

            header = '# Continuous spectrum\n'
            header += '# Generated with RepTate v%s %s\n' % (Version.VERSION,
                                                             Version.DATE)
            header += '# At %s on %s\n' % (time.strftime("%X"),
                                           time.strftime("%a %b %d, %Y"))
            f.write(header)

            f.write('\n#%15s\t%15s\n'%('tau_i','G_i'))

            n = len(self.scont)
            for i in range(n):
                f.write('%15g\t%15g\n'%(self.scont[i],np.exp(self.Hcont[i])))
            
            f.write('\n#end')

        QMessageBox.information(self, 'Success',
                                'Wrote spectrum \"%s\"' % fpath)


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

    def plateauaction_change(self, checked):
        self.set_param_value("plateau", checked)

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
    """Extract continuous and discrete relaxation spectra from relaxation modulus G(t)
        
    * **Parameters**
       - plateau : is there a residual plateau in the data (default False).
       - ns : Number of grid points to represent the continuous spectrum (typical 50-100)
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
    thname = "ReSpect"
    description = "Relaxation spectra from relaxation modulus"
    citations = ["Shanbhag, S., Macromolecular Theory and Simulations, 2019, 1900005"]
    doi = ['http://dx.doi.org/10.1002/mats.201900005']

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
    help_file = 'http://reptate.readthedocs.io/manual/Applications/Gt/Theory/theory.html#shanbhag-maxwell-modes'
    single_file = True
    thname = TheoryShanbhagMaxwellModesTime.thname
    citations = TheoryShanbhagMaxwellModesTime.citations
    doi = TheoryShanbhagMaxwellModesTime.doi

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
        self.view_modes = True

        self.parameters["plateau"] = Parameter(
            "plateau",
            False,
            "is there a residual plateau?",
            ParameterType.boolean,
            opt_type=OptType.const,
            display_flag=False)
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
        self.parameters["FreqEnd"] = Parameter(
            name="FreqEnd",
            value=1,
            description="Treatment of Frequency Window ends (1, 2 or 3)",
            type=ParameterType.discrete_integer,
            opt_type=OptType.const,
            discrete_values=[1,2,3])
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
            2,
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

        self.prediction_mode = PredictionMode.cont 

        self.GtM = None
        self.K = None
        self.tfit = None

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
        """Called when the theory tab is closed"""
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
        self.parent_dataset.parent_application.update_plot()

    def get_modes(self):
        """Get the values of Maxwell Modes from this theory"""
        nmodes = len(self.sdisc)
        tau = self.sdisc
        G = self.Hdisc
        return tau, G, True

    def getKernMat(self, s, t):
        """furnish kerMat() which helps faster kernel evaluation
        given s, t generates hs * exp(-T/S) [n * ns matrix], where hs = wi = weights
        for trapezoidal rule integration.
        
        This matrix (K) times h = exp(H), Kh, is comparable with Gexp"""	   
        ns          = len(s)
        hsv         = np.zeros(ns);
        hsv[0]      = 0.5 * np.log(s[1]/s[0])
        hsv[ns-1]   = 0.5 * np.log(s[ns-1]/s[ns-2])
        hsv[1:ns-1] = 0.5 * (np.log(s[2:ns]) - np.log(s[0:ns-2]))
        S, T        = np.meshgrid(s, t);
        
        return np.exp(-T/S) * hsv;
        
    def kernel_prestore(self, H, kernMat, *argv):
        """
            turbocharging kernel function evaluation by prestoring kernel matrix
            Function: kernel_prestore(input) returns K*h, where h = exp(H)
            
            Same as kernel, except prestoring hs, S, and T to improve speed 3x.
            
            outputs the n*1 dimensional vector K(H)(t) which is comparable to Gexp = Gt
            
            3/11/2019: returning Kh + G0
            
            Input: H = substituted CRS,
                    kernMat = n*ns matrix [w * exp(-T/S)]
                        
        """
        
        if len(argv) > 0:
            G0 = argv[0]
        else:
            G0 = 0. 
        
        return np.dot(kernMat, np.exp(H)) + G0

    def InitializeH(self, Gexp, s, kernMat, *argv):
        """
        Function: InitializeH(input)
        
        Input:  Gexp       = n*1 vector [Gt],
                s       = relaxation modes,
                kernMat = matrix for faster kernel evaluation
                G0      = optional; if plateau is nonzero
                
        Output:   H = guessed H
                G0 = optional guess if *argv is nonempty
        """
        #
        # To guess spectrum, pick a negative Hgs and a large value of lambda to get a
        # solution that is most determined by the regularization
        # March 2019; a single guess is good enough now, because going from large lambda to small
        #             lambda in lcurve.

        H    = -5.0 * np.ones(len(s)) + np.sin(np.pi * s)
        lam  = 1e0
        
        if len(argv) > 0:
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
        n   = kernMat.shape[0];
        ns  = kernMat.shape[1];
        nl  = ns - 2;
        r   = np.zeros(n);   	  # vector of size (n);

        # furnish relevant portion of Jacobian and residual

        Kmatrix = np.dot((1./Gexp).reshape(n,1), np.ones((1,ns)));
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
        er    = rho/np.amin(rho) + eta/(np.sqrt(np.amax(eta)*np.amin(eta)));

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
        rhoF  = interp1d(lam, rho)

        rho_cutoff = self.parameters['rho_cutoff'].value
        if  rhoF(lamC) <= rho_cutoff:
            try:
                eridx = (np.abs(rhoF(lami) - rho_cutoff)).argmin()
                if lami[eridx] > lamC:
                    lamC = lami[eridx]				
            except:
                pass

        return lamC


    def lcurve(self, Gexp, Hgs, kernMat, *argv):

        """ 
        Function: lcurve(input)
        
        Input: Gexp    = n*1 vector [Gt],
                Hgs     = guessed H,
                kernMat = matrix for faster kernel evaluation
                par     = parameter dictionary
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
            
            self.Qprint(".", end='')
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
            lamM = np.exp(np.log(lamM) + SmFacLam*(max(np.log(lam)) - np.log(lamM)));
        elif SmFacLam < 0:
            lamM = np.exp(np.log(lamM) + SmFacLam*(np.log(lamM) - min(np.log(lam))));

        return lamM, lam, rho, eta, logP, Hlambda


    def getH(self, lam, Gexp, H, kernMat, *argv):

        """Purpose: Given a lambda, this function finds the H_lambda(s) that minimizes V(lambda)
        
                V(lambda) := ||Gexp - kernel(H)||^2 +  lambda * ||L H||^2
        
        Input  : lambda  = regularization parameter ,
                Gexp    = experimental data,
                H       = guessed H,
                kernMat = matrix for faster kernel evaluation
                G0      = optional
        
        Output : H_lam, [G0]
                Default uses Trust-Region Method with Jacobian supplied by jacobianLM
        """

        # send Hplus = [H, G0], on return unpack H and G0
        if len(argv) > 0:
            Hplus= np.append(H, argv[0])
            res_lsq = least_squares(self.residualLM, Hplus, jac=self.jacobianLM, args=(lam, Gexp, kernMat))
            return res_lsq.x[:-1], res_lsq.x[-1]
            
        # send normal H, and collect optimized H back
        else:
            res_lsq = least_squares(self.residualLM, H, jac=self.jacobianLM, args=(lam, Gexp, kernMat))			
            return res_lsq.x


    def residualLM(self, H, lam, Gexp, kernMat):
        """
        %
        % HELPER FUNCTION: Gets Residuals r
        Input  : H       = guessed H,
                lambda  = regularization parameter ,
                Gexp    = experimental data,
                kernMat = matrix for faster kernel evaluation
                G0      = plateau
        
        Output : a set of n+nl residuals,
                the first n correspond to the kernel
                the last  nl correspond to the smoothness criterion
        %"""


        n   = kernMat.shape[0];
        ns  = kernMat.shape[1];
        nl  = ns - 2;

        r   = np.zeros(n + nl);
        
        # if plateau then unfurl G0
        if len(H) > ns:
            G0     = H[-1]
            H      = H[:-1]
            r[0:n] = (1. - self.kernel_prestore(H, kernMat, G0)/Gexp)  # the Gt and
        else:
            r[0:n] = (1. - self.kernel_prestore(H, kernMat)/Gexp)  # the Gt and
        
        # the curvature constraint is not affected by G0
        r[n:n+nl] = np.sqrt(lam) * np.diff(H, n=2)  # second derivative

            
        return r
            
    def jacobianLM(self, H, lam, Gexp, kernMat):
        """
        HELPER FUNCTION for optimization: Get Jacobian J
        
        returns a (n+nl * ns) matrix Jr; (ns + 1) if G0 is also supplied.
        
        Jr_(i, j) = dr_i/dH_j
        
        It uses kernelD, which approximates dK_i/dH_j, where K is the kernel
        
        """
        n   = kernMat.shape[0];
        ns  = kernMat.shape[1];
        nl  = ns - 2;

        # L is a ns*ns tridiagonal matrix with 1 -2 and 1 on its diagonal;
        L  = np.diag(np.ones(ns-1), 1) + np.diag(np.ones(ns-1),-1) + np.diag(-2. * np.ones(ns))
        L  = L[1:nl+1,:]	
        
        # Furnish the Jacobian Jr (n+ns)*ns matrix
        Kmatrix         = np.dot((1./Gexp).reshape(n,1), np.ones((1,ns)));

        if len(H) > ns:

            G0     = H[-1]
            H      = H[:-1]
            
            Jr  = np.zeros((n + nl, ns+1))

            Jr[0:n, 0:ns]   = -self.kernelD(H, kernMat) * Kmatrix;
            Jr[0:n, ns]     = -1./Gexp							# column for dr_i/dG0

            Jr[n:n+nl,0:ns] = np.sqrt(lam) * L;
            Jr[n:n+nl, ns]  = np.zeros(nl)						# column for dr_i/dG0 = 0
            
        else:

            Jr  = np.zeros((n + nl, ns))

            Jr[0:n, 0:ns]   = -self.kernelD(H, kernMat) * Kmatrix;
            Jr[n:n+nl,0:ns] = np.sqrt(lam) * L;        
            
        return	Jr

    def kernelD(self, H, kernMat):
        """
        Function: kernelD(input)
        
        outputs the (n*ns) dimensional matrix DK(H)(t)
        It approximates dK_i/dH_j = K * e(H_j):
        
        Input: H       = substituted CRS,
                kernMat = matrix for faster kernel evaluation
        
        Output: DK = Jacobian of H
        """
        
        n   = kernMat.shape[0];
        ns  = kernMat.shape[1];


        # A n*ns matrix with all the rows = H'
        Hsuper  = np.dot(np.ones((n,1)), np.exp(H).reshape(1, ns))  
        DK      = kernMat  * Hsuper
            
        return DK


    def MaxwellModes(self, z, t, Gt, isPlateau):
        """
        
        Function: MaxwellModes(input)
        
        Solves the linear least squares problem to obtain the DRS

        Input: z  = points distributed according to the density, [z = log(tau)]
                t  = n*1 vector contains times,
                Gt = n*1 vector contains G(t),
                isPlateau = True if G0 \neq 0
        
        Output: g, tau = spectrum  (array)
                error = relative error between the input data and the G(t) inferred from the DRS
                condKp = condition number
        """
        N      = len(z)
        tau    = np.exp(z)
        n      = len(t)
        Gexp   = Gt

        #
        # Prune small and -ve weights g(i)
        #
        g, error, condKp = self.nnLLS(t, tau, Gexp, isPlateau)


        # search for small 
        if isPlateau:
            izero = np.where(g[:-1]/max(g[:-1]) < 1e-7)
        else:
            izero = np.where(g/max(g) < 1e-7)
        
        tau   = np.delete(tau, izero)
        g     = np.delete(g, izero)

        return g, tau, error, condKp

    def nnLLS(self, t, tau, Gexp, isPlateau):
        """
        #
        # Helper subfunction which does the actual LLS problem
        # helps MaxwellModes; relies on nnls
        #
        """
        n       = len(Gexp)
        S, T    = np.meshgrid(tau, t)
        K		= np.exp(-T/S)		# n * nmodes
        
        # K is n*ns [or ns+1]
        if isPlateau:
            K = np.hstack(( K, np.ones((len(Gexp), 1)) ))
            
        #
        # gets (Gt/GtE - 1)^2, instead of  (Gt -  GtE)^2
        #
        Kp      = np.dot(np.diag((1./Gexp)), K)
        condKp  = np.linalg.cond(Kp)
        g       = nnls(Kp, np.ones(len(Gexp)))[0]	

        GtM   	= np.dot(K, g)
        error 	= np.sum((GtM/Gexp - 1.)**2)

        return g, error, condKp

    def GetWeights(self, H, t, s, wb):
        """
        %
        % Function: GetWeights(input)
        %
        % Finds the weight of "each" mode by taking a weighted average of its contribution
        % to G(t)
        %
        % Input: H = CRS (ns * 1)
        %        t = n*1 vector contains times
        %        s = relaxation modes (ns * 1)
        %       wb = weightBaseDist
        %
        % Output: wt = weight of each mode
        %
        """
    
        ns         = len(s)
        n          = len(t)

        hs         = np.zeros(ns)
        wt         = hs
        
        hs[0]      = 0.5 * np.log(s[1]/s[0])
        hs[ns-1]   = 0.5 * np.log(s[ns-1]/s[ns-2])
        hs[1:ns-1] = 0.5 * (np.log(s[2:ns]) - np.log(s[0:ns-2]))

        S, T    = np.meshgrid(s, t)
        kern    = np.exp(-T/S)		# n * ns
        wij     =  np.dot(kern, np.diag(hs * np.exp(H)))  # n * ns
        K       = np.dot(kern, hs * np.exp(H))         # n * 1, comparable with Gexp

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

        # ci(Z_j,j+1) = (j - 0.5) * alfa
        beta       = np.arange(0.5, N-0.5) * alfa
        zij[0]     = z[0]
        zij[N]     = z[N-1]
        fint       = interp1d(ci, xi, 'cubic')
        zij[1:N]   = fint(beta)
        h          = np.diff(zij)

        # Quadrature points are not the centroids, but rather the center of masses
        # of the quadrature intervals
        beta     = np.arange(1, N-1) * alfa
        z[1:N-1] = fint(beta)

        return z, h

    def mergeModes_magic(self, g, tau, imode):
        """merge modes imode and imode+1 into a single mode
        return gp and taup corresponding to this new mode;
        12/2018 - also tries finetuning before returning
        
        uses helper functions:
        - normKern_magic()
        - costFcn_magic()   
        """
        
        iniGuess = [g[imode] + g[imode+1], 0.5*(tau[imode] + tau[imode+1])]
        res      = minimize(self.costFcn_magic, iniGuess, args=(g, tau, imode))

        newtau   = np.delete(tau, imode+1)
        newtau[imode] = res.x[1]
            
        return newtau

    def normKern_magic(self, t, gn, taun, g1, tau1, g2, tau2):
        """helper function: for costFcn and mergeModes"""
        Gn = gn * np.exp(-t/taun)
        Go = g1 * np.exp(-t/tau1) + g2 * np.exp(-t/tau2)
        return (Gn/Go - 1.)**2

    def costFcn_magic(self, par, g, tau, imode):
        """"helper function for mergeModes; establishes cost function to minimize"""
        gn   = par[0]
        taun = par[1]

        g1   = g[imode]
        g2   = g[imode+1]
        tau1 = tau[imode]
        tau2 = tau[imode+1]

        tmin = min(tau1, tau2)/10.
        tmax = max(tau1, tau2)*10.

        return quad(self.normKern_magic, tmin, tmax, args=(gn, taun, g1, tau1, g2, tau2))[0]

    def FineTuneSolution(self, tau, t, Gexp, isPlateau, estimateError=False):
        """Given a spacing of modes tau, tries to do NLLS to fine tune it further
        If it fails, then it returns the old tau back
        
        Uses helper function: res_tG which computes residuals
        """
        success = False
            
        try:
            res  = least_squares(self.res_tG, tau, bounds=(0., np.inf),	args=(t, Gexp, isPlateau))
            tau  = res.x
            tau0 = tau.copy()

            # Error Estimate	
            if estimateError:
                J = res.jac
                cov = np.linalg.pinv(J.T.dot(J)) * (res.fun**2).mean()
                dtau = np.sqrt(np.diag(cov))

            success = True			
        except:	
            e = sys.exc_info()[0]
            self.Qprint( "<p>Error: %s</p>" % e )            
            #pass

        
        g, tau, _, _ = self.MaxwellModes(np.log(tau), t, Gexp, isPlateau)   # Get g_i, taui

        #
        # if mode has dropped out, then need to delete corresponding dtau mode
        #
        if estimateError and success:
            if len(tau) < len(tau0):		
                nkill = 0
                for i in range(len(tau0)):
                    if np.min(np.abs(tau0[i] - tau)) > 1e-12 * tau0[i]:
                        dtau = np.delete(dtau, i-nkill)
                        nkill += 1
            return g, tau, dtau
        elif estimateError:
            return g, tau, -1*np.ones(len(tau))
        else:
            return g, tau

    def res_tG(self, tau, texp, Gexp, isPlateau):
        """
            Helper function for final optimization problem
        """
        g, _, _ = self.nnLLS(texp, tau, Gexp, isPlateau)
        Gmodel  = np.zeros(len(texp))

        for j in range(len(tau)):
            Gmodel += g[j] * np.exp(-texp/tau[j])
        
        # add G0
        if isPlateau:
            Gmodel += g[-1]
            
        residual = Gmodel/Gexp - 1.
            
        return residual


    def MaxwellModesTime(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns

        # CALCULATE THE CONTINUOUS SPECTRUM FIRST
        self.Qprint("<b>CONTINUOUS SPECTRUM</b>")

        t = ft.data[:, 0]
        Gexp =  ft.data[:, 1]
        # Remove points with t<=0
        filt=t>0
        t=t[filt]
        Gexp=Gexp[filt]

        # Sanitize the input: remove repeated values and space data homogeneously
        t, indices = np.unique(t, return_index = True)	
        Gexp         = Gexp[indices]
        f  =  interp1d(t, Gexp, fill_value="extrapolate")
        t  =  np.logspace(np.log10(np.min(t)), np.log10(np.max(t)), max(len(t),100))		
        Gexp =  f(t)
        self.tfit = np.copy(t)

        n = len(t)
        ns = self.parameters['ns'].value
        tmin = t[0]
        tmax = t[n-1]

        # determine frequency window
        if self.parameters['FreqEnd'].value == 1:
            smin = np.exp(-np.pi/2) * tmin; smax = np.exp(np.pi/2) * tmax		
        elif self.parameters['FreqEnd'].value == 2:
            smin = tmin; smax = tmax				
        elif self.parameters['FreqEnd'].value == 3:
            smin = np.exp(+np.pi/2) * tmin; smax = np.exp(-np.pi/2) * tmax		

        hs   = (smax/smin)**(1./(ns-1))
        s    = smin * hs**np.arange(ns)
        
        kernMat = self.getKernMat(s, t)
        tic     = time.time()
        plateau = self.parameters["plateau"].value

        self.Qprint('Initial Set up...',end='')
        if plateau:
            Hgs, G0  = self.InitializeH(Gexp, s, kernMat, np.min(Gexp))
        else:
            Hgs      = self.InitializeH(Gexp, s, kernMat)
        
        te   = time.time() - tic
        self.Qprint('({0:.1f} s)'.format(te))
        tic  = time.time()

        # Find Optimum Lambda with 'lcurve'
        lamC = self.parameters['lamC'].value
        self.Qprint('Building the L-curve ...',end='')
        if lamC == 0:
            if plateau:
                lamC, lam, rho, eta, logP, Hlam = self.lcurve(Gexp, Hgs, kernMat, G0)
            else:
                lamC, lam, rho, eta, logP, Hlam = self.lcurve(Gexp, Hgs, kernMat)

        te = time.time() - tic
        self.Qprint('({0:.1f} s)'.format(te))
        tic = time.time()
        self.Qprint('lamC = {0:0.3e}'.format(lamC))

        # Get the best spectrum	
        self.Qprint('Extracting CRS...',end='')
        if plateau:
            H, G0  = self.getH(lamC, Gexp, Hgs, kernMat, G0)
            self.Qprint('G0 = {0:0.3e} ...'.format(G0))
        else:
            H  = self.getH(lamC, Gexp, Hgs, kernMat)

        te = time.time() - tic
        self.Qprint('done ({0:.1f} s)'.format(te))

		# Save inferred H(s) and Gw
        if lamC != 0:
            if plateau:
                self.K   = self.kernel_prestore(H, kernMat, G0);	
                #np.savetxt('output/H.dat', np.c_[s, H], fmt='%e', header='G0 = {0:0.3e}'.format(G0))
            else:
                self.K   = self.kernel_prestore(H, kernMat)
                #np.savetxt('output/H.dat', np.c_[s, H], fmt='%e')
             
            #np.savetxt('output/Gfit.dat', np.c_[w, K[:n], K[n:]], fmt='%e')
            if self.prediction_mode == PredictionMode.cont:
                tt.num_rows = len(t)
                tt.data = np.zeros((tt.num_rows, tt.num_columns))
                tt.data[:, 0] = t
                tt.data[:, 1] = self.K

        # Spectrum
        self.scont = s
        self.Hcont = H

        # GET DISCRETE SPECTRUM
        self.Qprint("<b>DISCRETE SPECTRUM</b>")

        # range of N scanned
        MaxNumModes=self.parameters['MaxNumModes'].value

        if(MaxNumModes == 0):
            Nmax  = min(np.floor(3.0 * np.log10(max(t)/min(t))),n/4); # maximum N
            Nmin  = max(np.floor(0.5 * np.log10(max(t)/min(t))),2);   # minimum N
            Nv    = np.arange(Nmin, Nmax + 1).astype(int)
        else:
            Nv    = np.arange(MaxNumModes, MaxNumModes + 1).astype(int)

        Cerror  = 1./(np.std(self.K/Gexp - 1.))  #	Cerror = 1.?
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
            wt  = self.GetWeights(H, t, s, wb)

            # Scan the range of number of Maxwell modes N = (Nmin, Nmax) 
            ev    = np.zeros(npts)
            nzNv  = np.zeros(npts)  # number of nonzero modes 

            for i, N in enumerate(Nv):
                z, hz  = self.GridDensity(np.log(s), wt, N)         # select "tau" Points
                g, tau, ev[i], _ = self.MaxwellModes(z, t, Gexp, plateau)    # get g_i
                nzNv[i]                 = len(g)

            # store the best solution for this particular wb
            AIC        = 2. * Nv + 2. * Cerror * ev

            # Fine-Tune the best in class-fit further by trying an NLLS optimization on it.
            #		
            N      = Nv[np.argmin(AIC)]
            z, hz  = self.GridDensity(np.log(s), wt, N)     		# Select "tau" Points

            g, tau, error, cKp = self.MaxwellModes(z, t, Gexp, plateau)   # Get g_i, taui

            AICbst[ib] = min(AIC)
            Nbst[ib]   = Nv[np.argmin(AIC)]
            nzNbst[ib] = nzNv[np.argmin(AIC)]

        # global best settings of wb and Nopt; note this is nominal Nopt (!= len(g) due to NNLS)
        Nopt  = int(Nbst[np.argmin(AICbst)])
        wbopt = wtBase[np.argmin(AICbst)]

        #
        # Recompute the best data-set stats
        #
        wt                   = self.GetWeights(H, t, s, wbopt)
        z, hz                = self.GridDensity(np.log(s), wt, Nopt)             # Select "tau" Points
        g, tau, _, _   = self.MaxwellModes(z, t, Gexp, plateau)     # Get g_i, taui	
        g, tau, dtau       = self.FineTuneSolution(tau, t, Gexp, plateau, estimateError=True)
        
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
            tau     = self.mergeModes_magic(g, tau, imode)

            g, tau, dtau  = self.FineTuneSolution(tau, t, Gexp, plateau, estimateError=True)		

            if len(tau)==1:
                break        
            tauSpacing = tau[1:]/tau[:-1]
            itry      += 1

        if plateau:
            G0 = g[-1]
            g  = g[:-1]

        self.Qprint('Number of optimum nodes = {0:d}'.format(len(g)))
        self.Qprint('log10(Condition number) of matrix equation: {0:.2f}'.format(np.log10(cKp)))

        # Spectrum
        self.sdisc = tau
        self.Hdisc = g

        S, T    = np.meshgrid(tau, t)
        K      = np.exp(-T/S)
        self.GtM   	= np.dot(K, g)

        if plateau:
            self.GtM += G0

        # TODO: DECIDE IF WE PLOT THE CONTINUOUS OR DISCRETE FIT TO G*(omega)
        if self.prediction_mode == PredictionMode.disc:
            self.Qprint('<b>Fit from discrete spectrum</b>')
            tt.num_rows = len(t)
            tt.data = np.zeros((tt.num_rows, tt.num_columns))
            tt.data[:, 0] = t
            tt.data[:, 1] = self.GtM
        else:
            self.Qprint('<b>Fit from continuous spectrum</b>')

        try:
            gamma = float(f.file_parameters["gamma"])
            if (gamma==0):
                gamma=1
        except:
            gamma = 1

    def do_fit(self, line=''):
        self.Qprint("Fitting not allowed in this theory")

    def do_error(self, line):
        total_error = 0
        npoints = 0
        view = self.parent_dataset.parent_application.current_view
        tools = self.parent_dataset.parent_application.tools       
        # table='''<table border="1" width="100%">'''
        # table+='''<tr><th>File</th><th>Error (RSS)</th><th># Pts</th></tr>'''
        tab_data = [['%-18s' % 'File', '%-18s' % 'Error (RSS)', '%-18s' % '# Pts'],]
        for f in self.theory_files():
            if self.stop_theory_flag:
                break
            xexp, yexp, success = view.view_proc(f.data_table,
                                                 f.file_parameters)
            tmp_dt = self.get_non_extended_th_table(f)
            xth, yth, success = view.view_proc(tmp_dt,
                                               f.file_parameters)

            yth2=np.copy(yexp)
            for i in range(xexp.shape[1]):
                fint = interp1d(xth[:,i],yth[:,i],'cubic') # Get the theory at the same points as the data
                yth2[:,i] = np.copy(fint(xexp[:,i]))
            xth = np.copy(xexp)
            yth = np.copy(yth2)

            if (self.xrange.get_visible()):
                conditionx = (xexp > self.xmin) * (xexp < self.xmax)
            else:
                conditionx = np.ones_like(xexp, dtype=np.bool)
            if (self.yrange.get_visible()):
                conditiony = (yexp > self.ymin) * (yexp < self.ymax)
            else:
                conditiony = np.ones_like(yexp, dtype=np.bool)
            conditionnaninf = (~np.isnan(xexp)) * (~np.isnan(yexp)) * (
                ~np.isnan(xth)) * (~np.isnan(yth)) * (~np.isinf(xexp)) * (
                    ~np.isinf(yexp)) * (~np.isinf(xth)) * (~np.isinf(yth))
            yexp = np.extract(conditionx * conditiony * conditionnaninf, yexp)
            yth = np.extract(conditionx * conditiony * conditionnaninf, yth)
            f_error = np.mean((yth - yexp)**2)
            npt = len(yth)
            total_error += f_error * npt
            npoints += npt
            # table+= '''<tr><td>%-18s</td><td>%-18.4g</td><td>%-18d</td></tr>'''% (f.file_name_short, f_error, npt)
            tab_data.append(['%-18s'% f.file_name_short, '%-18.4g' % f_error, '%-18d' %npt])
        # table+='''</table><br>'''
        # self.Qprint(table)
        self.Qprint(tab_data)

    def plot_theory_stuff(self):
        """[summary]
        
        [description]
        """
        if not self.view_modes:
            return

        # PLOT CONTINUOUS SPECTRUM
        view = self.parent_dataset.parent_application.current_view
        data_table_tmp = DataTable(self.axarr)
        data_table_tmp.num_columns = 2
        ns = self.parameters['ns'].value
        data_table_tmp.num_rows = ns
        data_table_tmp.data = np.zeros((ns, 2))
        data_table_tmp.data[:, 0] = self.scont
        data_table_tmp.data[:, 1] = np.exp(self.Hcont)
        try:
            x, y, success = view.view_proc(data_table_tmp, None)
        except TypeError as e:
            print(e)
            return
        self.contspectrum.set_data(x, y)

        data_table_tmp.num_columns = 2
        nmodes = len(self.sdisc)
        data_table_tmp.num_rows = nmodes
        data_table_tmp.data = np.zeros((nmodes, 2))
        data_table_tmp.data[:, 0] = self.sdisc
        data_table_tmp.data[:, 1] = self.Hdisc
        try:
            x, y, success = view.view_proc(data_table_tmp, None)
        except TypeError as e:
            print(e)
            return
        self.discspectrum.set_data(x, y)


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

        self.tbutpredmode = QToolButton()
        self.tbutpredmode.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        self.cont_pred_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-minimum-value.png'),
            "Fit from Spectrum")
        self.disc_pred_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-scatter-plot.png'),
            "Fit from Discrete")
        if self.prediction_mode == PredictionMode.cont:
            self.tbutpredmode.setDefaultAction(self.cont_pred_action)
        else:
            self.tbutpredmode.setDefaultAction(self.disc_pred_action)
        self.tbutpredmode.setMenu(menu)
        tb.addWidget(self.tbutpredmode)
    
        self.modesaction = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-visible.png'), 'View modes')
        self.plateauaction = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-flat-tire-80.png'), 'is there a residual plateau?')
        self.save_modes_action = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-save-Maxwell.png'),
            "Save Modes")            
        self.save_spectrum_action = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-save_Ht.png'),
            "Save Spectrum")            
        self.modesaction.setCheckable(True)
        self.modesaction.setChecked(True)
        self.plateauaction.setCheckable(True)
        self.plateauaction.setChecked(False)
        self.thToolsLayout.insertWidget(0, tb)

        connection_id = self.modesaction.triggered.connect(
            self.modesaction_change)
        connection_id = self.plateauaction.triggered.connect(
            self.plateauaction_change)
        connection_id = self.save_modes_action.triggered.connect(
            self.save_modes)
        connection_id = self.save_spectrum_action.triggered.connect(
            self.save_spectrum)
        connection_id = self.cont_pred_action.triggered.connect(
            self.select_cont_pred)
        connection_id = self.disc_pred_action.triggered.connect(
            self.select_disc_pred)

    def select_cont_pred(self):
        self.prediction_mode = PredictionMode.cont
        self.tbutpredmode.setDefaultAction(self.cont_pred_action)

        if len(self.tfit) > 0:
            th_files = self.theory_files()
            for f in self.parent_dataset.files:
                if f in th_files:
                    tt = self.tables[f.file_name_short]
                    tt.num_rows = len(self.tfit)
                    tt.data = np.zeros((tt.num_rows, tt.num_columns))
                    tt.data[:, 0] = self.tfit
                    tt.data[:, 1] = self.K

            self.Qprint('<b>Fit from continuous spectrum</b>')
            self.do_error('')
            self.do_plot('')

    def select_disc_pred(self):
        self.prediction_mode = PredictionMode.disc
        self.tbutpredmode.setDefaultAction(self.disc_pred_action)

        if len(self.tfit) > 0:
            th_files = self.theory_files()
            for f in self.parent_dataset.files:
                if f in th_files:
                    tt = self.tables[f.file_name_short]
                    tt.num_rows = len(self.tfit)
                    tt.data = np.zeros((tt.num_rows, tt.num_columns))
                    tt.data[:, 0] = self.tfit
                    tt.data[:, 1] = self.GtM

            self.Qprint('<b>Fit from discrete spectrum</b>')
            self.do_error('')
            self.do_plot('')

    def plateauaction_change(self, checked):
        self.set_param_value("plateau", checked)

    def save_spectrum(self):
        """Save Spectrum to a text file"""
        fpath, _ = QFileDialog.getSaveFileName(self,
                                               "Save spectrum to a text file",
                                               "data/", "Text (*.txt)")
        if fpath == '':
            return
            
        with open(fpath, 'w') as f:

            header = '# Continuous spectrum\n'
            header += '# Generated with RepTate v%s %s\n' % (Version.VERSION,
                                                             Version.DATE)
            header += '# At %s on %s\n' % (time.strftime("%X"),
                                           time.strftime("%a %b %d, %Y"))
            f.write(header)

            f.write('\n#%15s\t%15s\n'%('tau_i','G_i'))

            n = len(self.scont)
            for i in range(n):
                f.write('%15g\t%15g\n'%(self.scont[i],np.exp(self.Hcont[i])))
            
            f.write('\n#end')

        QMessageBox.information(self, 'Success',
                                'Wrote spectrum \"%s\"' % fpath)

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
