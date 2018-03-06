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
"""Module ApplicationNLVE

Module for handling data from start up of shear and extensional flow experiments.

"""
from CmdBase import CmdBase, CmdMode
from Application import Application
from QApplicationWindow import QApplicationWindow
from View import View
from FileType import TXTColumnFile
import numpy as np


class ApplicationNLVE(CmdBase):
    """Application to Analyze Start up of Non Linear flow
    
    [description]
    """
    name = "NLVE"
    description = "Non-Linear Flow"
    extension = "shear"

    def __new__(cls, name="NLVE", parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"NLVE"})
            - parent {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUIApplicationNLVE(
            name,
            parent) if (CmdBase.mode == CmdMode.GUI) else CLApplicationNLVE(
                name, parent)


class BaseApplicationNLVE:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/en/latest/manual/Applications/NLVE/NLVE.html'

    def __init__(self, name="NLVE", parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"LVE"})
            - parent {[type]} -- [description] (default: {None})
        """
        from TheoryRoliePoly import TheoryRoliePoly
        from TheoryUCM import TheoryUCM
        from TheoryGiesekus import TheoryGiesekus
        from TheoryPomPom import TheoryPomPom

        super().__init__(name, parent)

        # VIEWS
        self.views["log(eta(t))"] = View(
            name="log(eta(t))",
            description="log transient viscosity",
            x_label="log(t)",
            y_label="log($\eta$(t))",
            x_units="s",
            y_units="Pa$\cdot$s",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogeta,
            n=1,
            snames=["$\eta$(t)"])
        self.views["log(sigma(t))-gamma"] = View(
            name="log(sigma(t))",
            description="log transient shear stress vs gamma",
            x_label="log($\gamma$)",
            y_label="log($\sigma_{xy}$($\gamma$))",
            x_units="-",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogSigmaGamma,
            n=1,
            snames=["$\sigma_{xy}$($\gamma$)"])
        self.views["log(sigma(t))-t"] = View(
            name="log(sigma(t))",
            description="log transient shear stress vs time",
            x_label="log(t)",
            y_label="log($\sigma_{xy}$(t))",
            x_units="s",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogSigmaTime,
            n=1,
            snames=["$\sigma_{xy}$($\gamma$)"])

        #set multiviews
        self.multiviews = [
            self.views["log(eta(t))"]
        ]  #default view order in multiplot views, set only one item for single view
        self.nplots = len(self.multiviews)

        # FILES
        ftype = TXTColumnFile("Start-up of shear flow", "shear",
                              "Shear flow files", ['t', 'sigma_xy'], ['gdot', 'T'],
                              ['s', 'Pa$\cdot$s'])
        self.filetypes[ftype.extension] = ftype
        ftype = TXTColumnFile("Elongation flow", "uext",
                              "Elongation flow files", ['t', 'N1'],
                              ['gdot', 'T'], ['s', 'Pa$\cdot$s'])
        self.filetypes[ftype.extension] = ftype

        # THEORIES
        self.theories[TheoryRoliePoly.thname] = TheoryRoliePoly
        self.theories[TheoryUCM.thname] = TheoryUCM
        self.theories[TheoryGiesekus.thname] = TheoryGiesekus
        self.theories[TheoryPomPom.thname] = TheoryPomPom
        self.add_common_theories()
        
        #set the current view
        self.set_views()

    def viewLogeta(self, dt, file_parameters):
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
        try:
            flow_rate = float(file_parameters["gdot"])
        except:
            flow_rate = float(file_parameters["edot"])
        y[:, 0] = np.log10(dt.data[:, 1] / flow_rate)
        return x, y, True

    def viewLogSigmaTime(self, dt, file_parameters):
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
        y[:, 0] = np.log10(dt.data[:, 1])
        return x, y, True

    def viewLogSigmaGamma(self, dt, file_parameters):
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
        try:
            flow_rate = float(file_parameters["gdot"])
        except:
            flow_rate = float(file_parameters["edot"])
        x[:, 0] = np.log10(dt.data[:, 0] * flow_rate)  #compute strain
        y[:, 0] = np.log10(dt.data[:, 1])
        return x, y, True


class CLApplicationNLVE(BaseApplicationNLVE, Application):
    """[summary]
    
    [description]
    """

    def __init__(self, name="NLVE", parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"LVE"})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)


class GUIApplicationNLVE(BaseApplicationNLVE, QApplicationWindow):
    """[summary]
    
    [description]
    """

    def __init__(self, name="NLVE", parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"LVE"})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)
