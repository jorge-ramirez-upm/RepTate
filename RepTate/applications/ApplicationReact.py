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
"""Module ApplicationReact

React module

"""
from CmdBase import CmdBase, CmdMode
from Application import Application
from QApplicationWindow import QApplicationWindow
from View import View
from FileType import TXTColumnFile
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class ApplicationReact(CmdBase):
    """[summary]
    
    [description]
    """
    name = 'React'
    description = 'React Application'  #used in the command-line Reptate
    extension = 'reac'

    def __new__(cls, name='React', parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'React'})
            - parent {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUIApplicationReact(
            name,
            parent) if (CmdBase.mode == CmdMode.GUI) else CLApplicationReact(
                name, parent)


class BaseApplicationReact:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/en/latest/manual/Applications/React/React.html'

    def __init__(self, name='React', parent=None, **kwargs):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'React'})
            - parent {[type]} -- [description] (default: {None})
        """
        from TheoryLDPEBatch import TheoryTobitaBatch
        from TheoryTobitaCSTR import TheoryTobitaCSTR
        from TheoryMultiMetCSTR import TheoryMultiMetCSTR
        from TheoryReactMix import TheoryReactMix

        super().__init__(
            name, parent, nplots=3,
            ncols=2)  # will call Application.__init__ with these args

        # VIEWS
        # set the views that can be selected in the view combobox
        self.views["w(M)"] = View(
            name="w(M)",
            description="Molecular weight distribution",
            x_label="M",
            y_label="w(M)",
            x_units="g/mol",
            y_units="-",
            log_x=True,
            log_y=False,
            view_proc=self.view_wM,
            n=1,
            snames=["w(M)"])
        self.views["log(w(M))"] = View(
            name="log(w(M))",
            description="Molecular weight distribution",
            x_label="M",
            y_label="log w(M)",
            x_units="g/mol",
            y_units="-",
            log_x=True,
            log_y=False,
            view_proc=self.view_logwM,
            n=1,
            snames=["w(M)"])
        self.views["g(M)"] = View(
            name="g(M)",
            description="g(M)",
            x_label="M",
            y_label="g(M)",
            x_units="g/mol",
            y_units="-",
            log_x=True,
            log_y=False,
            view_proc=self.view_gM,
            n=1,
            snames=["g(M)"])
        self.views["log(g(M))"] = View(
            name="log(g(M))",
            description="log(g(M))",
            x_label="M",
            y_label="log g(M)",
            x_units="g/mol",
            y_units="-",
            log_x=True,
            log_y=False,
            view_proc=self.view_loggM,
            n=1,
            snames=["g(M)"])
        self.views['br/1000C'] = View(
            name="br/1000C",
            description="br/1000C(M)",
            x_label="M",
            y_label="br/1000C(M)",
            x_units="g/mol",
            y_units="-",
            log_x=True,
            log_y=False,
            view_proc=self.view_br_1000C,
            n=1,
            snames=["br/1000C(M)"])

        #set multiviews
        self.multiviews = [
            self.views["w(M)"], self.views["g(M)"], self.views['br/1000C']
        ]  #default view order in multiplot views
        self.nplots = len(self.multiviews)

        # FILES
        # set the type of files that ApplicationReact can open
        ftype = TXTColumnFile(
            name='React files',
            extension='reac',
            description='Reatc file',
            col_names=['M', 'w(M)', 'g', 'br/1000C'],
            basic_file_parameters=[],
            col_units=['g/mol', '-', '-', '-'])
        self.filetypes[
            ftype.extension] = ftype  #add each the file type to dictionary

        # THEORIES
        # add the theories related to ApplicationReact to the dictionary, e.g.:
        self.theories[TheoryTobitaBatch.thname] = TheoryTobitaBatch
        self.theories[TheoryTobitaCSTR.thname] = TheoryTobitaCSTR
        self.theories[TheoryMultiMetCSTR.thname] = TheoryMultiMetCSTR
        self.theories[TheoryReactMix.thname] = TheoryReactMix
        self.add_common_theories()

        #set the current view
        self.set_views()

    def view_wM(self, dt, file_parameters):
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

    def view_logwM(self, dt, file_parameters):
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
        y[:, 0] = np.log10(dt.data[:, 1])
        return x, y, True

    def view_gM(self, dt, file_parameters):
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
        y[:, 0] = dt.data[:, 2]
        return x, y, True

    def view_loggM(self, dt, file_parameters):
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
        y[:, 0] = np.log10(dt.data[:, 2])
        return x, y, True

    def view_br_1000C(self, dt, file_parameters):
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
        y[:, 0] = dt.data[:, 3]
        return x, y, True


class CLApplicationReact(BaseApplicationReact, Application):
    """[summary]
    
    [description]
    """

    def __init__(self, name='React', parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'React'})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)
        #usually this class stays empty


class GUIApplicationReact(BaseApplicationReact, QApplicationWindow):
    """[summary]
    
    [description]
    """

    def __init__(self, name='React', parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'React'})
            - parent {[type]} -- [description] (default: {None})
        """

        super().__init__(name, parent)

        #add the GUI-specific objects here:
