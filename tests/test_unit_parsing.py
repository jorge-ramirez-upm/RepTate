from RepTate.core.units import parse_column_label


def test_parse_square_bracket_unit():
    assert parse_column_label("time [s]") == ("time", "s", "time [s]")


def test_parse_parentheses_unit():
    assert parse_column_label("time (s)") == ("time", "s", "time (s)")


def test_parse_label_with_apostrophe():
    assert parse_column_label("G' [Pa]") == ("G'", "Pa", "G' [Pa]")


def test_parse_angular_frequency_unit():
    assert parse_column_label("omega [rad/s]") == (
        "omega",
        "rad/s",
        "omega [rad/s]",
    )


def test_parse_viscosity_unit():
    assert parse_column_label("eta [Pa.s]") == ("eta", "Pa.s", "eta [Pa.s]")


def test_parse_no_unit_present():
    assert parse_column_label("time") == ("time", None, "time")


def test_parse_parenthesized_label_without_space_as_no_unit():
    assert parse_column_label("W(logM)") == ("W(logM)", None, "W(logM)")


def test_parse_unknown_unit_without_validation():
    assert parse_column_label("length [furlong]") == (
        "length",
        "furlong",
        "length [furlong]",
    )
