from __future__ import annotations

import os
import sys
from collections import OrderedDict
from typing import Any, cast

import numpy as np
import numpy.testing as npt

from PySide6.QtWidgets import QApplication

from RepTate.core.CmdBase import CalcMode, CmdBase
from RepTate.core.Parameter import Parameter, ParameterType
from RepTate.gui.QApplicationManager import QApplicationManager
from RepTate.gui.QTheory import QTheory
from RepTate.gui.QTool import QTool
from RepTate.runtime import configure_numpy_errors
from RepTate.theories.TheoryMaxwellModes import TheoryMaxwellModesFrequency
from RepTate.theories.TheoryUCM import TheoryUCM
from RepTate.tools.ToolBounds import ToolBounds
from RepTate.tools.ToolGradient import ToolGradient
from RepTate.tools.ToolPowerLaw import ToolPowerLaw


def _parameter_owner(cls: type[Any]) -> Any:
    owner = cast(Any, cls).__new__(cls)
    owner.parameters = OrderedDict(
        [
            ("real", Parameter("real", "2.5", "real parameter", ParameterType.real)),
            ("integer", Parameter("integer", "3", "integer parameter", ParameterType.integer)),
            ("boolean", Parameter("boolean", "1", "boolean parameter", ParameterType.boolean)),
            ("string", Parameter("string", 42, "string parameter", ParameterType.string)),
        ]
    )
    return owner


def test_qtheory_parameter_helpers_return_plain_scalar_values() -> None:
    theory = _parameter_owner(QTheory)

    assert theory.parameter_float("real") == 2.5
    assert theory.parameter_int("integer") == 3
    assert theory.parameter_bool("boolean") is True
    assert theory.parameter_str("string") == "42"


def test_qtool_parameter_helpers_return_plain_scalar_values() -> None:
    tool = _parameter_owner(QTool)

    assert tool.parameter_float("real") == 2.5
    assert tool.parameter_int("integer") == 3
    assert tool.parameter_bool("boolean") is True
    assert tool.parameter_str("string") == "42"


def test_power_law_tool_calculation_uses_float_parameter() -> None:
    tool = ToolPowerLaw.__new__(ToolPowerLaw)
    tool.parameters = OrderedDict(
        [
            ("n", Parameter("n", "2", "power law exponent", ParameterType.real)),
        ]
    )
    x = np.array([1.0, 2.0, 4.0])
    y = np.array([2.0, 8.0, 32.0])

    xout, yout = tool.calculate(x, y)

    npt.assert_array_equal(xout, x)
    npt.assert_allclose(yout, np.array([2.0, 2.0, 2.0]))


def test_bounds_tool_calculation_uses_scalar_parameters() -> None:
    tool = ToolBounds.__new__(ToolBounds)
    tool.parameters = OrderedDict(
        [
            ("xmin", Parameter("xmin", 0.0, "minimum x", ParameterType.real)),
            ("xmax", Parameter("xmax", 3.0, "maximum x", ParameterType.real)),
            ("ymin", Parameter("ymin", 0.0, "minimum y", ParameterType.real)),
            ("ymax", Parameter("ymax", 10.0, "maximum y", ParameterType.real)),
        ]
    )
    x = np.array([-1.0, 0.5, 2.0, 4.0])
    y = np.array([5.0, -1.0, 9.0, 3.0])

    xout, yout = tool.calculate(x, y)

    npt.assert_allclose(xout, np.array([2.0]))
    npt.assert_allclose(yout, np.array([9.0]))


def test_gradient_tool_calculates_derivative_without_parameters() -> None:
    tool = ToolGradient.__new__(ToolGradient)
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = x**2

    xout, yout = tool.calculate(x, y)

    npt.assert_array_equal(xout, x)
    npt.assert_allclose(yout, np.gradient(y, x))


def test_dataset_theory_creation_and_maxwell_mode_listing() -> None:
    configure_numpy_errors()
    CmdBase.calcmode = CalcMode.singlethread
    app_instance = QApplication.instance() or QApplication(sys.argv)
    manager = QApplicationManager()
    app = manager.handle_new_app("LVE")
    assert app is not None

    dataset = app.new_tables_from_files([os.path.join("data", "PI_LINEAR", "PI_225.9k_T-35.tts")])
    assert dataset.files

    theory = dataset.new_theory("Maxwell Modes", calculate=False, show=False)
    assert theory.name == dataset.current_theory
    assert theory.name in dataset.theories
    assert theory.has_modes is True

    get_modes, set_modes = manager.list_theories_Maxwell()
    assert theory.get_modes in get_modes.values()
    assert theory.set_modes in set_modes.values()
    assert set(get_modes) == set(set_modes)


def test_maxwell_modes_export_import_contract() -> None:
    exporter = TheoryMaxwellModesFrequency.__new__(TheoryMaxwellModesFrequency)
    exporter.parameters = OrderedDict(
        [
            ("nmodes", Parameter("nmodes", 2, "number of modes", ParameterType.integer)),
            ("logwmin", Parameter("logwmin", -1.0, "minimum log frequency", ParameterType.real)),
            ("logwmax", Parameter("logwmax", 1.0, "maximum log frequency", ParameterType.real)),
            ("logG00", Parameter("logG00", 2.0, "mode modulus", ParameterType.real)),
            ("logG01", Parameter("logG01", 3.0, "mode modulus", ParameterType.real)),
        ]
    )

    tau, modulus, success = exporter.get_modes()

    assert success is True
    npt.assert_allclose(tau, np.array([10.0, 0.1]))
    npt.assert_allclose(modulus, np.array([100.0, 1000.0]))

    importer = TheoryUCM.__new__(TheoryUCM)
    importer.parameters = OrderedDict(
        [
            ("nmodes", Parameter("nmodes", 1, "number of modes", ParameterType.integer)),
            ("G00", Parameter("G00", 1.0, "mode modulus", ParameterType.real)),
            ("tauD00", Parameter("tauD00", 1.0, "mode time", ParameterType.real)),
        ]
    )

    assert importer.set_modes(tau, modulus) is True

    imported_tau, imported_modulus, imported_success = importer.get_modes()
    assert imported_success is True
    npt.assert_allclose(imported_tau, tau)
    npt.assert_allclose(imported_modulus, modulus)
