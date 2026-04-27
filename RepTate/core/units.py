"""Minimal unit conversion helpers for RepTate.

Units may use either multiplicative or affine conversions to the internal
canonical unit for their quantity. Generic conversions are only allowed within a
single quantity; frequency and angular frequency require explicit helpers.
"""

from dataclasses import dataclass
import re

import numpy as np


@dataclass(frozen=True)
class Unit:
    symbol: str
    quantity: str
    factor_to_internal: float
    offset_to_internal: float = 0.0
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


_UNIT_LABEL_RE = re.compile(
    r"^\s*(?P<label>.+?)\s+(?:\[(?P<bracket>[^\]]+)\]|\((?P<paren>[^)]+)\))\s*$"
)
_PARAMETER_VALUE_UNIT_RE = re.compile(
    r"^\s*(?P<number>[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s+(?P<unit>\S+)\s*$"
)


_UNITS = {
    "-": Unit("-", "dimensionless", 1.0),
    "ns": Unit("ns", "time", 1.0e-9),
    "μs": Unit("μs", "time", 1.0e-6),
    "ms": Unit("ms", "time", 1.0e-3),
    "s": Unit("s", "time", 1.0),
    "min": Unit("min", "time", 60.0),
    "h": Unit("h", "time", 3600.0),
    "1/A": Unit("1/A", "inverse_distance", 1.0),
    "1/Å": Unit("1/Å", "inverse_distance", 1.0, 0.0, "1/A"),
    "A-1": Unit("A-1", "inverse_distance", 1.0, 0.0, "1/A"),
    "A^-1": Unit("A^-1", "inverse_distance", 1.0, 0.0, "1/A"),
    "A⁻¹": Unit("A⁻¹", "inverse_distance", 1.0, 0.0, "1/A"),
    "Å-1": Unit("Å-1", "inverse_distance", 1.0, 0.0, "1/A"),
    "Å^-1": Unit("Å^-1", "inverse_distance", 1.0, 0.0, "1/A"),
    "Å⁻¹": Unit("Å⁻¹", "inverse_distance", 1.0, 0.0, "1/A"),
    "1/nm": Unit("1/nm", "inverse_distance", 1.0e-1),
    "nm-1": Unit("nm-1", "inverse_distance", 1.0e-1, 0.0, "1/nm"),
    "nm^-1": Unit("nm^-1", "inverse_distance", 1.0e-1, 0.0, "1/nm"),
    "nm⁻¹": Unit("nm⁻¹", "inverse_distance", 1.0e-1, 0.0, "1/nm"),
    "1/um": Unit("1/um", "inverse_distance", 1.0e-4),
    "1/μm": Unit("1/μm", "inverse_distance", 1.0e-4, 0.0, "1/um"),
    "um-1": Unit("um-1", "inverse_distance", 1.0e-4, 0.0, "1/um"),
    "um^-1": Unit("um^-1", "inverse_distance", 1.0e-4, 0.0, "1/um"),
    "um⁻¹": Unit("um⁻¹", "inverse_distance", 1.0e-4, 0.0, "1/um"),
    "μm-1": Unit("μm-1", "inverse_distance", 1.0e-4, 0.0, "1/um"),
    "μm^-1": Unit("μm^-1", "inverse_distance", 1.0e-4, 0.0, "1/um"),
    "μm⁻¹": Unit("μm⁻¹", "inverse_distance", 1.0e-4, 0.0, "1/um"),
    "1/mm": Unit("1/mm", "inverse_distance", 1.0e-7),
    "mm-1": Unit("mm-1", "inverse_distance", 1.0e-7, 0.0, "1/mm"),
    "mm^-1": Unit("mm^-1", "inverse_distance", 1.0e-7, 0.0, "1/mm"),
    "mm⁻¹": Unit("mm⁻¹", "inverse_distance", 1.0e-7, 0.0, "1/mm"),
    "1/cm": Unit("1/cm", "inverse_distance", 1.0e-8),
    "cm-1": Unit("cm-1", "inverse_distance", 1.0e-8, 0.0, "1/cm"),
    "cm^-1": Unit("cm^-1", "inverse_distance", 1.0e-8, 0.0, "1/cm"),
    "cm⁻¹": Unit("cm⁻¹", "inverse_distance", 1.0e-8, 0.0, "1/cm"),
    "1/m": Unit("1/m", "inverse_distance", 1.0e-10),
    "m-1": Unit("m-1", "inverse_distance", 1.0e-10, 0.0, "1/m"),
    "m^-1": Unit("m^-1", "inverse_distance", 1.0e-10, 0.0, "1/m"),
    "m⁻¹": Unit("m⁻¹", "inverse_distance", 1.0e-10, 0.0, "1/m"),
    "1/s/m3": Unit("1/s/m3", "nucleation_rate", 1.0),
    "1/s/m^3": Unit("1/s/m^3", "nucleation_rate", 1.0, 0.0, "1/s/m3"),
    "1/s/m³": Unit("1/s/m³", "nucleation_rate", 1.0, 0.0, "1/s/m3"),
    "1/m3/s": Unit("1/m3/s", "nucleation_rate", 1.0, 0.0, "1/s/m3"),
    "1/m^3/s": Unit("1/m^3/s", "nucleation_rate", 1.0, 0.0, "1/s/m3"),
    "1/m³/s": Unit("1/m³/s", "nucleation_rate", 1.0, 0.0, "1/s/m3"),
    "1/s/cm3": Unit("1/s/cm3", "nucleation_rate", 1.0e6),
    "1/s/cm^3": Unit("1/s/cm^3", "nucleation_rate", 1.0e6, 0.0, "1/s/cm3"),
    "1/s/cm³": Unit("1/s/cm³", "nucleation_rate", 1.0e6, 0.0, "1/s/cm3"),
    "1/cm3/s": Unit("1/cm3/s", "nucleation_rate", 1.0e6, 0.0, "1/s/cm3"),
    "1/cm^3/s": Unit("1/cm^3/s", "nucleation_rate", 1.0e6, 0.0, "1/s/cm3"),
    "1/cm³/s": Unit("1/cm³/s", "nucleation_rate", 1.0e6, 0.0, "1/s/cm3"),
    "1/s/mm3": Unit("1/s/mm3", "nucleation_rate", 1.0e9),
    "1/s/mm^3": Unit("1/s/mm^3", "nucleation_rate", 1.0e9, 0.0, "1/s/mm3"),
    "1/s/mm³": Unit("1/s/mm³", "nucleation_rate", 1.0e9, 0.0, "1/s/mm3"),
    "1/mm3/s": Unit("1/mm3/s", "nucleation_rate", 1.0e9, 0.0, "1/s/mm3"),
    "1/mm^3/s": Unit("1/mm^3/s", "nucleation_rate", 1.0e9, 0.0, "1/s/mm3"),
    "1/mm³/s": Unit("1/mm³/s", "nucleation_rate", 1.0e9, 0.0, "1/s/mm3"),
    "1/s/um3": Unit("1/s/um3", "nucleation_rate", 1.0e18),
    "1/s/um^3": Unit("1/s/um^3", "nucleation_rate", 1.0e18, 0.0, "1/s/um3"),
    "1/s/um³": Unit("1/s/um³", "nucleation_rate", 1.0e18, 0.0, "1/s/um3"),
    "1/s/μm3": Unit("1/s/μm3", "nucleation_rate", 1.0e18, 0.0, "1/s/um3"),
    "1/s/μm^3": Unit("1/s/μm^3", "nucleation_rate", 1.0e18, 0.0, "1/s/um3"),
    "1/s/μm³": Unit("1/s/μm³", "nucleation_rate", 1.0e18, 0.0, "1/s/um3"),
    "1/um3/s": Unit("1/um3/s", "nucleation_rate", 1.0e18, 0.0, "1/s/um3"),
    "1/um^3/s": Unit("1/um^3/s", "nucleation_rate", 1.0e18, 0.0, "1/s/um3"),
    "1/um³/s": Unit("1/um³/s", "nucleation_rate", 1.0e18, 0.0, "1/s/um3"),
    "1/μm3/s": Unit("1/μm3/s", "nucleation_rate", 1.0e18, 0.0, "1/s/um3"),
    "1/μm^3/s": Unit("1/μm^3/s", "nucleation_rate", 1.0e18, 0.0, "1/s/um3"),
    "1/μm³/s": Unit("1/μm³/s", "nucleation_rate", 1.0e18, 0.0, "1/s/um3"),
    "1/s/nm3": Unit("1/s/nm3", "nucleation_rate", 1.0e27),
    "1/s/nm^3": Unit("1/s/nm^3", "nucleation_rate", 1.0e27, 0.0, "1/s/nm3"),
    "1/s/nm³": Unit("1/s/nm³", "nucleation_rate", 1.0e27, 0.0, "1/s/nm3"),
    "1/nm3/s": Unit("1/nm3/s", "nucleation_rate", 1.0e27, 0.0, "1/s/nm3"),
    "1/nm^3/s": Unit("1/nm^3/s", "nucleation_rate", 1.0e27, 0.0, "1/s/nm3"),
    "1/nm³/s": Unit("1/nm³/s", "nucleation_rate", 1.0e27, 0.0, "1/s/nm3"),
    "m/s": Unit("m/s", "rate", 1.0),
    "m/min": Unit("m/min", "rate", 1.0 / 60.0),
    "m/h": Unit("m/h", "rate", 1.0 / 3600.0),
    "cm/s": Unit("cm/s", "rate", 1.0e-2),
    "cm/min": Unit("cm/min", "rate", 1.0e-2 / 60.0),
    "cm/h": Unit("cm/h", "rate", 1.0e-2 / 3600.0),
    "mm/s": Unit("mm/s", "rate", 1.0e-3),
    "mm/min": Unit("mm/min", "rate", 1.0e-3 / 60.0),
    "mm/h": Unit("mm/h", "rate", 1.0e-3 / 3600.0),
    "um/s": Unit("um/s", "rate", 1.0e-6),
    "um/min": Unit("um/min", "rate", 1.0e-6 / 60.0),
    "um/h": Unit("um/h", "rate", 1.0e-6 / 3600.0),
    "μm/s": Unit("μm/s", "rate", 1.0e-6, 0.0, "um/s"),
    "μm/min": Unit("μm/min", "rate", 1.0e-6 / 60.0, 0.0, "um/min"),
    "μm/h": Unit("μm/h", "rate", 1.0e-6 / 3600.0, 0.0, "um/h"),
    "nm/s": Unit("nm/s", "rate", 1.0e-9),
    "nm/min": Unit("nm/min", "rate", 1.0e-9 / 60.0),
    "nm/h": Unit("nm/h", "rate", 1.0e-9 / 3600.0),
    "1/m3": Unit("1/m3", "unit_density", 1.0),
    "1/m^3": Unit("1/m^3", "unit_density", 1.0, 0.0, "1/m3"),
    "1/m³": Unit("1/m³", "unit_density", 1.0, 0.0, "1/m3"),
    "1/L": Unit("1/L", "unit_density", 1.0e3),
    "1/cm3": Unit("1/cm3", "unit_density", 1.0e6),
    "1/cm^3": Unit("1/cm^3", "unit_density", 1.0e6, 0.0, "1/cm3"),
    "1/cm³": Unit("1/cm³", "unit_density", 1.0e6, 0.0, "1/cm3"),
    "1/mL": Unit("1/mL", "unit_density", 1.0e6),
    "1/mm3": Unit("1/mm3", "unit_density", 1.0e9),
    "1/mm^3": Unit("1/mm^3", "unit_density", 1.0e9, 0.0, "1/mm3"),
    "1/mm³": Unit("1/mm³", "unit_density", 1.0e9, 0.0, "1/mm3"),
    "1/um3": Unit("1/um3", "unit_density", 1.0e18),
    "1/um^3": Unit("1/um^3", "unit_density", 1.0e18, 0.0, "1/um3"),
    "1/um³": Unit("1/um³", "unit_density", 1.0e18, 0.0, "1/um3"),
    "1/μm3": Unit("1/μm3", "unit_density", 1.0e18, 0.0, "1/um3"),
    "1/μm^3": Unit("1/μm^3", "unit_density", 1.0e18, 0.0, "1/um3"),
    "1/μm³": Unit("1/μm³", "unit_density", 1.0e18, 0.0, "1/um3"),
    "1/nm3": Unit("1/nm3", "unit_density", 1.0e27),
    "1/nm^3": Unit("1/nm^3", "unit_density", 1.0e27, 0.0, "1/nm3"),
    "1/nm³": Unit("1/nm³", "unit_density", 1.0e27, 0.0, "1/nm3"),
    "1/s": Unit("1/s", "deformation_rate", 1.0),
    "s-1": Unit("s-1", "deformation_rate", 1.0, 0.0, "1/s"),
    "s^-1": Unit("s^-1", "deformation_rate", 1.0, 0.0, "1/s"),
    "s⁻¹": Unit("s⁻¹", "deformation_rate", 1.0, 0.0, "1/s"),
    "1/min": Unit("1/min", "deformation_rate", 1.0 / 60.0),
    "min-1": Unit("min-1", "deformation_rate", 1.0 / 60.0, 0.0, "1/min"),
    "min^-1": Unit("min^-1", "deformation_rate", 1.0 / 60.0, 0.0, "1/min"),
    "min⁻¹": Unit("min⁻¹", "deformation_rate", 1.0 / 60.0, 0.0, "1/min"),
    "1/h": Unit("1/h", "deformation_rate", 1.0 / 3600.0),
    "h-1": Unit("h-1", "deformation_rate", 1.0 / 3600.0, 0.0, "1/h"),
    "h^-1": Unit("h^-1", "deformation_rate", 1.0 / 3600.0, 0.0, "1/h"),
    "h⁻¹": Unit("h⁻¹", "deformation_rate", 1.0 / 3600.0, 0.0, "1/h"),
    "rad/s": Unit("rad/s", "angular_frequency", 1.0),
    "Hz": Unit("Hz", "frequency", 1.0),
    "Pa": Unit("Pa", "stress", 1.0),
    "kPa": Unit("kPa", "stress", 1.0e3),
    "MPa": Unit("MPa", "stress", 1.0e6),
    "bar": Unit("bar", "stress", 1.0e5),
    "atm": Unit("atm", "stress", 101325.0),
    "1/Pa": Unit("1/Pa", "compliance", 1.0),
    "1/kPa": Unit("1/kPa", "compliance", 1.0e-3),
    "1/MPa": Unit("1/MPa", "compliance", 1.0e-6),
    "1/bar": Unit("1/bar", "compliance", 1.0e-5),
    "1/atm": Unit("1/atm", "compliance", 1.0 / 101325.0),
    "Pa.s": Unit("Pa.s", "viscosity", 1.0),
    "kPa.s": Unit("kPa.s", "viscosity", 1.0e3),
    "rad": Unit("rad", "angle", 1.0),
    "deg": Unit("deg", "angle", np.pi / 180.0),
    "kg/m3": Unit("kg/m3", "density", 1.0),
    "kg/m^3": Unit("kg/m^3", "density", 1.0, 0.0, "kg/m3"),
    "kg/m³": Unit("kg/m³", "density", 1.0, 0.0, "kg/m3"),
    "g/cm3": Unit("g/cm3", "density", 1.0e3),
    "g/cm^3": Unit("g/cm^3", "density", 1.0e3, 0.0, "g/cm3"),
    "g/cm³": Unit("g/cm³", "density", 1.0e3, 0.0, "g/cm3"),
    "g/cc": Unit("g/cc", "density", 1.0e3),
    "g/mL": Unit("g/mL", "density", 1.0e3),
    "kg/L": Unit("kg/L", "density", 1.0e3),
    "1/K": Unit("1/K", "inverse_temperature", 1.0),
    "K^-1": Unit("K^-1", "inverse_temperature", 1.0, 0.0, "1/K"),
    "K⁻¹": Unit("K⁻¹", "inverse_temperature", 1.0, 0.0, "1/K"),
    "K": Unit("K", "temperature", 1.0),
    "ºC": Unit("ºC", "temperature", 1.0, 273.15),
    "°C": Unit("°C", "temperature", 1.0, 273.15, "ºC"),
    "g/mol": Unit("g/mol", "molar_mass", 1.0e-3),
    "kg/mol": Unit("kg/mol", "molar_mass", 1.0),
    "Da": Unit("Da", "molar_mass", 1.0e-3),
    "kDa": Unit("kDa", "molar_mass", 1.0)
}

_INTERNAL_UNITS = {
    "dimensionless": "-",
    "time": "s",
    "inverse_distance": "1/A",
    "nucleation_rate": "1/s/m3",
    "rate": "m/s",
    "unit_density": "1/m3",
    "deformation_rate": "1/s",
    "angular_frequency": "rad/s",
    "frequency": "Hz",
    "stress": "Pa",
    "compliance": "1/Pa",
    "viscosity": "Pa.s",
    "angle": "rad",
    "density": "kg/m3",
    "inverse_temperature": "1/K",
    "temperature": "K",
    "molar_mass": "kg/mol",
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


def parse_column_label(label):
    """Return ``(base_label, unit_symbol, original_label)`` for a column label.

    Unit symbols are parsed but not validated here. Validation belongs to the
    unit metadata layer so legacy or application-specific units can be handled
    consistently there.
    """
    match = _UNIT_LABEL_RE.match(label)
    if not match:
        return label, None, label
    unit_symbol = match.group("bracket") or match.group("paren")
    return match.group("label").strip(), unit_symbol.strip(), label


def parse_parameter_value(value):
    """Parse a file parameter value with an optional trailing unit.

    Returns ``(parsed_value, unit_symbol)`` where ``unit_symbol`` is ``None``
    for plain numbers or non-numeric strings.
    """
    if not isinstance(value, str):
        return value, None
    stripped = value.strip()
    match = _PARAMETER_VALUE_UNIT_RE.match(stripped)
    if match:
        return float(match.group("number")), match.group("unit").strip()
    try:
        return float(stripped), None
    except ValueError:
        return value, None


def make_column_spec(name, unit_symbol, expected_unit_symbol=None):
    """Create metadata for a data column.

    Unknown units preserve RepTate's current implicit behavior: values are kept
    unchanged and the declared unit is treated as the internal unit.
    """
    # This explicit boundary conversion supports legacy/application files that
    # declare frequency where RepTate expects angular frequency. It is not a
    # generic compatibility rule: convert_value("Hz", "rad/s") still raises.
    if (unit_symbol, expected_unit_symbol) in (("Hz", "rad/s"), ("rad/s", "Hz")):
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


def _check_compatible_units(from_unit, to_unit):
    source = get_unit(from_unit)
    target = get_unit(to_unit)
    if source.quantity != target.quantity:
        raise ValueError(
            "Incompatible units: %s (%s) and %s (%s)"
            % (source.symbol, source.quantity, target.symbol, target.quantity)
        )
    return source, target


def _to_internal(values, unit):
    return values * unit.factor_to_internal + unit.offset_to_internal


def _from_internal(values, unit):
    return (values - unit.offset_to_internal) / unit.factor_to_internal


def _convert(values, from_unit, to_unit):
    source, target = _check_compatible_units(from_unit, to_unit)
    return _from_internal(_to_internal(values, source), target)


def convert_value(value, from_unit, to_unit):
    """Convert a scalar value between compatible units."""
    return _convert(value, from_unit, to_unit)


def convert_array(values, from_unit, to_unit):
    """Convert array-like values between compatible units."""
    return _convert(np.asarray(values), from_unit, to_unit)


def frequency_to_angular_frequency(values):
    """Convert frequency in Hz to angular frequency in rad/s."""
    return np.asarray(values) * (2.0 * np.pi)


def angular_frequency_to_frequency(values):
    """Convert angular frequency in rad/s to frequency in Hz."""
    return np.asarray(values) / (2.0 * np.pi)


def convert_array_to_internal(values, unit_symbol, internal_unit_symbol=None):
    """Convert values to the registered internal unit, preserving unknown units."""
    if (unit_symbol, internal_unit_symbol) == ("Hz", "rad/s"):
        return frequency_to_angular_frequency(values)
    if (unit_symbol, internal_unit_symbol) == ("rad/s", "Hz"):
        return angular_frequency_to_frequency(values)
    try:
        unit = get_unit(unit_symbol)
    except ValueError:
        return np.asarray(values)
    return convert_array(values, unit.symbol, internal_unit_symbol or _INTERNAL_UNITS[unit.quantity])


def convert_array_from_internal(values, internal_unit_symbol, unit_symbol=None):
    """Convert values from an internal unit to a requested display unit."""
    if unit_symbol in (None, "", internal_unit_symbol):
        return np.asarray(values)
    return convert_array_to_internal(values, internal_unit_symbol, unit_symbol)
