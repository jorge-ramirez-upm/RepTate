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
"""Module ToolBounds

Remove data ouside Bounds
"""
import numpy as np
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Parameter import Parameter, ParameterType, OptType
from RepTate.core.Tool import Tool
from RepTate.gui.QTool import QTool
from RepTate.core.DataTable import DataTable


class ToolBounds(CmdBase):
    """Remove points in the current view ïf :math:`x \\notin [x_{min}, x_{max}]` or :math:`y \\notin [y_{min}, y_{max}]`
    """
    toolname = 'Bounds'
    description = 'Bounds Tool'
    citations = []

    def __new__(cls, name='', parent_app=None):
        """[summary]

        [description]

        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})

        Returns:
            - [type] -- [description]
        """
        return GUIToolBounds(name, parent_app) if (CmdBase.mode == CmdMode.GUI) else CLToolBounds(name, parent_app)


class BaseToolBounds:
    """[summary]

    [description]
    """
    #help_file = 'http://reptate.readthedocs.io/manual/Tools/template.html'
    toolname = ToolBounds.toolname
    citations = ToolBounds.citations

    def __init__(self, name='', parent_app=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_app)
        self.parameters['xmin'] = Parameter(
            name='xmin',
            value=-np.Infinity,
            description='Minimum x',
            type=ParameterType.real)
        self.parameters['xmax'] = Parameter(
            name='xmax',
            value=np.Infinity,
            description='Maximum x',
            type=ParameterType.real)
        self.parameters['ymin'] = Parameter(
            name='ymin',
            value=-np.Infinity,
            description='Minimum y',
            type=ParameterType.real)
        self.parameters['ymax'] = Parameter(
            name='ymax',
            value=np.Infinity,
            description='Maximum y',
            type=ParameterType.real)

    def calculate(self, x, y, ax=None, color=None):
        """Bounds function that returns the square of the y, according to the view
        """
        xmin = self.parameters["xmin"].value
        xmax = self.parameters["xmax"].value
        ymin = self.parameters["ymin"].value
        ymax = self.parameters["ymax"].value
        conditionx = (x > xmin) * (x < xmax)
        conditiony = (y > ymin) * (y < ymax)
        x2 = np.extract(conditionx * conditiony, x)
        y2 = np.extract(conditionx * conditiony, y)
        return x2, y2


class CLToolBounds(BaseToolBounds, Tool):
    """[summary]

    [description]
    """

    def __init__(self, name='', parent_app=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_app)

    # This class usually stays empty


class GUIToolBounds(BaseToolBounds, QTool):
    """[summary]

    [description]
    """

    def __init__(self, name='', parent_app=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_app)
        self.update_parameter_table()
        self.parent_application.update_all_ds_plots()

    # add widgets specific to the Tool here:

    def set_param_value(self, name, value):
        p = self.parameters[name]
        old_value = p.value
        try:
            new_value = float(value)
        except ValueError:
            return "Value must be a float", False
        message, success = super().set_param_value(name, value)
        if success:
            if name == 'xmax':
                xmin = self.parameters['xmin'].value
                if new_value <= xmin:
                    p.value = old_value
                    message = "xmax must be > xmin"
                    success = False
            elif name == 'xmin':
                xmax = self.parameters['xmax'].value
                if new_value >= xmax:
                    p.value = old_value
                    message = "xmin must be < xmax"
                    success = False
            elif name == 'ymax':
                ymin = self.parameters['ymin'].value
                if new_value <= ymin:
                    p.value = old_value
                    message = "ymax must be > ymin"
                    success = False
            elif name == 'ymin':
                ymax = self.parameters['ymax'].value
                if new_value >= ymax:
                    p.value = old_value
                    message = "ymin must be < ymax"
                    success = False

        return message, success
