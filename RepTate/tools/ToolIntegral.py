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
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Tool import Tool
from QTool import QTool
from DataTable import DataTable
from scipy.integrate import odeint, simps
from scipy.interpolate import interp1d

class ToolIntegral(CmdBase):
    """[summary]
    
    [description]
    """
    toolname = 'IntegralTool'
    description = 'Integral Tool'
    citations = ''

    def __new__(cls, name=''):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUIToolIntegral(name) if (CmdBase.mode == CmdMode.GUI) else CLToolIntegral(name)


class BaseToolIntegral:
    """[summary]
    
    [description]
    """
    #help_file = 'http://reptate.readthedocs.io/en/latest/manual/Tools/Integral.html'
    toolname = ToolIntegral.toolname
    citations = ToolIntegral.citations

    def __init__(self, name=''):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name)
        #self.function = self.integral  # main Tool function
        # self.parameters['param1'] = Parameter(
            # name='param1',
            # value=1,
            # description='parameter 1',
            # type=ParameterType.real,
            # opt_type=OptType.const)


    def destructor(self):
        """[summary]
        
        [description]
        
        Arguments:

        """
        pass

    def calculate(self, x, y):
        """Integral function that returns the square of the y, according to the view"""
        xunique, indunique = np.unique(x, return_index=True)
        num_rows = len(xunique)
        yunique=y[indunique]
        try:
            ff = interp1d(xunique, yunique, kind='cubic', fill_value='extrapolate', assume_sorted=True)
                
            func = lambda y0, t: ff(t)
            y2 = odeint(func, [0], xunique)

            y2 = np.reshape(y2,num_rows,1)
            return xunique, y2
        except TypeError as e:
            print("in ToolIntegral.calculate() ", e)
            return x, y

    #def integral(self, f=None, v=None):
    #    """Integral function that returns the square of the y, according to the view
        
    #    [description]
        
    #    Keyword Arguments:
    #        - f {[type]} -- [description] (default: {None})
        
    #    Returns:
    #        - [type] -- [description]
    #    """
    #    n = v.n

    #    tt = self.tables[f.file_name_short]
    #    tt.num_columns = n+1
    #    # Here, we assume that all series have the same x axis
    #    s = f.data_table.series[0][0]
    #    x = np.array(s.get_xdata())
    #    xunique, indunique = np.unique(x, return_index=True)
    #    tt.num_rows = len(xunique)
    #    tt.data = np.zeros((tt.num_rows, tt.num_columns))
    #    tt.data[:, 0] = xunique

    #    print("%20s"%"FILE", end='')
    #    for i in range(n):
    #        print (" %9s%1d"%("Int",i), end='')
    #    print("") 
        
    #    print ("%20s"%f.file_name_short, end='')
    #    for i in range(n):
    #        s = f.data_table.series[0][i]
    #        y = np.array(s.get_ydata())
    #        yunique=y[indunique]
    #        try:
    #            ff = interp1d(xunique, yunique, kind='cubic', fill_value='extrapolate', assume_sorted=True)
                
    #            func = lambda y0, t: ff(t)
    #            y2 = odeint(func, [0], xunique)

    #            tt.data[:, i+1] = np.reshape(y2,tt.num_rows,1)
    #        except TypeError as e:
    #            print("in ToolIntegral.integral() ", e)
    #            return

    #        I = simps(yunique,xunique)
    #        print (" %10g"%I, end='')
    #    print("") 
            

class CLToolIntegral(BaseToolIntegral, Tool):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name)

    # This class usually stays empty


class GUIToolIntegral(BaseToolIntegral, QTool):
    """[summary]
    
    [description]
    """

    def __init__(self, name=''):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name)

    # add widgets specific to the Tool here:
