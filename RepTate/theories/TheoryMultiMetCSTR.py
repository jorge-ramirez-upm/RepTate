# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module TheoryMultiMetCSTR

"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from PyQt5.QtCore import pyqtSignal
from collections import OrderedDict
from PyQt5.QtWidgets import QApplication

import ctypes as ct
import react_ctypes_helper as rch
import react_gui_tools as rgt

class TheoryMultiMetCSTR(CmdBase):
    """[summary]
    
    [description]
    """
    thname='MultiMetCSTRTheory'
    description='MultiMetCSTR Theory'
    citations=''

    def __new__(cls, name='ThMultiMetCSTR', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThMultiMetCSTR'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryMultiMetCSTR(name, parent_dataset, axarr) if (CmdBase.mode==CmdMode.GUI) else CLTheoryMultiMetCSTR(name, parent_dataset, axarr)


class BaseTheoryMultiMetCSTR:
    """[summary]
    
    [description]
    """
    single_file = True # False if the theory can be applied to multiple files simultaneously
    signal_request_dist = pyqtSignal(object)
    signal_request_polymer = pyqtSignal(object)
    signal_request_arm = pyqtSignal(object)

    def __init__(self, name='ThMultiMetCSTR', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThMultiMetCSTR'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.reactname = "MultiMetCSTR %d"%(rch.MMCSTR_global.mulmetCSTRnumber)
        rch.MMCSTR_global.mulmetCSTRnumber += 1
        self.function = self.Calc 
        self.simexists = False
        self.dist_exists = False
        self.ndist = 0
        self.has_modes = False # True if the theory has modes

        self.parameters = OrderedDict() # keep the dictionary key in order for the parameter table
        self.parameters['num_to_make'] = Parameter(name='num_to_make', value=1000, description='number of molecules made in the simulation', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['mon_mass'] = Parameter(name='mon_mass', value=28, description='this is the mass, in a.m.u., of a monomer (usually set to 28 for PE)', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['Me'] = Parameter(name='Me', value=1000, description='the entanglement molecular weight', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.parameters['nbin'] = Parameter(name='nbin', value=50, description='number of bins', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.numcat_max = 30
        # default parameters value
        self.numcat = 2
        self.time_const = 300.0
        self.monomer_conc = 2.0
        self.init_param_values()

        self.signal_request_dist.connect(rgt.request_more_dist)
        self.signal_request_polymer.connect(rgt.request_more_polymer)
        self.signal_request_arm.connect(rgt.request_more_arm)

    def init_param_values(self):
        self.pvalues = [['0' for j in range(5)] for i in range(self.numcat_max)] #initially self.numcat=2 lines of parameters
        self.pvalues[0][0] = '4e-4' #cat conc
        self.pvalues[0][1] = '101.1' #Kp
        self.pvalues[0][2] = '0.1' #K=
        self.pvalues[0][3] = '0.2' #Ks
        self.pvalues[0][4] = '5' #KpLCB

        self.pvalues[1][0] = '1e-3'
        self.pvalues[1][1] = '90.17'
        self.pvalues[1][2] = '1.5'
        self.pvalues[1][3] = '0.3'



    def Calc(self, f=None):
        """MultiMetCSTR function that returns the square of y
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        
        # get parameters
        numtomake = np.round(self.parameters['num_to_make'].value)
        monmass = self.parameters['mon_mass'].value
        Me = self.parameters['Me'].value
        nbins = int(np.round(self.parameters['nbin'].value))
        
        c_ndist = ct.c_int()

        #resize theory datatable
        ft = f.data_table        
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = 1
        tt.data = np.zeros((tt.num_rows, tt.num_columns))

        #request a dist
        if not self.dist_exists:
            success = rch.request_dist(ct.byref(c_ndist))
            self.ndist = c_ndist.value
            if not success:
                #launch dialog asking for more dist
                self.signal_request_dist.emit(self) #use signal to open QDialog in the main GUI window
                return
            else:
                self.dist_exists = True
        ndist = self.ndist
        # rch.react_dist[ndist].contents.name = self.reactname #TODO: set the dist name in the C library 
        rch.react_dist[ndist].contents.polysaved = False

        if self.simexists:
            rch.return_dist_polys(ct.c_int(ndist))
        self.simexists = False

        #launch form
        dialog = rgt.ParameterMultiMetCSTR(self)

        if not dialog.exec_(): #TODO: use signal->emit
            return


        conc = (ct.c_double * self.numcat)()
        kp = (ct.c_double * self.numcat)()
        kdb = (ct.c_double * self.numcat)()
        ks = (ct.c_double * self.numcat)()
        kplcb = (ct.c_double * self.numcat)()
        for i in range(self.numcat):
            conc[i] = ct.c_double(float(self.pvalues[i][0]))
            kp[i] = ct.c_double(float(self.pvalues[i][1]))
            kdb[i] = ct.c_double(float(self.pvalues[i][2]))
            ks[i] = ct.c_double(float(self.pvalues[i][3]))
            kplcb[i] = ct.c_double(float(self.pvalues[i][4]))

        #initialise metallocene CSTR
        rch.mulmetCSTRstart(kp, kdb, ks, kplcb, conc, ct.c_double(self.time_const), ct.c_double(self.monomer_conc), ct.c_int(self.numcat), ct.c_int(ndist), ct.c_int(self.numcat_max))

        rch.react_dist[ndist].contents.npoly = 0
        rch.react_dist[ndist].contents.M_e = Me
        rch.react_dist[ndist].contents.monmass = monmass
        rch.react_dist[ndist].contents.nummwdbins = nbins
        c_m = ct.c_int()

        # make numtomake polymers
        i = 0
        while i < numtomake:
            if self.stop_theory_calc_flag:
                self.print_signal.emit('Polymer creation stopped by user')
                break
            # get a polymer
            success = rch.request_poly(ct.byref(c_m))
            m = c_m.value
            if success: # check availability of polymers
            # put it in list
                if rch.react_dist[ndist].contents.npoly == 0:  # case of first polymer made
                    rch.react_dist[ndist].contents.first_poly = m
                    rch.set_br_poly_nextpoly(ct.c_int(m), ct.c_int(0)) #br_poly[m].contents.nextpoly = 0
                else:           # next polymer, put to top of list
                    rch.set_br_poly_nextpoly(ct.c_int(m), ct.c_int(rch.react_dist[ndist].contents.first_poly)) #br_poly[m].contents.nextpoly = rch.react_dist[ndist].contents.first_poly
                    rch.react_dist[ndist].contents.first_poly = m
                
                # make a polymer
                if rch.mulmetCSTR(ct.c_int(m), ct.c_int(ndist)): # routine returns false if arms ran out
                    rch.react_dist[ndist].contents.npoly += 1
                    i += 1
                    # check for error
                    if rch.MMCSTR_global.mulmetCSTRerrorflag:
                        self.print_signal.emit('Polymers too large: gelation occurs for these parameters')
                        i = numtomake
                else: # error message if we ran out of arms
                    self.success_increase_memory = None
                    self.signal_request_arm.emit(self)
                    while self.success_increase_memory is None: # wait for the end of QDialog
                        pass
                    if self.success_increase_memory:
                        continue  # back to the start of while loop
                    else:
                        i = numtomake
                        rch.MMCSTR_global.mulmetCSTRerrorflag = True

                # update on number made
                if rch.react_dist[ndist].contents.npoly % np.trunc(numtomake/20) == 0:
                    self.print_signal.emit('Made %d polymers'%rch.react_dist[ndist].contents.npoly)
                    # QApplication.processEvents() # needed to use Qprint if in single-thread

            else:   # polymer wasn't available
                self.success_increase_memory = None
                self.signal_request_polymer.emit(self)
                while self.success_increase_memory is None:
                    pass
                if self.success_increase_memory:
                    continue
                else:
                    i = numtomake
        # end make polymers loop

        calc = 0
        # do analysis of polymers made
        if (rch.react_dist[ndist].contents.npoly >= 100) and (not rch.MMCSTR_global.mulmetCSTRerrorflag):
            rch.molbin(ndist)
            ft = f.data_table

            #resize theory data table
            ft = f.data_table
            tt = self.tables[f.file_name_short]
            tt.num_columns = ft.num_columns
            tt.num_rows = rch.react_dist[ndist].contents.nummwdbins
            tt.data = np.zeros((tt.num_rows, tt.num_columns))

            for i in range(1, rch.react_dist[ndist].contents.nummwdbins + 1):
                tt.data[i - 1, 0] = np.power(10, rch.react_dist[ndist].contents.lgmid[i])
                tt.data[i - 1, 1] = rch.react_dist[ndist].contents.wt[i]
                tt.data[i - 1, 2] = rch.react_dist[ndist].contents.avg[i]
                tt.data[i - 1, 3] = rch.react_dist[ndist].contents.avbr[i]

            self.print_signal.emit('*************************')
            # self.print_signal.emit('End of calculation \"%s\"'%rch.react_dist[ndist].contents.name)
            self.print_signal.emit('Made %d polymers'%rch.react_dist[ndist].contents.npoly)
            self.print_signal.emit('Saved %d polymers in memory'%rch.react_dist[ndist].contents.nsaved)
            self.print_signal.emit('Mn = %.3g'%rch.react_dist[ndist].contents.m_n)
            self.print_signal.emit('Mw = %.3g'%rch.react_dist[ndist].contents.m_w)
            self.print_signal.emit('br/1000C = %.3g'%rch.react_dist[ndist].contents.brav)
            self.print_signal.emit('*************************')

            calc = rch.react_dist[ndist].contents.nummwdbins - 1
            rch.react_dist[ndist].contents.polysaved = True

        self.simexists = True
        self.print_signal.emit('%d arm records left in memory'%rch.pb_global.arms_left) 
        return calc


    def destructor(self):
        """Return arms to pool"""
        rch.return_dist(ct.c_int(self.ndist))

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
        


class CLTheoryMultiMetCSTR(BaseTheoryMultiMetCSTR, Theory):
    """[summary]
    
    [description]
    """
    def __init__(self, name='ThMultiMetCSTR', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThMultiMetCSTR'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
   
    # This class usually stays empty


class GUITheoryMultiMetCSTR(BaseTheoryMultiMetCSTR, QTheory):
    """[summary]
    
    [description]
    """
    def __init__(self, name='ThMultiMetCSTR', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThMultiMetCSTR'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        rgt.initialise_tool_bar(self)

    def theory_buttons_disabled(self, state):
        rgt.theory_buttons_disabled(self, state)

    def handle_stop_calulation(self):
        rgt.handle_stop_calulation(self)

    def handle_save_bob_configuration(self):
        rgt.handle_save_bob_configuration(self)
       
    def handle_edit_bob_settings(self):
        rgt.handle_edit_bob_settings(self)

       