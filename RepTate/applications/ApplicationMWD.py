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
"""Module ApplicationMWD

Module for handling Molecular weight distributions from GPC experiments.

"""
from CmdBase import CmdBase, CmdMode
from Application import Application
from QApplicationWindow import QApplicationWindow
from View import View
from FileType import TXTColumnFile
import numpy as np


class ApplicationMWD(CmdBase):
    """Application to analyze Molecular Weight Distributions
    
    """
    name = "MWD"
    description = "Experimental Molecular weight distributions"
    extension = "gpc"

    def __new__(cls, name="LVE", parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"LVE"})
            - parent {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUIApplicationMWD(
            name,
            parent) if (CmdBase.mode == CmdMode.GUI) else CLApplicationMWD(
                name, parent)


class BaseApplicationMWD:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/en/latest/manual/Applications/MWD/MWD.html'

    def __init__(self, name="MWD", parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"MWD"})
            - parent {[type]} -- [description] (default: {None})
        """
        from TheoryDiscrMWD import TheoryDiscrMWD
        from TheoryGEX import TheoryGEX
        from TheoryLogNormal import TheoryLogNormal

        super().__init__(name, parent)

        # VIEWS
        self.views["log-lin"] = View(
            name="log-lin",
            description="Molecular weight distribution",
            x_label="M",
            y_label="W(M)",
            x_units="g/mol",
            y_units="-",
            log_x=True,
            log_y=False,
            view_proc=self.view_WM,
            n=1,
            snames=["W(M)"])
        self.views["log-log"] = View(
            name="log-log",
            description="Molecular weight distribution",
            x_label="log(M)",
            y_label="log(W(M))",
            x_units="g/mol",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.view_logWM,
            n=1,
            snames=["W(M)"])
        self.views["lin-lin"] = View(
            name="lin-lin",
            description="Molecular weight distribution",
            x_label="M",
            y_label="W(M)",
            x_units="g/mol",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.view_WM,
            n=1,
            snames=["W(M)"])

        #set multiviews
        self.multiviews = [
            self.views["log-lin"]
        ]  #default view order in multiplot views, set only one item for single view
        self.nplots = len(self.multiviews)

        # FILES
        ftype = TXTColumnFile(
            "GPC Files", "gpc", "Molecular Weight Distribution",
            ['M', 'W(logM)'], ['Mn', 'Mw', 'PDI'], ["g/mol", '-'])
        #ftype=TXTColumnFile("GPC Files", "gpc", "Molecular Weight Distribution", ['M','W(logM)'], [], ['kDa', '-'])
        self.filetypes[ftype.extension] = ftype
        ftype = TXTColumnFile("React Files", "reac", "Relaxation modulus",
                              ['M', 'W(logM)', 'g', 'br/1000C'],
                              ['Mn', 'Mw', 'PDI'], ["g/mol", '-'])
        self.filetypes[ftype.extension] = ftype

        # THEORIES
        self.theories[TheoryDiscrMWD.thname] = TheoryDiscrMWD
        self.theories[TheoryGEX.thname]=TheoryGEX
        self.theories[TheoryLogNormal.thname]=TheoryLogNormal
        self.add_common_theories()

        #set the current view
        self.set_views()

    def view_WM(self, dt, file_parameters):
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
        
    def view_logWM(self, dt, file_parameters):
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

class CLApplicationMWD(BaseApplicationMWD, Application):
    """[summary]
    
    [description]
    """

    def __init__(self, name="MWD", parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"MWD"})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)


class GUIApplicationMWD(BaseApplicationMWD, QApplicationWindow):
    """[summary]
    
    [description]
    """

    def __init__(self, name="MWD", parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"MWD"})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)
