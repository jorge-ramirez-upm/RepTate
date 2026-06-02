from __future__ import annotations

from collections import OrderedDict

import numpy as np
import numpy.testing as npt

from RepTate.core.Parameter import Parameter, ParameterType
from RepTate.theories.TheoryMaxwellModes import TheoryMaxwellModesTime
from RepTate.theories.TheoryRetardationModes import TheoryRetardationModesTime


def test_maxwell_modes_time_single_mode_export_uses_time_maximum() -> None:
    theory = TheoryMaxwellModesTime.__new__(TheoryMaxwellModesTime)
    theory.parameters = OrderedDict(
        [
            ("nmodes", Parameter("nmodes", 1, "number of modes", ParameterType.integer)),
            ("logtmin", Parameter("logtmin", -2.0, "minimum log time", ParameterType.real)),
            ("logtmax", Parameter("logtmax", 1.0, "maximum log time", ParameterType.real)),
            ("logG00", Parameter("logG00", 3.0, "mode modulus", ParameterType.real)),
        ]
    )

    tau, modulus, success = theory.get_modes()

    assert success is True
    npt.assert_allclose(tau, np.array([10.0]))
    npt.assert_allclose(modulus, np.array([1000.0]))


def test_retardation_modes_time_export_returns_reciprocal_compliances() -> None:
    theory = TheoryRetardationModesTime.__new__(TheoryRetardationModesTime)
    theory.parameters = OrderedDict(
        [
            ("nmodes", Parameter("nmodes", 2, "number of modes", ParameterType.integer)),
            ("logtmin", Parameter("logtmin", -1.0, "minimum log time", ParameterType.real)),
            ("logtmax", Parameter("logtmax", 1.0, "maximum log time", ParameterType.real)),
            ("logJ00", Parameter("logJ00", -2.0, "mode compliance", ParameterType.real)),
            ("logJ01", Parameter("logJ01", -3.0, "mode compliance", ParameterType.real)),
        ]
    )

    tau, modulus, success = theory.get_modes()

    assert success is True
    npt.assert_allclose(tau, np.array([0.1, 10.0]))
    npt.assert_allclose(modulus, np.array([100.0, 1000.0]))
