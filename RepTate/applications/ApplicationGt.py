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
# Copyright (2017): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module ApplicationGt

Module for the analysis of stress relaxation data from simulations and experiments.

"""
from CmdBase import CmdBase, CmdMode
from Application import Application
from View import View
from FileType import TXTColumnFile
from QApplicationWindow import QApplicationWindow
import numpy as np
from scipy import interpolate

from schwarzl_ctypes_helper import *
from ctypes import *


class ApplicationGt(CmdBase):
    """Application to analyze the relaxation modulus
    
    [description]
    """
    name = "Gt"
    description = "Relaxation modulus"
    extension = "gt"

    def __new__(cls, name="Gt", parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"Gt"})
            parent {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUIApplicationGt(
            name,
            parent) if (CmdBase.mode == CmdMode.GUI) else CLApplicationGt(
                name, parent)


class BaseApplicationGt:
    """[summary]
    
    [description]
    """

    def __init__(self, name="Gt", parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"Gt"})
            parent {[type]} -- [description] (default: {None})
        """
        from TheoryMaxwellModes import TheoryMaxwellModesTime

        super().__init__(
            name, parent, nplots=2,
            ncols=2)  # will call Application.__init__ with these args

        # VIEWS
        self.views["log[G(t)]"] = View(
            name="log[G(t)]",
            description="log Relaxation modulus",
            x_label="log(t)",
            y_label="log(G(t))",
            x_units="s",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogGt,
            n=1,
            snames=["log(G(t))"])
        self.views["G(t)"] = View(
            name="G(t)",
            description="Relaxation modulus",
            x_label="t",
            y_label="G(t)",
            x_units="s",
            y_units="Pa",
            log_x=True,
            log_y=True,
            view_proc=self.viewGt,
            n=1,
            snames=["G(t)"])
        self.views["Schwarzl G',G''"] = View(
            name="Schwarzl G',G''",
            description="G', G'' from Schwarzl transformation of G(t)",
            x_label="$\omega$",
            y_label="G',G''",
            x_units="rad/s",
            y_units="Pa",
            log_x=True,
            log_y=True,
            view_proc=self.viewSchwarzl_Gt,
            n=2,
            snames=["G',G''"])
#        self.views["i-Rheo G',G''"] = View(
#            name="i-Rheo G',G''",
#            description="G', G'' from i-Rheo transformation of G(t)",
#            x_label="$\omega$",
#            y_label="G',G''",
#            x_units="rad/s",
#            y_units="Pa",
#            log_x=True,
#            log_y=True,
#            view_proc=self.viewiRheo,
#            n=2,
#            snames=["G',G''"])
        
            
        #set multiviews
        self.multiviews = [
            self.views["log[G(t)]"], self.views["Schwarzl G',G''"]
        ]  #default view order in multiplot views, set only one item for single view
        self.nplots = len(self.multiviews)

        # FILES
        ftype = TXTColumnFile("G(t) files", "gt", "Relaxation modulus",
                              ['t', 'Gt'], ['Mw', 'ncontri'], ['s', 'Pa'])
        self.filetypes[ftype.extension] = ftype

        # THEORIES
        self.theories[TheoryMaxwellModesTime.thname] = TheoryMaxwellModesTime
        self.add_common_theories()
        
        #set the current view
        self.set_views()

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
        y[:, 0] = dt.data[:, 1]
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
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 1])
        return x, y, True

    def viewSchwarzl_Gt(self, dt,
                        file_parameters):  #TODO: code the Schwarzl transform.
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

        wp, Gp, wpp, Gpp = do_schwarzl_gt(dt.num_rows, dt.data[:, 1],
                                          dt.data[:, 0])  #call the C function

        x[:, 0] = wp[:]
        x[:, 1] = wpp[:]
        y[:, 0] = Gp[:]
        y[:, 1] = Gpp[:]
        return x, y, True

    def viewiRheo (self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
        """
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        f = interpolate.interp1d(dt.data[:,0], dt.data[:,1], kind='cubic', assume_sorted=True, fill_value='extrapolate')
        g0 = f(0)
        ind1 = np.argmax(dt.data[:,0]>0)
        t1 = dt.data[ind1,0]
        g1 = dt.data[ind1,1]
        tinf = np.max(dt.data[:,0])
        wp = np.logspace(np.log10(1/tinf), np.log10(1/t1), dt.num_rows)
        x[:, 0] = wp[:]
        x[:, 1] = wp[:]

        coeff=(dt.data[ind1+1:,1]-dt.data[ind1:-1,1])/(dt.data[ind1+1:,0]-dt.data[ind1:-1,0])
        for i, w in enumerate(wp):
            y[i, 0]=((1-np.cos(w*t1))*(g1-g0)/t1+np.dot(coeff,np.cos(w*dt.data[ind1:-1,0])-np.cos(w*dt.data[ind1+1:,0])))/(-w*w)
            y[i, 1]=(w*g0+np.sin(w*t1)*(g1-g0)/t1+np.dot(coeff,-np.sin(w*dt.data[ind1:-1,0])+np.sin(w*dt.data[ind1+1:,0])))/(-w*w)
        
        return x, y, True
        

class CLApplicationGt(BaseApplicationGt, Application):
    """[summary]
    
    [description]
    """

    def __init__(self, name="Gt", parent=None):
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

    def __init__(self, name="Gt", parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"Gt"})
            parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)
