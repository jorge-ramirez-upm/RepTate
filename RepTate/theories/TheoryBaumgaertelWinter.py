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
conversion to a retardation spectrum.  This implementation includes a conservative
mode-simplification helper, but the retardation spectrum is intentionally left for
a later implementation.
"""

from typing import Any, ClassVar

import numpy as np
from scipy.optimize import least_squares
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QDoubleSpinBox, QFormLayout, QMessageBox, QSpinBox, QToolBar

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

    def __init__(self, name: str = "", parent_dataset: DataSetLike | None = None, ax: AxesArray | None = None) -> None:
        """Constructor."""
        super().__init__(name, parent_dataset, ax)
        self.function = self.BaumgaertelWinterFrequency
        self.has_modes = True
        self.MAX_MODES = 40
        self.view_modes = True
        self.min_logtau_separation = 0.25
        self.max_residual_increase = 0.05
        self.weak_mode_threshold = 1.0e-3

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
        self.simplify_modes_action = tb.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-broom.png"),
            "Simplify BW spectrum",
        )
        self.configure_simplification_action = tb.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-maintenance.png"),
            "Configure BW simplification",
        )
        self.configure_simplification_action.setToolTip("Configure the Baumgaertel-Winter mode merging and deletion thresholds")
        self.save_modes_action = tb.addAction(QIcon(":/Icon8/Images/new_icons/icons8-save-Maxwell.png"), "Save Modes")
        self.simplify_modes_action.setToolTip("Merge close modes and remove redundant modes if the relative residual increase is small")
        self.modesaction.setCheckable(True)
        self.modesaction.setChecked(True)
        self.thToolsLayout.insertWidget(0, tb)

        self.spinbox.valueChanged.connect(self.handle_spinboxValueChanged)
        self.modesaction.triggered.connect(self.modesaction_change)
        self.save_modes_action.triggered.connect(self.save_modes)
        self.simplify_modes_action.triggered.connect(self.simplify_spectrum)
        self.configure_simplification_action.triggered.connect(self.configure_simplification_parameters)

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

    def configure_simplification_parameters(self) -> None:
        """Show a dialog to configure BW mode simplification thresholds."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Baumgaertel-Winter simplification")

        layout = QFormLayout(dialog)

        min_sep_spinbox = QDoubleSpinBox(dialog)
        min_sep_spinbox.setDecimals(3)
        min_sep_spinbox.setRange(0.0, 10.0)
        min_sep_spinbox.setSingleStep(0.05)
        min_sep_spinbox.setValue(float(self.min_logtau_separation))
        min_sep_spinbox.setToolTip("Minimum separation between relaxation times in log10 decades before two modes are merged")

        max_increase_spinbox = QDoubleSpinBox(dialog)
        max_increase_spinbox.setDecimals(4)
        max_increase_spinbox.setRange(0.0, 10.0)
        max_increase_spinbox.setSingleStep(0.01)
        max_increase_spinbox.setValue(float(self.max_residual_increase))
        max_increase_spinbox.setToolTip("Maximum accepted relative increase of the mean square relative residual after deleting one mode")

        weak_mode_spinbox = QDoubleSpinBox(dialog)
        weak_mode_spinbox.setDecimals(6)
        weak_mode_spinbox.setRange(0.0, 1.0)
        weak_mode_spinbox.setSingleStep(1.0e-4)
        weak_mode_spinbox.setValue(float(self.weak_mode_threshold))
        weak_mode_spinbox.setToolTip("Remove modes with G_i smaller than this fraction of the total mode strength")

        layout.addRow("Minimum log(tau) separation / decades", min_sep_spinbox)
        layout.addRow("Maximum residual increase", max_increase_spinbox)
        layout.addRow("Weak-mode threshold", weak_mode_spinbox)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.min_logtau_separation = float(min_sep_spinbox.value())
            self.max_residual_increase = float(max_increase_spinbox.value())
            self.weak_mode_threshold = float(weak_mode_spinbox.value())

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

    def _first_valid_file(self) -> FileLike | None:
        """Return the first data file with omega, G' and G'' columns."""
        for file in self.parent_dataset.files:
            data = file.data_table.data
            if data is not None and data.ndim == 2 and data.shape[1] >= 3 and data.shape[0] > 0:
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

    def _residual_vector_for_modes(self, file: FileLike, tau: FloatArray, G: FloatArray) -> FloatArray:
        """Return the Baumgaertel-Winter relative residual vector for one file."""
        data = file.data_table.data
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

    def _fit_modes_to_file(self, file: FileLike, tau: FloatArray, G: FloatArray) -> tuple[FloatArray, FloatArray, float]:
        """Refit tau and G for a fixed number of modes using scipy least_squares."""
        x0 = self._pack_modes(tau, G)

        def residual_from_variables(variables: FloatArray) -> FloatArray:
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
        return tau_fit[order], G_fit[order], residual

    def _set_mode_values(self, tau: FloatArray, G: FloatArray) -> None:
        """Replace the current mode parameters by the supplied mode arrays."""
        tau = np.asarray(tau, dtype=float)
        G = np.asarray(G, dtype=float)
        if tau.size != G.size:
            raise ValueError("tau and G must have the same length")
        nmodes_old = self.parameter_int("nmodes")
        for i in range(nmodes_old):
            self.parameters.pop("logtau%02d" % i, None)
            self.parameters.pop("logG%02d" % i, None)

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
            self.parameters["logG%02d" % i] = Parameter(
                "logG%02d" % i,
                float(np.log10(max(G[i], _LOG_FLOOR))),
                "Log of Mode %d relaxation strength" % i,
                ParameterType.real,
                opt_type=OptType.opt,
                min_value=-30,
                max_value=30,
            )
        self.spinbox.blockSignals(True)
        self.spinbox.setValue(nmodes_new)
        self.spinbox.blockSignals(False)

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

    def _best_single_mode_removal(
        self,
        file: FileLike,
        tau: FloatArray,
        G: FloatArray,
        current_residual: float,
        candidate_indices: list[int] | None = None,
    ) -> tuple[FloatArray, FloatArray, float, bool]:
        """Try removing candidate modes and keep the least damaging refitted spectrum."""
        if tau.size <= 1:
            return tau, G, current_residual, False
        if candidate_indices is None:
            candidate_indices = list(range(tau.size))
        candidate_indices = [i for i in candidate_indices if 0 <= i < tau.size]
        if len(candidate_indices) == 0:
            return tau, G, current_residual, False

        best_tau = tau
        best_G = G
        best_residual = np.inf
        for i in candidate_indices:
            tau_trial = np.delete(tau, i)
            G_trial = np.delete(G, i)
            tau_fit, G_fit, residual = self._fit_modes_to_file(file, tau_trial, G_trial)
            if residual < best_residual:
                best_tau = tau_fit
                best_G = G_fit
                best_residual = residual
        accept = self._residual_increase_is_acceptable(current_residual, best_residual)
        return best_tau, best_G, best_residual, accept

    def simplify_spectrum(self) -> None:
        """Conservatively merge/delete redundant BW modes and refit the result."""
        file = self._first_valid_file()
        if file is None:
            QMessageBox.warning(self, "Baumgaertel-Winter", "No valid G', G'' data file was found.")
            return

        tau, G = self._mode_values()
        tau, G, current_residual = self._fit_modes_to_file(file, tau, G)
        initial_nmodes = tau.size
        n_merged_total = 0
        n_weak_removed_total = 0
        n_deleted_total = 0

        changed = True
        while changed and tau.size > 1:
            changed = False
            tau_merged, G_merged, n_merged = self._merge_close_mode_arrays(tau, G)
            if n_merged > 0:
                tau_fit, G_fit, merged_residual = self._fit_modes_to_file(file, tau_merged, G_merged)
                if self._residual_increase_is_acceptable(current_residual, merged_residual):
                    tau, G = tau_fit, G_fit
                    current_residual = merged_residual
                    n_merged_total += n_merged
                    changed = True

            weak_candidates = self._weak_mode_indices(G)
            tau_trial, G_trial, trial_residual, accept = self._best_single_mode_removal(file, tau, G, current_residual, weak_candidates)
            if accept and tau_trial.size < tau.size:
                tau, G = tau_trial, G_trial
                current_residual = trial_residual
                n_weak_removed_total += 1
                changed = True
                continue

            tau_trial, G_trial, trial_residual, accept = self._best_single_mode_removal(file, tau, G, current_residual)
            if accept and tau_trial.size < tau.size:
                tau, G = tau_trial, G_trial
                current_residual = trial_residual
                n_deleted_total += 1
                changed = True

        self._set_mode_values(tau, G)
        self.do_calculate("")
        self.plot_theory_stuff()
        self.update_parameter_table()
        self.parent_dataset.parent_application.update_plot()
        self.Qprint(f"<font color=red><b>Spectrum simplified from {initial_nmodes} to {tau.size} modes.</b></font>")
        self.Qprint(f"<b>Merged close modes</b>: {n_merged_total}.")
        self.Qprint(f"<b>Removed weak modes</b>: {n_weak_removed_total}.")
        self.Qprint(f"<b>Accepted trial deletions</b>: {n_deleted_total}.")
        self.Qprint(f"<b>Final mean square relative residual</b>: {current_residual:.4g}.")

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
