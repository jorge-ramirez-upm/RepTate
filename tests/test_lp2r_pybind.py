import math

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


def _material():
    from RepTate.theories import _lp2r

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


def test_lp2r_import_and_lognormal_smoke():
    from RepTate.theories import _lp2r

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


def test_lp2r_discrete_component_and_cancel():
    from RepTate.theories import _lp2r

    controls = _lp2r.Controls()
    controls.time_ratio = 1.05
    solver = _lp2r.Solver(_material(), controls)
    solver.add_discrete_component([50000.0, 120000.0], [0.4, 0.6])
    solver.prepare()
    solver.cancel()

    assert solver.cancelled()
    assert solver.step() is False


def test_lp2r_progress_advances_and_cancel_stops_relaxation():
    from RepTate.theories import _lp2r

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
    from RepTate.theories import _lp2r

    solver = _lp2r.Solver(_material(), _lp2r.Controls())
    solver.add_lognormal_component(weight=1.0, n=8, mw=100000.0, pdi=1.05)

    result = solver.run(freq_min=1.0e-2, freq_max=1.0e2, freq_ratio=2.0)

    _assert_matches_reference(result, LP2R_ORIGINAL_LOGNORMAL_REFERENCE)


def test_lp2r_discrete_matches_original_reference():
    from RepTate.theories import _lp2r

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


def test_lp2r_lve_application_registration():
    from PySide6.QtWidgets import QApplication

    from RepTate.gui.QApplicationManager import QApplicationManager
    from RepTate.theories.TheoryLP2RLVE import TheoryLP2RLVE

    QApplication.instance() or QApplication([])
    app = QApplicationManager().handle_new_app("LVE")

    assert app.theories[TheoryLP2RLVE.thname] is TheoryLP2RLVE
