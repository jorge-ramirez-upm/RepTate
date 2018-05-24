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
"""Module ToolEvaluate

Evaluate expression
"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Tool import Tool
from QTool import QTool
from DataTable import DataTable

class ToolEvaluate(CmdBase):
    """[summary]
    
    [description]
    """
    toolname = 'EvalExp'
    description = 'Evaluate Expression Tool'
    citations = ''

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
        return GUIToolEvaluate(name, parent_app) if (CmdBase.mode == CmdMode.GUI) else CLToolEvaluate(name, parent_app)


class BaseToolEvaluate:
    """[summary]
    
    [description]
    """
    #help_file = 'http://reptate.readthedocs.io/en/latest/manual/Tools/template.html'
    toolname = ToolEvaluate.toolname
    citations = ToolEvaluate.citations

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
            value='x',
            description='Expression for abscissa',
            type=ParameterType.string)
        self.parameters['y'] = Parameter(
            name='y',
            value='y',
            description='Expression for ordinate',
            type=ParameterType.string)


    def destructor(self):
        """[summary]
        
        [description]
        
        Arguments:

        """
        pass

    def calculate(self, x, y, ax=None, color=None):
        """Evaluate function that returns the square of the y, according to the view        
        """
        xexpr = self.parameters["x"].value
        yexpr = self.parameters["y"].value
        var = {'x':x, 'y':y}
        x2 = eval(xexpr, var)
        y2 = eval(yexpr, var)
        return x2, y2


class CLToolEvaluate(BaseToolEvaluate, Tool):
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


class GUIToolEvaluate(BaseToolEvaluate, QTool):
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
