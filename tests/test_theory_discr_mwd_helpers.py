from __future__ import annotations

from typing import Any, cast

import numpy as np
import pytest

from RepTate.theories.TheoryDiscrMWD import TheoryDiscrMWD


def _discr_mwd_stub() -> TheoryDiscrMWD:
    return TheoryDiscrMWD.__new__(TheoryDiscrMWD)


def test_discr_mwd_calculate_moments_returns_weighted_distribution_moments() -> None:
    theory = _discr_mwd_stub()
    distribution = np.array(
        [
            [10.0, 0.2],
            [100.0, 0.3],
            [1000.0, 0.5],
        ]
    )

    mn, mw, pdi, mz_over_mw = theory.calculate_moments(distribution)

    expected_mw = 0.2 * 10.0 + 0.3 * 100.0 + 0.5 * 1000.0
    expected_mn = 1.0 / (0.2 / 10.0 + 0.3 / 100.0 + 0.5 / 1000.0)
    expected_mz = (0.2 * 10.0**2 + 0.3 * 100.0**2 + 0.5 * 1000.0**2) / expected_mw

    assert mn == pytest.approx(expected_mn)
    assert mw == pytest.approx(expected_mw)
    assert pdi == pytest.approx(expected_mw / expected_mn)
    assert mz_over_mw == pytest.approx(expected_mz / expected_mw)


def test_discr_mwd_calculate_moments_reports_nan_for_degenerate_distribution() -> None:
    theory = _discr_mwd_stub()
    messages: list[str] = []
    dynamic_theory = cast(Any, theory)
    dynamic_theory.Qprint = lambda message, end="<br>": messages.append(message)
    distribution = np.array(
        [
            [10.0, 0.0],
            [100.0, 0.0],
        ]
    )

    mn, mw, pdi, mz_over_mw = theory.calculate_moments(distribution)

    assert np.isnan(mn)
    assert np.isnan(mw)
    assert np.isnan(pdi)
    assert np.isnan(mz_over_mw)
    assert messages == ["Could not determine moments"]
