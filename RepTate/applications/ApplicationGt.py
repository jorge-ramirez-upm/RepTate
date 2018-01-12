# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License.
"""Module ApplicationGt

Module for the analysis of stress relaxation data from simulations and experiments.

"""
from CmdBase import CmdBase, CmdMode
from Application import Application
from View import View
from FileType import TXTColumnFile
from QApplicationWindow import QApplicationWindow
import numpy as np

from schwarzl_ctypes_helper import *
from ctypes import *

# from TheoryMaxwellModes import TheoryMaxwellModesTime

class ApplicationGt(CmdBase):
    """Application to analyze the relaxation modulus
    
    [description]
    """
    name="Gt"
    description="Relaxation modulus"
    
    def __new__(cls, name="Gt", parent = None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"Gt"})
            parent {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUIApplicationGt(name, parent) if (CmdBase.mode==CmdMode.GUI) else CLApplicationGt(name, parent)

class BaseApplicationGt:
    """[summary]
    
    [description]
    """
    def __init__(self, name = "Gt", parent = None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"Gt"})
            parent {[type]} -- [description] (default: {None})
        """
        from TheoryMaxwellModes import TheoryMaxwellModesTime

        super().__init__(name, parent, nplots=3, ncols=2) # will call Application.__init__ with these args

        # VIEWS
        self.views["log[G(t)]"]=View(name="log[G(t)]", description="log Relaxation modulus", x_label="log(t)", 
                                     y_label="log(G(t))", x_units="s", y_units="Pa", log_x=False, log_y=False, 
                                     view_proc=self.viewLogGt, n=1, snames=["log(G(t))"], index=0)
        self.views["G(t)"]=View(name="G(t)", description="Relaxation modulus", x_label="t", y_label="G(t)", 
                                x_units="s", y_units="Pa", log_x=True, log_y=True, view_proc=self.viewGt, 
                                n=1, snames=["G(t)"], index=1)
        self.views["Schwarzl G',G''"]=View(name="Schwarzl G',G''", description="G', G'' from Schwarzl transformation of G(t)", x_label="$\omega$", y_label="G',G''", 
                                x_units="rad/s", y_units="Pa", log_x=True, log_y=True, view_proc=self.viewSchwarzl_Gt, 
                                n=2, snames=["G',G''"], index=2)


        #set multiviews
        self.multiviews = [self.views["log[G(t)]"], self.views["G(t)"], self.views["G',G''"]] #default view order in multiplot views, set only one item for single view
        self.nplots = len(self.multiviews) 

        # FILES
        ftype=TXTColumnFile("G(t) files", "gt", "Relaxation modulus", ['t','Gt'], ['Mw','ncontri'], ['s', 'Pa'])
        self.filetypes[ftype.extension]=ftype

        # THEORIES
        self.theories[TheoryMaxwellModesTime.thname]=TheoryMaxwellModesTime

    def viewGt(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            dt {[type]} -- [description]
            file_parameters {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[: ,0] = dt.data[:, 1]
        return x, y, True

    def viewLogGt(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            dt {[type]} -- [description]
            file_parameters {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        #validindex = np.logical_and(dt.data[:, 0]>0, dt.data[:, 1]>0)
        #x = np.zeros((np.sum(validindex), 1))
        #y = np.zeros((np.sum(validindex), 1))
        #x[:, 0] = np.log10(dt.data[validindex, 0])
        #y[:, 0] = np.log10(dt.data[validindex, 1])
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[: ,0] = dt.data[:, 1]
        return x, y, True

    def viewSchwarzl_Gt(self, dt, file_parameters): #TODO: code the Schwarzl transform. 
        """[summary]
        
        [description]
        
        Arguments:
            dt {[type]} -- [description]
            file_parameters {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))

        wp, Gp, wpp, Gpp = do_schwarzl_gt(dt.num_rows, dt.data[:, 1], dt.data[:, 0]) #call the C function

        x[:, 0] = wp[:]
        x[:, 1] = wpp[:]
        y[: ,0] = Gp[:]
        y[: ,1] = Gpp[:]
        return x, y, True

class CLApplicationGt(BaseApplicationGt, Application):
    """[summary]
    
    [description]
    """
    def __init__(self, name="Gt", parent = None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"Gt"})
            parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)
        

class GUIApplicationGt(BaseApplicationGt, QApplicationWindow):
    """[summary]
    
    [description]
    """
    def __init__(self, name="Gt", parent = None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"Gt"})
            parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)

        self.populate_views() #populate the view ComboBox
