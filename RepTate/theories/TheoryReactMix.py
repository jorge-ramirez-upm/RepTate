# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# --------------------------------------------------------------------------------------------------------
#
# Authors:
#     Jorge Ramirez, jorge.ramirez@upm.es
#     Victor Boudara, victor.boudara@gmail.com
#     Daniel Read, d.j.read@leeds.ac.uk
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
"""Module TheoryReactMix

"""
import os
import numpy as np
import time
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal

import ctypes as ct
import react_ctypes_helper as rch
import react_gui_tools as rgt


class TheoryReactMix(CmdBase):
    """[summary]
    
    [description]
    """
    thname = 'React Mix'
    description = 'Combine other active React theories'
    citations = []
    doi = []

    def __new__(cls, name='', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUITheoryReactMix(
            name, parent_dataset,
            axarr) if (CmdBase.mode == CmdMode.GUI) else CLTheoryReactMix(
                name, parent_dataset, axarr)


class BaseTheoryReactMix:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/React/Theory/mixture.html'
    single_file = True  # False if the theory can be applied to multiple files simultaneously
    thname = TheoryReactMix.thname
    citations = TheoryReactMix.citations
    doi = TheoryReactMix.doi

    signal_mix_dialog = pyqtSignal(object)

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.Calc
        self.simexists = False
        self.calc_exists = False
        self.has_modes = False  # True if the theory has modes

        self.parameters['nbin'] = Parameter(
            name='nbin',
            value=100,
            description='Number of molecular weight bins',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.reactname = 'ReactMix'
        self.dists = []  # index of the react_dist array used in mix
        self.weights = []  # weight of the dist
        self.n_inmix = 0  # number of theories in mix
        self.theory_names = []  # names of theories in mix
        self.theory_simnumber = [
        ]  # 'react_dist[].simnumber' of theories in mix
        self.calcexists = False
        self.do_priority_seniority = False
        self.signal_mix_dialog.connect(rgt.launch_mix_dialog)
        self.ratios = [] # list of ratios in dialog
        self.include = [] # list of (0 or 1) include in dialog

    def Calc(self, f=None):
        """ReactMix function
        
        [description]
        
        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        self.calcexists = False
        nbins = int(np.round(self.parameters['nbin'].value))
        rch.set_do_prio_senio(ct.c_bool(self.do_priority_seniority))

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
        if not distscheck:  #no distributions have polymers in
            self.Qprint(
                'No polymers made in other theories yet!  Make some polymers.')
            return

        #show form
        self.success_dialog = None
        self.signal_mix_dialog.emit(self)
        while self.success_dialog is None:  # wait for the end of QDialog
            time.sleep(
                0.5
            )  # TODO: find a better way to wait for the dialog thread to finish
        if not self.success_dialog:
            self.Qprint('Mixture cancelled')
            return

        #check mix settings
        if (self.n_inmix == 0):
            self.Qprint('Mixture not defined')
            return

        #do multiple binning based on form results
        c_weights = (ct.c_double * self.n_inmix)()
        c_dists = (ct.c_int * self.n_inmix)()
        for i in range(self.n_inmix):
            c_weights[i] = ct.c_double(float(self.weights[i]))
            c_dists[i] = ct.c_int(int(self.dists[i]))
        rch.multimolbin(
            ct.c_int(nbins), c_weights, c_dists, ct.c_int(self.n_inmix))

        #resize theory data table
        tt.num_rows = rch.bab_global.multi_nummwdbins
        tt.data = np.zeros((tt.num_rows, tt.num_columns))

        for i in range(1, rch.bab_global.multi_nummwdbins + 1):
            c_i = ct.c_int(i)
            tt.data[i - 1, 0] = np.power(
                10, rch.return_binsandbob_multi_lgmid(c_i))
            tt.data[i - 1, 1] = rch.return_binsandbob_multi_wt(c_i)
            tt.data[i - 1, 2] = rch.return_binsandbob_multi_avg(c_i)
            tt.data[i - 1, 3] = rch.return_binsandbob_multi_avbr(c_i)

        totpoly = 0
        totsaved = 0
        self.Qprint('<b>Mixture calculation results:</b>')
        # for i in range (1, rch.pb_global_const.maxreact):
        #     if mixtureform.inmix[i]:
        table = []
        table.append(['Distribution', '#Polymer', '#Saved'])
        for i, dist in enumerate(self.dists):
            totpoly = totpoly + rch.react_dist[dist].contents.npoly
            totsaved = totsaved + rch.react_dist[dist].contents.nsaved
            table.append([str(self.theory_names[i]), str(rch.react_dist[dist].contents.npoly), str(rch.react_dist[dist].contents.nsaved)])
            # self.Qprint('Used distribution %s' % self.theory_names[i])
            # self.Qprint(
            #     'Containing %d polymers' % rch.react_dist[dist].contents.npoly)
            # self.Qprint('Including %d saved polymers' %
            #             rch.react_dist[dist].contents.nsaved)
        self.Qprint(table)
        table = []
        table.append(['', '']) # no header
        table.append(['Total polymers', '%d' % totpoly])
        table.append(['Total saved polymers', '%d' % totsaved])
        table.append(['Mn', '%.3g' % rch.bab_global.multi_m_n])
        table.append(['Mw', '%.3g' % rch.bab_global.multi_m_w])
        table.append(['br/1000C', '%.3g' % rch.bab_global.multi_brav])
        self.Qprint(table)
        self.calcexists = True
        return rch.bab_global.multi_nummwdbins - 1

    def do_error(self, line):
        """This theory does not calculate the error"""
        pass

    def set_extra_data(self, extra_data):
        """Called when loading a project, set saved parameter values"""
        self.ratios = extra_data['ratios']
        self.include = extra_data['include']
        rgt.set_extra_data(self, extra_data)
    
    def get_extra_data(self):
        """Called when saving project. Save parameters in extra_data dict"""
        self.extra_data['ratios'] = self.ratios
        self.extra_data['include'] = self.include
        rgt.get_extra_data(self)

class CLTheoryReactMix(BaseTheoryReactMix, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # This class usually stays empty


class GUITheoryReactMix(BaseTheoryReactMix, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        rgt.initialise_tool_bar(self)
        self.bob_settings_button.setDisabled(True)
        self.btn_prio_senio.setDisabled(True)

    def theory_buttons_disabled(self, state):
        """
        Enable/Disable theory buttons, typically called at the start and stop of a calculation.
        This is relevant in multithread mode only.
        """
        self.save_bob_configuration_button.setDisabled(state)

    def handle_save_bob_configuration(self):
        """Save polymer configuraions to a file"""
        rgt.handle_save_mix_configuration(self)

    def handle_edit_bob_settings(self):
        """Open the BoB binnig settings dialog"""
        rgt.handle_edit_bob_settings(self)

    def handle_btn_prio_senio(self, checked):
        """Change do_priority_seniority"""
        # rgt.handle_btn_prio_senio(self, checked)