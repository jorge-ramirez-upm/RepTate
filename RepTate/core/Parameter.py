# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module Parameter

Module that defines theory parameters and their properties.

""" 
import enum
import math

class ShiftType(enum.Enum):
    """[summary]
    
    [description]
    """
    linear=0
    log=1

class ParameterType(enum.Enum):
    """[summary]
    
    [description]
    """
    real = 0
    integer = 1
    discrete = 2

class Parameter(object):
    """Abstract class to describe theory parameters
    
    [description]
    """
    def __init__(self, name="", value=0.0, description="", type=ParameterType.real, 
                 min_flag=True, min_factor=1.0, min_shift_type=ShiftType.linear, 
                 bracketed = False, min_value=-math.inf, max_value=math.inf):
        """Constructor
        
        [description]

        Arguments:
            name {str} -- Parameter name
            description {str} -- Meaning of parameter
            type {enum} -- Type of parameter (real, integer, discrete)
            value {real} -- Value of parameter
            min_flag {bool} -- Is this parameter optimized?
            min_factor {real} -- Factor to scale this parameter during minimization
            min_shift_type {user} -- How do we shift this parameter during minimization
            bracketed {bool} -- Is the parameter bracketed?
            min_value {real} -- Minimum allowed value for the parameter
            max_value {real} -- Maximum allowed value        
        """
        self.name=name
        self.description=description
        self.type = type
        if (self.type==ParameterType.real):
            self.value=float(value)
        elif (self.type==ParameterType.integer):
            self.value=int(value)
        else:
            pass # NOT IMPLEMENTED YET
        self.error=math.inf
        self.min_flag = min_flag
        self.min_factor = min_factor
        self.min_shift_type = min_shift_type
        self.bracketed = bracketed
        self.min_value = min_value
        self.max_value= max_value
        self.min_allowed = min_flag

    def copy(self, par2):
        """Copy the contents of another parameter
        
        [description]
        
        Arguments:
            par2 {[type]} -- [description]
        """
        self.name=par2.name
        self.description=par2.description
        self.type = par2.type
        self.value=par2.value
        self.min_flag = par2.min_flag
        self.min_factor = par2.min_factor
        self.min_shift_type = par2.min_shift_type
        self.bracketed = par2.bracketed
        self.min_value = par2.min_value
        self.max_value= par2.max_value
        
    def __str__(self):
        """[summary]
        
        [description]
        
        Returns:
            [type] -- [description]

        .. todo:: Refine this.
        """
        return "%s=%g"%(self.name,self.value)

    def __repr__(self):
        """[summary]
        
        [description]
        
        Returns:
            [type] -- [description]

        .. todo:: Refine this.
        """
        return "Parameter(\"%s\",%g,\"%s\",%s,%s,%g,%s,%s,%g,%g)"%(self.name,self.value,self.description, self.type, self.min_flag,\
                self.min_factor, self.min_shift_type, self.bracketed, self.min_value, self.max_value)
