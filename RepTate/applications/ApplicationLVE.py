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
"""Module ApplicationLVE

Module for the analysis of small angle oscillatory shear data - Master curves

"""
from RepTate.gui.QApplicationWindow import QApplicationWindow
from RepTate.core.View import View
from RepTate.core.FileType import TXTColumnFile, ExcelFile
import numpy as np


class ApplicationLVE(QApplicationWindow):
    """Application to Analyze Linear Viscoelastic Data"""

    appname = "LVE"
    description = "Linear Viscoelasticity"
    extension = "tts"
    html_help_file = "http://reptate.readthedocs.io/manual/Applications/LVE/LVE.html"

    def __init__(self, name="LVE", parent=None):
        """**Constructor**"""
        from RepTate.theories.TheoryMaxwellModes import TheoryMaxwellModesFrequency
        from RepTate.theories.TheoryLikhtmanMcLeish2002 import TheoryLikhtmanMcLeish2002
        from RepTate.theories.TheoryDSMLinear import TheoryDSMLinear
        from RepTate.theories.TheoryCarreauYasuda import TheoryCarreauYasuda
        from RepTate.theories.TheoryRouse import TheoryRouseFrequency
        from RepTate.theories.TheoryDTDStars import TheoryDTDStarsFreq
        from RepTate.theories.TheoryBobLVE import TheoryBobLVE
        from RepTate.theories.TheoryRDPLVE import TheoryRDPLVE
        from RepTate.theories.TheoryStickyReptation import TheoryStickyReptation
        from RepTate.theories.TheoryShanbhagMaxwellModes import (
            TheoryShanbhagMaxwellModesFrequency,
        )

        super().__init__(name, parent)

        # VIEWS
        self.views["log(G',G''(w))"] = View(
            name="log(G',G''(w))",
            description="log Storage,Loss moduli",
            x_label="log($\omega$)",
            y_label="log(G'($\omega$),G''($\omega$))",
            x_units="rad/s",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogG1G2,
            n=2,
            snames=["log(G'(w))", "log(G''(w))"],
        )
        self.views["G',G''(w)"] = View(
            "G',G''(w)",
            "Storage,Loss moduli",
            r"$\omega$",
            r"G'($\omega$),G''($\omega$)",
            "rad/s",
            "Pa",
            True,
            True,
            self.viewG1G2,
            2,
            ["G'(w)", "G''(w)"],
        )
        self.views["etastar"] = View(
            "etastar",
            "Complex Viscosity",
            r"$\omega$",
            r"$|\eta^*(\omega)|$",
            "rad/s",
            "Pa.s",
            True,
            True,
            self.viewEtaStar,
            1,
            ["eta*(w)"],
        )
        self.views["logetastar"] = View(
            "logetastar",
            "log Complex Viscosity",
            r"log($\omega$)",
            r"log$|\eta^*(\omega)|$",
            "rad/s",
            "Pa.s",
            False,
            False,
            self.viewLogEtaStar,
            1,
            ["log(eta*(w))"],
        )
        self.views["delta"] = View(
            "delta",
            "delta",
            r"$\omega$",
            r"$\delta(\omega)$",
            "rad/s",
            "-",
            True,
            True,
            self.viewDelta,
            1,
            ["delta(w)"],
        )
        self.views["tan(delta)"] = View(
            "tan(delta)",
            "tan(delta)",
            r"$\omega$",
            r"tan($\delta$)",
            "rad/s",
            "-",
            True,
            True,
            self.viewTanDelta,
            1,
            ["tan(delta((w))"],
        )
        self.views["log(tan(delta))"] = View(
            "log(tan(delta))",
            "log(tan(delta))",
            r"log($\omega$)",
            r"log(tan($\delta$))",
            "rad/s",
            "-",
            False,
            False,
            self.viewLogTanDelta,
            1,
            ["log(tan(delta((w)))"],
        )
        self.views["log(G*)"] = View(
            "log(G*)",
            "log(G*(omega))",
            r"log($\omega$)",
            r"log(G*($\omega$))",
            "rad/s",
            "Pa",
            False,
            False,
            self.viewLogGstar,
            1,
            ["log(G*)"],
        )
        self.views["log(tan(delta),G*)"] = View(
            "log(tan(delta),G*)",
            r"log(tan($\delta$))",
            "log(G*)",
            r"log(tan($\delta$))",
            "Pa",
            "-",
            False,
            False,
            self.viewLogtandeltaGstar,
            1,
            [r"log(tan($\delta))"],
        )
        self.views["delta(G*)"] = View(
            "delta(G*)",
            r"$\delta$)",
            "log(G*)",
            r"$\delta$)",
            "Pa",
            "deg",
            False,
            False,
            self.viewdeltatanGstar,
            1,
            ["delta"],
        )
        self.views["J',J''(w)"] = View(
            "J',J''(w)",
            "J moduli",
            r"$\omega$",
            r"J'($\omega$),J''($\omega$)",
            "rad/s",
            r"$Pa^{-1}$",
            True,
            True,
            self.viewJ1J2,
            2,
            ["J'(w)", "J''(w)"],
        )
        self.views["Cole-Cole"] = View(
            "Cole-Cole",
            "Cole-Cole plot",
            r"$\eta'$",
            r"$\eta''$",
            "Pa.s",
            "Pa.s",
            False,
            False,
            self.viewColeCole,
            1,
            [r"$eta'$"],
        )
        self.views["log(G')"] = View(
            name="log(G')",
            description="log Storage modulus",
            x_label=r"log($\omega$)",
            y_label=r"log(G'($\omega$))",
            x_units="rad/s",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogG1,
            n=1,
            snames=["log(G'(w))"],
        )
        self.views["G'"] = View(
            "G'",
            "Storage modulus",
            r"$\omega$",
            r"G'($\omega$)",
            "rad/s",
            "Pa",
            True,
            True,
            self.viewG1,
            1,
            ["G'(w)"],
        )
        self.views["log(G'')"] = View(
            name="log(G'')",
            description="log Loss modulus",
            x_label=r"log($\omega$)",
            y_label=r"log(G'($\omega$))",
            x_units="rad/s",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogG2,
            n=1,
            snames=["log(G''(w))"],
        )
        self.views["G''"] = View(
            "G''",
            "Loss modulus",
            r"$\omega$",
            r"G''($\omega$)",
            "rad/s",
            "Pa",
            True,
            True,
            self.viewG2,
            1,
            ["G''(w)"],
        )
        self.views["log(G',G''(w),tan(delta))"] = View(
            name="log(G',G''(w),tan(delta))",
            description="log Storage,Loss moduli, tan(delta)",
            x_label=r"log($\omega$)",
            y_label=r"log(G'($\omega$),G''($\omega$),tan($\delta$))",
            x_units="rad/s",
            y_units="Pa,-",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogG1G2tandelta,
            n=3,
            snames=["log(G'(w))", "log(G''(w)),log(tan(delta))"],
        )

        # set multiviews
        self.nplots = 1
        self.multiviews = []
        for i in range(self.nplot_max):
            # set views in the same order as declared above
            self.multiviews.append(list(self.views.values())[i])
        self.multiplots.reorg_fig(self.nplots)

        # FILES
        ftype = TXTColumnFile(
            "LVE files",
            "tts",
            "LVE files",
            ["w", "G'", "G''"],
            ["Mw", "T"],
            ["rad/s", "Pa", "Pa"],
        )
        self.filetypes[ftype.extension] = ftype
        self.filetypes["osc"] = TXTColumnFile(
            "OSC files",
            "osc",
            "Small-angle oscillatory masurements from the Rheometer",
            ["w", "G'", "G''"],
            ["Mw", "T"],
            ["rad/s", "Pa", "Pa"],
        )

        self.filetypes["xlsx"] = ExcelFile(
            "Excel files",
            "xlsx",
            "Excel File",
            ["w", "G'", "G''"],
            [],
            ["rad/s", "Pa", "Pa"],
        )

        # THEORIES
        self.theories[TheoryMaxwellModesFrequency.thname] = TheoryMaxwellModesFrequency
        self.theories[TheoryLikhtmanMcLeish2002.thname] = TheoryLikhtmanMcLeish2002
        self.theories[TheoryCarreauYasuda.thname] = TheoryCarreauYasuda
        self.theories[TheoryDSMLinear.thname] = TheoryDSMLinear
        self.theories[TheoryRouseFrequency.thname] = TheoryRouseFrequency
        self.theories[TheoryDTDStarsFreq.thname] = TheoryDTDStarsFreq
        self.theories[TheoryBobLVE.thname] = TheoryBobLVE
        self.theories[TheoryRDPLVE.thname] = TheoryRDPLVE
        self.theories[TheoryStickyReptation.thname] = TheoryStickyReptation
        self.theories[
            TheoryShanbhagMaxwellModesFrequency.thname
        ] = TheoryShanbhagMaxwellModesFrequency
        self.add_common_theories()

        # set the current view
        self.set_views()

    def viewLogG1G2(self, dt, file_parameters):
        """Logarithm of the storage modulus :math:`\\log(G'(\\omega))` and loss modulus :math:`\\log(G''(\\omega))` vs :math:`\\log(\\omega)`"""
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = np.log10(dt.data[:, 0])
        x[:, 1] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 1])
        y[:, 1] = np.log10(dt.data[:, 2])
        return x, y, True

    def viewG1G2(self, dt, file_parameters):
        """Storage modulus :math:`G'(\\omega)` and loss modulus :math:`G''(\\omega)` (in logarithmic scale) vs :math:`\\omega` (in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = dt.data[:, 0]
        x[:, 1] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        y[:, 1] = dt.data[:, 2]
        return x, y, True

    def viewEtaStar(self, dt, file_parameters):
        """Complex viscosity :math:`\\eta^*(\\omega) = \\sqrt{G'^2 + G''^2}/\\omega` (in logarithmic scale) vs :math:`\\omega` (in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = np.sqrt(dt.data[:, 1] ** 2 + dt.data[:, 2] ** 2) / dt.data[:, 0]
        return x, y, True

    def viewLogEtaStar(self, dt, file_parameters):
        """Logarithm of the complex viscosity :math:`\\eta^*(\\omega) = \\sqrt{G'^2 + G''^2}/\\omega` vs :math:`\\log(\\omega)`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(
            np.sqrt(dt.data[:, 1] ** 2 + dt.data[:, 2] ** 2) / dt.data[:, 0]
        )
        return x, y, True

    def viewDelta(self, dt, file_parameters):
        """Loss or phase angle :math:`\\delta(\\omega)=\\arctan(G''/G')\\cdot 180/\\pi` (in degrees, in logarithmic scale) vs :math:`\\omega` (in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = np.arctan2(dt.data[:, 2], dt.data[:, 1]) * 180 / np.pi
        return x, y, True

    def viewTanDelta(self, dt, file_parameters):
        """Tangent of the phase angle :math:`\\tan(\\delta(\\omega))=G''/G'` (in logarithmic scale) vs :math:`\\omega` (in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 2] / dt.data[:, 1]
        return x, y, True

    def viewLogTanDelta(self, dt, file_parameters):
        """:math:`\\log(\\tan(\\delta(\\omega)))=\\log(G''/G')` vs :math:`\\log(\\omega)`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 2] / dt.data[:, 1])
        return x, y, True

    def viewLogGstar(self, dt, file_parameters):
        """Logarithm of the modulus of the complex viscosity :math:`|G^*(\\omega)|=\\sqrt{G'^2+G''^2}` vs :math:`\\log(\\omega)`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(np.sqrt(np.square(dt.data[:, 1]) + np.square(dt.data[:, 2])))
        return x, y, True

    def viewLogtandeltaGstar(self, dt, file_parameters):
        """Logarithm of the tangent of the loss angle :math:`\\tan(\\delta(\\omega))=G''/G'` vs logarithm of the modulus of the complex viscosity :math:`|G^*(\\omega)|=\\sqrt{G'^2+G''^2}`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(np.sqrt(np.square(dt.data[:, 1]) + np.square(dt.data[:, 2])))
        y[:, 0] = np.log10(dt.data[:, 2] / dt.data[:, 1])
        return x, y, True

    def viewdeltatanGstar(self, dt, file_parameters):
        """Loss angle :math:`\\delta(\\omega)=\\arctan(G''/G')` vs logarithm of the modulus of the complex viscosity :math:`|G^*(\\omega)|=\\sqrt{G'^2+G''^2}`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(np.sqrt(np.square(dt.data[:, 1]) + np.square(dt.data[:, 2])))
        y[:, 0] = np.arctan2(dt.data[:, 2], dt.data[:, 1]) * 180 / np.pi
        return x, y, True

    def viewJ1J2(self, dt, file_parameters):
        """Storage compliance :math:`J'(\\omega)=G'/(G'^2+G''^2)` and loss compliance :math:`J''(\\omega)=G''/(G'^2+G''^2)` (in logarithmic scale) vs :math:`\\omega` (in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = dt.data[:, 0]
        x[:, 1] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1] / (np.square(dt.data[:, 1]) + np.square(dt.data[:, 2]))
        y[:, 1] = dt.data[:, 2] / (np.square(dt.data[:, 1]) + np.square(dt.data[:, 2]))
        return x, y, True

    def viewColeCole(self, dt, file_parameters):
        """Cole-Cole plot: out of phase viscosity :math:`\\eta''(\\omega)=G'(\\omega)/\\omega` vs dynamic viscosity :math:`\\eta'(\\omega)=G''(\\omega)/\\omega`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 2] / dt.data[:, 0]
        y[:, 0] = dt.data[:, 1] / dt.data[:, 0]
        return x, y, True

    def viewLogG1(self, dt, file_parameters):
        """Logarithm of the storage modulus :math:`\\log(G'(\\omega))` vs :math:`\\log(\\omega)`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 1])
        return x, y, True

    def viewG1(self, dt, file_parameters):
        """Storage modulus :math:`G'(\\omega)` (in logarithmic scale) vs :math:`\\omega` (in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True

    def viewLogG2(self, dt, file_parameters):
        """Logarithm of the loss modulus :math:`\\log(G''(\\omega))` vs :math:`\\log(\\omega)`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 2])
        return x, y, True

    def viewG2(self, dt, file_parameters):
        """Loss modulus :math:`G''(\\omega)` (in logarithmic scale) vs :math:`\\omega` (in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 2]
        return x, y, True

    def viewLogG1G2tandelta(self, dt, file_parameters):
        """Logarithm of the storage modulus :math:`\\log(G'(\\omega))`, loss modulus :math:`\\log(G''(\\omega))` and tangent of the loss angle :math:`\\log(\\tan(\\delta(\\omega)))=\\log(G''/G')` vs :math:`\\log(\\omega)`"""
        x = np.zeros((dt.num_rows, 3))
        y = np.zeros((dt.num_rows, 3))
        x[:, 0] = np.log10(dt.data[:, 0])
        x[:, 1] = np.log10(dt.data[:, 0])
        x[:, 2] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 1])
        y[:, 1] = np.log10(dt.data[:, 2])
        y[:, 2] = np.log10(dt.data[:, 2] / dt.data[:, 1])
        return x, y, True
