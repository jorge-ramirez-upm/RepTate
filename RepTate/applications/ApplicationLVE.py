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
# Copyright (2017-2026): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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

from typing import Any, ClassVar

from RepTate.gui.QApplicationWindow import QApplicationWindow
from RepTate.core.View import AxisSpec, View
from RepTate.core.File import FileParameterSpec
from RepTate.core.FileType import TXTColumnFile, ExcelFile
from RepTate.core.typing import ApplicationManagerLike, DataTableLike, FileParameters, ViewResult
import numpy as np


class ApplicationLVE(QApplicationWindow):
    """Application to Analyze Linear Viscoelastic Data"""

    appname: ClassVar[str] = "LVE"
    description: ClassVar[str] = "Linear Viscoelasticity"
    extension: ClassVar[str] = "tts"
    html_help_file: ClassVar[str] = "http://reptate.readthedocs.io/manual/Applications/LVE/LVE.html"

    def __init__(self, name: str = "LVE", parent: ApplicationManagerLike | None = None) -> None:
        """**Constructor**"""
        from RepTate.theories.TheoryMaxwellModes import TheoryMaxwellModesFrequency
        from RepTate.theories.TheoryLikhtmanMcLeish2002 import TheoryLikhtmanMcLeish2002
        from RepTate.theories.TheoryDSMLinear import TheoryDSMLinear
        from RepTate.theories.TheoryCarreauYasuda import TheoryCarreauYasuda
        from RepTate.theories.TheoryRouse import TheoryRouseFrequency
        from RepTate.theories.TheoryDTDStars import TheoryDTDStarsFreq
        from RepTate.theories.TheoryBobLVE import TheoryBobLVE
        from RepTate.theories.TheoryLP2RLVE import TheoryLP2RLVE
        from RepTate.theories.TheoryRDPLVE import TheoryRDPLVE
        from RepTate.theories.TheoryStickyReptation import TheoryStickyReptation
        from RepTate.theories.TheoryShanbhagMaxwellModes import (
            TheoryShanbhagMaxwellModesFrequency,
        )
        from RepTate.theories.TheoryBaumgaertelWinter import TheoryBaumgaertelWinter

        super().__init__(name, parent)

        frequency_units: tuple[str, ...] = ("rad/s", "Hz")
        stress_units: tuple[str, ...] = ("Pa", "kPa", "MPa", "bar", "atm")
        viscosity_units: tuple[str, ...] = ("Pa.s", "kPa.s")
        compliance_units: tuple[str, ...] = ("1/Pa", "1/kPa", "1/MPa", "1/bar", "1/atm")

        # VIEWS
        self.views["log(G',G''(w))"] = View(
            name="log(G',G''(w))",
            description="log Storage,Loss moduli",
            x_label=r"log($\omega$)",
            y_label=r"log(G'($\omega$),G''($\omega$))",
            x_units="rad/s",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogG1G2,
            n=2,
            snames=["log(G'(w))", "log(G''(w))"],
            x_axis=AxisSpec(
                label=r"log($\omega$)",
                internal_unit="rad/s",
                transform="log10",
                unit_choices=frequency_units,
            ),
            y_axis=AxisSpec(
                label=r"log(G'($\omega$),G''($\omega$))",
                internal_unit="Pa",
                transform="log10",
                unit_choices=stress_units,
            ),
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
            x_axis=AxisSpec(
                label=r"$\omega$",
                internal_unit="rad/s",
                unit_choices=frequency_units,
            ),
            y_axis=AxisSpec(
                label=r"G'($\omega$),G''($\omega$)",
                internal_unit="Pa",
                unit_choices=stress_units,
            ),
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
            x_axis=AxisSpec(
                label=r"$\omega$",
                internal_unit="rad/s",
                unit_choices=frequency_units,
            ),
            y_axis=AxisSpec(
                label=r"$|\eta^*(\omega)|$",
                internal_unit="Pa.s",
                unit_choices=viscosity_units,
            ),
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
            x_axis=AxisSpec(
                label=r"log($\omega$)",
                internal_unit="rad/s",
                transform="log10",
                unit_choices=frequency_units,
            ),
            y_axis=AxisSpec(
                label=r"log$|\eta^*(\omega)|$",
                internal_unit="Pa.s",
                transform="log10",
                unit_choices=viscosity_units,
            ),
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
            x_axis=AxisSpec(
                label=r"$\omega$",
                internal_unit="rad/s",
                unit_choices=frequency_units,
            ),
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
            x_axis=AxisSpec(
                label=r"$\omega$",
                internal_unit="rad/s",
                unit_choices=frequency_units,
            ),
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
            x_axis=AxisSpec(
                label=r"log($\omega$)",
                internal_unit="rad/s",
                transform="log10",
                unit_choices=frequency_units,
            ),
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
            x_axis=AxisSpec(
                label=r"log($\omega$)",
                internal_unit="rad/s",
                transform="log10",
                unit_choices=frequency_units,
            ),
            y_axis=AxisSpec(
                label=r"log(G*($\omega$))",
                internal_unit="Pa",
                transform="log10",
                unit_choices=stress_units,
            ),
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
            x_axis=AxisSpec(
                label="log(G*)",
                internal_unit="Pa",
                transform="log10",
                unit_choices=stress_units,
            ),
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
            x_axis=AxisSpec(
                label="log(G*)",
                internal_unit="Pa",
                transform="log10",
                unit_choices=stress_units,
            ),
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
            x_axis=AxisSpec(
                label=r"$\omega$",
                internal_unit="rad/s",
                unit_choices=frequency_units,
            ),
            y_axis=AxisSpec(
                label=r"J'($\omega$),J''($\omega$)",
                internal_unit="1/Pa",
                unit_choices=compliance_units,
            ),
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
            x_axis=AxisSpec(
                label=r"$\eta'$",
                internal_unit="Pa.s",
                unit_choices=viscosity_units,
            ),
            y_axis=AxisSpec(
                label=r"$\eta''$",
                internal_unit="Pa.s",
                unit_choices=viscosity_units,
            ),
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
            x_axis=AxisSpec(
                label=r"log($\omega$)",
                internal_unit="rad/s",
                transform="log10",
                unit_choices=frequency_units,
            ),
            y_axis=AxisSpec(
                label=r"log(G'($\omega$))",
                internal_unit="Pa",
                transform="log10",
                unit_choices=stress_units,
            ),
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
            x_axis=AxisSpec(
                label=r"$\omega$",
                internal_unit="rad/s",
                unit_choices=frequency_units,
            ),
            y_axis=AxisSpec(
                label=r"G'($\omega$)",
                internal_unit="Pa",
                unit_choices=stress_units,
            ),
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
            x_axis=AxisSpec(
                label=r"log($\omega$)",
                internal_unit="rad/s",
                transform="log10",
                unit_choices=frequency_units,
            ),
            y_axis=AxisSpec(
                label=r"log(G'($\omega$))",
                internal_unit="Pa",
                transform="log10",
                unit_choices=stress_units,
            ),
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
            x_axis=AxisSpec(
                label=r"$\omega$",
                internal_unit="rad/s",
                unit_choices=frequency_units,
            ),
            y_axis=AxisSpec(
                label=r"G''($\omega$)",
                internal_unit="Pa",
                unit_choices=stress_units,
            ),
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
            x_axis=AxisSpec(
                label=r"log($\omega$)",
                internal_unit="rad/s",
                transform="log10",
                unit_choices=frequency_units,
            ),
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
            name="LVE files",
            extension="tts",
            description="LVE files",
            col_names=["w", "G'", "G''"],
            basic_file_parameters=["Mw", "T"],
            col_units=["rad/s", "Pa", "Pa"],
            # Legacy RepTate theory code expects file parameter T in Celsius
            # and converts to Kelvin locally when needed.
            file_parameter_specs=[
                FileParameterSpec("Mw", "molar_mass", "kg/mol", "kg/mol"),
                FileParameterSpec("T", "temperature", "ºC", "ºC"),
            ],
        )
        self.filetypes[ftype.extension] = ftype
        self.filetypes["osc"] = TXTColumnFile(
            name="OSC files",
            extension="osc",
            description="Small-angle oscillatory masurements from the Rheometer",
            col_names=["w", "G'", "G''"],
            basic_file_parameters=["Mw", "T"],
            col_units=["rad/s", "Pa", "Pa"],
            file_parameter_specs=[
                FileParameterSpec("Mw", "molar_mass", "kg/mol", "kg/mol"),
                FileParameterSpec("T", "temperature", "ºC", "ºC"),
            ],
        )

        self.filetypes["xlsx"] = ExcelFile(
            name="Excel files",
            extension="xlsx",
            description="Excel File",
            col_names=["w", "G'", "G''"],
            basic_file_parameters=[],
            col_units=["rad/s", "Pa", "Pa"],
        )

        # THEORIES
        self.theories[TheoryMaxwellModesFrequency.thname] = TheoryMaxwellModesFrequency
        self.theories[TheoryLikhtmanMcLeish2002.thname] = TheoryLikhtmanMcLeish2002
        self.theories[TheoryCarreauYasuda.thname] = TheoryCarreauYasuda
        self.theories[TheoryDSMLinear.thname] = TheoryDSMLinear
        self.theories[TheoryRouseFrequency.thname] = TheoryRouseFrequency
        self.theories[TheoryDTDStarsFreq.thname] = TheoryDTDStarsFreq
        self.theories[TheoryBobLVE.thname] = TheoryBobLVE
        self.theories[TheoryLP2RLVE.thname] = TheoryLP2RLVE
        self.theories[TheoryRDPLVE.thname] = TheoryRDPLVE
        self.theories[TheoryStickyReptation.thname] = TheoryStickyReptation
        self.theories[TheoryShanbhagMaxwellModesFrequency.thname] = TheoryShanbhagMaxwellModesFrequency
        self.theories[TheoryBaumgaertelWinter.thname] = TheoryBaumgaertelWinter
        self.add_common_theories()

        # set the current view
        self.set_views()

    def viewLogG1G2(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Logarithm of the storage modulus :math:`\\log(G'(\\omega))` and loss modulus :math:`\\log(G''(\\omega))` vs :math:`\\log(\\omega)`"""
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = np.log10(dt.data[:, 0])
        x[:, 1] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 1])
        y[:, 1] = np.log10(dt.data[:, 2])
        return x, y, True

    def viewG1G2(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Storage modulus :math:`G'(\\omega)` and loss modulus :math:`G''(\\omega)` (in logarithmic scale) vs :math:`\\omega` (in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = dt.data[:, 0]
        x[:, 1] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        y[:, 1] = dt.data[:, 2]
        return x, y, True

    def viewEtaStar(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Complex viscosity :math:`\\eta^*(\\omega) = \\sqrt{G'^2 + G''^2}/\\omega` (in logarithmic scale) vs :math:`\\omega` (in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = np.sqrt(dt.data[:, 1] ** 2 + dt.data[:, 2] ** 2) / dt.data[:, 0]
        return x, y, True

    def viewLogEtaStar(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Logarithm of the complex viscosity :math:`\\eta^*(\\omega) = \\sqrt{G'^2 + G''^2}/\\omega` vs :math:`\\log(\\omega)`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(np.sqrt(dt.data[:, 1] ** 2 + dt.data[:, 2] ** 2) / dt.data[:, 0])
        return x, y, True

    def viewDelta(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Loss or phase angle :math:`\\delta(\\omega)=\\arctan(G''/G')\\cdot 180/\\pi` (in degrees, in logarithmic scale) vs :math:`\\omega` (in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = np.arctan2(dt.data[:, 2], dt.data[:, 1]) * 180 / np.pi
        return x, y, True

    def viewTanDelta(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Tangent of the phase angle :math:`\\tan(\\delta(\\omega))=G''/G'` (in logarithmic scale) vs :math:`\\omega` (in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 2] / dt.data[:, 1]
        return x, y, True

    def viewLogTanDelta(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """:math:`\\log(\\tan(\\delta(\\omega)))=\\log(G''/G')` vs :math:`\\log(\\omega)`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 2] / dt.data[:, 1])
        return x, y, True

    def viewLogGstar(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Logarithm of the modulus of the complex viscosity :math:`|G^*(\\omega)|=\\sqrt{G'^2+G''^2}` vs :math:`\\log(\\omega)`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(np.sqrt(np.square(dt.data[:, 1]) + np.square(dt.data[:, 2])))
        return x, y, True

    def viewLogtandeltaGstar(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Logarithm of the tangent of the loss angle :math:`\\tan(\\delta(\\omega))=G''/G'` vs logarithm of the modulus of the complex viscosity :math:`|G^*(\\omega)|=\\sqrt{G'^2+G''^2}`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(np.sqrt(np.square(dt.data[:, 1]) + np.square(dt.data[:, 2])))
        y[:, 0] = np.log10(dt.data[:, 2] / dt.data[:, 1])
        return x, y, True

    def viewdeltatanGstar(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Loss angle :math:`\\delta(\\omega)=\\arctan(G''/G')` vs logarithm of the modulus of the complex viscosity :math:`|G^*(\\omega)|=\\sqrt{G'^2+G''^2}`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(np.sqrt(np.square(dt.data[:, 1]) + np.square(dt.data[:, 2])))
        y[:, 0] = np.arctan2(dt.data[:, 2], dt.data[:, 1]) * 180 / np.pi
        return x, y, True

    def viewJ1J2(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Storage compliance :math:`J'(\\omega)=G'/(G'^2+G''^2)` and loss compliance :math:`J''(\\omega)=G''/(G'^2+G''^2)` (in logarithmic scale) vs :math:`\\omega` (in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = dt.data[:, 0]
        x[:, 1] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1] / (np.square(dt.data[:, 1]) + np.square(dt.data[:, 2]))
        y[:, 1] = dt.data[:, 2] / (np.square(dt.data[:, 1]) + np.square(dt.data[:, 2]))
        return x, y, True

    def viewColeCole(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Cole-Cole plot: out of phase viscosity :math:`\\eta''(\\omega)=G'(\\omega)/\\omega` vs dynamic viscosity :math:`\\eta'(\\omega)=G''(\\omega)/\\omega`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 2] / dt.data[:, 0]
        y[:, 0] = dt.data[:, 1] / dt.data[:, 0]
        return x, y, True

    def viewLogG1(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Logarithm of the storage modulus :math:`\\log(G'(\\omega))` vs :math:`\\log(\\omega)`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 1])
        return x, y, True

    def viewG1(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Storage modulus :math:`G'(\\omega)` (in logarithmic scale) vs :math:`\\omega` (in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True

    def viewLogG2(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Logarithm of the loss modulus :math:`\\log(G''(\\omega))` vs :math:`\\log(\\omega)`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 2])
        return x, y, True

    def viewG2(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Loss modulus :math:`G''(\\omega)` (in logarithmic scale) vs :math:`\\omega` (in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 2]
        return x, y, True

    def viewLogG1G2tandelta(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
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
