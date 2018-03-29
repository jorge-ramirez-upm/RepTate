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
"""Module ApplicationCreep

Module for the analysis of data from Creep experiments

"""
from CmdBase import CmdBase, CmdMode
from Application import Application
from QApplicationWindow import QApplicationWindow
from View import View
from FileType import TXTColumnFile
import numpy as np


class ApplicationCreep(CmdBase):
    """Application to Analyze Data from Creep experiments
    
    [description]
    """
    name = "Creep"
    description = "Creep Experiments"
    extension = "creep"

    def __new__(cls, name="Creep", parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"Creep"})
            - parent {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUIApplicationCreep(
            name,
            parent) if (CmdBase.mode == CmdMode.GUI) else CLApplicationCreep(
                name, parent)


class BaseApplicationCreep:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/en/latest/manual/Applications/Creep/Creep.html'

    def __init__(self, name="Creep", parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"Creep"})
            - parent {[type]} -- [description] (default: {None})
        """
        from TheoryRetardationModes import TheoryRetardationModesTime
        super().__init__(name, parent)

        # VIEWS
        self.views["log(gamma(t))"] = View(
            name="log(gamma(t))",
            description="log strain",
            x_label="log(t)",
            y_label="log($\gamma$(t))",
            x_units="s",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogStraint,
            n=1,
            snames=["gamma(t)"])
        self.views["gamma(t)"] = View(
            name="gamma(t)",
            description="strain",
            x_label="t",
            y_label="$\gamma$(t)",
            x_units="s",
            y_units="-",
            log_x=True,
            log_y=True,
            view_proc=self.viewStraint,
            n=1, 
            snames=["gamma(t)"])
        self.views["log(J(t))"] = View(
            name="log(J(t))",
            description="creep compliance",
            x_label="log(t)",
            y_label="log(J(t))",
            x_units="s",
            y_units="$\mathrm{Pa}^{-1}$",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogJt,
            n=1, 
            snames=["J(t)"])
        self.views["J(t)"] = View(
            name="J(t)",
            description="creep compliance",
            x_label="t",
            y_label="J(t)",
            x_units="s",
            y_units="$\mathrm{Pa}^{-1}$",
            log_x=True,
            log_y=True,
            view_proc=self.viewJt,
            n=1, 
            snames=["J(t)"])
        self.views["t/J(t)"] = View(
            name="t/J(t)",
            description="t/creep compliance",
            x_label="t",
            y_label="t/J(t)",
            x_units="s",
            y_units="Pa.s",
            log_x=True,
            log_y=True,
            view_proc=self.viewt_Jt,
            n=1, 
            snames=["t/J(t)"])

        #set multiviews
        self.multiviews = [
            self.views["log(gamma(t))"]
        ]  #default view order in multiplot views, set only one item for single view
        self.nplots = len(self.multiviews)

        # FILES
        ftype = TXTColumnFile("Creep files", "creep", "Creep files",
                              ['t', 'strain'], ['stress', 'Mw', 'T'],
                              ['s', '-', 'Pa', 'C'])
        self.filetypes[ftype.extension] = ftype

        # THEORIES
        self.theories[
            TheoryRetardationModesTime.thname] = TheoryRetardationModesTime
        self.add_common_theories()

        #set the current view
        self.set_views()

    def viewLogStraint(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(np.abs(dt.data[:, 1]))
        return x, y, True

    def viewStraint(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True

    def viewLogJt(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        sigma = float(file_parameters['stress'])
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(np.abs(dt.data[:, 1])/sigma)
        return x, y, True

    def viewJt(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        sigma = float(file_parameters['stress'])
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]/sigma
        return x, y, True

    def viewt_Jt(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        sigma = float(file_parameters['stress'])
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 0]/dt.data[:, 1]*sigma
        return x, y, True

class CLApplicationCreep(BaseApplicationCreep, Application):
    """[summary]
    
    [description]
    """

    def __init__(self, name="Creep", parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"Creep"})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)


class GUIApplicationCreep(BaseApplicationCreep, QApplicationWindow):
    """[summary]
    
    [description]
    """

    def __init__(self, name="Creep", parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"Creep"})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)
