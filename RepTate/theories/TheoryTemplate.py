# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License.
"""Module TheoryTemplate

Template file for creating a new theory
"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable


class TheoryTemplate(CmdBase):
    """[summary]
    
    [description]
    """
    thname = 'TemplateTheory'
    description = 'Template Theory'
    citations = ''

    def __new__(cls, name='ThTemplate', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTemplate'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryTemplate(
            name, parent_dataset,
            axarr) if (CmdBase.mode == CmdMode.GUI) else CLTheoryTemplate(
                name, parent_dataset, axarr)


class BaseTheoryTemplate:
    """[summary]
    
    [description]
    """
    single_file = False  # False if the theory can be applied to multiple files simultaneously

    def __init__(self, name='ThTemplate', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTemplate'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.function_template  # main theory function
        self.has_modes = False  # True if the theory has modes
        self.parameters['param1'] = Parameter(
            name='param1',
            value=1,
            description='parameter 1',
            type=ParameterType.real,
            opt_type=OptType.const)

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
        """Template function that returns the square of y
        
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


class CLTheoryTemplate(BaseTheoryTemplate, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='ThTemplate', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTemplate'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # This class usually stays empty


class GUITheoryTemplate(BaseTheoryTemplate, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='ThTemplate', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThTemplate'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # add widgets specific to the theory here:
