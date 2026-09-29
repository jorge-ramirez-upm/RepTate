"""Independent-time Havriliak-Negami modes for dielectric spectroscopy."""

from typing import ClassVar

import numpy as np

from RepTate.core.typing import FloatArray
from RepTate.core.Parameter import OptType, Parameter, ParameterType
from RepTate.theories.TheoryIndependentDielectricModes import TheoryIndependentDielectricModes


class TheoryHavriliakNegamiModesIndependent(TheoryIndependentDielectricModes):
    """Fit Havriliak-Negami modes with independent times and amplitudes."""

    thname: ClassVar[str] = "Havriliak-Negami modes (independent)"
    description: ClassVar[str] = "Fit independent-time Havriliak-Negami modes"
    html_help_file: ClassVar[str] = (
        "http://reptate.readthedocs.io/manual/Applications/Dielectric/Theory/theory.html"
    )

    def _mode_family_name(self) -> str:
        return "Havriliak-Negami"

    def _spectrum_label(self) -> str:
        return "Havriliak-Negami"

    def _add_domain_parameters(self) -> None:
        self.parameters["alpha"] = Parameter(
            name="alpha",
            value=1.0,
            description="Common Havriliak-Negami asymmetry parameter",
            type=ParameterType.real,
            opt_type=OptType.opt,
            min_value=0.0,
        )
        self.parameters["gamma"] = Parameter(
            name="gamma",
            value=1.0,
            description="Common Havriliak-Negami broadness parameter",
            type=ParameterType.real,
            opt_type=OptType.opt,
            min_value=0.0,
        )

    def _predict_dynamic_moduli(
        self, omega: FloatArray, tau: FloatArray, amplitude: FloatArray
    ) -> tuple[FloatArray, FloatArray]:
        omega = np.asarray(omega, dtype=float)
        alpha = self.parameter_float("alpha")
        gamma = self.parameter_float("gamma")
        response = np.full(omega.shape, self.parameter_float("einf"), dtype=complex)
        for tau_i, amplitude_i in zip(tau, amplitude):
            response += amplitude_i / np.power(
                1.0 + np.power(1j * omega * tau_i, alpha), gamma
            )
        return np.real(response), -np.imag(response)
