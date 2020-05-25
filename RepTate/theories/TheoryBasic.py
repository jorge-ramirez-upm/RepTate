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
# Copyright (2017-2020): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
from numpy import *
import numpy as np
import re
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Theory import Theory
from RepTate.gui.QTheory import QTheory
from RepTate.core.Parameter import Parameter, ParameterType, OptType
from PyQt5.QtWidgets import QToolBar, QSpinBox, QComboBox
from PyQt5.QtCore import QSize

"""
             _                             _       _ 
 _ __   ___ | |_   _ _ __   ___  _ __ ___ (_) __ _| |
| '_ \ / _ \| | | | | '_ \ / _ \| '_ ` _ \| |/ _` | |
| |_) | (_) | | |_| | | | | (_) | | | | | | | (_| | |
| .__/ \___/|_|\__, |_| |_|\___/|_| |_| |_|_|\__,_|_|
|_|            |___/                                 
"""

class TheoryPolynomial(CmdBase):
    """Fit a polynomial of degree :math:`n` to the data

    * **Function**
        .. math::
            y(x) = \\sum_{i=0}^n A_i x^i

    * **Parameters**
       - :math:`n`: degree of the polynomial function.
       - :math:`A_i`: polynomial coefficeints.
    """
    thname = "Polynomial"
    description = "Fit a polynomial of degree n"

    def __new__(cls, name="", parent_dataset=None, ax=None):
        """Create an instance of the GUI or CL class"""
        return GUITheoryPolynomial(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryPolynomial(
                name, parent_dataset, ax)


class BaseTheoryPolynomial:
    """Base class for both GUI and CL"""

    html_help_file = 'http://reptate.readthedocs.io/manual/All_Theories/basic_theories.html#polynomial'
    single_file = True
    thname = TheoryPolynomial.thname

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**

        Keyword Arguments:
            - name {str} -- Name of the theory (default: {""})
            - parent_dataset {DataSet} -- DataSet that contains this theory (default: {None})
            - ax {Axes array} -- Matplotlib axes where the theory will plot the data (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.MAX_DEGREE = 10
        self.function = self.polynomial
        self.parameters["n"] = Parameter(
            name="n",
            value=1,
            description="Degree of Polynomial",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False)
        for i in range(self.parameters["n"].value + 1):
            self.parameters["A%d" % i] = Parameter(
                "A%d" % i,
                1.0,
                "Coefficient order %d" % i,
                ParameterType.real,
                opt_type=OptType.opt)
        self.Qprint("%s: A0 + A1*x + A2*x^2 + ..." % self.thname)

    def set_param_value(self, name, value):
        """Change a parameter value, in particular *n*
        """
        if name == 'n':
            nold = self.parameters["n"].value
            Aold = np.zeros(nold + 1)
            for i in range(nold + 1):
                Aold[i] = self.parameters["A%d" % i].value
                del self.parameters["A%d" % i]

            nnew = value
            message, success = super().set_param_value("n", nnew)
            for i in range(nnew + 1):
                if i <= nold:
                    Aval = Aold[i]
                else:
                    Aval = 1.0
                self.parameters["A%d" % i] = Parameter(
                    "A%d" % i,
                    Aval,
                    "Coefficient degree %d" % i,
                    ParameterType.real,
                    opt_type=OptType.opt)
        else:
            message, success = super().set_param_value(name, value)

        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()
        self.update_parameter_table()
        return message, success

    def polynomial(self, f=None):
        """Actual polynomial function.

        .. math::
            y(x) = \\sum_{i=0}^n A_i x^i
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        for i in range(self.parameters["n"].value + 1):
            a = self.parameters["A%d" % i].value
            for j in range(1, tt.num_columns):
                tt.data[:, j] += a * tt.data[:, 0]**i


class CLTheoryPolynomial(BaseTheoryPolynomial, Theory):
    """CL Version"""

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)


class GUITheoryPolynomial(BaseTheoryPolynomial, QTheory):
    """GUI Version"""

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, self.MAX_DEGREE) # min and max number of modes
        self.spinbox.setPrefix("degree ")
        self.spinbox.setValue(self.parameters["n"].value)  #initial value
        tb.addWidget(self.spinbox)
        self.thToolsLayout.insertWidget(0, tb)
        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged)

    def handle_spinboxValueChanged(self, value):
        """Handle a change of the parameter 'nmode'"""
        self.set_param_value("n", value)

"""
 _ __   _____      _____ _ __  | | __ ___      __
| '_ \ / _ \ \ /\ / / _ \ '__| | |/ _` \ \ /\ / /
| |_) | (_) \ V  V /  __/ |    | | (_| |\ V  V / 
| .__/ \___/ \_/\_/ \___|_|    |_|\__,_| \_/\_/  
|_|                                              
"""

class TheoryPowerLaw(CmdBase):
    """Fit a power law to the data

    * **Function**
        .. math::
            y(x) = a x^b

    * **Parameters**
       - :math:`a`: prefactor.
       - :math:`b`: exponent.
    """
    thname = "Power Law"
    description = "Fit Power Law"

    def __new__(cls, name="", parent_dataset=None, ax=None):
        """Create an instance of the GUI or CL class"""
        return GUITheoryPowerLaw(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryPowerLaw(
                name, parent_dataset, ax)


class BaseTheoryPowerLaw:
    """Base class for both GUI and CL"""
    html_help_file = 'http://reptate.readthedocs.io/manual/All_Theories/basic_theories.html#power-law'
    single_file = True
    thname = TheoryPowerLaw.thname

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)
        self.function = self.powerlaw
        self.parameters["a"] = Parameter(
            "a", 1.0, "Prefactor", ParameterType.real, opt_type=OptType.opt)
        self.parameters["b"] = Parameter(
            "b", 1.0, "Exponent", ParameterType.real, opt_type=OptType.opt)
        self.Qprint("%s: a*x^b" % self.thname)

    def powerlaw(self, f=None):
        """Actual function

    * **Function**
        .. math::
            y(x) = a x^b
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        for j in range(1, tt.num_columns):
            tt.data[:, j] = self.parameters[
                "a"].value * tt.data[:, 0]**self.parameters["b"].value


class CLTheoryPowerLaw(BaseTheoryPowerLaw, Theory):
    """CL Version"""

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)


class GUITheoryPowerLaw(BaseTheoryPowerLaw, QTheory):
    """GUI Version"""

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)

"""
                                        _   _       _ 
  _____  ___ __   ___  _ __   ___ _ __ | |_(_) __ _| |
 / _ \ \/ / '_ \ / _ \| '_ \ / _ \ '_ \| __| |/ _` | |
|  __/>  <| |_) | (_) | | | |  __/ | | | |_| | (_| | |
 \___/_/\_\ .__/ \___/|_| |_|\___|_| |_|\__|_|\__,_|_|
          |_|                                         
"""

class TheoryExponential(CmdBase):
    """Fit a single exponential decay to the data

    * **Function**
        .. math::
            y(x) = a \\exp(-x/T)

    * **Parameters**
       - :math:`a`: prefactor.
       - :math:`T`: exponential "time" constant.

    """
    thname = "Exponential"
    description = "Fit Exponential"

    def __new__(cls, name="", parent_dataset=None, ax=None):
        """Create an instance of the GUI or CL class"""
        return GUITheoryExponential(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryExponential(
                name, parent_dataset, ax)

class BaseTheoryExponential:
    """Base class for both GUI and CL"""
    html_help_file = 'http://reptate.readthedocs.io/manual/All_Theories/basic_theories.html#exponential'
    single_file = True
    thname = TheoryExponential.thname

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)
        self.function = self.exponential
        self.parameters["a"] = Parameter(
            "a", 1.0, "Prefactor", ParameterType.real, opt_type=OptType.opt)
        self.parameters["T"] = Parameter(
            "T",
            1.0,
            "Exponential time constant",
            ParameterType.real,
            opt_type=OptType.opt)
        self.Qprint("%s: a*exp(-x/T)" % self.thname)

    def exponential(self, f=None):
        """**Function** :math:`y(x) = a \\exp(-x/T)`"""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        for j in range(1, tt.num_columns):
            tt.data[:, j] = self.parameters["a"].value * np.exp(
                -tt.data[:, 0] / self.parameters["T"].value)

class CLTheoryExponential(BaseTheoryExponential, Theory):
    """CL Version"""

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)


class GUITheoryExponential(BaseTheoryExponential, QTheory):
    """GUI Version"""

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)

"""
 ____                                           _   _       _     
|___ \    _____  ___ __   ___  _ __   ___ _ __ | |_(_) __ _| |___ 
  __) |  / _ \ \/ / '_ \ / _ \| '_ \ / _ \ '_ \| __| |/ _` | / __|
 / __/  |  __/>  <| |_) | (_) | | | |  __/ | | | |_| | (_| | \__ \
|_____|  \___/_/\_\ .__/ \___/|_| |_|\___|_| |_|\__|_|\__,_|_|___/
                  |_|                                             
"""

class TheoryTwoExponentials(CmdBase):
    """Fit **two** single exponential decay to the data

    * **Function**
        .. math::
            y(x) = a_1 \\exp(x/T_1) + a_2 \\exp(-x/T_2)

    * **Parameters**
       - :math:`a_1`, :math:`a_2`: prefactors.
       - :math:`T_1`, :math:`T_2`: exponential "time" constants.
    """
    thname = "Two Exponentials"
    description = "Fit two exponentials"

    def __new__(cls, name="", parent_dataset=None, ax=None):
        """Create an instance of the GUI or CL class"""
        return GUITheoryTwoExponentials(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryTwoExponentials(
                name, parent_dataset, ax)

class BaseTheoryTwoExponentials:
    """Base class for both GUI and CL"""
    html_help_file = 'http://reptate.readthedocs.io/manual/All_Theories/basic_theories.html#double-exponential'
    single_file = True
    thname = TheoryTwoExponentials.thname

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)
        self.function = self.two_exponentials
        self.parameters["a1"] = Parameter(
            "a1", 0.9, "Prefactor 1", ParameterType.real, opt_type=OptType.opt)
        self.parameters["T1"] = Parameter(
            "T1",
            1.0,
            "Exponential time constant 1",
            ParameterType.real,
            opt_type=OptType.opt)
        self.parameters["a2"] = Parameter(
            "a2", 0.1, "Prefactor 2", ParameterType.real, opt_type=OptType.opt)
        self.parameters["T2"] = Parameter(
            "T2",
            10.0,
            "Exponential time constant 2",
            ParameterType.real,
            opt_type=OptType.opt)
        self.Qprint("%s: a1*exp(-x/T1) + a2*exp(-x/T2)" % self.thname)

    def two_exponentials(self, f=None):
        """Actual function

    * **Function**
        .. math::
            y(x) = a_1 \\exp(x/T_1) + a_2 \\exp(-x/T_2)
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        a1 = self.parameters["a1"].value
        a2 = self.parameters["a2"].value
        T1 = self.parameters["T1"].value
        T2 = self.parameters["T2"].value
        for j in range(1, tt.num_columns):
            tt.data[:, j] = a1 * np.exp(-tt.data[:, 0] / T1) + a2 * np.exp(
                -tt.data[:, 0] / T2)

class CLTheoryTwoExponentials(BaseTheoryTwoExponentials, Theory):
    """CL Version"""

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)


class GUITheoryTwoExponentials(BaseTheoryTwoExponentials, QTheory):
    """GUI Version"""

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)

"""
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

class TheoryAlgebraicExpression(CmdBase):
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
    thname = "Algebraic Expression"
    description = "Fit an algebraic expression with n parameters"

    def __new__(cls, name="", parent_dataset=None, ax=None):
        """Create an instance of the GUI or CL class"""
        return GUITheoryAlgebraicExpression(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryAlgebraicExpression(
                name, parent_dataset, ax)


class BaseTheoryAlgebraicExpression:
    """Base class for both GUI and CL"""
    html_help_file = 'http://reptate.readthedocs.io/manual/All_Theories/basic_theories.html#algebraic-expression'
    single_file = False
    thname = TheoryAlgebraicExpression.thname

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)
        self.MAX_DEGREE = 10
        self.function = self.algebraicexpression
        self.parameters["n"] = Parameter(
            name="n",
            value=2,
            description="Number of Parameters",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False)
        self.parameters["expression"] = Parameter(
            name="expression",
            value="A0+A1*x",
            description="Algebraic Expression",
            type=ParameterType.string,
            opt_type=OptType.const,
            display_flag=False)
        for i in range(self.parameters["n"].value):
            self.parameters["A%d" % i] = Parameter(
                "A%d" % i,
                1.0,
                "Parameter %d" % i,
                ParameterType.real,
                opt_type=OptType.opt)

        safe_list = ['sin', 'cos', 'tan', 'arccos', 'arcsin', 'arctan', 'arctan2', 'deg2rad', 'rad2deg', 'sinh', 'cosh', 'tanh', 'arcsinh', 'arccosh', 'arctanh', 'around', 'round_', 'rint', 'floor', 'ceil','trunc', 'exp', 'log', 'log10', 'fabs', 'mod', 'e', 'pi', 'power', 'sqrt']
        self.safe_dict = {}
        for k in safe_list:
            self.safe_dict[k] = globals().get(k, None)
        

    def set_param_value(self, name, value):
        """Change a parameter value, in particular *n*
        """
        if name == 'n':
            nold = self.parameters["n"].value
            Aold = np.zeros(nold)
            for i in range(nold):
                Aold[i] = self.parameters["A%d" % i].value
                del self.parameters["A%d" % i]

            nnew = value
            message, success = super().set_param_value("n", nnew)
            for i in range(nnew):
                if i < nold:
                    Aval = Aold[i]
                else:
                    Aval = 1.0
                self.parameters["A%d" % i] = Parameter(
                    "A%d" % i,
                    Aval,
                    "Parameter %d" % i,
                    ParameterType.real,
                    opt_type=OptType.opt)
        else:
            message, success = super().set_param_value(name, value)

        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()
        self.update_parameter_table()
        return message, success

    def algebraicexpression(self, f=None):
        """Actual function.

    * **Function**
        .. math::
            y(x) = f({A_i}, x)
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        expression = self.parameters["expression"].value
        params = set(re.findall( "A\d{1,2}", expression))
        nparams=len(params)
        maxparamindex=-1;
        for p in params:
            paramindex=int(p.split('A')[1])
            if paramindex>maxparamindex:
                maxparamindex = paramindex
        n = self.parameters["n"].value
        if (maxparamindex!=n-1) or (nparams!=n):
            self.logger.warning("Wrong expression or number of parameters. Review your theory")
            self.Qprint("<b><font color=red>Wrong expression or number of parameters</font></b>. Review your theory")
        else:
            # Find FILE PARAMETERS IN THE EXPRESSION
            fparams = re.findall("\[(.*?)\]",expression)
            for fp in fparams:
                if fp in f.file_parameters:
                    self.safe_dict[fp]=float(f.file_parameters[fp])
                else:
                    self.logger.warning("File parameter not found. Review your theory")
                    self.Qprint("<b><font color=red>File parameter not found</font></b>. Review your theory")
                    self.safe_dict[fp]=0.0
            expression = expression.replace("[","").replace("]","")

            self.safe_dict['x']=tt.data[:, 0]
            for i in range(n):
                self.safe_dict['A%d'%i]=self.parameters["A%d" % i].value
            
            try:
                y = eval(expression, {"__builtins__":None}, self.safe_dict)
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
                #print (e.__class__, ":", e)


    def do_error(self, line):
        super().do_error(line)
        self.Qprint("%s: <b>%s</b>" % (self.thname, self.parameters["expression"].value))

class CLTheoryAlgebraicExpression(BaseTheoryAlgebraicExpression, Theory):
    """CL Version"""

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)


class GUITheoryAlgebraicExpression(BaseTheoryAlgebraicExpression, QTheory):
    """GUI Version"""

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, self.MAX_DEGREE)  # min and max number of modes
        self.spinbox.setToolTip("Number of parameters")
        self.spinbox.setValue(self.parameters["n"].value)  #initial value
        tb.addWidget(self.spinbox)
        self.expressionCB = QComboBox()
        self.expressionCB.setToolTip("Algebraic expression")
        self.expressionCB.addItem("A0+A1*x")
        self.expressionCB.addItem("A0*sin(A1*x)")
        self.expressionCB.addItem("A0*sin(A1*x+A2)")
        self.expressionCB.setEditable(True)
        self.expressionCB.setMinimumWidth(self.parent_dataset.width()-75)
        tb.addWidget(self.expressionCB)

        self.thToolsLayout.insertWidget(0, tb)
        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged)
        connection_id = self.expressionCB.currentIndexChanged.connect(
            self.handle_expressionChanged)

    def handle_spinboxValueChanged(self, value):
        """Handle a change of the parameter 'n'"""
        self.set_param_value("n", value)

    def handle_expressionChanged(self, item):
        """Handle a change in the algebraic expression"""
        self.set_param_value("expression", self.expressionCB.itemText(item))