# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# --------------------------------------------------------------------------------------------------------
#
# Copyright (2018-2026): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
#
# This file is part of RepTate.
#
# RepTate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RepTate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RepTate.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------------------------
"""Module ToolResampleData

Resample the current view data by interpolation.
"""

import traceback
from typing import Any, ClassVar

import numpy as np
from PySide6.QtWidgets import QComboBox, QLabel
from RepTate.core.Parameter import OptType, Parameter, ParameterType
from RepTate.core.typing import AnyArray, ApplicationLike, AxesLike, FileParameters, ToolResult, ViewLike
from RepTate.gui.QTool import QTool
from scipy.interpolate import CubicSpline, PchipInterpolator


METHOD_PCHIP = "PCHIP"
METHOD_CUBIC = "Cubic spline"
INTERPOLATION_METHODS = [METHOD_PCHIP, METHOD_CUBIC]
SCALE_LINEAR = "Linear"
SCALE_LOG = "Logarithmic"
INTERPOLATION_SCALES = [SCALE_LINEAR, SCALE_LOG]


def clean_sort_unique_xy(x: AnyArray, y: AnyArray) -> tuple[AnyArray, AnyArray, int, int]:
    """Return finite x/y values sorted by x, consolidating repeated x values."""
    x_arr = np.asarray(x, dtype=float).reshape(-1)
    y_arr = np.asarray(y, dtype=float).reshape(-1)
    finite = np.isfinite(x_arr) & np.isfinite(y_arr)
    removed_invalid = int(len(x_arr) - np.count_nonzero(finite))
    x_valid = x_arr[finite]
    y_valid = y_arr[finite]

    order = np.argsort(x_valid, kind="mergesort")
    x_sorted = x_valid[order]
    y_sorted = y_valid[order]

    x_unique, inverse, counts = np.unique(x_sorted, return_inverse=True, return_counts=True)
    y_unique = np.zeros_like(x_unique, dtype=float)
    np.add.at(y_unique, inverse, y_sorted)
    y_unique /= counts
    removed_duplicates = int(len(x_sorted) - len(x_unique))
    return x_unique, y_unique, removed_invalid, removed_duplicates


def resample_xy(
    x: AnyArray,
    y: AnyArray,
    xnew: AnyArray,
    method: str,
    scale: str = SCALE_LINEAR,
) -> tuple[AnyArray, int, int]:
    """Interpolate y(x) at xnew without extrapolation."""
    x_unique, y_unique, removed_invalid, removed_duplicates = clean_sort_unique_xy(x, y)
    if len(x_unique) < 2:
        raise ValueError("At least 2 finite points with distinct x values are required")
    if xnew[0] < x_unique[0] - np.finfo(float).eps or xnew[-1] > x_unique[-1] + np.finfo(float).eps:
        raise ValueError("Interpolation range is outside the valid x range")
    if scale == SCALE_LOG:
        if np.any(x_unique <= 0) or np.any(y_unique <= 0) or np.any(xnew <= 0):
            raise ValueError("Logarithmic interpolation requires positive x and y values")
        x_fit = np.log10(x_unique)
        y_fit = np.log10(y_unique)
        x_eval = np.log10(xnew)
    elif scale == SCALE_LINEAR:
        x_fit = x_unique
        y_fit = y_unique
        x_eval = xnew
    else:
        raise ValueError("Unknown interpolation scale: %s" % scale)

    if method == METHOD_PCHIP:
        interpolator = PchipInterpolator(x_fit, y_fit, extrapolate=False)
    elif method == METHOD_CUBIC:
        if len(x_unique) < 4:
            raise ValueError("Cubic spline requires at least 4 finite points with distinct x values")
        interpolator = CubicSpline(x_fit, y_fit, extrapolate=False)
    else:
        raise ValueError("Unknown interpolation method: %s" % method)

    ynew = interpolator(x_eval)
    if scale == SCALE_LOG:
        ynew = np.power(10.0, ynew)
    if not np.all(np.isfinite(ynew)):
        raise ValueError("Interpolation produced NaN or Inf values")
    return ynew, removed_invalid, removed_duplicates


def make_resampling_grid(xmin: float, xmax: float, npoints: int, scale: str) -> AnyArray:
    """Return an output x grid in linear or logarithmic spacing."""
    if scale == SCALE_LINEAR:
        return np.linspace(xmin, xmax, npoints)
    if scale == SCALE_LOG:
        if xmin <= 0 or xmax <= 0:
            raise ValueError("Logarithmic interpolation requires positive x values")
        return np.logspace(np.log10(xmin), np.log10(xmax), npoints)
    raise ValueError("Unknown interpolation scale: %s" % scale)


class ToolResampleData(QTool):
    """Resample the current view data by interpolation."""

    toolname: ClassVar[str] = "Resample Data"
    description: ClassVar[str] = "Resample current view data by interpolation"
    citations: ClassVar[list[str]] = []

    method_combo: QComboBox
    scale_combo: QComboBox

    def __init__(self, name: str = "", parent_app: ApplicationLike | None = None) -> None:
        """**Constructor**"""
        super().__init__(name, parent_app)
        self.parameters["npoints"] = Parameter(
            name="npoints",
            value=100,
            description="Number of output points",
            type=ParameterType.integer,
            opt_type=OptType.const,
            min_value=2,
        )
        self.parameters["method"] = Parameter(
            name="method",
            value=METHOD_PCHIP,
            description="Interpolation method: PCHIP or Cubic spline",
            type=ParameterType.string,
            opt_type=OptType.const,
            display_flag=False,
        )
        self.parameters["scale"] = Parameter(
            name="scale",
            value=SCALE_LINEAR,
            description="Interpolation scale: Linear or Logarithmic",
            type=ParameterType.string,
            opt_type=OptType.const,
            display_flag=False,
        )

        self.update_parameter_table()

        self.tb.addWidget(QLabel("Method:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems(INTERPOLATION_METHODS)
        self.method_combo.setToolTip("Interpolation method")
        self.method_combo.currentTextChanged.connect(self.handle_method_changed)
        self.tb.addWidget(self.method_combo)
        self.tb.addWidget(QLabel("Scale:"))
        self.scale_combo = QComboBox()
        self.scale_combo.addItems(INTERPOLATION_SCALES)
        self.scale_combo.setToolTip("Interpolation scale")
        self.scale_combo.currentTextChanged.connect(self.handle_scale_changed)
        self.tb.addWidget(self.scale_combo)

        self.parent_application.update_all_ds_plots()

    def handle_method_changed(self, method: str) -> None:
        self.set_param_value("method", method)
        self.update_parameter_table()
        self.parent_application.update_all_ds_plots()

    def handle_scale_changed(self, scale: str) -> None:
        self.set_param_value("scale", scale)
        self.update_parameter_table()
        self.parent_application.update_all_ds_plots()

    def set_param_value(self, name: str, value: Any) -> tuple[str, bool]:
        if name == "method":
            method = str(value)
            if method not in INTERPOLATION_METHODS:
                return "Method must be one of: %s" % ", ".join(INTERPOLATION_METHODS), False
            self.parameters[name].value = method
            if hasattr(self, "method_combo") and self.method_combo.currentText() != method:
                self.method_combo.setCurrentText(method)
            return "", True
        if name == "scale":
            scale = str(value)
            if scale not in INTERPOLATION_SCALES:
                return "Scale must be one of: %s" % ", ".join(INTERPOLATION_SCALES), False
            self.parameters[name].value = scale
            if hasattr(self, "scale_combo") and self.scale_combo.currentText() != scale:
                self.scale_combo.setCurrentText(scale)
            return "", True
        return super().set_param_value(name, value)

    def calculate_all(
        self,
        n: int,
        x: AnyArray,
        y: AnyArray,
        ax: AxesLike | None = None,
        color: Any = None,
        file_parameters: FileParameters | None = None,
    ) -> ToolResult:
        """Resample all displayed y series on a common uniformly spaced x grid."""
        npoints = self.parameter_int("npoints")
        method = self.parameter_str("method")
        scale = self.parameter_str("scale")

        view = self._view_from_axes(ax)
        if view is not None:
            x_interp, y_interp = view.convert_xy_to_display(x, y)
        else:
            x_interp, y_interp = x, y

        try:
            clean_series = [
                clean_sort_unique_xy(x_interp[:, i], y_interp[:, i])
                for i in range(n)
            ]
            if any(len(series[0]) < 2 for series in clean_series):
                raise ValueError("At least 2 finite points with distinct x values are required in each series")
            if method == METHOD_CUBIC and any(len(series[0]) < 4 for series in clean_series):
                raise ValueError("Cubic spline requires at least 4 finite points with distinct x values in each series")

            xmin = min(float(series[0][0]) for series in clean_series)
            xmax = max(float(series[0][-1]) for series in clean_series)
            if xmin == xmax:
                raise ValueError("Cannot resample data with zero x range")
            for series in clean_series:
                x_unique = series[0]
                if xmin < x_unique[0] or xmax > x_unique[-1]:
                    raise ValueError("All displayed y series must cover the common x range")

            xnew = make_resampling_grid(xmin, xmax, npoints, scale)
            xnew_all = np.empty((npoints, n))
            ynew_all = np.empty((npoints, n))
            total_invalid = 0
            total_duplicates = 0
            for i in range(n):
                ynew, removed_invalid, removed_duplicates = resample_xy(
                    x_interp[:, i],
                    y_interp[:, i],
                    xnew,
                    method,
                    scale,
                )
                xnew_all[:, i] = xnew
                ynew_all[:, i] = ynew
                total_invalid += removed_invalid
                total_duplicates += removed_duplicates

            if total_invalid:
                self.Qprint("Ignored %d NaN/Inf point(s)" % total_invalid)
            if total_duplicates:
                self.Qprint("Consolidated %d repeated x value(s) by averaging y" % total_duplicates)
            self.Qprint("Resampled to %d point(s) using %s, %s scale" % (npoints, method, scale))

            if view is not None:
                return view.convert_xy_to_internal(xnew_all, ynew_all)
            return xnew_all, ynew_all
        except Exception:
            self.Qprint("<b><font color=red>in ToolResampleData.calculate_all():</font></b> %s" % traceback.format_exc())
            return x, y

    def calculate(
        self,
        x: AnyArray,
        y: AnyArray,
        ax: AxesLike | None = None,
        color: Any = None,
        file_parameters: FileParameters | None = None,
    ) -> ToolResult:
        """Resample a single x/y series."""
        npoints = self.parameter_int("npoints")
        method = self.parameter_str("method")
        scale = self.parameter_str("scale")
        try:
            x_unique, _, _, _ = clean_sort_unique_xy(x, y)
            xnew = make_resampling_grid(float(x_unique[0]), float(x_unique[-1]), npoints, scale)
            ynew, removed_invalid, removed_duplicates = resample_xy(x, y, xnew, method, scale)
            if removed_invalid:
                self.Qprint("Ignored %d NaN/Inf point(s)" % removed_invalid)
            if removed_duplicates:
                self.Qprint("Consolidated %d repeated x value(s) by averaging y" % removed_duplicates)
            return xnew, ynew
        except Exception:
            self.Qprint("<b><font color=red>in ToolResampleData.calculate():</font></b> %s" % traceback.format_exc())
            return x, y

    def _view_from_axes(self, ax: AxesLike | None) -> ViewLike | None:
        if ax is None:
            return None
        try:
            for i, app_ax in enumerate(self.parent_application.axarr):
                if app_ax is ax:
                    return self.parent_application.multiviews[i]
        except Exception:
            return None
        return None
