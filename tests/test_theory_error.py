import numpy as np

from RepTate.gui.QTheory import compute_error
from RepTate.theories.TheoryShanbhagMaxwellModes import interpolate_shanbhag_theory_to_data, shanbhag_error


def test_compute_error_measures():
    yexp = np.array([1.0, 2.0, 4.0])
    yth = np.array([2.0, 1.0, 8.0])

    cases = [
        (False, False, "MSE", np.mean((yth - yexp) ** 2)),
        (True, False, "MSRE", np.mean(((yth - yexp) / yexp) ** 2)),
        (False, True, "MAE", np.mean(np.abs(yth - yexp))),
        (True, True, "MRAE", np.mean(np.abs((yth - yexp) / yexp))),
    ]

    for normalize_by_data, use_absolute_error, expected_label, expected_error in cases:
        error, label = compute_error(
            yth,
            yexp,
            normalize_by_data=normalize_by_data,
            use_absolute_error=use_absolute_error,
        )

        assert label == expected_label
        assert np.isclose(error, expected_error)


def test_shanbhag_error_reports_selected_measure():
    yexp = np.array([1.0, 2.0, 4.0])
    yth = np.array([2.0, 1.0, 8.0])

    error, label = shanbhag_error(
        yth,
        yexp,
        normalize_by_data=True,
        use_absolute_error=True,
    )

    assert label == "MRAE"
    assert np.isclose(error, np.mean(np.abs((yth - yexp) / yexp)))


def test_shanbhag_error_handles_empty_selection():
    error, label = shanbhag_error(
        np.array([]),
        np.array([]),
        normalize_by_data=True,
        use_absolute_error=False,
    )

    assert label == "MSRE"
    assert np.isnan(error)


def test_shanbhag_interpolation_drops_out_of_range_g1g2_points():
    xexp = np.array(
        [
            [0.5, 0.5],
            [1.0, 1.0],
            [2.0, 2.0],
            [3.0, 3.0],
        ]
    )
    xth = np.array(
        [
            [1.0, 1.0],
            [2.0, 2.0],
        ]
    )
    yth = np.array(
        [
            [10.0, 20.0],
            [30.0, 40.0],
        ]
    )

    yinterp = interpolate_shanbhag_theory_to_data(xth, yth, xexp, "linear")

    assert np.isnan(yinterp[0, 0])
    assert np.isnan(yinterp[3, 1])
    assert np.allclose(yinterp[1:3], yth)
