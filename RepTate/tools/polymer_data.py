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
"""Module polymer_data

Module to define the basic information about a polymer for the materials database.

"""

from typing import Any, TypeAlias

from RepTate.core.units import convert_value


MaterialParameterUnits: TypeAlias = dict[str, str]


MATERIAL_DATABASE_UNIT_SYSTEM: str = "RepTate internal units v1"


MATERIAL_PARAMETER_UNITS: dict[str, MaterialParameterUnits] = {
    "tau_e": {
        "quantity": "time",
        "internal_unit": "s",
        "display_unit": "s",
        "legacy_unit": "s",
    },
    "Ge": {
        "quantity": "stress",
        "internal_unit": "Pa",
        "display_unit": "Pa",
        "legacy_unit": "Pa",
    },
    "B2": {
        "quantity": "temperature",
        "internal_unit": "°C",
        "display_unit": "°C",
        "legacy_unit": "°C",
    },
    "Me": {
        "quantity": "molar_mass",
        "internal_unit": "kg/mol",
        "display_unit": "kg/mol",
        "legacy_unit": "kDa",
    },
    "rho0": {
        "quantity": "density",
        "internal_unit": "kg/m3",
        "display_unit": "g/cm3",
        "legacy_unit": "g/cm3",
    },
    "Te": {
        "quantity": "temperature",
        "internal_unit": "°C",
        "display_unit": "°C",
        "legacy_unit": "°C",
    },
    "M0": {
        "quantity": "molar_mass",
        "internal_unit": "kg/mol",
        "display_unit": "g/mol",
        "legacy_unit": "g/mol",
    },
    "MK": {
        "quantity": "molar_mass",
        "internal_unit": "kg/mol",
        "display_unit": "Da",
        "legacy_unit": "Da",
    },
}


def material_parameter_units(name: str) -> MaterialParameterUnits:
    """Return unit metadata for a material parameter, if known."""
    return MATERIAL_PARAMETER_UNITS.get(name, {})


def canonicalize_material(material: Any) -> Any:
    """Convert a material from legacy database units to RepTate internal units."""
    if getattr(material, "unit_system", "") == MATERIAL_DATABASE_UNIT_SYSTEM:
        return material
    for name, units in MATERIAL_PARAMETER_UNITS.items():
        if name not in material.data:
            continue
        value = material.data[name]
        if not isinstance(value, (int, float)):
            continue
        material.data[name] = float(
            convert_value(value, units["legacy_unit"], units["internal_unit"])
        )
    material.unit_system = MATERIAL_DATABASE_UNIT_SYSTEM
    return material


def canonicalize_database(database: dict[Any, Any]) -> dict[Any, Any]:
    """Convert all materials in a database dictionary to internal units."""
    for material in database.values():
        canonicalize_material(material)
    return database


def convert_database_value_to_parameter(
    name: str, value: Any, target_parameter: Any
) -> Any:
    """Convert a database value to the target parameter's declared internal unit."""
    units = material_parameter_units(name)
    target_unit = getattr(target_parameter, "internal_unit", "")
    if not units or not target_unit or target_unit == units["internal_unit"]:
        return value
    return convert_value(value, units["internal_unit"], target_unit)


class polymer:
    """Defines the basic information held by the materials database"""

    def __init__(self, **kwargs: Any) -> None:
        """**Constructor**"""
        self.unit_system: str = kwargs.pop("unit_system", "legacy")
        self.data: dict[str, Any] = {
            # Basic info
            "name": "",  # Short name
            "long": "",  # Full name
            "author": "",  # Who added/Modified the parameters
            "date": "",  # Date of parameter modification
            "source": "",  # Source/paper from where the data was obtained
            "comment": "",  # Additional comments about the parameters
            "chem": "",  # Short hand Chemistry
            # WLF Parameters
            "B1": 0,  # Material parameter B1 for WLF Shift
            "B2": 0,  # Material parameter B2 for WLF Shift
            "logalpha": 0,  # Log_10 of the thermal expansion coefficient at 0 °C
            "CTg": 0,  # Molecular weight dependence of Tg
            # Likhtman-McLeish parameters
            "tau_e": 0,  # Rouse time of one entanglement
            "Ge": 0,  # Entanglement modulus
            "Me": 0,  # Entanglemnet molecular while
            "c_nu": 0,  # Constraint release parameter
            "rho0": 0,  # Density of polymer at 0 °C
            "Te": 0,  # Temperature at which the tube parameters have been determined
            "M0": 0,  # Molecular weight of repeating unit
        }

        self.data.update(kwargs)

    # def __init__ (self, oldpolymer):
    #     self.data={}
    #     for k in oldpolymer.data.keys():
    #         self.data[k] = oldpolymer.data[k]
