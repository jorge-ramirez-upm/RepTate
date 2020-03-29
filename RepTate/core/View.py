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
# Copyright (2017-2020): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module View

Module that defines the basic properties of a View, that will be used to represent
the data graphically.

"""
from enum import Enum

class ViewMode(Enum):
    """Defines how to show the experimental/theoretical data view
    TO BE DONE...
    
    Parameters can be:
        - symbol: Show symbols (default for experimental data -- files in the dataset)
        - line: Show lines (default for theories)
        - bar: Show bars 
    """
    symbol = 0
    line = 1
    bar = 2

class View(object):
    """Abstract class to describe a view
 
    [description]
    """

    def __init__(self,
                 name="",
                 description="",
                 x_label="",
                 y_label="",
                 x_units="",
                 y_units="",
                 log_x=False,
                 log_y=False,
                 view_proc=None,
                 n=1,
                 snames=[],
                 inverse_view_proc=None,
                 index=0,
                 with_thline=True,
                 filled=False,
                 viewmode_data=ViewMode.symbol,
                 viewmode_theory=ViewMode.line):
        """
        **Constructor**
        
        [description]
        
        Keyword Arguments:
            - name {str} -- View name
            - description {str} -- Description of the view
            - x_label {str} -- Label of the x axis
            - y_label {str} -- Label of the y axis
            - x_units {str} -- Default units of the x axis
            - y_units {str} -- Default units of the y axis
            - log_x {bool} -- X axis logarithmic? (default: {False})
            - log_y {bool} -- Y axis logarithmic? (default: {False})
            - view_proc {func} -- Function that creates the X, Y1, Y2 values of the view (default: {None})
            - inverse_view_proc {func} -- Function that inverses the view: From the n values of the view, returns the data table values (default: {None})
            - n {int} -- Number of series that the view represents (default: {1})
            - snames {list of str} -- Names of the series represented by the view
            - with_thline {bool} -- if True, plot the theory with lines, else use symbols
            - filled {bool} -- if True, use filled symbols (when with_thline=False)
        """
        self.name = name
        self.description = description
        self.x_label = x_label
        self.y_label = y_label
        self.x_units = x_units
        self.y_units = y_units
        self.log_x = log_x
        self.log_y = log_y
        self.view_proc = view_proc
        self.inverse_view_proc = inverse_view_proc
        self.n = n
        self.snames = snames
        self.with_thline = with_thline
        self.filled = filled
        self.viewmode_data=viewmode_data
        self.viewmode_theory=viewmode_theory
