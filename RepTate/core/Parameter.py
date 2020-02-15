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
"""Module Parameter

Module that defines theory parameters and their properties.

""" 
import enum
import numpy as np

class ParameterType(enum.Enum):
    """Types of parameters that can be used in a Theory
    
    Parameters can be:
        - real: Any real number
        - integer: Any integer number
        - discrete_real: It can take a value only from a discrete set of prescribed real values
        - discrete_integer: It can take a value only from a discrete set of prescribed integer values
        - bool: The parameter is a flag
    """
    real = 0
    integer = 1
    discrete_real = 2
    discrete_integer = 3
    boolean = 4
    string = 5

class OptType(enum.Enum):
    """Store the optimization type that can be used in a Theory
    
    Parameters can be:
        - opt: Optimized at the next minimization
        - nopt: Not optimized at the next minimization
        - const: Not allowed to be minimized
    """
    opt = 1 
    nopt = 2
    const = 3 

class Parameter(object):
    """Abstract class to describe theory parameters
    
    [description]
    """
    def __init__(self, name="", value=0, description="", type=ParameterType.real, 
                 opt_type=OptType.opt, 
                 min_value=-np.inf, max_value=np.inf, 
                 display_flag=True, discrete_values=[]):
        """
        **Constructor**

        Arguments:
            - name {str} -- Parameter name
            - value {real} -- Value of parameter
            - description {str} -- Meaning of parameter
            - type {enum} -- Type of parameter (real, integer, discrete_real, discrete_integer)
            - opt_type {enum} -- Is this parameter optimized at the next minimization (opt, nopt, const)?
            - min_value {real} -- Minimum allowed value for the parameter
            - max_value {real} -- Maximum allowed value
            - display_flag {bool} -- This parameter will be shown in the Theory table
            - discrete_values {list} -- Allowed values that the parameter can take
        """
        self.name=name
        self.description=description
        self.type = type
        if (self.type==ParameterType.real):
            self.value=float(value)
        elif (self.type==ParameterType.integer):
            self.value=int(value)
        elif (self.type==ParameterType.discrete_real):
            self.value=float(value)
        elif (self.type==ParameterType.discrete_integer):
            self.value=int(value)
        elif (self.type==ParameterType.boolean):
            if value in [True, 'true', 'True', '1', 't', 'T', 'y', 'yes']:
                self.value=True
            else:
                self.value=False
        elif (self.type==ParameterType.string):
            self.value=str(value)

        else:
            pass # NOT IMPLEMENTED YET
        self.error=np.inf
        self.opt_type = opt_type
        self.min_value = min_value
        self.max_value= max_value
        self.display_flag = display_flag
        self.discrete_values = discrete_values

    def copy(self, par2):
        """Copy the contents of another parameter
        
        [description]
        
        Arguments:
            - par2 {[type]} -- [description]
        """
        self.name=par2.name
        self.description=par2.description
        self.type = par2.type
        self.value=par2.value
        self.opt_type = par2.opt_type
        self.min_value = par2.min_value
        self.max_value= par2.max_value
        
    def __str__(self):
        """[summary]
        
        [description]
        
        Returns:
            - [type] -- [description]

        .. todo:: Refine this.
        """
        return "%s=%g"%(self.name,self.value)

    def __repr__(self):
        """[summary]
        
        [description]
        
        Returns:
            - [type] -- [description]

        .. todo:: Refine this.
        """
        return "Parameter(\"%s\",%g,\"%s\",%s,%s,%g,%s,%s,%g,%g,%s)"%(
            self.name, self.value, self.description, self.type, 
            self.opt_type, 
            self.min_value, self.max_value, self.display_flag)
