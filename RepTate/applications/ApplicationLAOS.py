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
"""Module ApplicationLAOS

Large Amplitude Oscillatory Shear

"""
from CmdBase import CmdBase, CmdMode
from Application import Application
from QApplicationWindow import QApplicationWindow
from View import View
from FileType import TXTColumnFile
import numpy as np


class ApplicationLAOS(CmdBase):
    """Application for ...
    
    [description]
    """
    appname = 'LAOS'
    description = 'LAOS Application'  #used in the command-line Reptate
    extension = "laos"  # drag and drop this extension automatically opens this application

    def __new__(cls, name='LAOS', parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'LAOS'})
            - parent {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUIApplicationLAOS(name, parent) if (
            CmdBase.mode == CmdMode.GUI) else CLApplicationLAOS(
                name, parent)


class BaseApplicationLAOS:
    """[summary]
    
    [description]
    """

    #help_file = ''
    appname = ApplicationLAOS.appname

    def __init__(self, name='LAOS', parent=None, **kwargs):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'LAOS'})
            - parent {[type]} -- [description] (default: {None})
        """
        # IMPORT THEORIES
        # Import theories specific to the Application e.g.:
        # from TheoryLAOS import TheoryA

        super().__init__(name, parent)

        # VIEWS
        # set the views that can be selected in the view combobox
        self.views['sigma(gamma)'] = View(
            name='sigma(gamma)',
            description='Stress as a function of strain',
            x_label='$\gamma(t)$',
            y_label='$\sigma(t)$',
            x_units='-',
            y_units='Pa',
            log_x=False,
            log_y=False,
            view_proc=self.view_sigmagamma,
            n=1,
            snames=['$\sigma(\gamma)$'])

        self.views['sigma(t),gamma(t)'] = View(
            name='sigma-gamma(t)',
            description='Stress and strain as a function of time',
            x_label='$t$',
            y_label='$\sigma(t),\gamma(t)$',
            x_units='s',
            y_units='Pa, -',
            log_x=False,
            log_y=False,
            view_proc=self.view_sigmatgammat,
            n=2,
            snames=['$\sigma(t)$', '$\gamma(t)$'])

        self.views['sigma(t)'] = View(
            name='sigma(t)',
            description='Stress as a function of time',
            x_label='$t$',
            y_label='$\sigma(t)$',
            x_units='s',
            y_units='Pa',
            log_x=False,
            log_y=False,
            view_proc=self.view_sigmat,
            n=1,
            snames=['$\sigma(t)$'])

        self.views['gamma(t)'] = View(
            name='gamma(t)',
            description='Strain as a function of time',
            x_label='$t$',
            y_label='$\gamma(t)$',
            x_units='s',
            y_units='-',
            log_x=False,
            log_y=False,
            view_proc=self.view_gammat,
            n=1,
            snames=['$\gamma(t)$'])

        #set multiviews
        #default view order in multiplot views, set only one item for single view
        #if more than one item, modify the 'nplots' in the super().__init__ call
        self.nplots = 4
        self.multiviews = []
        for i in range(self.nplot_max):
            # set views in the same order as declared above
            self.multiviews.append(list(self.views.values())[i])
        self.multiplots.reorg_fig(self.nplots)

        # FILES
        # set the type of files that ApplicationLAOS can open
        ftype = TXTColumnFile(
            name='Large-Angle Oscillatory Shear data',
            extension='laos',
            description='file containing laos data',
            col_names=['time', 'gamma', 'sigma'],
            basic_file_parameters=['omega', 'gamma'],
            col_units=['s','-', 'Pa'])
        self.filetypes[
            ftype.extension] = ftype  #add each the file type to dictionary

        # THEORIES
        # add the theories related to ApplicationLAOS to the dictionary, e.g.:
        # self.theories[TheoryA.thname] = TheoryA
        # self.theories[TheoryB.thname] = TheoryB
        self.add_common_theories()  # Add basic theories to the application

        #set the current view
        self.set_views()

    def view_sigmagamma(self, dt, file_parameters):
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
        x[:, 0] = dt.data[:, 1]
        y[:, 0] = dt.data[:, 2]
        return x, y, True

    def view_sigmat(self, dt, file_parameters):
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

        # If times==0, set time column using the index
        # if (np.max(x)==0):
        #     x[:, 0] = np.linspace(1, dt.num_rows, dt.num_rows)
        return x, y, True

    def view_gammat(self, dt, file_parameters):
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
        # If times==0, set time column using the index
        # if (np.max(x)==0):
        #     x[:, 0] = np.linspace(1, dt.num_rows, dt.num_rows)
        return x, y, True

    def view_sigmatgammat(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            - dt {[type]} -- [description]
            - file_parameters {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = dt.data[:, 0]
        x[:, 1] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 2]
        y[:, 1] = dt.data[:, 1]
        # If times==0, set time column using the index
        # if (np.max(x)==0):
        #     x[:, 0] = np.linspace(1, dt.num_rows, dt.num_rows)
        #     x[:, 1] = np.linspace(1, dt.num_rows, dt.num_rows)
        return x, y, True


class CLApplicationLAOS(BaseApplicationLAOS, Application):
    """[summary]
    
    [description]
    """

    def __init__(self, name='LAOS', parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'LAOS'})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)
        #usually this class stays empty


class GUIApplicationLAOS(BaseApplicationLAOS, QApplicationWindow):
    """[summary]
    
    [description]
    """

    def __init__(self, name='LAOS', parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'LAOS'})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)

        #add the GUI-specific objects here:
