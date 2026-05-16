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
# Copyright (2017-2026): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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

from typing import Any, ClassVar

import numpy as np
from RepTate.core.DataTable import DataTable
from RepTate.core.Parameter import Parameter, ParameterType, OptType
from RepTate.core.typing import AxesArray, FileLike
from RepTate.gui.QTheory import QTheory
from PySide6.QtWidgets import QToolBar, QSpinBox
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from RepTate.core.DraggableArtists import DragType, DraggableModesSeries

from RepTate.theories.kww_ctypes_helper import kwwc, kwws


def _logspace(start: Any, stop: Any, num: Any) -> Any:
    return np.logspace(start, stop, num)


class TheoryKWWModesFrequency(QTheory):
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

    thname: ClassVar[str] = "KWW modes"
    description: ClassVar[str] = "Fit Kohlrausch-Williams-Watts modes"
    citations: ClassVar[list[str]] = [
        "Kohlrausch, R. Annalen der Physik und Chemie 1854, 91, 56-82",
        "Williams G. and Watts D.C., Trans. Faraday Soc. 1970, 66, 80-85",
    ]
    doi: ClassVar[list[str]] = [
        "http://dx.doi.org/10.1002/andp.18541670203",
        "http://dx.doi.org/10.1039/TF9706600080",
    ]
    html_help_file: ClassVar[str] = (
        "http://reptate.readthedocs.io/manual/Applications/Dielectric/Theory/theory.html#kolhrauch-williams-watts-kww-modes"
    )
    single_file: ClassVar[bool] = True

    def __init__(self, name: str = "", parent_dataset: Any = None, ax: AxesArray | None = None) -> None:
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
            name="einf",
            value=0.0,
            description="Unrelaxed permittivity",
            type=ParameterType.real,
            opt_type=OptType.opt,
            min_value=0,
        )
        self.parameters["beta"] = Parameter(
            name="beta",
            value=0.5,
            description="Stretched exponential parameter",
            type=ParameterType.real,
            opt_type=OptType.opt,
            min_value=0.1,
            max_value=2.0,
        )
        self.parameters["logwmin"] = Parameter(
            name="logwmin",
            value=np.log10(wmin),
            description="log10(wmin) of frequency range minimum expressed in rad/s",
            type=ParameterType.real,
            opt_type=OptType.opt,
        )
        self.parameters["logwmax"] = Parameter(
            name="logwmax",
            value=np.log10(wmax),
            description="log10(wmax) of frequency range maximum expressed in rad/s",
            type=ParameterType.real,
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
        w = _logspace(np.log10(wmin), np.log10(wmax), nmodes)
        eps = np.abs(
            np.interp(
                w,
                self.parent_dataset.files[0].data_table.data[:, 0],
                self.parent_dataset.files[0].data_table.data[:, 1],
            )
        )
        nmodes_value: Any = self.parameters["nmodes"].value
        for i in range(nmodes_value):
            self.parameters["logDe%02d" % i] = Parameter(
                name="logDe%02d" % i,
                value=np.log10(eps[i]),
                description="Log of Mode %d amplitude" % i,
                type=ParameterType.real,
                opt_type=OptType.opt,
            )

        # GRAPHIC MODES
        self.graphicmodes: Any = []
        self.artistmodes: Any = []
        self.setup_graphic_modes()

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, self.MAX_MODES)  # min and max number of modes
        self.spinbox.setSuffix(" modes")
        self.spinbox.setValue(nmodes_value)  # initial value
        tb.addWidget(self.spinbox)
        self.modesaction = tb.addAction(QIcon(":/Icon8/Images/new_icons/icons8-visible.png"), "View modes")
        self.modesaction.setCheckable(True)
        self.modesaction.setChecked(True)
        self.thToolsLayout.insertWidget(0, tb)

        self.spinbox.valueChanged.connect(self.handle_spinboxValueChanged)
        self.modesaction.triggered.connect(self.modesaction_change)

    def Qhide_theory_extras(self, state: bool) -> None:
        """Uncheck the modeaction button. Called when curent theory is changed"""
        self.modesaction.setChecked(state)

    def modesaction_change(self, checked: bool) -> None:
        """Change mode visibility"""
        self.graphicmodes_visible(checked)
        # self.view_modes = self.modesaction.isChecked()
        # self.graphicmodes.set_visible(self.view_modes)
        # self.do_calculate("")

    def handle_spinboxValueChanged(self, value: int) -> None:
        """Handle a change of the parameter 'nmode'"""
        nmodesold: Any = self.parameters["nmodes"].value
        wminold: Any = self.parameters["logwmin"].value
        wmaxold: Any = self.parameters["logwmax"].value
        wold = _logspace(wminold, wmaxold, nmodesold)
        Gold = np.zeros(nmodesold)
        for i in range(nmodesold):
            Gold[i] = self.parameters["logDe%02d" % i].value
            del self.parameters["logDe%02d" % i]

        nmodesnew = value
        self.set_param_value("nmodes", nmodesnew)
        wnew = _logspace(wminold, wmaxold, nmodesnew)

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

    def drag_mode(self, dx: Any, dy: Any) -> None:
        """Drag modes"""
        dx, dy = self.convert_view_data_to_internal(dx, dy)
        nmodes: Any = self.parameters["nmodes"].value
        if self.current_view().log_x:
            self.set_param_value("logwmin", np.log10(dx[0]))
            self.set_param_value("logwmax", np.log10(dx[nmodes - 1]))
        else:
            self.set_param_value("logwmin", dx[0])
            self.set_param_value("logwmax", dx[nmodes - 1])

        if self.current_view().log_y:
            for i in range(nmodes):
                self.set_param_value("logDe%02d" % i, np.log10(dy[i]))
        else:
            for i in range(nmodes):
                self.set_param_value("logDe%02d" % i, dy[i])

        self.do_calculate("")
        self.update_parameter_table()

    def update_modes(self) -> None:
        """Do nothing"""
        pass

    def setup_graphic_modes(self) -> None:
        """Setup graphical helpers"""
        nmodes: Any = self.parameters["nmodes"].value
        logwmin: Any = self.parameters["logwmin"].value
        logwmax: Any = self.parameters["logwmax"].value
        w = _logspace(logwmin, logwmax, nmodes)
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

    def destructor(self) -> None:
        """Called when the theory tab is closed"""
        self.graphicmodes_visible(False)
        # self.ax.lines.remove(self.graphicmodes)
        self.graphicmodes.remove()

    def show_theory_extras(self, show: bool = False) -> None:
        """Called when the active theory is changed"""
        self.Qhide_theory_extras(show)
        self.graphicmodes_visible(show)

    def graphicmodes_visible(self, state: bool) -> None:
        """Change visibility of modes"""
        self.view_modes = state
        self.graphicmodes.set_visible(self.view_modes)
        if self.view_modes:
            self.artistmodes.connect()
        else:
            self.artistmodes.disconnect()
        # self.do_calculate("")
        self.parent_dataset.parent_application.update_plot()

    def get_modes(self) -> tuple[Any, Any, bool]:
        """Get the values of Maxwell Modes from this theory"""
        nmodes: Any = self.parameters["nmodes"].value
        logwmin: Any = self.parameters["logwmin"].value
        logwmax: Any = self.parameters["logwmax"].value
        freq = _logspace(logwmin, logwmax, nmodes)
        tau = 1.0 / freq
        eps = np.zeros(nmodes)
        for i in range(nmodes):
            eps[i] = np.power(10, self.parameters["logDe%02d" % i].value)
        return tau, eps, True

    def KWWModesFrequency(self, f: FileLike) -> None:
        """Calculate theory"""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        einf: Any = self.parameters["einf"].value
        beta: Any = self.parameters["beta"].value
        nmodes: Any = self.parameters["nmodes"].value
        logwmin: Any = self.parameters["logwmin"].value
        logwmax: Any = self.parameters["logwmax"].value
        freq = _logspace(logwmin, logwmax, nmodes)
        tau = 1.0 / freq

        tt.data[:, 1] += einf
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            eps = np.power(10, self.parameters["logDe%02d" % i].value)
            for j, w in enumerate(tt.data[:, 0]):
                tt.data[j, 1] += eps * kwwc(w * tau[i], beta)
                tt.data[j, 2] += eps * kwws(w * tau[i], beta)

    def plot_theory_stuff(self) -> None:
        """Plot theory helpers"""
        # if not self.view_modes:
        #     return
        data_table_tmp: Any = DataTable(self.axarr)
        data_table_tmp.num_columns = 3
        nmodes: Any = self.parameters["nmodes"].value
        data_table_tmp.num_rows = nmodes
        data_table_tmp.data = np.zeros((nmodes, 3))
        logwmin: Any = self.parameters["logwmin"].value
        logwmax: Any = self.parameters["logwmax"].value
        freq = _logspace(logwmin, logwmax, nmodes)
        data_table_tmp.data[:, 0] = freq
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            data_table_tmp.data[i, 1] = data_table_tmp.data[i, 2] = np.power(10, self.parameters["logDe%02d" % i].value)
        view = self.parent_dataset.parent_application.current_view
        try:
            x, y, success = view.view_proc(data_table_tmp, None)
        except TypeError as e:
            print(e)
            return
        x, y = self.convert_view_data_to_display(x, y, view)
        self.graphicmodes.set_data(x, y)
        for i in range(data_table_tmp.MAX_NUM_SERIES):
            for nx in range(len(self.axarr)):
                # self.axarr[nx].lines.remove(data_table_tmp.series[nx][i])
                data_table_tmp.series[nx][i].remove()
