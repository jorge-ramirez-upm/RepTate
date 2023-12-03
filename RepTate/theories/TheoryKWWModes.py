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
"""Module TheoryKWWModes

Module that defines theories related to Havriliak-Negami modes, in the frequency and time domains.

"""
import numpy as np
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.DataTable import DataTable
from RepTate.core.Parameter import Parameter, ParameterType, OptType
from RepTate.core.Theory import Theory
from RepTate.gui.QTheory import QTheory
from PySide6.QtWidgets import QToolBar, QSpinBox
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from RepTate.core.DraggableArtists import DragType, DraggableModesSeries

from RepTate.theories.kww_ctypes_helper import kwwc, kwws


class TheoryKWWModesFrequency(CmdBase):
    """Fit a Kohlrausch-Williams-Watts (KWW, stretched exponential) model to a frequency dependent relaxation function. 
    
    * **Function**
        .. math::
            \\epsilon (t) - \\epsilon_\\infty =  \\Delta\\epsilon \\left[ 1 - \\exp \\left( - \\frac{t}{\\tau} \\right)^\\beta\\right]
    
    * **Parameters**
       - einf = :math:`\\epsilon_{\\infty}`: Unrelaxed permitivity
       - :math:`n_{modes}`: number of Havriliak-Negami modes equally distributed in logarithmic scale between :math:`\\omega_{min}` and :math:`\\omega_{max}`.
       - logwmin = :math:`\\log(\\omega_{min})`: decimal logarithm of the minimum frequency.
       - logwmax = :math:`\\log(\\omega_{max})`: decimal logarithm of the maximum frequency.
       - logDei = :math:`\\log(\\Delta\\epsilon_{i})`, where :math:`\\Delta\\epsilon_{i}=\\epsilon_{s,i}-\\epsilon_\\infty`: decimal logarithm of the relaxation strength of Debye mode :math:`i`, where :math:`\\epsilon_{s,i}` is the static permitivity of mode :math:`i`.
       - :math:`\\beta`: stretched exponential parameter
       
    .. note::
        It makes use of the libkww code, by Joachim Wuttke, CITE: doi:10.3390/a5040604
    
    """

    thname = "KWW modes"
    description = "Fit Kohlrausch-Williams-Watts modes"
    citations = [
        "Kohlrausch, R. Annalen der Physik und Chemie 1854, 91, 56-82",
        "Williams G. and Watts D.C., Trans. Faraday Soc. 1970, 66, 80-85",
    ]
    doi = [
        "http://dx.doi.org/10.1002/andp.18541670203",
        "http://dx.doi.org/10.1039/TF9706600080",
    ]

    def __new__(cls, name="", parent_dataset=None, ax=None):
        """Create an instance of the GUI or CL class"""
        return (
            GUITheoryKWWModesFrequency(name, parent_dataset, ax)
            if (CmdBase.mode == CmdMode.GUI)
            else CLTheoryKWWModesFrequency(name, parent_dataset, ax)
        )


class BaseTheoryKWWModesFrequency:
    """Base class for both GUI and CL"""

    html_help_file = "http://reptate.readthedocs.io/manual/Applications/Dielectric/Theory/theory.html#kolhrauch-williams-watts-kww-modes"
    single_file = True
    thname = TheoryKWWModesFrequency.thname
    citations = TheoryKWWModesFrequency.citations
    doi = TheoryKWWModesFrequency.doi

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)
        self.function = self.KWWModesFrequency
        self.has_modes = False
        self.MAX_MODES = 40
        self.view_modes = True
        wmin = self.parent_dataset.minpositivecol(0)
        wmax = self.parent_dataset.maxcol(0)
        nmodes = int(np.round(np.log10(wmax / wmin)))

        self.parameters["einf"] = Parameter(
            "einf",
            0.0,
            "Unrelaxed permittivity",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0,
        )
        self.parameters["beta"] = Parameter(
            "beta",
            0.5,
            "Stretched exponential parameter",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0.1,
            max_value=2.0,
        )
        self.parameters["logwmin"] = Parameter(
            "logwmin",
            np.log10(wmin),
            "Log of frequency range minimum",
            ParameterType.real,
            opt_type=OptType.opt,
        )
        self.parameters["logwmax"] = Parameter(
            "logwmax",
            np.log10(wmax),
            "Log of frequency range maximum",
            ParameterType.real,
            opt_type=OptType.opt,
        )
        self.parameters["nmodes"] = Parameter(
            name="nmodes",
            value=nmodes,
            description="Number of KWW modes",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False,
        )
        # Interpolate modes from data
        w = np.logspace(np.log10(wmin), np.log10(wmax), nmodes)
        eps = np.abs(
            np.interp(
                w,
                self.parent_dataset.files[0].data_table.data[:, 0],
                self.parent_dataset.files[0].data_table.data[:, 1],
            )
        )
        for i in range(self.parameters["nmodes"].value):
            self.parameters["logDe%02d" % i] = Parameter(
                "logDe%02d" % i,
                np.log10(eps[i]),
                "Log of Mode %d amplitude" % i,
                ParameterType.real,
                opt_type=OptType.opt,
            )

        # GRAPHIC MODES
        self.graphicmodes = []
        self.artistmodes = []
        self.setup_graphic_modes()

    def drag_mode(self, dx, dy):
        """Drag modes"""
        nmodes = self.parameters["nmodes"].value
        if self.parent_dataset.parent_application.current_view.log_x:
            self.set_param_value("logwmin", np.log10(dx[0]))
            self.set_param_value("logwmax", np.log10(dx[nmodes - 1]))
        else:
            self.set_param_value("logwmin", dx[0])
            self.set_param_value("logwmax", dx[nmodes - 1])

        if self.parent_dataset.parent_application.current_view.log_y:
            for i in range(nmodes):
                self.set_param_value("logDe%02d" % i, np.log10(dy[i]))
        else:
            for i in range(nmodes):
                self.set_param_value("logDe%02d" % i, dy[i])

        self.do_calculate("")
        self.update_parameter_table()

    def update_modes(self):
        """Do nothing"""
        pass

    def setup_graphic_modes(self):
        """Setup graphical helpers"""
        nmodes = self.parameters["nmodes"].value
        w = np.logspace(
            self.parameters["logwmin"].value, self.parameters["logwmax"].value, nmodes
        )
        eps = np.zeros(nmodes)
        for i in range(nmodes):
            eps[i] = np.power(10, self.parameters["logDe%02d" % i].value)

        self.graphicmodes = self.ax.plot(w, eps)[0]
        self.graphicmodes.set_marker("D")
        self.graphicmodes.set_linestyle("")
        self.graphicmodes.set_visible(self.view_modes)
        self.graphicmodes.set_markerfacecolor("yellow")
        self.graphicmodes.set_markeredgecolor("black")
        self.graphicmodes.set_markeredgewidth(3)
        self.graphicmodes.set_markersize(8)
        self.graphicmodes.set_alpha(0.5)
        self.artistmodes = DraggableModesSeries(
            self.graphicmodes,
            DragType.special,
            self.parent_dataset.parent_application,
            self.drag_mode,
        )
        self.plot_theory_stuff()

    def destructor(self):
        """Called when the theory tab is closed"""
        self.graphicmodes_visible(False)
        self.ax.lines.remove(self.graphicmodes)

    def show_theory_extras(self, show=False):
        """Called when the active theory is changed"""
        if CmdBase.mode == CmdMode.GUI:
            self.Qhide_theory_extras(show)
        self.graphicmodes_visible(show)

    def graphicmodes_visible(self, state):
        """Change visibility of modes"""
        self.view_modes = state
        self.graphicmodes.set_visible(self.view_modes)
        if self.view_modes:
            self.artistmodes.connect()
        else:
            self.artistmodes.disconnect()
        # self.do_calculate("")
        self.parent_dataset.parent_application.update_plot()

    def get_modes(self):
        """Get the values of Maxwell Modes from this theory"""
        nmodes = self.parameters["nmodes"].value
        freq = np.logspace(
            self.parameters["logwmin"].value, self.parameters["logwmax"].value, nmodes
        )
        tau = 1.0 / freq
        eps = np.zeros(nmodes)
        for i in range(nmodes):
            eps[i] = np.power(10, self.parameters["logDe%02d" % i].value)
        return tau, eps, True

    def KWWModesFrequency(self, f=None):
        """Calculate theory"""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        einf = self.parameters["einf"].value
        beta = self.parameters["beta"].value
        nmodes = self.parameters["nmodes"].value
        freq = np.logspace(
            self.parameters["logwmin"].value, self.parameters["logwmax"].value, nmodes
        )
        tau = 1.0 / freq

        tt.data[:, 1] += einf
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            eps = np.power(10, self.parameters["logDe%02d" % i].value)
            for j, w in enumerate(tt.data[:, 0]):
                tt.data[j, 1] += eps * kwwc(w * tau[i], beta)
                tt.data[j, 2] += eps * kwws(w * tau[i], beta)

    def plot_theory_stuff(self):
        """Plot theory helpers"""
        # if not self.view_modes:
        #     return
        data_table_tmp = DataTable(self.axarr)
        data_table_tmp.num_columns = 3
        nmodes = self.parameters["nmodes"].value
        data_table_tmp.num_rows = nmodes
        data_table_tmp.data = np.zeros((nmodes, 3))
        freq = np.logspace(
            self.parameters["logwmin"].value, self.parameters["logwmax"].value, nmodes
        )
        data_table_tmp.data[:, 0] = freq
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            data_table_tmp.data[i, 1] = data_table_tmp.data[i, 2] = np.power(
                10, self.parameters["logDe%02d" % i].value
            )
        view = self.parent_dataset.parent_application.current_view
        try:
            x, y, success = view.view_proc(data_table_tmp, None)
        except TypeError as e:
            print(e)
            return
        self.graphicmodes.set_data(x, y)
        for i in range(data_table_tmp.MAX_NUM_SERIES):
            for nx in range(len(self.axarr)):
                self.axarr[nx].lines.remove(data_table_tmp.series[nx][i])


class CLTheoryKWWModesFrequency(BaseTheoryKWWModesFrequency, Theory):
    """CL Version"""

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)


class GUITheoryKWWModesFrequency(BaseTheoryKWWModesFrequency, QTheory):
    """GUI Version"""

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, self.MAX_MODES)  # min and max number of modes
        self.spinbox.setSuffix(" modes")
        self.spinbox.setValue(self.parameters["nmodes"].value)  # initial value
        tb.addWidget(self.spinbox)
        self.modesaction = tb.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-visible.png"), "View modes"
        )
        self.modesaction.setCheckable(True)
        self.modesaction.setChecked(True)
        self.thToolsLayout.insertWidget(0, tb)

        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged
        )
        connection_id = self.modesaction.triggered.connect(self.modesaction_change)

    def Qhide_theory_extras(self, state):
        """Uncheck the modeaction button. Called when curent theory is changed"""
        self.modesaction.setChecked(state)

    def modesaction_change(self, checked):
        """Change mode visibility"""
        self.graphicmodes_visible(checked)
        # self.view_modes = self.modesaction.isChecked()
        # self.graphicmodes.set_visible(self.view_modes)
        # self.do_calculate("")

    def handle_spinboxValueChanged(self, value):
        """Handle a change of the parameter 'nmode'"""
        nmodesold = self.parameters["nmodes"].value
        wminold = self.parameters["logwmin"].value
        wmaxold = self.parameters["logwmax"].value
        wold = np.logspace(wminold, wmaxold, nmodesold)
        Gold = np.zeros(nmodesold)
        for i in range(nmodesold):
            Gold[i] = self.parameters["logDe%02d" % i].value
            del self.parameters["logDe%02d" % i]

        nmodesnew = value
        self.set_param_value("nmodes", nmodesnew)
        wnew = np.logspace(wminold, wmaxold, nmodesnew)

        Gnew = np.interp(wnew, wold, Gold)

        for i in range(nmodesnew):
            self.parameters["logDe%02d" % i] = Parameter(
                "logDe%02d" % i,
                Gnew[i],
                "Log of Mode %d amplitude" % i,
                ParameterType.real,
                opt_type=OptType.opt,
            )

        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()
        self.update_parameter_table()
