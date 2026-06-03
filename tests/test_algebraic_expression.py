from __future__ import annotations

from collections import OrderedDict
from types import SimpleNamespace
from typing import Any, cast

import numpy as np
import numpy.testing as npt

from RepTate.core.DataTable import DataTable
from RepTate.core.Parameter import Parameter, ParameterType
from RepTate.theories.TheoryBasic import TheoryAlgebraicExpression


class _LoggerStub:
    def warning(self, message: str) -> None:
        pass

    def exception(self, message: str) -> None:
        pass


def _qprint_stub(msg: Any, end: str = "<br>") -> None:
    pass


def _algebraic_expression_theory(expression: str) -> tuple[Any, Any]:
    ft = DataTable()
    ft.num_rows = 3
    ft.num_columns = 2
    ft.data = np.array([[1.0, 0.0], [2.0, 0.0], [4.0, 0.0]])

    tt = DataTable()
    file = SimpleNamespace(
        data_table=ft,
        file_name_short="sample",
        file_parameters={"scale": "2.5"},
    )

    theory = TheoryAlgebraicExpression.__new__(TheoryAlgebraicExpression)
    dynamic_theory = cast(Any, theory)
    theory.parameters = OrderedDict(
        [
            ("n", Parameter("n", 2, "number of parameters", ParameterType.integer)),
            ("expression", Parameter("expression", expression, "expression", ParameterType.string)),
            ("A0", Parameter("A0", 1.0, "parameter 0", ParameterType.real)),
            ("A1", Parameter("A1", 2.0, "parameter 1", ParameterType.real)),
        ]
    )
    theory.tables = {"sample": tt}
    theory.safe_dict = {"sin": np.sin}
    dynamic_theory.logger = _LoggerStub()
    dynamic_theory.Qprint = _qprint_stub
    return theory, file


def test_algebraic_expression_accepts_numpy_functions_and_file_parameters() -> None:
    theory, file = _algebraic_expression_theory("A0 + A1*sin(x) + [scale]")

    theory.algebraicexpression(file)

    expected = 1.0 + 2.0 * np.sin(file.data_table.data[:, 0]) + 2.5
    npt.assert_allclose(theory.tables["sample"].data[:, 1], expected)


def test_algebraic_expression_rejects_attribute_access() -> None:
    theory, file = _algebraic_expression_theory("A0 + A1*x.__class__")

    theory.algebraicexpression(file)

    npt.assert_allclose(theory.tables["sample"].data[:, 1], np.zeros(3))


def test_algebraic_expression_rejects_conditional_expression() -> None:
    theory, file = _algebraic_expression_theory("A0 + A1*(x if 1 else x)")

    theory.algebraicexpression(file)

    npt.assert_allclose(theory.tables["sample"].data[:, 1], np.zeros(3))
