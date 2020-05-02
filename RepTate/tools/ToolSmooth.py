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
"""Module ToolSmooth

Smooth data by applying a Savitzky-Golay filter
"""
import traceback
import numpy as np
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Parameter import Parameter, ParameterType, OptType
from RepTate.core.Tool import Tool
from RepTate.gui.QTool import QTool
from RepTate.core.DataTable import DataTable
from scipy.signal import savgol_filter

class ToolSmooth(CmdBase):
    """Smooths the current view data by applying a Savitzky-Golay filter. The smoothing procedure is controlled by means of two parameters: the **window** length (a positive, odd integer), which represents the number of convolution coefficients of the filter, and the **order** of the polynomial used to fit the samples (must be smaller than the window length).
    """
    toolname = 'Smooth'
    description = 'Smooth Tool'
    citations = []

    def __new__(cls, name='', parent_app=None):
        """
        """
        return GUIToolSmooth(name, parent_app) if (CmdBase.mode == CmdMode.GUI) else CLToolSmooth(name, parent_app)


class BaseToolSmooth:
    """[summary]

    [description]
    """
    #help_file = 'http://reptate.readthedocs.io/manual/Tools/template.html'
    toolname = ToolSmooth.toolname
    citations = ToolSmooth.citations

    def __init__(self, name='', parent_app=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_app)
        self.parameters['window'] = Parameter(
            name='window',
            value=11,
            description='Length of filter window. Positive odd integer, smaller than the size of y and larger than order',
            type=ParameterType.integer)
        self.parameters['order'] = Parameter(
            name='order',
            value=3,
            description='Order of smoothing polynomial (must be smaller than window)',
            type=ParameterType.integer)

    def calculate(self, x, y, ax=None, color=None):
        """Smooth the x, y data
        """
        window = self.parameters["window"].value
        order = self.parameters["order"].value
        if (window % 2 == 0):
            self.Qprint("Invalid window (must be an odd number)")
            return x, y
        if (window >= len(y)):
            self.Qprint("Invalid window (must be smaller than the length of the data)")
            return x, y
        if (window<=order):
            self.Qprint("Invalid order (must be smaller than the window)")
            return x, y

        try:
            y2 = savgol_filter(y, window, order)
            return x, y2
        except Exception as e:
            self.Qprint("in ToolSmooth.calculate(): %s"%traceback.format_exc())
            return x, y



class CLToolSmooth(BaseToolSmooth, Tool):
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


class GUIToolSmooth(BaseToolSmooth, QTool):
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
            new_value = int(value)
        except ValueError:
            return "Value must be a integer", False
        message, success = super().set_param_value(name, value)
        if success:
            if name == 'window':
                order = self.parameters['order'].value
                if (new_value <= order or new_value < 0 or new_value%2==0):
                    p.value = old_value
                    message = "window must be a positive, odd integer, larger than order"
                    success = False
            elif name == 'order':
                window = self.parameters['window'].value
                if (new_value >= window or new_value<0):
                    p.value = old_value
                    message = "order must be >=0 and smaller than window"
                    success = False

        return message, success
