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
# Copyright (2017): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
import numpy as np
from CmdBase import CmdBase, CmdMode
from Theory import Theory
from QTheory import QTheory
from Parameter import Parameter, ParameterType, ShiftType, OptType
from PyQt5.QtWidgets import QToolBar, QSpinBox
from PyQt5.QtCore import QSize

##################################################################
##################################################################


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

    def __new__(cls, name="ThPolynomial", parent_dataset=None, ax=None):
        return GUITheoryPolynomial(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryPolynomial(
                name, parent_dataset, ax)


class BaseTheoryPolynomial:
    help_file = 'http://reptate.readthedocs.io/en/latest/manual/All_Theories/basic_theories.html#polynomial'
    single_file = True

    def __init__(self, name="ThPolynomial", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"Polynomial"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
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
            self.parameters["A%02d" % i] = Parameter(
                "A%02d" % i,
                1.0,
                "Coefficient order %d" % i,
                ParameterType.real,
                opt_type=OptType.opt)

    def set_param_value(self, name, value):
        """[summary]

        [description]

        Arguments:
            name {[type]} -- [description]
            value {[type]} -- [description]
        """
        if name == 'n':
            nold = self.parameters["n"].value
            Aold = np.zeros(nold + 1)
            for i in range(nold + 1):
                Aold[i] = self.parameters["A%02d" % i].value
                del self.parameters["A%02d" % i]

            nnew = value
            message, success = super().set_param_value("n", nnew)
            for i in range(nnew + 1):
                if i <= nold:
                    Aval = Aold[i]
                else:
                    Aval = 1.0
                self.parameters["A%02d" % i] = Parameter(
                    "A%02d" % i,
                    Aval,
                    "Coefficient order %d" % i,
                    ParameterType.real,
                    opt_type=OptType.opt)
        else:
            message, success = super().set_param_value(name, value)

        self.do_calculate("")
        self.update_parameter_table()
        return message, success

    def polynomial(self, f=None):
        """Actual polynomial function.
        
        .. math::
            (a + b)^2  =  (a + b)(a + b) =  a^2 + 2ab + b^2
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        for i in range(self.parameters["n"].value + 1):
            a = self.parameters["A%02d" % i].value
            tt.data[:, 1] += a * tt.data[:, 0]**i


class CLTheoryPolynomial(BaseTheoryPolynomial, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name="ThPolynomial", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)


class GUITheoryPolynomial(BaseTheoryPolynomial, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self,
                 name="ThMaxwellFrequencyPolynomial",
                 parent_dataset=None,
                 ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1,
                              self.MAX_DEGREE)  # min and max number of modes
        self.spinbox.setPrefix("degree ")
        self.spinbox.setValue(self.parameters["n"].value)  #initial value
        tb.addWidget(self.spinbox)
        self.thToolsLayout.insertWidget(0, tb)
        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged)

    def handle_spinboxValueChanged(self, value):
        """[summary]
        
        [description]
        
        Arguments:
            value {[type]} -- [description]
        """
        """Handle a change of the parameter 'nmode'"""
        self.set_param_value("n", value)


##################################################################
##################################################################


class TheoryPowerLaw(CmdBase):
    """Fit a power law to the data
    
    * **Function**
        .. math::
            y(x) = a x^b

    * **Parameters**
       - :math:`a`: prefactor.
       - :math:`b`: exponent.

    """
    thname = "PowerLaw"
    description = "Fit Power Law"

    def __new__(cls, name="ThPowerLaw", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryPowerLaw(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryPowerLaw(
                name, parent_dataset, ax)


class BaseTheoryPowerLaw:
    """Fit a power law to the data
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/en/latest/manual/All_Theories/basic_theories.html#power-law'
    single_file = True

    def __init__(self, name="PowerLaw", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"PowerLaw"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.powerlaw
        self.parameters["a"] = Parameter(
            "a", 1.0, "Prefactor", ParameterType.real, opt_type=OptType.opt)
        self.parameters["b"] = Parameter(
            "b", 1.0, "Exponent", ParameterType.real, opt_type=OptType.opt)

    def powerlaw(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        tt.data[:, 1] = self.parameters[
            "a"].value * tt.data[:, 0]**self.parameters["b"].value


class CLTheoryPowerLaw(BaseTheoryPowerLaw, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name="ThPowerLaw", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)


class GUITheoryPowerLaw(BaseTheoryPowerLaw, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self, name="ThPowerLaw", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)


##################################################################
##################################################################


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

    def __new__(cls, name="ThExponential", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryExponential(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryExponential(
                name, parent_dataset, ax)


class BaseTheoryExponential:
    """Fit an exponential decay to the data
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/en/latest/manual/All_Theories/basic_theories.html#exponential'
    single_file = True

    def __init__(self, name="Exponential", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"Exponential"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
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

    def exponential(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        tt.data[:, 1] = self.parameters["a"].value * np.exp(
            -tt.data[:, 0] / self.parameters["T"].value)


class CLTheoryExponential(BaseTheoryExponential, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name="ThExponential", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)


class GUITheoryExponential(BaseTheoryExponential, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self, name="ThExponential", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)


##################################################################
##################################################################


class TheoryTwoExponentials(CmdBase):
    """Fit **two** single exponential decay to the data
    
    * **Function**
        .. math::
            y(x) = a_1 \\exp(x/T_1) + a_2 \\exp(-x/T_2)

    * **Parameters**
       - :math:`a_1`, :math:`a_2`: prefactors.
       - :math:`T_1`, :math:`T_2`: exponential "time" constants.

    """
    thname = "TwoExponentials"
    description = "Fit two exponentials"

    def __new__(cls, name="ThTwoExponentials", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryTwoExponentials(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryTwoExponentials(
                name, parent_dataset, ax)


class BaseTheoryTwoExponentials:
    """Fit 2 exponentials decay to the data
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/en/latest/manual/All_Theories/basic_theories.html#double-exponential'
    single_file = True

    def __init__(self, name="TwoExponentials", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"TwoExponentials"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
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

    def two_exponentials(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
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
        tt.data[:, 1] = a1 * np.exp(-tt.data[:, 0] / T1) + a2 * np.exp(
            -tt.data[:, 0] / T2)


class CLTheoryTwoExponentials(BaseTheoryTwoExponentials, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name="ThTwoExponentials", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellTime"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)


class GUITheoryTwoExponentials(BaseTheoryTwoExponentials, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self, name="ThTwoExponentials", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellTime"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)


##################################################################
##################################################################
