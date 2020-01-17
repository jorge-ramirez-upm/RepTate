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
"""Module ApplicationLAOS

Large Amplitude Oscillatory Shear

"""
from CmdBase import CmdBase, CmdMode
from Application import Application
from QApplicationWindow import QApplicationWindow
from View import View
from FileType import TXTColumnFile
import numpy as np


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
        from TheoryMITlaos import TheoryMITlaos

        super().__init__(name, parent)

        # VIEWS
        # set the views that can be selected in the view combobox
        self.views['sigma(t),gamma(t) RAW'] = View(
            name='sigma-gamma(t)',
            description='Stress and strain as a function of time',
            x_label='$t$',
            y_label='$\sigma(t),\gamma(t)$',
            x_units='s',
            y_units='Pa, -',
            log_x=False,
            log_y=False,
            view_proc=self.view_sigmatgammat,
            n=2,
            snames=['$\sigma(t)^\mathrm{raw}$', '$\gamma(t)^\mathrm{raw}$'])

        self.views['sigma(gamma) RAW'] = View(
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

        self.views['sigma(gamma) FILTERED'] = View(
            name='sigma(gamma)',
            description='Stress as a function of strain',
            x_label='$\gamma(t)$',
            y_label='$\sigma(t)$',
            x_units='-',
            y_units='Pa',
            log_x=False,
            log_y=False,
            view_proc=self.view_sigmagammaFILTERED,
            n=1,
            snames=['$\sigma(\gamma)$'])

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

        self.views['sigma(gammadot)'] = View(
            name='sigma(gammadot)',
            description='Stress as a function of strain-rate',
            x_label='$\dot\gamma(t)$',
            y_label='$\sigma(t)$',
            x_units='s$^{-1}$',
            y_units='Pa',
            log_x=False,
            log_y=False,
            view_proc=self.view_sigmagammadot,
            n=1,
            snames=['$\sigma(\dot\gamma)$'])

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
            snames=['chebelastic'])

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

        self.views['sigma(t) RAW'] = View(
            name='sigma(t)',
            description='Stress as a function of time - RAW',
            x_label='$t$',
            y_label='$\sigma(t)^\mathrm{raw}$',
            x_units='s',
            y_units='Pa',
            log_x=False,
            log_y=False,
            view_proc=self.view_sigmat,
            n=1,
            snames=['$\sigma(t)^\mathrm{raw}$'])

        self.views['gamma(t) RAW'] = View(
            name='gamma(t)',
            description='Strain as a function of time - RAW',
            x_label='$t$',
            y_label='$\gamma(t)^\mathrm{raw}$',
            x_units='s',
            y_units='-',
            log_x=False,
            log_y=False,
            view_proc=self.view_gammat,
            n=1,
            snames=['$\gamma(t)^\mathrm{raw}$'])

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
        self.theories[TheoryMITlaos.thname] = TheoryMITlaos
        self.add_common_theories()  # Add basic theories to the application

        #set the current view
        self.set_views()

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

    def view_sigmagammaFILTERED(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """

        # DO EVERYTHING IN THEORYMITLAOS UNTIL COLUMNS 3 (gam_recon) AND 4 (tau_recon) ARE CREATED
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

        #n = self.parameters['n'].value
        n=15
        self.maxharmonic = 0
        if Ncycles !=0:
            # finds max odd harmonic
            self.maxharmonic = int(np.floor(len(gam)/(2*Ncycles)))
            evencheck = self.maxharmonic/2
            if (evencheck == round(evencheck)):
                self.maxharmonic = self.maxharmonic-1
        #self.Qprint('Max odd harminic = %d'%self.maxharmonic)

        n = min(n, self.maxharmonic)

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

        #PPQC = self.parameters['pq'].value
        PPQC=50
        PPC=4*PPQC #Points Per Cycle

        gam_recon=np.zeros(PPC)
        for q in range(PPC): # sum for each point in time, 1 full cycle, no overlap
            gam_recon[q] = gam_0*np.sin(2*np.pi*q/PPC) # Reconstruct WITHOUT phase shift

        # make gam_recon 1.5 cycles with 1 point overlap
        gam_recon = np.array(gam_recon.tolist() + gam_recon[:2*PPQC+1].tolist())

        tau_recon = np.zeros(PPC) # initialize tau_recon   (m harmonics included)

        #m = self.parameters['n'].value
        m = 15
        for q in range(PPC):  # sum for each point in time for 1 full cycle, no overlap
            for p in range(1,m+1,2): # m:total number of harmonics to consider; sum over ODD harmonics only
                tau_recon[q] += Bn[Ncycles*p-1]*np.sin(p*2*np.pi*q/PPC) + An[Ncycles*p-1]*np.cos(p*2*np.pi*q/PPC)

        #make tau_recon* 1.5 cycles with 1 point overlap
        tau_recon = np.array(tau_recon.tolist() + tau_recon[0:2*PPQC+1].tolist())

        ndata=len(gam_recon)
        x = np.zeros((ndata, 1))
        y = np.zeros((ndata, 1))
        x[:, 0] = gam_recon
        y[:, 0] = tau_recon
        return x, y, True        

    def view_sigmat(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        if dt.num_columns>3:
            pickindex=np.abs(dt.data[:,0])>0
            time=dt.data[pickindex, 0]
            sigma=dt.data[pickindex, 2]
            ndata=len(time)
            x = np.zeros((ndata, 1))
            y = np.zeros((ndata, 1))
            x[:, 0] = time
            y[:, 0] = sigma
        else:
            x = np.zeros((dt.num_rows, 1))
            y = np.zeros((dt.num_rows, 1))
            x[:, 0] = dt.data[:, 0]
            y[:, 0] = dt.data[:, 2]

        return x, y, True

    def view_gammat(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        if dt.num_columns>3:
            pickindex=np.abs(dt.data[:,0])>0
            time=dt.data[pickindex, 0]
            gamma=dt.data[pickindex, 1]
            ndata=len(time)
            x = np.zeros((ndata, 1))
            y = np.zeros((ndata, 1))
            x[:, 0] = time
            y[:, 0] = gamma
        else:
            x = np.zeros((dt.num_rows, 1))
            y = np.zeros((dt.num_rows, 1))
            x[:, 0] = dt.data[:, 0]
            y[:, 0] = dt.data[:, 1]
        return x, y, True

    def view_sigmatgammat(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        if dt.num_columns>3:
            pickindex=np.abs(dt.data[:,0])>0
            time=dt.data[pickindex, 0]
            gamma=dt.data[pickindex, 1]
            sigma=dt.data[pickindex, 2]
            ndata=len(time)
            x = np.zeros((ndata, 2))
            y = np.zeros((ndata, 2))
            x[:, 0] = time
            x[:, 1] = time
            y[:, 0] = sigma
            y[:, 1] = gamma
        else:
            x = np.zeros((dt.num_rows, 2))
            y = np.zeros((dt.num_rows, 2))
            x[:, 0] = dt.data[:, 0]
            x[:, 1] = dt.data[:, 0]
            y[:, 0] = dt.data[:, 2]
            y[:, 1] = dt.data[:, 1]


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
        if dt.num_columns>3:
            pickindex=np.abs(dt.data[:,5])>0
            gdot=dt.data[pickindex, 5]
            tau=dt.data[pickindex, 6]
            ndata=len(gdot)
            x = np.zeros((ndata, 1))
            y = np.zeros((ndata, 1))
            x[:, 0] = gdot
            y[:, 0] = tau
        else:
            x = np.zeros((0,1))
            y = np.zeros((0,1))
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
        # EVERYTHING UP TO         
        # tt.data[0:wn_end, 7] = wn[0:wn_end]
        # tt.data[0:wn_end, 8] = G_compNORM[0:wn_end]



        if dt.num_columns>3:
            pickindex=np.abs(dt.data[:,7])>0
            w=dt.data[pickindex, 7]
            Gn=dt.data[pickindex, 8]
            ndata=len(w)
            x = np.zeros((ndata, 1))
            y = np.zeros((ndata, 1))
            x[:, 0] = w
            y[:, 0] = Gn
        else:
            x = np.zeros((0,1))
            y = np.zeros((0,1))
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
        if dt.num_columns>3:
            pickindex=np.abs(dt.data[:,9])>0
            n=dt.data[pickindex, 9]
            en=dt.data[pickindex, 10]
            ndata=len(n)
            x = np.zeros((ndata, 1))
            y = np.zeros((ndata, 1))
            x[:, 0] = n
            y[:, 0] = en
        else:
            x = np.zeros((0,1))
            y = np.zeros((0,1))
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
        if dt.num_columns>3:
            pickindex=np.abs(dt.data[:,9])>0
            n=dt.data[pickindex, 9]
            vn=dt.data[pickindex, 11]
            ndata=len(n)
            x = np.zeros((ndata, 1))
            y = np.zeros((ndata, 1))
            x[:, 0] = n
            y[:, 0] = vn
        else:
            x = np.zeros((0,1))
            y = np.zeros((0,1))
        return x, y, True

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

        #add the GUI-specific objects here:
