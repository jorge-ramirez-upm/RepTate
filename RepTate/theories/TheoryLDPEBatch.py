# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Daniel Read, d.j.read@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module TheoryTobitaBatch

TobitaBatch file for creating a new theory
""" 
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable


class TheoryTobitaBatch(CmdBase):
    """Rolie-Poly
    
    [description]
    """
    thname='TobitaBatchTheory'
    description='TobitaBatch Theory'
    citations=''

    def __new__(cls, name='ThTobitaBatch', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTobitaBatch'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryTobitaBatch(name, parent_dataset, ax) if (CmdBase.mode==CmdMode.GUI) else CLTheoryTobitaBatch(name, parent_dataset, ax)


class BaseTheoryTobitaBatch:
    """[summary]
    
    [description]
    """
    single_file = False # True if the theory can be applied to multiple files simultaneously

    def __init__(self, name='ThTobitaBatch', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTobitaBatch'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.function_template # main theory function
        self.has_modes = False # True if the theory has modes
        self.parameters['param1'] = Parameter(name='param1', value=1, description='parameter 1', 
                                          type=ParameterType.real, opt_type=OptType.const)
                



    def get_modes(self):
        """[summary]
        
        [description]
        
        Returns:
            [type] -- [description]
        """
        pass

    def set_modes(self):
        """[summary]
        
        [description]
        
        Arguments:

        """
        pass
        
    def function_template(self, f=None):
        """TobitaBatch function that returns the square of y
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        tt.data[:, 1] = ft.data[:, 1] * ft.data[:, 1]


class CLTheoryTobitaBatch(BaseTheoryTobitaBatch, Theory):
    """[summary]
    
    [description]
    """
    def __init__(self, name='ThTobitaBatch', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTobitaBatch'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
   
    # This class usually stays empty


class GUITheoryTobitaBatch(BaseTheoryTobitaBatch, QTheory):
    """[summary]
    
    [description]
    """
    def __init__(self, name='ThTobitaBatch', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTobitaBatch'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)

    # add widgets specific to the theory here:
       