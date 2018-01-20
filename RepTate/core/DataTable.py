# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
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

    def __init__(self, axarr=None):
        """Constructor
        
        [description]
        
        Keyword Arguments:
            ax {[type]} -- [description] (default: {None})
        """
        self.num_columns=0
        self.num_rows=0
        self.column_names=[]
        self.column_units=[]
        self.data=np.zeros((self.num_rows, self.num_columns))
        self.series=[]
        
        for nx in range(len(axarr)): #create series for each plot
            serries_nx = []
            for i in range(self.MAX_NUM_SERIES): 
                ss = axarr[nx].plot([], [], label='', picker=5)
                serries_nx.append(ss[0])
            self.series.append(serries_nx)

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
        