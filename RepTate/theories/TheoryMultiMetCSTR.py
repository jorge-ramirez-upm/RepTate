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
# Copyright (2017-2023): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module TheoryMultiMetCSTR

"""
import numpy as np
import time
from RepTate.core.CmdBase import CmdBase
from RepTate.core.Parameter import Parameter, ParameterType, OptType
from RepTate.core.Theory import Theory
from RepTate.gui.QTheory import QTheory
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication

import ctypes as ct
import RepTate.theories.react_ctypes_helper as rch
import RepTate.theories.react_gui_tools as rgt


class TheoryMultiMetCSTR(CmdBase):
    """THEORY DOCUMENTATION IS MISSING"""

    thname = "Multi-Met CSTR"
    description = "Multiple Metallocene CSTR Reaction Theory"
    citations = ["Read D.J. and Soares J.B.P., Macromolecules 2003, 36, 10037–10051"]
    doi = ["http://dx.doi.org/10.1021/ma030354l"]

    def __new__(cls, name="", parent_dataset=None, axarr=None):
        """Create an instance of the GUI"""
        return GUITheoryMultiMetCSTR(name, parent_dataset, axarr)


class BaseTheoryMultiMetCSTR:
    """Base class for both GUI"""

    html_help_file = "http://reptate.readthedocs.io/manual/Applications/React/Theory/MetalloceneCSTR.html"
    single_file = (
        True  # False if the theory can be applied to multiple files simultaneously
    )
    thname = TheoryMultiMetCSTR.thname
    citations = TheoryMultiMetCSTR.citations
    doi = TheoryMultiMetCSTR.doi

    signal_request_dist = Signal(object)
    signal_request_polymer = Signal(object)
    signal_request_arm = Signal(object)
    signal_mulmet_dialog = Signal(object)

    def __init__(self, name="", parent_dataset=None, axarr=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, axarr)
        self.reactname = "MultiMetCSTR %d" % (rch.MMCSTR_global.mulmetCSTRnumber)
        rch.MMCSTR_global.mulmetCSTRnumber += 1
        self.function = self.Calc
        self.simexists = False
        self.dist_exists = False
        self.ndist = 0
        self.has_modes = False  # True if the theory has modes
        self.autocalculate = False
        self.do_priority_seniority = False

        self.parameters["num_to_make"] = Parameter(
            name="num_to_make",
            value=1000,
            description="Number of molecules made in the simulation",
            type=ParameterType.real,
            opt_type=OptType.const,
        )
        self.parameters["mon_mass"] = Parameter(
            name="mon_mass",
            value=28,
            description="Mass, in a.m.u., of a monomer (usually set to 28 for PE)",
            type=ParameterType.real,
            opt_type=OptType.const,
        )
        self.parameters["Me"] = Parameter(
            name="Me",
            value=1000,
            description="Entanglement molecular weight",
            type=ParameterType.real,
            opt_type=OptType.const,
        )
        self.parameters["nbin"] = Parameter(
            name="nbin",
            value=50,
            description="Number of molecular weight bins",
            type=ParameterType.real,
            opt_type=OptType.const,
        )
        self.NUMCAT_MAX = 30
        # default parameters value
        self.init_param_values()

        self.signal_request_dist.connect(rgt.request_more_dist)
        self.signal_request_polymer.connect(rgt.request_more_polymer)
        self.signal_request_arm.connect(rgt.request_more_arm)
        self.signal_mulmet_dialog.connect(rgt.launch_mulmet_dialog)
        self.do_xrange("", visible=self.xrange.get_visible())

    def request_stop_computations(self):
        """Called when user wants to terminate the current computation"""
        rch.set_flag_stop_all(ct.c_bool(True))
        super().request_stop_computations()

    def set_extra_data(self, extra_data):
        """Called when loading a project, set saved parameter values"""
        self.numcat = extra_data["numcat"]
        self.time_const = extra_data["time_const"]
        self.monomer_conc = extra_data["monomer_conc"]
        self.pvalues = extra_data["pvalues"]
        rgt.set_extra_data(self, extra_data)

    def get_extra_data(self):
        """Called when saving project. Save parameters in extra_data dict"""
        self.extra_data["numcat"] = self.numcat
        self.extra_data["time_const"] = self.time_const
        self.extra_data["monomer_conc"] = self.monomer_conc
        self.extra_data["pvalues"] = self.pvalues
        rgt.get_extra_data(self)

    def init_param_values(self):
        """Initialise parameters with default values"""
        self.numcat = 2
        self.time_const = 300.0
        self.monomer_conc = 2.0

        self.pvalues = [
            ["0" for j in range(5)] for i in range(self.NUMCAT_MAX)
        ]  # initially self.numcat=2 lines of parameters
        self.pvalues[0][0] = "4e-4"  # cat conc
        self.pvalues[0][1] = "101.1"  # Kp
        self.pvalues[0][2] = "0.1"  # K=
        self.pvalues[0][3] = "0.2"  # Ks
        self.pvalues[0][4] = "5"  # KpLCB

        self.pvalues[1][0] = "1e-3"
        self.pvalues[1][1] = "90.17"
        self.pvalues[1][2] = "1.5"
        self.pvalues[1][3] = "0.3"

    def Calc(self, f=None):
        """MultiMetCSTR function that returns the square of y"""

        # get parameters
        numtomake = np.round(self.parameters["num_to_make"].value)
        monmass = self.parameters["mon_mass"].value
        Me = self.parameters["Me"].value
        nbins = int(np.round(self.parameters["nbin"].value))
        rch.set_do_prio_senio(ct.c_bool(self.do_priority_seniority))
        rch.set_flag_stop_all(ct.c_bool(False))

        c_ndist = ct.c_int()

        # resize theory datatable
        ft = f.data_table
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = 1
        tt.data = np.zeros((tt.num_rows, tt.num_columns))

        # request a dist
        if not self.dist_exists:
            success = rch.request_dist(ct.byref(c_ndist))
            self.ndist = c_ndist.value
            if not success:
                # launch dialog asking for more dist
                self.signal_request_dist.emit(
                    self
                )  # use signal to open QDialog in the main GUI window
                return
            else:
                self.dist_exists = True
        ndist = self.ndist
        # rch.react_dist[ndist].contents.name = self.reactname #TODO: set the dist name in the C library
        rch.react_dist[ndist].contents.npoly = 0
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
        self.simexists = False

        # launch form
        self.success_dialog = None
        self.signal_mulmet_dialog.emit(self)
        while self.success_dialog is None:  # wait for the end of QDialog
            time.sleep(
                0.5
            )  # TODO: find a better way to wait for the dialog thread to finish
        if not self.success_dialog:
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

        # initialise metallocene CSTR
        rch.mulmetCSTRstart(
            kp,
            kdb,
            ks,
            kplcb,
            conc,
            ct.c_double(self.time_const),
            ct.c_double(self.monomer_conc),
            ct.c_int(self.numcat),
            ct.c_int(ndist),
            ct.c_int(self.NUMCAT_MAX),
        )

        c_m = ct.c_int()

        # make numtomake polymers
        i = 0
        rate_print = np.trunc(numtomake / 20)
        self.Qprint("Making polymers:")
        self.Qprint("0% ", end="")
        while i < numtomake:
            if self.stop_theory_flag:
                self.Qprint(
                    "<br><big><font color=red><b>Polymer creation stopped by user</b></font></big>"
                )
                break
            # get a polymer
            success = rch.request_poly(ct.byref(c_m))
            m = c_m.value
            if success:  # check availability of polymers
                # put it in list
                if (
                    rch.react_dist[ndist].contents.npoly == 0
                ):  # case of first polymer made
                    rch.react_dist[ndist].contents.first_poly = m
                    rch.set_br_poly_nextpoly(
                        ct.c_int(m), ct.c_int(0)
                    )  # br_poly[m].contents.nextpoly = 0
                else:  # next polymer, put to top of list
                    rch.set_br_poly_nextpoly(
                        ct.c_int(m), ct.c_int(rch.react_dist[ndist].contents.first_poly)
                    )  # br_poly[m].contents.nextpoly = rch.react_dist[ndist].contents.first_poly
                    rch.react_dist[ndist].contents.first_poly = m

                # make a polymer
                if rch.mulmetCSTR(
                    ct.c_int(m), ct.c_int(ndist)
                ):  # routine returns false if arms ran out
                    rch.react_dist[ndist].contents.npoly += 1
                    i += 1
                    # check for error
                    if rch.MMCSTR_global.mulmetCSTRerrorflag:
                        self.Qprint(
                            "<br><big><font color=red><b>Polymers too large: gelation occurs for these parameters</b></font></big>"
                        )
                        i = numtomake
                else:  # error message if we ran out of arms
                    self.success_increase_memory = None
                    self.signal_request_arm.emit(self)
                    while (
                        self.success_increase_memory is None
                    ):  # wait for the end of QDialog
                        time.sleep(
                            0.5
                        )  # TODO: find a better way to wait for the dialog thread to finish
                    if self.success_increase_memory:
                        continue  # back to the start of while loop
                    else:
                        i = numtomake
                        rch.MMCSTR_global.mulmetCSTRerrorflag = True

                # update on number made
                if i % rate_print == 0:
                    self.Qprint("-", end="")
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
        if not rch.MMCSTR_global.mulmetCSTRerrorflag:
            self.Qprint("&nbsp;100%")

        calc = 0
        # do analysis of polymers made
        if (rch.react_dist[ndist].contents.npoly >= 100) and (
            not rch.MMCSTR_global.mulmetCSTRerrorflag
        ):
            rch.molbin(ndist)
            ft = f.data_table

            # resize theory data table
            ft = f.data_table
            tt = self.tables[f.file_name_short]
            tt.num_columns = ft.num_columns + 2
            tt.num_rows = rch.react_dist[ndist].contents.nummwdbins
            tt.data = np.zeros((tt.num_rows, tt.num_columns))

            for i in range(1, rch.react_dist[ndist].contents.nummwdbins + 1):
                tt.data[i - 1, 0] = np.power(
                    10, rch.react_dist[ndist].contents.lgmid[i]
                )
                tt.data[i - 1, 1] = rch.react_dist[ndist].contents.wt[i]
                tt.data[i - 1, 2] = rch.react_dist[ndist].contents.avg[i]
                tt.data[i - 1, 3] = rch.react_dist[ndist].contents.avbr[i]

            rch.end_print(self, ndist, self.do_priority_seniority)
            rch.prio_and_senio(self, f, ndist, self.do_priority_seniority)

            calc = rch.react_dist[ndist].contents.nummwdbins - 1
            rch.react_dist[ndist].contents.polysaved = True

        self.simexists = True
        # self.Qprint('%d arm records left in memory' % rch.pb_global.arms_left)
        return calc

    def show_theory_extras(self, checked):
        rgt.show_theory_extras(self, checked)

    def destructor(self):
        """Return arms to pool"""
        rch.return_dist(ct.c_int(self.ndist))

    def do_fit(self, line=""):
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

    def do_error(self, line):
        """This theory does not calculate the error"""
        pass



class GUITheoryMultiMetCSTR(BaseTheoryMultiMetCSTR, QTheory):
    """GUI Version"""

    def __init__(self, name="", parent_dataset=None, axarr=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, axarr)
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
