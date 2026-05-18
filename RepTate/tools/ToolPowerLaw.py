# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Tool and Experiments
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
# Copyright (2018-2023): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module ToolPowerLaw

Tool to check the power law of some data
"""
from typing import Any, ClassVar

from RepTate.core.Parameter import Parameter, ParameterType, OptType
from RepTate.core.typing import ApplicationLike, AxesLike
from RepTate.gui.QTool import QTool


class ToolPowerLaw(QTool):
    """Check the power law of the data (or some part of it) by dividing the y coordinate by the x coordinate 
raised to n.
    """

    toolname: ClassVar[str] = "PowerLaw"
    description: ClassVar[str] = "Check the power law of the data"
    citations: ClassVar[list[str]] = []
    # html_help_file = 'http://reptate.readthedocs.io/manual/Tools/template.html'

    parameters: Any
    parent_application: ApplicationLike

    def __init__(self, name: str = "", parent_app: ApplicationLike | None = None) -> None:
        """**Constructor**"""
        super().__init__(name, parent_app)
        self.parameters["n"] = Parameter(
            name="n",
            value=1,
            description="Power law exponent",
            type=ParameterType.real,
            opt_type=OptType.const,
        )

        self.update_parameter_table()
        self.parent_application.update_all_ds_plots()

        # add widgets specific to the Tool here:


    def destructor(self) -> None:
        """If the tool needs to clear up memory in a very special way, fill up the contents of this function.
If not, you can safely delete it."""
        pass

    def calculate(
        self, x: Any, y: Any, ax: AxesLike | None = None, color: Any = None, file_parameters: Any = []
    ) -> tuple[Any, Any]:
        """Returns y divided by x^n, according to the view"""
        n = self.parameters["n"].value
        return x, y / x ** n

