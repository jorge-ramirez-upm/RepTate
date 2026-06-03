import math
from importlib import import_module
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest


LP2R_ORIGINAL_LOGNORMAL_REFERENCE = [
    (0.01, 0.0442951, 49.1957),
    (0.02, 0.177178, 98.3909),
    (0.04, 0.708666, 196.778),
    (0.08, 2.83395, 393.527),
    (0.16, 11.3245, 786.826),
    (0.32, 45.1235, 1571.84),
    (0.64, 178.0, 3129.9),
    (1.28, 681.356, 6163.06),
    (2.56, 2428.28, 11745.1),
    (5.12, 7579.43, 20735.0),
    (10.24, 19413.0, 31798.7),
    (20.48, 38833.3, 40004.9),
    (40.96, 60633.6, 41559.9),
    (81.92, 79315.9, 39754.0),
    (163.84, 95600.0, 39101.8),
]

LP2R_ORIGINAL_DISCRETE_REFERENCE = [
    (0.01, 0.0551202, 45.5723),
    (0.02, 0.220479, 91.1442),
    (0.04, 0.881895, 182.285),
    (0.08, 3.52722, 364.539),
    (0.16, 14.1031, 728.836),
    (0.32, 56.3206, 1455.74),
    (0.64, 223.825, 2896.15),
    (1.28, 872.792, 5673.77),
    (2.56, 3175.83, 10512.7),
    (5.12, 9423.68, 16609.1),
    (10.24, 19217.2, 20287.9),
    (20.48, 27741.4, 22284.6),
    (40.96, 36032.6, 28232.5),
    (81.92, 50384.8, 37787.0),
    (163.84, 71502.5, 44100.8),
]

LP2R_CASE_DIRS = [
    Path("data/LP2R/01rcdefault"),
    Path("data/LP2R/02PIblend"),
    Path("data/LP2R/03MWD"),
    Path("data/LP2R/03PS8"),
]


def _lp2r_module() -> Any:
    return import_module("RepTate.theories._lp2r")


def _material():
    _lp2r = _lp2r_module()

    material = _lp2r.Material()
    material.m_kuhn = 500.0
    material.m_e = 5000.0
    material.g0 = 2.0e5
    material.tau_e = 1.0e-5
    material.g_glass = 1.0e9
    material.tau_glass = 1.0e-8
    material.beta_glass = 0.7
    return material


def _assert_matches_reference(result, reference):
    actual = list(zip(result.omega, result.gp, result.gpp))
    assert len(actual) == len(reference)
    for actual_row, expected_row in zip(actual, reference):
        for actual_value, expected_value in zip(actual_row, expected_row):
            scale = max(abs(expected_value), 1.0)
            assert abs(actual_value - expected_value) / scale < 5.0e-6


def _read_lp2r_expected(path):
    expected = []
    for line in Path(path).read_text().splitlines():
        try:
            expected.append(tuple(map(float, line.split()[:3])))
        except ValueError:
            continue
    return expected


def _read_lp2r_discrete_dat(path):
    masses = []
    weights = []
    for raw_line in Path(path).read_text().splitlines():
        line = raw_line.split("%", 1)[0].strip()
        if not line or line.startswith("#"):
            continue
        mass, weight = map(float, line.split()[:2])
        masses.append(mass)
        weights.append(weight)
    return masses, weights


def _meaningful_lp2r_input_lines(path):
    lines = []
    for raw_line in Path(path).read_text().splitlines():
        line = raw_line.split("%", 1)[0].strip()
        if line:
            lines.append(line)
    return lines


def _build_lp2r_solver_from_input(input_path):
    from RepTate.theories.TheoryLP2RLVE import TheoryLP2RLVE

    _lp2r = _lp2r_module()
    lines = _meaningful_lp2r_input_lines(input_path)
    m_kuhn, m_e, g0, tau_e = map(float, lines[1].split()[:4])
    g_glass, tau_glass, beta_glass = map(float, lines[2].split()[:3])
    ncomponents = int(lines[3].split()[0])

    material = _lp2r.Material()
    material.m_kuhn = m_kuhn
    material.m_e = m_e
    material.g0 = g0
    material.tau_e = tau_e
    material.g_glass = g_glass
    material.tau_glass = tau_glass
    material.beta_glass = beta_glass

    controls = _lp2r.Controls()
    controls.time_ratio = 1.02
    solver = _lp2r.Solver(material, controls)

    index = 4
    for _ in range(ncomponents):
        ptype, weight = lines[index].split()[:2]
        index += 1
        if int(ptype) == 0:
            npoly, mw, pdi = lines[index].split()[:3]
            solver.add_lognormal_component(
                weight=float(weight),
                n=int(npoly),
                mw=float(mw),
                pdi=float(pdi),
            )
            index += 1
        elif int(ptype) == 2:
            mwd_path = input_path.parent / lines[index].split()[0]
            if not mwd_path.exists() and mwd_path.suffix == ".dat":
                mwd_path = mwd_path.with_suffix(".gpc")
            if mwd_path.suffix == ".gpc":
                masses, weights = TheoryLP2RLVE.read_gpc_mwd(mwd_path)
                masses = [mass * 1000.0 for mass in masses]
            else:
                masses, weights = _read_lp2r_discrete_dat(mwd_path)
            solver.add_discrete_component(
                masses,
                weights,
                component_weight=float(weight),
            )
            index += 1
        else:
            raise ValueError("Unsupported LP2R test ptype %s" % ptype)
    return solver


def _run_lp2r_lve_input(input_path):
    lines = _meaningful_lp2r_input_lines(input_path)
    freq_min, freq_max, freq_ratio = map(float, lines[0].split()[:3])
    solver = _build_lp2r_solver_from_input(input_path)
    return solver.run(freq_min, freq_max, freq_ratio)


def _run_lp2r_dielectric_input(input_path):
    result = _run_lp2r_lve_input(input_path)
    return list(zip(result.omega, result.epsilonp, result.epsilonpp))


def _run_lp2r_gt_input(input_path):
    solver = _build_lp2r_solver_from_input(input_path)
    solver.prepare()
    solver.run_relaxation()
    result = solver.calculate_relaxation_modulus()
    return list(zip(result.time, result.gt))


def _assert_rows_match_reference(actual, expected, tolerance=1.0e-5):
    assert len(actual) == len(expected)
    for actual_row, expected_row in zip(actual, expected):
        for actual_value, expected_value in zip(actual_row, expected_row):
            scale = max(abs(expected_value), 1.0)
            assert abs(actual_value - expected_value) / scale < tolerance


def test_lp2r_import_and_lognormal_smoke():
    _lp2r = _lp2r_module()

    solver = _lp2r.Solver(_material(), _lp2r.Controls())
    solver.add_lognormal_component(weight=1.0, n=8, mw=100000.0, pdi=1.05)

    result = solver.run(freq_min=1.0e-2, freq_max=1.0e2, freq_ratio=2.0)

    assert len(result.omega) > 0
    assert len(result.omega) == len(result.gp) == len(result.gpp)
    assert all(math.isfinite(v) for v in result.omega)
    assert all(math.isfinite(v) for v in result.gp)
    assert all(math.isfinite(v) for v in result.gpp)
    assert all(a < b for a, b in zip(result.omega, result.omega[1:]))
    assert math.isfinite(result.mw)
    assert math.isfinite(result.eta0)


def test_lp2r_dielectric_and_gt_outputs_are_available_and_finite():
    _lp2r = _lp2r_module()

    material = _lp2r.Material()
    material.m_kuhn = 720.0
    material.m_e = 12870.0
    material.g0 = 230000.0
    material.tau_e = 2.0e-3
    material.g_glass = 1.20e9
    material.tau_glass = 1.30e-9
    material.beta_glass = 0.380

    masses, weights = _read_lp2r_discrete_dat("data/LP2R/03PS8/PS390Kmcut.dat")
    solver = _lp2r.Solver(material, _lp2r.Controls())
    solver.add_discrete_component(masses, weights)
    solver.prepare()
    solver.run_relaxation()

    spectra = solver.calculate_spectra(freq_min=1.0e-5, freq_max=1.0e3, freq_ratio=1.5)
    assert len(spectra.epsilonp) == len(spectra.omega)
    assert len(spectra.epsilonpp) == len(spectra.omega)
    assert all(math.isfinite(v) for v in spectra.epsilonp)
    assert all(math.isfinite(v) for v in spectra.epsilonpp)
    assert max(spectra.epsilonp) == pytest.approx(0.935252)
    assert max(spectra.epsilonpp) == pytest.approx(0.13554746727566974)

    relaxation = solver.calculate_relaxation_modulus()
    assert len(relaxation.time) > 0
    assert len(relaxation.time) == len(relaxation.gt) == len(relaxation.mu) == len(relaxation.r)
    assert all(math.isfinite(v) and v > 0.0 for v in relaxation.time)
    assert all(math.isfinite(v) for v in relaxation.gt)
    assert all(a < b for a, b in zip(relaxation.time, relaxation.time[1:]))
    assert relaxation.time[0] == pytest.approx(2.0e-7)
    assert relaxation.gt[0] == pytest.approx(6395753.232983634)
    assert relaxation.gt[50] == pytest.approx(1655530.3089384811)


def test_lp2r_discrete_component_and_cancel():
    _lp2r = _lp2r_module()

    controls = _lp2r.Controls()
    controls.time_ratio = 1.05
    solver = _lp2r.Solver(_material(), controls)
    solver.add_discrete_component([50000.0, 120000.0], [0.4, 0.6])
    solver.prepare()
    solver.cancel()

    assert solver.cancelled()
    assert solver.step() is False


def test_lp2r_progress_advances_and_cancel_stops_relaxation():
    _lp2r = _lp2r_module()

    solver = _lp2r.Solver(_material(), _lp2r.Controls())
    solver.add_lognormal_component(weight=1.0, n=8, mw=100000.0, pdi=1.05)
    solver.prepare()

    progress = [solver.progress()]
    for _ in range(10):
        assert solver.step() is True
        progress.append(solver.progress())

    assert progress[0] == 0.0
    assert progress[-1] > progress[0]
    assert all(a <= b for a, b in zip(progress, progress[1:]))

    solver.cancel()

    assert solver.cancelled()
    assert solver.step() is False


def test_lp2r_lognormal_matches_original_reference():
    _lp2r = _lp2r_module()

    solver = _lp2r.Solver(_material(), _lp2r.Controls())
    solver.add_lognormal_component(weight=1.0, n=8, mw=100000.0, pdi=1.05)

    result = solver.run(freq_min=1.0e-2, freq_max=1.0e2, freq_ratio=2.0)

    _assert_matches_reference(result, LP2R_ORIGINAL_LOGNORMAL_REFERENCE)


def test_lp2r_discrete_matches_original_reference():
    _lp2r = _lp2r_module()

    solver = _lp2r.Solver(_material(), _lp2r.Controls())
    solver.add_discrete_component([50000.0, 120000.0], [0.4, 0.6])

    result = solver.run(freq_min=1.0e-2, freq_max=1.0e2, freq_ratio=2.0)

    _assert_matches_reference(result, LP2R_ORIGINAL_DISCRETE_REFERENCE)


def test_lp2r_lve_theory_import():
    from RepTate.theories.TheoryLP2RLVE import TheoryLP2RLVE

    assert TheoryLP2RLVE.thname == "LP2R LVE"


def test_lp2r_lve_discrete_distribution_parser():
    from RepTate.theories.TheoryLP2RLVE import TheoryLP2RLVE

    masses, weights = TheoryLP2RLVE._parse_discrete_distribution(
        "50, 120; 200",
        "0.2 0.3, 0.5",
    )

    assert masses == [50.0, 120.0, 200.0]
    assert weights == [0.2, 0.3, 0.5]

    with pytest.raises(ValueError, match="same length"):
        TheoryLP2RLVE._parse_discrete_distribution("50, 120", "1.0")

    with pytest.raises(ValueError, match="positive"):
        TheoryLP2RLVE._parse_discrete_distribution("50, -120", "0.4, 0.6")


def test_lp2r_lve_mwd_import_formatting_helpers():
    from RepTate.theories.TheoryLP2RLVE import TheoryLP2RLVE

    masses, weights = TheoryLP2RLVE._normalise_discrete_distribution(
        [50.0, 120.0],
        [2.0, 3.0],
    )

    assert masses == [50.0, 120.0]
    assert weights == [0.4, 0.6]
    assert TheoryLP2RLVE._format_number_list(masses) == "50, 120"
    assert TheoryLP2RLVE._format_number_list(weights) == "0.4, 0.6"

    with pytest.raises(ValueError, match="positive total"):
        TheoryLP2RLVE._normalise_discrete_distribution([50.0], [0.0])


def test_lp2r_mwd_dialog_shows_input_units():
    from PySide6.QtWidgets import QApplication, QLabel, QWidget

    from RepTate.core.Parameter import OptType, Parameter, ParameterType
    from RepTate.theories.theory_helpers import EditMWDDialog

    _qt_app = QApplication.instance() or QApplication([])
    parent: Any = QWidget()
    parent.parameters = {
        "Me": Parameter(
            name="Me",
            value=5.0,
            type=ParameterType.real,
            opt_type=OptType.const,
            quantity="molar_mass",
            internal_unit="kg/mol",
            display_unit="kg/mol",
        ),
        "tau_e": Parameter(
            name="tau_e",
            value=1.0e-5,
            type=ParameterType.real,
            opt_type=OptType.const,
            quantity="time",
            internal_unit="s",
            display_unit="s",
        ),
    }

    dialog = EditMWDDialog(parent, [50.0, 120.0], [0.4, 0.6], 200)

    assert dialog.table.horizontalHeaderItem(0).text() == "M [kg/mol]"
    labels = {label.text() for label in dialog.findChildren(QLabel)}
    assert "Me [kg/mol]" in labels
    assert "tau_e [s]" in labels


def test_lp2r_lve_component_default_and_validation():
    from RepTate.theories.TheoryLP2RLVE import TheoryLP2RLVE

    component = TheoryLP2RLVE.make_lognormal_component(
        weight=0.25,
        npoly=12,
        mw=250.0,
        pdi=1.2,
        label="PI blend",
        source="test",
    )

    assert component == {
        "kind": "lognormal",
        "weight": 0.25,
        "npoly": 12,
        "Mw": 250.0,
        "PDI": 1.2,
        "label": "PI blend",
        "source": "test",
    }

    with pytest.raises(ValueError, match="PDI"):
        TheoryLP2RLVE.make_lognormal_component(pdi=0.99)


def test_lp2r_lve_component_mwd_normalization_and_weight_normalization():
    from RepTate.theories.TheoryLP2RLVE import TheoryLP2RLVE

    components = [
        TheoryLP2RLVE.make_lognormal_component(weight=2.0),
        TheoryLP2RLVE.make_mwd_component(
            [50.0, 120.0],
            [2.0, 3.0],
            weight=3.0,
        ),
    ]

    assert components[1]["weights"] == [0.4, 0.6]
    normalized = TheoryLP2RLVE.normalize_component_weights(components)

    assert normalized[0]["weight"] == pytest.approx(0.4)
    assert normalized[1]["weight"] == pytest.approx(0.6)


def test_lp2r_lve_gpc_import_parsing_and_normalization(tmp_path):
    from RepTate.theories.TheoryLP2RLVE import TheoryLP2RLVE

    gpc_file = tmp_path / "blend.gpc"
    gpc_file.write_text(
        "# M W(logM)\n"
        "100 1\n"
        "10 1\n"
        "1000 1\n",
        encoding="latin-1",
    )

    masses, weights = TheoryLP2RLVE.read_gpc_mwd(gpc_file)

    assert masses == [10.0, 100.0, 1000.0]
    assert sum(weights) == pytest.approx(1.0)
    assert all(weight > 0 for weight in weights)


def test_lp2r_lve_gpc_import_converts_declared_mass_units():
    from RepTate.theories.TheoryLP2RLVE import TheoryLP2RLVE

    masses, weights = TheoryLP2RLVE.read_gpc_mwd(
        "data/LP2R/03MWD/MWD.gpc"
    )

    assert masses == pytest.approx([100.0, 1000.0, 10000.0])
    assert weights == pytest.approx([1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0])


def test_lp2r_lve_extra_data_roundtrip_and_legacy_migration():
    from RepTate.theories.TheoryLP2RLVE import TheoryLP2RLVE

    components = [
        TheoryLP2RLVE.make_lognormal_component(weight=0.7, mw=200.0),
        TheoryLP2RLVE.make_mwd_component(
            [50.0, 120.0],
            [0.4, 0.6],
            weight=0.3,
        ),
    ]
    copied = TheoryLP2RLVE.copy_lp2r_components(components)
    copied[1]["masses"][0] = 1.0

    assert components[1]["masses"][0] == 50.0
    restored = TheoryLP2RLVE.migrate_old_lp2r_state(
        {"lp2r_components": components}
    )
    legacy = TheoryLP2RLVE.migrate_old_lp2r_state(
        {"MWD_m": [50.0, 120.0], "MWD_phi": [2.0, 3.0]}
    )
    assert restored is not None
    assert legacy is not None

    assert restored == components
    assert legacy[0]["kind"] == "mwd"
    assert legacy[0]["weights"] == [0.4, 0.6]


def test_lp2r_lve_build_solver_uses_mixed_components(monkeypatch):
    import RepTate.theories.TheoryLP2RLVE as lp2r_module
    from RepTate.theories.TheoryLP2RLVE import TheoryLP2RLVE

    class FakeSolver:
        calls = []

        def __init__(self, material, controls):
            self.material = material
            self.controls = controls

        def add_lognormal_component(self, weight, n, mw, pdi):
            self.calls.append(("lognormal", weight, n, mw, pdi))

        def add_discrete_component(self, mass, weight, component_weight=1.0):
            self.calls.append(("mwd", mass, weight, component_weight))

    monkeypatch.setattr(lp2r_module._lp2r, "Solver", FakeSolver)

    def parameter(value):
        return SimpleNamespace(value=value)

    theory: Any = TheoryLP2RLVE.__new__(TheoryLP2RLVE)
    theory.parameters = {
        "MK": parameter(0.5),
        "Me": parameter(5.0),
        "G0": parameter(2.0e5),
        "tau_e": parameter(1.0e-5),
        "G_glass": parameter(1.0e9),
        "tau_glass": parameter(1.0e-8),
        "beta_glass": parameter(0.7),
        "alpha": parameter(1.0),
        "t_cr_start": parameter(1.0),
        "delta_cr": parameter(0.3),
        "b_zeta": parameter(2.0),
        "a_eq": parameter(2.0),
        "b_eq": parameter(10.0),
        "ret_pref": parameter(0.189),
        "ret_pref_0": parameter(0.020),
        "ret_switch_exponent": parameter(0.42),
        "rept_switch_factor": parameter(1.664),
        "rouse_switch_factor": parameter(1.5),
        "disentanglement_switch": parameter(1.0),
        "start_time": parameter(1.0e-3),
        "time_ratio": parameter(1.02),
    }
    theory.lp2r_components = [
        TheoryLP2RLVE.make_lognormal_component(
            weight=0.25,
            npoly=6,
            mw=150.0,
            pdi=1.1,
        ),
        TheoryLP2RLVE.make_mwd_component(
            [50.0, 120.0],
            [0.4, 0.6],
            weight=0.75,
        ),
    ]

    FakeSolver.calls = []
    solver = theory._build_solver()

    assert isinstance(solver, FakeSolver)
    assert FakeSolver.calls == [
        ("lognormal", 0.25, 6, 150000.0, 1.1),
        ("mwd", [50000.0, 120000.0], [0.4, 0.6], 0.75),
    ]


def test_lp2r_lve_default_component_tracks_visible_parameters():
    from RepTate.theories.TheoryLP2RLVE import TheoryLP2RLVE

    def parameter(value):
        return SimpleNamespace(value=value)

    theory: Any = TheoryLP2RLVE.__new__(TheoryLP2RLVE)
    theory.parameters = {
        "n": parameter(12),
        "Mw": parameter(250.0),
        "PDI": parameter(1.2),
    }
    theory.lp2r_components = [
        {
            "kind": "lognormal",
            "weight": 1.0,
            "npoly": 8,
            "Mw": 100.0,
            "PDI": 1.05,
            "label": "Lognormal",
            "source": "parameters",
        }
    ]

    assert theory.current_lp2r_components()[0]["npoly"] == 12
    assert theory.current_lp2r_components()[0]["Mw"] == 250.0
    assert theory.current_lp2r_components()[0]["PDI"] == 1.2


def test_lp2r_lve_default_component_file_moments_use_defaults_and_derivations():
    from RepTate.theories.TheoryLP2RLVE import TheoryLP2RLVE

    def parameter(value):
        return SimpleNamespace(value=value)

    def theory_with_file_params(file_parameters):
        theory: Any = TheoryLP2RLVE.__new__(TheoryLP2RLVE)
        theory.parameters = {
            "n": parameter(0),
            "Mw": parameter(0.0),
            "PDI": parameter(0.0),
        }
        theory.parent_dataset = SimpleNamespace(
            files=[SimpleNamespace(file_parameters=file_parameters)]
        )
        return theory

    theory = theory_with_file_params({"Mw": "0", "Mn": "0", "PDI": "0"})
    assert theory._read_default_component_params_from_first_file() is False
    assert theory.parameters["n"].value == TheoryLP2RLVE.DEFAULT_NPOLY
    assert theory.parameters["Mw"].value == TheoryLP2RLVE.DEFAULT_MW
    assert theory.parameters["PDI"].value == TheoryLP2RLVE.DEFAULT_PDI

    theory = theory_with_file_params({"Mn": "200", "PDI": "1.4"})
    assert theory._read_default_component_params_from_first_file() is True
    assert theory.parameters["Mw"].value == pytest.approx(280.0)
    assert theory.parameters["PDI"].value == pytest.approx(1.4)

    theory = theory_with_file_params({"Mw": "300", "Mn": "200"})
    assert theory._read_default_component_params_from_first_file() is True
    assert theory.parameters["Mw"].value == pytest.approx(300.0)
    assert theory.parameters["PDI"].value == pytest.approx(1.5)


def test_lp2r_lve_application_registration():
    from PySide6.QtWidgets import QApplication

    from RepTate.gui.QApplicationManager import QApplicationManager
    from RepTate.theories.TheoryLP2RLVE import (
        TheoryLP2RDielectric,
        TheoryLP2RGt,
        TheoryLP2RLVE,
    )

    _qt_app = QApplication.instance() or QApplication([])
    manager = QApplicationManager()

    app = manager.handle_new_app("LVE")
    assert app is not None

    assert app.theories[TheoryLP2RLVE.thname] is TheoryLP2RLVE

    app = manager.handle_new_app("Dielectric")
    assert app is not None
    assert app.theories[TheoryLP2RDielectric.thname] is TheoryLP2RDielectric

    app = manager.handle_new_app("Gt")
    assert app is not None
    assert app.theories[TheoryLP2RGt.thname] is TheoryLP2RGt


@pytest.mark.parametrize("case_dir", LP2R_CASE_DIRS, ids=lambda path: path.name)
def test_lp2r_lve_references_match_expected_output(case_dir):
    result = _run_lp2r_lve_input(case_dir / "inp.dat")
    expected = _read_lp2r_expected(case_dir / "Expected_Output.tts")

    _assert_rows_match_reference(
        list(zip(result.omega, result.gp, result.gpp)),
        expected,
    )


@pytest.mark.parametrize("case_dir", LP2R_CASE_DIRS, ids=lambda path: path.name)
def test_lp2r_dielectric_references_match_expected_output(case_dir):
    actual = _run_lp2r_dielectric_input(case_dir / "inp.dat")
    expected = _read_lp2r_expected(case_dir / "Expected_Output.dls")

    _assert_rows_match_reference(
        actual,
        expected,
    )


@pytest.mark.parametrize("case_dir", LP2R_CASE_DIRS, ids=lambda path: path.name)
def test_lp2r_gt_references_match_expected_output(case_dir):
    actual = _run_lp2r_gt_input(case_dir / "inp.dat")
    expected = _read_lp2r_expected(case_dir / "Expected_Output.gt")

    _assert_rows_match_reference(
        actual,
        expected,
    )


def test_lp2r_kww_midrange_failure_reports_as_exception_not_abort():
    _lp2r = _lp2r_module()

    material = _material()
    material.tau_glass = 1.0e-6
    material.beta_glass = 0.7

    solver = _lp2r.Solver(material, _lp2r.Controls())
    solver.add_lognormal_component(weight=1.0, n=8, mw=100000.0, pdi=1.05)
    result = solver.run(freq_min=1.0e5, freq_max=2.0e5, freq_ratio=1.1)

    assert len(result.omega) > 0
    assert all(math.isfinite(value) for value in result.gp)
    assert all(math.isfinite(value) for value in result.gpp)
