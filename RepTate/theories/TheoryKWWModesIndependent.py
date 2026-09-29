"""Independent-time KWW modes for dielectric spectroscopy."""

from typing import Any, ClassVar

import numpy as np

from RepTate.core.Parameter import OptType, Parameter, ParameterType
from RepTate.core.typing import AxesArray, DataSetLike, FileLike, FloatArray
from RepTate.theories.TheoryBaumgaertelWinter import TheoryBaumgaertelWinter
from RepTate.theories.kww_ctypes_helper import kwwc, kwws


def _kww_values(omega: FloatArray, tau: float, beta: float) -> tuple[FloatArray, FloatArray]:
    """Return the cosine and sine KWW transforms at ``omega * tau``."""
    scaled = np.asarray(omega, dtype=float) * tau
    cosine = np.fromiter((kwwc(float(value), beta) for value in scaled), dtype=float, count=scaled.size)
    sine = np.fromiter((kwws(float(value), beta) for value in scaled), dtype=float, count=scaled.size)
    return cosine, sine


class TheoryKWWModesIndependent(TheoryBaumgaertelWinter):
    """Fit KWW dielectric modes with independent times and strengths.

    The relaxation times ``tau_i`` and strengths ``Delta-epsilon_i`` are
    independent positive parameters. All modes share one fitted stretching
    exponent ``beta``. The mode-management and conservative simplification
    controls are inherited from the Baumgaertel-Winter spectrum theory.
    """

    thname: ClassVar[str] = "KWW modes (independent)"
    description: ClassVar[str] = "Fit independent-time KWW dielectric modes"
    html_help_file: ClassVar[str] = (
        "http://reptate.readthedocs.io/manual/Applications/Dielectric/Theory/theory.html"
    )
    is_dielectric_domain: ClassVar[bool] = True

    def _mode_family_name(self) -> str:
        return "KWW"

    def _spectrum_label(self) -> str:
        return "KWW"

    def _add_domain_parameters(self) -> None:
        self.parameters["beta"] = Parameter(
            name="beta",
            value=0.5,
            description="Common KWW stretching exponent",
            type=ParameterType.real,
            opt_type=OptType.opt,
            min_value=0.1,
            max_value=2.0,
        )

    def _mode_parameter_description(self, index: int) -> str:
        return "log10(Delta-epsilon%02d) of Mode %d dielectric strength" % (index, index)

    def _mode_fit_signature(self, file: FileLike | None = None) -> tuple[Any, ...]:
        return super()._mode_fit_signature(file) + (round(self.parameter_float("beta"), 14),)

    def _predict_dynamic_moduli(
        self, omega: FloatArray, tau: FloatArray, amplitude: FloatArray
    ) -> tuple[FloatArray, FloatArray]:
        """Predict epsilon' and epsilon'' for independent KWW modes."""
        omega = np.asarray(omega, dtype=float)
        epsilon_prime = np.full_like(omega, self.parameter_float("einf"), dtype=float)
        epsilon_double_prime = np.zeros_like(omega, dtype=float)
        beta = self.parameter_float("beta")
        for tau_i, amplitude_i in zip(tau, amplitude):
            cosine, sine = _kww_values(omega, tau_i, beta)
            epsilon_prime += amplitude_i * cosine
            epsilon_double_prime += amplitude_i * sine
        return epsilon_prime, epsilon_double_prime

    def _residual_vector_for_modes(
        self, file: FileLike, tau: FloatArray, amplitude: FloatArray
    ) -> FloatArray:
        data = file.data_table.data
        omega = np.asarray(data[:, 0], dtype=float)
        epsilon_prime_exp = np.asarray(data[:, 1], dtype=float)
        epsilon_double_prime_exp = np.asarray(data[:, 2], dtype=float)
        valid = (omega > 0.0) & (epsilon_prime_exp > 0.0) & (epsilon_double_prime_exp > 0.0)
        if not np.any(valid):
            return np.array([], dtype=float)
        epsilon_prime, epsilon_double_prime = self._predict_dynamic_moduli(
            omega[valid], tau, amplitude
        )
        return np.r_[
            epsilon_prime / epsilon_prime_exp[valid] - 1.0,
            epsilon_double_prime / epsilon_double_prime_exp[valid] - 1.0,
        ]

    def BaumgaertelWinterFrequency(self, f: FileLike) -> None:
        """Calculate epsilon' and epsilon'' for the current independent KWW modes."""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        if tt.num_columns <= 1:
            return

        tau, amplitude = self._mode_values()
        epsilon_prime, epsilon_double_prime = self._predict_dynamic_moduli(
            tt.data[:, 0], tau, amplitude
        )
        tt.data[:, 1] = epsilon_prime
        if tt.num_columns > 2:
            tt.data[:, 2] = epsilon_double_prime
