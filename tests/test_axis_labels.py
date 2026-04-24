from RepTate.core.axis_labels import axis_label_from_column_specs
from RepTate.core.units import ColumnSpec


def test_axis_label_uses_matching_column_spec():
    specs = [
        ColumnSpec(name="time", display_unit="min", internal_unit="s", quantity="time")
    ]

    assert axis_label_from_column_specs("time", "min", specs) == "time [s]"


def test_axis_label_falls_back_without_column_specs():
    assert axis_label_from_column_specs("time", "min", []) == "time [min]"


def test_axis_label_falls_back_without_matching_column_spec():
    specs = [
        ColumnSpec(name="stress", display_unit="kPa", internal_unit="Pa", quantity="stress")
    ]

    assert axis_label_from_column_specs("time", "min", specs) == "time [min]"


def test_axis_label_omits_dimensionless_unit_from_column_spec():
    specs = [
        ColumnSpec(name="strain", display_unit="-", internal_unit="-", quantity="dimensionless")
    ]

    assert axis_label_from_column_specs("strain", "-", specs) == "strain"
