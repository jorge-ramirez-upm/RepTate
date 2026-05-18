import ast
import warnings
from pathlib import Path

from RepTate.core.units import get_unit, units_are_compatible


THEORY_DIR = Path(__file__).resolve().parents[1] / "RepTate" / "theories"
CANONICAL_UNITS = {
    "time": "s",
    "stress": "Pa",
    "viscosity": "Pa.s",
    "molar_mass": "kg/mol",
}


def _literal_keyword(call: ast.Call, name: str) -> str | None:
    for keyword in call.keywords:
        if keyword.arg == name and isinstance(keyword.value, ast.Constant):
            value = keyword.value.value
            if isinstance(value, str):
                return value
    return None


def test_theory_parameter_unit_metadata_uses_registered_compatible_units():
    checked = []
    for path in THEORY_DIR.glob("Theory*.py"):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name) or node.func.id != "Parameter":
                continue
            quantity = _literal_keyword(node, "quantity")
            internal_unit = _literal_keyword(node, "internal_unit")
            display_unit = _literal_keyword(node, "display_unit")
            if not any((quantity, internal_unit, display_unit)):
                continue

            assert quantity, "%s has unit metadata without quantity" % path.name
            assert internal_unit, "%s has unit metadata without internal_unit" % path.name
            assert display_unit, "%s has unit metadata without display_unit" % path.name
            assert get_unit(internal_unit).quantity == quantity
            assert get_unit(display_unit).quantity == quantity
            assert units_are_compatible(display_unit, internal_unit)
            if quantity in CANONICAL_UNITS:
                assert internal_unit == CANONICAL_UNITS[quantity]
            checked.append((path.name, quantity, internal_unit, display_unit))

    assert checked
