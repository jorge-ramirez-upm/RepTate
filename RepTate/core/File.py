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
# Copyright (2017): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module File

Module that defines a basic File, with headers, columns and data.

""" 
import os
from DataTable import DataTable

class File(object):
    """Basic class that describes elements of a DataSet
    
    [description]
    """

    def __init__(self, file_name="", file_type=None, parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        [description]
        
        Keyword Arguments:
            - file_name {str} -- Full path
            - file_type {[type]} -- [description] (default: {None})
            - parent_dataset {[type]} -- [description] (default: {None})
            - axarr {[type]} -- [description] (default: {None})
        """
        self.file_full_path = os.path.abspath(file_name)
        tmpname = self.file_full_path.split(os.sep)
        tmpname = tmpname[len(tmpname)-1]
        lst = tmpname.split('.')
        short = '.'.join(lst[:-1])      
        self.file_name_short = short
        self.file_type = file_type
        self.parent_dataset = parent_dataset
        self.axarr = axarr

        #plot attributes
        self.marker = None
        self.color = None
        self.filled = None
        self.size = None

        self.header_lines=[]
        self.file_parameters={}
        self.active = True
        self.data_table = DataTable(axarr, self.file_name_short)

    def __str__(self):
        """[summary]
        
        [description]
        """
        return '%s: %s' % (self.file_full_path, self.file_parameters)
        
    def mincol(self, col):
        """Minimum value in data_table column col
        [description]

        """
        return self.data_table.mincol(col)
        
    def minpositivecol(self, col):
        """Minimum positive value in data_table column col
        [description]

        """
        return self.data_table.minpositivecol(col)

    def maxcol(self, col):
        """Maximum value in data_table column col
        [description]

        """
        return self.data_table.maxcol(col)
    