# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# --------------------------------------------------------------------------------------------------------
#
# Authors:
#     Jorge Ramirez, jorge.ramirez@upm.es
#     Victor Boudara, victor.boudara@gmail.com
#
# Useful links:
#     http://blogs.upm.es/compsoftmatter/software/reptate/
#     https://github.com/jorge-ramirez-upm/RepTate
#     http://reptate.readthedocs.io
#
# --------------------------------------------------------------------------------------------------------
#
# Copyright (2017-2026): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module View

Module that defines the basic properties of a View, that will be used to represent
the data graphically.

"""
import enum
from dataclasses import dataclass
from collections.abc import Callable, Sequence
from typing import Any, TypeAlias

import numpy as np
from numpy.typing import ArrayLike, NDArray

from RepTate.core.units import available_units, convert_array_to_internal, get_unit


NumericArray: TypeAlias = NDArray[Any]
ViewCallback: TypeAlias = Callable[..., Any]


class ViewMode(enum.Enum):
    """Defines how to show the experimental/theoretical data view
    TO BE DONE...
    
    Parameters can be:
        - symbol: Show symbols (default for experimental data -- files in the dataset)
        - line: Show lines (default for theories)
        - bar: Show bars 
    """

    symbol = 0
    line = 1
    bar = 2


@dataclass
class AxisSpec:
    """Describe the unit behaviour of a plotted axis."""

    label: str = ""
    internal_unit: str = ""
    display_unit: str = ""
    quantity: str = ""
    transform: str = "identity"
    unit_choices: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.display_unit:
            self.display_unit = self.internal_unit
        if not self.quantity and self.internal_unit not in ("", "-"):
            try:
                self.quantity = get_unit(self.internal_unit).quantity
            except ValueError:
                self.quantity = ""
        if not self.unit_choices and self.quantity:
            self.unit_choices = tuple(unit.symbol for unit in available_units(self.quantity))

    def is_unit_aware(self):
        return self.internal_unit not in ("", "-") and self.display_unit not in ("", "-")

    def axis_label(self) -> str:
        if self.display_unit in ("", "-"):
            return self.label
        return "%s [%s]" % (self.label, self.display_unit)

    def available_display_units(self) -> list[str]:
        units = []
        for unit_symbol in self.unit_choices:
            if self.transform == "log10":
                try:
                    unit = get_unit(unit_symbol)
                    internal = get_unit(self.internal_unit)
                except ValueError:
                    continue
                if unit.offset_to_internal != 0.0 or internal.offset_to_internal != 0.0:
                    continue
            if unit_symbol not in units:
                units.append(unit_symbol)
        return units

    def set_display_unit(self, unit_symbol: str) -> None:
        self.display_unit = unit_symbol

    def convert_from_internal(self, values: ArrayLike) -> NumericArray:
        arr = np.asarray(values)
        if not self.is_unit_aware() or self.display_unit == self.internal_unit:
            return arr
        if self.transform == "identity":
            return convert_array_to_internal(arr, self.internal_unit, self.display_unit)
        if self.transform == "log10":
            return arr + np.log10(self._conversion_factor_from_internal())
        raise ValueError("Unknown axis transform: %s" % self.transform)

    def convert_to_internal(self, values: ArrayLike) -> NumericArray:
        arr = np.asarray(values)
        if not self.is_unit_aware() or self.display_unit == self.internal_unit:
            return arr
        if self.transform == "identity":
            return convert_array_to_internal(arr, self.display_unit, self.internal_unit)
        if self.transform == "log10":
            return arr - np.log10(self._conversion_factor_from_internal())
        raise ValueError("Unknown axis transform: %s" % self.transform)

    def _conversion_factor_from_internal(self) -> float:
        internal = get_unit(self.internal_unit)
        display = get_unit(self.display_unit)
        if internal.offset_to_internal != 0.0 or display.offset_to_internal != 0.0:
            raise ValueError(
                "Log-transformed axes do not support affine units: %s -> %s"
                % (self.internal_unit, self.display_unit)
            )
        factor = convert_array_to_internal(
            np.asarray([1.0]), self.internal_unit, self.display_unit
        )[0]
        if factor <= 0.0:
            raise ValueError(
                "Log-transformed axes require positive conversion factors: %s -> %s"
                % (self.internal_unit, self.display_unit)
            )
        return float(factor)


class View(object):
    """Abstract class to describe a view"""

    def __init__(
        self,
        name: str = "",
        description: str = "",
        x_label: str = "",
        y_label: str = "",
        x_units: str = "",
        y_units: str = "",
        log_x: bool = False,
        log_y: bool = False,
        view_proc: ViewCallback | None = None,
        n: int = 1,
        snames: Sequence[str] = [],
        inverse_view_proc: ViewCallback | None = None,
        index: int = 0,
        with_thline: bool = True,
        filled: bool = False,
        viewmode_data: ViewMode = ViewMode.symbol,
        viewmode_theory: ViewMode = ViewMode.line,
        x_axis: AxisSpec | None = None,
        y_axis: AxisSpec | None = None,
    ) -> None:
        """**Constructor**
        
        Keyword Arguments:
            - name {str} -- View name
            - description {str} -- Description of the view
            - x_label {str} -- Label of the x axis
            - y_label {str} -- Label of the y axis
            - x_units {str} -- Default units of the x axis
            - y_units {str} -- Default units of the y axis
            - log_x {bool} -- X axis logarithmic? (default: {False})
            - log_y {bool} -- Y axis logarithmic? (default: {False})
            - view_proc {func} -- Function that creates the X, Y1, Y2 values of the view (default: {None})
            - inverse_view_proc {func} -- Function that inverses the view: From the n values of the view, returns the data table values (default: {None})
            - n {int} -- Number of series that the view represents (default: {1})
            - snames {list of str} -- Names of the series represented by the view
            - with_thline {bool} -- if True, plot the theory with lines, else use symbols
            - filled {bool} -- if True, use filled symbols (when with_thline=False)
        """
        self.name: str = name
        self.description: str = description
        self.x_label: str = x_label
        self.y_label: str = y_label
        self.x_units: str = x_units
        self.y_units: str = y_units
        self.x_axis: AxisSpec = x_axis or AxisSpec(label=x_label, display_unit=x_units)
        self.y_axis: AxisSpec = y_axis or AxisSpec(label=y_label, display_unit=y_units)
        self.log_x: bool = log_x
        self.log_y: bool = log_y
        self.view_proc: ViewCallback | None = view_proc
        self.inverse_view_proc: ViewCallback | None = inverse_view_proc
        self.n: int = n
        self.snames: Sequence[str] = snames
        self.with_thline: bool = with_thline
        self.filled: bool = filled
        self.viewmode_data: ViewMode = viewmode_data
        self.viewmode_theory: ViewMode = viewmode_theory

    def convert_xy_to_display(
        self, x: ArrayLike, y: ArrayLike
    ) -> tuple[NumericArray, NumericArray]:
        return self.x_axis.convert_from_internal(x), self.y_axis.convert_from_internal(y)

    def convert_xy_to_internal(
        self, x: ArrayLike, y: ArrayLike
    ) -> tuple[NumericArray, NumericArray]:
        return self.x_axis.convert_to_internal(x), self.y_axis.convert_to_internal(y)
