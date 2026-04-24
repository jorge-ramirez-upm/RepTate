import pytest

from RepTate.core.File import File, FileParameterSpec


def test_file_parameter_without_units_is_unchanged():
    file = File("sample.tts")

    file.set_file_parameter("chem", "PI")

    assert file.file_parameters["chem"] == "PI"
    assert file.file_parameter_value_to_display("chem") == "PI"
    assert file.file_parameter_value_from_display("chem", "PE") == "PE"
    assert file.file_parameter_label("chem") == "chem"


def test_temperature_file_parameter_is_stored_in_kelvin_and_displayed_in_celsius():
    file = File("sample.tts")
    spec = FileParameterSpec(
        name="T",
        quantity="temperature",
        internal_unit="K",
        display_unit="ºC",
    )

    file.set_file_parameter("T", 25.0, spec=spec)

    assert file.file_parameters["T"] == pytest.approx(298.15)
    assert file.file_parameter_value_to_display("T") == pytest.approx(25.0)
    assert file.file_parameter_value_from_display("T", 0.0) == pytest.approx(273.15)
    assert file.file_parameter_label("T") == "T [ºC]"


def test_pressure_file_parameter_is_stored_in_pascal_and_displayed_in_atm():
    file = File("sample.creep")
    spec = FileParameterSpec(
        name="stress",
        quantity="stress",
        internal_unit="Pa",
        display_unit="atm",
    )

    file.set_file_parameter("stress", 1.0, spec=spec)

    assert file.file_parameters["stress"] == pytest.approx(101325.0)
    assert file.file_parameter_value_to_display("stress") == pytest.approx(1.0)
    assert file.file_parameter_label("stress") == "stress [atm]"


def test_incompatible_file_parameter_metadata_raises_value_error():
    with pytest.raises(ValueError, match="internal unit"):
        FileParameterSpec(
            name="T",
            quantity="temperature",
            internal_unit="Pa",
            display_unit="ºC",
        )

    with pytest.raises(ValueError, match="display unit"):
        FileParameterSpec(
            name="stress",
            quantity="stress",
            internal_unit="Pa",
            display_unit="ºC",
        )
