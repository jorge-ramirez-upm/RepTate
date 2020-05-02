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
"""Module InterpolateExtrapolate

Interpolate/Extrapolate data
"""
import traceback
import numpy as np
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Parameter import Parameter, ParameterType, OptType
from RepTate.core.Tool import Tool
from RepTate.gui.QTool import QTool
from RepTate.core.DataTable import DataTable
from scipy.interpolate import interp1d

class ToolInterpolateExtrapolate(CmdBase):
    """[summary]

    [description]
    """
    toolname = 'Interpolate/Extrapolate'
    description = 'Interpolate/Extrapolate from view'
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
        return GUIToolInterpolateExtrapolate(name, parent_app) if (CmdBase.mode == CmdMode.GUI) else CLToolInterpolateExtrapolate(name, parent_app)


class BaseToolInterpolateExtrapolate:
    """[summary]

    [description]
    """
    #help_file = 'http://reptate.readthedocs.io/manual/Tools/template.html'
    toolname = ToolInterpolateExtrapolate.toolname
    citations = ToolInterpolateExtrapolate.citations

    def __init__(self, name='', parent_app=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_app)
        self.parameters['x'] = Parameter(
            name='x',
            value=1,
            description='x',
            type=ParameterType.real,
            opt_type=OptType.const)

    def calculate(self, x, y, ax=None, color=None):
        """InterpolateExtrapolate function that returns the square of the y, according to the view
        """
        xval = self.parameters["x"].value
        xunique, indunique = np.unique(x, return_index=True)
        yunique=y[indunique]
        try:
            # table='''<table border="1" width="100%">'''
            # table+='''<tr><th>x</th><th>y</th></tr>'''
            table = [['%-10s' % 'x', '%-10s' % 'y'], ]
            ff = interp1d(xunique, yunique, bounds_error=False, kind='cubic', fill_value='extrapolate', assume_sorted=True)
            func = lambda t: ff(t)
            yval = func(xval)
            # table+='''<tr><td>%.4e</td><td>%.4e</td></tr>'''%(xval,yval)
            table.append(['%-10.4e' % xval, '%-10.4e' % yval])
            # table+='''</table><br>'''
            self.Qprint(table)
        except Exception as e:
            self.Qprint("in ToolInterpolateExtrapolate.calculate(): %s"%traceback.format_exc())
        return x, y


class CLToolInterpolateExtrapolate(BaseToolInterpolateExtrapolate, Tool):
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


class GUIToolInterpolateExtrapolate(BaseToolInterpolateExtrapolate, QTool):
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
