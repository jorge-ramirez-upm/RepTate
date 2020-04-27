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
"""Module TheoryTobitaCSTR

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


class TheoryTobitaCSTR(CmdBase):
    """LDPE CSTR reaction theory
    
    The LDPE CSTR reaction theory uses an algorithm based on the one described in
the paper by H. Tobita (J. Pol. Sci. Part B, 39, 391-403 (2001)) for batch
reactions. The algorithm is based upon a set of processes occuring in the
reactor during free-radical polymerisation.
    
    [description]
    """
    thname = 'Tobita CSTR'
    description = 'Tobita LDPE CSTR reaction theory'
    citations = ['Tobita H., J. Pol. Sci. Part B 2001, 39, 391-403']
    doi = ["http://dx.doi.org/10.1002/1099-0488(20010115)39:4<391::AID-POLB1011>3.0.CO;2-3"]

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
        return GUITheoryTobitaCSTR(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryTobitaCSTR(
                name, parent_dataset, ax)


class BaseTheoryTobitaCSTR:
    """[summary]
    
    [description]
    """
    # help_file = 'docs%sbuild%shtml%smanual%sTheories%sReact%stobitaCSTR.html' % ((os.sep, )*6)
    help_file = 'http://reptate.readthedocs.io/manual/Applications/React/Theory/tobitaCSTR.html'
    single_file = True  # False if the theory can be applied to multiple files simultaneously
    thname = TheoryTobitaCSTR.thname
    citations = TheoryTobitaCSTR.citations
    doi = TheoryTobitaCSTR.doi
    
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
        self.reactname = "LDPE CSTR %d" % (rch.tCSTR_global.tobCSTRnumber)
        rch.tCSTR_global.tobCSTRnumber += 1
        self.function = self.Calc
        self.simexists = False
        self.dist_exists = False
        self.ndist = 0
        self.has_modes = False  # True if the theory has modes
        self.autocalculate = False
        self.do_priority_seniority = False

        self.parameters['tau'] = Parameter(
            name='tau',
            value=1.11e-3,
            description='Ratio (term. by dispropor. + chain transf. to small mol.) to polym. rates',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['beta'] = Parameter(
            name='beta',
            value=9.75e-6,
            description='Ratio term. by combin. to polym. rates',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['lambda'] = Parameter(
            name='lambda',
            value=2e-3,
            description='Ratio long-chain-branch. to polym. rates',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['sigma'] = Parameter(
            name='sigma',
            value=1.8e-4,
            description='Ratio scission to polym. rates',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['num_to_make'] = Parameter(
            name='num_to_make',
            value=1000,
            description='Number of molecules made in the simulation',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['mon_mass'] = Parameter(
            name='mon_mass',
            value=28,
            description=
            'Mass, in a.m.u., of a monomer (usually set to 28 for PE)',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['Me'] = Parameter(
            name='Me',
            value=1000,
            description='Entanglement molecular weight',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['nbin'] = Parameter(
            name='nbin',
            value=100,
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
        tau = self.parameters['tau'].value
        beta = self.parameters['beta'].value
        lambda_ = self.parameters['lambda'].value
        sigma = self.parameters['sigma'].value
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

        # initialise tobita batch
        rch.tobCSTRstart(
            ct.c_double(tau), ct.c_double(beta), ct.c_double(sigma),
            ct.c_double(lambda_), ct.c_int(ndist))
        rch.react_dist[ndist].contents.npoly = 0

        c_m = ct.c_int()

        # make numtomake polymers
        i = 0
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
                if rch.react_dist[
                        ndist].contents.npoly == 0:  # case of first polymer made
                    rch.react_dist[ndist].contents.first_poly = m
                    rch.set_br_poly_nextpoly(
                        ct.c_int(m),
                        ct.c_int(0))  #br_poly[m].contents.nextpoly = 0
                else:  # next polymer, put to top of list
                    rch.set_br_poly_nextpoly(
                        ct.c_int(m),
                        ct.c_int(rch.react_dist[ndist].contents.first_poly)
                    )  #br_poly[m].contents.nextpoly = rch.react_dist[ndist].contents.first_poly
                    rch.react_dist[ndist].contents.first_poly = m

                # make a polymer
                if rch.tobCSTR(ct.c_int(m), ct.c_int(
                        ndist)):  # routine returns false if arms ran out
                    rch.react_dist[ndist].contents.npoly += 1
                    i += 1
                    # check for error
                    if rch.tCSTR_global.tobitaCSTRerrorflag:
                        self.Qprint(
                            '<br><big><font color=red><b>Polymers too large: gelation occurs for these parameters</b></font></big>'
                        )
                        i = numtomake
                else:  # error message if we ran out of arms
                    self.success_increase_memory = None
                    self.signal_request_arm.emit(self)
                    while self.success_increase_memory is None:  # wait for the end of QDialog
                        time.sleep(
                            0.5
                        )  # TODO: find a better way to wait for the dialog thread to finish
                    if self.success_increase_memory:
                        continue  # back to the start of while loop
                    else:
                        i = numtomake
                        rch.tCSTR_global.tobitaCSTRerrorflag = True

                # update on number made
                if i % rate_print == 0:
                    self.Qprint('-', end='')
                    # needed to use Qprint if in single-thread
                    QApplication.processEvents()  

            else:  # polymer wasn't available
                self.success_increase_memory = None
                self.signal_request_polymer.emit(self)
                while self.success_increase_memory is None:
                    time.sleep(
                        0.5
                    )  # TODO: find a better way to wait for the dialog thread to finish
                if self.success_increase_memory:
                    continue
                else:
                    i = numtomake
        # end make polymers loop
        if not rch.tCSTR_global.tobitaCSTRerrorflag:
            self.Qprint('&nbsp;100%')

        calc = 0
        # do analysis of polymers made
        if (rch.react_dist[ndist].contents.npoly >=
                100) and (not rch.tCSTR_global.tobitaCSTRerrorflag):
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
        # self.Qprint('%d arm records left in memory' % rch.pb_global.arms_left)
        # rch.print_arch_stats(ct.c_int(ndist))
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
            self.Qprint("<b>xrange</b>=[%0.3g, %0.3g]" % (self.xmin, self.xmax))
        if self.yrange.get_visible():
            if self.ymin > self.ymax:
                temp = self.ymin
                self.ymin = self.ymax
                self.ymax = temp
            self.Qprint("<b>yrange</b>=[%.03g, %0.3g]" % (self.ymin, self.ymax))

class CLTheoryTobitaCSTR(BaseTheoryTobitaCSTR, Theory):
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


class GUITheoryTobitaCSTR(BaseTheoryTobitaCSTR, QTheory):
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