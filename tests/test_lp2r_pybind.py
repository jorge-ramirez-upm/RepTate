import math


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
