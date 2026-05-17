# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
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
# Copyright (2017-2026): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module TheoryBasic

Module that defines the basic theories that should be available for all Applications.

"""

from numpy import (
    sin,
    cos,
    tan,
    arccos,
    arcsin,
    arctan,
    arctan2,
    deg2rad,
    rad2deg,
    sinh,
    cosh,
    tanh,
    arcsinh,
    arccosh,
    arctanh,
    around,
    rint,
    floor,
    ceil,
    trunc,
    exp,
    log,
    log10,
    fabs,
    mod,
    e,
    pi,
    power,
    sqrt,
)
import numpy as np
import re
from typing import Any, cast

from RepTate.core.DataTable import DataTable
from RepTate.core.typing import AxesArray, FileLike
from RepTate.gui.QTheory import QTheory
from RepTate.core.Parameter import Parameter, ParameterType, OptType
from PySide6.QtWidgets import QToolBar, QSpinBox, QComboBox
from PySide6.QtCore import QSize

r"""
             _                             _       _ 
 _ __   ___ | |_   _ _ __   ___  _ __ ___ (_) __ _| |
| '_ \ / _ \| | | | | '_ \ / _ \| '_ ` _ \| |/ _` | |
| |_) | (_) | | |_| | | | | (_) | | | | | | | (_| | |
| .__/ \___/|_|\__, |_| |_|\___/|_| |_| |_|_|\__,_|_|
|_|            |___/                                 
"""


class TheoryPolynomial(QTheory):
    """Fit a polynomial of degree :math:`n` to the data

    * **Function**
        .. math::
            y(x) = \\sum_{i=0}^n A_i x^i

    * **Parameters**
       - :math:`n`: degree of the polynomial function.
       - :math:`A_i`: polynomial coefficeints.
    """

    thname: str = "Polynomial"
    description: str = "Fit a polynomial of degree n"
    html_help_file: str = "http://reptate.readthedocs.io/manual/All_Theories/basic_theories.html#polynomial"
    single_file: bool = True

    def __init__(self, name: str = "", parent_dataset: Any = None, ax: AxesArray | None = None) -> None:
        """**Constructor**

        Keyword Arguments:
            - name {str} -- Name of the theory (default: {""})
            - parent_dataset {DataSet} -- DataSet that contains this theory (default: {None})
            - ax {Axes array} -- Matplotlib axes where the theory will plot the data (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.MAX_DEGREE: int = 10
        self.function = self.polynomial
        self.parameters["n"] = Parameter(
            name="n", value=1, description="Degree of Polynomial", type=ParameterType.integer, opt_type=OptType.const, display_flag=False
        )
        n: Any = self.parameters["n"].value
        for i in range(n + 1):
            self.parameters["A%d" % i] = Parameter("A%d" % i, 1.0, "Coefficient order %d" % i, ParameterType.real, opt_type=OptType.opt)
        self.Qprint("%s: A0 + A1*x + A2*x^2 + ..." % self.thname)

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, self.MAX_DEGREE)  # min and max number of modes
        self.spinbox.setPrefix("degree ")
        self.spinbox.setValue(int(self.parameters["n"].value))  # initial value
        tb.addWidget(self.spinbox)
        self.thToolsLayout.insertWidget(0, tb)
        self.spinbox.valueChanged.connect(self.handle_spinboxValueChanged)

    def handle_spinboxValueChanged(self, value: Any) -> None:
        """Handle a change of the parameter 'nmode'"""
        self.set_param_value("n", value)

    def set_param_value(self, name: str, value: Any) -> tuple[str, bool]:
        """Change a parameter value, in particular *n*"""
        if name == "n":
            nold: Any = self.parameters["n"].value
            Aold = np.zeros(nold + 1)
            for i in range(nold + 1):
                Aold[i] = self.parameters["A%d" % i].value
                del self.parameters["A%d" % i]

            nnew: Any = value
            message, success = super().set_param_value("n", nnew)
            for i in range(nnew + 1):
                if i <= nold:
                    Aval = Aold[i]
                else:
                    Aval = 1.0
                self.parameters["A%d" % i] = Parameter(
                    "A%d" % i, Aval, "Coefficient degree %d" % i, ParameterType.real, opt_type=OptType.opt
                )
        else:
            message, success = super().set_param_value(name, value)

        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()
        self.update_parameter_table()
        return message, success

    def polynomial(self, f: FileLike | None = None) -> None:
        """Actual polynomial function.

        .. math::
            y(x) = \\sum_{i=0}^n A_i x^i
        """
        file = cast(FileLike, f)
        ft: DataTable = file.data_table
        tt: DataTable = self.tables[file.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        n: Any = self.parameters["n"].value
        for i in range(n + 1):
            a = self.parameters["A%d" % i].value
            for j in range(1, tt.num_columns):
                tt.data[:, j] += a * tt.data[:, 0] ** i


r"""
 _ __   _____      _____ _ __  | | __ ___      __
| '_ \ / _ \ \ /\ / / _ \ '__| | |/ _` \ \ /\ / /
| |_) | (_) \ V  V /  __/ |    | | (_| |\ V  V / 
| .__/ \___/ \_/\_/ \___|_|    |_|\__,_| \_/\_/  
|_|                                              
"""


class TheoryPowerLaw(QTheory):
    """Fit a power law to the data

    * **Function**
        .. math::
            y(x) = a x^b

    * **Parameters**
       - :math:`a`: prefactor.
       - :math:`b`: exponent.
    """

    thname: str = "Power Law"
    description: str = "Fit Power Law"
    html_help_file: str = "http://reptate.readthedocs.io/manual/All_Theories/basic_theories.html#power-law"
    single_file: bool = True

    def __init__(self, name: str = "", parent_dataset: Any = None, ax: AxesArray | None = None) -> None:
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)
        self.function = self.powerlaw
        self.parameters["a"] = Parameter("a", 1.0, "Prefactor", ParameterType.real, opt_type=OptType.opt)
        self.parameters["b"] = Parameter("b", 1.0, "Exponent", ParameterType.real, opt_type=OptType.opt)
        self.Qprint("%s: a*x^b" % self.thname)

    def powerlaw(self, f: FileLike | None = None) -> None:
        """Actual function

        * **Function**
            .. math::
                y(x) = a x^b
        """
        file = cast(FileLike, f)
        ft: DataTable = file.data_table
        tt: DataTable = self.tables[file.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        for j in range(1, tt.num_columns):
            a: Any = self.parameters["a"].value
            b: Any = self.parameters["b"].value
            tt.data[:, j] = a * tt.data[:, 0] ** b


r"""
                                        _   _       _ 
  _____  ___ __   ___  _ __   ___ _ __ | |_(_) __ _| |
 / _ \ \/ / '_ \ / _ \| '_ \ / _ \ '_ \| __| |/ _` | |
|  __/>  <| |_) | (_) | | | |  __/ | | | |_| | (_| | |
 \___/_/\_\ .__/ \___/|_| |_|\___|_| |_|\__|_|\__,_|_|
          |_|                                         
"""


class TheoryExponential(QTheory):
    """Fit a single exponential decay to the data

    * **Function**
        .. math::
            y(x) = a \\exp(-x/T)

    * **Parameters**
       - :math:`a`: prefactor.
       - :math:`T`: exponential "time" constant.

    """

    thname: str = "Exponential"
    description: str = "Fit Exponential"
    html_help_file: str = "http://reptate.readthedocs.io/manual/All_Theories/basic_theories.html#exponential"
    single_file: bool = True

    def __init__(self, name: str = "", parent_dataset: Any = None, ax: AxesArray | None = None) -> None:
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)
        self.function = self.exponential
        self.parameters["a"] = Parameter("a", 1.0, "Prefactor", ParameterType.real, opt_type=OptType.opt)
        self.parameters["T"] = Parameter("T", 1.0, "Exponential time constant", ParameterType.real, opt_type=OptType.opt)
        self.Qprint("%s: a*exp(-x/T)" % self.thname)

    def exponential(self, f: FileLike | None = None) -> None:
        """**Function** :math:`y(x) = a \\exp(-x/T)`"""
        file = cast(FileLike, f)
        ft: DataTable = file.data_table
        tt: DataTable = self.tables[file.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        for j in range(1, tt.num_columns):
            tt.data[:, j] = self.parameters["a"].value * np.exp(-tt.data[:, 0] / self.parameters["T"].value)


r"""
 ____                                           _   _       _     
|___ \    _____  ___ __   ___  _ __   ___ _ __ | |_(_) __ _| |___ 
  __) |  / _ \ \/ / '_ \ / _ \| '_ \ / _ \ '_ \| __| |/ _` | / __|
 / __/  |  __/>  <| |_) | (_) | | | |  __/ | | | |_| | (_| | \__ \
|_____|  \___/_/\_\ .__/ \___/|_| |_|\___|_| |_|\__|_|\__,_|_|___/
                  |_|                                             
"""


class TheoryTwoExponentials(QTheory):
    """Fit **two** single exponential decay to the data

    * **Function**
        .. math::
            y(x) = a_1 \\exp(x/T_1) + a_2 \\exp(-x/T_2)

    * **Parameters**
       - :math:`a_1`, :math:`a_2`: prefactors.
       - :math:`T_1`, :math:`T_2`: exponential "time" constants.
    """

    thname: str = "Two Exponentials"
    description: str = "Fit two exponentials"
    html_help_file: str = "http://reptate.readthedocs.io/manual/All_Theories/basic_theories.html#double-exponential"
    single_file: bool = True

    def __init__(self, name: str = "", parent_dataset: Any = None, ax: AxesArray | None = None) -> None:
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)
        self.function = self.two_exponentials
        self.parameters["a1"] = Parameter("a1", 0.9, "Prefactor 1", ParameterType.real, opt_type=OptType.opt)
        self.parameters["T1"] = Parameter("T1", 1.0, "Exponential time constant 1", ParameterType.real, opt_type=OptType.opt)
        self.parameters["a2"] = Parameter("a2", 0.1, "Prefactor 2", ParameterType.real, opt_type=OptType.opt)
        self.parameters["T2"] = Parameter("T2", 10.0, "Exponential time constant 2", ParameterType.real, opt_type=OptType.opt)
        self.Qprint("%s: a1*exp(-x/T1) + a2*exp(-x/T2)" % self.thname)

    def two_exponentials(self, f: FileLike | None = None) -> None:
        """Actual function

        * **Function**
            .. math::
                y(x) = a_1 \\exp(x/T_1) + a_2 \\exp(-x/T_2)
        """
        file = cast(FileLike, f)
        ft: DataTable = file.data_table
        tt: DataTable = self.tables[file.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        a1: Any = self.parameters["a1"].value
        a2: Any = self.parameters["a2"].value
        T1: Any = self.parameters["T1"].value
        T2: Any = self.parameters["T2"].value
        for j in range(1, tt.num_columns):
            tt.data[:, j] = a1 * np.exp(-tt.data[:, 0] / T1) + a2 * np.exp(-tt.data[:, 0] / T2)


r"""
       _            _               _      
  __ _| | __ _  ___| |__  _ __ __ _(_) ___ 
 / _` | |/ _` |/ _ \ '_ \| '__/ _` | |/ __|
| (_| | | (_| |  __/ |_) | | | (_| | | (__ 
 \__,_|_|\__, |\___|_.__/|_|  \__,_|_|\___|
         |___/                             
                                   _             
  _____  ___ __  _ __ ___  ___ ___(_) ___  _ __  
 / _ \ \/ / '_ \| '__/ _ \/ __/ __| |/ _ \| '_ \ 
|  __/>  <| |_) | | |  __/\__ \__ \ | (_) | | | |
 \___/_/\_\ .__/|_|  \___||___/___/_|\___/|_| |_|
          |_|                                    
"""


class TheoryAlgebraicExpression(QTheory):
    """Fit a user algebraic expression with :math:`n` parameters.

    The expression can contain any of the following mathematical functions: sin, cos, tan, arccos, arcsin, arctan, arctan2, deg2rad, rad2deg, sinh, cosh, tanh, arcsinh, arccosh, arctanh, around, round, rint, floor, ceil,trunc, exp, log, log10, fabs, mod, e, pi, power, sqrt

    It is the responsability of the user to input functions that make mathematical sense.

    * **Function**
        .. math::
            y(x) = f({A_i}, x, F_{params})

    * **Parameters**
       - :math:`n`: number of parameters.
       - :math:`A_i`: coefficeints of the algebraic expression
    """

    thname: str = "Algebraic Expression"
    description: str = "Fit an algebraic expression with n parameters"
    html_help_file: str = "http://reptate.readthedocs.io/manual/All_Theories/basic_theories.html#algebraic-expression"
    single_file: bool = False

    def __init__(self, name: str = "", parent_dataset: Any = None, ax: AxesArray | None = None) -> None:
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)
        self.MAX_DEGREE: int = 10
        self.function = self.algebraicexpression
        self.parameters["n"] = Parameter(
            name="n", value=2, description="Number of Parameters", type=ParameterType.integer, opt_type=OptType.const, display_flag=False
        )
        self.parameters["expression"] = Parameter(
            name="expression",
            value="A0+A1*x",
            description="Algebraic Expression",
            type=ParameterType.string,
            opt_type=OptType.const,
            display_flag=False,
        )
        n: Any = self.parameters["n"].value
        for i in range(n):
            self.parameters["A%d" % i] = Parameter("A%d" % i, 1.0, "Parameter %d" % i, ParameterType.real, opt_type=OptType.opt)

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
        self.safe_dict: dict[str, Any] = {}
        for k in safe_list:
            self.safe_dict[k] = globals().get(k, None)

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, self.MAX_DEGREE)  # min and max number of modes
        self.spinbox.setToolTip("Number of parameters")
        self.spinbox.setValue(int(self.parameters["n"].value))  # initial value
        tb.addWidget(self.spinbox)
        self.expressionCB = QComboBox()
        self.expressionCB.setToolTip("Algebraic expression")
        self.expressionCB.addItem("A0+A1*x")
        self.expressionCB.addItem("A0*sin(A1*x)")
        self.expressionCB.addItem("A0*sin(A1*x+A2)")
        self.expressionCB.setEditable(True)
        self.expressionCB.setMinimumWidth(self.parent_dataset.width() - 75)
        tb.addWidget(self.expressionCB)

        self.thToolsLayout.insertWidget(0, tb)
        self.spinbox.valueChanged.connect(self.handle_spinboxValueChanged)
        self.expressionCB.currentIndexChanged.connect(self.handle_expressionChanged)

    def handle_spinboxValueChanged(self, value: Any) -> None:
        """Handle a change of the parameter 'n'"""
        self.set_param_value("n", value)

    def handle_expressionChanged(self, item: int) -> None:
        """Handle a change in the algebraic expression"""
        self.set_param_value("expression", self.expressionCB.itemText(item))

    def set_param_value(self, name: str, value: Any) -> tuple[str, bool]:
        """Change a parameter value, in particular *n*"""
        if name == "n":
            nold: Any = self.parameters["n"].value
            Aold = np.zeros(nold)
            for i in range(nold):
                Aold[i] = self.parameters["A%d" % i].value
                del self.parameters["A%d" % i]

            nnew: Any = value
            message, success = super().set_param_value("n", nnew)
            for i in range(nnew):
                if i < nold:
                    Aval = Aold[i]
                else:
                    Aval = 1.0
                self.parameters["A%d" % i] = Parameter("A%d" % i, Aval, "Parameter %d" % i, ParameterType.real, opt_type=OptType.opt)
        else:
            message, success = super().set_param_value(name, value)

        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()
        self.update_parameter_table()
        return message, success

    def algebraicexpression(self, f: FileLike | None = None) -> None:
        """Actual function.

        * **Function**
            .. math::
                y(x) = f({A_i}, x)
        """
        file = cast(FileLike, f)
        ft: DataTable = file.data_table
        tt: DataTable = self.tables[file.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        expression: Any = self.parameters["expression"].value
        params = set(re.findall(r"A\d{1,2}", expression))
        nparams = len(params)
        maxparamindex = -1
        for p in params:
            paramindex = int(p.split("A")[1])
            if paramindex > maxparamindex:
                maxparamindex = paramindex
        n: Any = self.parameters["n"].value
        if (maxparamindex != n - 1) or (nparams != n):
            self.logger.warning("Wrong expression or number of parameters. Review your theory")
            self.Qprint("<b><font color=red>Wrong expression or number of parameters</font></b>. Review your theory")
        else:
            # Find FILE PARAMETERS IN THE EXPRESSION
            fparams = re.findall(r"\[(.*?)\]", expression)
            for fp in fparams:
                if fp in file.file_parameters:
                    self.safe_dict[fp] = float(file.file_parameters[fp])
                else:
                    self.logger.warning("File parameter not found. Review your theory")
                    self.Qprint("<b><font color=red>File parameter not found</font></b>. Review your theory")
                    self.safe_dict[fp] = 0.0
            expression = expression.replace("[", "").replace("]", "")

            self.safe_dict["x"] = tt.data[:, 0]
            for i in range(n):
                self.safe_dict["A%d" % i] = self.parameters["A%d" % i].value

            try:
                y = eval(expression, {"__builtins__": None}, self.safe_dict)
                for j in range(1, tt.num_columns):
                    tt.data[:, j] = y
            except NameError as e:
                self.Qprint("<b>Error in algebraic expression <b>")
                self.logger.exception("Error in Algebraic Expression")
            except TypeError as e:
                self.Qprint("<b>Error in algebraic expression <b>")
                self.logger.exception("Error in Algebraic Expression")
            except Exception as e:
                self.Qprint("<b>Error in algebraic expression <b>")
                self.logger.exception("Error in Algebraic Expression")
                # print (e.__class__, ":", e)

    def do_error(self, line: str) -> None:
        super().do_error(line)
        self.Qprint("%s: <b>%s</b>" % (self.thname, self.parameters["expression"].value))
