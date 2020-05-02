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
"""Module ToolIntegral

Integral file for creating a new Tool
"""
import traceback
import numpy as np
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Parameter import Parameter, ParameterType, OptType
from RepTate.core.Tool import Tool
from RepTate.gui.QTool import QTool
from RepTate.core.DataTable import DataTable
from scipy.integrate import odeint, simps
from scipy.interpolate import interp1d

class ToolIntegral(CmdBase):
    """Calculate the integral of y with respect to x, where y is the ordinate and x is the abcissa in the current view. Repeated points in the data are removed before the integral is performed. The data between the point is interpolated with a cubic spline. The total value of the definite integral is shown in the Tool output region.
    If a different integration interval is needed, the Bounds tool can be used before the Integral tool.
    """
    toolname = 'Integral'
    description = 'Integral of current data/view'
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
        return GUIToolIntegral(name, parent_app) if (CmdBase.mode == CmdMode.GUI) else CLToolIntegral(name, parent_app)


class BaseToolIntegral:
    """[summary]

    [description]
    """
    #help_file = 'http://reptate.readthedocs.io/manual/Tools/Integral.html'
    toolname = ToolIntegral.toolname
    citations = ToolIntegral.citations

    def __init__(self, name='', parent_app=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_app)

        #self.function = self.integral  # main Tool function
        # self.parameters['param1'] = Parameter(
            # name='param1',
            # value=1,
            # description='parameter 1',
            # type=ParameterType.real,
            # opt_type=OptType.const)

    def calculate(self, x, y, ax=None, color=None):
        """Integral function that returns the square of the y, according to the view"""
        xunique, indunique = np.unique(x, return_index=True)
        num_rows = len(xunique)
        yunique=y[indunique]
        try:
            ff = interp1d(xunique, yunique, bounds_error=False, kind='cubic', fill_value='extrapolate', assume_sorted=True)

            func = lambda y0, t: ff(t)
            y2 = odeint(func, [0], xunique)

            y2 = np.reshape(y2,num_rows,1)
            self.Qprint("<b>I</b> = %g"%y2[-1])
            return xunique, y2
        except Exception as e:
            self.Qprint("in ToolIntegral.calculate(): %s"%traceback.format_exc())
            return x, y


class CLToolIntegral(BaseToolIntegral, Tool):
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


class GUIToolIntegral(BaseToolIntegral, QTool):
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
