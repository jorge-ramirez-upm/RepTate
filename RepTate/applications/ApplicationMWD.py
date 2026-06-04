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
"""Module ApplicationMWD

Module for handling Molecular weight distributions from GPC experiments.

"""

from typing import Any, ClassVar

from RepTate.gui.QApplicationWindow import QApplicationWindow
from RepTate.core.View import AxisSpec, View
from RepTate.core.File import FileParameterSpec
from RepTate.core.FileType import TXTColumnFile
from RepTate.core.typing import ApplicationManagerLike, DataTableLike, FileParameters, ViewResult
import numpy as np


class ApplicationMWD(QApplicationWindow):
    """Application to analyze Molecular Weight Distributions"""

    appname: ClassVar[str] = "MWD"
    description: ClassVar[str] = "Experimental Molecular weight distributions"
    extension: ClassVar[str] = "gpc"
    html_help_file: ClassVar[str] = "http://reptate.readthedocs.io/manual/Applications/MWD/MWD.html"

    def __init__(self, name: str = "MWD", parent: ApplicationManagerLike | None = None) -> None:
        """**Constructor**"""
        from RepTate.theories.TheoryDiscrMWD import TheoryDiscrMWD
        from RepTate.theories.TheoryGEX import TheoryGEX
        from RepTate.theories.TheoryLogNormal import TheoryLogNormal

        super().__init__(name, parent, nplot_max=3)

        molar_mass_units: tuple[str, ...] = ("g/mol", "kg/mol", "Da", "kDa")

        # VIEWS
        self.views["log-lin"] = View(
            name="log-lin",
            description="MWD lin W vs log M",
            x_label="M",
            y_label="dW/dlogM",
            x_units="kg/mol",
            y_units="-",
            log_x=True,
            log_y=False,
            view_proc=self.view_WM,
            n=1,
            snames=["W"],
            x_axis=AxisSpec(
                label="M",
                internal_unit="kg/mol",
                unit_choices=molar_mass_units,
            ),
        )
        self.views["log-log"] = View(
            name="log-log",
            description="MWD log W vs log M",
            x_label="log(M)",
            y_label="log(dW/dlogM)",
            x_units="kg/mol",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.view_logWM,
            n=1,
            snames=["log(W)"],
            x_axis=AxisSpec(
                label="log(M)",
                internal_unit="kg/mol",
                transform="log10",
                unit_choices=molar_mass_units,
            ),
        )
        self.views["lin-lin"] = View(
            name="lin-lin",
            description="MWD lin W vs lin M",
            x_label="M",
            y_label="dW/dlogM",
            x_units="kg/mol",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.view_WM,
            n=1,
            snames=["W"],
            x_axis=AxisSpec(
                label="M",
                internal_unit="kg/mol",
                unit_choices=molar_mass_units,
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
            "GPC Files",
            "gpc",
            "Molecular Weight Distribution",
            ["M", "W(logM)"],
            ["Mn", "Mw", "PDI"],
            ["kg/mol", "-"],
            file_parameter_specs=[
                FileParameterSpec("Mn", "molar_mass", "kg/mol", "kg/mol"),
                FileParameterSpec("Mw", "molar_mass", "kg/mol", "kg/mol"),
            ]
        )
        # ftype=TXTColumnFile("GPC Files", "gpc", "Molecular Weight Distribution", ['M','W(logM)'], [], ['kDa', '-'])
        self.filetypes[ftype.extension] = ftype
        ftype = TXTColumnFile(
            "React Files",
            "reac",
            "Relaxation modulus",
            ["M", "W(logM)", "g", "br/1000C"],
            ["Mn", "Mw", "PDI"],
            ["g/mol", "-"],
        )
        self.filetypes[ftype.extension] = ftype

        # THEORIES
        self.theories[TheoryDiscrMWD.thname] = TheoryDiscrMWD
        self.theories[TheoryGEX.thname] = TheoryGEX
        self.theories[TheoryLogNormal.thname] = TheoryLogNormal
        self.add_common_theories()

        # set the current view
        self.set_views()
        self.finalize_application_setup()

    def view_WM(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """:math:`W(M)` vs :math:`M`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True

    def view_logWM(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """:math:`\\log(W(M))` vs :math:`\\log(M)`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 1])
        return x, y, True
