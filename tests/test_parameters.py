from RepTate.core.Parameter import OptType, Parameter, ParameterType


def test_parameter_unit_metadata_defaults_do_not_change_value():
    parameter = Parameter("tau_e", 2e-6, "Rouse time", ParameterType.real)

    assert parameter.value == 2e-6
    assert parameter.quantity == ""
    assert parameter.internal_unit == ""
    assert parameter.display_unit == ""
    assert parameter.display_label() == "tau_e"


def test_parameter_unit_metadata_is_stored_and_copied():
    source = Parameter(
        "tau_e",
        2e-6,
        "Rouse time",
        ParameterType.real,
        opt_type=OptType.opt,
        min_value=1e-7,
        max_value=1e2,
        quantity="time",
        internal_unit="s",
        display_unit="s",
    )
    target = Parameter()

    target.copy(source)

    assert target.value == 2e-6
    assert target.quantity == "time"
    assert target.internal_unit == "s"
    assert target.display_unit == "s"
    assert target.display_label() == "tau_e [s]"


def test_parameter_display_value_converts_from_internal_unit():
    parameter = Parameter(
        "tau_e",
        120.0,
        "Rouse time",
        ParameterType.real,
        quantity="time",
        internal_unit="s",
        display_unit="min",
    )

    assert parameter.value == 120.0
    assert parameter.display_value() == 2.0
    assert parameter.value_from_display(2.0) == 120.0


def test_parameter_display_value_supports_small_time_units():
    parameter = Parameter(
        "tau_e",
        2e-6,
        "Rouse time",
        ParameterType.real,
        quantity="time",
        internal_unit="s",
        display_unit="μs",
    )

    assert parameter.display_value() == 2.0
    assert parameter.value_from_display(500.0) == 5e-4
