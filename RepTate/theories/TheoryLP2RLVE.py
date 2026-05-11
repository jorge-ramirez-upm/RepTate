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
"""LP2R linear viscoelastic theory backed by the pybind11 solver."""

import numpy as np
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QToolBar,
    QVBoxLayout,
)

from RepTate.core.Parameter import OptType, Parameter, ParameterType
from RepTate.gui.QTheory import QTheory
from RepTate.theories import _lp2r
from RepTate.theories.theory_helpers import GetMwdRepTate
from RepTate.tools.ToolMaterialsDatabase import (
    check_chemistry,
    get_single_parameter,
)


class LP2RAdvancedControlsDialog(QDialog):
    """Edit the LP2R resource-file style controls."""

    def __init__(self, parent, control_names):
        super().__init__(parent)
        self.parent_theory = parent
        self.edits = {}

        layout = QVBoxLayout()
        form = QFormLayout()
        for name in control_names:
            edit = QLineEdit()
            edit.setText("%g" % self.parent_theory.parameters[name].value)
            edit.setToolTip(self.parent_theory.parameters[name].description)
            self.edits[name] = edit
            form.addRow(name, edit)
        layout.addLayout(form)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        self.setLayout(layout)
        self.setWindowTitle("Advanced LP2R Controls")

    def values(self):
        return {name: float(edit.text()) for name, edit in self.edits.items()}


class TheoryLP2RLVE(QTheory):
    """Linear viscoelastic predictions from the LP2R solver.

    This first integration exposes one lognormal linear polymer component. RepTate
    owns GUI state and parameter handling, while the pybind11 solver owns the
    numerical relaxation and spectra calculation.
    """

    thname = "LP2R LVE"
    description = "Linear viscoelastic predictions of the LP2R model"
    citations = []
    html_help_file = "http://reptate.readthedocs.io/manual/Applications/LVE/Theory/theory.html"
    single_file = True
    INPUT_LOGNORMAL = 0
    INPUT_DISCRETE = 1
    ADVANCED_CONTROLS = [
        "alpha",
        "t_cr_start",
        "delta_cr",
        "b_zeta",
        "a_eq",
        "b_eq",
        "ret_pref",
        "ret_pref_0",
        "ret_switch_exponent",
        "rept_switch_factor",
        "rouse_switch_factor",
        "disentanglement_switch",
        "start_time",
        "time_ratio",
    ]

    def __init__(self, name="", parent_dataset=None, axarr=None):
        """Constructor."""
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate
        self.has_modes = False
        self.solver = None

        self.parameters["input_mode"] = Parameter(
            name="input_mode",
            value=self.INPUT_LOGNORMAL,
            description="Polymer input mode: 0=lognormal, 1=discrete masses/weights",
            type=ParameterType.discrete_integer,
            opt_type=OptType.const,
            discrete_values=[self.INPUT_LOGNORMAL, self.INPUT_DISCRETE],
        )

        self.parameters["Mw"] = Parameter(
            name="Mw",
            value=100.0,
            description="Weight-average molar mass of the lognormal component",
            type=ParameterType.real,
            opt_type=OptType.nopt,
            min_value=0,
            quantity="molar_mass",
            internal_unit="kg/mol",
            display_unit="kg/mol",
        )
        self.parameters["PDI"] = Parameter(
            name="PDI",
            value=1.05,
            description="Polydispersity index of the lognormal component",
            type=ParameterType.real,
            opt_type=OptType.nopt,
            min_value=1.0,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["n"] = Parameter(
            name="n",
            value=8,
            description="Number of lognormal bins",
            type=ParameterType.integer,
            opt_type=OptType.const,
            min_value=1,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["discrete_masses"] = Parameter(
            name="discrete_masses",
            value="50, 120",
            description="Discrete polymer masses in kg/mol",
            type=ParameterType.string,
            opt_type=OptType.const,
            display_flag=False,
        )
        self.parameters["discrete_weights"] = Parameter(
            name="discrete_weights",
            value="0.4, 0.6",
            description="Discrete polymer weights",
            type=ParameterType.string,
            opt_type=OptType.const,
            display_flag=False,
        )
        self.parameters["MK"] = Parameter(
            name="MK",
            value=0.5,
            description="Kuhn molar mass",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            quantity="molar_mass",
            internal_unit="kg/mol",
            display_unit="kg/mol",
        )
        self.parameters["Me"] = Parameter(
            name="Me",
            value=5.0,
            description="Entanglement molar mass",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            quantity="molar_mass",
            internal_unit="kg/mol",
            display_unit="kg/mol",
        )
        self.parameters["G0"] = Parameter(
            name="G0",
            value=2.0e5,
            description="Plateau modulus",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            quantity="stress",
            internal_unit="Pa",
            display_unit="Pa",
        )
        self.parameters["tau_e"] = Parameter(
            name="tau_e",
            value=1.0e-5,
            description="Entanglement time",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            quantity="time",
            internal_unit="s",
            display_unit="s",
        )
        self.parameters["G_glass"] = Parameter(
            name="G_glass",
            value=1.0e9,
            description="Glass modulus",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            quantity="stress",
            internal_unit="Pa",
            display_unit="Pa",
        )
        self.parameters["tau_glass"] = Parameter(
            name="tau_glass",
            value=1.0e-8,
            description="Glass relaxation time",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            quantity="time",
            internal_unit="s",
            display_unit="s",
        )
        self.parameters["beta_glass"] = Parameter(
            name="beta_glass",
            value=0.7,
            description="Glass KWW exponent",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            max_value=1,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["freq_ratio"] = Parameter(
            name="freq_ratio",
            value=1.2,
            description="Ratio between consecutive calculated frequencies",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=1.0,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["alpha"] = Parameter(
            name="alpha",
            value=1.0,
            description="LP2R constraint-release alpha parameter",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["t_cr_start"] = Parameter(
            name="t_cr_start",
            value=1.0,
            description="Constraint-release start time",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["delta_cr"] = Parameter(
            name="delta_cr",
            value=0.30,
            description="Fractional tube-constraint drop at CR events",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["b_zeta"] = Parameter(
            name="b_zeta",
            value=2.0,
            description="LP2R B_zeta resource parameter",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["a_eq"] = Parameter(
            name="a_eq",
            value=2.0,
            description="LP2R A_eq resource parameter",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["b_eq"] = Parameter(
            name="b_eq",
            value=10.0,
            description="LP2R B_eq resource parameter",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["ret_pref"] = Parameter(
            name="ret_pref",
            value=0.189,
            description="Long-time arm-retraction prefactor",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["ret_pref_0"] = Parameter(
            name="ret_pref_0",
            value=0.020,
            description="Short-time arm-retraction prefactor",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["ret_switch_exponent"] = Parameter(
            name="ret_switch_exponent",
            value=0.42,
            description="Arm-retraction prefactor switch exponent",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["rept_switch_factor"] = Parameter(
            name="rept_switch_factor",
            value=1.664,
            description="CLF-to-reptation switch factor",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["rouse_switch_factor"] = Parameter(
            name="rouse_switch_factor",
            value=1.5,
            description="Minimum bare entanglements for entangled dynamics",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["disentanglement_switch"] = Parameter(
            name="disentanglement_switch",
            value=1.0,
            description="LP2R disentanglement switch",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["start_time"] = Parameter(
            name="start_time",
            value=1.0e-3,
            description="Start time for LP2R relaxation integration",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["time_ratio"] = Parameter(
            name="time_ratio",
            value=1.02,
            description="Ratio between consecutive LP2R relaxation time steps",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=1.0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )

        self.get_material_parameters()
        self._read_mw_from_first_file()
        self.autocalculate = False

        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        self.get_mwd_action = tb.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-broadcasting.png"),
            "Get MWD (MWD app)",
        )
        self.advanced_controls_action = tb.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-maintenance.png"),
            "Advanced LP2R controls",
        )
        self.thToolsLayout.insertWidget(0, tb)
        self.advanced_controls_action.triggered.connect(self.edit_advanced_controls)
        self.get_mwd_action.triggered.connect(self.get_mwd_reptate)

    def edit_advanced_controls(self):
        """Open a dialog for the LP2R resource-file style controls."""
        dialog = LP2RAdvancedControlsDialog(self, self.ADVANCED_CONTROLS)
        if dialog.exec_():
            try:
                values = dialog.values()
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Advanced LP2R controls",
                    "All LP2R controls must be numeric.",
                )
                return
            for name, value in values.items():
                self.parameters[name].value = value

    def get_material_parameters(self):
        """Get common LP2R material parameters from the materials database."""
        success = super().get_material_parameters()
        if success:
            self._set_g0_from_material_ge()
        return success

    def _set_g0_from_material_ge(self):
        """Set LP2R G0 from the material database Ge value when available."""
        try:
            fparam = self.parent_dataset.files[0].file_parameters
            chem = fparam["chem"]
        except (AttributeError, IndexError, KeyError):
            return False
        dbindex = check_chemistry(chem)
        if dbindex < 0:
            return False
        ge, success = get_single_parameter(chem, "Ge", fparam, dbindex)
        if success:
            self.parameters["G0"].value = 0.8 * ge
            return True
        return False

    def _read_mw_from_first_file(self):
        """Use the first dataset file's Mw as the lognormal Mw when available."""
        try:
            mw = float(self.parent_dataset.files[0].file_parameters["Mw"])
        except (AttributeError, IndexError, KeyError, TypeError, ValueError):
            return False
        self.parameters["Mw"].value = mw
        return True

    def _clear_table(self, tt):
        """Leave the theory table empty after validation errors or cancellation."""
        tt.num_rows = 0
        tt.data = np.zeros((0, tt.num_columns))

    def _report_progress(self, progress, last_percent):
        """Report relaxation progress as GLaMM-style dash markers."""
        percent = int(100.0 * max(0.0, min(1.0, progress)))
        while percent >= last_percent + 10 and last_percent < 100:
            self.Qprint("-", end="")
            last_percent += 10
        QApplication.processEvents()
        return last_percent

    @staticmethod
    def _parse_number_list(value, name):
        """Parse a comma, semicolon, or whitespace separated list of floats."""
        tokens = str(value).replace(",", " ").replace(";", " ").split()
        if not tokens:
            raise ValueError("%s must contain at least one value" % name)
        try:
            return [float(token) for token in tokens]
        except ValueError as exc:
            raise ValueError("%s must contain only numbers" % name) from exc

    @classmethod
    def _parse_discrete_distribution(cls, masses_value, weights_value):
        """Parse and validate discrete mass and weight arrays."""
        masses = cls._parse_number_list(masses_value, "discrete_masses")
        weights = cls._parse_number_list(weights_value, "discrete_weights")
        if len(masses) != len(weights):
            raise ValueError("discrete_masses and discrete_weights must have the same length")
        if any(m <= 0 for m in masses):
            raise ValueError("discrete_masses values must be positive")
        if any(w <= 0 for w in weights):
            raise ValueError("discrete_weights values must be positive")
        if sum(weights) <= 0:
            raise ValueError("discrete_weights must have positive total weight")
        return masses, weights

    @staticmethod
    def _format_number_list(values):
        """Format numeric arrays for storage in string theory parameters."""
        return ", ".join("%.12g" % value for value in values)

    @classmethod
    def _normalise_discrete_distribution(cls, masses, weights):
        """Validate and normalize a discrete MWD in RepTate internal units."""
        masses = [float(mass) for mass in masses]
        weights = [float(weight) for weight in weights]
        if len(masses) != len(weights) or not masses:
            raise ValueError("MWD masses and weights must be non-empty and have the same length")
        if any(mass <= 0 for mass in masses):
            raise ValueError("MWD masses must be positive")
        if any(weight < 0 for weight in weights):
            raise ValueError("MWD weights must be non-negative")
        total_weight = sum(weights)
        if total_weight <= 0:
            raise ValueError("MWD weights must have positive total weight")
        return masses, [weight / total_weight for weight in weights]

    def set_discrete_distribution_from_mwd(self, masses, weights):
        """Populate LP2R discrete parameters from MWD masses and weights."""
        masses, weights = self._normalise_discrete_distribution(masses, weights)
        self.set_param_value("discrete_masses", self._format_number_list(masses))
        self.set_param_value("discrete_weights", self._format_number_list(weights))
        self.set_param_value("input_mode", self.INPUT_DISCRETE)
        self.update_parameter_table()
        self.Qprint("Got %d LP2R discrete MWD components" % len(masses))
        self.Qprint('<font color=green><b>Press "Calculate" to update theory</b></font>')

    def _collect_mwd_getters(self):
        """Collect available Discretize MWD theory outputs from RepTate apps."""
        apmng = self.parent_dataset.parent_application.parent_manager
        get_dict = {}
        for app in apmng.applications.values():
            app_index = apmng.ApplicationtabWidget.indexOf(app)
            app_tab_name = apmng.ApplicationtabWidget.tabText(app_index)
            for ds in app.datasets.values():
                ds_index = app.DataSettabWidget.indexOf(ds)
                ds_tab_name = app.DataSettabWidget.tabText(ds_index)
                for th in ds.theories.values():
                    th_index = ds.TheorytabWidget.indexOf(th)
                    th_tab_name = ds.TheorytabWidget.tabText(th_index)
                    if th.thname == "Discretize MWD":
                        get_dict[
                            "%s.%s.%s" % (app_tab_name, ds_tab_name, th_tab_name)
                        ] = th.get_mwd
        return get_dict

    def get_mwd_reptate(self):
        """Import discrete molecular weights from a Discretize MWD theory."""
        get_dict = self._collect_mwd_getters()
        if not get_dict:
            QMessageBox.warning(
                self, "Get MW distribution", 'No "Discretize MWD" theory found'
            )
            return

        dialog = GetMwdRepTate(self, get_dict, "Select Discretized MWD")
        if dialog.exec_() and dialog.btngrp.checkedButton() is not None:
            _, success1 = self.set_param_value("tau_e", dialog.taue_text.text())
            _, success2 = self.set_param_value("Me", dialog.Me_text.text())
            if not success1 * success2:
                self.Qprint("Could not understand Me or tau_e, try again")
                return
            item = dialog.btngrp.checkedButton().text()
            masses, weights = get_dict[item]()
            try:
                self.set_discrete_distribution_from_mwd(masses, weights)
            except ValueError as exc:
                self.Qprint("<font color=red><b>%s</b></font>" % exc)

    def _build_solver(self):
        """Create and configure a solver instance from the current parameters."""
        material = _lp2r.Material()
        material.m_kuhn = self.parameters["MK"].value * 1000.0
        material.m_e = self.parameters["Me"].value * 1000.0
        material.g0 = self.parameters["G0"].value
        material.tau_e = self.parameters["tau_e"].value
        material.g_glass = self.parameters["G_glass"].value
        material.tau_glass = self.parameters["tau_glass"].value
        material.beta_glass = self.parameters["beta_glass"].value

        controls = _lp2r.Controls()
        controls.alpha = self.parameters["alpha"].value
        controls.t_cr_start = self.parameters["t_cr_start"].value
        controls.delta_cr = self.parameters["delta_cr"].value
        controls.b_zeta = self.parameters["b_zeta"].value
        controls.a_eq = self.parameters["a_eq"].value
        controls.b_eq = self.parameters["b_eq"].value
        controls.ret_pref = self.parameters["ret_pref"].value
        controls.ret_pref_0 = self.parameters["ret_pref_0"].value
        controls.ret_switch_exponent = self.parameters["ret_switch_exponent"].value
        controls.rept_switch_factor = self.parameters["rept_switch_factor"].value
        controls.rouse_switch_factor = self.parameters["rouse_switch_factor"].value
        controls.disentanglement_switch = self.parameters["disentanglement_switch"].value
        controls.start_time = self.parameters["start_time"].value
        controls.time_ratio = self.parameters["time_ratio"].value

        solver = _lp2r.Solver(material, controls)
        if self.parameters["input_mode"].value == self.INPUT_DISCRETE:
            masses, weights = self._parse_discrete_distribution(
                self.parameters["discrete_masses"].value,
                self.parameters["discrete_weights"].value,
            )
            solver.add_discrete_component(
                mass=[mass * 1000.0 for mass in masses],
                weight=weights,
            )
        else:
            solver.add_lognormal_component(
                weight=1.0,
                n=self.parameters["n"].value,
                mw=self.parameters["Mw"].value * 1000.0,
                pdi=self.parameters["PDI"].value,
            )
        return solver

    def request_stop_computations(self):
        """Called when the user wants to terminate the current computation."""
        if self.solver is not None:
            self.solver.cancel()
        super().request_stop_computations()

    def do_error(self, line=""):
        """Calculate error by interpolating the generated LP2R spectrum."""
        self.do_error_interpolated(line="")

    def calculate(self, f=None):
        """Calculate LP2R G' and G'' over the active LVE frequency range."""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns

        omega_data = np.asarray(ft.data[:, 0], dtype=float)
        omega_data = omega_data[np.isfinite(omega_data) & (omega_data > 0)]
        if len(omega_data) == 0:
            self.Qprint("<font color=red><b>LP2R needs positive frequencies</b></font>")
            self._clear_table(tt)
            return

        freq_min = float(np.min(omega_data))
        freq_max = float(np.max(omega_data))
        freq_ratio = self.parameters["freq_ratio"].value
        if freq_ratio <= 1.0:
            self.Qprint("<font color=red><b>LP2R freq_ratio must be larger than 1</b></font>")
            self._clear_table(tt)
            return

        try:
            self.solver = self._build_solver()
            self.solver.prepare()
            last_progress = 0
            if not self.is_fitting:
                self.Qprint("LP2R relaxation:<br>  0% ", end="")
            while self.solver.step():
                if self.stop_theory_flag:
                    self.solver.cancel()
                    self._clear_table(tt)
                    self.Qprint(
                        "<br><font color=red><b>LP2R calculation cancelled</b></font>"
                    )
                    return
                if not self.is_fitting:
                    last_progress = self._report_progress(
                        self.solver.progress(), last_progress
                    )
                QApplication.processEvents()
            if self.solver.cancelled():
                self._clear_table(tt)
                self.Qprint(
                    "<br><font color=red><b>LP2R calculation cancelled</b></font>"
                )
                return
            if not self.is_fitting:
                while last_progress < 100:
                    self.Qprint("-", end="")
                    last_progress += 10
                self.Qprint(" 100%")
            result = self.solver.calculate_spectra(freq_min, freq_max, freq_ratio)
        except Exception as exc:
            self.Qprint("<font color=red><b>LP2R calculation failed: %s</b></font>" % exc)
            self._clear_table(tt)
            return
        finally:
            self.solver = None

        tt.num_rows = len(result.omega)
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = result.omega
        if tt.num_columns > 1:
            tt.data[:, 1] = result.gp
        if tt.num_columns > 2:
            tt.data[:, 2] = result.gpp
