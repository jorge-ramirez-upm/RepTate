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
# Copyright (2018): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module ToolGradient

Gradient file for creating a new Tool
"""
import numpy as np
from RepTate.core.CmdBase import CmdBase
from RepTate.core.Tool import Tool
from RepTate.gui.QTool import QTool


class ToolGradient(CmdBase):
    """Calculate the derivative of y with respect to x, where y is the ordinate and x is the abcissa in the current view. The gradient function from numpy is used, where the derivative is computed using second order accurate central differences in the interior points and first order accurate one-sides (forward or backwards) differences at the boundaries.
    """

    toolname = "Gradient"
    description = "Take derivative of current data/view"
    citations = []

    def __new__(cls, name="", parent_app=None):
        """Create an instance of the GUI"""
        return GUIToolGradient(name, parent_app)


class BaseToolGradient:
    """Base class for both GUI"""

    # html_help_file = 'http://reptate.readthedocs.io/manual/Tools/Gradient.html'
    toolname = ToolGradient.toolname
    citations = ToolGradient.citations

    def __init__(self, name="", parent_app=None):
        """**Constructor**"""
        super().__init__(name, parent_app)
        # self.function = self.gradient  # main Tool function
        # self.parameters['param1'] = Parameter(
        # name='param1',
        # value=1,
        # description='parameter 1',
        # type=ParameterType.real,
        # opt_type=OptType.const)

    def calculate(self, x, y, ax=None, color=None, file_parameters=[]):
        try:
            y2 = np.gradient(y, x)
            return x, y2

        except TypeError as e:
            print("in ToolGradient.Gradient() ", e)
            return x, y


class GUIToolGradient(BaseToolGradient, QTool):
    """GUI Version"""

    def __init__(self, name="", parent_app=None):
        """**Constructor**"""
        super().__init__(name, parent_app)
        self.update_parameter_table()
        self.parent_application.update_all_ds_plots()

    # add widgets specific to the Tool here:
