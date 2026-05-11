import pytest

from RepTate.core.Parameter import Parameter
from RepTate.tools import polymer_data
from RepTate.tools.ToolMaterialsDatabase import (
    get_single_parameter,
    materials_database,
)


def test_legacy_material_values_are_canonicalized_to_internal_units():
    material = polymer_data.polymer(
        name="PI",
        tau_e=1.0e-5,
        Ge=5.0e5,
        B2=114.3,
        Me=4.8,
        rho0=0.928,
        Te=25.0,
        M0=68.0,
        MK=140.5,
    )

    polymer_data.canonicalize_material(material)

    assert material.unit_system == polymer_data.MATERIAL_DATABASE_UNIT_SYSTEM
    assert material.data["tau_e"] == pytest.approx(1.0e-5)
    assert material.data["Ge"] == pytest.approx(5.0e5)
    assert material.data["B2"] == pytest.approx(114.3)
    assert material.data["Me"] == pytest.approx(4.8)
    assert material.data["rho0"] == pytest.approx(928.0)
    assert material.data["Te"] == pytest.approx(25.0)
    assert material.data["M0"] == pytest.approx(0.068)
    assert material.data["MK"] == pytest.approx(0.1405)


def test_shipped_material_database_is_loaded_in_internal_units():
    pi = materials_database["PI"]

    assert pi.unit_system == polymer_data.MATERIAL_DATABASE_UNIT_SYSTEM
    assert pi.data["Me"] == pytest.approx(4.8158)
    assert pi.data["B2"] == pytest.approx(114.3)
    assert pi.data["rho0"] == pytest.approx(928.0)
    assert pi.data["Te"] == pytest.approx(25.0)
    assert pi.data["M0"] == pytest.approx(0.068)
    assert pi.data["MK"] == pytest.approx(0.1405)


def test_material_database_values_convert_to_target_parameter_units():
    target = Parameter(
        "MK",
        0.0,
        "Kuhn molar mass",
        quantity="molar_mass",
        internal_unit="g/mol",
        display_unit="g/mol",
    )

    converted = polymer_data.convert_database_value_to_parameter("MK", 0.1405, target)

    assert converted == pytest.approx(140.5)


def test_get_single_parameter_returns_shifted_internal_values():
    rho, success = get_single_parameter("PI", "rho0", {"T": 0}, 1)

    assert success
    assert rho == pytest.approx(928.0)
