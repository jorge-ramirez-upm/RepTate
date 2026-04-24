"""Axis label helpers that do not depend on the GUI."""


def default_axis_label(label, unit):
    return "%s [%s]" % (label, unit)


def axis_label_from_column_specs(label, unit, column_specs):
    """Use column metadata when a view label directly names a data column."""
    for spec in column_specs or []:
        if spec.name == label:
            return spec.axis_label()
    return default_axis_label(label, unit)
