# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Tool and Experiments
# --------------------------------------------------------------------------------------------------------
#
# Authors:
#     Jorge Ramirez, jorge.ramirez@upm.es
#     Victor Boudara, victor.boudara@gmail.com
#
# Useful links:
#     http://blogs.upm.es/compsoftmatter/software/reptate/
#     https://github.com/jorge-ramirez-upm/RepTate
#     http://reptate.readthedocs.io
#
# --------------------------------------------------------------------------------------------------------
#
# Copyright (2018-2023): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
#
# This file is part of RepTate.
#
# RepTate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RepTate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RepTate.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------------------------
"""Module ToolEvaluate

Evaluate algebraic expressions in the current view
"""

import traceback
from typing import Any, ClassVar

from RepTate.core.expression_parser import evaluate_expression
from RepTate.core.Parameter import Parameter, ParameterType
from RepTate.core.typing import AnyArray, ApplicationLike, AxesLike, FileParameters, ToolResult
from RepTate.gui.QTool import QTool


class ToolEvaluate(QTool):
    """Create new abscissa and ordinate data by evaluating expressions.

    The expressions are functions of ``x`` and ``y``, where ``x`` and ``y`` are
    the abscissa and ordinate of the current view data.

    Standard algebraic expressions and mathematical functions are understood by
    the expression parser. File parameters can be referenced as ``[parameter]``.
    """

    toolname: ClassVar[str] = "Evaluate Expression"
    description: ClassVar[str] = "Evaluate Expression Tool"
    citations: ClassVar[list[str]] = []
    # html_help_file = 'http://reptate.readthedocs.io/manual/Tools/template.html'

    def __init__(self, name: str = "", parent_app: ApplicationLike | None = None) -> None:
        """**Constructor**"""
        super().__init__(name, parent_app)
        self.parameters["x"] = Parameter(
            name="x",
            value="x",
            description="Expression for abscissa",
            type=ParameterType.string,
        )
        self.parameters["y"] = Parameter(
            name="y",
            value="y",
            description="Expression for ordinate",
            type=ParameterType.string,
        )

        self.update_parameter_table()
        self.parent_application.update_all_ds_plots()

        # add widgets specific to the Tool here:

    def calculate(
        self,
        x: AnyArray,
        y: AnyArray,
        ax: AxesLike | None = None,
        color: Any = None,
        file_parameters: FileParameters | None = None,
    ) -> ToolResult:
        """Evaluate the x and y expressions for the current view data."""
        file_parameters = file_parameters or {}

        variables = {"x": x, "y": y}

        try:
            x2 = evaluate_expression(
                self.parameter_str("x"),
                variables,
                file_parameters,
            )
            y2 = evaluate_expression(
                self.parameter_str("y"),
                variables,
                file_parameters,
            )
            return x2, y2

        except Exception:
            self.Qprint("<b><font color=red>in ToolEvaluate.calculate():</font></b> %s" % traceback.format_exc())
            return x, y
