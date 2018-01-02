# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Daniel Read, d.j.read@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module TheoryTobitaBatch

TobitaBatch file for creating a new theory
""" 
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable

from react_ctypes_helper import *

class TheoryTobitaBatch(CmdBase):
    """TheoryTobitaBatch
    
    [description]
    """
    thname='TobitaBatchTheory'
    description='TobitaBatch Theory'
    citations=''

    def __new__(cls, name='ThTobitaBatch', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTobitaBatch'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryTobitaBatch(name, parent_dataset, ax) if (CmdBase.mode==CmdMode.GUI) else CLTheoryTobitaBatch(name, parent_dataset, ax)


class BaseTheoryTobitaBatch():
    """[summary]
    
    [description]
    """
    single_file = False # True if the theory can be applied to multiple files simultaneously

    def __init__(self, name='ThTobitaBatch', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTobitaBatch'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        
        react_pool_init()
        self.link_lists()
        self.reactname = "LDPE batch %d"%(tb_global.tobbatchnumber)
        tb_global.tobbatchnumber += 1
        self.function = self.Calc
        self.simexists = False
        self.dist_exists = False
        self.ndist = 0
        self.has_modes = False # True if the theory has modes

        self.parameters['tau'] = Parameter(name='tau', value=0.002, description='tau', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['beta'] = Parameter(name='beta', value=0.0, description='beta', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['Cb'] = Parameter(name='Cb', value=0.02, description='Cb', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['Cs'] = Parameter(name='Cs', value=0.0005, description='Cs', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['fin_conv'] = Parameter(name='fin_conv', value=0.4, description='fin_conv', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['num_to_make'] = Parameter(name='num_to_make', value=1000, description='number of molecules made in the simulation', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['mon_mass'] = Parameter(name='mon_mass', value=28, description='this is the mass, in a.m.u., of a monomer (usually set to 28 for PE)', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['Me'] = Parameter(name='Me', value=1000, description='the entanglement molecular weight', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['nbin'] = Parameter(name='nbin', value=100, description='number of bins', 
                                          type=ParameterType.real, opt_type=OptType.const)

    def link_lists(self):
        for i in range(pb_global_const.maxarm + 1):
            arm_pool[i] = return_arm_pool(c_int(i))
        
        for i in range(pb_global_const.maxpol + 1):
            br_poly[i] = return_br_poly(c_int(i))

        for i in range(pb_global_const.maxreact + 1):
            react_dist[i] = return_react_dist(c_int(i))
    

# function TTheory_tobita_batch.Calc(var ytheory, ydata: TTable; var FileParam: TStringList;
#   var TheoryParam: array of real): Integer;
    def Calc(self, f=None):
        # var
        # i,nbins,numtomake,m:integer
        # fin_conv, tau, beta, Cb, Cs, monmass, Me:double

        # get parameters
        tau = self.parameters['tau'].value
        beta = self.parameters['beta'].value
        Cb = self.parameters['Cb'].value
        Cs = self.parameters['Cs'].value
        fin_conv = self.parameters['fin_conv'].value
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
        # react_dist[ndist].name = self.reactname #TODO: set the dist name in the C library 
        react_dist[ndist].contents.polysaved = False

        if self.simexists:
            return_dist_polys(c_int(ndist))

        # initialise tobita batch
        tobbatchstart(c_double(fin_conv), c_double(tau), c_double(beta), c_double(Cs), c_double(Cb), c_int(ndist))
        react_dist[ndist].contents.npoly = 0

        react_dist[ndist].contents.M_e = Me
        react_dist[ndist].contents.monmass = monmass
        react_dist[ndist].contents.nummwdbins = nbins

        # make numtomake polymers
        i = 0
        while i < numtomake:
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
                if tobbatch(c_int(m), c_int(ndist)): # routine returns false if arms ran out
                    react_dist[ndist].contents.npoly += 1
                    i += 1
                    # check for error
                    if tb_global.tobitabatcherrorflag:
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
                    tb_global.tobitabatcherrorflag = True
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
        if (react_dist[ndist].contents.npoly >= 100) and (not tb_global.tobitabatcherrorflag):
            molbin(ndist)
            ft = f.data_table
            # print("nummwdbins=", polybits.react_dist[ndist].contents.nummwdbins)
            
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

    def do_error(self, line):
        pass

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
        
    def destructor(self):
        """Return arms to pool"""
        polybits.return_dist(self.ndist)

class CLTheoryTobitaBatch(BaseTheoryTobitaBatch, Theory):
    """[summary]
    
    [description]
    """
    def __init__(self, name='ThTobitaBatch', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTobitaBatch'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
   
    # This class usually stays empty


class GUITheoryTobitaBatch(BaseTheoryTobitaBatch, QTheory):
    """[summary]
    
    [description]
    """
    def __init__(self, name='ThTobitaBatch', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTobitaBatch'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)


        #disable buttons 
        self.parent_dataset.actionMinimize_Error.setDisabled(True)
        # self.parent_dataset.actionCalculate_Theory.setDisabled(True)
        self.parent_dataset.actionShow_Limits.setDisabled(True)
        self.parent_dataset.actionVertical_Limits.setDisabled(True)
        self.parent_dataset.actionHorizontal_Limits.setDisabled(True)
       