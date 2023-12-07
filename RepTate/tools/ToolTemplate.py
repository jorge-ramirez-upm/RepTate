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
"""Module ToolTemplate

Template file for creating a new Tool
"""
from RepTate.core.CmdBase import CmdBase
from RepTate.core.Parameter import Parameter, ParameterType
from RepTate.core.Tool import Tool
from RepTate.gui.QTool import QTool


class ToolTemplate(CmdBase):
    """TEMPLATE FOR NEW TOOLS. HERE IS WHERE THE BASIC INFORMATION OF THE TOOL SHOULD APPEAR.
    """

    toolname = "TemplateTool"
    description = "Template Tool"
    citations = []

    def __new__(cls, name="", parent_app=None):
        """Create an instance of the GUI"""
        return GUIToolTemplate(name, parent_app)


class BaseToolTemplate:
    """Base class for both GUI"""

    # html_help_file = 'http://reptate.readthedocs.io/manual/Tools/template.html'
    toolname = ToolTemplate.toolname
    citations = ToolTemplate.citations

    def __init__(self, name="", parent_app=None):
        """**Constructor**"""
        super().__init__(name, parent_app)
        # self.parameters['param1'] = Parameter(
        # name='param1',
        # value=1,
        # description='parameter 1',
        # type=ParameterType.real,
        # opt_type=OptType.const)

    def destructor(self):
        """If the tool needs to clear up memory in a very special way, fill up the contents of this function.
If not, you can safely delete it."""
        pass

    def calculate(self, x, y, ax=None, color=None, file_parameters=[]):
        """Template function that returns the square of the y, according to the view
        """
        return x, y * y



class GUIToolTemplate(BaseToolTemplate, QTool):
    """GUI Version"""

    def __init__(self, name="", parent_app=None):
        """**Constructor**"""
        super().__init__(name, parent_app)
        self.update_parameter_table()
        self.parent_application.update_all_ds_plots()

    # add widgets specific to the Tool here:
