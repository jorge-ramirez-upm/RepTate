import numpy as np

from RepTate.theories.TheoryDebyeModesIndependent import TheoryDebyeModesIndependent
from RepTate.theories.TheoryHavriliakNegamiModesIndependent import (
    TheoryHavriliakNegamiModesIndependent,
)


def test_independent_debye_kernel_matches_standard_debye_response():
    theory = TheoryDebyeModesIndependent.__new__(TheoryDebyeModesIndependent)
    theory.parameter_float = lambda name: {"einf": 0.25}[name]
    omega = np.array([0.1, 1.0, 10.0])
    tau = np.array([2.0])
    amplitude = np.array([3.0])
    prime, double_prime = theory._predict_dynamic_moduli(omega, tau, amplitude)
    wt = omega * 2.0
    np.testing.assert_allclose(prime, 0.25 + 3.0 / (1.0 + wt**2))
    np.testing.assert_allclose(double_prime, 3.0 * wt / (1.0 + wt**2))


def test_independent_hn_defaults_reduce_to_debye():
    theory = TheoryHavriliakNegamiModesIndependent.__new__(TheoryHavriliakNegamiModesIndependent)
    theory.parameter_float = lambda name: {"einf": 0.25, "alpha": 1.0, "gamma": 1.0}[name]
    omega = np.array([0.1, 1.0, 10.0])
    tau = np.array([2.0])
    amplitude = np.array([3.0])
    prime, double_prime = theory._predict_dynamic_moduli(omega, tau, amplitude)
    wt = omega * 2.0
    np.testing.assert_allclose(prime, 0.25 + 3.0 / (1.0 + wt**2))
    np.testing.assert_allclose(double_prime, 3.0 * wt / (1.0 + wt**2))
