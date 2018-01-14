# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module ApplicationNLVE

Module for handling data from start up of shear and extensional flow experiments.

""" 
from CmdBase import CmdBase, CmdMode
from Application import Application
from QApplicationWindow import QApplicationWindow
from View import View
from FileType import TXTColumnFile
import numpy as np
from TheoryRoliePoly import TheoryRoliePoly

class ApplicationNLVE(CmdBase):
    """Application to Analyze Start up of Non Linear flow
    
    [description]
    """
    name = "NLVE"
    description = "Non-Linear Flow"

    def __new__(cls, name="NLVE", parent = None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"NLVE"})
            parent {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUIApplicationNLVE(name, parent) if (CmdBase.mode==CmdMode.GUI) else CLApplicationNLVE(name, parent)

class BaseApplicationNLVE:
    """[summary]
    
    [description]
    """    
    def __init__(self, name="NLVE", parent = None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"LVE"})
            parent {[type]} -- [description] (default: {None})
        """
        from TheoryRoliePoly import TheoryRoliePoly

        super().__init__(name, parent)
        
        # VIEWS
        self.views["log(eta(t))"]=View(name="log(eta(t))", description="log transient viscosity", 
                                       x_label="log(t)", y_label="log($\eta$(t))", x_units="s", y_units="Pa$\cdot$s",
                                       log_x=False, log_y=False, view_proc=self.viewLogeta, n=1, snames=["$\eta$(t)"], index=0)
        self.views["log(sigma(t))-gamma"]=View(name="log(sigma(t))", description="log transient shear stress vs gamma", 
                                         x_label="log($\gamma$)", y_label="log($\sigma_{xy}$($\gamma$))", 
                                         x_units="-", y_units="Pa", log_x=False, log_y=False, view_proc=self.viewLogSigmaGamma, 
                                         n=1, snames=["$\sigma_{xy}$($\gamma$)"], index=1)
        self.views["log(sigma(t))-t"]=View(name="log(sigma(t))", description="log transient shear stress vs time", 
                                         x_label="log(t)", y_label="log($\sigma_{xy}$(t))", 
                                         x_units="s", y_units="Pa", log_x=False, log_y=False, view_proc=self.viewLogSigmaTime, 
                                         n=1, snames=["$\sigma_{xy}$($\gamma$)"], index=2)
        
        #set multiviews
        self.multiviews = [self.views["log(eta(t))"]] #default view order in multiplot views, set only one item for single view
        self.nplots = len(self.multiviews) 

        # FILES
        ftype=TXTColumnFile("Start-up of shear flow", "shear", "Shear flow files", ['t','eta'], ['gdot','T'], ['s','Pa$\cdot$s'])
        self.filetypes[ftype.extension]=ftype

        # THEORIES
        self.theories[TheoryRoliePoly.thname]=TheoryRoliePoly

    def viewLogeta(self, dt, file_parameters):
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
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 1]/float(file_parameters["gdot"]))    
        return x, y, True

    def viewLogSigmaTime(self, dt, file_parameters):
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
        x[:, 0] = np.log10(dt.data[:, 0]) 
        y[:, 0] = np.log10(dt.data[:, 1]) 
        return x, y, True

    def viewLogSigmaGamma(self, dt, file_parameters):
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
        x[:, 0] = np.log10(dt.data[:, 0]*float(file_parameters["gdot"])) #compute strain
        y[:, 0] = np.log10(dt.data[:, 1]) 
        return x, y, True

class CLApplicationNLVE(BaseApplicationNLVE, Application):
    """[summary]
    
    [description]
    """
    def __init__(self, name="NLVE", parent = None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"LVE"})
            parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)
        

class GUIApplicationNLVE(BaseApplicationNLVE, QApplicationWindow):
    """[summary]
    
    [description]
    """
    def __init__(self, name="NLVE", parent = None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"LVE"})
            parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)

        self.populate_views() #populate the view ComboBox
