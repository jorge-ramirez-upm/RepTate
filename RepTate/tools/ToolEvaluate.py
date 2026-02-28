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
from numpy import *
import re
from RepTate.core.Parameter import Parameter, ParameterType
from RepTate.gui.QTool import QTool


class ToolEvaluate(QTool):
    """Create new abcissa and ordinate data by evaluating an expression as a function of x and y (the abcissa and ordinate of the current view data). Standard algebraic expressions and mathematical functions (``sin, cos, tan, arccos, arcsin, arctan, arctan2, deg2rad, rad2deg, sinh, cosh, tanh, arcsinh, arccosh, arctanh, around, round_, rint, floor, ceil, trunc, exp, log, log10, fabs, mod, e, pi, power, sqrt``) are understood by the expression parser."""

    toolname = "Eval Exp"
    description = "Evaluate Expression Tool"
    citations = []
    # html_help_file = 'http://reptate.readthedocs.io/manual/Tools/template.html'

    def __init__(self, name="", parent_app=None):
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

        safe_list = [
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
            "round_",
            "rint",
            "floor",
            "ceil",
            "trunc",
            "exp",
            "log",
            "log10",
            "fabs",
            "mod",
            "e",
            "pi",
            "power",
            "sqrt",
        ]
        self.safe_dict = {}
        for k in safe_list:
            self.safe_dict[k] = globals().get(k, None)

        self.update_parameter_table()
        self.parent_application.update_all_ds_plots()

        # add widgets specific to the Tool here:


    def calculate(self, x, y, ax=None, color=None, file_parameters=[]):
        """Evaluate function that returns the square of the y, according to the view"""
        xexpr = self.parameters["x"].value
        yexpr = self.parameters["y"].value
        self.safe_dict["x"] = x
        self.safe_dict["y"] = y

        # Find FILE PARAMETERS IN THE EXPRESSION
        fparams = re.findall(r"\[(.*?)\]", xexpr)
        for fp in fparams:
            if fp in file_parameters:
                self.safe_dict[fp] = float(file_parameters[fp])
            else:
                self.logger.warning(
                    "File parameter not found. Review your Tool expression for x"
                )
                self.Qprint(
                    "<b><font color=red>File parameter not found</font></b>. Review your Tool expression for x"
                )
                self.safe_dict[fp] = 0.0
        xexpr = xexpr.replace("[", "").replace("]", "")

        fparams = re.findall(r"\[(.*?)\]", yexpr)
        for fp in fparams:
            if fp in file_parameters:
                self.safe_dict[fp] = float(file_parameters[fp])
            else:
                self.logger.warning(
                    "File parameter not found. Review your Tool expression for y"
                )
                self.Qprint(
                    "<b><font color=red>File parameter not found</font></b>. Review your Tool expression for y"
                )
                self.safe_dict[fp] = 0.0
        yexpr = yexpr.replace("[", "").replace("]", "")

        try:
            x2 = eval(xexpr, {"__builtins__": None}, self.safe_dict)
            # x2 = eval(xexpr, var)
            y2 = eval(yexpr, {"__builtins__": None}, self.safe_dict)
            # y2 = eval(yexpr, var)
            return x2, y2
        except Exception as e:
            self.Qprint("in ToolEvaluate.calculate(): %s" % traceback.format_exc())
            return x, y

