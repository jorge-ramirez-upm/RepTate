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

Discrete Baumgaertel-Winter relaxation/retardation spectra from dynamic
moduli, relaxation modulus, or creep data.

The frequency-domain theory fits G'(omega), G''(omega) to a discrete generalized
Maxwell spectrum.  The time-domain theory uses the same independent modes to fit
G(t).  The original Baumgaertel-Winter method also discusses adaptive mode
elimination/merging and conversion to a retardation spectrum.  This implementation
includes a conservative mode-simplification helper for frequency-domain,
time-domain, and creep retardation data.
"""

import os
import time
import traceback
from dataclasses import dataclass
from html import escape
from typing import Any, ClassVar

import numpy as np
import RepTate
from scipy.optimize import least_squares
from PySide6.QtCore import QObject, QThread, QSize, Signal
from PySide6.QtGui import QCursor, QIcon
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QMessageBox,
    QCheckBox,
    QSpinBox,
    QToolBar,
    QToolButton,
    QMenu,
)

from RepTate.core.DataTable import DataTable
from RepTate.core.DraggableArtists import DragType, DraggableModeIndividual
from RepTate.core.Parameter import OptType, Parameter, ParameterType
from RepTate.core.typing import AxesArray, DataSetLike, FileLike, FloatArray, ModesResult
from RepTate.gui.QTheory import QTheory


_LOG_FLOOR = 1.0e-300


class _SimplificationCancelled(Exception):
    """Internal exception used to stop BW simplification cleanly."""


class _BaumgaertelWinterSimplificationWorker(QObject):
    sig_done = Signal(object)

    def __init__(
        self,
        theory: "TheoryBaumgaertelWinter",
        file: FileLike,
        tau: FloatArray,
        G: FloatArray,
        skip_initial_fit: bool,
    ) -> None:
        super().__init__()
        self.theory = theory
        self.file = file
        self.tau = tau
        self.G = G
        self.skip_initial_fit = skip_initial_fit

    def work(self) -> None:
        start_time = time.perf_counter()
        result: dict[str, Any]
        try:
            result = self.theory._simplify_spectrum_worker(self.file, self.tau, self.G, self.skip_initial_fit)
        except _SimplificationCancelled:
            result = {"cancelled": True}
        except Exception:
            result = {"error": traceback.format_exc()}
        result["elapsed_seconds"] = time.perf_counter() - start_time
        self.sig_done.emit(result)


@dataclass
class _SimplificationReportEvent:
    pass_number: int
    operation: str
    modes_before: int
    modes_after: int
    residual_before: float
    residual_after: float
    accepted: bool | None
    note: str = ""
    mode_index: int | None = None


def _logspace(start: float, stop: float, num: int) -> FloatArray:
    return np.logspace(start, stop, num)


def _safe_log10(values: FloatArray) -> FloatArray:
    return np.log10(np.maximum(np.asarray(values, dtype=float), _LOG_FLOOR))


def _format_residual(value: float) -> str:
    if not np.isfinite(value):
        return "N/A"
    return "%.3e" % value


def _format_residual_change(before: float, after: float) -> str:
    if not np.isfinite(before) or not np.isfinite(after):
        return ""
    if abs(before) < 1.0e-300:
        return "Δ = N/A"
    change = 100.0 * (after - before) / abs(before)
    return "Δ = %+.3g%%" % change


def _format_modes_change(before: int, after: int) -> str:
    return "%d &rarr; %d" % (before, after)


def _format_decision(accepted: bool | None) -> str:
    if accepted is True:
        return '<font color="green">accepted</font>'
    if accepted is False:
        return '<font color="red">rejected</font>'
    return ""


def _format_simplification_report_table(events: list[_SimplificationReportEvent]) -> str:
    rows = [
        "<table border=\"1\" cellspacing=\"0\" cellpadding=\"3\">",
        "<tr><th>Pass</th><th>Operation</th><th>Modes</th><th>Residual</th><th>Decision</th><th>Note</th></tr>",
    ]
    for event in events:
        residual = "%s &rarr; %s<br>%s" % (
            _format_residual(event.residual_before),
            _format_residual(event.residual_after),
            _format_residual_change(event.residual_before, event.residual_after),
        )
        note = event.note
        if event.mode_index is not None:
            note = ("%s; " % note if note else "") + "mode %d" % event.mode_index
        rows.append(
            "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
            % (
                event.pass_number if event.pass_number > 0 else "",
                escape(event.operation),
                _format_modes_change(event.modes_before, event.modes_after),
                residual,
                _format_decision(event.accepted),
                escape(note),
            )
        )
    rows.append("</table>")
    return "".join(rows)


def _format_simplification_summary(result: dict[str, Any]) -> str:
    return (
        "<b>BW spectrum simplification summary</b><br>"
        "<b>Initial modes</b>: %d<br>"
        "<b>Final modes</b>: %d<br>"
        "<b>Initial residual</b>: %s<br>"
        "<b>Final residual</b>: %s<br>"
        "<b>Simplification time</b>: %.3g s<br>"
        % (
            result["initial_nmodes"],
            int(len(result["tau"])),
            _format_residual(result["initial_residual"]),
            _format_residual(result["current_residual"]),
            result.get("elapsed_seconds", 0.0),
        )
    )


def read_maxwell_modes_file(path: str) -> tuple[FloatArray, FloatArray]:
    """Read positive Maxwell modes from a RepTate text file."""
    expected_modes: int | None = None
    modes: list[tuple[float, float]] = []
    with open(path, "r") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if line == "" or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) == 1 and expected_modes is None and len(modes) == 0:
                try:
                    expected_modes = int(parts[0])
                except ValueError as exc:
                    raise ValueError("Invalid number of modes on line %d" % line_number) from exc
                if expected_modes <= 0:
                    raise ValueError("Number of modes must be positive")
                continue
            if len(parts) == 3:
                tau_text, G_text = parts[1], parts[2]
            elif len(parts) == 2:
                tau_text, G_text = parts
            else:
                raise ValueError("Malformed Maxwell mode line %d" % line_number)
            try:
                tau_i = float(tau_text)
                G_i = float(G_text)
            except ValueError as exc:
                raise ValueError("Invalid Maxwell mode value on line %d" % line_number) from exc
            if tau_i <= 0.0 or G_i <= 0.0:
                raise ValueError("Maxwell modes must have positive tau_i and G_i values")
            modes.append((tau_i, G_i))

    if len(modes) == 0:
        raise ValueError("No Maxwell modes found")
    if expected_modes is not None and expected_modes != len(modes):
        raise ValueError("Expected %d modes but found %d data line(s)" % (expected_modes, len(modes)))
    tau = np.asarray([mode[0] for mode in modes], dtype=float)
    G = np.asarray([mode[1] for mode in modes], dtype=float)
    return tau, G


class TheoryBaumgaertelWinter(QTheory):
    r"""Fit a Baumgaertel-Winter discrete relaxation spectrum to dynamic moduli.

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
    is_time_domain: ClassVar[bool] = False
    is_retardation_domain: ClassVar[bool] = False
    last_load_modes_folder: ClassVar[str | None] = None

    def __init__(self, name: str = "", parent_dataset: DataSetLike | None = None, ax: AxesArray | None = None) -> None:
        """Constructor."""
        super().__init__(name, parent_dataset, ax)
        if self.is_retardation_domain:
            self.function = self.BaumgaertelWinterRetardation
        elif self.is_time_domain:
            self.function = self.BaumgaertelWinterTime
        else:
            self.function = self.BaumgaertelWinterFrequency
        self.has_modes = True
        self.MAX_MODES = 40
        self.view_modes = True
        if self.is_retardation_domain:
            self.min_logtau_separation = 0.12
            self.max_residual_increase = 0.005
            self.max_cumulative_residual_increase = 0.01
            self.weak_mode_threshold = 0.0
            self.allow_trial_deletion = False
        else:
            self.min_logtau_separation = 0.25
            self.max_residual_increase = 0.05
            self.max_cumulative_residual_increase = np.inf
            self.weak_mode_threshold = 1.0e-3
            self.allow_trial_deletion = True
        self.simplification_running = False
        self.simplification_cancel_requested = False
        self.simplification_thread: QThread | None = None
        self.simplification_worker: _BaumgaertelWinterSimplificationWorker | None = None
        self._last_minimized_mode_signature: tuple[Any, ...] | None = None
        self.mode_context_menu_cid: int | None = None

        xmin = self.parent_dataset.minpositivecol(0)
        xmax = self.parent_dataset.maxcol(0)
        nmodes = max(1, int(np.round(np.log10(xmax / xmin))))
        nmodes = min(nmodes, self.MAX_MODES)

        self.parameters["nmodes"] = Parameter(
            name="nmodes",
            value=nmodes,
            description="Number of Baumgaertel-Winter %s modes" % self._mode_family_name(),
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False,
            min_value=1,
            max_value=self.MAX_MODES,
        )
        if self.is_retardation_domain:
            self.parameters["logJini"] = Parameter(
                name="logJini",
                value=-4.0,
                description="Log of instantaneous compliance expressed in 1/Pa",
                type=ParameterType.real,
                opt_type=OptType.opt,
            )
            self.parameters["logeta0"] = Parameter(
                name="logeta0",
                value=0.0,
                description="Log of terminal viscosity expressed in Pa.s",
                type=ParameterType.real,
                opt_type=OptType.opt,
            )
        else:
            self.parameters["Ge"] = Parameter(
                name="Ge",
                value=0.0,
                description="Equilibrium modulus expressed in Pa; keep zero for viscoelastic liquids",
                type=ParameterType.real,
                opt_type=OptType.const,
                min_value=0.0,
            )

        tau = self._initial_tau(xmin, xmax, nmodes)
        mode_x = self._mode_x_from_tau(tau)
        G = self._initial_moduli(mode_x)

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
            mode_parameter = self._mode_parameter_name(i)
            self.parameters[mode_parameter] = Parameter(
                name=mode_parameter,
                value=float(np.log10(max(G[i], _LOG_FLOOR))),
                description=self._mode_parameter_description(i),
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
        self.tbutloadmodes = QToolButton()
        menu_button_popup: Any = getattr(QToolButton, "MenuButtonPopup")
        self.tbutloadmodes.setPopupMode(menu_button_popup)
        load_modes_menu = QMenu(self)
        self.load_modes_action = load_modes_menu.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-broadcasting.png"),
            "Load Modes",
        )
        self.get_modes_action = load_modes_menu.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-broadcasting.png"),
            "Get Modes",
        )
        self.tbutloadmodes.setDefaultAction(self.get_modes_action)
        self.tbutloadmodes.setMenu(load_modes_menu)
        tb.addWidget(self.tbutloadmodes)
        self.save_modes_action = tb.addAction(QIcon(":/Icon8/Images/new_icons/icons8-save-Maxwell.png"), "Save Modes")
        self.simplify_modes_action = tb.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-broom.png"),
            "Simplify BW spectrum",
        )
        self.configure_simplification_action = tb.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-maintenance.png"),
            "Configure BW simplification",
        )
        self.configure_simplification_action.setToolTip("Configure the Baumgaertel-Winter mode merging and deletion thresholds")
        self.simplify_modes_action.setToolTip("Merge close modes and remove redundant modes if the relative residual increase is small")
        self.modesaction.setCheckable(True)
        self.modesaction.setChecked(True)
        self.thToolsLayout.insertWidget(0, tb)

        self.spinbox.valueChanged.connect(self.handle_spinboxValueChanged)
        self.modesaction.triggered.connect(self.modesaction_change)
        self.load_modes_action.triggered.connect(self.load_modes)
        self.get_modes_action.triggered.connect(self.get_modes_reptate)
        self.save_modes_action.triggered.connect(self.save_modes)
        self.simplify_modes_action.triggered.connect(self.simplify_spectrum)
        self.configure_simplification_action.triggered.connect(self.configure_simplification_parameters)

    def _initial_tau(self, xmin: float, xmax: float, nmodes: int) -> FloatArray:
        if self.is_time_domain or self.is_retardation_domain:
            if nmodes > 1:
                return _logspace(np.log10(xmin), np.log10(xmax), nmodes)
            return _logspace(np.log10(np.sqrt(xmin * xmax)), np.log10(np.sqrt(xmin * xmax)), nmodes)
        if nmodes > 1:
            return _logspace(-np.log10(xmax), -np.log10(xmin), nmodes)
        return _logspace(-np.log10(np.sqrt(xmin * xmax)), -np.log10(np.sqrt(xmin * xmax)), nmodes)

    def _mode_x_from_tau(self, tau: FloatArray) -> FloatArray:
        if self.is_time_domain or self.is_retardation_domain:
            return tau
        return 1.0 / np.maximum(tau, _LOG_FLOOR)

    def _initial_moduli(self, mode_x: FloatArray) -> FloatArray:
        data = self.parent_dataset.files[0].data_table.data
        x_data = data[:, 0]
        storage = np.abs(data[:, 1])
        if self.is_retardation_domain:
            try:
                stress = abs(float(self.parent_dataset.files[0].file_parameters["stress"]))
            except (ValueError, KeyError):
                self.Qprint("Invalid stress value")
                stress = 1.0
            if stress <= 0.0:
                self.Qprint("Invalid stress value")
                stress = 1.0
            modulus_scale = storage / stress
        elif not self.is_time_domain and data.shape[1] > 2:
            loss = np.abs(data[:, 2])
            modulus_scale = np.sqrt(storage**2 + loss**2)
        else:
            modulus_scale = storage
        return np.maximum(np.interp(mode_x, x_data, modulus_scale), _LOG_FLOOR)

    def _mode_family_name(self) -> str:
        if self.is_retardation_domain:
            return "retardation"
        return "Maxwell"

    def _mode_parameter_name(self, index: int) -> str:
        if self.is_retardation_domain:
            return "logJ%02d" % index
        return "logG%02d" % index

    def _mode_parameter_description(self, index: int) -> str:
        if self.is_retardation_domain:
            return "log10(J%02d) of Mode %d retardation compliance expressed in 1/Pa" % (index, index)
        return "log10(G%02d) of Mode %d relaxation strength expressed in Pa" % (index, index)

    def _mode_amplitude_label(self) -> str:
        if self.is_retardation_domain:
            return "J"
        return "G"

    def Qhide_theory_extras(self, state: bool) -> None:
        """Uncheck the modeaction button. Called when current theory is changed."""
        self.modesaction.setChecked(state)

    def modesaction_change(self, checked: bool) -> None:
        """Change visibility of modes."""
        self.graphicmodes_visible(checked)

    def handle_spinboxValueChanged(self, value: int) -> None:
        """Handle a change of the parameter 'nmodes'."""
        if self.simplification_running:
            self.spinbox.blockSignals(True)
            self.spinbox.setValue(self.parameter_int("nmodes"))
            self.spinbox.blockSignals(False)
            self.Qprint("Cannot change modes while BW spectrum simplification is running.")
            return
        self.set_param_value("nmodes", value)
        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()
        self.update_parameter_table()

    def set_param_value(self, name: str, value: Any) -> tuple[str, bool]:
        """Change mode parameters when nmodes changes; otherwise call parent."""
        mode_prefix = self._mode_parameter_name(0)[:-2]
        if self.simplification_running and (
            name == "nmodes" or name.startswith("logtau") or name.startswith(mode_prefix)
        ):
            return "Cannot change BW modes while spectrum simplification is running", False
        if name == "nmodes":
            nmodesold = self.parameter_int("nmodes")
            logtauold = np.zeros(nmodesold)
            logGold = np.zeros(nmodesold)
            for i in range(nmodesold):
                logtauold[i] = self.parameter_float("logtau%02d" % i)
                mode_parameter = self._mode_parameter_name(i)
                logGold[i] = self.parameter_float(mode_parameter)
                del self.parameters["logtau%02d" % i]
                del self.parameters[mode_parameter]

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
                mode_parameter = self._mode_parameter_name(i)
                self.parameters[mode_parameter] = Parameter(
                    mode_parameter,
                    float(logGnew[i]),
                    self._mode_parameter_description(i),
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

        if success and (
            name in ("nmodes", "Ge", "logJini", "logeta0")
            or name.startswith("logtau")
            or name.startswith(mode_prefix)
        ):
            self._invalidate_minimized_modes()
        return message, success

    def drag_mode(self, dx: Any, dy: Any) -> None:
        """Drag individual modes.

        In frequency-domain views, mode symbols are displayed at
        omega_i = 1/tau_i.  In time-domain views, mode symbols are displayed at
        tau_i.
        """
        dx, dy = self.convert_view_data_to_internal(dx, dy)
        nmodes = self.parameter_int("nmodes")

        if self.is_time_domain and self.current_view().log_x:
            logtau = _safe_log10(dx)
        elif self.is_time_domain:
            logtau = np.asarray(dx, dtype=float)
        elif self.current_view().log_x:
            logtau = -_safe_log10(dx)
        else:
            logtau = -np.asarray(dx, dtype=float)

        if self.current_view().log_y:
            log_amplitude = _safe_log10(dy)
        else:
            log_amplitude = np.asarray(dy, dtype=float)

        for i in range(nmodes):
            self.set_param_value("logtau%02d" % i, float(logtau[i]))
            self.set_param_value(self._mode_parameter_name(i), float(log_amplitude[i]))

        self.do_calculate("")
        self.update_parameter_table()

    def handle_mode_context_menu(self, event: Any) -> None:
        """Show a context menu for a BW mode marker."""
        if event.inaxes != self.graphicmodes.axes:
            return
        if event.button != 3:
            return
        if self.simplification_running:
            return
        contains, _ = self.graphicmodes.contains(event)
        if not contains:
            return
        if event.xdata is None or event.ydata is None:
            return

        mode_index = self._nearest_displayed_mode_index(float(event.xdata), float(event.ydata))
        if mode_index is None:
            return

        parent_application = self.parent_dataset.parent_application
        if hasattr(parent_application, "suppress_next_right_click_zoom"):
            parent_application.suppress_next_right_click_zoom()
        if getattr(event, "guiEvent", None) is not None:
            event.guiEvent.accept()

        menu = QMenu(self)
        delete_action = menu.addAction("Delete Mode %d" % mode_index)
        delete_action.setEnabled(self.parameter_int("nmodes") > 1)
        action = menu.exec(QCursor.pos())
        if action == delete_action:
            self.delete_mode(mode_index)
            parent_application.clear_suppressed_right_click_zoom()

    def _nearest_displayed_mode_index(self, x: float, y: float) -> int | None:
        """Return the nearest displayed mode marker index to an axes coordinate."""
        xdata_raw, ydata_raw = self.graphicmodes.get_data()
        xdata = np.asarray(xdata_raw, dtype=float)
        ydata = np.asarray(ydata_raw, dtype=float)
        if xdata.ndim > 1:
            xdata = xdata[:, 0]
        if ydata.ndim > 1:
            ydata = ydata[:, 0]
        if xdata.size == 0 or ydata.size == 0:
            return None

        view = self.current_view()
        if view.log_x:
            xdist = _safe_log10(xdata) - np.log10(max(x, _LOG_FLOOR))
        else:
            xdist = xdata - x
        if view.log_y:
            ydist = _safe_log10(ydata) - np.log10(max(y, _LOG_FLOOR))
        else:
            ydist = ydata - y
        return int(np.argmin(xdist**2 + ydist**2))

    def delete_mode(self, mode_index: int) -> None:
        """Delete one independent BW mode and refresh the theory."""
        tau, amplitude = self._mode_values()
        if tau.size <= 1:
            self.Qprint("Cannot delete the last BW mode.")
            return
        if mode_index < 0 or mode_index >= tau.size:
            return

        self._set_mode_values(np.delete(tau, mode_index), np.delete(amplitude, mode_index))
        self.do_calculate("")
        self.plot_theory_stuff()
        self.update_parameter_table()
        self.parent_dataset.parent_application.update_plot()

    def update_modes(self) -> None:
        """Do nothing."""
        pass

    def configure_simplification_parameters(self) -> None:
        """Show a dialog to configure BW mode simplification thresholds."""
        if self.simplification_running:
            self.Qprint("Cannot configure BW simplification while it is running.")
            return
        dialog = QDialog(self)
        dialog.setWindowTitle("Baumgaertel-Winter simplification")

        layout = QFormLayout(dialog)

        min_sep_spinbox = QDoubleSpinBox(dialog)
        min_sep_spinbox.setDecimals(3)
        min_sep_spinbox.setRange(0.0, 10.0)
        min_sep_spinbox.setSingleStep(0.05)
        min_sep_spinbox.setValue(float(self.min_logtau_separation))
        min_sep_spinbox.setToolTip("Minimum separation between mode times in log10 decades before two modes are merged")

        max_increase_spinbox = QDoubleSpinBox(dialog)
        max_increase_spinbox.setDecimals(4)
        max_increase_spinbox.setRange(0.0, 10.0)
        max_increase_spinbox.setSingleStep(0.01)
        max_increase_spinbox.setValue(float(self.max_residual_increase))
        max_increase_spinbox.setToolTip("Maximum accepted relative increase of the mean square relative residual after deleting one mode")

        max_cumulative_increase_spinbox = QDoubleSpinBox(dialog)
        max_cumulative_increase_spinbox.setDecimals(4)
        max_cumulative_increase_spinbox.setRange(0.0, 10.0)
        max_cumulative_increase_spinbox.setSingleStep(0.01)
        if np.isfinite(self.max_cumulative_residual_increase):
            max_cumulative_increase_spinbox.setValue(float(self.max_cumulative_residual_increase))
        else:
            max_cumulative_increase_spinbox.setValue(10.0)
        max_cumulative_increase_spinbox.setToolTip("Maximum accepted residual increase relative to the initial simplified spectrum")

        weak_mode_spinbox = QDoubleSpinBox(dialog)
        weak_mode_spinbox.setDecimals(6)
        weak_mode_spinbox.setRange(0.0, 1.0)
        weak_mode_spinbox.setSingleStep(1.0e-4)
        weak_mode_spinbox.setValue(float(self.weak_mode_threshold))
        weak_mode_spinbox.setToolTip(
            "Remove modes with %s_i smaller than this fraction of the total mode strength; use 0 to disable"
            % self._mode_amplitude_label()
        )

        trial_deletion_checkbox = QCheckBox(dialog)
        trial_deletion_checkbox.setChecked(bool(self.allow_trial_deletion))
        trial_deletion_checkbox.setToolTip("Allow residual-guarded deletion of the best single mode even when it is not amplitude-weak")

        layout.addRow("Minimum log(tau) separation / decades", min_sep_spinbox)
        layout.addRow("Maximum step residual increase", max_increase_spinbox)
        layout.addRow("Maximum cumulative residual increase", max_cumulative_increase_spinbox)
        layout.addRow("Weak-mode threshold", weak_mode_spinbox)
        layout.addRow("Allow trial deletion", trial_deletion_checkbox)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.min_logtau_separation = float(min_sep_spinbox.value())
            self.max_residual_increase = float(max_increase_spinbox.value())
            self.max_cumulative_residual_increase = float(max_cumulative_increase_spinbox.value())
            self.weak_mode_threshold = float(weak_mode_spinbox.value())
            self.allow_trial_deletion = bool(trial_deletion_checkbox.isChecked())

    def load_modes(self) -> None:
        """Load independent BW modes from a text file."""
        if self.simplification_running:
            self.Qprint("Cannot load modes while BW spectrum simplification is running.")
            return
        start_folder = self.last_load_modes_folder or os.path.join(RepTate.root_dir, "data")
        fpath, _ = QFileDialog.getOpenFileName(
            self,
            "Load %s modes from a text file" % self._mode_family_name(),
            start_folder,
            "Text (*.txt);;All files (*)",
        )
        if fpath == "":
            return
        type(self).last_load_modes_folder = os.path.dirname(fpath)
        try:
            tau, G = self._read_modes_file(fpath)
            if tau.size > self.MAX_MODES:
                raise ValueError("Loaded %d modes, but the maximum is %d" % (tau.size, self.MAX_MODES))
            self._set_mode_values(tau, G)
        except Exception as exc:
            self.Qprint("<font color=red><b>Could not load %s modes:</b></font> %s" % (self._mode_family_name(), exc))
            QMessageBox.warning(self, "Load %s modes" % self._mode_family_name(), str(exc))
            return

        self.update_parameter_table()
        self.do_calculate("")
        self.plot_theory_stuff()
        self.parent_dataset.parent_application.update_plot()
        self.Qprint(
            "<font color=red><b>Loaded %d %s modes from %s.</b></font>"
            % (tau.size, self._mode_family_name(), os.path.basename(fpath))
        )

    def get_modes_reptate(self) -> None:
        """Get modes from another open RepTate theory."""
        if self.simplification_running:
            self.Qprint("Cannot get modes while BW spectrum simplification is running.")
            return
        self.Qcopy_modes()

    def save_modes(self) -> None:
        """Save independent BW modes to a text file."""
        fpath, _ = QFileDialog.getSaveFileName(
            self,
            "Save %s modes to a text file" % self._mode_family_name(),
            os.path.join(RepTate.root_dir, "data"),
            "Text (*.txt)",
        )
        if fpath == "":
            self.logger.debug("Save modes cancelled: theory=%s thname=%s", self.name, self.thname)
            return

        times, amplitudes, success = self.get_modes()
        if not success:
            self.logger.warning("Could not get modes correctly for %s", self.name)
            return

        self.logger.debug(
            "Saving modes: theory=%s thname=%s path=%s modes=%d",
            self.name,
            self.thname,
            fpath,
            len(times),
        )
        with open(fpath, "w") as f:
            version = RepTate.__version__.split("+")[0]
            try:
                build = RepTate.__version__.split("+")[1]
            except IndexError:
                build = ""
            f.write("# %s modes\n" % self._mode_family_name().capitalize())
            f.write("# Generated with RepTate %s  (build %s)\n" % (version, build))
            f.write("# At %s on %s\n" % (time.strftime("%X"), time.strftime("%a %b %d, %Y")))
            f.write("\n#number of modes\n")
            f.write("%d\n" % len(times))
            f.write("\n#%4s\t%15s\t%15s\n" % ("i", "tau_i", "%s_i" % self._mode_amplitude_label()))
            for i, (tau_i, amplitude_i) in enumerate(zip(times, amplitudes), start=1):
                f.write("%5d\t%15g\t%15g\n" % (i, tau_i, amplitude_i))

    def do_fit(self, line: str) -> None:
        """Minimize BW modes and remember that this exact state is fitted."""
        self._invalidate_minimized_modes()
        nfev_before = self.nfev
        super().do_fit(line)
        if self.nfev > nfev_before and not self.is_fitting:
            self._mark_modes_minimized()

    def _read_modes_file(self, path: str) -> tuple[FloatArray, FloatArray]:
        """Read Maxwell modes from a text file."""
        return read_maxwell_modes_file(path)

    def setup_graphic_modes(self) -> None:
        """Setup graphic helpers."""
        omega, G = self._mode_marker_data()
        self.graphicmodes = self.ax.plot(omega, G)[0]
        self.graphicmodes.set_marker("D")
        self.graphicmodes.set_linestyle("")
        self.graphicmodes.set_visible(self.view_modes)
        self.graphicmodes.set_markerfacecolor("orange")
        self.graphicmodes.set_markeredgecolor("black")
        self.graphicmodes.set_markeredgewidth(3)
        self.graphicmodes.set_markersize(8)
        self.graphicmodes.set_alpha(0.5)
        self.artistmodes = DraggableModeIndividual(
            self.graphicmodes,
            DragType.both,
            self.parent_dataset.parent_application,
            self.drag_mode,
        )
        self.mode_context_menu_cid = self.graphicmodes.figure.canvas.mpl_connect(
            "button_press_event",
            self.handle_mode_context_menu,
        )
        self.plot_theory_stuff()

    def destructor(self) -> None:
        """Called when the theory tab is closed."""
        if self.simplification_running:
            self._request_simplification_cancel()
        if self.mode_context_menu_cid is not None:
            self.graphicmodes.figure.canvas.mpl_disconnect(self.mode_context_menu_cid)
            self.mode_context_menu_cid = None
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
            G[i] = np.power(10.0, self.parameter_float(self._mode_parameter_name(i)))
        return tau, G

    def _mode_fit_signature(self, file: FileLike | None = None) -> tuple[Any, ...]:
        """Return a compact signature for the current BW fit state."""
        tau, G = self._mode_values()
        if file is None:
            file = self._first_valid_file()
        file_id = id(file) if file is not None else None
        return (
            file_id,
            self.is_time_domain,
            self.is_retardation_domain,
            self.parameter_int("nmodes"),
            tuple(np.round(tau, decimals=14)),
            tuple(np.round(G, decimals=14)),
            round(self.parameter_float("Ge"), 14) if "Ge" in self.parameters else None,
            round(self.parameter_float("logJini"), 14) if "logJini" in self.parameters else None,
            round(self.parameter_float("logeta0"), 14) if "logeta0" in self.parameters else None,
        )

    def _mark_modes_minimized(self) -> None:
        self._last_minimized_mode_signature = self._mode_fit_signature()

    def _invalidate_minimized_modes(self) -> None:
        self._last_minimized_mode_signature = None

    def _mode_marker_data(self) -> tuple[FloatArray, FloatArray]:
        tau, G = self._mode_values()
        return self._mode_x_from_tau(tau), G

    def _first_valid_file(self) -> FileLike | None:
        """Return the first data file with enough columns for this domain."""
        min_columns = 2 if self.is_time_domain or self.is_retardation_domain else 3
        for file in self.parent_dataset.files:
            data = file.data_table.data
            if data is not None and data.ndim == 2 and data.shape[1] >= min_columns and data.shape[0] > 0:
                if self.is_retardation_domain:
                    try:
                        self._file_stress(file)
                    except (ValueError, KeyError):
                        continue
                return file
        return None

    def _pack_modes(self, tau: FloatArray, G: FloatArray) -> FloatArray:
        """Pack positive mode parameters into logarithmic optimization variables."""
        return np.r_[_safe_log10(tau), _safe_log10(G)]

    def _unpack_modes(self, variables: FloatArray) -> tuple[FloatArray, FloatArray]:
        """Unpack logarithmic optimization variables into positive mode parameters."""
        nmodes = len(variables) // 2
        tau = np.power(10.0, variables[:nmodes])
        G = np.power(10.0, variables[nmodes:])
        return tau, G

    def _predict_dynamic_moduli(self, omega: FloatArray, tau: FloatArray, G: FloatArray) -> tuple[FloatArray, FloatArray]:
        """Predict G' and G'' for a given discrete relaxation spectrum."""
        omega = np.asarray(omega, dtype=float)
        Gp = np.full_like(omega, self.parameter_float("Ge"), dtype=float)
        Gpp = np.zeros_like(omega, dtype=float)
        for tau_i, G_i in zip(tau, G):
            wt = omega * tau_i
            wt2 = wt**2
            denominator = 1.0 + wt2
            Gp += G_i * wt2 / denominator
            Gpp += G_i * wt / denominator
        return Gp, Gpp

    def _predict_relaxation_modulus(self, time: FloatArray, tau: FloatArray, G: FloatArray, gamma: float) -> FloatArray:
        """Predict G(t) or stress relaxation for a discrete relaxation spectrum."""
        time = np.asarray(time, dtype=float)
        Gt = np.full_like(time, self.parameter_float("Ge"), dtype=float)
        for tau_i, G_i in zip(tau, G):
            Gt += G_i * np.exp(-time / tau_i)
        return Gt * gamma

    def _predict_creep_strain(self, file: FileLike, time: FloatArray, tau: FloatArray, J: FloatArray) -> FloatArray:
        """Predict creep strain for a discrete retardation spectrum."""
        time = np.asarray(time, dtype=float)
        stress = self._file_stress(file)
        Jt = np.full_like(time, np.power(10.0, self.parameter_float("logJini")), dtype=float)
        for tau_i, J_i in zip(tau, J):
            Jt += J_i * (1.0 - np.exp(-time / tau_i))
        if self._file_recovery_flag(file) != 1:
            Jt += time / np.power(10.0, self.parameter_float("logeta0"))
        return stress * Jt

    def _file_gamma(self, file: FileLike) -> float:
        value = file.file_parameters.get("gamma")
        if value is None:
            return 1.0
        gamma = float(value)
        if gamma == 0.0:
            return 1.0
        return gamma

    def _file_stress(self, file: FileLike) -> float:
        stress = float(file.file_parameters["stress"])
        if stress == 0.0:
            raise ValueError("stress must be non-zero")
        return stress

    def _file_recovery_flag(self, file: FileLike) -> int:
        try:
            return int(file.file_parameters["rec"])
        except (ValueError, KeyError):
            return 0

    def _residual_vector_for_modes(self, file: FileLike, tau: FloatArray, G: FloatArray) -> FloatArray:
        """Return the Baumgaertel-Winter relative residual vector for one file."""
        data = file.data_table.data
        if self.is_retardation_domain:
            time = np.asarray(data[:, 0], dtype=float)
            strain_exp = np.asarray(data[:, 1], dtype=float)
            valid = (time >= 0.0) & (np.abs(strain_exp) > _LOG_FLOOR)
            if not np.any(valid):
                return np.array([], dtype=float)
            try:
                strain_fit = self._predict_creep_strain(file, time[valid], tau, G)
            except (ValueError, KeyError):
                return np.array([], dtype=float)
            return strain_fit / strain_exp[valid] - 1.0

        if self.is_time_domain:
            time = np.asarray(data[:, 0], dtype=float)
            Gt_exp = np.asarray(data[:, 1], dtype=float)
            valid = (time >= 0.0) & (Gt_exp > 0.0)
            if not np.any(valid):
                return np.array([], dtype=float)
            Gt_fit = self._predict_relaxation_modulus(time[valid], tau, G, self._file_gamma(file))
            return Gt_fit / Gt_exp[valid] - 1.0

        omega = np.asarray(data[:, 0], dtype=float)
        Gp_exp = np.asarray(data[:, 1], dtype=float)
        Gpp_exp = np.asarray(data[:, 2], dtype=float)
        valid = (omega > 0.0) & (Gp_exp > 0.0) & (Gpp_exp > 0.0)
        if not np.any(valid):
            return np.array([], dtype=float)
        Gp_fit, Gpp_fit = self._predict_dynamic_moduli(omega[valid], tau, G)
        return np.r_[Gp_fit / Gp_exp[valid] - 1.0, Gpp_fit / Gpp_exp[valid] - 1.0]

    def _residual_value_for_modes(self, file: FileLike, tau: FloatArray, G: FloatArray) -> float:
        """Return the mean square Baumgaertel-Winter relative residual."""
        residual = self._residual_vector_for_modes(file, tau, G)
        if residual.size == 0:
            return np.inf
        return float(np.mean(residual**2))

    def _check_simplification_cancelled(self) -> None:
        if self.simplification_cancel_requested:
            raise _SimplificationCancelled

    def _fit_modes_to_file(self, file: FileLike, tau: FloatArray, G: FloatArray) -> tuple[FloatArray, FloatArray, float]:
        """Refit tau and G for a fixed number of modes using scipy least_squares."""
        self._check_simplification_cancelled()
        x0 = self._pack_modes(tau, G)

        def residual_from_variables(variables: FloatArray) -> FloatArray:
            self._check_simplification_cancelled()
            tau_trial, G_trial = self._unpack_modes(variables)
            return self._residual_vector_for_modes(file, tau_trial, G_trial)

        result = least_squares(
            residual_from_variables,
            x0,
            method="trf",
            max_nfev=4000,
            xtol=1.0e-10,
            ftol=1.0e-10,
            gtol=1.0e-10,
        )
        tau_fit, G_fit = self._unpack_modes(result.x)
        residual = self._residual_value_for_modes(file, tau_fit, G_fit)
        order = np.argsort(tau_fit)
        self._check_simplification_cancelled()
        return tau_fit[order], G_fit[order], residual

    def _set_mode_values(self, tau: FloatArray, G: FloatArray) -> None:
        """Replace the current mode parameters by the supplied mode arrays."""
        self._invalidate_minimized_modes()
        tau = np.asarray(tau, dtype=float)
        G = np.asarray(G, dtype=float)
        if tau.size != G.size:
            raise ValueError("tau and %s must have the same length" % self._mode_amplitude_label())
        if tau.size < 1:
            raise ValueError("At least one mode is required")
        if tau.size > self.MAX_MODES:
            raise ValueError("Number of modes must be no larger than %d" % self.MAX_MODES)
        if np.any(tau <= 0.0) or np.any(G <= 0.0):
            raise ValueError("tau and %s mode values must be positive" % self._mode_amplitude_label())
        nmodes_old = self.parameter_int("nmodes")
        for i in range(nmodes_old):
            self.parameters.pop("logtau%02d" % i, None)
            self.parameters.pop(self._mode_parameter_name(i), None)

        nmodes_new = int(tau.size)
        super().set_param_value("nmodes", nmodes_new)
        order = np.argsort(tau)
        tau = tau[order]
        G = G[order]
        for i in range(nmodes_new):
            self.parameters["logtau%02d" % i] = Parameter(
                "logtau%02d" % i,
                float(np.log10(max(tau[i], _LOG_FLOOR))),
                "Log of Mode %d relaxation time" % i,
                ParameterType.real,
                opt_type=OptType.opt,
                min_value=-30,
                max_value=30,
            )
            mode_parameter = self._mode_parameter_name(i)
            self.parameters[mode_parameter] = Parameter(
                mode_parameter,
                float(np.log10(max(G[i], _LOG_FLOOR))),
                self._mode_parameter_description(i),
                ParameterType.real,
                opt_type=OptType.opt,
                min_value=-30,
                max_value=30,
            )
        self.spinbox.blockSignals(True)
        self.spinbox.setValue(nmodes_new)
        self.spinbox.blockSignals(False)

    def set_modes(self, tau: Any, G: Any) -> bool:
        """Set independent modes in this theory."""
        try:
            self._set_mode_values(tau, G)
        except ValueError as exc:
            self.Qprint("<font color=red><b>Could not set %s modes:</b></font> %s" % (self._mode_family_name(), exc))
            return False
        return True

    def _merge_close_mode_arrays(self, tau: FloatArray, G: FloatArray) -> tuple[FloatArray, FloatArray, int]:
        """Merge modes separated by less than min_logtau_separation decades."""
        if tau.size <= 1:
            return tau, G, 0
        order = np.argsort(tau)
        logtau = _safe_log10(tau[order])
        G_sorted = G[order]
        merged_logtau: list[float] = []
        merged_G: list[float] = []
        n_merged = 0
        i = 0
        while i < len(logtau):
            group = [i]
            j = i + 1
            while j < len(logtau) and logtau[j] - logtau[group[-1]] < self.min_logtau_separation:
                group.append(j)
                j += 1
            weights = G_sorted[group]
            total_G = float(np.sum(weights))
            if total_G > 0.0:
                new_logtau = float(np.sum(weights * logtau[group]) / total_G)
            else:
                new_logtau = float(np.mean(logtau[group]))
            merged_logtau.append(new_logtau)
            merged_G.append(max(total_G, _LOG_FLOOR))
            n_merged += len(group) - 1
            i = j
        return np.power(10.0, np.asarray(merged_logtau)), np.asarray(merged_G), n_merged

    def _weak_mode_indices(self, G: FloatArray) -> list[int]:
        """Return indices of modes that are weak by amplitude only.

        A small amplitude alone is not enough to delete a mode: a weak mode can
        still dominate a part of the frequency window.  The returned indices are
        therefore only candidates for residual-guarded deletion.
        """
        if self.is_retardation_domain:
            return []
        if G.size <= 1 or self.weak_mode_threshold <= 0.0:
            return []
        total_G = float(np.sum(G))
        if total_G <= 0.0:
            return []
        keep = G >= self.weak_mode_threshold * total_G
        if not np.any(keep):
            keep[np.argmax(G)] = True
        return [int(i) for i in np.flatnonzero(~keep)]

    def _residual_increase_is_acceptable(self, old_residual: float, new_residual: float) -> bool:
        """Return True if a simplified spectrum is still an acceptable fit.

        The residual can be extremely small for synthetic or very clean data.  In
        that case, using old_residual itself as denominator makes the relative
        increase test numerically meaningless.  The floor prevents deletion of
        physically necessary modes from an almost exact fit while still allowing
        harmless simplifications.
        """
        if not np.isfinite(new_residual):
            return False
        if new_residual <= old_residual:
            return True
        residual_floor = max(old_residual, 1.0e-8)
        relative_increase = (new_residual - old_residual) / residual_floor
        return bool(relative_increase <= self.max_residual_increase)

    def _cumulative_residual_increase_is_acceptable(self, initial_residual: float, new_residual: float) -> bool:
        """Return True if a simplified spectrum remains close to the initial fit."""
        if not np.isfinite(new_residual):
            return False
        if new_residual <= initial_residual:
            return True
        if not np.isfinite(self.max_cumulative_residual_increase):
            return True
        residual_floor = max(initial_residual, 1.0e-8)
        relative_increase = (new_residual - initial_residual) / residual_floor
        return bool(relative_increase <= self.max_cumulative_residual_increase)

    def _simplification_residual_is_acceptable(
        self,
        current_residual: float,
        initial_residual: float,
        new_residual: float,
    ) -> bool:
        """Apply both local and cumulative residual guards."""
        return self._residual_increase_is_acceptable(
            current_residual,
            new_residual,
        ) and self._cumulative_residual_increase_is_acceptable(initial_residual, new_residual)

    def _best_single_mode_removal(
        self,
        file: FileLike,
        tau: FloatArray,
        G: FloatArray,
        current_residual: float,
        candidate_indices: list[int] | None = None,
    ) -> tuple[FloatArray, FloatArray, float, bool, int | None]:
        """Try removing candidate modes and keep the least damaging refitted spectrum."""
        if tau.size <= 1:
            return tau, G, current_residual, False, None
        if candidate_indices is None:
            candidate_indices = list(range(tau.size))
        candidate_indices = [i for i in candidate_indices if 0 <= i < tau.size]
        if len(candidate_indices) == 0:
            return tau, G, current_residual, False, None

        best_tau = tau
        best_G = G
        best_residual = np.inf
        best_removed_index: int | None = None
        for i in candidate_indices:
            self._check_simplification_cancelled()
            tau_trial = np.delete(tau, i)
            G_trial = np.delete(G, i)
            tau_fit, G_fit, residual = self._fit_modes_to_file(file, tau_trial, G_trial)
            if residual < best_residual:
                best_tau = tau_fit
                best_G = G_fit
                best_residual = residual
                best_removed_index = int(i)
        accept = self._residual_increase_is_acceptable(current_residual, best_residual)
        return best_tau, best_G, best_residual, accept, best_removed_index

    def simplify_spectrum(self) -> None:
        """Conservatively merge/delete redundant BW modes and refit the result."""
        if self.simplification_running:
            self._request_simplification_cancel()
            return
        if self.thread_calc_busy or self.thread_fit_busy or self.calculate_is_busy or self.is_fitting:
            self.Qprint("Busy calculating or minimizing theory...")
            return
        file = self._first_valid_file()
        if file is None:
            if self.is_retardation_domain:
                data_description = "creep"
            elif self.is_time_domain:
                data_description = "G(t)"
            else:
                data_description = "G', G''"
            QMessageBox.warning(self, "Baumgaertel-Winter", f"No valid {data_description} data file was found.")
            return

        tau, G = self._mode_values()
        skip_initial_fit = self._last_minimized_mode_signature == self._mode_fit_signature(file)
        self._set_simplification_running(True)
        thread = QThread()
        worker = _BaumgaertelWinterSimplificationWorker(self, file, tau.copy(), G.copy(), skip_initial_fit)
        self.simplification_thread = thread
        self.simplification_worker = worker
        worker.moveToThread(thread)
        worker.sig_done.connect(self._apply_simplification_result)
        worker.sig_done.connect(thread.quit)
        thread.started.connect(worker.work)
        thread.finished.connect(worker.deleteLater)
        thread.start()
        self.Qprint("<font color=red><b>Started BW spectrum simplification...</b></font>")
        if skip_initial_fit:
            self.Qprint("<font color=red><b>Skipping initial BW refit because the current modes were just minimized.</b></font>")

    def _simplify_spectrum_worker(
        self,
        file: FileLike,
        tau: FloatArray,
        G: FloatArray,
        skip_initial_fit: bool = False,
    ) -> dict[str, Any]:
        """Run BW simplification away from the GUI thread."""
        self._check_simplification_cancelled()
        # self.Qprint("<b>Started BW spectrum simplification...</b>")
        initial_modes_requested = int(tau.size)
        if skip_initial_fit:
            order = np.argsort(tau)
            tau = tau[order]
            G = G[order]
            current_residual = self._residual_value_for_modes(file, tau, G)
        else:
            tau, G, current_residual = self._fit_modes_to_file(file, tau, G)
        initial_nmodes = tau.size
        initial_residual = current_residual
        n_merged_total = 0
        n_weak_removed_total = 0
        n_deleted_total = 0
        report_events = [
            _SimplificationReportEvent(
                pass_number=0,
                operation="initial state" if skip_initial_fit else "initial fit",
                modes_before=initial_modes_requested,
                modes_after=int(tau.size),
                residual_before=current_residual,
                residual_after=current_residual,
                accepted=True,
                note="already minimized" if skip_initial_fit else "initial refit",
            )
        ]
        try:
            changed = True
            iteration = 0
            while changed and tau.size > 1:
                self._check_simplification_cancelled()
                iteration += 1
                self.Qprint("Pass %d: %d modes" % (iteration, tau.size))
                changed = False
                tau_merged, G_merged, n_merged = self._merge_close_mode_arrays(tau, G)
                if n_merged > 0:
                    self._check_simplification_cancelled()
                    modes_before = int(tau.size)
                    residual_before = current_residual
                    tau_fit, G_fit, merged_residual = self._fit_modes_to_file(file, tau_merged, G_merged)
                    if self._simplification_residual_is_acceptable(current_residual, initial_residual, merged_residual):
                        tau, G = tau_fit, G_fit
                        current_residual = merged_residual
                        n_merged_total += n_merged
                        changed = True
                        accepted = True
                        modes_after = int(tau.size)
                    else:
                        accepted = False
                        modes_after = int(tau_fit.size)
                    report_events.append(
                        _SimplificationReportEvent(
                            pass_number=iteration,
                            operation="close-mode merge",
                            modes_before=modes_before,
                            modes_after=modes_after,
                            residual_before=residual_before,
                            residual_after=merged_residual,
                            accepted=accepted,
                            note="%d close mode(s)" % n_merged,
                        )
                    )

                weak_candidates = self._weak_mode_indices(G)
                self._check_simplification_cancelled()
                tau_trial, G_trial, trial_residual, accept, removed_index = self._best_single_mode_removal(
                    file, tau, G, current_residual, weak_candidates
                )
                accept = accept and self._cumulative_residual_increase_is_acceptable(initial_residual, trial_residual)
                modes_before = int(tau.size)
                residual_before = current_residual
                if accept and tau_trial.size < tau.size:
                    tau, G = tau_trial, G_trial
                    current_residual = trial_residual
                    n_weak_removed_total += 1
                    changed = True
                    report_events.append(
                        _SimplificationReportEvent(
                            pass_number=iteration,
                            operation="weak-mode deletion",
                            modes_before=modes_before,
                            modes_after=int(tau.size),
                            residual_before=residual_before,
                            residual_after=trial_residual,
                            accepted=True,
                            note="removed weak mode",
                            mode_index=removed_index,
                        )
                    )
                    continue
                if weak_candidates:
                    report_events.append(
                        _SimplificationReportEvent(
                            pass_number=iteration,
                            operation="weak-mode deletion",
                            modes_before=modes_before,
                            modes_after=int(tau_trial.size),
                            residual_before=residual_before,
                            residual_after=trial_residual,
                            accepted=False,
                            note="best weak candidate rejected",
                            mode_index=removed_index,
                        )
                    )

                if self.allow_trial_deletion:
                    self._check_simplification_cancelled()
                    tau_trial, G_trial, trial_residual, accept, removed_index = self._best_single_mode_removal(
                        file,
                        tau,
                        G,
                        current_residual,
                    )
                    accept = accept and self._cumulative_residual_increase_is_acceptable(initial_residual, trial_residual)
                    modes_before = int(tau.size)
                    residual_before = current_residual
                    if accept and tau_trial.size < tau.size:
                        tau, G = tau_trial, G_trial
                        current_residual = trial_residual
                        n_deleted_total += 1
                        changed = True
                        report_events.append(
                            _SimplificationReportEvent(
                                pass_number=iteration,
                                operation="trial deletion",
                                modes_before=modes_before,
                                modes_after=int(tau.size),
                                residual_before=residual_before,
                                residual_after=trial_residual,
                                accepted=True,
                                note="removed best candidate",
                                mode_index=removed_index,
                            )
                        )
                    else:
                        report_events.append(
                            _SimplificationReportEvent(
                                pass_number=iteration,
                                operation="trial deletion",
                                modes_before=modes_before,
                                modes_after=int(tau_trial.size),
                                residual_before=residual_before,
                                residual_after=trial_residual,
                                accepted=False,
                                note="best candidate rejected",
                                mode_index=removed_index,
                            )
                        )
            self._check_simplification_cancelled()
        except _SimplificationCancelled:
            self.Qprint("BW simplification stopped after pass %d with %d accepted mode(s)." % (iteration, tau.size))
            return {
                "cancelled": True,
                "tau": tau,
                "G": G,
                "initial_nmodes": initial_nmodes,
                "n_merged_total": n_merged_total,
                "n_weak_removed_total": n_weak_removed_total,
                "n_deleted_total": n_deleted_total,
                "initial_residual": initial_residual,
                "current_residual": current_residual,
                "report_events": report_events,
                "has_candidate": True,
            }
        self.Qprint("BW simplification finished.")
        return {
            "cancelled": False,
            "tau": tau,
            "G": G,
            "initial_nmodes": initial_nmodes,
            "n_merged_total": n_merged_total,
            "n_weak_removed_total": n_weak_removed_total,
            "n_deleted_total": n_deleted_total,
            "initial_residual": initial_residual,
            "current_residual": current_residual,
            "report_events": report_events,
        }

    def _set_simplification_running(self, running: bool) -> None:
        """Enable/disable controls while BW simplification is running."""
        self.simplification_running = running
        self.simplification_cancel_requested = False
        self.spinbox.setDisabled(running)
        self.thParamTable.setDisabled(running)
        self.parent_dataset.actionCalculate_Theory.setDisabled(running)
        self.parent_dataset.actionMinimize_Error.setDisabled(running)
        self.save_modes_action.setDisabled(running)
        self.tbutloadmodes.setDisabled(running)
        self.configure_simplification_action.setDisabled(running)
        if running:
            self.simplify_modes_action.setIcon(QIcon(":/Icon8/Images/new_icons/icons8-stop-sign.png"))
            self.simplify_modes_action.setText("Cancel BW simplification")
            self.simplify_modes_action.setToolTip("Cancel the running Baumgaertel-Winter spectrum simplification")
        else:
            self.simplify_modes_action.setIcon(QIcon(":/Icon8/Images/new_icons/icons8-broom.png"))
            self.simplify_modes_action.setText("Simplify BW spectrum")
            self.simplify_modes_action.setToolTip("Merge close modes and remove redundant modes if the relative residual increase is small")

    def _request_simplification_cancel(self) -> None:
        """Request cancellation of the running BW simplification."""
        if not self.simplification_running:
            return
        self.simplification_cancel_requested = True
        self.Qprint("<font color=red><b>BW spectrum simplification cancellation requested</b></font>")

    def _apply_simplification_result(self, result: dict[str, Any]) -> None:
        """Apply the simplification result on the GUI thread."""
        run_final_minimize = False
        try:
            if result.get("cancelled"):
                if not result.get("has_candidate"):
                    self.Qprint("<font color=red><b>BW spectrum simplification cancelled before a fitted candidate was available.</b></font>")
                    return
                self.Qprint("<font color=red><b>BW spectrum simplification cancelled; applying latest accepted fitted candidate.</b></font>")
            if "error" in result:
                self.Qprint("<font color=red><b>BW spectrum simplification failed:</b></font> %s" % result["error"])
                return

            tau = result["tau"]
            G = result["G"]
            self._set_mode_values(tau, G)
            self.do_calculate("")
            self.plot_theory_stuff()
            self.update_parameter_table()
            self.parent_dataset.parent_application.update_plot()
            self.Qprint(_format_simplification_summary(result))
            self.Qprint(_format_simplification_report_table(result.get("report_events", [])))
            if result.get("cancelled"):
                self.Qprint(
                    "<font color=red><b>BW simplification cancelled by user. Applied latest accepted fitted candidate.</b></font>"
                )
            else:
                self.Qprint(
                    "<font color=red><b>BW simplification finished.</b></font>"
                )
            run_final_minimize = True
        finally:
            self._set_simplification_running(False)
            if self.simplification_thread is not None:
                self.simplification_thread.deleteLater()
            self.simplification_thread = None
            self.simplification_worker = None
        if run_final_minimize:
            self.Qprint("<font color=red><b>Running final Minimize Error with the simplified BW modes...</b></font>")
            self.parent_dataset.handle_actionMinimize_Error()

    #   QMessageBox.information(
    #       self,
    #       "Baumgaertel-Winter",
    #       (
    #           f"Spectrum simplified from {initial_nmodes} to {tau.size} modes.\n"
    #           f"Merged close modes: {n_merged_total}.\n"
    #           f"Removed weak modes: {n_weak_removed_total}.\n"
    #           f"Accepted trial deletions: {n_deleted_total}.\n"
    #           f"Final mean square relative residual: {current_residual:.4g}."
    #       ),
    #   )

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

    def BaumgaertelWinterTime(self, f: FileLike) -> None:
        """Calculate the time-domain Maxwell relaxation response."""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        if tt.num_columns <= 1:
            return

        value = f.file_parameters.get("gamma")
        if value is None:
            gamma = 1.0
        else:
            gamma = float(value)
            if gamma == 0.0:
                gamma = 1.0

        tau, G = self._mode_values()
        if tt.num_columns > 1:
            tt.data[:, 1] = self.parameter_float("Ge") * gamma

        for i in range(self.parameter_int("nmodes")):
            if self.stop_theory_flag:
                break
            tt.data[:, 1] += G[i] * np.exp(-tt.data[:, 0] / tau[i]) * gamma

    def BaumgaertelWinterRetardation(self, f: FileLike) -> None:
        """Calculate the time-domain creep response from independent retardation modes."""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        if tt.num_columns <= 1:
            return

        try:
            stress = self._file_stress(f)
        except (ValueError, KeyError):
            self.Qprint("Invalid stress value")
            return

        tau, J = self._mode_values()
        tt.data[:, 1] = stress * np.power(10.0, self.parameter_float("logJini"))
        for tau_i, J_i in zip(tau, J):
            if self.stop_theory_flag:
                break
            tt.data[:, 1] += stress * J_i * (1.0 - np.exp(-tt.data[:, 0] / tau_i))
        if self._file_recovery_flag(f) != 1:
            tt.data[:, 1] += stress * tt.data[:, 0] / np.power(10.0, self.parameter_float("logeta0"))

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


class TheoryBaumgaertelWinterTime(TheoryBaumgaertelWinter):
    r"""Fit a Baumgaertel-Winter discrete relaxation spectrum to G(t).

    * **Function**
        .. math::
            G(t) = G_e + \sum_{i=1}^{n_{modes}} g_i \exp(-t/\tau_i)

    The mode times :math:`\tau_i` and strengths :math:`g_i` are independent
    adjustable parameters, matching the frequency-domain Baumgaertel-Winter
    theory but evaluated in the time domain.
    """

    thname: ClassVar[str] = "Baumgaertel-Winter"
    description: ClassVar[str] = "Discrete relaxation spectrum from G(t)"
    html_help_file: ClassVar[str] = "http://reptate.readthedocs.io/manual/Applications/Gt/Theory/theory.html"
    is_time_domain: ClassVar[bool] = True


class TheoryBaumgaertelWinterRetardation(TheoryBaumgaertelWinter):
    r"""Fit a Baumgaertel-Winter discrete retardation spectrum to creep data.

    * **Function**
        .. math::
            \gamma(t) = \sigma_0 \left[
                J_0 + \sum_i J_i \left(1 - \exp(-t/\tau_i)\right)
                + \frac{t}{\eta_0}
            \right]

    The retardation times :math:`\tau_i` and compliances :math:`J_i` are
    independent adjustable parameters.
    """

    thname: ClassVar[str] = "Baumgaertel-Winter Retardation"
    description: ClassVar[str] = "Discrete retardation spectrum from creep data"
    html_help_file: ClassVar[str] = "http://reptate.readthedocs.io/manual/Applications/Creep/Theory/theory.html"
    single_file: ClassVar[bool] = False
    is_retardation_domain: ClassVar[bool] = True


TheoryBaumgaertelWinterFrequency = TheoryBaumgaertelWinter
