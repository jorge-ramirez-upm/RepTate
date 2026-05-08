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
from PySide6.QtWidgets import QApplication

from RepTate.core.Parameter import OptType, Parameter, ParameterType
from RepTate.gui.QTheory import QTheory
from RepTate.theories import _lp2r


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

    def __init__(self, name="", parent_dataset=None, axarr=None):
        """Constructor."""
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate
        self.has_modes = False
        self.solver = None

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
        self.parameters["M_Kuhn"] = Parameter(
            name="M_Kuhn",
            value=0.5,
            description="Kuhn molar mass",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            quantity="molar_mass",
            internal_unit="kg/mol",
            display_unit="kg/mol",
        )
        self.parameters["M_e"] = Parameter(
            name="M_e",
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

    def _build_solver(self):
        """Create and configure a solver instance from the current parameters."""
        material = _lp2r.Material()
        material.m_kuhn = self.parameters["M_Kuhn"].value * 1000.0
        material.m_e = self.parameters["M_e"].value * 1000.0
        material.g0 = self.parameters["G0"].value
        material.tau_e = self.parameters["tau_e"].value
        material.g_glass = self.parameters["G_glass"].value
        material.tau_glass = self.parameters["tau_glass"].value
        material.beta_glass = self.parameters["beta_glass"].value

        controls = _lp2r.Controls()
        controls.alpha = self.parameters["alpha"].value
        controls.time_ratio = self.parameters["time_ratio"].value

        solver = _lp2r.Solver(material, controls)
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
            tt.num_rows = 0
            tt.data = np.zeros((0, tt.num_columns))
            return

        freq_min = float(np.min(omega_data))
        freq_max = float(np.max(omega_data))
        freq_ratio = self.parameters["freq_ratio"].value
        if freq_ratio <= 1.0:
            self.Qprint("<font color=red><b>LP2R freq_ratio must be larger than 1</b></font>")
            tt.num_rows = 0
            tt.data = np.zeros((0, tt.num_columns))
            return

        try:
            self.solver = self._build_solver()
            self.solver.prepare()
            while self.solver.step():
                if self.stop_theory_flag:
                    self.solver.cancel()
                    return
                QApplication.processEvents()
            if self.solver.cancelled():
                return
            result = self.solver.calculate_spectra(freq_min, freq_max, freq_ratio)
        except Exception as exc:
            self.Qprint("<font color=red><b>LP2R calculation failed: %s</b></font>" % exc)
            tt.num_rows = 0
            tt.data = np.zeros((0, tt.num_columns))
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
