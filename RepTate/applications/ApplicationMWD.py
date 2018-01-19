# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module ApplicationMWD

Module for handling Molecular weight distributions from GPC experiments.

""" 
from CmdBase import CmdBase, CmdMode
from Application import Application
from QApplicationWindow import QApplicationWindow
from View import View
from FileType import TXTColumnFile
import numpy as np
# from TheoryDiscrMWD import TheoryDiscrMWD

class ApplicationMWD(CmdBase):
    """Application to analyze Molecular Weight distributions
    
    [description]
    """
    name="MWD"
    description="Experimental Molecular weight distributions"
    def __new__(cls, name="LVE", parent = None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"LVE"})
            parent {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUIApplicationMWD(name, parent) if (CmdBase.mode==CmdMode.GUI) else CLApplicationMWD(name, parent)

class BaseApplicationMWD:
    """[summary]
    
    [description]
    """
    
    def __init__(self, name="MWD", parent = None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"MWD"})
            parent {[type]} -- [description] (default: {None})
        """
        from TheoryDiscrMWD import TheoryDiscrMWD
        
        super().__init__(name, parent)
    
        # VIEWS
        self.views["W(M)"]=View(name="W(M)", description="Molecular weight distribution", x_label="M", y_label="W(M)", 
                                x_units="g/mol", y_units="-", log_x=True, log_y=False, view_proc=self.viewWM, n=1, 
                                snames=["W(M)"], index=0)
        self.views["LogW(M)"]=View(name="W(M)", description="Molecular weight distribution", x_label="log M", y_label="log W(M)", 
                                x_units="g/mol", y_units="-", log_x=False, log_y=False, view_proc=self.viewlogWM, n=1, 
                                snames=["W(M)"], index=1)

        #set multiviews
        self.multiviews = [self.views["W(M)"]] #default view order in multiplot views, set only one item for single view
        self.nplots = len(self.multiviews) 

        # FILES
        ftype=TXTColumnFile("GPC Files", "gpc", "Molecular Weight Distribution", ['M','W(logM)'], ['Mn','Mw','PDI'], ["g/mol", '-'])
        #ftype=TXTColumnFile("GPC Files", "gpc", "Molecular Weight Distribution", ['M','W(logM)'], [], ['kDa', '-'])
        self.filetypes[ftype.extension]=ftype
        ftype=TXTColumnFile("React Files", "reac", "Relaxation modulus", ['M','W(logM)', 'g', 'br/1000C'], ['Mn','Mw','PDI'], ["g/mol", '-'])
        self.filetypes[ftype.extension]=ftype

        # THEORIES
        self.theories[TheoryDiscrMWD.thname] = TheoryDiscrMWD
        #self.theories[TheoryMaxwellModesTime.thname]=TheoryMaxwellModesTime

        #set the current view
        self.set_views()

    def viewWM(self, dt, file_parameters):
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
        y[:, 0] = dt.data[:, 1]
        return x, y, True

    def viewlogWM(self, dt, file_parameters):
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

class CLApplicationMWD(BaseApplicationMWD, Application):
    """[summary]
    
    [description]
    """
    def __init__(self, name="MWD", parent = None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"MWD"})
            parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)

class GUIApplicationMWD(BaseApplicationMWD, QApplicationWindow):
    """[summary]
    
    [description]
    """
    def __init__(self, name="MWD", parent = None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"MWD"})
            parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)

