"""Minimal unit conversion helpers for RepTate.

The module intentionally uses only multiplicative conversion factors. Offset
units such as Celsius are not included until the conversion model needs them.
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Unit:
    symbol: str
    quantity: str
    factor_to_internal: float
    label: str = ""

    def __post_init__(self):
        if not self.label:
            object.__setattr__(self, "label", self.symbol)


@dataclass(frozen=True)
class ColumnSpec:
    name: str
    display_unit: str
    internal_unit: str
    quantity: str = ""

    def axis_label(self):
        if self.internal_unit in ("", "-"):
            return self.name
        return "%s [%s]" % (self.name, self.internal_unit)


_UNITS = {
    "-": Unit("-", "dimensionless", 1.0),
    "s": Unit("s", "time", 1.0),
    "min": Unit("min", "time", 60.0),
    "h": Unit("h", "time", 3600.0),
    "rad/s": Unit("rad/s", "angular_frequency", 1.0),
    "Hz": Unit("Hz", "frequency", 1.0),
    "Pa": Unit("Pa", "stress", 1.0),
    "kPa": Unit("kPa", "stress", 1.0e3),
    "MPa": Unit("MPa", "stress", 1.0e6),
    "bar": Unit("bar", "stress", 1.0e5),
    "atm": Unit("atm", "stress", 101325.0),
    "Pa.s": Unit("Pa.s", "viscosity", 1.0),
    "kPa.s": Unit("kPa.s", "viscosity", 1.0e3),
    "K": Unit("K", "temperature", 1.0),
    "g/mol": Unit("g/mol", "molar_mass", 1.0),
    "kg/mol": Unit("kg/mol", "molar_mass", 1.0e3),
}

_INTERNAL_UNITS = {
    "dimensionless": "-",
    "time": "s",
    "angular_frequency": "rad/s",
    "frequency": "Hz",
    "stress": "Pa",
    "viscosity": "Pa.s",
    "temperature": "K",
    "molar_mass": "g/mol",
}

_CONTEXTUAL_CONVERSIONS = {
    ("Hz", "rad/s"): 2.0 * np.pi,
}


def get_unit(symbol):
    """Return the Unit registered for *symbol*."""
    try:
        return _UNITS[symbol]
    except KeyError as exc:
        raise ValueError("Unknown unit: %s" % symbol) from exc


def available_units(quantity):
    """Return registered units for a quantity."""
    units = tuple(unit for unit in _UNITS.values() if unit.quantity == quantity)
    if not units:
        raise ValueError("Unknown quantity: %s" % quantity)
    return units


def make_column_spec(name, unit_symbol, expected_unit_symbol=None):
    """Create metadata for a data column.

    Unknown units preserve RepTate's current implicit behavior: values are kept
    unchanged and the declared unit is treated as the internal unit.
    """
    if (unit_symbol, expected_unit_symbol) in _CONTEXTUAL_CONVERSIONS:
        expected_unit = get_unit(expected_unit_symbol)
        return ColumnSpec(
            name=name,
            display_unit=unit_symbol,
            internal_unit=_INTERNAL_UNITS[expected_unit.quantity],
            quantity=expected_unit.quantity,
        )
    try:
        unit = get_unit(unit_symbol)
    except ValueError:
        return ColumnSpec(name=name, display_unit=unit_symbol, internal_unit=unit_symbol)
    return ColumnSpec(
        name=name,
        display_unit=unit.symbol,
        internal_unit=_INTERNAL_UNITS[unit.quantity],
        quantity=unit.quantity,
    )


def make_column_specs(names, unit_symbols, expected_unit_symbols=None):
    """Create column metadata from parallel column name and unit lists."""
    expected_unit_symbols = expected_unit_symbols or unit_symbols
    return [
        make_column_spec(
            name,
            unit_symbols[i] if i < len(unit_symbols) else "-",
            expected_unit_symbols[i] if i < len(expected_unit_symbols) else None,
        )
        for i, name in enumerate(names)
    ]


def units_are_compatible(from_unit, to_unit):
    """Return True when both units describe the same quantity."""
    source = get_unit(from_unit)
    target = get_unit(to_unit)
    return source.quantity == target.quantity


def _conversion_factor(from_unit, to_unit):
    source = get_unit(from_unit)
    target = get_unit(to_unit)
    if source.quantity != target.quantity:
        raise ValueError(
            "Incompatible units: %s (%s) and %s (%s)"
            % (source.symbol, source.quantity, target.symbol, target.quantity)
        )
    return source.factor_to_internal / target.factor_to_internal


def convert_value(value, from_unit, to_unit):
    """Convert a scalar value between compatible units."""
    return value * _conversion_factor(from_unit, to_unit)


def convert_array(values, from_unit, to_unit):
    """Convert array-like values between compatible units."""
    return np.asarray(values) * _conversion_factor(from_unit, to_unit)


def convert_array_to_internal(values, unit_symbol, internal_unit_symbol=None):
    """Convert values to the registered internal unit, preserving unknown units."""
    if (unit_symbol, internal_unit_symbol) in _CONTEXTUAL_CONVERSIONS:
        return np.asarray(values) * _CONTEXTUAL_CONVERSIONS[(unit_symbol, internal_unit_symbol)]
    try:
        unit = get_unit(unit_symbol)
    except ValueError:
        return np.asarray(values)
    return convert_array(values, unit.symbol, internal_unit_symbol or _INTERNAL_UNITS[unit.quantity])
