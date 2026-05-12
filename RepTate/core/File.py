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
"""Module File

Module that defines a basic File, with headers, columns and data.

"""
import os
from dataclasses import dataclass
from typing import Any, TypeAlias
from RepTate.core.DataTable import DataTable
from RepTate.core.units import convert_value, get_unit


FileParameterValue: TypeAlias = Any
FileParameters: TypeAlias = dict[str, FileParameterValue]


@dataclass(frozen=True)
class FileParameterSpec:
    """Optional metadata for a file-level parameter.

    Values stored in ``File.file_parameters`` remain plain Python values. When a
    spec declares units, helper methods convert values at the boundary so stored
    numeric values use RepTate's canonical internal units.
    """

    name: str
    quantity: str = ""
    internal_unit: str = ""
    display_unit: str = ""

    def __post_init__(self) -> None:
        if not any((self.quantity, self.internal_unit, self.display_unit)):
            return
        if not all((self.quantity, self.internal_unit, self.display_unit)):
            raise ValueError(
                "File parameter '%s' has incomplete unit metadata" % self.name
            )
        internal = get_unit(self.internal_unit)
        display = get_unit(self.display_unit)
        if internal.quantity != self.quantity:
            raise ValueError(
                "File parameter '%s' internal unit %s has quantity %s, expected %s"
                % (self.name, internal.symbol, internal.quantity, self.quantity)
            )
        if display.quantity != self.quantity:
            raise ValueError(
                "File parameter '%s' display unit %s has quantity %s, expected %s"
                % (self.name, display.symbol, display.quantity, self.quantity)
            )

    def value_to_display(
        self, value: FileParameterValue
    ) -> FileParameterValue:
        """Convert an internally stored value to the display unit."""
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                return value
        if self.internal_unit and self.display_unit:
            return convert_value(value, self.internal_unit, self.display_unit)
        return value

    def value_from_display(
        self, value: FileParameterValue
    ) -> FileParameterValue:
        """Convert a display/input value to the internal unit."""
        if isinstance(value, str):
            value = float(value)
        if self.internal_unit and self.display_unit:
            return convert_value(value, self.display_unit, self.internal_unit)
        return value

    def value_from_unit(
        self, value: FileParameterValue, unit_symbol: str
    ) -> FileParameterValue:
        """Convert a value expressed in ``unit_symbol`` to the internal unit."""
        if isinstance(value, str):
            value = float(value)
        if self.internal_unit and unit_symbol:
            return convert_value(value, unit_symbol, self.internal_unit)
        return value

    def label_with_unit(self) -> str:
        """Return a user-facing label for this parameter."""
        if self.display_unit and self.display_unit != "-":
            return "%s [%s]" % (self.name, self.display_unit)
        return self.name


FileParameterSpecs: TypeAlias = dict[str, FileParameterSpec]


class File(object):
    """Basic class that describes elements of a DataSet"""

    def __init__(
        self,
        file_name: str = "",
        file_type: Any = None,
        parent_dataset: Any = None,
        axarr: Any = None,
    ) -> None:
        """**Constructor**"""
        self.file_full_path: str = os.path.abspath(file_name)
        tmpname = os.path.basename(self.file_full_path)
        self.file_name_short: str = os.path.splitext(tmpname)[0]
        self.file_type: Any = file_type
        self.parent_dataset: Any = parent_dataset
        self.axarr: Any = axarr

        #plot attributes
        self.marker: Any = None
        self.color: Any = None
        self.filled: Any = None
        self.size: Any = None

        # Shift variables
        self.isshifted: list[bool] = [False]*DataTable.MAX_NUM_SERIES
        self.xshift: list[float | int] = [0]*DataTable.MAX_NUM_SERIES
        self.yshift: list[float | int] = [0]*DataTable.MAX_NUM_SERIES

        self.header_lines: list[str] = []
        self.file_parameters: FileParameters = {}
        self.file_parameter_specs: FileParameterSpecs = {}
        if file_type is not None:
            self.file_parameter_specs.update(
                getattr(file_type, "file_parameter_specs", {})
            )
        self.active: bool = True
        self.data_table: DataTable = DataTable(axarr, self.file_name_short)
        # extra theory xrange
        self.with_extra_x: bool = False
        self.theory_xmin: Any = "None"
        self.theory_xmax: Any = "None"
        self.theory_logspace: bool = True
        self.th_num_pts: int = 10 # number of points
        self.nextramin: int = 0
        self.nextramax: int = 0

    def __str__(self) -> Any:
        """Return a string"""
        # return Fore.YELLOW + 'File: ' + Fore.RESET  + '%s\n'%self.file_name_short + Fore.CYAN  + 'Path: ' + Fore.RESET + '%s\n'%self.file_full_path + Fore.RED + 'Parameters: ' + Fore.RESET + '%s'%self.file_parameters
        pass

    def mincol(self, col: int) -> Any:
        """Minimum value in data_table column col"""
        return self.data_table.mincol(col)

    def minpositivecol(self, col: int) -> Any:
        """Minimum positive value in data_table column col"""
        return self.data_table.minpositivecol(col)

    def maxcol(self, col: int) -> Any:
        """Maximum value in data_table column col"""
        return self.data_table.maxcol(col)

    def set_file_parameter_spec(self, spec: FileParameterSpec) -> None:
        """Attach optional metadata to a file parameter."""
        self.file_parameter_specs[spec.name] = spec

    def set_file_parameter(
        self,
        name: str,
        value: FileParameterValue,
        spec: FileParameterSpec | None = None,
        from_display: bool = True,
        source_unit: str | None = None,
    ) -> None:
        """Set a file parameter, converting to internal units when possible."""
        if spec is not None:
            self.set_file_parameter_spec(spec)
        spec = self.file_parameter_specs.get(name)
        if spec is not None:
            if source_unit is not None:
                value = spec.value_from_unit(value, source_unit)
            elif from_display:
                value = spec.value_from_display(value)
        self.file_parameters[name] = value

    def file_parameter_value_to_display(
        self, name: str, value: FileParameterValue | None = None
    ) -> FileParameterValue:
        """Return a file parameter value converted to display units."""
        value = self.file_parameters[name] if value is None else value
        spec = self.file_parameter_specs.get(name)
        if spec is None:
            return value
        return spec.value_to_display(value)

    def file_parameter_value_from_display(
        self, name: str, value: FileParameterValue
    ) -> FileParameterValue:
        """Convert a display value to this parameter's internal units."""
        spec = self.file_parameter_specs.get(name)
        if spec is None:
            return value
        return spec.value_from_display(value)

    def file_parameter_label(self, name: str) -> str:
        """Return the parameter label with display unit metadata when present."""
        spec = self.file_parameter_specs.get(name)
        if spec is None:
            return name
        return spec.label_with_unit()
