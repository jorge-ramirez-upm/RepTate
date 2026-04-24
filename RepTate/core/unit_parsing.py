"""Helpers for parsing optional units from column labels."""

import re


_UNIT_LABEL_RE = re.compile(r"^\s*(?P<label>.+?)\s+(?:\[(?P<bracket>[^\]]+)\]|\((?P<paren>[^)]+)\))\s*$")


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
