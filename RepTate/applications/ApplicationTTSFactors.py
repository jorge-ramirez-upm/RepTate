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
"""Module ApplicationTTSFactors

Module for handling time-temperature superposition factors and fit theories.

"""
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Application import Application
from RepTate.gui.QApplicationWindow import QApplicationWindow
from RepTate.core.View import View
from RepTate.core.FileType import TXTColumnFile
import numpy as np


class ApplicationTTSFactors(CmdBase):
    """Application handling time-temperature superposition factors and fit theories

    """
    appname = "TTSF"
    description = "TTS shift factors"
    extension = 'ttsf'

    def __new__(cls, name="TTSF", parent=None):
        """[summary]

        [description]

        Keyword Arguments:
            - name {[type]} -- [description] (default: {"TTSFactors"})
            - parent {[type]} -- [description] (default: {None})

        Returns:
            - [type] -- [description]
        """
        if CmdBase.mode == CmdMode.GUI:
            return GUIApplicationTTSFactors(name, parent)
        else:
            return CLApplicationTTSFactors(name, parent)


class BaseApplicationTTSFactors:
    """[summary]

    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/TTSFactors/TTSFactors.html'
    appname = ApplicationTTSFactors.appname

    def __init__(self, name="TTSF", parent=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {"TTSFactors"})
            - parent {[type]} -- [description] (default: {None})
        """
        from TheoryWLF import TheoryWLF
        from TheoryArrhenius import TheoryArrhenius
        #from TheoryArrhenius import TheoryArrhenius
        super().__init__(name, parent)

        # VIEWS
        self.views["log(aT)"] = View(
            name="log(aT)",
            description="log Horizontal shift factor",
            x_label="T",
            y_label="$\log(a_T)$",
            x_units="°C",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogaT,
            n=1,
            snames=["log(aT)"])
        self.views["aT"] = View(
            name="aT",
            description="Horizontal shift factor",
            x_label="T",
            y_label="$a_T$",
            x_units="°C",
            y_units="-",
            log_x=False,
            log_y=True,
            view_proc=self.viewaT,
            n=1,
            snames=["aT"])
        self.views["log(bT)"] = View(
            name="log(bT)",
            description="log Vertical shift factor",
            x_label="T",
            y_label="$\log(b_T)$",
            x_units="°C",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogbT,
            n=1,
            snames=["log(bT)"])
        self.views["bT"] = View(
            name="bT",
            description="Vertical shift factor",
            x_label="T",
            y_label="$b_T$",
            x_units="°C",
            y_units="-",
            log_x=False,
            log_y=True,
            view_proc=self.viewbT,
            n=1,
            snames=["bT"])

        self.views["log(aT, bT)"] = View(
            name="log(aT, bT)",
            description="log Horizontal and Vertical shift factors",
            x_label="T",
            y_label="$\log(a_T, b_T)$",
            x_units="°C",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogaTbT,
            n=2,
            snames=["log(aT)", "log(bT)"])

        self.views["log(aT) vs 1/T"] = View(
            name="log(aT) vs 1/T",
            description="log Horizontal shift factors vs 1/T",
            x_label="1/T",
            y_label="$\log(a_T)$",
            x_units="K$^{-1}$",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogaT_invT,
            n=1,
            snames=["log(aT)"])

        #set multiviews
        self.nplots = 1
        self.multiviews = []
        for i in range(self.nplot_max):
            # set views in the same order as declared above
            self.multiviews.append(list(self.views.values())[i])
        self.multiplots.reorg_fig(self.nplots)

        # FILES
        ftype = TXTColumnFile(
            "TTS factors", "ttsf",
            "TTS shift factors",
            ['T', 'aT', 'bT'], ['Mw'], ['°C', '-', '-'])
        self.filetypes[ftype.extension] = ftype

        # THEORIES
        self.theories[TheoryWLF.thname] = TheoryWLF
        self.theories[TheoryArrhenius.thname] = TheoryArrhenius
        #self.theories[TheoryWLFShiftTest.thname] = TheoryWLFShiftTest
        self.add_common_theories()

        #set the current view
        self.set_views()

    def viewLogaT(self, dt, file_parameters):
        """Logarithm of the horizontal shift factor
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = np.log10(dt.data[:, 1])
        return x, y, True

    def viewaT(self, dt, file_parameters):
        """Horizontal shift factor
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True

    def viewLogbT(self, dt, file_parameters):
        """Logarithm of the vertical shift factor
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = np.log10(dt.data[:, 2])
        return x, y, True

    def viewbT(self, dt, file_parameters):
        """Vertical shift factor
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 2]
        return x, y, True

    def viewLogaTbT(self, dt, file_parameters):
        """Logarithm of the vertical shift factor
        """
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = dt.data[:, 0]
        x[:, 1] = dt.data[:, 0]
        y[:, 0] = np.log10(dt.data[:, 1])
        y[:, 1] = np.log10(dt.data[:, 2])
        return x, y, True

    def viewLogaT_invT(self, dt, file_parameters):
        """Logarithm of the horizontal shift factor
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = 1/(dt.data[:, 0] + 273.15)
        y[:, 0] = np.log10(dt.data[:, 1])
        return x, y, True

class CLApplicationTTSFactors(BaseApplicationTTSFactors, Application):
    """[summary]

    [description]
    """

    def __init__(self, name="TTSFactors", parent=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {"TTSFactors"})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)


class GUIApplicationTTSFactors(BaseApplicationTTSFactors, QApplicationWindow):
    """[summary]

    [description]
    """

    def __init__(self, name="TTSFactors", parent=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {"TTSFactors"})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)
