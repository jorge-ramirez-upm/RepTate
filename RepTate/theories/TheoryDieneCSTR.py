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
"""Module TheoryDieneCSTR

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


class TheoryDieneCSTR(CmdBase):
    """DieneCSTR reaction theory
    """
    thname = 'Diene CSTR'
    description = 'The Diene CSTR reaction theory'
    citations = ['Das C. et al., Macromol. Theory Simul., 26, 1700006 (2017)']
    doi = ["https://doi.org/10.1002/mats.201700006"]

    def __new__(cls, name='', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUITheoryDieneCSTR(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryDieneCSTR(
                name, parent_dataset, ax)


class BaseTheoryDieneCSTR:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/React/Theory/dieneCSTR.html'
    single_file = True  # False if the theory can be applied to multiple files simultaneously
    thname = TheoryDieneCSTR.thname
    citations = TheoryDieneCSTR.citations
    doi = TheoryDieneCSTR.doi
    signal_request_dist = pyqtSignal(object)
    signal_request_polymer = pyqtSignal(object)
    signal_request_arm = pyqtSignal(object)

    def __init__(self, name='', parent_dataset=None, ax=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.reactname = "Diene CSTR %d" % (rch.dCSTR_global.dieneCSTRnumber)
        rch.dCSTR_global.dieneCSTRnumber += 1
        self.function = self.Calc
        self.simexists = False
        self.dist_exists = False
        self.ndist = 0
        self.has_modes = False  # True if the theory has modes
        self.autocalculate = False
        self.do_priority_seniority = False
        self.M_diene = 138

        self.parameters['col_time'] = Parameter(
            name='col_time',
            value=1e3,
            min_value=0,
            description='Collection time',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['tau'] = Parameter(
            name='tau',
            value=200,
            description='Reactor time constant',
            type=ParameterType.real,
            min_value=0,
            opt_type=OptType.const)
        self.parameters['D0'] = Parameter(
            name='D0',
            value=1e-4,
            min_value=0,
            description='Rate of diene feed to the reactor',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['C0'] = Parameter(
            name='C0',
            value=2e-3,
            min_value=0,
            description='Rate of catalyst feed to the reactor',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['kpM'] = Parameter(
            name='kpM',
            value=150,
            min_value=0,
            description='Polymerisation rate times Monomer conc.',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['k='] = Parameter(
            name='k=',
            value=0.2,
            min_value=0,
            description='Rate of termination leaving double bond behind',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['ks'] = Parameter(
            name='ks',
            value=0.005,
            min_value=0,
            description='Rate of termination leaving saturated chain behind',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['kpD'] = Parameter(
            name='kpD',
            value=30,
            min_value=0,
            description='Rate of free-diene incorporation',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['kDLCB'] = Parameter(
            name='kDLCB',
            value=0.2,
            min_value=0,
            description='Rate of long-chain branching by addition of a pendant diene',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['kpLCB'] = Parameter(
            name='kpLCB',
            value=1,
            min_value=0,
            description='Rate of long-chain branching by macromer incorporation',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['num_to_make'] = Parameter(
            name='num_to_make',
            value=1000,
            min_value=0,
            description='Number of molecules made in the simulation',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['mon_mass'] = Parameter(
            name='mon_mass',
            value=28,
            min_value=0,
            description=
            'Mass, in a.m.u., of a monomer (usually set to 28 for PE)',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['Me'] = Parameter(
            name='Me',
            value=1000,
            min_value=0,
            description='Entanglement molecular weight',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['nbin'] = Parameter(
            name='nbin',
            value=100,
            min_value=1,
            description='Number of molecular weight bins',
            type=ParameterType.real,
            opt_type=OptType.const)

        self.signal_request_dist.connect(rgt.request_more_dist)
        self.signal_request_polymer.connect(rgt.request_more_polymer)
        self.signal_request_arm.connect(rgt.request_more_arm)
        self.do_xrange('', visible=self.xrange.get_visible())

    def request_stop_computations(self):
        """Called when user wants to terminate the current computation"""
        rch.set_flag_stop_all(ct.c_bool(True))
        super().request_stop_computations()

    def do_error(self, line):
        pass

    def Calc(self, f=None):
        """Template function that returns the square of y
        
        [description]
        
        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """

        # get parameters
        col_time = self.parameters['col_time'].value
        tau = self.parameters['tau'].value
        kpM = self.parameters['kpM'].value
        kDLCB = self.parameters['kDLCB'].value
        kpLCB = self.parameters['kpLCB'].value
        kpD = self.parameters['kpD'].value
        keq = self.parameters['k='].value
        ks = self.parameters['ks'].value
        D0 = self.parameters['D0'].value
        C0 = self.parameters['C0'].value
        numtomake = np.round(self.parameters['num_to_make'].value)
        monmass = self.parameters['mon_mass'].value
        Me = self.parameters['Me'].value
        nbins = int(np.round(self.parameters['nbin'].value))
        rch.set_do_prio_senio(ct.c_bool(self.do_priority_seniority))
        rch.set_flag_stop_all(ct.c_bool(False))

        c_ndist = ct.c_int()

        #resize theory datatable
        ft = f.data_table
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = 1
        tt.data = np.zeros((tt.num_rows, tt.num_columns))

        if not self.dist_exists:
            success = rch.request_dist(ct.byref(c_ndist))
            self.ndist = c_ndist.value
            if not success:
                #launch dialog asking for more dist
                self.signal_request_dist.emit(
                    self)  #use signal to open QDialog in the main GUI window
                return
            else:
                self.dist_exists = True
        ndist = self.ndist
        # rch.react_dist[ndist].contents.name = self.reactname #TODO: set the dist name in the C library
        rch.react_dist[ndist].contents.M_e = Me
        rch.react_dist[ndist].contents.monmass = monmass
        rch.react_dist[ndist].contents.nummwdbins = nbins
        rch.react_dist[ndist].contents.polysaved = False
        rch.react_dist[ndist].contents.nsaved_arch = 0
        rch.react_dist[ndist].contents.arch_minwt = self.xmin
        rch.react_dist[ndist].contents.arch_maxwt = self.xmax
        rch.init_bin_prio_vs_senio(ndist)

        if self.simexists:
            rch.return_dist_polys(ct.c_int(ndist))

        # initialise diene batch
        ldiene = self.M_diene / monmass
        rch.dieneCSTRstart(ct.c_double(tau), ct.c_double(kpM), ct.c_double(kDLCB), ct.c_double(kpLCB), ct.c_double(kpD), ct.c_double(keq), ct.c_double(ks), ct.c_double(D0), ct.c_double(C0), ct.c_double(ldiene), ct.c_double(col_time), ct.c_int(ndist))
        rch.react_dist[ndist].contents.npoly = 0

        c_m = ct.c_int()

        # make numtomake polymers
        i = 0
        n_gel = 0
        rate_print = np.trunc(numtomake / 20)
        self.Qprint('Making polymers:')
        self.Qprint('0% ', end='')
        while i < numtomake:
            if self.stop_theory_flag:
                self.Qprint('<br><big><font color=red><b>Polymer creation stopped by user</b></font></big>')
                break
            # get a polymer
            success = rch.request_poly(ct.byref(c_m))
            m = c_m.value
            if success:  # check availability of polymers
                # put it in list
                # case of first polymer made
                if rch.react_dist[ndist].contents.npoly == 0:
                    rch.react_dist[ndist].contents.first_poly = m
                    #br_poly[m].contents.nextpoly = 0
                    rch.set_br_poly_nextpoly(ct.c_int(m), ct.c_int(0))
                else:  # next polymer, put to top of list
                    #br_poly[m].contents.nextpoly = rch.react_dist[ndist].contents.first_poly
                    rch.set_br_poly_nextpoly(
                        ct.c_int(m),
                        ct.c_int(rch.react_dist[ndist].contents.first_poly))
                    rch.react_dist[ndist].contents.first_poly = m

                # make a polymer
                # routine returns false if arms ran out
                if rch.dieneCSTR(ct.c_int(m), ct.c_int(ndist)):
                    rch.react_dist[ndist].contents.npoly += 1
                    i += 1
                    # check for error
                    if rch.dCSTR_global.dieneCSTRerrorflag:
                        n_gel += 1
                        rch.dCSTR_global.dieneCSTRerrorflag = False
                        # self.Qprint(
                        #     '<br><big><font color=red><b>Polymers too large: gelation occurs for these parameters</b></font></big>'
                        # )
                        # i = numtomake
                else:  # error message if we ran out of arms
                    self.success_increase_memory = None
                    self.signal_request_arm.emit(self)
                    # wait for the end of QDialog
                    while self.success_increase_memory is None:
                        # TODO: find a better way to wait for the dialog thread to finish
                        time.sleep(0.5)
                    if self.success_increase_memory:
                        continue  # back to the start of while loop
                    else:
                        i = numtomake
                        rch.dCSTR_global.dieneCSTRerrorflag = True

                # update on number made
                if i % rate_print == 0:
                    self.Qprint('-', end='')
                    # needed to use Qprint if in single-thread
                    QApplication.processEvents()  

            else:  # polymer wasn't available
                self.success_increase_memory = None
                self.signal_request_polymer.emit(self)
                while self.success_increase_memory is None:
                    # TODO: find a better way to wait for the dialog thread to finish
                    time.sleep(0.5)
                if self.success_increase_memory:
                    continue
                else:
                    i = numtomake
        # end make polymers loop
        if not rch.dCSTR_global.dieneCSTRerrorflag:
            self.Qprint('&nbsp;100%')

        calc = 0
        # do analysis of polymers made
        if (rch.react_dist[ndist].contents.npoly):
            rch.molbin(ndist)
            ft = f.data_table

            #resize theory data table
            ft = f.data_table
            tt = self.tables[f.file_name_short]
            tt.num_columns = ft.num_columns + 2
            tt.num_rows = rch.react_dist[ndist].contents.nummwdbins
            tt.data = np.zeros((tt.num_rows, tt.num_columns))

            for i in range(1, rch.react_dist[ndist].contents.nummwdbins + 1):
                tt.data[i - 1, 0] = np.power(
                    10, rch.react_dist[ndist].contents.lgmid[i])
                tt.data[i - 1, 1] = rch.react_dist[ndist].contents.wt[i]
                tt.data[i - 1, 2] = rch.react_dist[ndist].contents.avg[i]
                tt.data[i - 1, 3] = rch.react_dist[ndist].contents.avbr[i]
            rch.end_print(self, ndist, self.do_priority_seniority)
            rch.prio_and_senio(self, f, ndist, self.do_priority_seniority)

            calc = rch.react_dist[ndist].contents.nummwdbins - 1
            rch.react_dist[ndist].contents.polysaved = True
        self.simexists = True
        if n_gel != 0:
            self.Qprint('<br><big><font color=red><b>Gelation might occurs for these parameters.<br>%.3g%% of the molecules exceeded the maximum recursion level</b></font></big>' % (n_gel/numtomake*100.0))    
        return calc
    
    def show_theory_extras(self, checked):
        rgt.show_theory_extras(self, checked)

    def destructor(self):
        """Return arms to pool"""
        rch.return_dist(ct.c_int(self.ndist))
    def do_fit(self, line=''):
        """No fitting allowed in this theory"""
        if self.xrange.get_visible():
            if self.xmin > self.xmax:
                temp = self.xmin
                self.xmin = self.xmax
                self.xmax = temp
            self.Qprint("<b>xrange</b>=[%0.3g, %0.3g]" % (self.xmin,
                                                          self.xmax))
        if self.yrange.get_visible():
            if self.ymin > self.ymax:
                temp = self.ymin
                self.ymin = self.ymax
                self.ymax = temp
            self.Qprint("<b>yrange</b>=[%.03g, %0.3g]" % (self.ymin,
                                                          self.ymax))


class CLTheoryDieneCSTR(BaseTheoryDieneCSTR, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_dataset=None, ax=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)

    # This class usually stays empty


class GUITheoryDieneCSTR(BaseTheoryDieneCSTR, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_dataset=None, ax=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        rgt.initialise_tool_bar(self)

    def theory_buttons_disabled(self, state):
        """Disable/Enable some theory buttons before/after calculation start."""
        rgt.theory_buttons_disabled(self, state)

    def handle_save_bob_configuration(self):
        """Save polymer configuraions to a file"""
        rgt.handle_save_bob_configuration(self)

    def handle_edit_bob_settings(self):
        """Open the BoB binnig settings dialog"""
        rgt.handle_edit_bob_settings(self)

    def handle_btn_prio_senio(self, checked):
        """Change do_priority_seniority"""
        rgt.handle_btn_prio_senio(self, checked)
    def set_extra_data(self, extra_data):
        """set extra data"""
        rgt.set_extra_data(self, extra_data)

    def get_extra_data(self):
        """set extra data"""
        rgt.get_extra_data(self)