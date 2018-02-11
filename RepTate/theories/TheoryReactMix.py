# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module TheoryReactMix

"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from PyQt5.QtWidgets import QApplication

import ctypes as ct
import react_ctypes_helper as rch
import react_gui_tools as rgt

class TheoryReactMix(CmdBase):
    """[summary]
    
    [description]
    """
    thname='ReactMixTheory'
    description='ReactMix Theory'
    citations=''

    def __new__(cls, name='ThReactMix', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThReactMix'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryReactMix(name, parent_dataset, axarr) if (CmdBase.mode==CmdMode.GUI) else CLTheoryReactMix(name, parent_dataset, axarr)


class BaseTheoryReactMix:
    """[summary]
    
    [description]
    """
    single_file = True # False if the theory can be applied to multiple files simultaneously

    def __init__(self, name='ThReactMix', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThReactMix'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.Calc 
        self.simexists = False
        self.calc_exists = False
        self.has_modes = False # True if the theory has modes

        self.parameters['nbin'] = Parameter(name='nbin', value=100, description='number of bins', 
                                          type=ParameterType.real, opt_type=OptType.const)
        self.reactname = 'ReactMix'
        self.dists = [] # index of the react_dist array used in mix
        self.weights = [] # weight of the dist
        self.n_inmix = None # number of theories in mix
        self.theory_names = None # names of theories in mix

    def Calc(self, f=None):
        """ReactMix function that returns the square of y
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        nbins = int(np.round(self.parameters['nbin'].value))
        
        #init theory data table - in case of error and 'return'
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = 0
        tt.data = np.zeros((tt.num_rows, tt.num_columns))

        #first check that some distributions have polymers in
        distscheck = False
        for i in range(rch.pb_global_const.maxreact):
            distscheck = distscheck or rch.react_dist[i].contents.polysaved
        if not distscheck: #no distributions have polymers in
            self.print_signal.emit('No polymers made in other theories yet!  Make some polymers.')
            return

        #show form
        dialog = rgt.ParameterReactMix(self)
        if not dialog.exec_(): #TODO: use signal->emit
            self.print_signal.emit('Mixture canceled')
            return
        
        #check mix settings
        if (self.n_inmix==0):
            self.print_signal.emit('Mixture not defined')
            return

        #do multiple binning based on form results
        c_weights = (ct.c_double * self.n_inmix)()
        c_dists = (ct.c_int * self.n_inmix)()
        for i in range(self.n_inmix):
            c_weights[i] = ct.c_double(float(self.weights[i]))
            c_dists[i] = ct.c_int(int(self.dists[i]))
        rch.multimolbin(ct.c_int(nbins), c_weights, c_dists, ct.c_int(self.n_inmix))        
        
        #resize theory data table
        tt.num_rows = rch.bab_global.multi_nummwdbins
        tt.data = np.zeros((tt.num_rows, tt.num_columns))

        for i in range(1, rch.bab_global.multi_nummwdbins + 1):
            c_i = ct.c_int(i)
            tt.data[i - 1, 0] = np.power(10, rch.return_binsandbob_multi_lgmid(c_i))
            tt.data[i - 1, 1] = rch.return_binsandbob_multi_wt(c_i)
            tt.data[i - 1, 2] = rch.return_binsandbob_multi_avg(c_i)
            tt.data[i - 1, 3] = rch.return_binsandbob_multi_avbr(c_i)

        totpoly = 0
        totsaved = 0
        self.print_signal.emit('*************************')
        self.print_signal.emit('End of mixture calculation')
        # for i in range (1, rch.pb_global_const.maxreact):
        #     if mixtureform.inmix[i]:

        for i, dist in enumerate(self.dists):
            totpoly = totpoly + rch.react_dist[dist].contents.npoly
            totsaved = totsaved + rch.react_dist[dist].contents.nsaved
            self.print_signal.emit('Used distribution %s'%self.theory_names[i])
            self.print_signal.emit('Containing %d polymers'%rch.react_dist[dist].contents.npoly)
            self.print_signal.emit('Including %d saved polymers'%rch.react_dist[dist].contents.nsaved)

        self.print_signal.emit('Total polymers: %d'%totpoly)
        self.print_signal.emit('Total saved polymers: %d'%totsaved)
        self.print_signal.emit('Mn = %.3g'%rch.bab_global.multi_m_n)
        self.print_signal.emit('Mw = %.3g'%rch.bab_global.multi_m_w)
        self.print_signal.emit('br/1000C = %.3g'%rch.bab_global.multi_brav)
        self.print_signal.emit('*************************')

        return rch.bab_global.multi_nummwdbins - 1
        self.calcexists = True

    def destructor(self):
        """Return arms to pool"""
        pass

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
        


class CLTheoryReactMix(BaseTheoryReactMix, Theory):
    """[summary]
    
    [description]
    """
    def __init__(self, name='ThReactMix', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThReactMix'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
   
    # This class usually stays empty


class GUITheoryReactMix(BaseTheoryReactMix, QTheory):
    """[summary]
    
    [description]
    """
    def __init__(self, name='ThReactMix', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThReactMix'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        rgt.initialise_tool_bar(self)
        self.bob_settings_button.setDisabled(True)
        self.save_bob_configuration_button.setDisabled(True)

    def theory_buttons_disabled(self, state):
        rgt.theory_buttons_disabled(self, state)

    def handle_stop_calulation(self):
        rgt.handle_stop_calulation(self)

    def handle_save_bob_configuration(self):
        rgt.handle_save_mix_configuration(self)
       
    def handle_edit_bob_settings(self):
        rgt.handle_edit_bob_settings(self)

       