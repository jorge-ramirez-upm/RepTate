import numpy as np

from RepTate.theories.TheoryKWWModesIndependent import (
    TheoryKWWModesIndependent,
    _kww_values,
)


def test_independent_kww_beta_one_is_debye_kernel():
    omega = np.array([0.1, 1.0, 10.0])
    cosine, sine = _kww_values(omega, tau=2.0, beta=1.0)
    wt = omega * 2.0
    np.testing.assert_allclose(cosine, 1.0 / (1.0 + wt**2), rtol=1e-7, atol=1e-10)
    np.testing.assert_allclose(sine, wt / (1.0 + wt**2), rtol=1e-7, atol=1e-10)


def test_independent_kww_uses_shared_mode_contract():
    theory = TheoryKWWModesIndependent.__new__(TheoryKWWModesIndependent)
    assert theory.is_dielectric_domain is True
    assert theory._mode_parameter_name(3) == "logDe03"
    assert theory._mode_family_name() == "KWW"
    assert theory._spectrum_label() == "KWW"
