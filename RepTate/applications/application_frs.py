# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# --------------------------------------------------------------------------------------------------------
#
# Authors:
#     Jorge Ramirez, jorge.ramirez@upm.es
#     Victor Boudara, mmvahb@leeds.ac.uk
#
# Useful links:
#     http://blogs.upm.es/compsoftmatter/software/reptate/
#     https://github.com/jorge-ramirez-upm/RepTate
#     http://reptate.readthedocs.io
#
# --------------------------------------------------------------------------------------------------------
#
# Copyright (2017-2020): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module Application_frs

Module for handling FRS experiments and simulations.

"""
from RepTate.core.Application import Application


class ApplicationFRS_I(Application):
    """Application to FRS Intensity simulations

    [description]
    """
    name = "FRS_I"
    description = "FRS Intensity"

    def __init__(self, name="FRS_I", parent=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {"FRS_I"})
            - parent {[type]} -- [description] (default: {None})
        """
        super(ApplicationFRS_I, self).__init__(name, parent)

        # VIEWS
        self.views["I(t)"] = View(
            name="I(t)",
            description="FRS Intensity decay",
            x_label="t",
            y_label="I(t)",
            x_units="s",
            y_units="-",
            log_x=True,
            log_y=True,
            view_proc=self.viewIt,
            n=1,
            snames=["I(t)"])
        self.views["log[I(t)]"] = View(
            name="log[I(t)]",
            description="log FRS Intensity decay",
            x_label="log(t)",
            y_label="log(I(t))",
            x_units="s",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogIt,
            n=1,
            snames=["log(I(t))"])

        #set multiviews
        self.multiviews = [self.views['I(t)']]
        self.nplots = len(self.multiviews)

        # FILES
        ftype = TXTColumnFile("I(t) FRS files", "FRS_INTENSITY",
                              "I(t) decay from FRS", ['t', 'I'],
                              ['d', 'Na', 'ka', 'Ns', 'ka', 'Keq', 'beta'],
                              ['s', 'Pa'])
        self.filetypes[ftype.extension] = ftype

        #Theories
        self.add_common_theories()

    def viewIt(self, dt, file_parameters):
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

    def viewLogIt(self, dt, file_parameters):
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
