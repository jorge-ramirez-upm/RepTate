# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module TheoryBasic

Module that defines the basic theories that should be available for all Applications.

""" 
from CmdBase import CmdBase
from Theory import Theory
import numpy as np

class TheoryPolynomial(Theory, CmdBase):
    """Fit a polynomial of degree n to the data
    
    :math:`ax^2 + bx + c`
    """
    thname = "Polynomial"
    description = "Fit a polynomial of degree n"

    def __init__(self, name="Polynomial", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"Polynomial"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super(TheoryPolynomial, self).__init__(name, parent_dataset, ax)
        self.function = self.polynomial
        self.parameters["n"] = Parameter("n", 1.0, "Degree of Polynomial", ParameterType.integer, opt_type=OptType.const)
        for i in range(self.parameters["n"].value+1):
            self.parameters["A%d"%i] = Parameter("A%d"%i,1.0,"Coefficient order %d"%i, ParameterType.real, opt_type=OptType.opt)

    def set_param_value(self, name, value):
        """[summary]
        
        [description]
        
        Arguments:
            name {[type]} -- [description]
            value {[type]} -- [description]
        """
        if (name=="n"):
            oldn=self.parameters["n"].value
        super(TheoryPolynomial, self).set_param_value(name, value)
        if (name=="n"):
            for i in range(self.parameters["n"].value+1):
                self.parameters["A%d"%i] = Parameter("A%d"%i,1.0,"Coefficient order %d"%i, ParameterType.real, opt_type=OptType.opt)
            if (oldn>self.parameters["n"].value):
                for i in range(self.parameters["n"].value+1,oldn+1):
                    del self.parameters["A%d"%i]

    def polynomial(self, f=None):
        """Actual polynomial function.
        
        .. math:: 
        
            (a + b)^2  &=  (a + b)(a + b) \\
              &=  a^2 + 2ab + b^2
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:,0] = ft.data[:,0]
        for c in range(1, tt.num_columns):
            for i in range(self.parameters["n"].value+1):
                tt.data[:,c]+=self.parameters["A%d"%i].value*tt.data[:,0]**i

class TheoryPowerLaw(Theory, CmdBase):
    """Fit a power law to the data
    
    [description]
    """
    thname = "PowerLaw"
    description = "Fit a power law A*x^b to the data"

    def __init__(self, name="PowerLaw", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"PowerLaw"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super(TheoryPowerLaw, self).__init__(name, parent_dataset, ax)
        self.function = self.powerlaw
        self.parameters["A"] = Parameter("A", 1.0, "Prefactor", ParameterType.real, opt_type=OptType.opt)
        self.parameters["b"] = Parameter("b",1.0,"Exponent", ParameterType.real, opt_type=OptType.opt)

    def powerlaw(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:,0] = ft.data[:,0]
        for c in range(1, tt.num_columns):
            tt.data[:,c] = self.parameters["A"].value*tt.data[:,0]**self.parameters["b"].value

class TheoryExponential(Theory, CmdBase):
    """Fit an exponential decay to the data
    
    [description]
    """
    thname="Exponential"
    description="Fit an exponential decay A*exp(-x/T) to the data"

    def __init__(self, name="Exponential", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"Exponential"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super(TheoryExponential, self).__init__(name, parent_dataset, ax)
        self.function = self.exponential
        self.parameters["A"] = Parameter("A", 1.0, "Prefactor", ParameterType.real, opt_type=OptType.opt)
        self.parameters["T"] = Parameter("T", 1.0, "Time", ParameterType.real, opt_type=OptType.opt)

    def exponential(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:,0] = ft.data[:,0]
        for c in range(1, tt.num_columns):
            tt.data[:,c] = self.parameters["A"].value*np.exp(-tt.data[:,0]/self.parameters["T"].value)

class TheoryExponential2(Theory, CmdBase):
    """Fit 2 exponentials decay to the data
    
    [description]
    """
    thname="Exponential2"
    description="Fit 2 exponentials decay A*exp(-x/T) to the data"

    def __init__(self, name="Exponential2", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"Exponential2"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super(TheoryExponential2, self).__init__(name, parent_dataset, ax)
        self.function = self.exponential2
        self.parameters["A1"] = Parameter("A1", 0.9, "Prefactor", ParameterType.real, opt_type=OptType.opt)
        self.parameters["T1"] = Parameter("T1",1.0,"Time", ParameterType.real, opt_type=OptType.opt)
        self.parameters["A2"] = Parameter("A2", 0.1, "Prefactor", ParameterType.real, opt_type=OptType.opt)
        self.parameters["T2"] = Parameter("T2",10.0,"Time", ParameterType.real, opt_type=OptType.opt)

    def exponential2(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:,0] = ft.data[:,0]
        for c in range(1, tt.num_columns):
            tt.data[:,c] = self.parameters["A1"].value*np.exp(-tt.data[:,0]/self.parameters["T1"].value)+self.parameters["A2"].value*np.exp(-tt.data[:,0]/self.parameters["T2"].value)
