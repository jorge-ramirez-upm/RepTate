from __future__ import annotations

import os
import sys
from collections import OrderedDict
from typing import Any

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


def _parameter_owner(cls: type[Any]) -> Any:
    owner = cls.__new__(cls)
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


def test_dataset_theory_creation_and_maxwell_mode_listing() -> None:
    configure_numpy_errors()
    CmdBase.calcmode = CalcMode.singlethread
    QApplication.instance() or QApplication(sys.argv)
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
