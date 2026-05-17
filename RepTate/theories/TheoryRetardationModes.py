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
"""Module TheoryRetardationModes

Module that defines theories related to Retardation modes, in the frequency and time domains.

"""

from typing import Any, ClassVar

import numpy as np
from RepTate.core.DataTable import DataTable
from RepTate.core.Parameter import Parameter, ParameterType, OptType
from RepTate.core.typing import AxesArray, FileLike, FloatArray
from RepTate.gui.QTheory import QTheory
from PySide6.QtWidgets import QToolBar, QSpinBox
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from RepTate.core.DraggableArtists import DragType, DraggableModesSeries


def _logspace(start: float, stop: float, num: int) -> FloatArray:
    return np.logspace(start, stop, num)


class TheoryRetardationModesTime(QTheory):
    """Fit a discrete Retardation spectrum to time dependent creep data

    * **Function**
        .. math::
            \\gamma(t) = \\sigma_0 \\left( J_0 + \\sum_{1}^{n_{modes}} J_i \\left[ 1 - \\exp\\left(\\frac{-t}{\\tau_i}\\right) \\right] + \\frac{t}{\\eta_0} \\right)

        where:
          - :math:`\\sigma_0`: constant stress applied during the creep experiment.

    * **Parameters**
       - :math:`J_0`: Instantaneous compliance (``logJini``, in logarithmic scale).
       - :math:`\\eta_0`: Terminal viscosity (``logeta0``, in logarithmic scale).
       - :math:`n_{modes}`: number of Retardation modes equally distributed in logarithmic scale between :math:`t_{min}` and :math:`t_{max}`.
       - logtmin = :math:`\\log(t_{min})`: decimal logarithm of the minimum time range for the modes.
       - logtmax = :math:`\\log(t_{max})`: decimal logarithm of the maximum time.
       - logJi = :math:`\\log(J_{i})`: decimal logarithm of the compliance of Retardation mode :math:`i`.

    """

    thname: ClassVar[str] = "Retardation Modes"
    description: ClassVar[str] = "Fit Retardation modes to time dependent creep data"
    citations: ClassVar[list[str]] = []
    doi: ClassVar[list[str]] = []
    html_help_file: ClassVar[str] = "http://reptate.readthedocs.io/manual/Applications/Creep/Theory/theory.html#retardation-modes"
    single_file: ClassVar[bool] = False

    def __init__(self, name: str = "", parent_dataset: Any = None, ax: AxesArray | None = None) -> None:
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)
        self.function = self.RetardationModesTime
        self.has_modes = True
        self.MAX_MODES = 40
        self.view_modes = True
        tmin = self.parent_dataset.minpositivecol(0)
        tmax = self.parent_dataset.maxcol(0)
        nmodes = int(np.round(np.log10(tmax / tmin)))

        self.parameters["logJini"] = Parameter(
            name="logJini",
            value=-4.0,
            description="Log of Instantaneous Compliance expressed in 1/Pa",
            type=ParameterType.real,
            opt_type=OptType.opt,
        )
        self.parameters["logeta0"] = Parameter(
            name="logeta0",
            value=0.0,
            description="Log of Terminal Viscosity expressed in Pa.s",
            type=ParameterType.real,
            opt_type=OptType.opt,
        )
        self.parameters["logtmin"] = Parameter(
            name="logtmin",
            value=np.log10(tmin),
            description="log10(tmin) of time range minimum expressed in s",
            type=ParameterType.real,
            opt_type=OptType.opt,
        )
        self.parameters["logtmax"] = Parameter(
            name="logtmax",
            value=np.log10(tmax),
            description="log10(tmax) of time range maximum expressed in s",
            type=ParameterType.real,
            opt_type=OptType.opt,
        )
        self.parameters["nmodes"] = Parameter(
            name="nmodes",
            value=nmodes,
            description="Number of Retardation modes",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False,
        )
        # Interpolate modes from data
        try:
            sigma = float(self.parent_dataset.files[0].file_parameters["stress"])
        except (ValueError, KeyError):
            self.Qprint("Invalid stress value")
            return
        tau = _logspace(np.log10(tmin), np.log10(tmax), nmodes)
        J = (
            np.abs(
                np.interp(
                    tau,
                    self.parent_dataset.files[0].data_table.data[:, 0],
                    self.parent_dataset.files[0].data_table.data[:, 1],
                )
            )
            / sigma
        )
        nmodes_value: Any = self.parameters["nmodes"].value
        for i in range(nmodes_value):
            self.parameters["logJ%02d" % i] = Parameter(
                "logJ%02d" % i,
                np.log10(J[i]),
                "Log of Mode %d amplitude" % i,
                ParameterType.real,
                opt_type=OptType.opt,
            )

        # GRAPHIC MODES
        self.graphicmodes: Any = None
        self.artistmodes: Any = None
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
        """Change visibility of modes"""
        self.graphicmodes_visible(checked)
        # self.view_modes = self.modesaction.isChecked()
        # self.graphicmodes.set_visible(self.view_modes)
        # if self.view_modes:
        #     self.artistmodes.connect()
        # else:
        #     self.artistmodes.disconnect()
        # self.do_calculate("")

    def handle_spinboxValueChanged(self, value: int) -> None:
        """Handle a change of the parameter 'nmode'"""
        nmodesold: Any = self.parameters["nmodes"].value
        tminold: Any = self.parameters["logtmin"].value
        tmaxold: Any = self.parameters["logtmax"].value
        tauold = _logspace(tminold, tmaxold, nmodesold)
        Gold = np.zeros(nmodesold)
        for i in range(nmodesold):
            Gold[i] = self.parameters["logJ%02d" % i].value
            del self.parameters["logJ%02d" % i]

        nmodesnew = value
        self.set_param_value("nmodes", nmodesnew)
        taunew = _logspace(tminold, tmaxold, nmodesnew)

        Gnew = np.interp(taunew, tauold, Gold)

        for i in range(nmodesnew):
            self.parameters["logJ%02d" % i] = Parameter(
                "logJ%02d" % i,
                Gnew[i],
                "Log of Mode %d compliance" % i,
                ParameterType.real,
                opt_type=OptType.opt,
            )

        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()
        self.update_parameter_table()

    def drag_mode(self, dx: Any, dy: Any) -> None:
        """Drag modes around"""
        dx, dy = self.convert_view_data_to_internal(dx, dy)
        nmodes: Any = self.parameters["nmodes"].value
        self.set_param_value("logtmin", dx[0])
        self.set_param_value("logtmax", dx[nmodes - 1])
        for i in range(nmodes):
            self.set_param_value("logJ%02d" % i, dy[i])
        self.do_calculate("")
        self.update_parameter_table()

    def update_modes(self) -> None:
        """Do nothing"""
        pass

    def setup_graphic_modes(self) -> None:
        """Setup graphic helpers"""
        nmodes: Any = self.parameters["nmodes"].value
        logtmin: Any = self.parameters["logtmin"].value
        logtmax: Any = self.parameters["logtmax"].value
        tau = _logspace(logtmin, logtmax, nmodes)
        J = np.zeros(nmodes)
        for i in range(nmodes):
            J[i] = np.power(10, self.parameters["logJ%02d" % i].value)

        self.graphicmodes = self.ax.plot(tau, J)[0]
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

    def get_modes(self) -> tuple[FloatArray, FloatArray, bool]:
        """Get the values of Maxwell Modes from this theory"""
        nmodes: Any = self.parameters["nmodes"].value
        logtmin: Any = self.parameters["logtmin"].value
        logtmax: Any = self.parameters["logtmax"].value
        tau = _logspace(logtmin, logtmax, nmodes)
        J = np.zeros(nmodes)
        for i in range(nmodes):
            J[i] = 1.0 / np.power(10, self.parameters["logJ%02d" % i].value)
        return tau, J, True

    def RetardationModesTime(self, f: FileLike) -> None:
        """Calculate the theory"""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        try:
            stress = float(f.file_parameters["stress"])
        except (ValueError, KeyError):
            self.Qprint("Invalid stress value")
            return
        nmodes: Any = self.parameters["nmodes"].value
        logjini: Any = self.parameters["logJini"].value
        logeta0: Any = self.parameters["logeta0"].value
        J0 = np.power(10, logjini)
        eta0 = np.power(10, logeta0)
        logtmin: Any = self.parameters["logtmin"].value
        logtmax: Any = self.parameters["logtmax"].value
        tau = _logspace(logtmin, logtmax, nmodes)
        try:
            rec = int(f.file_parameters["rec"])
        except (ValueError, KeyError):
            rec = 0

        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            expT_tau = 1.0 - np.exp(-tt.data[:, 0] / tau[i])
            J = np.power(10, self.parameters["logJ%02d" % i].value)
            tt.data[:, 1] += stress * J * expT_tau
        if rec == 1:
            tt.data[:, 1] += stress * J0
        else:
            tt.data[:, 1] += stress * (J0 + tt.data[:, 0] / eta0)

    def plot_theory_stuff(self) -> None:
        """Plot theory helpers"""
        if not self.view_modes:
            return
        data_table_tmp: Any = DataTable(self.axarr)
        data_table_tmp.num_columns = 2
        nmodes: Any = self.parameters["nmodes"].value
        data_table_tmp.num_rows = nmodes
        data_table_tmp.data = np.zeros((nmodes, 2))
        logtmin: Any = self.parameters["logtmin"].value
        logtmax: Any = self.parameters["logtmax"].value
        tau = _logspace(logtmin, logtmax, nmodes)
        data_table_tmp.data[:, 0] = tau
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            data_table_tmp.data[i, 1] = np.power(10, self.parameters["logJ%02d" % i].value)
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
