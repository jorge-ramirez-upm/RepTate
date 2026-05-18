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
"""Module TheoryMaxwellModes

Module that defines theories related to Maxwell modes, in the frequency and time domains.

"""

from typing import Any, ClassVar

import numpy as np
from RepTate.core.DataTable import DataTable
from RepTate.core.Parameter import Parameter, ParameterType, OptType
from RepTate.core.typing import AxesArray, DataSetLike, FileLike, FloatArray, ModesResult
from RepTate.gui.QTheory import QTheory
from PySide6.QtWidgets import QToolBar, QSpinBox
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from RepTate.core.DraggableArtists import DragType, DraggableModesSeries


def _logspace(start: float, stop: float, num: int) -> FloatArray:
    return np.logspace(start, stop, num)


class TheoryMaxwellModesFrequency(QTheory):
    """Fit a generalized Maxwell model to a frequency dependent relaxation function. 
    
    * **Function**
        .. math::
            \\begin{eqnarray}
            G'(\\omega) & = & \\sum_{1}^{n_{modes}} G_i \\frac{(\\omega\\tau_i)^2}{1+(\\omega\\tau_i)^2} \\\\
            G''(\\omega) & = & \\sum_{1}^{n_{modes}} G_i \\frac{\\omega\\tau_i}{1+(\\omega\\tau_i)^2}
            \\end{eqnarray}
    
    * **Parameters**
       - :math:`n_{modes}`: number of Maxwell modes equally distributed in logarithmic scale between :math:`\\omega_{min}` and :math:`\\omega_{max}`.
       - logwmin = :math:`\\log(\\omega_{min})`: decimal logarithm of the minimum frequency.
       - logwmax = :math:`\\log(\\omega_{max})`: decimal logarithm of the maximum frequency.
       - logGi = :math:`\\log(G_{i})`: decimal logarithm of the amplitude of Maxwell mode :math:`i`.
    
    """

    thname: ClassVar[str] = "Maxwell Modes"
    description: ClassVar[str] = "Maxwell modes, frequency dependent"
    citations: ClassVar[list[str]] = []
    doi: ClassVar[list[str]] = []
    html_help_file: ClassVar[str] = "http://reptate.readthedocs.io/manual/Applications/LVE/Theory/theory.html#maxwell-modes"
    single_file: ClassVar[bool] = True

    def __init__(self, name: str = "", parent_dataset: DataSetLike | None = None, ax: AxesArray | None = None) -> None:
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)
        self.function = self.MaxwellModesFrequency
        self.has_modes = True
        self.MAX_MODES = 40
        self.view_modes = True
        wmin = self.parent_dataset.minpositivecol(0)
        wmax = self.parent_dataset.maxcol(0)
        nmodes = int(np.round(np.log10(wmax / wmin)))

        self.parameters["logwmin"] = Parameter(
            name="logwmin",
            value=np.log10(wmin),
            description="log10(wmin) of frequency range minimum expressed in rad/s",
            type=ParameterType.real,
            opt_type=OptType.opt,
            min_value=-10,
            max_value=10,
        )
        self.parameters["logwmax"] = Parameter(
            name="logwmax",
            value=np.log10(wmax),
            description="log10(wmax) of frequency range maximum expressed in rad/s",
            type=ParameterType.real,
            opt_type=OptType.opt,
            min_value=-10,
            max_value=10,
        )
        self.parameters["nmodes"] = Parameter(
            name="nmodes",
            value=nmodes,
            description="Number of Maxwell modes",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False,
            min_value=1,
            max_value=self.MAX_MODES,
        )
        # Interpolate modes from data
        if nmodes > 1:
            w = _logspace(np.log10(wmin), np.log10(wmax), nmodes)
        else:
            w = _logspace(np.log10(wmin), np.log10(wmin), nmodes)
            self.parameters["logwmax"].opt_type = OptType.const
        G = np.abs(
            np.interp(
                w,
                self.parent_dataset.files[0].data_table.data[:, 0],
                self.parent_dataset.files[0].data_table.data[:, 1],
            )
        )
        nmodes_value = self.parameter_int("nmodes")
        for i in range(nmodes_value):
            self.parameters["logG%02d" % i] = Parameter(
                name="logG%02d" % i,
                value=np.log10(G[i]),
                description="log10(G%02d) of Mode %d amplitude expressed in Pa" % (i, i),
                type=ParameterType.real,
                opt_type=OptType.opt,
                min_value=-10,
                max_value=10,
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
        self.save_modes_action = tb.addAction(QIcon(":/Icon8/Images/new_icons/icons8-save-Maxwell.png"), "Save Modes")
        self.modesaction.setCheckable(True)
        self.modesaction.setChecked(True)
        self.thToolsLayout.insertWidget(0, tb)

        self.spinbox.valueChanged.connect(self.handle_spinboxValueChanged)
        self.modesaction.triggered.connect(self.modesaction_change)
        self.save_modes_action.triggered.connect(self.save_modes)

    def Qhide_theory_extras(self, state: bool) -> None:
        """Uncheck the modeaction button. Called when curent theory is changed"""
        self.modesaction.setChecked(state)

    def modesaction_change(self, checked: bool) -> None:
        """Change visibility of modes"""
        self.graphicmodes_visible(checked)
        # self.view_modes = self.modesaction.isChecked()
        # self.graphicmodes.set_visible(self.view_modes)
        # self.do_calculate("")

    def handle_spinboxValueChanged(self, value: int) -> None:
        """Handle a change of the parameter 'nmodes'"""
        self.set_param_value("nmodes", value)
        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()
        self.update_parameter_table()

    def set_param_value(self, name: str, value: Any) -> tuple[str, bool]:
        """Change other parameters when nmodes is changed, else call parent function"""
        if name == "nmodes":
            nmodesold = self.parameter_int("nmodes")
            wminold = self.parameter_float("logwmin")
            wmaxold = self.parameter_float("logwmax")
            wold = _logspace(wminold, wmaxold, nmodesold)
            Gold = np.zeros(nmodesold)
            for i in range(nmodesold):
                Gold[i] = self.parameter_float("logG%02d" % i)
                del self.parameters["logG%02d" % i]

            nmodesnew = int(value)
            message, success = super().set_param_value("nmodes", nmodesnew)
            if nmodesnew > 1 and nmodesold == 1:
                if wminold > wmaxold:
                    wminold, wmaxold = wmaxold, wminold
                self.parameters["logwmax"].opt_type = OptType.opt
            if nmodesnew > 1:
                wnew = _logspace(wminold, wmaxold, nmodesnew)
                Gnew = np.interp(wnew, wold, Gold)
            else:
                wnew = _logspace(wminold, wminold, nmodesnew)
                Gnew = np.array([Gold[0]])
                self.parameters["logwmax"].opt_type = OptType.const

            for i in range(nmodesnew):
                self.parameters["logG%02d" % i] = Parameter(
                    "logG%02d" % i,
                    Gnew[i],
                    "Log of Mode %d amplitude" % i,
                    ParameterType.real,
                    opt_type=OptType.opt,
                    min_value=-10,
                    max_value=10,
                )
            self.spinbox.blockSignals(True)
            self.spinbox.setValue(nmodesnew)
            self.spinbox.blockSignals(False)
        else:
            message, success = super().set_param_value(name, value)

        return message, success

    def drag_mode(self, dx: Any, dy: Any) -> None:
        """Drag modes around"""
        dx, dy = self.convert_view_data_to_internal(dx, dy)
        nmodes = self.parameter_int("nmodes")
        if self.current_view().log_x:
            self.set_param_value("logwmin", np.log10(dx[0]))
            self.set_param_value("logwmax", np.log10(dx[nmodes - 1]))
        else:
            self.set_param_value("logwmin", dx[0])
            self.set_param_value("logwmax", dx[nmodes - 1])

        if self.current_view().log_y:
            for i in range(nmodes):
                self.set_param_value("logG%02d" % i, np.log10(dy[i]))
        else:
            for i in range(nmodes):
                self.set_param_value("logG%02d" % i, dy[i])

        self.do_calculate("")
        self.update_parameter_table()

    def update_modes(self) -> None:
        """Do nothing"""
        pass

    def setup_graphic_modes(self) -> None:
        """Setup graphic helpers"""
        nmodes = self.parameter_int("nmodes")
        logwmin = self.parameter_float("logwmin")
        logwmax = self.parameter_float("logwmax")
        if nmodes > 1:
            w = _logspace(logwmin, logwmax, nmodes)
        else:
            w = _logspace(logwmin, logwmin, nmodes)
        G = np.zeros(nmodes)
        for i in range(nmodes):
            G[i] = np.power(10, self.parameters["logG%02d" % i].value)

        self.graphicmodes = self.ax.plot(w, G)[0]
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

    def get_modes(self) -> ModesResult:
        """Get the values of Maxwell Modes from this theory"""
        nmodes = self.parameter_int("nmodes")
        logwmin = self.parameter_float("logwmin")
        logwmax = self.parameter_float("logwmax")
        if nmodes > 1:
            freq = _logspace(logwmin, logwmax, nmodes)
        else:
            freq = _logspace(logwmin, logwmin, nmodes)
        tau = 1.0 / freq
        G = np.zeros(nmodes)
        for i in range(nmodes):
            G[i] = np.power(10, self.parameters["logG%02d" % i].value)
        return tau, G, True

    def MaxwellModesFrequency(self, f: FileLike) -> None:
        """Calculate the theory"""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        nmodes = self.parameter_int("nmodes")
        logwmin = self.parameter_float("logwmin")
        logwmax = self.parameter_float("logwmax")
        if nmodes > 1:
            freq = _logspace(logwmin, logwmax, nmodes)
        else:
            freq = _logspace(logwmin, logwmin, nmodes)
        tau = 1.0 / freq

        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            wT = tt.data[:, 0] * tau[i]
            wTsq = wT**2
            G = np.power(10, self.parameters["logG%02d" % i].value)
            tt.data[:, 1] += G * wTsq / (1 + wTsq)
            tt.data[:, 2] += G * wT / (1 + wTsq)

    def plot_theory_stuff(self) -> None:
        """Plot theory helpers"""
        # if not self.view_modes:
        #     return
        data_table_tmp: Any = DataTable(self.axarr)
        data_table_tmp.num_columns = 3
        nmodes = self.parameter_int("nmodes")
        data_table_tmp.num_rows = nmodes
        data_table_tmp.data = np.zeros((nmodes, 3))
        logwmin = self.parameter_float("logwmin")
        logwmax = self.parameter_float("logwmax")
        if nmodes > 1:
            freq = _logspace(logwmin, logwmax, nmodes)
        else:
            freq = _logspace(logwmin, logwmin, nmodes)
        data_table_tmp.data[:, 0] = freq
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            data_table_tmp.data[i, 1] = data_table_tmp.data[i, 2] = np.power(10, self.parameters["logG%02d" % i].value)
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


##################################################################################
#   MAXWELL MODES TIME
##################################################################################


class TheoryMaxwellModesTime(QTheory):
    """Fit a generalized Maxwell model to a time dependent relaxation function.

    * **Function**
        .. math::
            \\begin{eqnarray}
            G(t) & = & \\sum_{i=1}^{n_{modes}} G_i \\exp (-t/\\tau_i)
            \\end{eqnarray}

    * **Parameters**
       - :math:`n_{modes}`: number of Maxwell modes equally distributed in logarithmic scale between :math:`\\omega_{min}` and :math:`\\omega_{max}`.
       - logtmin = :math:`\\log(t_{min})`: decimal logarithm of the minimum time.
       - logtmax = :math:`\\log(t_{max})`: decimal logarithm of the maximum time.
       - logGi = :math:`\\log(G_{i})`: decimal logarithm of the amplitude of Maxwell mode :math:`i`.

    """

    thname: ClassVar[str] = "Maxwell Modes"
    description: ClassVar[str] = "Maxwell modes, time dependent"
    citations: ClassVar[list[str]] = []
    html_help_file: ClassVar[str] = "http://reptate.readthedocs.io/manual/Applications/Gt/Theory/theory.html#maxwell-modes"
    single_file: ClassVar[bool] = True

    def __init__(self, name: str = "", parent_dataset: DataSetLike | None = None, ax: AxesArray | None = None) -> None:
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)
        self.function = self.MaxwellModesTime
        self.has_modes = True
        self.MAX_MODES = 40
        self.view_modes = True
        tmin = self.parent_dataset.minpositivecol(0)
        tmax = self.parent_dataset.maxcol(0)
        nmodes = int(np.round(np.log10(tmax / tmin)))

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
            description="Number of Maxwell modes",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False,
        )
        # Interpolate modes from data
        if nmodes > 1:
            tau = _logspace(np.log10(tmin), np.log10(tmax), nmodes)
        else:
            tau = _logspace(np.log10(tmax), np.log10(tmax), nmodes)
            self.parameters["logtmin"].opt_type = OptType.const
        G = np.abs(
            np.interp(
                tau,
                self.parent_dataset.files[0].data_table.data[:, 0],
                self.parent_dataset.files[0].data_table.data[:, 1],
            )
        )
        nmodes_value = self.parameter_int("nmodes")
        for i in range(nmodes_value):
            self.parameters["logG%02d" % i] = Parameter(
                name="logG%02d" % i,
                value=np.log10(G[i]),
                description="log10(G%02d) of Mode %d amplitude expressed in Pa" % (i, i),
                type=ParameterType.real,
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
        self.save_modes_action = tb.addAction(QIcon(":/Icon8/Images/new_icons/icons8-save-Maxwell.png"), "Save Modes")
        self.modesaction.setCheckable(True)
        self.modesaction.setChecked(True)
        self.thToolsLayout.insertWidget(0, tb)

        self.spinbox.valueChanged.connect(self.handle_spinboxValueChanged)
        self.modesaction.triggered.connect(self.modesaction_change)
        self.save_modes_action.triggered.connect(self.save_modes)

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
        """Handle a change of the parameter 'nmodes'"""
        self.set_param_value("nmodes", value)
        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()
        self.update_parameter_table()

    def set_param_value(self, name: str, value: Any) -> tuple[str, bool]:
        """Change other parameters when nmodes is changed, else call parent function"""
        if name == "nmodes":
            nmodesold = self.parameter_int("nmodes")
            tminold = self.parameter_float("logtmin")
            tmaxold = self.parameter_float("logtmax")
            tauold = _logspace(tminold, tmaxold, nmodesold)
            Gold = np.zeros(nmodesold)
            for i in range(nmodesold):
                Gold[i] = self.parameter_float("logG%02d" % i)
                del self.parameters["logG%02d" % i]

            nmodesnew: Any = value
            message, success = super().set_param_value("nmodes", nmodesnew)
            if nmodesnew > 1 and nmodesold == 1:
                if tminold > tmaxold:  # pyright: ignore[reportUnboundVariable, reportOperatorIssue]
                    tminold, tmaxold = tmaxold, tminold  # pyright: ignore[reportUnboundVariable]
                self.parameters["logtmin"].opt_type = OptType.opt
            if nmodesnew > 1:
                taunew = _logspace(tminold, tmaxold, nmodesnew)
                Gnew = np.interp(taunew, tauold, Gold)
            else:
                taunew = 10.0 ** np.array([tmaxold])
                Gnew = np.array([Gold[-1]])
                self.parameters["logtmin"].opt_type = OptType.const

            for i in range(nmodesnew):
                self.parameters["logG%02d" % i] = Parameter(
                    "logG%02d" % i,
                    Gnew[i],
                    "Log of Mode %d amplitude" % i,
                    ParameterType.real,
                    opt_type=OptType.opt,
                    min_value=-10,
                    max_value=10,
                )
            self.spinbox.setValue(value)
        else:
            message, success = super().set_param_value(name, value)

        return message, success

    def drag_mode(self, dx: Any, dy: Any) -> None:
        """Drag modes around"""
        dx, dy = self.convert_view_data_to_internal(dx, dy)
        nmodes = self.parameter_int("nmodes")
        self.set_param_value("logtmin", dx[0])
        self.set_param_value("logtmax", dx[nmodes - 1])
        for i in range(nmodes):
            self.set_param_value("logG%02d" % i, dy[i])
        self.do_calculate("")
        self.update_parameter_table()

    def update_modes(self) -> None:
        """Do nothing"""
        pass

    def setup_graphic_modes(self) -> None:
        """setup graphic helpers"""
        nmodes = self.parameter_int("nmodes")
        logtmin = self.parameter_float("logtmin")
        logtmax = self.parameter_float("logtmax")
        if nmodes > 1:
            tau = _logspace(logtmin, logtmax, nmodes)
        else:
            tau = _logspace(logtmax, logtmax, nmodes)
        G = np.zeros(nmodes)
        for i in range(nmodes):
            G[i] = np.power(10, self.parameters["logG%02d" % i].value)

        self.graphicmodes = self.ax.plot(tau, G)[0]
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

    def get_modes(self) -> ModesResult:
        """Get the values of Maxwell Modes from this theory"""
        nmodes = self.parameter_int("nmodes")
        logtmin = self.parameter_float("logtmin")
        logtmax = self.parameter_float("logtmax")
        if nmodes > 1:
            tau = _logspace(logtmin, logtmax, nmodes)
        else:
            tau = _logspace(logtmax, logtmax, nmodes)
        G = np.zeros(nmodes)
        for i in range(nmodes):
            G[i] = np.power(10, self.parameters["logG%02d" % i].value)
        return tau, G, True

    def MaxwellModesTime(self, f: FileLike) -> None:
        """Calculate the theory"""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        value = f.file_parameters.get("gamma")
        if value is None:
            gamma = 1
        else:
            gamma = float(value)
            if gamma == 0:
                gamma = 1

        nmodes = self.parameter_int("nmodes")
        logtmin = self.parameter_float("logtmin")
        logtmax = self.parameter_float("logtmax")
        if nmodes > 1:
            tau = _logspace(logtmin, logtmax, nmodes)
        else:
            tau = _logspace(logtmax, logtmax, nmodes)

        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            expT_tau = np.exp(-tt.data[:, 0] / tau[i])
            G = np.power(10, self.parameters["logG%02d" % i].value)
            tt.data[:, 1] += G * expT_tau * gamma

    def plot_theory_stuff(self) -> None:
        """Plot theory helpers"""
        if not self.view_modes:
            return
        data_table_tmp: Any = DataTable(self.axarr)
        data_table_tmp.num_columns = 2
        nmodes = self.parameter_int("nmodes")
        data_table_tmp.num_rows = nmodes
        data_table_tmp.data = np.zeros((nmodes, 2))
        logtmin = self.parameter_float("logtmin")
        logtmax = self.parameter_float("logtmax")
        if nmodes > 1:
            tau = _logspace(logtmin, logtmax, nmodes)
        else:
            tau = _logspace(logtmax, logtmax, nmodes)
        data_table_tmp.data[:, 0] = tau
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            data_table_tmp.data[i, 1] = np.power(10, self.parameters["logG%02d" % i].value)
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
                data_table_tmp.series[nx][i].remove()
                # self.axarr[nx].lines.remove(data_table_tmp.series[nx][i])
