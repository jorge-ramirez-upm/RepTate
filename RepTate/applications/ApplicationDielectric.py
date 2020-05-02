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
"""Module ApplicationDielectric

Module for the analysis of small angle oscillatory shear data - Master curves

"""
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Application import Application
from RepTate.gui.QApplicationWindow import QApplicationWindow
from RepTate.core.View import View
from RepTate.core.FileType import TXTColumnFile
import numpy as np


class ApplicationDielectric(CmdBase):
    """Application to Analyze Dielectric Spectroscopy Data

    """
    appname = "Dielectric"
    description = "Dielectric Spectroscopy"
    extension = "dls"

    def __new__(cls, name="Dielectric", parent=None):
        """[summary]

        [description]

        Keyword Arguments:
            - name {[type]} -- [description] (default: {"Dielectric"})
            - parent {[type]} -- [description] (default: {None})

        Returns:
            - [type] -- [description]
        """
        return GUIApplicationDielectric(
            name,
            parent) if (CmdBase.mode == CmdMode.GUI) else CLApplicationDielectric(
                name, parent)


class BaseApplicationDielectric:
    """[summary]

    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/Dielectric/Dielectric.html'
    appname = ApplicationDielectric.appname

    def __init__(self, name="Dielectric", parent=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {"Dielectric"})
            - parent {[type]} -- [description] (default: {None})
        """
        from TheoryDebyeModes import TheoryDebyeModesFrequency
        from TheoryHavriliakNegamiModes import TheoryHavriliakNegamiModesFrequency
        from TheoryKWWModes import TheoryKWWModesFrequency

        super().__init__(name, parent)

        # VIEWS
        self.views["log(e',e''(w))"] = View(
            name="log(e',e''(w))",
            description="log Relative permittivity, Dielectric Loss",
            x_label="log($\omega$)",
            y_label="log($\epsilon',\epsilon''$)",
            x_units="rad/s",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogE1E2,
            n=2,
            snames=["log(e')", "log(e'')"])
        self.views["semilog(e',e''(w))"] = View(
            name="semilog(e',e''(w))",
            description="semilog Relative permittivity, Dielectric Loss",
            x_label="log($\omega$)",
            y_label="$\epsilon',\epsilon''$",
            x_units="rad/s",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.viewSemiLogE1E2,
            n=2,
            snames=["e'(w)", "e''(w)"])
        self.views["e',e''(w)"] = View(
            "e',e''(w)",
            "Relative permittivity, Dielectric Loss",
            "$\omega$",
            "$\epsilon',\epsilon''$",
            "rad/s",
            "-",
            True,
            True,
            self.viewE1E2,
            2, ["e'(w)", "e''(w)"])
        self.views["log(e')"] = View(
            name="log(e')",
            description="log Relative Permittivity",
            x_label="log($\omega$)",
            y_label="log($\epsilon'$)",
            x_units="rad/s",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogE1,
            n=1,
            snames=["log(e')"])
        self.views["semilog(e')"] = View(
            name="semilog(e')",
            description="log Relative Permittivity",
            x_label="log($\omega$)",
            y_label="$\epsilon'$",
            x_units="rad/s",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.viewSemiLogE1,
            n=1,
            snames=["e'"])
        self.views["e'"] = View(
            "e'",
            "Relative Permittivity",
            "$\omega$",
            "$\epsilon'$",
            "rad/s",
            "-",
            True,
            True,
            self.viewE1,
            1, ["e'"])
        self.views["log(e'')"] = View(
            name="log(e'')",
            description="log Dielectric Loss",
            x_label="log($\omega$)",
            y_label="log($\epsilon''$)",
            x_units="rad/s",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogE2,
            n=1,
            snames=["log(e'')"])
        self.views["semilog(e'')"] = View(
            name="semilog(e'')",
            description="semilog Dielectric Loss",
            x_label="log($\omega$)",
            y_label="$\epsilon''$",
            x_units="rad/s",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.viewSemiLogE2,
            n=1,
            snames=["e''"])
        self.views["e''"] = View(
            "e''",
            "Dielectric Loss",
            "$\omega$",
            "$\epsilon''$",
            "rad/s",
            "-",
            True,
            True,
            self.viewE2,
            1, ["e''"])
        self.views["Cole-Cole"] = View(
            "Cole-Cole",
            "Cole-Cole plot",
            "$\epsilon'$",
            "$\epsilon''$",
            "-",
            "-",
            False,
            False,
            self.viewColeCole,
            1, ["e''"])

        #set multiviews
        self.nplots = 1
        self.multiviews = []
        for i in range(self.nplot_max):
            # set views in the same order as declared above
            self.multiviews.append(list(self.views.values())[i])
        self.multiplots.reorg_fig(self.nplots)

        # FILES
        ftype = TXTColumnFile("Dielectric Spectroscopy files", "dls", "Dielectric Spectroscopy files",
                              ['w', 'e\'', 'e\'\''], ['Mw', 'T'],
                              ['rad/s', '-', '-'])
        self.filetypes[ftype.extension] = ftype

        # THEORIES
        self.theories[TheoryDebyeModesFrequency.thname] = TheoryDebyeModesFrequency
        self.theories[TheoryHavriliakNegamiModesFrequency.thname] = TheoryHavriliakNegamiModesFrequency
        self.theories[TheoryKWWModesFrequency.thname] = TheoryKWWModesFrequency
        self.add_common_theories()

        #set the current view
        self.set_views()

    def viewLogE1E2(self, dt, file_parameters):
        """Log or the relative permittivity and Dielectric Loss :math:`\\epsilon'(\\omega), \\epsilon''(\\omega)` vs logarithm of the frequency :math:`\\omega`
        """
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = np.log10(dt.data[:, 0])
        x[:, 1] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 1])
        y[:, 1] = np.log10(dt.data[:, 2])
        return x, y, True

    def viewSemiLogE1E2(self, dt, file_parameters):
        """Semilog plot: Relative permittivity and Dielectric Loss :math:`\\epsilon'(\\omega), \\epsilon''(\\omega)` vs logarithm of frequency :math:`\\omega`
        """
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = np.log10(dt.data[:, 0])
        x[:, 1] = np.log10(dt.data[:, 0])
        y[:, 0] = dt.data[:, 1]
        y[:, 1] = dt.data[:, 2]
        return x, y, True

    def viewE1E2(self, dt, file_parameters):
        """Relative permittivity and Dielectric Loss :math:`\\epsilon'(\\omega), \\epsilon''(\\omega)` vs frequency :math:`\\omega`
        """
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = dt.data[:, 0]
        x[:, 1] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        y[:, 1] = dt.data[:, 2]
        return x, y, True


    def viewLogE1(self, dt, file_parameters):
        """Log or the relative permittivity :math:`\\epsilon'(\\omega)` vs logarithm of the frequency :math:`\\omega`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 1])
        return x, y, True

    def viewSemiLogE1(self, dt, file_parameters):
        """Semilog plot: Relative permittivity :math:`\\epsilon'(\\omega)` vs logarithm of the frequency :math:`\\omega`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = dt.data[:, 1]
        return x, y, True

    def viewE1(self, dt, file_parameters):
        """Relative permittivity :math:`\\epsilon'(\\omega)` vs frequency :math:`\\omega`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True

    def viewLogE2(self, dt, file_parameters):
        """Log or the Dielectric Loss :math:`\\epsilon''(\\omega)` vs logarithm of the frequency :math:`\\omega`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 2])
        return x, y, True

    def viewSemiLogE2(self, dt, file_parameters):
        """Semilog plot: Dielectric Loss :math:`\\epsilon''(\\omega)` vs logarithm of the frequency :math:`\\omega`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = dt.data[:, 2]
        return x, y, True

    def viewE2(self, dt, file_parameters):
        """Dielectric Loss :math:`\\epsilon''(\\omega)` vs frequency :math:`\\omega`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 2]
        return x, y, True

    def viewColeCole(self, dt, file_parameters):
        """Cole-Cole plot: Dielectric Loss :math:`\\epsilon''(\\omega)` vs relative permittivity :math:`\\epsilon'(\\omega)`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 1]
        y[:, 0] = dt.data[:, 2]
        return x, y, True


class CLApplicationDielectric(BaseApplicationDielectric, Application):
    """[summary]

    [description]
    """

    def __init__(self, name="Dielectric", parent=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {"Dielectric"})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)


class GUIApplicationDielectric(BaseApplicationDielectric, QApplicationWindow):
    """[summary]

    [description]
    """

    def __init__(self, name="Dielectric", parent=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {"Dielectric"})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)
