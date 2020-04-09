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
"""Module DataTable

Module for the actual object that contains the data, both for experiments and theory. 

""" 
import numpy as np
import matplotlib.pyplot as plt

class DataTable(object):
    """Class that stores data and series
    
    [description]
    """
    MAX_NUM_SERIES=3
    PICKRADIUS = 10

    def __init__(self, axarr=None, _name=''):
        """
        **Constructor**
        
        [description]
        
        Keyword Arguments:
            - axarr {[type]} -- [description] (default: {None})
        """
        self.num_columns=0
        self.num_rows=0
        self.column_names=[]
        self.column_units=[]
        self.data=np.zeros((self.num_rows, self.num_columns))
        self.series=[]
        self.extra_tables = {}
        
        if axarr != None:
            for nx in range(len(axarr)): #create series for each plot
                series_nx = []
                for i in range(self.MAX_NUM_SERIES): 
                    ss = axarr[nx].plot([], [], label='', picker=self.PICKRADIUS)
                    if i == 0:
                        ss[0]._name = _name #define artist name
                    else:    
                        ss[0]._name = _name + " #%d"%(i + 1) #define artist name
                    series_nx.append(ss[0])
                self.series.append(series_nx)

    def __str__(self):
        """[summary]
        
        [description]

        .. todo:: Refine this. It doesn't work
        """
        return self.data
        
    def mincol(self, col):
        """Minimum value in table column col
        
        [description]

        """
        return np.min(self.data[:,col])
        
    def minpositivecol(self, col):
        """Minimum positive value in table column col
        
        [description]

        """
        return (self.data[self.data[:,col]>0,col]).min()

    def maxcol(self, col):
        """Maximum value in table column col
        
        [description]

        """
        return np.max(self.data[:,col])
        