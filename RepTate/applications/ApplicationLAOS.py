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
"""Module ApplicationLAOS

Large Amplitude Oscillatory Shear

"""
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Application import Application
from RepTate.gui.QApplicationWindow import QApplicationWindow
from RepTate.core.View import View
from RepTate.core.FileType import TXTColumnFile
import numpy as np
from PyQt5.QtWidgets import QSpinBox, QPushButton, QHBoxLayout, QLineEdit, QLabel, QSizePolicy


class ApplicationLAOS(CmdBase):
    """Application for ...

    [description]
    """
    appname = 'LAOS'
    description = 'LAOS Application'  #used in the command-line Reptate
    extension = "laos"  # drag and drop this extension automatically opens this application

    def __new__(cls, name='LAOS', parent=None):
        """[summary]

        [description]

        Keyword Arguments:
            - name {[type]} -- [description] (default: {'LAOS'})
            - parent {[type]} -- [description] (default: {None})

        Returns:
            - [type] -- [description]
        """
        return GUIApplicationLAOS(name, parent) if (
            CmdBase.mode == CmdMode.GUI) else CLApplicationLAOS(
                name, parent)


class BaseApplicationLAOS:
    """[summary]

    [description]
    """

    #help_file = ''
    appname = ApplicationLAOS.appname


    def __init__(self, name='LAOS', parent=None, **kwargs):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {'LAOS'})
            - parent {[type]} -- [description] (default: {None})
        """
        # IMPORT THEORIES
        from TheoryRoliePoly import TheoryRoliePoly
        from TheoryUCM import TheoryUCM
        from TheoryGiesekus import TheoryGiesekus
        from TheoryPomPom import TheoryPomPom

        super().__init__(name, parent)

        # VIEWS
        # set the views that can be selected in the view combobox
        self.views['sigma,gamma(t)'] = View(
            name='sigma,gamma(t)',
            description='RAW Stress and RAW strain as a function of time',
            x_label='$t$',
            y_label='$\sigma^\mathrm{raw}(t),\gamma^\mathrm{raw}(t)$',
            x_units='s',
            y_units='Pa, -',
            log_x=False,
            log_y=False,
            view_proc=self.view_sigmatgammatRAW,
            n=2,
            snames=['$\sigma(t)^\mathrm{raw}$', '$\gamma(t)^\mathrm{raw}$'])

        self.views['sigma SCA,gamma(t)'] = View(
            name='sigma SCA,gamma(t)',
            description='RAW SCALED Stress and RAW strain as a function of time',
            x_label='$t$',
            y_label='$\sigma^\mathrm{raw,scaled}(t),\gamma^\mathrm{raw}(t)$',
            x_units='s',
            y_units='Pa, -',
            log_x=False,
            log_y=False,
            view_proc=self.view_sigmatgammatRAWSCALED,
            n=2,
            snames=['$\sigma(t)^\mathrm{raw,scaled}$', '$\gamma(t)^\mathrm{raw}$'])

        self.views['sigma(gamma)'] = View(
            name='sigma(gamma)',
            description='Stress as a function of strain - RAW',
            x_label='$\gamma(t)^\mathrm{raw}$',
            y_label='$\sigma(t)^\mathrm{raw}$',
            x_units='-',
            y_units='Pa',
            log_x=False,
            log_y=False,
            view_proc=self.view_sigmagammaRAW,
            n=1,
            snames=['$\sigma^\mathrm{raw}(\gamma^\mathrm{raw})$'])

        self.views['sigma(gamma) FILT'] = View(
            name='sigma(gamma) FILT',
            description='Stress as a function of strain',
            x_label='$\gamma^\mathrm{filtered}(t)$',
            y_label='$\sigma^\mathrm{filtered}(t)$',
            x_units='-',
            y_units='Pa',
            log_x=False,
            log_y=False,
            view_proc=self.view_sigmagammaFILTERED,
            n=1,
            snames=['$\sigma^\mathrm{filtered}(\gamma^\mathrm{filtered})$'])

        self.views['FFT spectrum'] = View(
            name='FFT spectrum',
            description='Full Fast Fourier Transform spectrum',
            x_label='$\omega$',
            y_label='$|\sigma^*_n|/|\sigma^*_1|$',
            x_units='rad.s$^{-1}$',
            y_units='-',
            log_x=False,
            log_y=True,
            view_proc=self.view_fftspectrum,
            n=1,
            snames=['FFT'])

        self.views['sigma(gdot) FILT'] = View(
            name='sigma(gdot) FILT',
            description='FILTERED Stress as a function of strain-rate',
            x_label='$\dot\gamma^\mathrm{filtered}(t)$',
            y_label='$\sigma^\mathrm{filtered}(t)$',
            x_units='s$^{-1}$',
            y_units='Pa',
            log_x=False,
            log_y=False,
            view_proc=self.view_sigmagammadot,
            n=1,
            snames=['$\sigma(\dot\gamma)$'])

        self.views['sigma(gamma) ANLS'] = View(
            name='sigma(gamma) ANLS',
            description='FILTERED Stress as a function of strain - Analysis of contributions',
            x_label='$\gamma^\mathrm{filtered}(t)$',
            y_label='$\sigma^\mathrm{filtered}(t)$',
            x_units='s$^{-1}$',
            y_units='Pa',
            log_x=False,
            log_y=False,
            view_proc=self.view_sigmagammaANLS,
            n=3,
            snames=['$\sigma^\mathrm{filtered}$', '$\sigma^\mathrm{elastic}$', '$\sigma^\mathrm{Chebyshev 1+3}$'])

        self.views['sigma(gdot) ANLS'] = View(
            name='sigma(gdot) ANLS',
            description='FILTERED Stress as a function of strain-rate - Analysis of contributions',
            x_label='$\dot\gamma^\mathrm{filtered}(t)$',
            y_label='$\sigma^\mathrm{filtered}(t)$',
            x_units='s$^{-1}$',
            y_units='Pa',
            log_x=False,
            log_y=False,
            view_proc=self.view_sigmagammadotANLS,
            n=3,
            snames=['$\sigma^\mathrm{filtered}$', '$\sigma^\mathrm{elastic}$', '$\sigma^\mathrm{Chebyshev 1+3}$'])

        self.views['Cheb elastic'] = View(
            name='Cheb elastic',
            description='Chebyshev Coeff tau_elastic',
            x_label='Polynomial order, $n$',
            y_label='$e_n$',
            x_units='-',
            y_units='Pa',
            log_x=False,
            log_y=False,
            view_proc=self.view_chebelastic,
            n=1,
            snames=['chebelastic'],
            viewmode_data=ViewMode.bar)

        self.views['Cheb viscous'] = View(
            name='Cheb viscous',
            description='Chebyshev Coeff tau_viscous',
            x_label='Polynomial order, $n$',
            y_label='$v_n$',
            x_units='-',
            y_units='Pa.s',
            log_x=False,
            log_y=False,
            view_proc=self.view_chebviscous,
            n=1,
            snames=['chebviscous'])

        self.views['sigma(t)'] = View(
            name='sigma(t)',
            description='Stress as a function of time - RAW',
            x_label='$t$',
            y_label='$\sigma(t)^\mathrm{raw}$',
            x_units='s',
            y_units='Pa',
            log_x=False,
            log_y=False,
            view_proc=self.view_sigmatRAW,
            n=1,
            snames=['$\sigma(t)^\mathrm{raw}$'])

        self.views['gamma(t)'] = View(
            name='gamma(t)',
            description='Strain as a function of time - RAW',
            x_label='$t$',
            y_label='$\gamma(t)^\mathrm{raw}$',
            x_units='s',
            y_units='-',
            log_x=False,
            log_y=False,
            view_proc=self.view_gammatRAW,
            n=1,
            snames=['$\gamma(t)^\mathrm{raw}$'])

        self.HHSR = 15  # Highest harmonic to consider in stress reconstruction
        self.PPQC = 50  # Points per quarter cycle in FT reconstruction (20-500)

        #set multiviews
        #default view order in multiplot views, set only one item for single view
        #if more than one item, modify the 'nplots' in the super().__init__ call
        self.nplots = 4
        self.multiviews = []
        for i in range(self.nplot_max):
            # set views in the same order as declared above
            self.multiviews.append(list(self.views.values())[i])
        self.multiplots.reorg_fig(self.nplots)

        # FILES
        # set the type of files that ApplicationLAOS can open
        ftype = TXTColumnFile(
            name='Large-Angle Oscillatory Shear data',
            extension='laos',
            description='file containing laos data',
            col_names=['time', 'gamma', 'sigma'],
            basic_file_parameters=['omega', 'gamma'],
            col_units=['s','-', 'Pa'])
        self.filetypes[
            ftype.extension] = ftype  #add each the file type to dictionary

        # THEORIES
        self.theories[TheoryRoliePoly.thname] = TheoryRoliePoly
        self.theories[TheoryUCM.thname] = TheoryUCM
        self.theories[TheoryGiesekus.thname] = TheoryGiesekus
        self.theories[TheoryPomPom.thname] = TheoryPomPom
        self.add_common_theories()  # Add basic theories to the application

        #set the current view
        self.set_views()

    def view_sigmatgammatRAW(self, dt, file_parameters):
        """[summary]

        [description]

        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]

        Returns:
            - [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = dt.data[:, 0]
        x[:, 1] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 2]
        y[:, 1] = dt.data[:, 1]

        return x, y, True

    def view_sigmatgammatRAWSCALED(self, dt, file_parameters):
        """[summary]

        [description]

        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]

        Returns:
            - [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = dt.data[:, 0]
        x[:, 1] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 2]/np.max(np.abs(dt.data[:, 2]))
        y[:, 1] = dt.data[:, 1]

        return x, y, True

    def view_sigmagammaRAW(self, dt, file_parameters):
        """[summary]

        [description]

        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]

        Returns:
            - [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 1]
        y[:, 0] = dt.data[:, 2]
        return x, y, True

    def view_sigmagammaFILTERED(self, dt, file_parameters):
        """[summary]

        [description]

        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]

        Returns:
            - [type] -- [description]
        """
        gam_0, Bn, An, Ncycles = self.do_FFT_and_STUFF(dt)

        gam_recon, tau_recon = self.reconstruct_gamma_tau(An, Bn, gam_0, Ncycles)

        ndata=len(gam_recon)
        x = np.zeros((ndata, 1))
        y = np.zeros((ndata, 1))
        x[:, 0] = gam_recon
        y[:, 0] = tau_recon
        return x, y, True

    def view_fftspectrum(self, dt, file_parameters):
        """[summary]

        [description]

        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]

        Returns:
            - [type] -- [description]
        """
        gam_0, Bn, An, Ncycles = self.do_FFT_and_STUFF(dt)

        if Bn[Ncycles-1]>0:  # ensure that G_1' is positive
            Gp = Bn/gam_0    # G' from sine terms
        else:
            Gp = -Bn/gam_0

        if An[Ncycles-1]>0:  # ensure that G_1'' is positive
            Gpp = An/gam_0   # G'' from cosine terms
        else:
            Gpp = -An/gam_0

        N=len(An) # number of available harmonics
        G_complex = np.zeros(N)
        G_compNORM = np.zeros(N)
        for j in range(N):
            G_complex[j]=(Gp[j]**2+Gpp[j]**2)**0.5
        for j in range(N):
            G_compNORM[j] = G_complex[j]/G_complex[Ncycles-1] # max intensity occurs at Ncycles frequency

        # strain-rate is equal to omega*strain-shifted-1/4-cycle
        w = float(file_parameters["omega"])
        dw = w/Ncycles
        wn = np.linspace(dw,N*dw,N)
        if N > 25*Ncycles: # display a maximum of 25 harmonics, so that plot is not too "squished"
            wn_end = 25*Ncycles
        else:
            wn_end = len(wn)

        x = np.zeros((wn_end, 1))
        y = np.zeros((wn_end, 1))
        x[:, 0] = wn[0:wn_end]
        y[:, 0] = G_compNORM[0:wn_end]

        return x, y, True


    def view_sigmagammadot(self, dt, file_parameters):
        """[summary]

        [description]

        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]

        Returns:
            - [type] -- [description]
        """
        gam_0, Bn, An, Ncycles = self.do_FFT_and_STUFF(dt)
        gam_recon, tau_recon = self.reconstruct_gamma_tau(An, Bn, gam_0, Ncycles)

        PPC=4*self.PPQC #Points Per Cycle

        # w (omega) is currently a MANUAL input
        # strain-rate is equal to omega*strain-shifted-1/4-cycle
        w = float(file_parameters["omega"])
        gamdot_recon=w*gam_recon[self.PPQC:self.PPQC+PPC]  # One cylce of gamdot
        gamdot_recon = np.array(gamdot_recon.tolist() + gamdot_recon[:2*self.PPQC+1].tolist()) # make 1.5 cycles

        x = np.zeros((len(gamdot_recon), 1))
        y = np.zeros((len(tau_recon), 1))
        x[:, 0] = gamdot_recon # gamdot_recon interp1d
        y[:, 0] = tau_recon # tau_recon interp1d
        return x, y, True


    def view_sigmagammaANLS(self, dt, file_parameters):
        """[summary]

        [description]

        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]

        Returns:
            - [type] -- [description]
        """
        gam_0, Bn, An, Ncycles = self.do_FFT_and_STUFF(dt)
        gam_recon, tau_recon = self.reconstruct_gamma_tau(An, Bn, gam_0, Ncycles)

        PPC=4*self.PPQC #Points Per Cycle

        FTtau_e = np.zeros(PPC+1)
        tau_e_3    = np.zeros(PPC+1)  # "elastic" stress, from 1st & 3rd Harmonics

        for q in range(PPC):  # sum for each point in time for 1 full cycle, no overlap
            for p in range(1,self.HHSR+1,2): # self.HHSR:total number of harmonics to consider; sum over ODD harmonics only
                FTtau_e[q]   += Bn[Ncycles*p-1]*np.sin(p*2*np.pi*q/PPC)

        #RHE, added June 15, 2007, trying to use FT to reconstruct "Chebyshev"
        #curves
            for p in range(1,4,2): #Harmonics 1 & 3, for "elastic" stress
                tau_e_3[q] += Bn[Ncycles*p-1]*np.sin(p*2*np.pi*q/PPC)

        #make FTtau_* have one point overlap
        FTtau_e[PPC]=FTtau_e[0]
        tau_e_3[PPC]=tau_e_3[0]

        Xe=gam_recon[3*self.PPQC:5*self.PPQC+1]/gam_0 # gam_recon is 1.5 cycles
        # Create corresponding input function from Geo. Interp. decomposition
        fe = np.array(FTtau_e[3*self.PPQC:4*self.PPQC].tolist() + FTtau_e[:self.PPQC+1].tolist()) # tau_e is 1 cycle

        fe3 = np.array(tau_e_3[3*self.PPQC:4*self.PPQC].tolist() + tau_e_3[:self.PPQC+1].tolist()) # tau_e is 1 cycle

        ndata=max(len(gam_recon), len(Xe))
        x = np.zeros((ndata, 3))
        y = np.zeros((ndata, 3))
        x[:len(gam_recon), 0] = gam_recon
        y[:len(gam_recon), 0] = tau_recon
        x[:len(Xe), 1] = gam_0*Xe
        y[:len(Xe), 1] = fe
        x[:len(Xe), 2] = gam_0*Xe
        y[:len(Xe), 2] = fe3

        return x, y, True

    def view_sigmagammadotANLS(self, dt, file_parameters):
        """[summary]

        [description]

        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]

        Returns:
            - [type] -- [description]
        """

        gam_0, Bn, An, Ncycles = self.do_FFT_and_STUFF(dt)
        gam_recon, tau_recon = self.reconstruct_gamma_tau(An, Bn, gam_0, Ncycles)

        PPC=4*self.PPQC #Points Per Cycle

        # w (omega) is currently a MANUAL input
        # strain-rate is equal to omega*strain-shifted-1/4-cycle
        w = float(file_parameters["omega"])
        gamdot_recon=w*gam_recon[self.PPQC:self.PPQC+PPC]  # One cylce of gamdot
        gamdot_recon = np.array(gamdot_recon.tolist() + gamdot_recon[:2*self.PPQC+1].tolist()) # make 1.5 cycles

        FTtau_v = np.zeros(PPC+1)
        tau_v_3    = np.zeros(PPC+1)  # "viscous" stress, from 1st & 3rd Harmonics

        for q in range(PPC):  # sum for each point in time for 1 full cycle, no overlap
            for p in range(1,self.HHSR+1,2): # self.HHSR:total number of harmonics to consider; sum over ODD harmonics only
                FTtau_v[q]   += An[Ncycles*p-1]*np.cos(p*2*np.pi*q/PPC)

        #RHE, added June 15, 2007, trying to use FT to reconstruct "Chebyshev"
        #curves
            for p in range(1,4,2): #Harmonics 1 & 3, for "elastic" stress
                tau_v_3[q] += An[Ncycles*p-1]*np.cos(p*2*np.pi*q/PPC)

        #make FTtau_* have one point overlap
        FTtau_v[PPC]=FTtau_v[0]
        tau_v_3[PPC]=tau_v_3[0]

        Xv=gamdot_recon[2*self.PPQC:4*self.PPQC+1]/(gam_0*w) # gamdot_recon is 1.5 cycles
        # Create corresponding input function from Geo. Interp. decomposition
        fv = FTtau_v[2*self.PPQC:4*self.PPQC+1] # tau_v is 1 cycle

        fv3 = tau_v_3[2*self.PPQC:4*self.PPQC+1] # tau_v is 1 cycle

        ndata=max(len(gamdot_recon), len(Xv))
        x = np.zeros((ndata, 3))
        y = np.zeros((ndata, 3))
        x[:len(gamdot_recon), 0] = gamdot_recon
        y[:len(gamdot_recon), 0] = tau_recon
        x[:len(Xv), 1] = gam_0*w*Xv
        y[:len(Xv), 1] = fv
        x[:len(Xv), 2] = gam_0*w*Xv
        y[:len(Xv), 2] = fv3

        return x, y, True


    def view_chebelastic(self, dt, file_parameters):
        """[summary]

        [description]

        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]

        Returns:
            - [type] -- [description]
        """
        gam_0, Bn, An, Ncycles = self.do_FFT_and_STUFF(dt)

        if Bn[Ncycles-1]>0:  # ensure that G_1' is positive
            Gp = Bn/gam_0    # G' from sine terms
        else:
            Gp = -Bn/gam_0

        # Chebyshev coefficients, found from FT results
        e_n = np.zeros(int(np.floor(len(Gp)/Ncycles)))
        # contains e1, e2, e3, e4, ...
        for o in range(0,int(np.floor(len(Gp)/Ncycles)),2):
            e_n[o] = Gp[Ncycles*(o+1)-1]*(-1)**(o/2)  # only works for ODD Chebyshevs, so I leave even Chebyshevs = 0;

        x = np.zeros((self.HHSR, 1))
        y = np.zeros((self.HHSR, 1))
        x[:, 0] = np.linspace(1,self.HHSR,self.HHSR)
        y[:, 0] = e_n[0:self.HHSR]
        return x, y, True

    def view_chebviscous(self, dt, file_parameters):
        """[summary]

        [description]

        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]

        Returns:
            - [type] -- [description]
        """
        gam_0, Bn, An, Ncycles = self.do_FFT_and_STUFF(dt)

        if An[Ncycles-1]>0:  # ensure that G_1'' is positive
            Gpp = An/gam_0   # G'' from cosine terms
        else:
            Gpp = -An/gam_0

        w = float(file_parameters["omega"])

        # Chebyshev coefficients, found from FT results
        v_n = np.zeros(int(np.floor(len(Gpp)/Ncycles)))
        for o in range(0,int(np.floor(len(Gpp)/Ncycles)),2):
            v_n[o] = Gpp[Ncycles*(o+1)-1]/w

        x = np.zeros((self.HHSR, 1))
        y = np.zeros((self.HHSR, 1))
        x[:, 0] = np.linspace(1,self.HHSR,self.HHSR)
        y[:, 0] = v_n[0:self.HHSR]
        return x, y, True

    def view_sigmatRAW(self, dt, file_parameters):
        """[summary]

        [description]

        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]

        Returns:
            - [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 2]

        return x, y, True

    def view_gammatRAW(self, dt, file_parameters):
        """[summary]

        [description]

        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]

        Returns:
            - [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True

    def cycletrim_MITlaos(self, gamma, tau):
        d_zero=[]

        k=0 # k is a counter for the number of times gamma changes sign
        sign_gam = np.sign(gamma)
        for i in range(len(gamma)-1):
            if sign_gam[i] != sign_gam[i+1]:
                d_zero.append(i+1)  # index location after sign change
                k+=1

        lgth = len(d_zero)

        if lgth <= 1:
            #if there are 0 or 1 locations of gamma crossing zero,
            #it is impossible to extract the minimum of 1 cycle

            # give an output before exiting
            istrain = 0
            istress = 0
            N       = 0
            istart  = 0
            istop   = 0
            return istrain, istress, N, istart, istop

        if lgth == 2:
            #if there are 2 locations where gamma crosses zero,
            #a fancy cycle trimming must be performed, which will NOT start with a
            #sine wave
            #SEQUENCE:  estimate points per cycle
            #           check if there are enough points for single cycle (Npts) (error if not)
            #           include final Npts of signal

            #estimate number of points per cycle
            Npts = (d_zero[1] - d_zero[0]) *2

            if (len(gamma) < Npts): # if there are not enough points
                # give an output before exiting
                istrain = 0
                istress = 0
                N       = 0
                istart  = 0
                istop   = 0
                return istrain, istress, N, istart, istop
            else: # if there are enough points
                istart = len(gamma) - Npts
                istop  = len(gamma)
                N = 1

        if lgth > 2:
            if (lgth/2 != np.round(lgth/2)):   # Check if lgth is odd
                istart = d_zero[0]
                istop  = d_zero[-1]
                N = int((lgth - 1)/2)
            else:
                istart = d_zero[0]
                istop  = d_zero[lgth-2]
                N = int((lgth - 2)/2)

        istrain = gamma[istart:istop]
        istress = tau[istart:istop]

        return istrain, istress, N, istart, istop

    def FTtrig_MITlaos(self, f):
        """
        Find trigonometric Fourier Series components from FFT:
        f = A0 + SUM_n( An*cos(n*2*pi*t/T + Bn*sin(n*2*pi*t/T)

        VARIABLES
        f           vector to be transformed
        A0          essentially mean(f)
        An          cosine terms
        Bn          sine terms

        SEQUENCE
        force input to have EVEN number of data points (reqd for fft.m)
        take FFT > complex vector results
        extract trigonometric terms from complex vector
        """
        if int(len(f)/2) != len(f)/2:
            # trim last data point to force even number of data points
            # f MUST HAVE EVEN NUMBER OF DATA POINTS!
            f = f[0:len(f)-1]

        n=len(f)
        N=int(n/2)       # N will be the number of harmonics to consider

        Fn = np.fft.fft(f)
        # rearrange values such that: Fn_new = [ high < low | low > high ]
        Fn_new = np.array([np.conj(Fn[N])]+Fn[N+1:].tolist()+Fn[0:N+1].tolist())
        Fn_new /= n  # scale results

        #A0 = Fn_new[N]
        A0 = np.mean(f)
        An = 2*np.real(Fn_new[N+1:])    # cosine terms
        Bn = -2*np.imag(Fn_new[N+1:])   # sine terms

        return A0, An, Bn

    def chebyshev_decompose_MITlaos(self, F,N,X=None):
        """
        Find Chebyshev Polynomial components of input data vector:
        f = A0*T0(x) + A1*T1(x) + A2*T2(x) + ...

        [An]= chebyshev_decompose(F,N,X)
                *Assumes F occupies the domain [-1 : +1]
        with an arbitrary number of data points
        Uses trapz.m to calculate integrals
              INPUT VARIABLES
              F: vector of data, in domain [-1:1]
              N: degree of desired Legendre Polynomial decomposition
              X: Range points associated with F
              OUTPUT VARIABLE
              An: vector of Chebyshev coefficients
                  An(i) = A_{i-1}
        """
        M=len(F)
        if X is None: # Make X (input range) linear spaced and same length as F
            X=np.linspace(-1,1,M)

        An = np.zeros(N) # initialize vector of Chebyshev coefficients

        #T = gallery('chebvand',X);  # Matrix of Chebyshev polynomials evaluated at X
                                    #T(i,:) is (i-1)order polynomial
        T = np.zeros((M,M))
        T = np.transpose(np.polynomial.chebyshev.chebvander(X,M-1))
        #for i in range(M):
        #    T[i,:] = np.transpose(np.polynomial.chebyshev.chebvander(X,i))

        # COORDINATE TRANSFORM TECHNIQUE: NO WEIGHTING NECESSARY

        THETA = np.arcsin(X)

        # 0th order polynomial has different front factor
        An[0] = 1/np.pi * np.trapz(F, THETA)
        # Remaining coefficients use same front factor
        for i in range (1,N):
            An[i] = 2/np.pi * np.trapz(T[i,:]*F, THETA)

        return An

    def do_FFT_and_STUFF(self, dt):
        time_uneven  = dt.data[:,0]  # raw time
        gamma_uneven = dt.data[:,1]  # raw strain
        tau_uneven =   dt.data[:,2]  # raw stress

        # Force strain & stress data to be linearly space in time
        time   = np.linspace(time_uneven[0],time_uneven[-1],len(time_uneven))
        gamma  = np.interp(time, time_uneven,gamma_uneven)  # untrimmed strain
        tauxy  = np.interp(time, time_uneven,tau_uneven)    # untrimmed stress

        # This section is equivilent to cycletrim

        d_zero=[]

        k=0  # k is a counter for the number of times gamma changes sign
        sign_gam = np.sign(gamma)
        for i in range(len(gamma)-1):
            if sign_gam[i] != sign_gam[i+1]:
                k+=1
                d_zero.append(i+1) # index location after sign change

        # if the sign changed, and the previous point was NEGATIVE (or ZERO)
        # then it's the beginning of the sine wave

        # NB: the following assumes that strain signal is smooth enough so that the
        # cycles can be trimmed by finding the gamma=0 crossover points.

        lgth = len(d_zero)

        if lgth == 0:
            # give an output before exiting
            #self.Qprint('ERROR: Selected data never crosses zero.  Unable to find integer number of cycles')
            return

        elif lgth == 1:
            # if there are 0 or 1 locations of gamma crossing zero, it is impossible to extract the minimum of 1 cycle
            #self.Qprint('WARNING: It looks like you have only one cycle, but this cannot be confirmed.')
            Ncycles = 1
            istart  = 0
            istop   = len(gamma)

            time = time[istart:istop]
            istrain     = gamma[istart:istop]
            istress     = tauxy[istart:istop]

        elif lgth == 2:
            # if there are 2 locations where gamma crosses zero, a fancy cycle trimming must be performed, which will NOT start with a sine wave
            # SEQUENCE:  estimate points per cycle
            #           check if there are enough points for single cycle (Npts) (error if not)
            #           include final Npts of signal

            Npts = (d_zero[1] - d_zero[0] ) *2 # estimate number of points per cycle

            if len(gamma) < (0.95*Npts):  # if there are not enough points
                # give an output before exiting
                #self.Qprint('WARNING: It looks like there aren''t enough points for a complete cycle. Proceed with extreme caution.')
                istart  = 0
                istop   = len(gamma)
                Ncycles       = 1

                time = time[istart:istop]
                istrain     = gamma[istart:istop]
                istress     = tauxy[istart:istop]


            elif len(gamma) > (1.05*Npts): #  check for excess data beyond one cycle (x% tolerance)
                istart = len(gamma) - Npts
                istop  = len(gamma)
                Ncycles = 1

                time = time[istart:istop]
                istrain     = gamma[istart:istop]
                istress     = tauxy[istart:istop]

                #self.Qprint('WARNING: The beginning of your data was trimmed in order to have exactly one cycle')
            else:
                istart = 0
                istop  = len(gamma)
                Ncycles = 1

                time = time[istart:istop]
                istrain     = gamma[istart:istop]
                istress     = tauxy[istart:istop]
                #self.Qprint('WARNING: It looks like you have exactly one cycle.  It will not be trimmed.')

        elif lgth > 2:
            # perform cycle trimming as usual
            [gam, tau, Ncycles, istart, istop] = self.cycletrim_MITlaos(gamma, tauxy)
            time = time[istart:istop]
            #self.Qprint('Ncycles = %d'%Ncycles)

        # FTtrig_MITlaos
        A0, AnS, BnS = self.FTtrig_MITlaos(tau)
        gA0, gAnS, gBnS = self.FTtrig_MITlaos(gam)

        gam_0 = np.sqrt( gBnS[Ncycles-1]**2 + gAnS[Ncycles-1]**2 )  # acknowledge possible phase shift, but neglect h.o.t.
        delta = np.arctan( gAnS[Ncycles-1] / gBnS[Ncycles-1])         # raw signal phase shift

        An = np.zeros(len(AnS))
        Bn = np.zeros(len(BnS))
        for q in range(len(AnS)):  # Create NOT SHIFTED Fourier coefficients
            An[q] = AnS[q]*np.cos((q+1)*delta/Ncycles) - BnS[q]*np.sin((q+1)*delta/Ncycles)
            Bn[q] = BnS[q]*np.cos((q+1)*delta/Ncycles) + AnS[q]*np.sin((q+1)*delta/Ncycles)

        if abs(An[Ncycles-1]) > abs(Bn[Ncycles-1]):
            if An[Ncycles-1] < 0:
                An = -An
                Bn = -Bn
        else: # if the fundamental of Bn was larger, use it as the reference
            if Bn[Ncycles-1] < 0:
                An = -An
                Bn = -Bn

        return gam_0, Bn, An, Ncycles

    def reconstruct_gamma_tau(self, An, Bn, gam_0, Ncycles):
        PPC=4*self.PPQC #Points Per Cycle

        gam_recon=np.zeros(PPC)
        for q in range(PPC): # sum for each point in time, 1 full cycle, no overlap
            gam_recon[q] = gam_0*np.sin(2*np.pi*q/PPC) # Reconstruct WITHOUT phase shift

        # make gam_recon 1.5 cycles with 1 point overlap
        gam_recon = np.array(gam_recon.tolist() + gam_recon[:2*self.PPQC+1].tolist())

        tau_recon = np.zeros(PPC) # initialize tau_recon   (m harmonics included)

        for q in range(PPC):  # sum for each point in time for 1 full cycle, no overlap
            for p in range(1,self.HHSR+1,2): # self.HHSR:total number of harmonics to consider; sum over ODD harmonics only
                tau_recon[q] += Bn[Ncycles*p-1]*np.sin(p*2*np.pi*q/PPC) + An[Ncycles*p-1]*np.cos(p*2*np.pi*q/PPC)

        #make tau_recon* 1.5 cycles with 1 point overlap
        tau_recon = np.array(tau_recon.tolist() + tau_recon[0:2*self.PPQC+1].tolist())

        return gam_recon, tau_recon

class CLApplicationLAOS(BaseApplicationLAOS, Application):
    """[summary]

    [description]
    """

    def __init__(self, name='LAOS', parent=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {'LAOS'})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)
        #usually this class stays empty


class GUIApplicationLAOS(BaseApplicationLAOS, QApplicationWindow):
    """[summary]

    [description]
    """

    def __init__(self, name='LAOS', parent=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {'LAOS'})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)

        self.add_HHSR_widget()
        self.set_HHSR_widget_visible(False)
        self.add_PPQC_widget()
        self.set_PPQC_widget_visible(False)

    def add_HHSR_widget(self):
        """Add spinbox for HHSR"""
        self.sb_HHSR = QSpinBox()
        self.sb_HHSR.setRange(1, 99)
        self.sb_HHSR.setSingleStep(2)
        self.sb_HHSR.setValue(self.HHSR)
        self.sb_HHSR.setToolTip("Highest harmonic to consider in stress reconstruction")
        self.sb_HHSR.valueChanged.connect(self.change_HHSR)
        self.viewLayout.insertWidget(3, self.sb_HHSR)

    def change_HHSR(self, val):
        """Change the value of the HHSR.
        Called when the spinbox value is changed"""
        self.HHSR = val
        self.update_all_ds_plots()

    def set_HHSR_widget_visible(self, state):
        """Show/Hide the extra widget "HHSR" """
        self.sb_HHSR.setVisible(state)

    def add_PPQC_widget(self):
        """Add spinbox for HHSR"""
        self.sb_PPQC = QSpinBox()
        self.sb_PPQC.setRange(20, 500)
        self.sb_PPQC.setSingleStep(10)
        self.sb_PPQC.setValue(self.PPQC)
        self.sb_PPQC.setToolTip("Points per quarter cycle in FT reconstruction (20-500)")
        self.sb_PPQC.valueChanged.connect(self.change_PPQC)
        self.viewLayout.insertWidget(3, self.sb_PPQC)

    def change_PPQC(self, val):
        """Change the value of the PPQC.
        Called when the spinbox value is changed"""
        self.PPQC = val
        self.update_all_ds_plots()

    def set_PPQC_widget_visible(self, state):
        """Show/Hide the extra widget "PPQC" """
        self.sb_PPQC.setVisible(state)

    def set_view_tools(self, view_name):
        """Show/Hide extra view widgets depending on the current view"""
        if view_name in ["sigma(gamma) FILT", "FFT spectrum", "sigma(gdot) FILT", "sigma(gamma) ANLS", "sigma(gdot) ANLS", "Cheb elastic", "Cheb viscous"]:
            self.set_HHSR_widget_visible(True)
            self.set_PPQC_widget_visible(True)
        else:
            try:
                self.set_HHSR_widget_visible(False)
                self.set_PPQC_widget_visible(False)
            except AttributeError:
                pass
