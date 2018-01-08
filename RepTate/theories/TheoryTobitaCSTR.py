# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module TheoryTobitaCSTR

Template file for creating a new theory
""" 
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable

from react_ctypes_helper import *
from ctypes import *

class TheoryTobitaCSTR(CmdBase):
    """LDPE CSTR reaction theory
    
    The LDPE CSTR reaction theory uses an algorithm based on the one described in
the paper by H. Tobita (J. Pol. Sci. Part B, 39, 391-403 (2001)) for batch
reactions. The algorithm is based upon a set of processes occuring in the
reactor during free-radical polymerisation.
    
    [description]
    """
    thname='TobitaCSTRTheory'
    description='Tobita LDPE CSTR reaction theory'
    citations='J. Pol. Sci. Part B, 39, 391-403 (2001)'

    def __new__(cls, name='ThTemplate', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTemplate'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryTobitaCSTR(name, parent_dataset, ax) if (CmdBase.mode==CmdMode.GUI) else CLTheoryTobitaCSTR(name, parent_dataset, ax)


class BaseTheoryTobitaCSTR:
    """[summary]
    
    [description]
    """
    single_file = True # True if the theory can be applied to multiple files simultaneously

    def __init__(self, name='ThTemplate', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTemplate'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.reactname = "LDPE CSTR %d"%(tCSTR_global.tobCSTRnumber)
        tCSTR_global.tobCSTRnumber += 1
        self.function = self.Calc
        self.simexists = False
        self.dist_exists = False
        self.ndist = 0
        self.has_modes = False # True if the theory has modes
        
        self.parameters['tau'] = Parameter(name='tau', value=1.11e-3, description='tau', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['beta'] = Parameter(name='beta', value=9.75e-6, description='beta', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['lambda'] = Parameter(name='lambda', value=2e-3, description='Cb', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['sigma'] = Parameter(name='sigma', value=1.8e-4, description='Cs', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['num_to_make'] = Parameter(name='num_to_make', value=1000, description='number of molecules made in the simulation', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['mon_mass'] = Parameter(name='mon_mass', value=28, description='this is the mass, in a.m.u., of a monomer (usually set to 28 for PE)', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['Me'] = Parameter(name='Me', value=1000, description='the entanglement molecular weight', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['nbin'] = Parameter(name='nbin', value=100, description='number of bins', 
                                          type=ParameterType.real, opt_type=OptType.const)

    def get_modes(self):
        """[summary]
        
        [description]
        
        Returns:
            [type] -- [description]
        """
        pass

    def set_modes(self):
        """[summary]
        
        [description]
        
        Arguments:

        """
        pass

    def do_error(self, line):
        pass

    def Calc(self, f=None):
        """Template function that returns the square of y
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        
        # get parameters
        tau = self.parameters['tau'].value
        beta = self.parameters['beta'].value
        lambda_ = self.parameters['lambda'].value
        sigma = self.parameters['sigma'].value
        numtomake = np.round(self.parameters['num_to_make'].value)
        monmass = self.parameters['mon_mass'].value
        Me = self.parameters['Me'].value
        nbins = int(np.round(self.parameters['nbin'].value))
        
        c_ndist = c_int()
        if not self.dist_exists:
            success = request_dist(byref(c_ndist))
            self.ndist = c_ndist.value
            if not success:
                self.Qprint('Too many theories open for internal storage. Please close a theory')
                return
            self.dist_exists = True
        ndist = self.ndist
        # react_dist[ndist].contents.name = self.reactname #TODO: set the dist name in the C library 
        react_dist[ndist].contents.polysaved = False

        if self.simexists:
            return_dist_polys(c_int(ndist))

        # initialise tobita batch
        tobCSTRstart(c_double(tau), c_double(beta), c_double(sigma), c_double(lambda_), c_int(ndist))
        react_dist[ndist].contents.npoly = 0

        react_dist[ndist].contents.M_e = Me
        react_dist[ndist].contents.monmass = monmass
        react_dist[ndist].contents.nummwdbins = nbins

        # make numtomake polymers
        i = 0
        while i < numtomake:
            if self.stop_theory_calc_flag:
                self.Qprint('Polymer creation stopped by user')
                break
            # get a polymer
            c_m = c_int()
            success = request_poly(byref(c_m))
            m = c_m.value
            if success: # check availability of polymers
            # put it in list
                if react_dist[ndist].contents.npoly == 0:  # case of first polymer made
                    react_dist[ndist].contents.first_poly = m
                    br_poly[m].contents.nextpoly = 0
                else:           # next polymer, put to top of list
                    br_poly[m].contents.nextpoly = react_dist[ndist].contents.first_poly
                    react_dist[ndist].contents.first_poly = m

                # make a polymer
                if tobCSTR(c_int(m), c_int(ndist)): # routine returns false if arms ran out
                    react_dist[ndist].contents.npoly += 1
                    i += 1
                    # check for error
                    if tCSTR_global.tobitaCSTRerrorflag:
                        self.Qprint('Polymers too large: gelation occurs for these parameters')
                        i = numtomake
                else: # error message if we ran out of arms
                    message = 'Ran out of storage for arm records. Options to avoid this are:\n'
                    message += '(1) Reduce number of polymers requested\n'
                    message += '(2) Adjust BoB parameters so that fewer polymers are saved\n'
                    message += '(3) Close some other theories\n'
                    message += '(4) Adjust parameters to avoid gelation'
                    self.Qprint(message)
                    i = numtomake
                    tCSTR_global.tobitaCSTRerrorflag = True
                # update on number made
                if react_dist[ndist].contents.npoly % np.trunc(numtomake/20) == 0:
                    self.Qprint('Made %d polymers'%react_dist[ndist].contents.npoly)

            else:   # polymer wasn't available
                message = 'Ran out of storage for polymer records. Options to avoid this are:'
                message += '(1) Reduce number of polymers requested'
                message += '(2) Close some other theories'
                self.Qprint(message)
                i = numtomake
        # end make polymers loop

        calc = 0
        # do analysis of polymers made
        if (react_dist[ndist].contents.npoly >= 100) and (not tCSTR_global.tobitaCSTRerrorflag):
            molbin(ndist)
            ft = f.data_table

            #resize theory data table
            ft = f.data_table
            tt = self.tables[f.file_name_short]
            tt.num_columns = ft.num_columns
            tt.num_rows = react_dist[ndist].contents.nummwdbins
            tt.data = np.zeros((tt.num_rows, tt.num_columns))

            for i in range(1, react_dist[ndist].contents.nummwdbins + 1):
                tt.data[i - 1, 0] = np.power(10, react_dist[ndist].contents.lgmid[i])
                tt.data[i - 1, 1] = react_dist[ndist].contents.wt[i]
                tt.data[i - 1, 2] = react_dist[ndist].contents.avg[i]
                tt.data[i - 1, 3] = react_dist[ndist].contents.avbr[i]

            self.Qprint('*************************')
            # self.Qprint('End of calculation \"%s\"'%react_dist[ndist].contents.name)
            self.Qprint('Made %d polymers'%react_dist[ndist].contents.npoly)
            self.Qprint('Saved %d polymers in memory'%react_dist[ndist].contents.nsaved)
            self.Qprint('Mn = %.3g'%react_dist[ndist].contents.m_n)
            self.Qprint('Mw = %.3g'%react_dist[ndist].contents.m_w)
            self.Qprint('br/1000C = %.3g'%react_dist[ndist].contents.brav)
            self.Qprint('*************************')
            # labelout.Caption = 'Made '+inttostr(polybits.react_dist[ndist].contents.npoly)+' polymers, Mn='
            #   +floattostrF(polybits.react_dist[ndist].contents.M_n,ffGeneral,5,2)+', Mw='
            #   +floattostrF(polybits.react_dist[ndist].contents.M_w,ffGeneral,5,2)+', br/1000C='
            #   +floattostrF(polybits.react_dist[ndist].contents.brav,ffGeneral,5,2)

            calc = react_dist[ndist].contents.nummwdbins - 1
            react_dist[ndist].contents.polysaved = True

        self.simexists = True
        self.Qprint('%d arm records left in memory'%pb_global.arms_left) 
        self.Qprint('%s'%ndist)
        return calc

    def destructor(self):
        """Return arms to pool"""
        return_dist(c_int(self.ndist))


class CLTheoryTobitaCSTR(BaseTheoryTobitaCSTR, Theory):
    """[summary]
    
    [description]
    """
    def __init__(self, name='ThTemplate', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTemplate'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
   
    # This class usually stays empty


class GUITheoryTobitaCSTR(BaseTheoryTobitaCSTR, QTheory):
    """[summary]
    
    [description]
    """
    def __init__(self, name='ThTemplate', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTemplate'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)

    # add widgets specific to the theory here:
       