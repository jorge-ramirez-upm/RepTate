import ast
import re
from types import CodeType
from typing import Any

import numpy as np


_SAFE_NUMPY_NAMES = [
    "sin",
    "cos",
    "tan",
    "arccos",
    "arcsin",
    "arctan",
    "arctan2",
    "deg2rad",
    "rad2deg",
    "sinh",
    "cosh",
    "tanh",
    "arcsinh",
    "arccosh",
    "arctanh",
    "around",
    "round",
    "rint",
    "floor",
    "ceil",
    "trunc",
    "exp",
    "log",
    "log10",
    "fabs",
    "mod",
    "power",
    "sqrt",
]

SAFE_MATH_NAMES: dict[str, Any] = {name: getattr(np, name) for name in _SAFE_NUMPY_NAMES}

SAFE_MATH_NAMES.update(
    {
        "pi": np.pi,
        "e": np.e,
        "abs": np.abs,
    }
)

_FILE_PARAM_RE = re.compile(r"\[(.*?)\]")

_ALLOWED_BINOPS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod)
_ALLOWED_UNARYOPS = (ast.UAdd, ast.USub)
_ALLOWED_CONSTANT_TYPES = (int, float)


def _replace_file_parameters(expression: str) -> tuple[str, dict[str, str]]:
    file_parameter_names: dict[str, str] = {}

    def replace_file_parameter(match: re.Match[str]) -> str:
        symbol = f"FP{len(file_parameter_names)}"
        file_parameter_names[symbol] = match.group(1)
        return symbol

    expression = _FILE_PARAM_RE.sub(replace_file_parameter, expression)
    return expression, file_parameter_names


def get_expression_names(expression: str) -> set[str]:
    """Return regular variable/function names used in an expression.

    File parameters written as ``[Mw]`` are not returned as ``Mw``. They are
    internally replaced before parsing.
    """
    expression, _ = _replace_file_parameters(expression)
    tree = ast.parse(expression, mode="eval")

    return {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}


def compile_expression(
    expression: str,
    variable_names: set[str],
) -> tuple[CodeType, dict[str, str]]:
    """Compile a validated algebraic expression.

    File parameters written as ``[param]`` are replaced internally by generated
    symbols and returned as ``{symbol: original_param_name}``.
    """
    expression, file_parameter_names = _replace_file_parameters(expression)
    tree = ast.parse(expression, mode="eval")

    valid_names = set(SAFE_MATH_NAMES) | variable_names | set(file_parameter_names)

    for node in ast.walk(tree):
        if isinstance(node, (ast.Expression, ast.Load)):
            continue

        if isinstance(node, ast.BinOp):
            if not isinstance(node.op, _ALLOWED_BINOPS):
                raise ValueError("Unsupported algebraic operator")
            continue

        if isinstance(node, ast.UnaryOp):
            if not isinstance(node.op, _ALLOWED_UNARYOPS):
                raise ValueError("Unsupported algebraic unary operator")
            continue

        if isinstance(node, _ALLOWED_BINOPS + _ALLOWED_UNARYOPS):
            continue

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only direct function calls are allowed")
            if node.func.id not in SAFE_MATH_NAMES:
                raise ValueError(f"Unknown function '{node.func.id}'")
            if node.keywords:
                raise ValueError("Function keyword arguments are not allowed")
            continue

        if isinstance(node, ast.Name):
            if node.id not in valid_names:
                raise ValueError(f"Unknown name '{node.id}'")
            continue

        if isinstance(node, ast.Constant):
            if not isinstance(node.value, _ALLOWED_CONSTANT_TYPES):
                raise ValueError("Only numeric constants are allowed")
            continue

        raise ValueError("Unsupported algebraic expression syntax")

    return compile(tree, "<algebraic expression>", "eval"), file_parameter_names


def evaluate_expression(
    expression: str,
    variables: dict[str, Any],
    file_parameters: dict[str, Any] | None = None,
) -> Any:
    """Evaluate a validated algebraic expression."""
    file_parameters = file_parameters or {}

    code, file_parameter_names = compile_expression(expression, set(variables))

    namespace = dict(SAFE_MATH_NAMES)
    namespace.update(variables)

    for symbol, parameter_name in file_parameter_names.items():
        namespace[symbol] = float(file_parameters.get(parameter_name, 0.0))

    return eval(code, {"__builtins__": {}}, namespace)
