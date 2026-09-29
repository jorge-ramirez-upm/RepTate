"""Shared independent-mode framework for dielectric relaxation theories."""

from typing import ClassVar

import numpy as np

from RepTate.core.typing import FileLike, FloatArray
from RepTate.theories.TheoryBaumgaertelWinter import TheoryBaumgaertelWinter


class TheoryIndependentDielectricModes(TheoryBaumgaertelWinter):
    """Base class for dielectric theories with independent relaxation modes."""

    is_dielectric_domain: ClassVar[bool] = True

    def _mode_family_name(self) -> str:
        return "dielectric"

    def _spectrum_label(self) -> str:
        return "dielectric"

    def _predict_dynamic_moduli(
        self, omega: FloatArray, tau: FloatArray, amplitude: FloatArray
    ) -> tuple[FloatArray, FloatArray]:
        raise NotImplementedError

    def BaumgaertelWinterFrequency(self, f: FileLike) -> None:
        """Calculate the dielectric response from the independent modes."""
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
