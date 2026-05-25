import numpy as np
import pytest

from RepTate.tools.ToolResampleData import (
    METHOD_CUBIC,
    METHOD_PCHIP,
    SCALE_LOG,
    clean_sort_unique_xy,
    make_resampling_grid,
    resample_xy,
)


def test_clean_sort_unique_xy_removes_invalid_and_averages_duplicates():
    x = np.asarray([2.0, 1.0, 1.0, np.nan, 3.0])
    y = np.asarray([4.0, 1.0, 3.0, 5.0, np.inf])

    x_unique, y_unique, removed_invalid, removed_duplicates = clean_sort_unique_xy(x, y)

    np.testing.assert_allclose(x_unique, [1.0, 2.0])
    np.testing.assert_allclose(y_unique, [2.0, 4.0])
    assert removed_invalid == 2
    assert removed_duplicates == 1


def test_resample_xy_pchip_uses_uniform_requested_grid():
    x = np.asarray([0.0, 1.0, 2.0, 3.0])
    y = x**2
    xnew = np.linspace(0.0, 3.0, 7)

    ynew, removed_invalid, removed_duplicates = resample_xy(x, y, xnew, METHOD_PCHIP)

    assert len(ynew) == 7
    assert removed_invalid == 0
    assert removed_duplicates == 0
    np.testing.assert_allclose(ynew[[0, -1]], [0.0, 9.0])


def test_resample_xy_cubic_requires_four_unique_points():
    x = np.asarray([0.0, 1.0, 2.0])
    y = x**2
    xnew = np.linspace(0.0, 2.0, 5)

    with pytest.raises(ValueError, match="Cubic spline requires"):
        resample_xy(x, y, xnew, METHOD_CUBIC)


def test_resample_xy_rejects_extrapolation():
    x = np.asarray([0.0, 1.0, 2.0])
    y = x**2
    xnew = np.linspace(-1.0, 2.0, 5)

    with pytest.raises(ValueError, match="outside the valid x range"):
        resample_xy(x, y, xnew, METHOD_PCHIP)


def test_make_resampling_grid_logarithmic():
    xnew = make_resampling_grid(1.0, 100.0, 3, SCALE_LOG)

    np.testing.assert_allclose(xnew, [1.0, 10.0, 100.0])


def test_resample_xy_logarithmic_interpolates_in_log_coordinates():
    x = np.asarray([1.0, 10.0, 100.0])
    y = x**2
    xnew = np.asarray([1.0, 10.0, 100.0])

    ynew, _, _ = resample_xy(x, y, xnew, METHOD_PCHIP, SCALE_LOG)

    np.testing.assert_allclose(ynew, [1.0, 100.0, 10000.0])


def test_resample_xy_logarithmic_requires_positive_values():
    x = np.asarray([1.0, 10.0, 100.0])
    y = np.asarray([1.0, 0.0, 100.0])
    xnew = make_resampling_grid(1.0, 100.0, 3, SCALE_LOG)

    with pytest.raises(ValueError, match="positive x and y"):
        resample_xy(x, y, xnew, METHOD_PCHIP, SCALE_LOG)
