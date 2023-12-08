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
# Copyright (2017-2023): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module TheoryArrhenius
"""
import numpy as np
from RepTate.core.Parameter import Parameter, ParameterType, OptType
from RepTate.gui.QTheory import QTheory


class TheoryArrhenius(QTheory):
    """Arrhenius Equation

    * **Function**
        .. math::
            a_T = \\exp\\left(\\frac{E_a}{R} \\left(\\frac{1}{T} - \\frac{1}{T_{ref}}\\right) \\right)
    
    * **Parameters**
       - :math:`E_a`: Activation Energy
       - :math:`T_{ref}`: Reference Temperature for the shift factors
       - :math:`R`: Gas Constant
    """

    thname = "ArrheniusTheory"
    description = "Arrhenius Theory"
    citations = []
    # html_help_file = ''
    single_file = (
        True  # False if the theory can be applied to multiple files simultaneously
    )

    def __init__(self, name="", parent_dataset=None, axarr=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate  # main theory function
        self.has_modes = False  # True if the theory has modes
        self.parameters["Tref"] = Parameter(
            name="Tref",
            value=0,
            description="Reference Temperature (°C)",
            type=ParameterType.real,
            opt_type=OptType.const,
        )
        self.parameters["Ea"] = Parameter(
            name="Ea",
            value=100,
            description="Activation Energy",
            type=ParameterType.real,
            opt_type=OptType.opt,
        )

    def calculate(self, f=None):
        """Arrhenius function"""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        tt.data[:, 1] = np.exp(
            self.parameters["Ea"].value
            / 8.314
            * (
                1 / (ft.data[:, 0] + 273.15)
                - 1 / (self.parameters["Tref"].value + 273.15)
            )
        )

