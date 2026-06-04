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
"""Module ApplicationNLVE

Module for handling data from start up of shear and extensional flow experiments.

"""

from typing import Any, ClassVar

from RepTate.gui.QApplicationWindow import QApplicationWindow
from RepTate.core.View import AxisSpec, View
from RepTate.core.File import FileParameterSpec
from RepTate.core.FileType import TXTColumnFile
from RepTate.core.typing import ApplicationManagerLike, DataTableLike, FileParameters, ViewResult
import numpy as np


class ApplicationNLVE(QApplicationWindow):
    """Application to Analyze Start up of Nonlinear flow"""

    appname: ClassVar[str] = "NLVE"
    description: ClassVar[str] = "Non-Linear Flow"
    extension: ClassVar[str] = "shear uext"
    html_help_file: ClassVar[str] = "http://reptate.readthedocs.io/manual/Applications/NLVE/NLVE.html"

    def __init__(self, name: str = "NLVE", parent: ApplicationManagerLike | None = None) -> None:
        """**Constructor**"""
        from RepTate.theories.TheoryRoliePoly import TheoryRoliePoly
        from RepTate.theories.TheoryUCM import TheoryUCM
        from RepTate.theories.TheoryGiesekus import TheoryGiesekus
        from RepTate.theories.TheoryPomPom import TheoryPomPom
        from RepTate.theories.TheoryRolieDoublePoly import TheoryRolieDoublePoly
        from RepTate.theories.TheoryBobNLVE import TheoryBobNLVE
        from RepTate.theories.TheoryPETS import TheoryPETS
        from RepTate.theories.TheorySCCR import TheorySCCR

        super().__init__(name, parent)

        time_units: tuple[str, ...] = ("ns", "μs", "ms", "s", "min", "h")
        stress_units: tuple[str, ...] = ("Pa", "kPa", "MPa", "bar", "atm")
        viscosity_units: tuple[str, ...] = ("Pa.s", "kPa.s")
        deformation_rate_units: tuple[str, ...] = ("1/s", "s-1", "s^-1", "s⁻¹", "1/min", "1/h")

        # VIEWS
        self.views["log(eta(t))"] = View(
            name="log(eta(t))",
            description="log transient viscosity",
            x_label="log(t)",
            y_label=r"log($\eta^+$)",
            x_units="s",
            y_units=r"Pa$\cdot$s",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogeta,
            n=1,
            snames=["log(eta)"],
            x_axis=AxisSpec(
                label="log(t)",
                internal_unit="s",
                transform="log10",
                unit_choices=time_units,
            ),
            y_axis=AxisSpec(
                label=r"log($\eta^+$)",
                internal_unit="Pa.s",
                transform="log10",
                unit_choices=viscosity_units,
            ),
        )
        self.views["eta(t)"] = View(
            name="eta(t)",
            description="transient viscosity",
            x_label="t",
            y_label=r"$\eta^+$",
            x_units="s",
            y_units=r"Pa$\cdot$s",
            log_x=True,
            log_y=True,
            view_proc=self.vieweta,
            n=1,
            snames=["eta"],
            x_axis=AxisSpec(label="t", internal_unit="s", unit_choices=time_units),
            y_axis=AxisSpec(
                label=r"$\eta^+$",
                internal_unit="Pa.s",
                unit_choices=viscosity_units,
            ),
        )
        self.views["log(sigma(gamma))"] = View(
            name="log(sigma(gamma))",
            description="log transient shear stress vs gamma",
            x_label=r"log($\gamma$)",
            y_label=r"log($\sigma^+$)",
            x_units="-",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogSigmaGamma,
            n=1,
            snames=["log(sigma)"],
            y_axis=AxisSpec(
                label=r"log($\sigma^+$)",
                internal_unit="Pa",
                transform="log10",
                unit_choices=stress_units,
            ),
        )
        self.views["sigma(gamma)"] = View(
            name="sigma(gamma)",
            description="transient shear stress vs gamma",
            x_label=r"$\gamma$",
            y_label=r"$\sigma^+$",
            x_units="-",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewSigmaGamma,
            n=1,
            snames=["sigma"],
            y_axis=AxisSpec(
                label=r"$\sigma^+$",
                internal_unit="Pa",
                unit_choices=stress_units,
            ),
        )
        self.views["log(sigma(t))"] = View(
            name="log(sigma(t))",
            description="log transient shear stress vs time",
            x_label="log(t)",
            y_label=r"log($\sigma^+$)",
            x_units="s",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogSigmaTime,
            n=1,
            snames=["log(sigma)"],
            x_axis=AxisSpec(
                label="log(t)",
                internal_unit="s",
                transform="log10",
                unit_choices=time_units,
            ),
            y_axis=AxisSpec(
                label=r"log($\sigma^+$)",
                internal_unit="Pa",
                transform="log10",
                unit_choices=stress_units,
            ),
        )
        self.views["sigma(t)"] = View(
            name="sigma(t)",
            description="transient shear stress vs time",
            x_label="t",
            y_label=r"$\sigma^+$",
            x_units="s",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewSigmaTime,
            n=1,
            snames=["sigma"],
            x_axis=AxisSpec(label="t", internal_unit="s", unit_choices=time_units),
            y_axis=AxisSpec(
                label=r"$\sigma^+$",
                internal_unit="Pa",
                unit_choices=stress_units,
            ),
        )
        self.views["Flow Curve"] = View(
            name="Flow Curve",
            description="Steady state stress vs flow rate",
            x_label="Flow rate",
            y_label=r"$\sigma$",
            x_units=r"s$^{-1}$",
            y_units="Pa",
            log_x=True,
            log_y=True,
            view_proc=self.view_flowcurve,
            n=1,
            snames=["sigma"],
            with_thline=False,
            filled=True,
            x_axis=AxisSpec(
                label="Flow rate",
                internal_unit="1/s",
                unit_choices=deformation_rate_units,
            ),
            y_axis=AxisSpec(
                label=r"$\sigma$",
                internal_unit="Pa",
                unit_choices=stress_units,
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
            name="Start-up of shear flow",
            extension="shear",
            description="Shear flow files",
            col_names=["t", "sigma_xy", "N1", "gdot"],
            basic_file_parameters=["gdot", "T"],
            col_units=["s", "Pa", "Pa", "s-1"],
            file_parameter_specs=[
                FileParameterSpec("T", "temperature", "ºC", "ºC"),
                FileParameterSpec("gdot", "deformation_rate", "1/s", "1/s"),
            ],
        )
        self.filetypes[ftype.extension] = ftype
        ftype = TXTColumnFile(
            "Elongation flow",
            "uext",
            "Elongation flow files",
            ["t", "N1", "gdot"],
            ["gdot", "T"],
            ["s", "Pa", "s-1"],
            file_parameter_specs=[
                FileParameterSpec("T", "temperature", "ºC", "ºC"),
            ],
        )
        self.filetypes[ftype.extension] = ftype

        # THEORIES
        self.theories[TheoryRoliePoly.thname] = TheoryRoliePoly
        self.theories[TheoryUCM.thname] = TheoryUCM
        self.theories[TheoryGiesekus.thname] = TheoryGiesekus
        self.theories[TheoryPomPom.thname] = TheoryPomPom
        self.theories[TheoryRolieDoublePoly.thname] = TheoryRolieDoublePoly
        self.theories[TheoryBobNLVE.thname] = TheoryBobNLVE
        self.theories[TheoryPETS.thname] = TheoryPETS
        self.theories[TheorySCCR.thname] = TheorySCCR
        self.add_common_theories()

        # set the current view
        self.set_views()
        self.finalize_application_setup()

    def viewLogeta(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Logarithm of the transient shear or extensional viscosity (depending on the experiment) :math:`\\eta(t)` vs logarithm of time :math:`t`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        if "gdot" in file_parameters:
            flow_rate = float(file_parameters["gdot"])
        else:
            flow_rate = float(file_parameters["edot"])
        y[:, 0] = np.log10(dt.data[:, 1] / flow_rate)
        return x, y, True

    def vieweta(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Transient shear or extensional viscosity (depending on the experiment) :math:`\\eta(t)` vs time :math:`t` (both axes in logarithmic scale by default)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        if "gdot" in file_parameters:
            flow_rate = float(file_parameters["gdot"])
        else:
            flow_rate = float(file_parameters["edot"])
        y[:, 0] = dt.data[:, 1] / flow_rate
        return x, y, True

    def viewLogSigmaTime(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Logarithm of the transient shear or extensional stress (depending on the experiment) :math:`\\sigma(t)` vs logarithm of time :math:`t`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 1])
        return x, y, True

    def viewSigmaTime(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Transient shear or extensional stress (depending on the experiment) :math:`\\sigma(t)` vs time :math:`t`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True

    def viewLogSigmaGamma(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Logarithm of the transient shear or extensional stress (depending on the experiment) :math:`\\sigma(t)` vs logarithm of the strain :math:`\\gamma`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        if "gdot" in file_parameters:
            flow_rate = float(file_parameters["gdot"])
        else:
            flow_rate = float(file_parameters["edot"])
        x[:, 0] = np.log10(dt.data[:, 0] * flow_rate)  # compute strain
        y[:, 0] = np.log10(dt.data[:, 1])
        return x, y, True

    def viewSigmaGamma(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Transient shear or extensional stress (depending on the experiment) :math:`\\sigma(t)` vs strain :math:`\\gamma`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        if "gdot" in file_parameters:
            flow_rate = float(file_parameters["gdot"])
        else:
            flow_rate = float(file_parameters["edot"])
        x[:, 0] = dt.data[:, 0] * flow_rate  # compute strain
        y[:, 0] = dt.data[:, 1]
        return x, y, True

    def view_flowcurve(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """:math:`\\sigma(t_{\\to\\infty})` vs flow rate"""

        try:
            flow_rate = float(file_parameters["gdot"])
        except KeyError:
            flow_rate = float(file_parameters["edot"])
        x = np.zeros((1, 1))
        y = np.zeros((1, 1))
        x[0, 0] = flow_rate
        y[0, 0] = dt.data[-1, 1]
        return x, y, True
