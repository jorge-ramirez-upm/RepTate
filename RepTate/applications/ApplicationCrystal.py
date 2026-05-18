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
"""Module ApplicationCrystal

Module for handling data from start up of shear and extensional flow experiments with flow induced crystallisation.

"""

from typing import Any, ClassVar

from RepTate.gui.QApplicationWindow import QApplicationWindow
from RepTate.core.View import AxisSpec, View
from RepTate.core.File import FileParameterSpec
from RepTate.core.FileType import TXTColumnFile
from RepTate.core.typing import ApplicationManagerLike, DataTableLike, FileParameters, ViewResult
import numpy as np


class ApplicationCrystal(QApplicationWindow):
    """Module for handling data from start up of shear and extensional flow experiments with flow induced crystallisation."""

    appname: ClassVar[str] = "Crystal"
    description: ClassVar[str] = "Flow induced Crystallisation"
    extension: ClassVar[str] = "shearxs uextxs shear uext"
    html_help_file: ClassVar[str] = "http://reptate.readthedocs.io/manual/Applications/Crystal/Crystal.html"

    def __init__(self, name: str = "Crystal", parent: ApplicationManagerLike | None = None) -> None:
        """**Constructor**"""
        from RepTate.theories.TheoryGoPolyStrand import TheoryGoPolyStrand
        from RepTate.theories.TheorySmoothPolyStrand import TheorySmoothPolyStrand

        super().__init__(name, parent)

        time_units: tuple[str, ...] = ("ns", "μs", "ms", "s", "min", "h")
        stress_units: tuple[str, ...] = ("Pa", "kPa", "MPa", "bar", "atm")
        viscosity_units: tuple[str, ...] = ("Pa.s", "kPa.s")
        deformation_rate_units: tuple[str, ...] = ("1/s", "s-1", "s^-1", "s⁻¹", "1/min", "1/h")
        nucleation_rate_units: tuple[str, ...] = ("1/s/m3", "1/s/cm3", "1/s/mm3", "1/s/um3", "1/s/nm3")
        unit_density_units: tuple[str, ...] = ("1/m3", "1/cm3", "1/mm3", "1/um3", "1/nm3")

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
        self.views["Ndot(t) [log-log]"] = View(
            name="Ndot(t) [log-log]",
            description="Nucleation rate (log-log)",
            x_label="t",
            y_label=r"$\dot{N}$",
            x_units="s",
            y_units=r"s$^{-1}$m$^{-3}$",
            log_x=True,
            log_y=True,
            view_proc=self.viewNdot,
            n=1,
            snames=["Ndot"],
            x_axis=AxisSpec(label="t", internal_unit="s", unit_choices=time_units),
            y_axis=AxisSpec(
                label=r"$\dot{N}$",
                internal_unit="1/s/m3",
                unit_choices=nucleation_rate_units,
            ),
        )
        self.views["N(t) [log-log]"] = View(
            name="N(t) [log-log]",
            description="Nucleation density (log-log)",
            x_label="t",
            y_label="N",
            x_units="s",
            y_units=r"m$^{-3}$",
            log_x=True,
            log_y=True,
            view_proc=self.viewNt,
            n=1,
            snames=["N"],
            x_axis=AxisSpec(label="t", internal_unit="s", unit_choices=time_units),
            y_axis=AxisSpec(
                label="N",
                internal_unit="1/m3",
                unit_choices=unit_density_units,
            ),
        )
        self.views["phiX(t) [log-log]"] = View(
            name="phiX(t) [log-log]",
            description="Crystal fraction (log-log)",
            x_label="t",
            y_label=r"$\phi_X$",
            x_units="s",
            y_units="-",
            log_x=True,
            log_y=True,
            view_proc=self.viewphiX,
            n=1,
            snames=["phiX"],
            x_axis=AxisSpec(label="t", internal_unit="s", unit_choices=time_units),
        )
        self.views["Ndot(t) [log-lin]"] = View(
            name="Ndot(t) [log-lin]",
            description="Nucleation rate (log-lin)",
            x_label="t",
            y_label=r"$\dot{N}$",
            x_units="s",
            y_units=r"s$^{-1}$m$^{-3}$",
            log_x=True,
            log_y=False,
            view_proc=self.viewNdot,
            n=1,
            snames=["Ndot"],
            x_axis=AxisSpec(label="t", internal_unit="s", unit_choices=time_units),
            y_axis=AxisSpec(
                label=r"$\dot{N}$",
                internal_unit="1/s/m3",
                unit_choices=nucleation_rate_units,
            ),
        )
        self.views["N(t) [log-lin]"] = View(
            name="N(t) [log-lin]",
            description="Nucleation density (log-lin)",
            x_label="t",
            y_label="N",
            x_units="s",
            y_units=r"m$^{-3}$",
            log_x=True,
            log_y=False,
            view_proc=self.viewNt,
            n=1,
            snames=["N"],
            x_axis=AxisSpec(label="t", internal_unit="s", unit_choices=time_units),
            y_axis=AxisSpec(
                label="N",
                internal_unit="1/m3",
                unit_choices=unit_density_units,
            ),
        )
        self.views["phiX(t) [log-lin]"] = View(
            name="phiX(t) [log-lin]",
            description="Crystal fraction (log-lin)",
            x_label="t",
            y_label=r"$\phi_X$",
            x_units="s",
            y_units="-",
            log_x=True,
            log_y=False,
            view_proc=self.viewphiX,
            n=1,
            snames=["phiX"],
            x_axis=AxisSpec(label="t", internal_unit="s", unit_choices=time_units),
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
        self.views["sigma(t) [log-lin]"] = View(
            name="sigma(t) [log-lin]",
            description="transient shear stress vs time (log-lin)",
            x_label="t",
            y_label=r"$\sigma^+$",
            x_units="s",
            y_units="Pa",
            log_x=True,
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
        self.views["Steady Nucleation"] = View(
            name="Steady Nucleation",
            description="Steady state nucleation rate vs flow rate",
            x_label="Flow rate",
            y_label=r"$\dot{N}$",
            x_units=r"s$^{-1}$",
            y_units=r"s$^{-1}$m$^{-3}$",
            log_x=True,
            log_y=True,
            view_proc=self.view_steadyNuc,
            n=1,
            snames=["Ndot"],
            with_thline=False,
            filled=True,
            x_axis=AxisSpec(
                label="Flow rate",
                internal_unit="1/s",
                unit_choices=deformation_rate_units,
            ),
            y_axis=AxisSpec(
                label=r"$\dot{N}$",
                internal_unit="1/s/m3",
                unit_choices=nucleation_rate_units,
            ),
        )

        # set multiviews
        self.nplots = 4
        self.multiviews = []
        for i in range(self.nplot_max):
            # set views in the same order as declared above
            self.multiviews.append(list(self.views.values())[i])
        self.multiplots.reorg_fig(self.nplots)

        # FILES
        ftype = TXTColumnFile(
            name="Start-up of shear flow with crystallisation",
            extension="shearxs",
            description="Shear crystallisation files",
            col_names=["t", "sigma_xy", "Ndot", "phi_X", "N"],
            basic_file_parameters=["gdot", "T", "tstop"],
            # col_units = ["s", r"Pa$\cdot$s", r"s$^{-1}$m$^{-3}$", "-", r"m$^{-3}$"],
            col_units=["s", "Pa.s", "1/s/m³", "-", "1/m³"],
            file_parameter_specs=[
                FileParameterSpec("gdot", "deformation_rate", "1/s", "1/s"),
                FileParameterSpec("T", "temperature", "ºC", "ºC"),
                FileParameterSpec("tstop", "time", "s", "s"),
            ],
        )
        self.filetypes[ftype.extension] = ftype
        ftype = TXTColumnFile(
            name="Elongation flow with crystallisation",
            extension="uextxs",
            description="Elongation crystallisation files",
            col_names=["t", "N1", "Ndot", "phi_X", "N"],
            basic_file_parameters=["gdot", "T", "tstop"],
            # col_units=["s", r"Pa$\cdot$s", r"s$^{-1}$m$^{-3}$", "-", r"m$^{-3}$"],
            col_units=["s", "Pa.s", "1/s/m³", "-", "1/m³"],
            file_parameter_specs=[
                FileParameterSpec("gdot", "deformation_rate", "1/s", "1/s"),
                FileParameterSpec("T", "temperature", "ºC", "ºC"),
                FileParameterSpec("tstop", "time", "s", "s"),
            ],
        )

        # THEORIES
        self.theories[TheoryGoPolyStrand.thname] = TheoryGoPolyStrand
        self.theories[TheorySmoothPolyStrand.thname] = TheorySmoothPolyStrand
        self.add_common_theories()

        # set the current view
        self.set_views()

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

    def viewNdot(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Nucleation rate as a function of time on log axis :math:`\\dot{N}(t)` vs time :math:`t` (x-axis on log scale by default)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 2]
        return x, y, True

    def viewNt(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Nucleation density as a function of time on log axis :math:`N(t)` vs time :math:`t` (x-axis on log scale by default)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 4]
        return x, y, True

    def viewphiX(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Crystal fraction as a function of time on log axis :math:`\\phi_X(t)` vs time :math:`t` (x-axis on log scale by default)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 3]
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

    def view_steadyNuc(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """:math:`\\dot{N}(t_{\\to\\infty})` vs flow rate"""

        try:
            flow_rate = float(file_parameters["gdot"])
        except KeyError:
            flow_rate = float(file_parameters["edot"])
        x = np.zeros((1, 1))
        y = np.zeros((1, 1))
        x[0, 0] = flow_rate
        y[0, 0] = dt.data[-1, 2]
        return x, y, True
