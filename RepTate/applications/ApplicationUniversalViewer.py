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
"""Module ApplicationUniversalViewer

Definition of a new Application for viewing generic txt data

"""
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Application import Application
from RepTate.gui.QApplicationWindow import QApplicationWindow
from RepTate.core.View import View
from RepTate.core.FileType import TXTColumnFile
from numpy import *
import numpy as np
import re
import configparser


class ViewParseExpression(object):
    """Auxiliary class to define views that must parse an expression before being shown"""

    def __init__(self, name="", n=1, col_names=[], xexpr=[], yexpr=[], parent=None):
        self.parent = parent
        self.name = name
        self.n = n
        self.col_names = col_names
        self.xexpr = xexpr
        self.yexpr = yexpr

        safe_list = [
            "sin",
            "cos",
            "tan",
            "arccos",
            "arcsin",
            "arctan",
            "arctan2",
            "deg2rad",
            "rad2deg",
            "sinh",
            "cosh",
            "tanh",
            "arcsinh",
            "arccosh",
            "arctanh",
            "around",
            "round_",
            "rint",
            "floor",
            "ceil",
            "trunc",
            "exp",
            "log",
            "log10",
            "fabs",
            "mod",
            "e",
            "pi",
            "power",
            "sqrt",
        ]
        self.safe_dict = {}
        for k in safe_list:
            self.safe_dict[k] = globals().get(k, None)

    def view(self, dt, file_parameters):
        """Actual function that processes the expression, extracts variables, file parameters and columns, and produces the view"""
        x = np.zeros((dt.num_rows, self.n))
        y = np.zeros((dt.num_rows, self.n))

        for i in range(self.n):
            # First we do it with x
            if i < len(self.xexpr):
                expression = self.xexpr[i].replace("^", "**")
            else:
                expression = self.xexpr[0].replace(
                    "^", "**"
                )  # For x, it is not necessary to provide all expressions
            # Find FILE PARAMETERS IN THE EXPRESSION
            fparams = re.findall("\[(.*?)\]", expression)
            for fp in fparams:
                if fp in file_parameters:
                    self.safe_dict[fp] = float(file_parameters[fp])
                else:
                    self.parent.logger.warning(
                        "File parameter not found. Review your views"
                    )
                    self.safe_dict[fp] = 0.0
            expression = expression.replace("[", "").replace("]", "")
            # Find Columns in the expression
            cols = re.findall("\{(.*?)\}", expression)
            for cl in cols:
                if cl in self.col_names:
                    ind = self.col_names.index(cl)
                    self.safe_dict[cl] = dt.data[:, ind]
                else:
                    self.parent.logger.warning("Column not found. Review your views")
                    self.safe_dict[fp] = np.zeros_like(dt.data[:, ind])
            expression = expression.replace("{", "").replace("}", "")
            try:
                x[:, i] = eval(expression, {"__builtins__": None}, self.safe_dict)
            except NameError as e:
                self.parent.logger.exception(
                    "Error in view (%s) x[%d]" % (self.name, i)
                )
            except TypeError as e:
                self.parent.logger.exception(
                    "Error in view (%s) x[%d]" % (self.name, i)
                )
            except Exception as e:
                self.parent.logger.exception(
                    "Error in view (%s) x[%d]" % (self.name, i)
                )

            # Now do the same for y
            expression = self.yexpr[i].replace("^", "**")
            # Find FILE PARAMETERS IN THE EXPRESSION
            fparams = re.findall("\[(.*?)\]", expression)
            for fp in fparams:
                if fp in file_parameters:
                    self.safe_dict[fp] = float(file_parameters[fp])
                else:
                    self.parent.logger.warning(
                        "File parameter not found. Review your views"
                    )
                    self.safe_dict[fp] = 0.0
            expression = expression.replace("[", "").replace("]", "")
            # Find Columns in the expression
            cols = re.findall("\{(.*?)\}", expression)
            for cl in cols:
                if cl in self.col_names:
                    ind = self.col_names.index(cl)
                    self.safe_dict[cl] = dt.data[:, ind]
                else:
                    self.parent.logger.warning("Column not found. Review your views")
                    self.safe_dict[fp] = np.zeros_like(dt.data[:, ind])
            expression = expression.replace("{", "").replace("}", "")
            try:
                y[:, i] = eval(expression, {"__builtins__": None}, self.safe_dict)
            except NameError as e:
                self.parent.logger.exception(
                    "Error in view (%s) y[%d]" % (self.name, i)
                )
            except TypeError as e:
                self.parent.logger.exception(
                    "Error in view (%s) y[%d]" % (self.name, i)
                )
            except Exception as e:
                self.parent.logger.exception(
                    "Error in view (%s) y[%d]" % (self.name, i)
                )

        return x, y, True


class ApplicationUniversalViewer(CmdBase):
    """Application for viewing generic txt data described by ini files"""

    appname = "Universal Viewer"
    description = "Universal Viewer Application"  # used in the command-line Reptate
    extension = ""  # drag and drop this extension automatically opens this application

    def __new__(cls, name="Universal Viewer", parent=None, inifile=None, nplot_max=1):
        """Create an instance of the GUI or CL class"""
        return (
            GUIApplicationUniversalViewer(name, parent, inifile, nplot_max)
            if (CmdBase.mode == CmdMode.GUI)
            else CLApplicationUniversalViewer(name, parent, inifile, nplot_max)
        )


class BaseApplicationUniversalViewer:
    """Base Class for both GUI and CL"""

    # html_help_file = ''
    appname = ApplicationUniversalViewer.appname

    def __init__(self, name="Universal Viewer", parent=None, inifile=None, nplot_max=1):
        """**Constructor**"""

        self.inifile = inifile
        self.config = configparser.ConfigParser()
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
        nv = 0
        moreviews = True
        self.viewclasses = {}
        while moreviews:
            if "view%d" % (nv + 1) in self.config.sections():
                nv += 1
                xexpr = self.config.get("view%d" % nv, "xexpr").split(",")
                yexpr = self.config.get("view%d" % nv, "yexpr").split(",")
                name, x_label, y_label = self.config.get("view%d" % nv, "name").split(
                    ","
                )
                x_units, y_units = self.config.get(
                    "view%d" % nv, "units", fallback="-,-"
                ).split(",")
                n = self.config.getint("view%d" % nv, "n", fallback=1)
                self.viewclasses[name] = ViewParseExpression(
                    name,
                    n,
                    col_names=ftype.col_names,
                    xexpr=xexpr,
                    yexpr=yexpr,
                    parent=self,
                )
                log_x = self.config.getboolean("view%d" % nv, "logx", fallback=False)
                log_y = self.config.getboolean("view%d" % nv, "logy", fallback=False)
                snames = self.config.get("view%d" % nv, "snames", fallback=',,,,,,,,,,,,').split(",")
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

    def viewyx(self, dt, file_parameters):
        """Example View function"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True


class CLApplicationUniversalViewer(BaseApplicationUniversalViewer, Application):
    """CL Version"""

    def __init__(self, name="Universal Viewer", parent=None, inifile=None, nplot_max=1):
        """**Constructor**"""
        super().__init__(name, parent, inifile, nplot_max)
        # usually this class stays empty


class GUIApplicationUniversalViewer(BaseApplicationUniversalViewer, QApplicationWindow):
    """GUI Version"""

    def __init__(self, name="Universal Viewer", parent=None, inifile=None, nplot_max=1):
        """**Constructor**"""
        super().__init__(name, parent, inifile, nplot_max)

        # add the GUI-specific objects here:
