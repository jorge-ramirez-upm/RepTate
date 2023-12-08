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
# Copyright (2017-2023): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module ApplicationTemplate

Template file for the definition of a new Application Module

"""
from RepTate.gui.QApplicationWindow import QApplicationWindow
from RepTate.core.View import View
from RepTate.core.FileType import TXTColumnFile
import numpy as np


class ApplicationTemplate(QApplicationWindow):
    """Application for [THE BASIC DOCUMENTATION OF THE APPLICATION GOES HERE]"""
    appname = 'Template'
    description = 'Template Application'  #used in the command-line Reptate
    extension = "txt"  # drag and drop this extension automatically opens this application
    #html_help_file = ''

    def __init__(self, name='Template', parent=None):
        """**Constructor**"""

        # IMPORT THEORIES
        # Import theories specific to the Application e.g.:
        # from TheoryTemplate import TheoryA

        super().__init__(name, parent, nplot_max=1)

        # VIEWS
        # set the views that can be selected in the view combobox
        self.views['y(x)'] = View(
            name='y(x)',
            description='y as a function of x',
            x_label='x',
            y_label='y(x)',
            x_units='-',
            y_units='-',
            log_x=False,
            log_y=False,
            view_proc=self.viewyx,
            n=1,
            snames=['y(x)'])

        # set multiviews
        # default view order in multiplot views, set nplots=1 for single view
        self.nplots = 1
        self.multiviews = []
        for i in range(self.nplot_max):
            # set views in the same order as declared above
            self.multiviews.append(list(self.views.values())[i])
        self.multiplots.reorg_fig(self.nplots)

        # FILES
        # set the type of files that ApplicationTemplate can open
        ftype = TXTColumnFile(
            name='content of files',
            extension='txt',
            description='description of the file type',
            col_names=['col1', 'col2'],
            basic_file_parameters=['param1', 'param2'],
            col_units=['units_col1', 'units_col2'])
        self.filetypes[
            ftype.extension] = ftype  #add each the file type to dictionary

        # THEORIES
        # add the theories related to ApplicationTemplate to the dictionary, e.g.:
        # self.theories[TheoryA.thname] = TheoryA
        # self.theories[TheoryB.thname] = TheoryB
        self.add_common_theories()  # Add basic theories to the application

        #set the current view
        self.set_views()

        #add the GUI-specific objects here:


    def viewyx(self, dt, file_parameters):
        """Function that defines how the view is shown. In this example, just the 1st and 2nd columns are shown. 
        
        The view must handle objects of type DataTable and can make use of the file parameters"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True

