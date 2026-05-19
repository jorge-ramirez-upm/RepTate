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
"""Module ApplicationUniversalViewer

Definition of a new Application for viewing generic txt data

"""

from typing import Any, ClassVar, cast

from RepTate.gui.QApplicationWindow import QApplicationWindow
from RepTate.core.View import View
from RepTate.core.FileType import TXTColumnFile
from RepTate.core.typing import ApplicationLike, ApplicationManagerLike, DataTableLike, FileParameters, ViewResult
from RepTate.core.expression_parser import evaluate_expression

import numpy as np
import configparser


class ViewParseExpression(object):
    """Auxiliary class to define views that must parse an expression before being shown."""

    def __init__(
        self,
        name: str = "",
        n: int = 1,
        col_names: list[str] = [],
        xexpr: list[str] = [],
        yexpr: list[str] = [],
        parent: ApplicationLike | None = None,
    ) -> None:
        self.parent: ApplicationLike = cast(ApplicationLike, parent)
        self.name: str = name
        self.n: int = n
        self.col_names: list[str] = col_names
        self.xexpr: list[str] = xexpr
        self.yexpr: list[str] = yexpr

    def _prepare_expression_variables(
        self,
        expression: str,
        dt: DataTableLike,
    ) -> tuple[str, dict[str, Any]]:
        """Replace column references and prepare variables for expression evaluation.

        Columns are referenced as ``{column_name}`` in the ini file. They are
        converted to generated internal names before passing the expression to
        the common expression parser.
        """
        variables: dict[str, Any] = {}
        expression = expression.replace("^", "**")

        for i, col_name in enumerate(self.col_names):
            placeholder = "{" + col_name + "}"
            symbol = f"COL{i}"

            if placeholder in expression:
                expression = expression.replace(placeholder, symbol)
                variables[symbol] = dt.data[:, i]

        return expression, variables

    def _evaluate_view_expression(
        self,
        expression: str,
        dt: DataTableLike,
        file_parameters: FileParameters,
    ) -> Any:
        expression, variables = self._prepare_expression_variables(expression, dt)

        return evaluate_expression(
            expression,
            variables,
            file_parameters,
        )

    def view(
        self,
        dt: DataTableLike,
        file_parameters: FileParameters,
    ) -> ViewResult:
        """Process the expressions and produce the view."""
        x = np.zeros((dt.num_rows, self.n))
        y = np.zeros((dt.num_rows, self.n))

        for i in range(self.n):
            if i < len(self.xexpr):
                x_expression = self.xexpr[i]
            else:
                x_expression = self.xexpr[0]

            try:
                x[:, i] = self._evaluate_view_expression(
                    x_expression,
                    dt,
                    file_parameters,
                )
            except Exception:
                self.parent.logger.exception(
                    "Error in view (%s) x[%d]",
                    self.name,
                    i,
                )

            try:
                y[:, i] = self._evaluate_view_expression(
                    self.yexpr[i],
                    dt,
                    file_parameters,
                )
            except Exception:
                self.parent.logger.exception(
                    "Error in view (%s) y[%d]",
                    self.name,
                    i,
                )

        return x, y, True


class ApplicationUniversalViewer(QApplicationWindow):
    """Application for viewing generic txt data described by ini files"""

    appname: ClassVar[str] = "Universal Viewer"
    description: ClassVar[str] = "Universal Viewer Application"  # used in the command-line Reptate
    extension: ClassVar[str] = ""  # drag and drop this extension automatically opens this application
    # html_help_file = ''

    def __init__(
        self,
        name: str = "Universal Viewer",
        parent: ApplicationManagerLike | None = None,
        inifile: Any = None,
        nplot_max: int = 1,
    ) -> None:
        """**Constructor**"""

        self.inifile: Any = inifile
        self.config: configparser.ConfigParser = configparser.ConfigParser()
        self.config.read_file(open(inifile))

        super().__init__(name, parent, nplot_max=nplot_max)

        # FILES
        # set the type of files that ApplicationUniversalViewer can open
        ftype = TXTColumnFile(
            name=self.config.get("file1", "name"),
            extension=self.config.get("file1", "extension").split(".")[1],
            description=self.config.get("file1", "name"),
            col_names=self.config.get("file1", "Colnames").split(","),
            basic_file_parameters=self.config.get("file1", "Parameters").split(","),
            col_units=["units_col1", "units_col2"],
        )
        self.filetypes[ftype.extension] = ftype

        # VIEWS
        # set the views that can be selected in the view combobox
        nv: int = 0
        moreviews: bool = True
        self.viewclasses: dict[str, ViewParseExpression] = {}
        while moreviews:
            if "view%d" % (nv + 1) in self.config.sections():
                nv += 1
                xexpr = self.config.get("view%d" % nv, "xexpr").split(",")
                yexpr = self.config.get("view%d" % nv, "yexpr").split(",")
                name, x_label, y_label = self.config.get("view%d" % nv, "name").split(",")
                x_units, y_units = self.config.get("view%d" % nv, "units", fallback="-,-").split(",")
                n = self.config.getint("view%d" % nv, "n", fallback=1)
                self.viewclasses[name] = ViewParseExpression(
                    name,
                    n,
                    col_names=ftype.col_names,
                    xexpr=xexpr,
                    yexpr=yexpr,
                    parent=cast(ApplicationLike, self),
                )
                log_x = self.config.getboolean("view%d" % nv, "logx", fallback=False)
                log_y = self.config.getboolean("view%d" % nv, "logy", fallback=False)
                snames = self.config.get("view%d" % nv, "snames", fallback=",,,,,,,,,,,,").split(",")
                self.views[name] = View(
                    name=name,
                    description=name,
                    x_label=x_label,
                    y_label=y_label,
                    x_units=x_units,
                    y_units=y_units,
                    log_x=log_x,
                    log_y=log_y,
                    view_proc=self.viewclasses[name].view,
                    n=n,
                    snames=snames,
                )
            else:
                moreviews = False

        # set multiviews
        # default view order in multiplot views, set nplots=1 for single view
        self.nplots = self.config.getint("application", "ncharts")
        self.multiviews = []
        for i in range(self.nplot_max):
            # set views in the same order as declared above
            self.multiviews.append(list(self.views.values())[i])
        self.multiplots.reorg_fig(self.nplots)

        # THEORIES
        self.add_common_theories()  # Add basic theories to the application

        # set the current view
        self.set_views()

    def viewyx(self, dt: DataTableLike, file_parameters: FileParameters) -> ViewResult:
        """Example View function"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True
