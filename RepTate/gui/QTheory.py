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
"""Module QTheory

Module that defines the GUI counterpart of the class Theory.

"""
import sys
import os
import enum
import time
import getpass
import ast
import numpy as np
from scipy.optimize import (
    curve_fit,
    basinhopping,
    dual_annealing,
    differential_evolution,
    shgo,
    brute,
)
from scipy.stats.distributions import t
from scipy.interpolate import interp1d

from PySide6.QtUiTools import loadUiType
import RepTate
from RepTate.core.CmdBase import CmdBase, CalcMode
from os.path import dirname, join, abspath
from PySide6.QtWidgets import (
    QWidget,
    QTabWidget,
    QTreeWidgetItem,
    QFrame,
    QHeaderView,
    QMessageBox,
    QDialog,
    QVBoxLayout,
    QRadioButton,
    QDialogButtonBox,
    QButtonGroup,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QFileDialog,
    QApplication,
    QAbstractItemView,
)
from PySide6.QtCore import Qt, QObject, QThread, Signal
from PySide6.QtGui import QIntValidator, QDoubleValidator, QCursor, QTextCursor
from RepTate.core.Parameter import OptType, ParameterType
from RepTate.core.DataTable import DataTable
from RepTate.core.DraggableArtists import DraggableVLine, DraggableHLine, DragType
from RepTate.tools.ToolMaterialsDatabase import check_chemistry, get_all_parameters
import logging
from collections import OrderedDict
from math import ceil, floor, log
import RepTate
from html.parser import HTMLParser

if getattr(sys, "frozen", False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    PATH = sys._MEIPASS
else:
    PATH = dirname(abspath(__file__))
Ui_TheoryTab, QWidget = loadUiType(join(PATH, "theorytab.ui"))
from RepTate.gui.fittingoptions import Ui_Dialog
import RepTate.gui.errorcalculationoptions


# IMPORT FROM THEORY
class MLStripper(HTMLParser):
    """Remove HTML tags from string"""

    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return "".join(self.fed)


class MinimizationMethod(enum.Enum):
    """Method used during minimization

    Parameters can be:
        - ls: Non-linear Least Squares (default)
        - basinhopping: Basin-hopping method
        - dualannealing: Dual-Annealing method
        - diffevol: Differential Evolution method
        - SHGO: simplicial homology global optimization
        - bruteforce: Find the minimum on a hypergrid

    """

    ls = 0
    basinhopping = 1
    dualannealing = 2
    diffevol = 3
    SHGO = 4
    bruteforce = 5
    types = ["ls", "basinhopping", "dualannealing", "diffevol", "SHGO", "bruteforce"]
    descriptions = [
        "Non-linear Least Squares",
        "Basin-hopping method",
        "Dual-Annealing",
        "Differential Evolution",
        "Simplicial Homology Global Optimization",
        "Find the minimum on a hypergrid",
    ]

    def __str__(self):
        stt = ""
        N = len(self.types.value)
        # for i, k in enumerate(self.types.value):
        #     stt += Fore.RED + k + Fore.RESET + ": " + self.descriptions.value[i] + "\n"
        return stt


class ErrorCalculationMethod(enum.Enum):
    """Method to determine the error of a theory calculation.

    Options are:
        - View1: Use current view number 1 in the application.
        - RawData: Use the data table as defined by the application.
        - AllViews: Use all active views.
    """

    View1 = 0
    RawData = 1
    AllViews = 2


class EndComputationRequested(Exception):
    """Exception class to end computations"""

    pass


# END IMPORT FROM THEORY


# def trap_exc_during_debug(*args):
#     # when app raises uncaught exception, print info
#     print(args)

# # install exception hook: without this, uncaught exception would cause application to exit
# sys.excepthook = trap_exc_during_debug


class EditThParametersDialog(QDialog):
    """Create the form that is used to modify the theorys parameters"""

    def __init__(self, parent, p_name):
        super().__init__(parent)
        self.parent_theory = parent
        self.tabs = QTabWidget()
        self.all_pattr = {}
        for pname in self.parent_theory.parameters:
            tab = self.create_param_tab(pname)
            self.tabs.addTab(tab, pname)
            if pname == p_name:
                index = self.tabs.indexOf(tab)
        self.tabs.setCurrentIndex(index)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tabs)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("Theory Parameters")

    def create_param_tab(self, p_name):
        """Create a form to set the new values of the file parameters"""
        tab = QWidget()
        layout = QFormLayout()

        p = self.parent_theory.parameters[p_name]
        p_attributes = p.__dict__
        attr_dict = {}
        a_new = []
        i = 0
        for attr_name in p_attributes:  # loop over the Parameters attributes
            if attr_name == "type":
                cb = QComboBox()
                cb.addItem("real")
                cb.addItem("integer")
                cb.addItem("discrete_real")
                cb.addItem("discrete_integer")
                cb.addItem("boolean")
                cb.addItem("string")
                # cb.setCurrentText('%s'.split(".")[-1] % p_attributes[attr_name])
                s = "%s" % p_attributes[attr_name]
                cb.setCurrentText(s.split(".")[-1])
                a_new.append(cb)
            elif attr_name == "opt_type":
                cb = QComboBox()
                cb.addItem("opt")
                cb.addItem("nopt")
                cb.addItem("const")
                # cb.setCurrentText('%s'.split(".")[-1] % p_attributes[attr_name])
                s = "%s" % p_attributes[attr_name]
                cb.setCurrentText(s.split(".")[-1])
                a_new.append(cb)
            elif attr_name == "display_flag":
                cb = QComboBox()
                cb.addItem("True")
                cb.addItem("False")
                cb.setCurrentText("%s" % p_attributes[attr_name])
                a_new.append(cb)
            elif attr_name in ["value", "error"]:
                continue
            else:
                qline = QLineEdit()
                if attr_name in ["name", "description"]:
                    qline.setReadOnly(True)
                a_new.append(qline)
                a_new[i].setText("%s" % p_attributes[attr_name])
            layout.addRow("%s:" % attr_name, a_new[i])
            attr_dict[attr_name] = a_new[i]
            i += 1
        tab.setLayout(layout)
        self.all_pattr[p_name] = attr_dict
        return tab


class CalculationThread(QObject):
    sig_done = Signal()

    def __init__(self, fthread, *args):
        super().__init__()
        self.args = args
        self.function = fthread

    def work(self):
        self.function(*self.args)
        self.sig_done.emit()


class GetModesDialog(QDialog):
    def __init__(self, parent=None, th_dict={}):
        super(GetModesDialog, self).__init__(parent)

        self.setWindowTitle("Get Maxwell modes")
        layout = QVBoxLayout(self)

        self.btngrp = QButtonGroup()

        for item in th_dict.keys():
            rb = QRadioButton(item, self)
            layout.addWidget(rb)
            self.btngrp.addButton(rb)

        # select first button by default
        rb = self.btngrp.buttons()[0]
        rb.setChecked(True)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


class QTheory(QWidget, Ui_TheoryTab):
    """Abstract class that defines a theory"""

    thname = ""
    """ thname {str} -- Theory name """
    description = ""
    """ description {str} -- Description of theory """
    citations = []
    """ citations {list of str} -- Articles that should be cited """
    doi = []
    """ doicode {list of str} -- Doi code of the article """
    nfev = 0
    """ nfev {int} -- Number of function evaluations """

    print_signal = Signal(str)

    def __init__(self, name="QTheory", parent_dataset=None, axarr=None):
        """
        **Constructor**

        The following variables should be set by the particular realization of the theory:
            - parameters     (dict): Parameters of the theory
            - function       (func): Function that calculates the theory
            - min            (real): min for integration/calculation
            - max            (real): max
            - npoints         (int): Number of points to calculate
            - point_distribution   : all_points, linear, log
            - dt             (real): default time step
            - dt_min         (real): minimum time step for adaptive algorithms
            - eps            (real): precision for adaptive algorithms
            - integration_method   : Euler, RungeKutta5, AdaptiveDt
            - stop_steady    (bool): Stop calculation if steady state of component 0 is attained

        Keyword Arguments:
            - name {str} -- Name of theory (default: {"Theory"})
            - parent_dataset {DataSet} -- DataSet that contains the Theory (default: {None})
            - ax {matplotlib axes} -- matplotlib graph (default: {None})
        """
        QWidget.__init__(self)
        Ui_TheoryTab.__init__(self)
        # Theory.__init__(self, name=name, parent_dataset=parent_dataset, axarr=axarr)
        # super().__init__(name=name, parent_dataset=parent_dataset, axarr=axarr)
        self.setupUi(self)

        self.name = name
        self.parent_dataset = parent_dataset
        self.axarr = axarr
        self.ax = axarr[0]  # theory calculation only on this plot
        self.parameters = (
            OrderedDict()
        )  # keep the dictionary key in order for the parameter table
        self.tables = {}
        self.function = None
        self.active = True  # defines if the theory is plotted
        self.calculate_is_busy = False
        self.axarr[0].autoscale(False)
        self.autocalculate = True
        self.extra_data = {}  # Dictionary saved during "Save Project"

        # THEORY OPTIONS
        self.npoints = 100
        self.dt = 0.001
        self.dt_min = 1e-6
        self.eps = 1e-4
        self.stop_steady = False
        self.is_fitting = False
        self.has_modes = False

        # LOGGING STUFF
        self.logger = logging.getLogger(
            self.parent_dataset.logger.name + "." + self.name
        )
        self.logger.debug("New " + self.thname + " Theory")
        # np.seterr(all="call")
        np.seterrcall(self.write)

        ax = self.ax

        # XRANGE for FIT
        self.xmin = -np.inf
        self.xmax = np.inf
        self.xrange = ax.axvspan(
            self.xmin, self.xmax, facecolor="yellow", alpha=0.3, visible=False
        )
        self.xminline = ax.axvline(
            self.xmin, color="black", linestyle="--", marker="o", visible=False
        )
        self.xmaxline = ax.axvline(
            self.xmax, color="black", linestyle="--", marker="o", visible=False
        )
        self.xminlinedrag = DraggableVLine(
            self.xminline, DragType.horizontal, self.change_xmin, self
        )
        self.xmaxlinedrag = DraggableVLine(
            self.xmaxline, DragType.horizontal, self.change_xmax, self
        )
        self.is_xrange_visible = False

        # YRANGE for FIT
        self.ymin = -np.inf
        self.ymax = np.inf
        self.yrange = ax.axhspan(
            self.ymin, self.ymax, facecolor="pink", alpha=0.3, visible=False
        )
        self.yminline = ax.axhline(
            self.ymin, color="black", linestyle="--", marker="o", visible=False
        )
        self.ymaxline = ax.axhline(
            self.ymax, color="black", linestyle="--", marker="o", visible=False
        )
        self.yminlinedrag = DraggableHLine(
            self.yminline, DragType.vertical, self.change_ymin, self
        )
        self.ymaxlinedrag = DraggableHLine(
            self.ymaxline, DragType.vertical, self.change_ymax, self
        )
        self.is_yrange_visible = False

        self.setup_default_minimization_options()
        self.setup_default_error_calculation_options()

        # Pre-create as many tables as files in the dataset
        for f in parent_dataset.files:
            self.tables[f.file_name_short] = DataTable(axarr, "TH-" + f.file_name_short)
            # initiallize theory table: important for 'single_file' theories
            ft = f.data_table
            tt = self.tables[f.file_name_short]
            tt.num_columns = ft.num_columns
            tt.num_rows = ft.num_rows
            tt.data = np.zeros((tt.num_rows, tt.num_columns))

        self.do_cite("")

        self.print_signal.connect(
            self.print_qtextbox
        )  # Asynchronous print when using multithread
        # flag for requesting end of computations
        self.stop_theory_flag = False

        # build the therory widget
        self.thParamTable.setIndentation(0)
        self.thParamTable.setColumnCount(3)
        self.thParamTable.setHeaderItem(
            QTreeWidgetItem(["Parameter", "Value", "Error"])
        )
        # self.thParamTable.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.thParamTable.header().resizeSections(QHeaderView.ResizeToContents)
        self.thParamTable.setAlternatingRowColors(True)
        self.thParamTable.setFrameShape(QFrame.NoFrame)
        self.thParamTable.setFrameShadow(QFrame.Plain)
        self.thParamTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.thTextBox.setReadOnly(True)
        self.thTextBox.setOpenExternalLinks(True)
        self.thTextBox.setContextMenuPolicy(Qt.CustomContextMenu)
        self.thTextBox.customContextMenuRequested.connect(self.thtextbox_context_menu)

        self.thread_calc_busy = False
        self.thread_fit_busy = False

        # Setup Theory Parameters Dialog
        self.fittingoptionsdialog = QDialog()
        self.fittingoptionsdialog.ui = Ui_Dialog()
        self.fittingoptionsdialog.ui.setupUi(self.fittingoptionsdialog)
        self.populate_default_minimization_options()

        # Setup Error Calculation Options
        self.errorcalculationdialog = QDialog()
        self.errorcalculationdialog.ui = RepTate.gui.errorcalculationoptions.Ui_Dialog()
        self.errorcalculationdialog.ui.setupUi(self.errorcalculationdialog)
        self.populate_default_error_calculation_options()

        connection_id = self.thParamTable.itemDoubleClicked.connect(
            self.onTreeWidgetItemDoubleClicked
        )
        connection_id = self.thParamTable.itemChanged.connect(
            self.handle_parameterItemChanged
        )

    def write(self, type, flag):
        """Write numpy error logs to the logger"""
        self.logger.info("numpy: %s (flag %s)" % (type, flag))

    def setup_default_minimization_options(self):
        # MINIMIZATION OPTIONS
        self.mintype = MinimizationMethod.ls
        self.LSmethod = "trf"
        self.LSjac = "2-point"
        self.LSftol = 1e-8
        self.LSxtol = 1e-8
        self.LSgtol = 1e-8
        self.LSloss = "linear"
        self.LSf_scale = 1.0
        self.LSmax_fnev = None
        self.LStr_solver = None
        self.basinniter = 100
        self.basinT = 1.0
        self.basinstepsize = 0.5
        self.basininterval = 50
        self.basinniter_success = None
        self.basinseed = None
        self.annealmaxiter = 1000
        self.annealinitial_temp = 5230.0
        self.annealrestart_temp_ratio = 2e-5
        self.annealvisit = 2.62
        self.annealaccept = -5.0
        self.annealmaxfun = 10000000
        self.annealseed = None
        self.annealno_local_search = False
        self.diffevolstrategy = "best1bin"
        self.diffevolmaxiter = 1000
        self.diffevolpopsize = 15
        self.diffevoltol = 0.01
        self.diffevolmutation = (0.5, 1)
        self.diffevolrecombination = 0.7
        self.diffevolseed = None
        self.diffevolpolish = True
        self.diffevolinit = "latinhypercube"
        self.diffevolatol = 0
        self.diffevolupdating = "immediate"
        self.SHGOn = 100
        self.SHGOiters = 1
        self.SHGOmaxfev = None
        self.SHGOf_min = None
        self.SHGOf_tol = 1e-4
        self.SHGOmaxiter = None
        self.SHGOmaxev = None
        self.SHGOmaxtime = None
        self.SHGOminhgrd = None
        self.SHGOminimize_every_iter = False
        self.SHGOlocal_iter = False
        self.SHGOinfty_constraints = True
        self.SHGOsampling_method = "simplicial"
        self.BruteNs = 20

    def setup_default_error_calculation_options(self):
        self.errormethod = ErrorCalculationMethod.View1
        self.normalizebydata = False

    def destructor(self):
        """If the theory needs to erase some memory in a special way, any
        child theory must rewrite this funcion"""
        pass

    def precmd(self, line):
        """Calculations before the theory is calculated

        This function could be erased
        This method is called after the line has been input but before
        it has been interpreted. If you want to modifdy the input line
        before execution (for example, variable substitution) do it here."""
        super(Theory, self).precmd(line)
        return line

    def update_parameter_table(self):
        """
        Added so that Maxwell modes works in CL
        """
        pass

    def handle_actionCalculate_Theory(self):
        """Used only in non GUI mode"""
        self.do_calculate("")

    def request_stop_computations(self):
        """Called when user wants to terminate the current computation"""
        self.Qprint("<font color=red><b>Stop current calculation requested</b></font>")
        self.stop_theory_flag = True

    def do_calculate(self, line, timing=True):
        """Calculate the theory"""
        if self.calculate_is_busy:
            return
        if not self.tables:
            return

        self.calculate_is_busy = True
        self.start_time_cal = time.time()
        th_files = self.theory_files()
        for f in self.parent_dataset.files:
            if f in th_files:
                if self.stop_theory_flag:
                    break
                if f.with_extra_x:
                    data_copy = f.data_table.data.copy()
                    self.extend_xrange(f)
                self.function(f)
                if f.with_extra_x:
                    # restore f
                    f.data_table.data = data_copy
                    f.data_table.num_rows = data_copy.shape[0]
            elif self.single_file:
                # delete theory data of other files
                tt = self.tables[f.file_name_short]
                tt.data = np.empty((tt.num_rows, tt.num_columns))
                tt.data[:] = np.nan

        if not self.is_fitting:
            self.do_plot(line)
            self.do_error(line)
        if timing:
            self.Qprint(
                """<i>---Calculated in %.3g seconds---</i><br>"""
                % (time.time() - self.start_time_cal)
            )
            self.do_cite("")
        self.calculate_is_busy = False

    def extend_xrange(self, fcopy):
        """Extend the xrange of the fcopy data"""
        # xmin/xmax of current data
        ncol = fcopy.data_table.data.shape[1]
        xmin = fcopy.data_table.data[:, 0][0]
        xmax = fcopy.data_table.data[:, 0][-1]
        try:
            thmin = float(fcopy.theory_xmin)
        except ValueError:
            fcopy.nextramin = 0  # number of extra rows added left
        else:
            if thmin < xmin:
                if 0 < thmin and fcopy.theory_logspace:
                    xextra_min = np.logspace(
                        np.log10(thmin), np.log10(xmin), fcopy.th_num_pts
                    )[:-1]
                else:
                    xextra_min = np.linspace(thmin, xmin, fcopy.th_num_pts)[:-1]
                fcopy.nextramin = len(xextra_min)
                data_min = np.zeros((len(xextra_min), ncol))
                data_min[:, 0] = xextra_min
                fcopy.data_table.data = np.concatenate(
                    (data_min, fcopy.data_table.data)
                )

        try:
            thmax = float(fcopy.theory_xmax)
        except ValueError:
            fcopy.nextramax = 0  # number of extra rows added right
        else:
            if thmax > xmax:
                if 0 < thmax and fcopy.theory_logspace:
                    xextra_max = np.logspace(
                        np.log10(xmax), np.log10(thmax), fcopy.th_num_pts
                    )[1:]
                else:
                    xextra_max = np.linspace(xmax, thmax, fcopy.th_num_pts)[1:]
                fcopy.nextramax = len(xextra_max)
                data_max = np.zeros((len(xextra_max), ncol))
                data_max[:, 0] = xextra_max
                fcopy.data_table.data = np.concatenate(
                    (fcopy.data_table.data, data_max)
                )
        fcopy.data_table.num_rows = fcopy.data_table.data.shape[0]

    def get_non_extended_th_table(self, f):
        """return a copy of the theory table associated with f, where the extra rows are deleted"""
        if f.with_extra_x:
            tmp_dt = DataTable(axarr=[])
            nrow = self.tables[f.file_name_short].num_rows
            tmp_dt.data = self.tables[f.file_name_short].data[
                f.nextramin : nrow - f.nextramax, :
            ]
            tmp_dt.num_rows = tmp_dt.data.shape[0]
            tmp_dt.num_columns = tmp_dt.data.shape[1]
            return tmp_dt
        else:
            return self.tables[f.file_name_short]

    def theory_files(self):
        f_list = []
        if self.single_file:
            selected_file = self.parent_dataset.selected_file
            if selected_file:
                if selected_file.active:
                    f_list.append(
                        self.parent_dataset.selected_file
                    )  # use the selected/highlighted file if active
        if (
            not f_list
        ):  # there is no selected file or it is inactive or single_file=False
            for f in self.parent_dataset.files:
                if f.active:
                    f_list.append(f)
                    if self.single_file:
                        break
        return f_list

    def do_error(self, line):
        """Report the error of the current theory

        Report the error of the current theory on all the files, taking into account the current selected xrange and yrange.

        File error is calculated as the mean square of the residual, averaged over all points in the file. Total error is the mean square of the residual, averaged over all points in all files.
        """
        total_error = 0
        npoints = 0
        view = self.parent_dataset.parent_application.current_view
        tools = self.parent_dataset.parent_application.tools
        # table='''<table border="1" width="100%">'''
        # table+='''<tr><th>File</th><th>Error (RSS)</th><th># Pts</th></tr>'''
        tab_data = [
            ["%-18s" % "File", "%-18s" % "Error (RSS)", "%-18s" % "# Pts"],
        ]
        for f in self.theory_files():
            if self.stop_theory_flag:
                break
            xexp, yexp, success = view.view_proc(f.data_table, f.file_parameters)
            tmp_dt = self.get_non_extended_th_table(f)
            xth, yth, success = view.view_proc(tmp_dt, f.file_parameters)
            if self.xrange.get_visible():
                conditionx = (xexp > self.xmin) * (xexp < self.xmax)
            else:
                conditionx = np.ones_like(xexp, dtype=bool)
            if self.yrange.get_visible():
                conditiony = (yexp > self.ymin) * (yexp < self.ymax)
            else:
                conditiony = np.ones_like(yexp, dtype=bool)
            conditionnaninf = (
                (~np.isnan(xexp))
                * (~np.isnan(yexp))
                * (~np.isnan(xth))
                * (~np.isnan(yth))
                * (~np.isinf(xexp))
                * (~np.isinf(yexp))
                * (~np.isinf(xth))
                * (~np.isinf(yth))
            )
            yexp = np.extract(conditionx * conditiony * conditionnaninf, yexp)
            yth = np.extract(conditionx * conditiony * conditionnaninf, yth)
            if self.normalizebydata:
                f_error = np.mean(((yth - yexp) / yexp) ** 2)
            else:
                f_error = np.mean((yth - yexp) ** 2)
            npt = len(yth)
            total_error += f_error * npt
            npoints += npt
            # table+= '''<tr><td>%-18s</td><td>%-18.4g</td><td>%-18d</td></tr>'''% (f.file_name_short, f_error, npt)
            tab_data.append(
                ["%-18s" % f.file_name_short, "%-18.4g" % f_error, "%-18d" % npt]
            )
        # table+='''</table><br>'''
        # self.Qprint(table)
        self.Qprint(tab_data)

        # count number of fitting parameters
        free_p = 0
        for p in self.parameters.values():
            if p.opt_type == OptType.opt:
                free_p += 1

        if npoints != 0 and total_error > 0:
            self.Qprint(
                "<b>TOTAL ERROR</b>: %12.5g (%d Pts)" % (total_error / npoints, npoints)
            )
            # Bayesian information criterion (BIC) penalise free parametters (overfitting)
            # Model with lowest BIC number is prefered
            self.Qprint(
                "<b>Bayesian IC</b>: %12.5g<br>"
                % (npoints * log(total_error / npoints) + free_p * log(npoints))
            )
        else:
            self.Qprint("<b>TOTAL ERROR</b>: %12s (%6d)<br>" % ("N/A", npoints))

    def do_error_interpolated(self, line):
        """Report the error of the current theory
        This routine works when the theory and the experimental data are not measured on the same points
        """
        total_error = 0
        npoints = 0
        view = self.parent_dataset.parent_application.current_view
        tools = self.parent_dataset.parent_application.tools
        tab_data = [
            ["%-18s" % "File", "%-18s" % "Error (RSS)", "%-18s" % "# Pts"],
        ]
        for f in self.theory_files():
            if self.stop_theory_flag:
                break
            xexp, yexp, success = view.view_proc(f.data_table, f.file_parameters)
            tmp_dt = self.get_non_extended_th_table(f)
            xth, yth, success = view.view_proc(tmp_dt, f.file_parameters)
            # HERE WE INTERPOLATE
            yth2 = np.zeros_like(yexp)
            for i in range(view.n):
                funcinterp = interp1d(
                    xth[:, i], yth[:, i], kind="linear"
                )  # Linear interpolation
                yth2[:, i] = funcinterp(xexp[:, i])

            if self.xrange.get_visible():
                conditionx = (xexp > self.xmin) * (xexp < self.xmax)
            else:
                conditionx = np.ones_like(xexp, dtype=bool)
            if self.yrange.get_visible():
                conditiony = (yexp > self.ymin) * (yexp < self.ymax)
            else:
                conditiony = np.ones_like(yexp, dtype=bool)
            conditionnaninf = (
                (~np.isnan(xexp))
                * (~np.isnan(yexp))
                * (~np.isnan(yth2))
                * (~np.isinf(xexp))
                * (~np.isinf(yexp))
                * (~np.isinf(yth2))
            )
            yexp = np.extract(conditionx * conditiony * conditionnaninf, yexp)
            yth2 = np.extract(conditionx * conditiony * conditionnaninf, yth2)

            if self.normalizebydata:
                f_error = np.mean(((yth2 - yexp) / yexp) ** 2)
            else:
                f_error = np.mean((yth2 - yexp) ** 2)
            npt = len(yth2)
            total_error += f_error * npt
            npoints += npt
            # table+= '''<tr><td>%-18s</td><td>%-18.4g</td><td>%-18d</td></tr>'''% (f.file_name_short, f_error, npt)
            tab_data.append(
                ["%-18s" % f.file_name_short, "%-18.4g" % f_error, "%-18d" % npt]
            )
        # table+='''</table><br>'''
        # self.Qprint(table)
        self.Qprint(tab_data)

        # count number of fitting parameters
        free_p = 0
        for p in self.parameters.values():
            if p.opt_type == OptType.opt:
                free_p += 1

        if npoints != 0 and total_error > 0:
            self.Qprint(
                "<b>TOTAL ERROR</b>: %12.5g (%d Pts)" % (total_error / npoints, npoints)
            )
            # Bayesian information criterion (BIC) penalise free parametters (overfitting)
            # Model with lowest BIC number is prefered
            self.Qprint(
                "<b>Bayesian IC</b>: %12.5g<br>"
                % (npoints * log(total_error / npoints) + free_p * log(npoints))
            )
        else:
            self.Qprint("<b>TOTAL ERROR</b>: %12s (%6d)<br>" % ("N/A", npoints))

    def fit_callback_basinhopping(self, x, f, accepted):
        if accepted and f < self.fminnow:
            self.fminnow = f
            self.Qprint("nfeval %6d f=%g" % (self.nfev, f))
        if self.stop_theory_flag:
            return True

    def fit_callback_dualannealing(self, x, f, context):
        if f < self.fminnow:
            self.fminnow = f
            self.Qprint("nfeval %6d f=%g" % (self.nfev, f))
        if self.stop_theory_flag:
            return True

    def fit_callback_diffevol(self, xk, convergence):
        self.Qprint("nfeval %6d frac=%g" % (self.nfev, convergence))
        if self.stop_theory_flag:
            return True

    def fit_callback_shgo(self, xk):
        if self.nfev % 10 == 0:
            self.Qprint("nfeval %6d" % self.nfev)
        if self.stop_theory_flag:
            return True

    def fit_check_bounds(self, **kwargs):
        x = kwargs["x_new"]
        tmax = bool(np.all(x <= self.param_max))
        tmin = bool(np.all(x >= self.param_min))
        return tmax and tmin

    def func_fit_and_error(self, x):
        """Calls the theory function, constructs the vector with the theory predictions and
        returns the sum of the squares of the residuals
        """
        # NEED TO RECOVER THE VECTOR y THAT WE CONSTRUCTED DURING FUNCTION FIT
        if self.normalizebydata:
            residuals = (
                self.fittingy - self.func_fit(self.fittingx, *x)
            ) / self.fittingy
        else:
            residuals = self.fittingy - self.func_fit(self.fittingx, *x)
        fres = sum(residuals**2)
        return fres

    def func_fit(self, x, *param_in):
        """Calls the theory function and constructs the vector with the theory predictions"""
        # 1. Assign the current values of the parameters being optimized
        ind = 0
        k = list(self.parameters.keys())
        k.sort()
        for p in k:
            par = self.parameters[p]
            if par.opt_type == OptType.opt:
                par.value = param_in[ind]
                ind += 1
        # 2. Call the theory function
        self.do_calculate("", timing=False)

        # 3. Constructs the y vector that contains all the Y values from the theory after
        #    applying the current view and respecting the {xmin, xmax} & {ymin, ymax} limits
        y = []
        view = self.parent_dataset.parent_application.current_view

        for f in self.theory_files():
            if f.active:
                tmp_dt = self.get_non_extended_th_table(f)
                xth, yth, success = view.view_proc(tmp_dt, f.file_parameters)
                xexp, yexp, success = view.view_proc(f.data_table, f.file_parameters)
                for i in range(view.n):
                    if self.xrange.get_visible():
                        conditionx = (xexp[:, i] > self.xmin) * (xexp[:, i] < self.xmax)
                    else:
                        conditionx = np.ones_like(xexp[:, i], dtype=bool)
                    if self.yrange.get_visible():
                        conditiony = (yexp[:, i] > self.ymin) * (yexp[:, i] < self.ymax)
                    else:
                        conditiony = np.ones_like(yexp[:, i], dtype=bool)
                    conditionnaninf = (
                        (~np.isnan(xexp)[:, 0])
                        * (~np.isnan(yexp)[:, 0])
                        * (~np.isinf(xexp)[:, 0])
                        * (~np.isinf(yexp)[:, 0])
                    )
                    ycond = np.extract(
                        conditionx * conditiony * conditionnaninf, yth[:, i]
                    )
                    y = np.append(y, ycond)
        self.nfev += 1
        return y

    def do_fit(self, line):
        """Minimize the error"""
        # Do some initial checks on the status of datasets and theories
        if not self.tables:
            self.is_fitting = False
            return
        if len(self.parent_dataset.inactive_files) == len(
            self.parent_dataset.files
        ):  # all files hidden
            self.is_fitting = False
            return
        th_files = self.theory_files()
        if not th_files:
            self.is_fitting = False
            return

        # Start the fitting procedure
        # 1. Create x and y vectors that contain the X and Y values of all the active files
        #    in the current view that respect the {xmin, xmax} & {ymin, ymax} limits
        self.is_fitting = True
        start_time = time.time()
        view = self.parent_dataset.parent_application.current_view
        self.Qprint("""<hr><h2>Parameter Fitting</h2>""")
        # Vectors that contain all X and Y in the files & view
        x = []
        y = []

        if self.xrange.get_visible():
            if self.xmin > self.xmax:
                temp = self.xmin
                self.xmin = self.xmax
                self.xmax = temp
            self.Qprint("<b>xrange</b>=[%0.3g, %0.3g]" % (self.xmin, self.xmax))
        if self.yrange.get_visible():
            if self.ymin > self.ymax:
                temp = self.ymin
                self.ymin = self.ymax
                self.ymax = temp
            self.Qprint("<b>yrange</b>=[%.03g, %0.3g]" % (self.ymin, self.ymax))

        for f in th_files:
            if self.stop_theory_flag:
                return
            if f.active:
                xexp, yexp, success = view.view_proc(f.data_table, f.file_parameters)
                for i in range(view.n):
                    if self.xrange.get_visible():
                        conditionx = (xexp[:, i] > self.xmin) * (xexp[:, i] < self.xmax)
                    else:
                        conditionx = np.ones_like(xexp[:, i], dtype=bool)
                    if self.yrange.get_visible():
                        conditiony = (yexp[:, i] > self.ymin) * (yexp[:, i] < self.ymax)
                    else:
                        conditiony = np.ones_like(yexp[:, i], dtype=bool)
                    conditionnaninf = (
                        (~np.isnan(xexp)[:, 0])
                        * (~np.isnan(yexp)[:, 0])
                        * (~np.isinf(xexp)[:, 0])
                        * (~np.isinf(yexp)[:, 0])
                    )
                    xcond = np.extract(
                        conditionx * conditiony * conditionnaninf, xexp[:, i]
                    )
                    ycond = np.extract(
                        conditionx * conditiony * conditionnaninf, yexp[:, i]
                    )

                    x = np.append(x, xcond)
                    y = np.append(y, ycond)

        # 2. Create the array of theory parameters that will be changed during the fitting (checked parameters)
        #    It also creates the arrays with the upper and lower bounds for parameters
        initial_guess = (
            []
        )  # Take the initial guess for the fit from the current value of the parameter
        self.param_min = []  # list of min values for fitting parameters
        self.param_max = []  # list of max values for fitting parameters
        k = list(self.parameters.keys())
        k.sort()
        for p in k:
            par = self.parameters[p]
            if par.opt_type == OptType.opt:
                initial_guess.append(par.value)
                self.param_min.append(par.min_value)
                self.param_max.append(par.max_value)
        # Return if the list of checked parameters is empty
        if (not initial_guess) or (not self.param_min) or (not self.param_max):
            self.Qprint("No parameter to minimize")
            self.is_fitting = False
            return

        # 3. This is where the actual optimization is done
        # TODO: We should add the option to use different minimization methods
        #       like those included in scipy or even other ones implemented by us (MC methods)
        # opt = dict(return_full=True) # I think this is not used
        self.nfev = 0
        self.fittingx = x  # MAKE EXPERIMENTAL x VECTOR AVAILABLE GLOBAL OPTIMISATION
        self.fittingy = y  # MAKE EXPERIMENTAL y VECTOR AVAILABLE GLOBAL OPTIMISATION
        self.fminnow = np.inf

        if (
            self.mintype == MinimizationMethod.dualannealing
            or self.mintype == MinimizationMethod.diffevol
            or self.mintype == MinimizationMethod.SHGO
        ):
            if (
                np.any(np.isinf(self.param_min))
                or np.any(np.isinf(self.param_max))
                or np.any(np.isnan(self.param_min))
                or np.any(np.isnan(self.param_max))
            ):
                msg = "This fitting method cannot be used if any of the bounds is ± nan or ± inf"
                self.Qprint(msg)
                self.is_fitting = False
                return

        if self.mintype == MinimizationMethod.ls:
            self.Qprint("<b>Non-linear Least-squares</b>")
            self.Qprint("<b>Local optimisation</b>")
            try:
                if self.LSmethod == "trf":
                    self.Qprint("Method: Trust Region Reflective")
                elif self.LSmethod == "dogbox":
                    self.Qprint("Method: dogleg")
                elif self.LSmethod == "lm":
                    self.Qprint("Method: Levenberg-Marquardt")
                if self.LSmethod == "trf" or self.LSmethod == "dogbox":
                    pars, pcov = curve_fit(
                        self.func_fit,
                        x,
                        y,
                        p0=initial_guess,
                        bounds=(self.param_min, self.param_max),
                        method=self.LSmethod,
                        jac=self.LSjac,
                        ftol=self.LSftol,
                        xtol=self.LSxtol,
                        gtol=self.LSgtol,
                        loss=self.LSloss,
                        f_scale=self.LSf_scale,
                        max_nfev=self.LSmax_fnev,
                        tr_solver=self.LStr_solver,
                    )
                else:
                    if self.LSmax_fnev == None:
                        pars, pcov = curve_fit(
                            self.func_fit,
                            x,
                            y,
                            p0=initial_guess,
                            bounds=(self.param_min, self.param_max),
                            method=self.LSmethod,
                            ftol=self.LSftol,
                            xtol=self.LSxtol,
                            gtol=self.LSgtol,
                        )
                    else:
                        pars, pcov = curve_fit(
                            self.func_fit,
                            x,
                            y,
                            p0=initial_guess,
                            bounds=(self.param_min, self.param_max),
                            method=self.LSmethod,
                            ftol=self.LSftol,
                            xtol=self.LSxtol,
                            gtol=self.LSgtol,
                            maxfev=self.LSmax_fnev,
                        )
            except Exception as e:
                print("In do_fit()", e)
                self.Qprint("%s" % e)
                self.is_fitting = False
                return

        elif self.mintype == MinimizationMethod.basinhopping:
            self.Qprint("<b>Basin Hopping<b>")
            self.Qprint("<b>Global optimisation</b>")
            minimizer_kwargs = {"method": "BFGS"}
            try:
                ret = basinhopping(
                    self.func_fit_and_error,
                    initial_guess,
                    niter=self.basinniter,
                    T=self.basinT,
                    stepsize=self.basinstepsize,
                    minimizer_kwargs=minimizer_kwargs,
                    accept_test=self.fit_check_bounds,
                    callback=self.fit_callback_basinhopping,
                    interval=self.basininterval,
                    niter_success=self.basinniter_success,
                    seed=self.basinseed,
                )
                initial_guess1 = ret.x
                pars, pcov = curve_fit(
                    self.func_fit,
                    x,
                    y,
                    p0=initial_guess1,
                    bounds=(self.param_min, self.param_max),
                    method="trf",
                )
            except Exception as e:
                print("In do_fit()", e)
                self.Qprint("%s" % e)
                self.is_fitting = False
                return

        elif self.mintype == MinimizationMethod.dualannealing:
            self.Qprint("<b>Dual Annealing<b>")
            self.Qprint("<b>Global optimisation</b>")
            try:
                param_bounds = list(zip(self.param_min, self.param_max))
                ret = dual_annealing(
                    self.func_fit_and_error,
                    bounds=param_bounds,
                    maxiter=self.annealmaxiter,
                    initial_temp=self.annealinitial_temp,
                    restart_temp_ratio=self.annealrestart_temp_ratio,
                    visit=self.annealvisit,
                    accept=self.annealaccept,
                    maxfun=self.annealmaxfun,
                    seed=self.annealseed,
                    no_local_search=self.annealno_local_search,
                    callback=self.fit_callback_dualannealing,
                    x0=initial_guess,
                )
                initial_guess1 = ret.x
                pars, pcov = curve_fit(
                    self.func_fit,
                    x,
                    y,
                    p0=initial_guess1,
                    bounds=(self.param_min, self.param_max),
                    method="trf",
                )
            except Exception as e:
                print("In do_fit()", e)
                self.Qprint("%s" % e)
                self.is_fitting = False
                return

        elif self.mintype == MinimizationMethod.diffevol:
            self.Qprint("<b>Differential Evolution<b>")
            self.Qprint("<b>Global optimisation</b>")
            try:
                param_bounds = list(zip(self.param_min, self.param_max))
                ret = differential_evolution(
                    self.func_fit_and_error,
                    bounds=param_bounds,
                    strategy=self.diffevolstrategy,
                    maxiter=self.diffevolmaxiter,
                    popsize=self.diffevolpopsize,
                    tol=self.diffevoltol,
                    mutation=self.diffevolmutation,
                    recombination=self.diffevolrecombination,
                    seed=self.diffevolseed,
                    callback=self.fit_callback_diffevol,
                    polish=self.diffevolpolish,
                    init=self.diffevolinit,
                    atol=self.diffevolatol,
                    updating=self.diffevolupdating,
                )
                initial_guess1 = ret.x
                pars, pcov = curve_fit(
                    self.func_fit,
                    x,
                    y,
                    p0=initial_guess1,
                    bounds=(self.param_min, self.param_max),
                    method="trf",
                )
            except Exception as e:
                print("In do_fit()", e)
                self.Qprint("%s" % e)
                self.is_fitting = False
                return

        elif self.mintype == MinimizationMethod.SHGO:
            self.Qprint("<b>Simplicial Homology Global Optimization<b>")
            try:
                param_bounds = list(zip(self.param_min, self.param_max))
                options = {
                    "maxfev": self.SHGOmaxfev,
                    "f_min": self.SHGOf_min,
                    "f_tol": self.SHGOf_tol,
                    "maxiter": self.SHGOmaxiter,
                    "maxev": self.SHGOmaxev,
                    "maxtime": self.SHGOmaxtime,
                    "minhgrd": self.SHGOminhgrd,
                    "minimize_every_iter": self.SHGOminimize_every_iter,
                    "local_iter": self.SHGOlocal_iter,
                    "infty_constraints": self.SHGOinfty_constraints,
                }
                ret = shgo(
                    self.func_fit_and_error,
                    bounds=param_bounds,
                    n=self.SHGOn,
                    iters=self.SHGOiters,
                    callback=self.fit_callback_shgo,
                    options=options,
                    sampling_method=self.SHGOsampling_method,
                )
                initial_guess1 = ret.x
                pars, pcov = curve_fit(
                    self.func_fit,
                    x,
                    y,
                    p0=initial_guess1,
                    bounds=(self.param_min, self.param_max),
                    method="trf",
                )
            except Exception as e:
                print("In do_fit()", e)
                self.Qprint("%s" % e)
                self.is_fitting = False
                return

        elif self.mintype == MinimizationMethod.bruteforce:
            self.Qprint("<b>Brute Force Global Optimization<b>")
            try:
                param_bounds = list(zip(self.param_min, self.param_max))
                ret = brute(
                    self.func_fit_and_error, ranges=param_bounds, Ns=self.BruteNs
                )
                initial_guess1 = ret
                pars, pcov = curve_fit(
                    self.func_fit,
                    x,
                    y,
                    p0=initial_guess1,
                    bounds=(self.param_min, self.param_max),
                    method="trf",
                )
            except Exception as e:
                print("In do_fit()", e)
                self.Qprint("%s" % e)
                self.is_fitting = False
                return

        # 4. Statistical analysis of the solution found
        residuals = y - self.func_fit(x, *initial_guess)
        fres0 = sum(residuals**2)
        residuals = y - self.func_fit(x, *pars)
        fres1 = sum(residuals**2)

        # table='''<table border="1" width="100%">'''
        # table+='''<tr><th>Initial Error</th><th>Final Error</th></tr>'''
        # table+='''<tr><td>%g</td><td>%g</td></tr>'''%(fres0, fres1)
        # table+='''</table><br>'''
        table = [
            ["%-18s" % "Initial Error", "%-18s" % "Final Error"],
        ]
        table.append(["%-18g" % fres0, "%-18g" % fres1])
        self.Qprint(table)

        self.Qprint("<b>%g</b> function evaluations" % (self.nfev))

        alpha = 0.05  # 95% confidence interval = 100*(1-alpha)
        n = len(y)  # number of data points
        p = len(pars)  # number of parameters
        dof = max(0, n - p)  # number of degrees of freedom
        # student-t value for the dof and confidence level
        tval = t.ppf(1.0 - alpha / 2.0, dof)

        par_error = []
        # for i, p, var in zip(range(p), pars, np.diag(pcov)):
        for var in np.diag(pcov):
            sigma = var**0.5
            par_error.append(sigma * tval)

        ind = 0
        # table='''<table border="1" width="100%">'''
        # table+='''<tr><th>Parameter</th><th>Value ± Error</th></tr>'''
        table = [
            ["%-18s" % "Parameter", "%-18s" % "Value ± Error"],
        ]
        for p in k:
            par = self.parameters[p]
            if par.opt_type == OptType.opt:
                par.error = par_error[ind]
                ind += 1
                # table+='''<tr><td>%s</td><td>%10.4g ± %-9.4g</td></tr>'''%(par.name, par.value, par.error)
                val_err = "%.4g ± %.4g" % (par.value, par.error)
                table.append(["%-18s" % par.name, "%-18s" % val_err])
            else:
                # table+='''<tr><td>%s</td><td>%10.4g</td></tr>'''%(par.name, par.value)
                if par.type == ParameterType.string:
                    table.append(["%-18s" % par.name, "%18s" % par.value])
                else:
                    table.append(["%-18s" % par.name, "%-18.4g" % par.value])
        # table+='''</table><br>'''
        self.Qprint(table)
        self.is_fitting = False
        self.do_calculate(line, timing=False)
        self.Qprint(
            """<i>---Fitted in %.3g seconds---</i><br>""" % (time.time() - start_time)
        )
        self.do_cite("")

    def plot_theory_stuff(self):
        """Plot theory helpers"""
        pass

    def do_save(self, line="", extra_txt=""):
        """Save the results from all theory predictions to file"""
        self.Qprint("Saving prediction(s) of " + self.name + " theory")
        counter = 0
        for f in self.parent_dataset.files:
            fparam = f.file_parameters
            ttable = self.tables[f.file_name_short]
            if line == "":
                ofilename = (
                    os.path.splitext(f.file_full_path)[0]
                    + "_TH"
                    + os.path.splitext(f.file_full_path)[1]
                )
            else:
                ofilename = os.path.join(
                    line,
                    f.file_name_short
                    + "_TH"
                    + extra_txt
                    + os.path.splitext(f.file_full_path)[1],
                )
            # print("ofilename", ofilename)
            # print('File: ' + f.file_name_short)
            fout = open(ofilename, "w")
            k = list(f.file_parameters.keys())
            k.sort()
            for i in k:
                fout.write(i + "=" + str(f.file_parameters[i]) + ";")
            fout.write("\n")
            fout.write("# Prediction of " + self.thname + " Theory\n")
            fout.write("# ")
            k = list(self.parameters.keys())
            k.sort()
            for i in k:
                fout.write(i + "=" + str(self.parameters[i].value) + "; ")
            fout.write("\n")
            fout.write(
                "# Date: "
                + time.strftime("%Y-%m-%d %H:%M:%S")
                + " - User: "
                + getpass.getuser()
                + "\n"
            )
            k = f.file_type.col_names
            for i in k:
                fout.write(i + "\t")
            fout.write("\n")
            for i in range(ttable.num_rows):
                for j in range(ttable.num_columns):
                    fout.write(str(ttable.data[i, j]) + "\t")
                fout.write("\n")
            fout.close()
            counter += 1

        # print information
        msg = 'Saved %d theory file(s) in "%s"' % (counter, line)
        QMessageBox.information(self, "Saved Theory", msg)

    def change_xmin(self, dx, dy):
        """Change the min x value of the span"""
        try:
            self.xmin += dx
            self.xminline.set_data([self.xmin, self.xmin], [0, 1])
            self.xrange.set_xy(
                [
                    [self.xmin, 0],
                    [self.xmin, 1],
                    [self.xmax, 1],
                    [self.xmax, 0],
                    [self.xmin, 0],
                ]
            )
        except:
            pass

    def change_xmax(self, dx, dy):
        """Change the max x value of the span"""
        try:
            self.xmax += dx
            self.xmaxline.set_data([self.xmax, self.xmax], [0, 1])
            self.xrange.set_xy(
                [
                    [self.xmin, 0],
                    [self.xmin, 1],
                    [self.xmax, 1],
                    [self.xmax, 0],
                    [self.xmin, 0],
                ]
            )
        except:
            pass

    def change_ymin(self, dx, dy):
        """Change the min y value of the span"""
        self.ymin += dy
        self.yminline.set_data([0, 1], [self.ymin, self.ymin])
        self.yrange.set_xy(
            [
                [0, self.ymin],
                [0, self.ymax],
                [1, self.ymax],
                [1, self.ymin],
                [0, self.ymin],
            ]
        )

    def change_ymax(self, dx, dy):
        """Change the max y value of the span"""
        self.ymax += dy
        self.ymaxline.set_data([0, 1], [self.ymax, self.ymax])
        self.yrange.set_xy(
            [
                [0, self.ymin],
                [0, self.ymax],
                [1, self.ymax],
                [1, self.ymin],
                [0, self.ymin],
            ]
        )

    def do_xrange(self, line, visible=None):
        """Set/show xrange for fit and shows limits. Arguments: limits of the span.
        With no arguments: switches ON/OFF the horizontal span. Example: xrange -4 5"""
        if visible == None:
            visible = not self.xrange.get_visible()
        if line == "":
            """.. todo:: Set range to current view limits"""
            self.xmin, self.xmax = self.ax.get_xlim()
            self.xminline.set_data([self.xmin, self.xmin], [0, 1])
            self.xmaxline.set_data([self.xmax, self.xmax], [0, 1])
            self.xrange.set_xy(
                [
                    [self.xmin, 0],
                    [self.xmin, 1],
                    [self.xmax, 1],
                    [self.xmax, 0],
                    [self.xmin, 0],
                ]
            )
            self.xrange.set_visible(visible)
            self.xminline.set_visible(visible)
            self.xmaxline.set_visible(visible)
        else:
            items = line.split()
            if len(items) < 2:
                print("Not enough parameters")
            else:
                self.xmin = float(items[0])
                self.xmax = float(items[1])
                self.xminline.set_data([self.xmin, self.xmin], [0, 1])
                self.xmaxline.set_data([self.xmax, self.xmax], [0, 1])
                self.xrange.set_xy(
                    [
                        [self.xmin, 0],
                        [self.xmin, 1],
                        [self.xmax, 1],
                        [self.xmax, 0],
                        [self.xmin, 0],
                    ]
                )
                if not self.xrange.get_visible():
                    self.xrange.set_visible(True)
                    self.xminline.set_visible(True)
                    self.xmaxline.set_visible(True)
        self.do_plot(line)

    def do_yrange(self, line, visible=None):
        """Set/show yrange for fit and shows limits

        With no arguments: switches ON/OFF the vertical span

        Arguments:
            - line {[ymin ymax]} -- Sets the limits of the span
        """
        if visible == None:
            visible = not self.yrange.get_visible()
        if line == "":
            self.ymin, self.ymax = self.ax.get_ylim()
            self.yminline.set_data([0, 1], [self.ymin, self.ymin])
            self.ymaxline.set_data([0, 1], [self.ymax, self.ymax])
            self.yrange.set_xy(
                [
                    [0, self.ymin],
                    [1, self.ymin],
                    [1, self.ymax],
                    [0, self.ymax],
                    [0, self.ymin],
                ]
            )
            self.yrange.set_visible(visible)
            self.yminline.set_visible(visible)
            self.ymaxline.set_visible(visible)
            # print("Ymin=%g Ymax=%g" % (self.ymin, self.ymax))
        else:
            items = line.split()
            if len(items) < 2:
                print("Not enough parameters")
            else:
                self.ymin = float(items[0])
                self.ymax = float(items[1])
                self.yminline.set_data([0, 1], [self.ymin, self.ymin])
                self.ymaxline.set_data([0, 1], [self.ymax, self.ymax])
                self.yrange.set_xy(
                    [
                        [0, self.ymin],
                        [0, self.ymax],
                        [1, self.ymax],
                        [1, self.ymin],
                        [0, self.ymin],
                    ]
                )
                if not self.yrange.get_visible():
                    self.yrange.set_visible(True)
                    self.yminline.set_visible(True)
                    self.ymaxline.set_visible(True)
        self.do_plot(line)

    def set_xy_limits_visible(self, xstate=False, ystate=False):
        """Hide the x- and y-range selectors"""
        self.xrange.set_visible(xstate)
        self.xminline.set_visible(xstate)
        self.xmaxline.set_visible(xstate)

        self.yrange.set_visible(ystate)
        self.yminline.set_visible(ystate)
        self.ymaxline.set_visible(ystate)

        self.parent_dataset.actionVertical_Limits.setChecked(xstate)
        self.parent_dataset.actionHorizontal_Limits.setChecked(ystate)
        self.parent_dataset.set_limit_icon()

    def get_modes(self):
        """Get Maxwell modes from this theory. This function must be rewritten from derived theories"""
        tau = np.ones(1)
        G = np.ones(1)
        return tau, G, False

    def set_modes(self, tau, G):
        """Set Maxwell modes in this theory. This function must be rewritten from derived theories
        that provide this functionality."""
        self.logger.info("set_modes not allowed in this theory (%s)" % self.thname)
        return False

    def do_cite(self, line):
        """Print citation information"""
        if len(self.citations) > 0:
            for i in range(len(self.citations)):
                self.Qprint(
                    """<b><font color=red>CITE</font>:</b> <a href="%s">%s</a><p>"""
                    % (self.doi[i], self.citations[i])
                )

    def do_plot(self, line):
        """Call the plot from the parent Dataset"""
        self.parent_dataset.do_plot(line)

    def set_param_value(self, name, value):
        """Set the value of a theory parameter"""
        p = self.parameters[name]
        try:
            if p.type == ParameterType.real:
                try:
                    val = float(value)
                except ValueError:
                    return "Value must be a float", False
                if val < p.min_value:
                    p.value = p.min_value
                    return "Value must be greater than %.4g" % p.min_value, False
                elif val > p.max_value:
                    p.value = p.max_value
                    return "Value must be smaller than %.4g" % p.max_value, False
                else:
                    p.value = val
                    return "", True

            elif p.type == ParameterType.integer:
                try:
                    val = int(value)  # convert to int
                except ValueError:
                    return "Value must be an integer", False
                if val < p.min_value:
                    p.value = p.min_value
                    return "Value must be greater than %d" % p.min_value, False
                elif val > p.max_value:
                    p.value = p.max_value
                    return "Value must be smaller than %d" % p.max_value, False
                else:
                    p.value = val
                    return "", True

            elif p.type == ParameterType.discrete_integer:
                try:
                    val = int(value)  # convert to int
                except ValueError:
                    return "Value must be an integer", False
                if val in p.discrete_values:
                    p.value = val
                    return "", True
                else:
                    message = "Values allowed: " + ", ".join(
                        [str(s) for s in p.discrete_values]
                    )
                    print(message)
                    return message, False

            elif p.type == ParameterType.discrete_real:
                try:
                    val = float(value)
                except ValueError:
                    return "Value must be a float", False
                if val in p.discrete_values:
                    p.value = val
                    return "", True
                else:
                    message = "Values allowed: " + ", ".join(
                        [str(s) for s in p.discrete_values]
                    )
                    print(message)
                    return message, False

            elif p.type == ParameterType.boolean:
                if value in [True, "true", "True", "1", "t", "T", "y", "yes"]:
                    p.value = True
                else:
                    p.value = False
                return "", True

            elif p.type == ParameterType.string:
                p.value = value
                return "", True

            else:
                return "", False

        except ValueError as e:
            print("In set_param_value:", e)
            return "", False

    def default(self, line):
        """Called when the input command is not recognized

        Called on an input line when the command prefix is not recognized.
        Check if there is an = sign in the line. If so, it is a parameter change.
        Else, we execute the line as Python code."""
        if "=" in line:
            par = line.split("=")
            if par[0] in self.parameters:
                self.set_param_value(par[0], par[1])
            else:
                print("Parameter %s not found" % par[0])
        elif line in self.parameters.keys():
            print(self.parameters[line])
            print(self.parameters[line].__repr__())
        else:
            super(Theory, self).default(line)

    def show_theory_extras(self, show):
        pass

    def do_hide(self, line=""):
        """Hide the theory artists and associated tools"""
        if self.active:
            self.set_xy_limits_visible(False, False)  # hide xrange and yrange
            for table in self.tables.values():
                for i in range(table.MAX_NUM_SERIES):
                    for nx in range(self.parent_dataset.nplots):
                        table.series[nx][i].set_visible(False)
            self.show_theory_extras(False)
            self.active = False

    def set_th_table_visible(self, fname, state):
        """Show/Hide all theory lines related to the file "fname" """
        tt = self.tables[fname]
        for i in range(tt.MAX_NUM_SERIES):
            for nx in range(self.parent_dataset.nplots):
                tt.series[nx][i].set_visible(state)

    def do_show(self, line=""):
        """Show theory"""
        self.active = True
        self.set_xy_limits_visible(self.is_xrange_visible, self.is_yrange_visible)
        for fname in self.tables:
            if fname in self.parent_dataset.inactive_files:
                return
            else:
                tt = self.tables[fname]
                for i in range(tt.MAX_NUM_SERIES):
                    for nx in range(self.parent_dataset.nplots):
                        tt.series[nx][i].set_visible(True)
        self.show_theory_extras(True)
        self.parent_dataset.do_plot("")

    def Qprint(self, msg, end="<br>"):
        """Print a message on the theory log area or on the terminal"""

        if isinstance(msg, list):
            msg = self.table_as_html(msg)
        self.print_signal.emit(msg + end)

    def table_as_html(self, tab):
        header = tab[0]
        rows = tab[1:]
        nrows = len(rows)
        table = """<table border="1" width="100%">"""
        # header
        if not np.all([h == "" for h in header]):
            table += "<tr>"
            table += "".join(["<th>%s</th>" % h for h in header])
            table += "</tr>"
        # data
        for row in rows:
            table += "<tr>"
            table += "".join(["<td>%s</td>" % d for d in row])
            table += "</tr>"
        table += """</table><br>"""
        return table

    def table_as_ascii(self, tab):
        text = ""
        for row in tab:
            text += " ".join(row)
            text += "\n"
        return text

    def strip_tags(self, html_text):
        s = MLStripper()
        s.feed(html_text)
        return s.get_data()

    def print_qtextbox(self, msg):
        """Print message in the GUI log text box"""
        self.thTextBox.moveCursor(QTextCursor.End)
        self.thTextBox.insertHtml(msg)
        self.thTextBox.verticalScrollBar().setValue(
            self.thTextBox.verticalScrollBar().maximum()
        )
        self.thTextBox.moveCursor(QTextCursor.End)

    def get_material_parameters(self):
        """Get theory parameters from materials database"""
        try:
            fparam = self.parent_dataset.files[0].file_parameters
        except:
            return False
        if "chem" not in fparam.keys():
            return False
        chem = fparam["chem"]
        dbindex = check_chemistry(chem)
        if dbindex < 0:
            return False
        get_all_parameters(chem, self, fparam, dbindex)
        return True

    def populate_default_minimization_options(self):
        dvalidator = QDoubleValidator()
        ivalidator = QIntValidator()
        # LEAST-SQUARES LOCAL MIN
        self.fittingoptionsdialog.ui.LSftollineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.LSxtollineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.LSgtollineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.LSf_scalelineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.LSmax_nfevlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.LSmethodcomboBox.setCurrentIndex(
            self.fittingoptionsdialog.ui.LSmethodcomboBox.findText(self.LSmethod)
        )
        self.fittingoptionsdialog.ui.LSjaccomboBox.setCurrentIndex(
            self.fittingoptionsdialog.ui.LSjaccomboBox.findText(self.LSjac)
        )
        self.fittingoptionsdialog.ui.LSftollineEdit.setText("%g" % self.LSftol)
        self.fittingoptionsdialog.ui.LSxtollineEdit.setText("%g" % self.LSxtol)
        self.fittingoptionsdialog.ui.LSgtollineEdit.setText("%g" % self.LSgtol)
        self.fittingoptionsdialog.ui.LSlosscomboBox.setCurrentIndex(
            self.fittingoptionsdialog.ui.LSlosscomboBox.findText(self.LSloss)
        )
        self.fittingoptionsdialog.ui.LSf_scalelineEdit.setText("%g" % self.LSf_scale)
        self.fittingoptionsdialog.ui.LSmax_nfevlineEdit.setText("100")
        # BASIN HOPPING
        self.fittingoptionsdialog.ui.basinniterlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.basinTlineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.basinstepsizelineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.basinintervallineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.basinniter_successlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.basinseedlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.basinniterlineEdit.setText("%d" % self.basinniter)
        self.fittingoptionsdialog.ui.basinTlineEdit.setText("%g" % self.basinT)
        self.fittingoptionsdialog.ui.basinstepsizelineEdit.setText(
            "%g" % self.basinstepsize
        )
        self.fittingoptionsdialog.ui.basinintervallineEdit.setText(
            "%d" % self.basininterval
        )
        self.fittingoptionsdialog.ui.basinniter_successlineEdit.setText("30")
        self.fittingoptionsdialog.ui.basinseedlineEdit.setText("4398495")
        # DUAL ANNEALING
        self.fittingoptionsdialog.ui.annealmaxiterlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.annealinitial_templineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.annealrestart_temp_ratiolineEdit.setValidator(
            dvalidator
        )
        self.fittingoptionsdialog.ui.annealvisitlineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.annealacceptlineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.annealmaxfunlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.annealseedlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.annealmaxiterlineEdit.setText(
            "%d" % self.annealmaxiter
        )
        self.fittingoptionsdialog.ui.annealinitial_templineEdit.setText(
            "%g" % self.annealinitial_temp
        )
        self.fittingoptionsdialog.ui.annealrestart_temp_ratiolineEdit.setText(
            "%g" % self.annealrestart_temp_ratio
        )
        self.fittingoptionsdialog.ui.annealvisitlineEdit.setText(
            "%g" % self.annealvisit
        )
        self.fittingoptionsdialog.ui.annealacceptlineEdit.setText(
            "%g" % self.annealaccept
        )
        self.fittingoptionsdialog.ui.annealmaxfunlineEdit.setText(
            "%d" % self.annealmaxfun
        )
        self.fittingoptionsdialog.ui.annealseedlineEdit.setText("4389439")
        # DIFFERENTIAL EVOLUTION
        self.fittingoptionsdialog.ui.diffevolmaxiterlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.diffevolpopsizelineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.diffevoltollineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.diffevolmutationAlineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.diffevolmutationBlineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.diffevolrecombinationlineEdit.setValidator(
            dvalidator
        )
        self.fittingoptionsdialog.ui.diffevolseedlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.diffevolatollineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.diffevolstrategycomboBox.setCurrentIndex(
            self.fittingoptionsdialog.ui.diffevolstrategycomboBox.findText(
                self.diffevolstrategy
            )
        )
        self.fittingoptionsdialog.ui.diffevolmaxiterlineEdit.setText(
            "%d" % self.diffevolmaxiter
        )
        self.fittingoptionsdialog.ui.diffevolpopsizelineEdit.setText(
            "%d" % self.diffevolpopsize
        )
        self.fittingoptionsdialog.ui.diffevoltollineEdit.setText(
            "%g" % self.diffevoltol
        )
        self.fittingoptionsdialog.ui.diffevolmutationAlineEdit.setText(
            "%g" % self.diffevolmutation[0]
        )
        self.fittingoptionsdialog.ui.diffevolmutationBlineEdit.setText(
            "%g" % self.diffevolmutation[1]
        )
        self.fittingoptionsdialog.ui.diffevolrecombinationlineEdit.setText(
            "%g" % self.diffevolrecombination
        )
        self.fittingoptionsdialog.ui.diffevolseedlineEdit.setText("4389439")
        self.fittingoptionsdialog.ui.diffevolinitcomboBox.setCurrentIndex(
            self.fittingoptionsdialog.ui.diffevolinitcomboBox.findText(
                self.diffevolinit
            )
        )
        self.fittingoptionsdialog.ui.diffevolatollineEdit.setText(
            "%g" % self.diffevolatol
        )
        # SHGO
        self.fittingoptionsdialog.ui.SHGOnlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.SHGOiterslineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.SHGOmaxfevlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.SHGOf_minlineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.SHGOf_tollineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.SHGOmaxiterlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.SHGOmaxevlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.SHGOmaxtimelineEdit.setValidator(dvalidator)
        self.fittingoptionsdialog.ui.SHGOminhgrdlineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.SHGOnlineEdit.setText("%d" % self.SHGOn)
        self.fittingoptionsdialog.ui.SHGOiterslineEdit.setText("%d" % self.SHGOiters)
        self.fittingoptionsdialog.ui.SHGOf_tollineEdit.setText("%g" % self.SHGOf_tol)
        # Brute Force
        self.fittingoptionsdialog.ui.BruteNslineEdit.setValidator(ivalidator)
        self.fittingoptionsdialog.ui.BruteNslineEdit.setText("%d" % self.BruteNs)

    def populate_default_error_calculation_options(self):
        # ERROR CALCULATION METHOD
        if self.errormethod == ErrorCalculationMethod.View1:
            self.errorcalculationdialog.ui.View1radioButton.setChecked(True)
        elif self.errormethod == ErrorCalculationMethod.RawData:
            self.errorcalculationdialog.ui.RawDataradioButton.setChecked(True)
        elif self.errormethod == ErrorCalculationMethod.AllViews:
            self.errorcalculationdialog.ui.AllViewsradioButton.setChecked(True)
        self.errorcalculationdialog.ui.NormalizecheckBox.setChecked(
            self.normalizebydata
        )

    def thtextbox_context_menu(self):
        """Custom contextual menu for the theory textbox"""
        menu = self.thTextBox.createStandardContextMenu()
        menu.addSeparator()
        menu.addAction(
            "Increase Font Size", lambda: self.change_thtextbox_fontsize(1.25)
        )
        menu.addAction(
            "Deacrease Font Size", lambda: self.change_thtextbox_fontsize(0.8)
        )
        menu.addAction("Clear Text", self.thTextBox.clear)
        menu.exec_(QCursor.pos())

    def change_thtextbox_fontsize(self, factor):
        """Change the thTextBox font size by a factor `factor`"""
        font = self.thTextBox.currentFont()
        if factor < 1:
            font_size = ceil(font.pointSize() * factor)
        else:
            font_size = floor(font.pointSize() * factor)
        font.setPointSize(font_size)
        self.thTextBox.document().setDefaultFont(font)

    def set_extra_data(self, extra_data):
        """set the extra data dict at loading, redefined in Child class if needed"""
        self.extra_data = extra_data

    def get_extra_data(self):
        """get the extra data dict before saving (defined in Child class if needed)"""
        pass

    def theory_buttons_disabled(self, state):
        """Disable theory button inside the theory"""
        pass

    def handle_actionCalculate_Theory(self):
        if self.thread_calc_busy:
            return
        self.thread_calc_busy = True
        # disable buttons
        self.parent_dataset.actionNew_Theory.setDisabled(
            True
        )  # only needed for theories using shared libraries
        self.theory_buttons_disabled(True)

        if CmdBase.calcmode == CalcMode.multithread:
            self.worker = CalculationThread(
                self.do_calculate,
                "",
            )
            self.worker.sig_done.connect(self.end_thread_calc)
            self.thread_calc = QThread()
            self.worker.moveToThread(self.thread_calc)
            self.thread_calc.started.connect(self.worker.work)
            self.thread_calc.start()
        elif CmdBase.calcmode == CalcMode.singlethread:
            self.do_calculate("")
            self.end_thread_calc()

    def end_thread_calc(self):
        if CmdBase.calcmode == CalcMode.multithread:
            try:
                self.thread_calc.quit()
            except:
                pass
        else:
            self.update_parameter_table()
            for file in self.theory_files():  # copy theory data to the plot series
                tt = self.tables[file.file_name_short]
                for nx in range(self.parent_dataset.nplots):
                    view = self.parent_dataset.parent_application.multiviews[nx]
                    x, y, success = view.view_proc(tt, file.file_parameters)
                    for i in range(tt.MAX_NUM_SERIES):
                        if i < view.n:
                            tt.series[nx][i].set_data(x[:, i], y[:, i])

            self.parent_dataset.parent_application.update_Qplot()
        self.thread_calc_busy = False
        # enable buttons
        self.parent_dataset.actionNew_Theory.setDisabled(False)
        self.theory_buttons_disabled(False)
        self.parent_dataset.end_of_computation(self.name)

    def handle_actionMinimize_Error(self):
        """Minimize the error"""
        if self.thread_fit_busy:
            return
        self.thread_fit_busy = True
        # disable buttons
        self.parent_dataset.actionNew_Theory.setDisabled(
            True
        )  # only needed for theories using shared libraries
        self.theory_buttons_disabled(True)

        if CmdBase.calcmode == CalcMode.multithread:
            self.worker = CalculationThread(
                self.do_fit,
                "",
            )
            self.worker.sig_done.connect(self.end_thread_fit)
            self.thread_fit = QThread()
            self.worker.moveToThread(self.thread_fit)
            self.thread_fit.started.connect(self.worker.work)
            self.thread_fit.start()
        elif CmdBase.calcmode == CalcMode.singlethread:
            self.do_fit("")
            self.end_thread_fit()

    def end_thread_fit(self):
        if CmdBase.calcmode == CalcMode.multithread:
            try:
                self.thread_fit.quit()
            except:
                pass
        self.update_parameter_table()
        self.parent_dataset.parent_application.update_Qplot()
        self.thread_fit_busy = False
        # enable buttons
        self.parent_dataset.actionNew_Theory.setDisabled(False)
        self.theory_buttons_disabled(False)
        self.parent_dataset.end_of_computation(self.name)

    def copy_parameters(self):
        text = ""
        for param in self.parameters:
            p = self.parameters[param]
            text += "%s\t%g\n" % (p.name, p.value)
        QApplication.clipboard().setText(text)

    def paste_parameters(self):
        text = QApplication.clipboard().text()
        if text == "":
            return
        rows = text.splitlines()  # split on newlines
        for i in range(len(rows)):
            cols = rows[i].split()  # split on whitespaces
            if len(cols) == 2:
                if cols[0] in self.parameters:
                    message, success = self.set_param_value(cols[0], cols[1])
        self.update_parameter_table()
        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()

    def update_parameter_table(self):
        """Update the theory parameter table"""
        # clean table
        self.thParamTable.clear()

        # populate table
        for param in self.parameters:
            p = self.parameters[param]
            if p.display_flag:  # only allowed param enter the table
                if p.opt_type == OptType.const:
                    if p.type == ParameterType.string:
                        item = QTreeWidgetItem(
                            self.thParamTable, [p.name, p.value, "N/A"]
                        )
                    else:
                        item = QTreeWidgetItem(
                            self.thParamTable, [p.name, "%0.3g" % p.value, "N/A"]
                        )
                    item.setCheckState(0, Qt.PartiallyChecked)
                    item.setFlags(item.flags() & ~Qt.ItemIsUserCheckable)
                else:
                    try:
                        err = "%0.3g" % p.error
                    except:
                        err = "-"
                    if p.type == ParameterType.string:
                        item = QTreeWidgetItem(
                            self.thParamTable, [p.name, p.value, "N/A"]
                        )
                    else:
                        item = QTreeWidgetItem(
                            self.thParamTable, [p.name, "%0.3g" % p.value, err]
                        )
                    if p.opt_type == OptType.opt:
                        item.setCheckState(0, Qt.Checked)
                    elif p.opt_type == OptType.nopt:
                        item.setCheckState(0, Qt.Unchecked)

                item.setFlags(item.flags() | Qt.ItemIsEditable)
                item.setToolTip(0, p.description)
        self.thParamTable.header().resizeSections(QHeaderView.ResizeToContents)

    def onTreeWidgetItemDoubleClicked(self, item, column):
        """Start editing text when a table cell is double clicked
        Or edit all parameters fittingoptionsdialog if parameter name is double clicked
        """
        if column == 0:
            p_name = item.text(0)
            d = EditThParametersDialog(self, p_name)
            if d.exec_():
                for pname in self.parameters:
                    p = self.parameters[pname]
                    attr_dict = d.all_pattr[pname]
                    for attr_name in attr_dict:
                        if attr_name == "type":
                            val = attr_dict[attr_name].currentText()
                            setattr(p, attr_name, ParameterType[val])
                        elif attr_name == "opt_type":
                            val = attr_dict[attr_name].currentText()
                            setattr(p, attr_name, OptType[val])
                        elif attr_name == "display_flag":
                            val = ast.literal_eval(
                                attr_dict[attr_name].currentText()
                            )  # bool
                            setattr(p, attr_name, val)
                        elif attr_name == "discrete_values":
                            val = attr_dict[attr_name].text()
                            l = ast.literal_eval(val)
                            if isinstance(l, list):
                                setattr(p, attr_name, l)
                        elif attr_name in ["name", "description"]:
                            continue
                        else:
                            val = float(attr_dict[attr_name].text())
                            setattr(p, attr_name, val)
                self.update_parameter_table()

        elif column == 1:
            self.thParamTable.editItem(item, column)
            # thcurrent = self.parent_dataset.TheorytabWidget.currentWidget()
            # thcurrent.editItem(item, column)

    def handle_parameterItemChanged(self, item, column):
        """Modify parameter values when changed in the theory table"""
        param_changed = item.text(0)
        if column == 0:  # param was checked/unchecked
            if item.checkState(0) == Qt.Checked:
                self.parameters[param_changed].opt_type = OptType.opt
            elif item.checkState(0) == Qt.Unchecked:
                self.parameters[param_changed].opt_type = OptType.nopt
            return
        # else, assign the entered value
        new_value = item.text(1)
        message, success = self.set_param_value(param_changed, new_value)
        if not success:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            if message != "":
                msg.setText("Not a valid value\n" + message)
            else:
                msg.setText("Not a valid value")
            msg.exec_()
            item.setText(1, str(self.parameters[param_changed].value))
        else:
            self.update_parameter_table()
            if self.autocalculate:
                self.parent_dataset.handle_actionCalculate_Theory()

    def Qcopy_modes(self):
        """Copy Maxwell modes between theories"""
        apmng = self.parent_dataset.parent_application.parent_manager
        G, S = apmng.list_theories_Maxwell(th_exclude=self)
        if G:
            d = GetModesDialog(self, G)
            if d.exec_() and d.btngrp.checkedButton() != None:
                item = d.btngrp.checkedButton().text()
                tau, G0, success = G[item]()
                if not success:
                    self.logger.warning("Could not get modes successfully")
                    return
                tauinds = (-tau).argsort()
                tau = tau[tauinds]
                G0 = G0[tauinds]
                success = self.set_modes(tau, G0)
                if not success:
                    self.logger.warning("Could not set modes successfully")
                    return
                self.update_parameter_table()
                self.parent_dataset.handle_actionCalculate_Theory()
        else:
            QMessageBox.information(
                self, "Import Modes", "Found no opened theory to import modes from"
            )

    def save_modes(self):
        """Save Maxwell modes to a text file"""
        fpath, _ = QFileDialog.getSaveFileName(
            self,
            "Save Maxwell modes to a text file",
            os.path.join(RepTate.root_dir, "data"),
            "Text (*.txt)",
        )
        if fpath == "":
            return

        with open(fpath, "w") as f:
            times, G, success = self.get_modes()
            if not success:
                self.logger.warning("Could not get modes correctly")
                return

            header = "# Maxwell modes\n"
            verdata = RepTate._version.get_versions()
            version = verdata["version"].split("+")[0]
            date = verdata["date"].split("T")[0]
            build = verdata["version"]
            header += "# Generated with RepTate %s %s (build %s)\n" % (
                version,
                date,
                build,
            )
            header += "# At %s on %s\n" % (
                time.strftime("%X"),
                time.strftime("%a %b %d, %Y"),
            )
            f.write(header)

            f.write("\n#number of modes\n")
            n = len(times)
            f.write("%d\n" % n)
            f.write("\n#%4s\t%15s\t%15s\n" % ("i", "tau_i", "G_i"))

            for i in range(n):
                f.write("%5d\t%15g\t%15g\n" % (i + 1, times[i], G[i]))

            f.write("\n#end")

        QMessageBox.information(self, "Success", 'Wrote Maxwell modes "%s"' % fpath)
