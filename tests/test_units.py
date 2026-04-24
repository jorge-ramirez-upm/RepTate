import numpy as np
import pytest

from RepTate.core.units import (
    angular_frequency_to_frequency,
    available_units,
    convert_array,
    convert_value,
    frequency_to_angular_frequency,
    get_unit,
    units_are_compatible,
)


def test_time_conversions():
    assert convert_value(1, "s", "ms") == pytest.approx(1000)
    assert convert_value(1, "ms", "μs") == pytest.approx(1000)
    assert convert_value(1, "μs", "ns") == pytest.approx(1000)
    assert convert_value(120, "s", "min") == pytest.approx(2)
    assert convert_value(2, "h", "min") == pytest.approx(120)
    assert convert_value(0.5, "h", "s") == pytest.approx(1800)


def test_stress_conversions():
    assert convert_value(1000, "Pa", "kPa") == pytest.approx(1)
    assert convert_value(2, "MPa", "Pa") == pytest.approx(2_000_000)
    assert convert_value(1, "bar", "Pa") == pytest.approx(100_000)
    assert convert_value(1, "atm", "Pa") == pytest.approx(101_325)
    assert convert_value(1, "MPa", "bar") == pytest.approx(10)


def test_viscosity_conversions():
    assert convert_value(1000, "Pa.s", "kPa.s") == pytest.approx(1)
    assert convert_value(2, "kPa.s", "Pa.s") == pytest.approx(2000)


def test_molar_mass_conversions():
    assert convert_value(1, "kg/mol", "g/mol") == pytest.approx(1000)
    assert convert_value(1000, "g/mol", "kg/mol") == pytest.approx(1)
    assert get_unit("kg/mol").factor_to_internal == pytest.approx(1)


def test_temperature_conversions_are_affine():
    assert convert_value(273.15, "K", "ºC") == pytest.approx(0)
    assert convert_value(0, "ºC", "K") == pytest.approx(273.15)
    assert convert_value(convert_value(300, "K", "ºC"), "ºC", "K") == pytest.approx(300)


def test_celsius_degree_alias():
    assert convert_value(25, "°C", "K") == pytest.approx(298.15)
    assert convert_value(298.15, "K", "°C") == pytest.approx(25)


def test_array_conversion():
    values = np.array([1, 2, 3])
    converted = convert_array(values, "min", "s")
    np.testing.assert_allclose(converted, np.array([60, 120, 180]))
    np.testing.assert_allclose(convert_array([1, 2, 3], "s", "min"), [1 / 60, 2 / 60, 3 / 60])
    np.testing.assert_allclose(convert_array([0, 25], "ºC", "K"), [273.15, 298.15])


def test_units_are_compatible():
    assert units_are_compatible("Pa", "bar")
    assert units_are_compatible("K", "ºC")
    assert not units_are_compatible("Hz", "rad/s")


def test_frequency_angular_frequency_helpers_are_explicit():
    assert frequency_to_angular_frequency(1) == pytest.approx(2 * np.pi)
    assert angular_frequency_to_frequency(2 * np.pi) == pytest.approx(1)
    np.testing.assert_allclose(
        frequency_to_angular_frequency([1, 2]),
        [2 * np.pi, 4 * np.pi],
    )


def test_available_units():
    symbols = {unit.symbol for unit in available_units("time")}
    assert {"ns", "μs", "ms", "s", "min", "h"} <= symbols


def test_available_units_include_display_choices_for_parameter_quantities():
    stress = {unit.symbol for unit in available_units("stress")}
    viscosity = {unit.symbol for unit in available_units("viscosity")}
    molar_mass = {unit.symbol for unit in available_units("molar_mass")}

    assert {"Pa", "kPa", "MPa", "bar", "atm"} <= stress
    assert {"Pa.s", "kPa.s"} <= viscosity
    assert {"kg/mol", "g/mol"} <= molar_mass


def test_get_unit():
    unit = get_unit("Pa")
    assert unit.symbol == "Pa"
    assert unit.quantity == "stress"
    assert unit.label == "Pa"


def test_incompatible_conversion_raises_value_error():
    with pytest.raises(ValueError, match="Incompatible units"):
        convert_value(1, "Hz", "rad/s")


def test_unknown_unit_raises_value_error():
    with pytest.raises(ValueError, match="Unknown unit"):
        convert_value(1, "furlong", "s")
