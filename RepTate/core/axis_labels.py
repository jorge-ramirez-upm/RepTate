"""Axis label helpers that do not depend on the GUI."""

from collections.abc import Iterable
from typing import Protocol


class AxisLabelSpec(Protocol):
    name: str

    def axis_label(self) -> str:
        ...


def default_axis_label(label: str, unit: str) -> str:
    return "%s [%s]" % (label, unit)


def axis_label_from_column_specs(
    label: str, unit: str, column_specs: Iterable[AxisLabelSpec] | None
) -> str:
    """Use column metadata when a view label directly names a data column."""
    for spec in column_specs or []:
        if spec.name == label:
            return spec.axis_label()
    return default_axis_label(label, unit)
