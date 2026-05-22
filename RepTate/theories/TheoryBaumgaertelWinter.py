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
# Copyright (2017-2026): Jorge Ramirez, Victor Boudara, Universidad Politecnica de Madrid, University of Leeds
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
"""Module TheoryBaumgaertelWinter.

Discrete Baumgaertel-Winter relaxation spectrum from dynamic moduli.

This first implementation covers only the frequency-domain conversion from
G'(omega), G''(omega) to a discrete generalized Maxwell spectrum.  The original
Baumgaertel-Winter method also discusses adaptive mode elimination/merging and
conversion to a retardation spectrum; those parts are intentionally left for a
later implementation.
"""

from typing import Any, ClassVar

import numpy as np
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QSpinBox, QToolBar

from RepTate.core.DataTable import DataTable
from RepTate.core.DraggableArtists import DragType, DraggableModesSeries
from RepTate.core.Parameter import OptType, Parameter, ParameterType
from RepTate.core.typing import AxesArray, DataSetLike, FileLike, FloatArray, ModesResult
from RepTate.gui.QTheory import QTheory


_LOG_FLOOR = 1.0e-300


def _logspace(start: float, stop: float, num: int) -> FloatArray:
    return np.logspace(start, stop, num)


def _safe_log10(values: FloatArray) -> FloatArray:
    return np.log10(np.maximum(np.asarray(values, dtype=float), _LOG_FLOOR))


class TheoryBaumgaertelWinter(QTheory):
    """Fit a Baumgaertel-Winter discrete relaxation spectrum to dynamic moduli.

    * **Function**
        .. math::
            \begin{eqnarray}
            G'(\omega) & = & G_e + \sum_{i=1}^{n_{modes}} g_i
                \frac{(\omega\tau_i)^2}{1+(\omega\tau_i)^2} \\
            G''(\omega) & = & \sum_{i=1}^{n_{modes}} g_i
                \frac{\omega\tau_i}{1+(\omega\tau_i)^2}
            \end{eqnarray}

    * **Parameters**
       - :math:`n_{modes}`: number of discrete relaxation modes.
       - :math:`G_e`: equilibrium modulus. It is constant and zero by default.
       - logtaui = :math:`\log_{10}(\tau_i/s)`: decimal logarithm of the
         relaxation time of mode :math:`i`.
       - logGi = :math:`\log_{10}(g_i/Pa)`: decimal logarithm of the
         relaxation strength of mode :math:`i`.

    In contrast to the standard Maxwell modes theory with equally spaced modes,
    both :math:`g_i` and :math:`\tau_i` are independent adjustable parameters.
    """

    thname: ClassVar[str] = "Baumgaertel-Winter"
    description: ClassVar[str] = "Discrete relaxation spectrum from dynamic moduli"
    citations: ClassVar[list[str]] = ["M. Baumgaertel and H. H. Winter, Rheol. Acta 28, 511-519 (1989)."]
    doi: ClassVar[list[str]] = ["http://dx.doi.org/10.1007/BF01332922"]
    html_help_file: ClassVar[str] = "http://reptate.readthedocs.io/manual/Applications/LVE/Theory/theory.html"
    single_file: ClassVar[bool] = True

    def __init__(self, name: str = "", parent_dataset: DataSetLike | None = None, ax: AxesArray | None = None) -> None:
        """Constructor."""
        super().__init__(name, parent_dataset, ax)
        self.function = self.BaumgaertelWinterFrequency
        self.has_modes = True
        self.MAX_MODES = 40
        self.view_modes = True

        wmin = self.parent_dataset.minpositivecol(0)
        wmax = self.parent_dataset.maxcol(0)
        nmodes = max(1, int(np.round(np.log10(wmax / wmin))))
        nmodes = min(nmodes, self.MAX_MODES)

        self.parameters["nmodes"] = Parameter(
            name="nmodes",
            value=nmodes,
            description="Number of Baumgaertel-Winter Maxwell modes",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False,
            min_value=1,
            max_value=self.MAX_MODES,
        )
        self.parameters["Ge"] = Parameter(
            name="Ge",
            value=0.0,
            description="Equilibrium modulus expressed in Pa; keep zero for viscoelastic liquids",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0.0,
        )

        # Initial modes: tau spans the reciprocal experimental frequency window.
        # The mode markers are displayed at omega_i = 1/tau_i, as in the LVE
        # frequency plot.  tau_i itself remains a freely adjustable parameter.
        tau = self._initial_tau(wmin, wmax, nmodes)
        omega_modes = 1.0 / tau
        G = self._initial_moduli(omega_modes)

        for i in range(nmodes):
            self.parameters["logtau%02d" % i] = Parameter(
                name="logtau%02d" % i,
                value=float(np.log10(tau[i])),
                description="log10(tau%02d) of Mode %d relaxation time expressed in s" % (i, i),
                type=ParameterType.real,
                opt_type=OptType.opt,
                min_value=-30,
                max_value=30,
            )
            self.parameters["logG%02d" % i] = Parameter(
                name="logG%02d" % i,
                value=float(np.log10(max(G[i], _LOG_FLOOR))),
                description="log10(G%02d) of Mode %d relaxation strength expressed in Pa" % (i, i),
                type=ParameterType.real,
                opt_type=OptType.opt,
                min_value=-30,
                max_value=30,
            )

        # GRAPHIC MODES
        self.graphicmodes: Any = []
        self.artistmodes: Any = []
        self.setup_graphic_modes()

        # Widgets specific to the theory.
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, self.MAX_MODES)
        self.spinbox.setSuffix(" modes")
        self.spinbox.setValue(nmodes)
        tb.addWidget(self.spinbox)
        self.modesaction = tb.addAction(QIcon(":/Icon8/Images/new_icons/icons8-visible.png"), "View modes")
        self.save_modes_action = tb.addAction(QIcon(":/Icon8/Images/new_icons/icons8-save-Maxwell.png"), "Save Modes")
        self.modesaction.setCheckable(True)
        self.modesaction.setChecked(True)
        self.thToolsLayout.insertWidget(0, tb)

        self.spinbox.valueChanged.connect(self.handle_spinboxValueChanged)
        self.modesaction.triggered.connect(self.modesaction_change)
        self.save_modes_action.triggered.connect(self.save_modes)

    def _initial_tau(self, wmin: float, wmax: float, nmodes: int) -> FloatArray:
        if nmodes > 1:
            return _logspace(-np.log10(wmax), -np.log10(wmin), nmodes)
        return _logspace(-np.log10(np.sqrt(wmin * wmax)), -np.log10(np.sqrt(wmin * wmax)), nmodes)

    def _initial_moduli(self, omega_modes: FloatArray) -> FloatArray:
        data = self.parent_dataset.files[0].data_table.data
        omega_data = data[:, 0]
        storage = np.abs(data[:, 1])
        if data.shape[1] > 2:
            loss = np.abs(data[:, 2])
            modulus_scale = np.sqrt(storage**2 + loss**2)
        else:
            modulus_scale = storage
        return np.maximum(np.interp(omega_modes, omega_data, modulus_scale), _LOG_FLOOR)

    def Qhide_theory_extras(self, state: bool) -> None:
        """Uncheck the modeaction button. Called when current theory is changed."""
        self.modesaction.setChecked(state)

    def modesaction_change(self, checked: bool) -> None:
        """Change visibility of modes."""
        self.graphicmodes_visible(checked)

    def handle_spinboxValueChanged(self, value: int) -> None:
        """Handle a change of the parameter 'nmodes'."""
        self.set_param_value("nmodes", value)
        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()
        self.update_parameter_table()

    def set_param_value(self, name: str, value: Any) -> tuple[str, bool]:
        """Change mode parameters when nmodes changes; otherwise call parent."""
        if name == "nmodes":
            nmodesold = self.parameter_int("nmodes")
            logtauold = np.zeros(nmodesold)
            logGold = np.zeros(nmodesold)
            for i in range(nmodesold):
                logtauold[i] = self.parameter_float("logtau%02d" % i)
                logGold[i] = self.parameter_float("logG%02d" % i)
                del self.parameters["logtau%02d" % i]
                del self.parameters["logG%02d" % i]

            nmodesnew = int(value)
            message, success = super().set_param_value("nmodes", nmodesnew)

            order = np.argsort(logtauold)
            logtauold_sorted = logtauold[order]
            logGold_sorted = logGold[order]
            if nmodesnew > 1:
                logtaunew = np.linspace(logtauold_sorted[0], logtauold_sorted[-1], nmodesnew)
                logGnew = np.interp(logtaunew, logtauold_sorted, logGold_sorted)
            else:
                logtaunew = np.array([np.mean(logtauold_sorted)])
                logGnew = np.array([np.mean(logGold_sorted)])

            for i in range(nmodesnew):
                self.parameters["logtau%02d" % i] = Parameter(
                    "logtau%02d" % i,
                    float(logtaunew[i]),
                    "Log of Mode %d relaxation time" % i,
                    ParameterType.real,
                    opt_type=OptType.opt,
                    min_value=-30,
                    max_value=30,
                )
                self.parameters["logG%02d" % i] = Parameter(
                    "logG%02d" % i,
                    float(logGnew[i]),
                    "Log of Mode %d relaxation strength" % i,
                    ParameterType.real,
                    opt_type=OptType.opt,
                    min_value=-30,
                    max_value=30,
                )
            self.spinbox.blockSignals(True)
            self.spinbox.setValue(nmodesnew)
            self.spinbox.blockSignals(False)
        else:
            message, success = super().set_param_value(name, value)

        return message, success

    def drag_mode(self, dx: Any, dy: Any) -> None:
        """Drag individual modes.

        Mode symbols are displayed at omega_i = 1/tau_i.  Therefore horizontal
        dragging changes logtau_i = -log10(omega_i) in logarithmic frequency
        views.
        """
        dx, dy = self.convert_view_data_to_internal(dx, dy)
        nmodes = self.parameter_int("nmodes")

        if self.current_view().log_x:
            logtau = -_safe_log10(dx)
        else:
            logtau = -np.asarray(dx, dtype=float)

        if self.current_view().log_y:
            logG = _safe_log10(dy)
        else:
            logG = np.asarray(dy, dtype=float)

        for i in range(nmodes):
            self.set_param_value("logtau%02d" % i, float(logtau[i]))
            self.set_param_value("logG%02d" % i, float(logG[i]))

        self.do_calculate("")
        self.update_parameter_table()

    def update_modes(self) -> None:
        """Do nothing."""
        pass

    def setup_graphic_modes(self) -> None:
        """Setup graphic helpers."""
        omega, G = self._mode_marker_data()
        self.graphicmodes = self.ax.plot(omega, G)[0]
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
        """Called when the theory tab is closed."""
        self.graphicmodes_visible(False)
        self.graphicmodes.remove()

    def show_theory_extras(self, show: bool = False) -> None:
        """Called when the active theory is changed."""
        self.Qhide_theory_extras(show)
        self.graphicmodes_visible(show)

    def graphicmodes_visible(self, state: bool) -> None:
        """Change visibility of modes."""
        self.view_modes = state
        self.graphicmodes.set_visible(self.view_modes)
        if self.view_modes:
            self.artistmodes.connect()
        else:
            self.artistmodes.disconnect()
        self.parent_dataset.parent_application.update_plot()

    def _mode_values(self) -> tuple[FloatArray, FloatArray]:
        nmodes = self.parameter_int("nmodes")
        tau = np.zeros(nmodes)
        G = np.zeros(nmodes)
        for i in range(nmodes):
            tau[i] = np.power(10.0, self.parameter_float("logtau%02d" % i))
            G[i] = np.power(10.0, self.parameter_float("logG%02d" % i))
        return tau, G

    def _mode_marker_data(self) -> tuple[FloatArray, FloatArray]:
        tau, G = self._mode_values()
        omega = 1.0 / np.maximum(tau, _LOG_FLOOR)
        return omega, G

    def get_modes(self) -> ModesResult:
        """Get relaxation times and strengths from this theory."""
        tau, G = self._mode_values()
        order = np.argsort(tau)
        return tau[order], G[order], True

    def BaumgaertelWinterFrequency(self, f: FileLike) -> None:
        """Calculate the frequency-domain Maxwell response."""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        tau, G = self._mode_values()
        Ge = self.parameter_float("Ge")
        if tt.num_columns > 1:
            tt.data[:, 1] = Ge
        if tt.num_columns <= 2:
            return

        for i in range(self.parameter_int("nmodes")):
            if self.stop_theory_flag:
                break
            wT = tt.data[:, 0] * tau[i]
            wTsq = wT**2
            tt.data[:, 1] += G[i] * wTsq / (1.0 + wTsq)
            tt.data[:, 2] += G[i] * wT / (1.0 + wTsq)

    def plot_theory_stuff(self) -> None:
        """Plot draggable mode helpers."""
        data_table_tmp: Any = DataTable(self.axarr)
        data_table_tmp.num_columns = 3
        nmodes = self.parameter_int("nmodes")
        data_table_tmp.num_rows = nmodes
        data_table_tmp.data = np.zeros((nmodes, 3))
        omega, G = self._mode_marker_data()
        data_table_tmp.data[:, 0] = omega
        data_table_tmp.data[:, 1] = G
        data_table_tmp.data[:, 2] = G
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
