"""Independent-time Debye modes for dielectric spectroscopy."""

from typing import ClassVar

import numpy as np

from RepTate.core.typing import FloatArray
from RepTate.theories.TheoryIndependentDielectricModes import TheoryIndependentDielectricModes


class TheoryDebyeModesIndependent(TheoryIndependentDielectricModes):
    """Fit Debye modes with independent relaxation times and amplitudes."""

    thname: ClassVar[str] = "Debye modes (independent)"
    description: ClassVar[str] = "Fit independent-time Debye modes"
    html_help_file: ClassVar[str] = (
        "http://reptate.readthedocs.io/manual/Applications/Dielectric/Theory/theory.html"
    )

    def _mode_family_name(self) -> str:
        return "Debye"

    def _spectrum_label(self) -> str:
        return "Debye"

    def _predict_dynamic_moduli(
        self, omega: FloatArray, tau: FloatArray, amplitude: FloatArray
    ) -> tuple[FloatArray, FloatArray]:
        omega = np.asarray(omega, dtype=float)
        epsilon_prime = np.full_like(omega, self.parameter_float("einf"), dtype=float)
        epsilon_double_prime = np.zeros_like(omega, dtype=float)
        for tau_i, amplitude_i in zip(tau, amplitude):
            wt = omega * tau_i
            denominator = 1.0 + wt**2
            epsilon_prime += amplitude_i / denominator
            epsilon_double_prime += amplitude_i * wt / denominator
        return epsilon_prime, epsilon_double_prime
