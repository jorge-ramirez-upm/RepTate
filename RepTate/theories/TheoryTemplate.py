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
"""Module TheoryTemplate

Template file for creating a new theory
"""
import numpy as np
from CmdBase import CmdBase
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory


class TheoryTemplate(CmdBase):
    """The basic documentation of the theory goes here. Please, add as much information as possible 
    (references, equations, qualitative descriptions, etc. """

    thname = "TemplateTheory"
    description = "Template Theory"
    citations = []
    doi = []

    def __new__(cls, name="", parent_dataset=None, axarr=None):
        """Create an instance of the GUI"""
        return GUITheoryTemplate(name, parent_dataset, axarr)


class BaseTheoryTemplate:
    """Base class for both GUI"""

    # html_help_file = ''
    single_file = (
        False  # False if the theory can be applied to multiple files simultaneously
    )
    thname = TheoryTemplate.thname
    citations = TheoryTemplate.citations

    def __init__(self, name="", parent_dataset=None, axarr=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate  # main theory function
        self.has_modes = False  # True if the theory has modes
        self.parameters["param1"] = Parameter(
            name="param1",
            value=1,
            description="parameter 1",
            type=ParameterType.real,
            opt_type=OptType.const,
        )

    def get_modes(self):
        """If the theory provides Maxwell modes, fill this up (see examples in TheoryMaxwellModes.
If the theory does not provide modes, simply delete this function."""
        tau = np.ones(1)
        G = np.ones(1)
        return tau, G, False

    def set_modes(self):
        """If the theory provides Maxwell modes, fill this up (see examples in TheoryMaxwellModes.
If the theory does not provide modes, simply delete this function."""
        self.logger.info("set_modes not allowed in this theory (%s)" % elf.thname)
        return False

    def destructor(self):
        """If the theory needs to clear up memory in a very special way, fill up the contents of this function.
If not, you can safely delete it."""
        pass

    def calculate(self, f=None):
        """THIS IS THE FUNCTION THAT CALCULATES THE THEORY"""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        tt.data[:, 1] = ft.data[:, 1] * ft.data[:, 1]


class GUITheoryTemplate(BaseTheoryTemplate, QTheory):
    """GUI Version"""

    def __init__(self, name="", parent_dataset=None, axarr=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, axarr)

    # add widgets specific to the theory here:
