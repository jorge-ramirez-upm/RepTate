import numpy as np

from RepTate.gui.QTheory import compute_error


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
