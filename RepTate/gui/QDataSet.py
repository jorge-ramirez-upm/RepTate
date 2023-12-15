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
"""Module QDataSet

Module that defines the GUI counterpart of Dataset.

"""
import sys
import os
import glob
import enum

from os.path import dirname, join, abspath, isdir
from PySide6.QtGui import (
    QPixmap,
    QColor,
    QPainter,
    QIcon,
    QAction,
    QIntValidator,
    QDoubleValidator,
    QStandardItem,
)
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QWidget,
    QTreeWidgetItem,
    QTabWidget,
    QToolBar,
    QComboBox,
    QMessageBox,
    QInputDialog,
    QToolButton,
    QMenu,
    QTableWidgetItem,
    QAbstractItemView,
    QDialog,
    QVBoxLayout,
    QDialogButtonBox,
    QGroupBox,
    QFormLayout,
    QLineEdit,
    QLabel,
    QFileDialog,
    QCheckBox,
)
import RepTate
from RepTate.core.File import File
from RepTate.core.DataTable import DataTable
from RepTate.gui.QTheory import MinimizationMethod, ErrorCalculationMethod
from RepTate.gui.DataSetWidget import DataSetWidget
import numpy as np
import matplotlib.patheffects as pe

import itertools
from collections import OrderedDict
import logging


if getattr(sys, "frozen", False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    PATH = sys._MEIPASS
else:
    PATH = dirname(abspath(__file__))
Ui_DataSet, QWidget = loadUiType(join(PATH, "DataSet.ui"))


class ColorMode(enum.Enum):
    """Class to describe how to change colors in the current DataSet"""

    fixed = 0
    variable = 1
    gradient = 2
    modes = ["Fixed color", "Variable color (from palette)", "Color gradient"]
    color1 = (0, 0, 0, 1)  # black RGB
    color2 = (1, 0, 0, 1)  # red RGB
    colorpalettes = {
        "Rainbow": [
            (0, 0, 0),
            (1.0, 0, 0),
            (0, 1.0, 0),
            (0, 0, 1.0),
            (1.0, 1.0, 0),
            (1.0, 0, 1.0),
            (0, 1.0, 1.0),
            (0.5, 0, 0),
            (0, 0.5, 0),
            (0, 0, 0.5),
            (0.5, 0.5, 0),
            (0.5, 0, 0.5),
            (0, 0.5, 0.5),
            (0.25, 0, 0),
            (0, 0.25, 0),
            (0, 0, 0.25),
            (0.25, 0.25, 0),
            (0.25, 0, 0.25),
            (0, 0.25, 0.25),
        ],
        "Pastel": [
            (0.573, 0.776, 1.0),
            (0.592, 0.941, 0.667),
            (1.0, 0.624, 0.604),
            (0.816, 0.733, 1.0),
            (1.0, 0.996, 0.639),
            (0.69, 0.878, 0.902),
            (0.573, 0.776, 1.0),
            (0.592, 0.941, 0.667),
            (1.0, 0.624, 0.604),
            (0.816, 0.733, 1.0),
            (1.0, 0.996, 0.639),
            (0.69, 0.878, 0.902),
            (0.573, 0.776, 1.0),
            (0.592, 0.941, 0.667),
            (1.0, 0.624, 0.604),
        ],
        "Bright": [
            (0.0, 0.247, 1.0),
            (0.012, 0.929, 0.227),
            (0.91, 0.0, 0.043),
            (0.541, 0.169, 0.886),
            (1.0, 0.769, 0.0),
            (0.0, 0.843, 1.0),
            (0.0, 0.247, 1.0),
            (0.012, 0.929, 0.227),
            (0.91, 0.0, 0.043),
            (0.541, 0.169, 0.886),
            (1.0, 0.769, 0.0),
            (0.0, 0.843, 1.0),
            (0.0, 0.247, 1.0),
            (0.012, 0.929, 0.227),
            (0.91, 0.0, 0.043),
        ],
        "Dark": [
            (0, 0, 0),
            (0.0, 0.11, 0.498),
            (0.004, 0.459, 0.09),
            (0.549, 0.035, 0.0),
            (0.463, 0.0, 0.631),
            (0.722, 0.525, 0.043),
            (0.0, 0.388, 0.455),
            (0.0, 0.11, 0.498),
            (0.004, 0.459, 0.09),
            (0.549, 0.035, 0.0),
            (0.463, 0.0, 0.631),
            (0.722, 0.525, 0.043),
            (0.0, 0.388, 0.455),
            (0.0, 0.11, 0.498),
            (0.004, 0.459, 0.09),
            (0.549, 0.035, 0.0),
        ],
        "ColorBlind": [
            (0, 0, 0),
            (0.0, 0.447, 0.698),
            (0.0, 0.62, 0.451),
            (0.835, 0.369, 0.0),
            (0.8, 0.475, 0.655),
            (0.941, 0.894, 0.259),
            (0.337, 0.706, 0.914),
            (0.0, 0.447, 0.698),
            (0.0, 0.62, 0.451),
            (0.835, 0.369, 0.0),
            (0.8, 0.475, 0.655),
            (0.941, 0.894, 0.259),
            (0.337, 0.706, 0.914),
            (0.0, 0.447, 0.698),
            (0.0, 0.62, 0.451),
            (0.835, 0.369, 0.0),
        ],
        "Paired": [
            (0.651, 0.808, 0.890),
            (0.122, 0.471, 0.706),
            (0.698, 0.875, 0.541),
            (0.200, 0.627, 0.173),
            (0.984, 0.604, 0.600),
            (0.890, 0.102, 0.11),
            (0.992, 0.749, 0.435),
            (1.0, 0.498, 0.0),
            (0.792, 0.698, 0.839),
            (0.416, 0.239, 0.604),
            (1.0, 1.0, 0.6),
            (0.694, 0.349, 0.157),
            (0.651, 0.808, 0.890),
            (0.122, 0.471, 0.706),
            (0.698, 0.875, 0.541),
            (0.200, 0.627, 0.173),
        ],
    }


class SymbolMode(enum.Enum):
    """Class to describe how to change the symbols in the DataSet"""

    fixed = 0
    fixedfilled = 1
    variable = 2
    variablefilled = 3
    modes = [
        "Fixed empty symbol",
        "Fixed filled symbol",
        "Variable empty symbols",
        "Variable filled symbols",
    ]
    # symbol1 = "."
    # symbol1_name = "point"
    symbol1 = "o"
    symbol1_name = "circle"
    allmarkers = [
        # ".",
        "o",
        "v",
        "^",
        "<",
        ">",
        "1",
        "2",
        "3",
        "4",
        "8",
        "s",
        "p",
        "P",
        "*",
        "h",
        "H",
        "+",
        "x",
        "X",
        "D",
        "d",
        "|",
        "_",
    ]
    allmarkernames = [
        # "point",
        "circle",
        "triangle_down",
        "triangle_up",
        "triangle_left",
        "triangle_right",
        "tri_down",
        "tri_up",
        "tri_left",
        "tri_right",
        "octagon",
        "square",
        "pentagon",
        "plus (filled)",
        "star",
        "hexagon1",
        "hexagon2",
        "plus",
        "x",
        "x (filled)",
        "diamond",
        "thin_diamond",
        "vline",
        "hline",
    ]
    filledmarkers = [
        # ".",
        "o",
        "v",
        "^",
        "<",
        ">",
        "8",
        "s",
        "p",
        "P",
        "*",
        "h",
        "H",
        "X",
        "D",
        "d",
    ]
    filledmarkernames = [
        # "point",
        "circle",
        "triangle_down",
        "triangle_up",
        "triangle_left",
        "triangle_right",
        "octagon",
        "square",
        "pentagon",
        "plus (filled)",
        "star",
        "hexagon1",
        "hexagon2",
        "x (filled)",
        "diamond",
        "thin_diamond",
    ]


class ThLineMode(enum.Enum):
    """Class to describe how to change the line types in Theories"""

    as_data = 0
    fixed = 1
    color = (0, 0, 0, 1)  # black RGB
    linestyles = OrderedDict(
        [
            ("solid", (0, ())),
            ("loosely dotted", (0, (1, 10))),
            ("dotted", (0, (1, 5))),
            ("densely dotted", (0, (1, 1))),
            ("loosely dashed", (0, (5, 10))),
            ("dashed", (0, (5, 5))),
            ("densely dashed", (0, (5, 1))),
            ("loosely dashdotted", (0, (3, 10, 1, 10))),
            ("dashdotted", (0, (3, 5, 1, 5))),
            ("densely dashdotted", (0, (3, 1, 1, 1))),
            ("loosely dashdotdotted", (0, (3, 10, 1, 10, 1, 10))),
            ("dashdotdotted", (0, (3, 5, 1, 5, 1, 5))),
            ("densely dashdotdotted", (0, (3, 1, 1, 1, 1, 1))),
        ]
    )
    # Cycle over line styles - JR
    linestylenames = [
        "solid",
        "dashed",
        "dashdotted",
        "dotted",
        "dashdotdotted",
        "densely dashed",
        "densely dashdotted",
        "densely dotted",
        "densely dashdotdotted",
        "loosely dashed",
        "loosely dashdotted",
        "loosely dotted",
        "loosely dashdotdotted",
    ]


class EditFileParametersDialog(QDialog):
    """Create the form that is used to modify the file parameters"""

    def __init__(self, parent, file):
        super().__init__(parent)
        self.parent_dataset = parent
        self.file = file
        self.createFormGroupBox(file)
        self.createFormGroupBoxTheory(file)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        tab_widget = QTabWidget()
        tab_widget.addTab(self.formGroupBox, "File Parameters")
        tab_widget.addTab(self.formGroupBoxTheory, "Theory Parameters")
        mainLayout.addWidget(tab_widget)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("Edit Parameters")

    def createFormGroupBox(self, file):
        """Create a form to set the new values of the file parameters"""
        self.formGroupBox = QGroupBox('Parameters of "%s"' % file.file_name_short)
        layout = QFormLayout()

        parameters = file.file_parameters
        self.param_dict = {}
        self.p_new = []
        for i, pname in enumerate(parameters):  # loop over the Parameters
            self.p_new.append(QLineEdit())
            if isinstance(parameters[pname], str):  # the parameter is a string
                self.p_new[i].setText("%s" % parameters[pname])
            else:  # parameter is a number:
                self.p_new[i].setValidator(QDoubleValidator())  # prevent letters
                self.p_new[i].setText("%.4g" % parameters[pname])
            layout.addRow("%s:" % pname, self.p_new[i])
            self.param_dict[pname] = self.p_new[i]
        self.formGroupBox.setLayout(layout)

    def createFormGroupBoxTheory(self, file):
        self.formGroupBoxTheory = QGroupBox(
            'Extend theory xrange of "%s"' % file.file_name_short
        )
        layout = QFormLayout()
        self.with_extra_x = QCheckBox(self)
        self.with_extra_x.setChecked(file.with_extra_x)
        layout.addRow("Extra theory xrange?", self.with_extra_x)
        self.with_extra_x.toggled.connect(self.activate_th_widgets)
        # Npoints
        self.th_num_pts = QLineEdit(self)
        intvalidator = QIntValidator()
        intvalidator.setBottom(2)
        self.th_num_pts.setValidator(QIntValidator())
        self.th_num_pts.setText("%s" % file.th_num_pts)
        layout.addRow("Num. of extra point", self.th_num_pts)
        # logspace
        self.th_logspace = QCheckBox(self)
        self.th_logspace.setChecked(file.theory_logspace)
        layout.addRow("logspace", self.th_logspace)
        # theory xmin/max
        dvalidator = QDoubleValidator()
        self.th_xmin = QLineEdit(self)
        self.th_xmax = QLineEdit(self)
        self.th_xmin.setValidator(dvalidator)
        self.th_xmax.setValidator(dvalidator)
        self.th_xmin.textEdited.connect(self.update_current_view_xrange)
        self.th_xmax.textEdited.connect(self.update_current_view_xrange)
        self.th_xmin.setText("%s" % file.theory_xmin)
        self.th_xmax.setText("%s" % file.theory_xmax)
        layout.addRow("xmin theory", self.th_xmin)
        layout.addRow("xmax theory", self.th_xmax)
        # current view theory xmin/max
        self.view_xmin = QLabel(self)
        self.view_xmax = QLabel(self)
        layout.addRow("xmin(current view)", self.view_xmin)
        layout.addRow("xmax(current view)", self.view_xmax)
        self.update_current_view_xrange()
        # set layout
        self.formGroupBoxTheory.setLayout(layout)
        self.activate_th_widgets()

    def update_current_view_xrange(self):
        view = self.parent_dataset.parent_application.current_view
        tmp_dt = DataTable(axarr=[])
        tmp_dt.data = np.empty((1, 3))
        tmp_dt.data[:] = np.nan
        tmp_dt.num_rows = 1
        tmp_dt.num_columns = 3
        try:
            xmin = float(self.th_xmin.text())
        except ValueError:
            self.view_xmin.setText("N/A")
        else:
            tmp_dt.data[0, 0] = xmin
            x, y, success = view.view_proc(tmp_dt, self.file.file_parameters)
            self.view_xmin.setText("%.4g" % x[0, 0])

        try:
            xmax = float(self.th_xmax.text())
        except ValueError:
            self.view_xmax.setText("N/A")
        else:
            tmp_dt.data[0, 0] = xmax
            x, y, success = view.view_proc(tmp_dt, self.file.file_parameters)
            self.view_xmax.setText("%.4g" % x[0, 0])

    def activate_th_widgets(self):
        checked = self.with_extra_x.isChecked()
        self.th_xmin.setDisabled(not checked)
        self.th_xmax.setDisabled(not checked)
        self.th_num_pts.setDisabled(not checked)
        self.th_logspace.setDisabled(not checked)
        self.view_xmin.setDisabled(not checked)
        self.view_xmax.setDisabled(not checked)


class QDataSet(QWidget, Ui_DataSet):
    """Abstract class to describe a data set that contains data files"""

    def __init__(self, name="QDataSet", parent=None):
        """**Constructor**"""
        # super().__init__(name=name, parent=parent)
        QWidget.__init__(self)
        Ui_DataSet.__init__(self)
        self.setupUi(self)

        self.name = name
        self.parent_application = parent
        self.nplots = self.parent_application.nplots
        self.files = []
        self.current_file = None
        self.num_files = 0
        # Marker settings
        self.marker_size = 6
        self.line_width = 1
        self.colormode = ColorMode.variable.value
        self.color1 = ColorMode.color1.value
        self.color2 = ColorMode.color2.value
        self.th_line_mode = ThLineMode.as_data.value
        self.th_color = ThLineMode.color.value
        self.palette_name = "ColorBlind"
        self.symbolmode = SymbolMode.fixed.value
        self.symbol1 = SymbolMode.symbol1.value
        self.symbol1_name = SymbolMode.symbol1_name.value
        self.th_linestyle = "solid"
        self.th_line_width = 1.5
        #
        self.theories = {}
        self.num_theories = 0
        self.inactive_files = {}
        self.current_theory = None
        self.table_icon_list = []  # save the file's marker shape, fill and color there
        self.selected_file = None

        # LOGGING STUFF
        self.logger = logging.getLogger(
            self.parent_application.logger.name + "." + self.name
        )
        self.logger.debug("New DataSet")
        np.seterrcall(self.write)

        self.DataSettreeWidget = DataSetWidget(self)
        self.splitter.insertWidget(0, self.DataSettreeWidget)

        self.DataSettreeWidget.setIndentation(0)
        self.DataSettreeWidget.setHeaderItem(QTreeWidgetItem([""]))
        # self.DataSettreeWidget.setSelectionMode(1)  # QAbstractItemView::SingleSelection
        self.DataSettreeWidget.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )  # QAbstractItemView::SingleSelection
        hd = self.DataSettreeWidget.header()
        hd.setSectionsMovable(False)
        w = self.DataSettreeWidget.width()
        w /= hd.count()
        for i in range(hd.count()):
            hd.resizeSection(0, w)

        # Theory Toolbar
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        tb.addAction(self.actionNew_Theory)
        self.cbtheory = QComboBox()
        model = self.cbtheory.model()
        self.cbtheory.setToolTip("Choose a Theory")

        item = QStandardItem("Select:")
        item.setForeground(QColor("grey"))
        model.appendRow(item)
        i = 1
        for th_name in self.parent_application.theories:
            if th_name not in self.parent_application.common_theories:
                item = QStandardItem(th_name)
                item.setToolTip(self.parent_application.theories[th_name].description)
                model.appendRow(item)
        flag_first = True
        for th_name in self.parent_application.theories:
            if th_name in self.parent_application.common_theories:
                if flag_first:
                    # add separator if al least one common theories is added
                    self.cbtheory.insertSeparator(self.cbtheory.count())
                    flag_first = False
                item = QStandardItem(th_name)
                item.setToolTip(self.parent_application.theories[th_name].description)
                model.appendRow(item)
        self.cbtheory.setCurrentIndex(0)

        ###

        self.cbtheory.setMaximumWidth(115)
        self.cbtheory.setMinimumWidth(50)
        tb.addWidget(self.cbtheory)
        tb.addAction(self.actionCalculate_Theory)
        # MINIMIZE BUTTON + OPTIONS
        tbut0 = QToolButton()
        tbut0.setPopupMode(QToolButton.MenuButtonPopup)
        tbut0.setDefaultAction(self.actionMinimize_Error)
        menu0 = QMenu(self)
        menu0.addAction(self.actionFitting_Options)
        menu0.addAction(self.actionError_Calc_Options)
        tbut0.setMenu(menu0)
        tb.addWidget(tbut0)
        # tb.addAction(self.actionMinimize_Error)
        # Buttons not wired yet
        # tb.addAction(self.actionTheory_Options)
        # self.actionTheory_Options.setDisabled(True)
        tbut = QToolButton()
        tbut.setPopupMode(QToolButton.MenuButtonPopup)
        tbut.setDefaultAction(self.actionShow_Limits)
        menu = QMenu(self)
        menu.addAction(self.actionVertical_Limits)
        menu.addAction(self.actionHorizontal_Limits)
        tbut.setMenu(menu)
        tb.addWidget(tbut)
        tbut2 = QToolButton()
        tbut2.setPopupMode(QToolButton.MenuButtonPopup)
        self.action_save_theory_data = QAction(
            QIcon(":/Icon8/Images/new_icons/icons8-save_TH.png"),
            "Save Theory Data",
            self,
        )
        tbut2.setDefaultAction(self.action_save_theory_data)
        menu2 = QMenu(self)
        menu2.addAction(self.actionCopy_Parameters)
        menu2.addAction(self.actionPaste_Parameters)
        tbut2.setMenu(menu2)
        tb.addWidget(tbut2)

        self.TheoryLayout.insertWidget(0, tb)
        self.splitter.setSizes((1000, 3000))

        # desactive buttons when no theory tab
        self.theory_actions_disabled(True)

        connection_id = self.actionNew_Theory.triggered.connect(
            self.handle_actionNew_Theory
        )
        connection_id = self.DataSettreeWidget.itemChanged.connect(
            self.handle_itemChanged
        )
        # connection_id = self.DataSettreeWidget.itemClicked.connect(self.handle_itemClicked)
        connection_id = self.DataSettreeWidget.itemDoubleClicked.connect(
            self.handle_itemDoubleClicked
        )
        connection_id = self.DataSettreeWidget.header().sortIndicatorChanged.connect(
            self.handle_sortIndicatorChanged
        )
        connection_id = self.DataSettreeWidget.itemSelectionChanged.connect(
            self.handle_itemSelectionChanged
        )
        # connection_id = self.DataSettreeWidget.currentItemChanged.connect(self.handle_currentItemChanged)

        connection_id = self.TheorytabWidget.tabCloseRequested.connect(
            self.handle_thTabCloseRequested
        )
        connection_id = self.TheorytabWidget.tabBarDoubleClicked.connect(
            self.handle_thTabBarDoubleClicked
        )
        connection_id = self.TheorytabWidget.currentChanged.connect(
            self.handle_thCurrentChanged
        )
        connection_id = self.actionMinimize_Error.triggered.connect(
            self.handle_actionMinimize_Error
        )
        connection_id = self.actionCalculate_Theory.triggered.connect(
            self.handle_actionCalculate_Theory
        )
        connection_id = self.action_save_theory_data.triggered.connect(
            self.handle_action_save_theory_data
        )
        connection_id = self.actionCopy_Parameters.triggered.connect(
            self.copy_parameters
        )
        connection_id = self.actionPaste_Parameters.triggered.connect(
            self.paste_parameters
        )

        connection_id = self.actionVertical_Limits.triggered.connect(
            self.toggle_vertical_limits
        )
        connection_id = self.actionHorizontal_Limits.triggered.connect(
            self.toggle_horizontal_limits
        )
        connection_id = self.actionFitting_Options.triggered.connect(
            self.handle_fitting_options
        )
        connection_id = self.actionError_Calc_Options.triggered.connect(
            self.handle_error_calculation_options
        )

    def write(self, type, flag):
        """Write numpy error logs to the logger"""
        self.logger.info("numpy: %s (flag %s)" % (type, flag))

    def change_file_visibility(self, file_name_short, check_state=True):
        """Hide/Show file in the figure"""
        file_matching = []
        for file in self.files:
            if file.file_name_short == file_name_short:  # find changed file
                file_matching.append(file)
        if len(file_matching) == 0:
            raise ValueError('Could not match file "%s"' % file_name_short)
            return
        if len(file_matching) > 1:
            raise ValueError('Too many match for file "%s"' % file_name_short)
            return

        file_matching[0].active = check_state

        # hide datatable
        dt = file_matching[0].data_table
        for i in range(dt.MAX_NUM_SERIES):
            for nx in range(self.nplots):  # loop over the plots
                dt.series[nx][i].set_visible(check_state)
        # hide theory table
        for th in self.theories.values():
            th.set_th_table_visible(file_matching[0].file_name_short, check_state)

        # save the check_state to recover it upon change of tab or 'view all' events
        if check_state == False:
            self.inactive_files[file_matching[0].file_name_short] = file_matching[0]
        else:
            try:
                del self.inactive_files[file_matching[0].file_name_short]
            except KeyError:
                pass
        self.do_plot()

    def do_show_all(self, line):
        """Show all files in the current DataSet"""
        for file in self.files:
            if file.file_name_short not in self.inactive_files:
                file.active = True
                dt = file.data_table
                for i in range(dt.MAX_NUM_SERIES):
                    for nx in range(self.nplots):  # loop over the plots
                        dt.series[nx][i].set_visible(True)
        if self.current_theory:
            self.theories[self.current_theory].do_show()
        self.do_plot("")

    def do_hide_all(self, line):
        """Hide all files in the current DataSet"""
        for file in self.files:
            file.active = False
            dt = file.data_table
            for i in range(dt.MAX_NUM_SERIES):
                for nx in range(self.nplots):  # loop over the plots
                    dt.series[nx][i].set_visible(False)
        for th in self.theories.values():
            th.do_hide()
        self.do_plot("")

    def do_plot(self, line=""):
        """Plot the current dataset using the current view of the parent application"""
        # view = self.parent_application.current_view

        self.table_icon_list.clear()
        filled = False
        if self.symbolmode == SymbolMode.fixed.value:  # single symbol, empty?
            markers = [self.symbol1]
            marker_names = [self.symbol1_name]
        elif self.symbolmode == SymbolMode.fixedfilled.value:  # single symbol, filled?
            markers = [self.symbol1]
            marker_names = [self.symbol1_name]
            filled = True
        elif self.symbolmode == SymbolMode.variable.value:  # variable symbols, empty
            markers = SymbolMode.allmarkers.value
            marker_names = SymbolMode.allmarkernames.value
        else:  #
            markers = SymbolMode.filledmarkers.value  # variable symbols, filled
            marker_names = SymbolMode.filledmarkernames.value
            filled = True

        if self.colormode == ColorMode.fixed.value:  # single color?
            colors = [self.color1]
        elif self.colormode == ColorMode.variable.value:  # variable colors from palette
            colors = ColorMode.colorpalettes.value[self.palette_name]
        else:
            n = len(self.files) - len(self.inactive_files)  # number of files to plot
            if n < 2:
                colors = [self.color1]  # only one color needed
            else:  # interpolate the color1 and color2
                r1, g1, b1, a1 = self.color1
                r2, g2, b2, a2 = self.color2
                dr = (r2 - r1) / (n - 1)
                dg = (g2 - g1) / (n - 1)
                db = (b2 - b1) / (n - 1)
                da = (a2 - a1) / (n - 1)
                colors = []
                for i in range(n):  # create a color palette
                    colors.append((r1 + i * dr, g1 + i * dg, b1 + i * db, a1 + i * da))

        linelst = itertools.cycle((":", "-", "-.", "--"))
        palette = itertools.cycle((colors))
        markerlst = itertools.cycle((markers))
        marker_name_lst = itertools.cycle((marker_names))
        size = self.marker_size  # if file.size is None else file.size
        width = self.line_width
        # theory settings
        th_linestyle = ThLineMode.linestyles.value[self.th_linestyle]

        for to in self.parent_application.tools:
            to.clean_graphic_stuff()
            if to.active:
                to.Qprint("<hr><h2>Calculating...</h2>")

        for j, file in enumerate(self.files):
            dt = file.data_table

            marker = next(markerlst)  # if file.marker is None else file.marker
            marker_name = next(
                marker_name_lst
            )  # if file.marker is None else file.marker
            color = next(palette)  # if file.color is None else file.color
            face = color if filled else "none"
            if self.th_line_mode == ThLineMode.as_data.value:
                th_color = color
            else:
                th_color = self.th_color
            if file.active:
                # save file name with associated marker shape, fill and color
                self.table_icon_list.append(
                    (file.file_name_short, marker_name, face, color)
                )

            for nx in range(self.nplots):
                view = self.parent_application.multiviews[nx]
                try:
                    x, y, success = view.view_proc(dt, file.file_parameters)
                except TypeError as e:
                    print("in do_plot()", e)
                    return

                ## Apply current shifts to data
                # for i in range(view.n):
                #    if file.isshifted[i]:
                #        if view.log_x:
                #            x[:,i]*=np.power(10, file.xshift[i])
                #        else:
                #            x[:,i]+=file.xshift[i]
                #        if view.log_y:
                #            y[:,i]*=np.power(10, file.yshift[i])
                #        else:
                #            y[:,i]+=file.yshift[i]

                # Apply the currently active tools
                for to in self.parent_application.tools:
                    if file.active and to.active:
                        to.Qprint("<h3>" + file.file_name_short + "</h3>")
                        x, y = to.calculate_all(
                            view.n,
                            x,
                            y,
                            self.parent_application.axarr[nx],
                            color,
                            file.file_parameters,
                        )

                # Apply current shifts to data
                for i in range(view.n):
                    if file.isshifted[i]:
                        if view.log_x:
                            x[:, i] *= np.power(10, file.xshift[i])
                        else:
                            x[:, i] += file.xshift[i]
                        if view.log_y:
                            y[:, i] *= np.power(10, file.yshift[i])
                        else:
                            y[:, i] += file.yshift[i]

                fillstylesempty = itertools.cycle(
                    ("none", "full", "left", "right", "bottom", "top")
                )
                fillstylesfilled = itertools.cycle(
                    ("full", "none", "right", "left", "top", "bottom")
                )
                for i in range(dt.MAX_NUM_SERIES):
                    if i < view.n and file.active:
                        dt.series[nx][i].set_data(x[:, i], y[:, i])
                        dt.series[nx][i].set_visible(True)
                        dt.series[nx][i].set_marker(marker)

                        if filled:
                            fs = next(fillstylesfilled)
                        else:
                            fs = next(fillstylesempty)
                        if fs == "none":
                            face = "none"
                        else:
                            face = color
                        dt.series[nx][i].set_fillstyle(fs)

                        # if i == 0:
                        #     face = color if filled else 'none'
                        # elif i == 1: # filled and empty symbols
                        #     if face == 'none':
                        #         face = color
                        #     elif face == color:
                        #         face = 'none'
                        # else:
                        #     face = color
                        #     fillstyles=["left", "right", "bottom", "top", "full", "left", "right", "bottom", "top", "full", "left", "right", "bottom", "top"]
                        #     fs = fillstyles[i-2]
                        #     dt.series[nx][i].set_fillstyle(fs)
                        dt.series[nx][i].set_markerfacecolor(face)
                        dt.series[nx][i].set_markeredgecolor(color)
                        dt.series[nx][i].set_markeredgewidth(width)
                        dt.series[nx][i].set_markersize(size)
                        dt.series[nx][i].set_linestyle("")
                        if file.active and i == 0:
                            label = ""
                            for pmt in file.file_type.basic_file_parameters:
                                try:
                                    label += (
                                        pmt + "=" + str(file.file_parameters[pmt]) + " "
                                    )
                                except (
                                    KeyError
                                ) as e:  # if parameter missing from data file
                                    self.logger.warning(
                                        "Parameter %s not found in data file" % e
                                    )
                            dt.series[nx][i].set_label(label)
                        else:
                            dt.series[nx][i].set_label("")
                    else:
                        dt.series[nx][i].set_visible(False)
                        dt.series[nx][i].set_label("")

                # Cycle over theory linestyles - JR
                th_linestyleJR = itertools.cycle(ThLineMode.linestylenames.value)

                for th in self.theories.values():
                    if th.active:
                        th.plot_theory_stuff()
                    tt = th.tables[file.file_name_short]
                    try:
                        x, y, success = view.view_proc(tt, file.file_parameters)
                    except Exception as e:
                        print("in do_plot th", e)
                        continue

                    # Apply the currently active tools
                    for to in self.parent_application.tools:
                        if file.active and to.active and to.applytotheory:
                            to.Qprint("* <i>" + th.name + "</i>")
                            x, y = to.calculate_all(
                                view.n,
                                x,
                                y,
                                self.parent_application.axarr[nx],
                                color,
                                file.file_parameters,
                            )

                    for i in range(tt.MAX_NUM_SERIES):
                        if i < view.n and file.active and th.active:
                            tt.series[nx][i].set_data(x[:, i], y[:, i])
                            tt.series[nx][i].set_visible(True)
                            if view.with_thline or i > 0:
                                tt.series[nx][i].set_marker("")

                                # JR - Cycle over theory linestyles
                                th_linestyle = ThLineMode.linestyles.value[
                                    next(th_linestyleJR)
                                ]

                                # if i == 1:  # 2nd theory line with different style
                                #     if self.th_linestyle == "solid":
                                #         th_linestyle = ThLineMode.linestyles.value[
                                #             "dashed"
                                #         ]
                                #     else:
                                #         th_linestyle = ThLineMode.linestyles.value[
                                #             "solid"
                                #         ]
                                # elif i == 2:  # 3rd theory line with different style
                                #     if self.th_linestyle == "solid":
                                #         th_linestyle = ThLineMode.linestyles.value[
                                #             "dashdotted"
                                #         ]
                                #     else:
                                #         th_linestyle = ThLineMode.linestyles.value[
                                #             "dotted"
                                #         ]
                                # else:
                                #     th_linestyle = ThLineMode.linestyles.value[
                                #         self.th_linestyle
                                #     ]
                                tt.series[nx][i].set_linestyle(th_linestyle)
                            else:
                                tt.series[nx][i].set_linestyle("")
                                tt.series[nx][i].set_marker(".")
                                if view.filled:
                                    tt.series[nx][i].set_markerfacecolor(th_color)
                                else:
                                    tt.series[nx][i].set_markerfacecolor("none")
                                tt.series[nx][i].set_markersize(size)

                            tt.series[nx][i].set_linewidth(self.th_line_width)
                            tt.series[nx][i].set_color(th_color)
                            tt.series[nx][i].set_label("")
                            tt.series[nx][i].set_path_effects([pe.Normal()])
                        else:
                            tt.series[nx][i].set_visible(False)
                            tt.series[nx][i].set_label("")
        # self.parent_application.update_datacursor_artists()
        self.parent_application.update_plot()

    def do_sort(self, line):
        """Sort files in dataset according to the value of a file parameter

        Examples:
            sort Mw,reverse
            sort T

        Arguments:
            - Par {[str]} -- File parameter according to which the files will be sorted
            - reverse -- The files will be sorted in reverse order"""
        items = line.split(",")
        if len(items) == 0:
            print("Wrong number of arguments")
        elif len(items) == 1:
            fp = items[0]
            rev = False
        elif len(items) == 2:
            fp = items[0]
            rev = items[1].strip() == "reverse"
        else:
            print("Wrong number of arguments")

        if self.current_file:
            if fp in self.current_file.file_parameters:
                self.files.sort(key=lambda x: float(x.file_parameters[fp]), reverse=rev)
                self.do_plot()
            elif fp == "File":
                self.files.sort(key=lambda x: x.file_name_short, reverse=rev)
                self.do_plot()
            else:
                self.logger.warning("Parameter %s not found in files" % line)
                # print("Parameter %s not found in files" % line)

    def new_dummy_file(
        self,
        fname="",
        xrange=[],
        yval=0,
        zval=None,
        z2val=None,
        fparams={},
        file_type=None,
    ):
        """Create File from xrange and file parameters
        xrange: list of x points
        yval: float
        fparam: dict containing file parameter names and values
        """
        if fname == "":
            filename = (
                "dummy_"
                + "_".join([pname + "%.3g" % fparams[pname] for pname in fparams])
                + "."
                + file_type.extension
            )
        else:
            str = ""
            for pname in fparams:
                try:
                    str += pname + "%.3g" % fparams[pname]
                except TypeError:
                    str += pname + fparams[pname]
            filename = fname + str + "." + file_type.extension

        f = File(
            file_name=filename,
            file_type=file_type,
            parent_dataset=self,
            axarr=self.parent_application.axarr,
        )
        f.file_parameters = fparams
        dt = f.data_table
        dt.num_columns = len(file_type.col_names)
        dt.num_rows = len(xrange)
        dt.data = np.zeros((dt.num_rows, dt.num_columns))
        dt.data[:, 0] = xrange
        if isinstance(yval, list):
            for i in range(1, dt.num_columns):
                dt.data[:, i] = yval[:]
        else:
            for i in range(1, dt.num_columns):
                dt.data[:, i] = yval
        if dt.num_columns > 2:
            if zval is None:
                dt.data[:, 2] = np.nan
            else:
                dt.data[:, 2] = zval[:]
        if dt.num_columns > 3:
            if z2val is None:
                dt.data[:, 3] = np.nan
            else:
                dt.data[:, 3] = z2val[:]
        unique = True
        for file in self.files:
            if (
                f.file_name_short == file.file_name_short
            ):  # check if file already exists in current ds
                unique = False
        if unique:
            self.files.append(f)
            self.current_file = f
            for th_name in self.theories:
                # add a theory table
                self.theories[th_name].tables[f.file_name_short] = DataTable(
                    self.parent_application.axarr, "TH_" + f.file_name_short
                )
                self.theories[th_name].function(f)
            return f, True
        else:
            return None, False

    def do_open(self, line):
        """Open file(s). Arguments: FILENAME(s) (pattern expansion characters -- \*, ? -- allowed"""
        f_names = line
        newtables = []
        if line == "" or len(f_names) == 0:
            message = "No valid file names provided"
            return (message, None, None)
        f_ext = [os.path.splitext(x)[1].split(".")[-1] for x in f_names]
        if f_ext.count(f_ext[0]) != len(f_ext):
            message = "File extensions of files must be equal!"
            return (message, None, None)
        if f_ext[0] in self.parent_application.filetypes:
            ft = self.parent_application.filetypes[f_ext[0]]
            for f in f_names:
                if not os.path.isfile(f):
                    print('File "%s" does not exists' % f)
                    continue  # next file name
                df = ft.read_file(f, self, self.parent_application.axarr)
                unique = True
                for file in self.files:
                    if (
                        df.file_name_short == file.file_name_short
                    ):  # check if file already exists in current ds
                        unique = False
                if unique:
                    self.files.append(df)
                    self.current_file = df
                    newtables.append(df)
                    for th_name in self.theories:
                        # add a theory table
                        self.theories[th_name].tables[df.file_name_short] = DataTable(
                            self.parent_application.axarr, "TH_" + df.file_name_short
                        )
            return (True, newtables, f_ext[0])
        else:
            message = 'File type "%s" does not exists' % f_ext[0]
            return (message, None, None)

    def do_reload_data(self, line=""):
        """Reload data files in the current DataSet"""
        for file in self.files:
            if not file.active:
                continue
            path = file.file_full_path
            ft = file.file_type
            if not os.path.isfile(path):
                self.logger.warning(
                    "Could not open file %s: %s" % (file.file_name_short, path)
                )
                continue
            df = ft.read_file(path, self, None)
            file.header_lines = df.header_lines[:]
            file.file_parameters.clear()
            file.file_parameters.update(df.file_parameters)
            file.data_table.data = np.array(df.data_table.data)
            file.data_table.num_columns = df.data_table.num_columns
            file.data_table.num_rows = df.data_table.num_rows
        self.do_plot("")

    def __listdir(self, root):
        """List directory 'root' appending the path separator to subdirs."""
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
                # name += '/'
            res.append(name)
        return res

    def do_delete(self, name):
        """Delete a theory from the current dataset"""
        if name in self.theories.keys():
            self.theories[name].destructor()
            for tt in self.theories[
                name
            ].tables.values():  # remove matplotlib artist from ax
                for i in range(tt.MAX_NUM_SERIES):
                    for nx in range(self.nplots):
                        tt.series[nx][i].remove()
                        # self.parent_application.axarr[nx].lines.remove(tt.series[nx][i])
            del self.theories[name]
            self.do_plot("")
        else:
            print('Theory "%s" not found' % name)

    def do_save(self, line="", extra_txt=""):
        """Save the active files of the current dataset to file"""
        counter = 0

        for f in self.files:
            ttable = self.tables[f.file_name_short]
            ofilename = f.file_full_path
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

    def new(self, line):
        """Create a new theory"""
        """Add a new theory of the type specified to the current Data Set"""
        thtypes = list(self.parent_application.theories.keys())
        if line in thtypes:
            if self.current_file is None:
                print("Current dataset is empty\n" "%s was not created" % line)
                return
            self.num_theories += 1
            th_id = "".join(
                c for c in line if c.isupper()
            )  # get the upper case letters of th_name
            th_id = "%s%d" % (th_id, self.num_theories)  # append number
            th = self.parent_application.theories[line](
                th_id, self, self.parent_application.axarr
            )
            self.theories[th.name] = th
            self.current_theory = th.name
            if th.autocalculate:
                th.do_calculate("")
            else:
                th.Qprint('<font color=green><b>Press "Calculate"</b></font>')
            return th, th_id
        else:
            print('Theory "%s" does not exists' % line)
            return None, None

    def do_new(self, line, calculate=True):
        """Add a new theory of the type specified to the current Data Set"""
        thtypes = list(self.parent_application.theories.keys())
        if line in thtypes:
            if self.current_file is None:
                print("Current dataset is empty\n" "%s was not created" % line)
                return
            self.num_theories += 1
            # th_id = "%s%02d"%(line,self.num_theories)
            # th_id = ''.join(c for c in line if c.isupper()) #get the upper case letters of th_name
            # th_id = "%s%02d" % (line, self.num_theories)
            th_id = "".join(
                c for c in line if c.isupper()
            )  # get the upper case letters of th_name
            th_id = "%s%d" % (th_id, self.num_theories)  # append number
            th = self.parent_application.theories[line](
                th_id, self, self.parent_application.axarr
            )
            self.theories[th.name] = th
            self.current_theory = th.name
            if calculate and th.autocalculate:
                th.do_calculate("")
            else:
                th.Qprint('<font color=green><b>Press "Calculate"</b></font>')
            return th
        else:
            print('Theory "%s" does not exists' % line)

    def mincol(self, col):
        """Minimum value in table column line of all Files in DataSet"""
        min = 1e100
        for f in self.files:
            minfile = f.mincol(col)
            if minfile < min:
                min = minfile
        return min

    def minpositivecol(self, col):
        """Minimum positive value in table column line of all Files in DataSet"""
        min = 1e100
        for f in self.files:
            minfile = f.minpositivecol(col)
            if minfile < min:
                min = minfile
        return min

    def maxcol(self, col):
        """Maximum value in table column line of all Files in DataSet"""
        max = -1e100
        for f in self.files:
            maxfile = f.maxcol(col)
            if maxfile > max:
                max = maxfile
        return max

    def copy_parameters(self):
        """Copy the parameters of the currently active theory to the clipboard"""
        th = self.current_theory
        if th:
            self.theories[th].copy_parameters()

    def paste_parameters(self):
        """Paste the parameters from the clipboard to the currently active theory"""
        th = self.current_theory
        if th:
            self.theories[th].paste_parameters()

    def handle_action_save_current_dataset(self):
        """Save data of the current dataset to file"""
        dir_start = join(RepTate.root_dir, "data")
        dilogue_name = "Select Folder"
        folder = QFileDialog.getExistingDirectory(self, dilogue_name, dir_start)
        if isdir(folder):
            dialog = QInputDialog(self)
            dialog.setWindowTitle("Add label to filename(s)?")
            dialog.setLabelText(
                "Add the following text to each saved theory filename(s):"
            )
            dialog.setTextValue("")
            dialog.setCancelButtonText("None")
            if dialog.exec():
                txt = dialog.textValue()
                if txt != "":
                    txt = "_" + txt
            else:
                txt = ""
            self.do_save(folder, txt)

    def handle_action_save_theory_data(self):
        """Save theory data of current theory"""
        th = self.current_theory
        if th:
            # file browser window
            dir_start = join(RepTate.root_dir, "data")
            dilogue_name = "Select Folder"
            folder = QFileDialog.getExistingDirectory(self, dilogue_name, dir_start)
            if isdir(folder):
                dialog = QInputDialog(self)
                dialog.setWindowTitle("Add label to filename(s)?")
                dialog.setLabelText(
                    "Add the following text to each saved theory filename(s):"
                )
                dialog.setTextValue("")
                dialog.setCancelButtonText("None")
                if dialog.exec():
                    txt = dialog.textValue()
                    if txt != "":
                        txt = "_" + txt
                else:
                    txt = ""
                self.theories[th].do_save(folder, txt)

    def set_table_icons(self, table_icon_list):
        """The list 'table_icon_list' contains tuples (file_name_short, marker_name, face, color)"""
        self.DataSettreeWidget.blockSignals(
            True
        )  # avoid triggering 'itemChanged' signal that causes a call to do_plot()

        for fname, marker_name, face, color in table_icon_list:
            item = self.DataSettreeWidget.findItems(
                fname, Qt.MatchCaseSensitive, column=0
            )  # returns list of items matching file name
            if item:
                # paint icon
                folder = ":/Markers/Images/Matplotlib_markers/"
                if face == "none":  # empty symbol
                    marker_path = folder + "marker_%s" % marker_name
                else:  # filled symbol
                    marker_path = folder + "marker_filled_%s" % marker_name
                qp = QPixmap(marker_path)
                mask = qp.createMaskFromColor(QColor(0, 0, 0), Qt.MaskOutColor)
                qpainter = QPainter()
                qpainter.begin(qp)
                qpainter.setPen(
                    QColor(
                        int(255 * color[0]),
                        int(255 * color[1]),
                        int(255 * color[2]),
                        255,
                    )
                )
                qpainter.drawPixmap(qp.rect(), mask, qp.rect())
                qpainter.end()
                item[0].setIcon(0, QIcon(qp))

        self.DataSettreeWidget.blockSignals(False)

    def theory_actions_disabled(self, state):
        """Disable theory buttons if no theory tab is open"""
        self.actionCalculate_Theory.setDisabled(state)
        self.actionMinimize_Error.setDisabled(state)
        # self.actionTheory_Options.setDisabled(state)
        self.actionShow_Limits.setDisabled(state)
        self.actionVertical_Limits.setDisabled(state)
        self.actionHorizontal_Limits.setDisabled(state)
        self.action_save_theory_data.setDisabled(state)

    def set_limit_icon(self):
        """Set xrange / yrange"""
        if self.current_theory:
            th = self.theories[self.current_theory]
        vlim = th.is_xrange_visible
        hlim = th.is_yrange_visible
        if hlim and vlim:
            img = "Line Chart Both Limits"
        elif vlim:
            img = "Line Chart Vertical Limits"
        elif hlim:
            img = "Line Chart Horizontal Limits"
        else:
            img = "Line Chart"
        self.actionShow_Limits.setIcon(QIcon(":/Images/Images/%s.png" % img))

    def set_no_limits(self, th_name):
        """Turn the x and yrange selectors off"""
        if th_name in self.theories:
            self.theories[self.current_theory].set_xy_limits_visible(
                False, False
            )  # hide xrange and yrange

    def toggle_vertical_limits(self, checked):
        """Show/Hide the xrange selector for fit"""
        if self.current_theory:
            th = self.theories[self.current_theory]
            th.do_xrange("", checked)
            th.is_xrange_visible = checked
            self.set_limit_icon()

    def toggle_horizontal_limits(self, checked):
        """Show/Hide the yrange selector for fit"""
        if self.current_theory:
            th = self.theories[self.current_theory]
            th.do_yrange("", checked)
            th.is_yrange_visible = checked
            self.set_limit_icon()

    def handle_fitting_options(self):
        if not self.current_theory:
            return
        th = self.theories[self.current_theory]
        th.fittingoptionsdialog.ui.tabWidget.setCurrentIndex(th.mintype.value)
        success = (
            th.fittingoptionsdialog.exec_()
        )  # this blocks the rest of the app as opposed to .show()

        if not success:
            return

        th.mintype = MinimizationMethod(
            th.fittingoptionsdialog.ui.tabWidget.currentIndex()
        )
        if th.mintype == MinimizationMethod.ls:
            th.LSmethod = th.fittingoptionsdialog.ui.LSmethodcomboBox.currentText()
            if th.fittingoptionsdialog.ui.LSftolcheckBox.isChecked():
                th.LSftol = float(th.fittingoptionsdialog.ui.LSftollineEdit.text())
            else:
                th.LSftol = None
            if th.fittingoptionsdialog.ui.LSxtolcheckBox.isChecked():
                th.LSxtol = float(th.fittingoptionsdialog.ui.LSxtollineEdit.text())
            else:
                th.LSxtol = None
            if th.fittingoptionsdialog.ui.LSgtolcheckBox.isChecked():
                th.LSgtol = float(th.fittingoptionsdialog.ui.LSgtollineEdit.text())
            else:
                th.LSgtol = None
            th.LSloss = th.fittingoptionsdialog.ui.LSlosscomboBox.currentText()
            th.LSf_scale = float(th.fittingoptionsdialog.ui.LSf_scalelineEdit.text())
            if th.fittingoptionsdialog.ui.LSmax_nfevcheckBox.isChecked():
                th.LSmax_nfev = int(
                    th.fittingoptionsdialog.ui.LSmax_nfevlineEdit.text()
                )
            else:
                th.LSmax_nfev = None
            if th.fittingoptionsdialog.ui.LStr_solvercheckBox.isChecked():
                th.LStr_solver = (
                    th.fittingoptionsdialog.ui.LStr_solvercomboBox.currentText()
                )
            else:
                th.LStr_solver = None

        elif th.mintype == MinimizationMethod.basinhopping:
            th.basinniter = int(th.fittingoptionsdialog.ui.basinniterlineEdit.text())
            th.basinT = float(th.fittingoptionsdialog.ui.basinTlineEdit.text())
            th.basinstepsize = float(
                th.fittingoptionsdialog.ui.basinstepsizelineEdit.text()
            )
            th.basininterval = int(
                th.fittingoptionsdialog.ui.basinintervallineEdit.text()
            )
            if th.fittingoptionsdialog.ui.basinniter_successcheckBox.isChecked():
                th.basinniter_success = int(
                    th.fittingoptionsdialog.ui.basinniter_successlineEdit.text()
                )
            else:
                th.basinniter_success = None
            if th.fittingoptionsdialog.ui.basinseedcheckBox.isChecked():
                th.basinseed = int(th.fittingoptionsdialog.ui.basinseedlineEdit.text())
            else:
                th.basinseed = None

        elif th.mintype == MinimizationMethod.dualannealing:
            th.annealmaxiter = int(
                th.fittingoptionsdialog.ui.annealmaxiterlineEdit.text()
            )
            th.annealinitial_temp = float(
                th.fittingoptionsdialog.ui.annealinitial_templineEdit.text()
            )
            th.annealrestart_temp_ratio = float(
                th.fittingoptionsdialog.ui.annealrestart_temp_ratiolineEdit.text()
            )
            th.annealvisit = float(
                th.fittingoptionsdialog.ui.annealvisitlineEdit.text()
            )
            th.annealaccept = float(
                th.fittingoptionsdialog.ui.annealacceptlineEdit.text()
            )
            th.annealmaxfun = int(
                th.fittingoptionsdialog.ui.annealmaxfunlineEdit.text()
            )
            if th.fittingoptionsdialog.ui.annealseedcheckBox.isChecked():
                th.annealseed = int(
                    th.fittingoptionsdialog.ui.annealseedlineEdit.text()
                )
            else:
                th.annealseed = None
            th.annealno_local_search = (
                th.fittingoptionsdialog.ui.annealno_local_searchcheckBox.isChecked()
            )

        elif th.mintype == MinimizationMethod.diffevol:
            th.diffevolstrategy = (
                th.fittingoptionsdialog.ui.diffevolstrategycomboBox.currentText()
            )
            th.diffevolmaxiter = int(
                th.fittingoptionsdialog.ui.diffevolmaxiterlineEdit.text()
            )
            th.diffevolpopsize = int(
                th.fittingoptionsdialog.ui.diffevolpopsizelineEdit.text()
            )
            th.diffevoltol = float(
                th.fittingoptionsdialog.ui.diffevoltollineEdit.text()
            )
            th.diffevolmutation = (
                float(th.fittingoptionsdialog.ui.diffevolmutationAlineEdit.text()),
                float(th.fittingoptionsdialog.ui.diffevolmutationBlineEdit.text()),
            )
            th.diffevolrecombination = float(
                th.fittingoptionsdialog.ui.diffevolrecombinationlineEdit.text()
            )
            if th.fittingoptionsdialog.ui.diffevolseedcheckBox.isChecked():
                th.diffevolseed = int(
                    th.fittingoptionsdialog.ui.diffevolseedlineEdit.text()
                )
            else:
                th.diffevolseed = None
            th.diffevolpolish = (
                th.fittingoptionsdialog.ui.diffevolpolishcheckBox.isChecked()
            )
            th.diffevolinit = (
                th.fittingoptionsdialog.ui.diffevolinitcomboBox.currentText()
            )
            th.diffevolatol = float(
                th.fittingoptionsdialog.ui.diffevolatollineEdit.text()
            )

        elif th.mintype == MinimizationMethod.SHGO:
            th.SHGOn = int(th.fittingoptionsdialog.ui.SHGOnlineEdit.text())
            th.SHGOiters = int(th.fittingoptionsdialog.ui.SHGOiterslineEdit.text())
            if th.fittingoptionsdialog.ui.SHGOmaxfevcheckBox.isChecked():
                th.SHGOmaxfev = int(
                    th.fittingoptionsdialog.ui.SHGOmaxfevlineEdit.text()
                )
            else:
                th.SHGOmaxfev = None
            if th.fittingoptionsdialog.ui.SHGOf_mincheckBox.isChecked():
                th.SHGOf_min = float(
                    th.fittingoptionsdialog.ui.SHGOf_minlineEdit.text()
                )
            else:
                th.SHGOf_min = None
            th.SHGOf_tol = float(th.fittingoptionsdialog.ui.SHGOf_tollineEdit.text())
            if th.fittingoptionsdialog.ui.SHGOmaxitercheckBox.isChecked():
                th.SHGOmaxiter = int(
                    th.fittingoptionsdialog.ui.SHGOmaxiterlineEdit.text()
                )
            else:
                th.SHGOmaxiter = None
            if th.fittingoptionsdialog.ui.SHGOmaxevcheckBox.isChecked():
                th.SHGOmaxev = int(th.fittingoptionsdialog.ui.SHGOmaxevlineEdit.text())
            else:
                th.SHGOmaxev = None
            if th.fittingoptionsdialog.ui.SHGOmaxtimecheckBox.isChecked():
                th.SHGOmaxtime = float(
                    th.fittingoptionsdialog.ui.SHGOmaxtimelineEdit.text()
                )
            else:
                th.SHGOmaxtime = None
            if th.fittingoptionsdialog.ui.SHGOminhgrdcheckBox.isChecked():
                th.SHGOminhgrd = int(
                    th.fittingoptionsdialog.ui.SHGOminhgrdlineEdit.text()
                )
            else:
                th.SHGOminhgrd = None
            th.SHGOminimize_every_iter = (
                th.fittingoptionsdialog.ui.SHGOminimize_every_itercheckBox.isChecked()
            )
            th.SHGOlocal_iter = (
                th.fittingoptionsdialog.ui.SHGOlocal_itercheckBox.isChecked()
            )
            th.SHGOinfty_constraints = (
                th.fittingoptionsdialog.ui.SHGOinfty_constraintscheckBox.isChecked()
            )
            th.SHGOsampling_method = (
                th.fittingoptionsdialog.ui.SHGOsampling_methodcomboBox.currentText()
            )

        elif th.mintype == MinimizationMethod.bruteforce:
            th.BruteNs = int(th.fittingoptionsdialog.ui.BruteNslineEdit.text())

        # if th.mintype==MinimizationMethod.trf:
        #     th.mintype=MinimizationMethod.basinhopping
        # elif th.mintype==MinimizationMethod.basinhopping:
        #     th.mintype=MinimizationMethod.dualannealing
        # elif th.mintype==MinimizationMethod.dualannealing:
        #     th.mintype=MinimizationMethod.differential_evolution
        # else:
        #     th.mintype=MinimizationMethod.trf

    def handle_error_calculation_options(self):
        if not self.current_theory:
            return
        th = self.theories[self.current_theory]
        success = (
            th.errorcalculationdialog.exec_()
        )  # this blocks the rest of the app as opposed to .show()

        if not success:
            return

        if th.errorcalculationdialog.ui.View1radioButton.isChecked():
            th.errormethod = ErrorCalculationMethod.View1
        elif th.errorcalculationdialog.ui.RawDataradioButton.isChecked():
            th.errormethod = ErrorCalculationMethod.RawData
        elif th.errorcalculationdialog.ui.AllViewsradioButton.isChecked():
            th.errormethod = ErrorCalculationMethod.AllViews

        th.normalizebydata = th.errorcalculationdialog.ui.NormalizecheckBox.isChecked()

    def end_of_computation(self, th_name):
        """Action when theory has finished computations"""
        try:
            th = self.theories[th_name]
            th.stop_theory_flag = False
        except KeyError:
            pass
        if self.current_theory == th_name:
            self.icon_calculate_is_stop(False)
            self.icon_fit_is_stop(False)

    def handle_actionCalculate_Theory(self):
        if self.current_theory and self.files:
            th = self.theories[self.current_theory]
            if th.thread_calc_busy:  # request stop if in do_calculate
                th.request_stop_computations()
                return
            elif (
                th.is_fitting or th.thread_fit_busy
            ):  # do nothing if already busy in do_fit
                th.Qprint("Busy minimising theory...")
                return
            if th.single_file and (len(self.files) - len(self.inactive_files)) > 1:
                header = "Calculate"
                message = (
                    '<p>Too many active files: "%s" uses only one data file.</p>\
                    <p>The theory will be applied to the highlighted file if any or to the first active file.</p>'
                    % th.thname
                )
                QMessageBox.warning(self, header, message)
            self.icon_calculate_is_stop(True)
            th.handle_actionCalculate_Theory()

    def handle_actionMinimize_Error(self):
        """Minimize the error"""
        if self.current_theory and self.files:
            th = self.theories[self.current_theory]
            if th.is_fitting or th.thread_fit_busy:  # request stop if in do_fit
                th.request_stop_computations()
                return
            elif (
                th.calculate_is_busy or th.thread_calc_busy
            ):  # do nothing if already busy in do_calculate
                th.Qprint("Busy calculating theory...")
                return
            if th.single_file and (len(self.files) - len(self.inactive_files)) > 1:
                header = "Minimization"
                message = (
                    '<p>Too many active files: "%s" uses only one data file.</p>\
                    <p>The theory will be applied to the highlighted file if any or to the first active file.</p>'
                    % th.thname
                )
                QMessageBox.warning(self, header, message)
            self.icon_fit_is_stop(True)
            th.handle_actionMinimize_Error()

    def icon_calculate_is_stop(self, ans):
        """Change the "calculate" button to "stop" button"""
        if ans:
            self.actionCalculate_Theory.setIcon(
                QIcon(":/Icon8/Images/new_icons/icons8-stop-sign.png")
            )
            self.actionCalculate_Theory.setToolTip("Stop current calculations")
        else:
            self.actionCalculate_Theory.setIcon(
                QIcon(":/Icon8/Images/new_icons/icons8-abacus.png")
            )
            self.actionCalculate_Theory.setToolTip("Calculate Theory (Alt+C)")

    def icon_fit_is_stop(self, ans):
        """Change the "fit" button to "stop" button"""
        if ans:
            self.actionMinimize_Error.setIcon(
                QIcon(":/Icon8/Images/new_icons/icons8-stop-sign.png")
            )
            self.actionCalculate_Theory.setToolTip("Stop current calculations")
        else:
            self.actionMinimize_Error.setIcon(
                QIcon(":/Icon8/Images/new_icons/icons8-minimum-value.png")
            )
            self.actionCalculate_Theory.setToolTip("Calculate Theory (Alt+C)")

    def handle_thCurrentChanged(self, index):
        """Change figure when the active theory tab is changed"""
        self.icon_calculate_is_stop(False)
        self.icon_fit_is_stop(False)
        th = self.TheorytabWidget.widget(index)
        if th:
            self.current_theory = th.name
            ntab = self.TheorytabWidget.count()
            # hide all theory curves
            for i in range(ntab):
                if i != index:
                    th_to_hide = self.TheorytabWidget.widget(i)
                    th_to_hide.do_hide()
            th.do_show()  # must be called last, after hiding other theories

            if th.thread_calc_busy or th.thread_fit_busy:
                self.icon_calculate_is_stop(th.thread_calc_busy)
                self.icon_fit_is_stop(th.thread_fit_busy)
                return
        else:
            self.current_theory = None
            self.theory_actions_disabled(True)
        self.parent_application.update_plot()
        self.parent_application.update_Qplot()

    def handle_thTabBarDoubleClicked(self, index):
        """Edit Theory name

        Edit the theory tab name, leave 'theories' dictionary keys unchanged.
        Two tabs can share the same name"""
        old_name = self.TheorytabWidget.tabText(index)
        dlg = QInputDialog(self)
        dlg.setWindowTitle("Change Theory Name")
        dlg.setLabelText("New Theory Name:")
        dlg.setTextValue(old_name)
        dlg.resize(400, 100)
        success = dlg.exec()
        new_tab_name = dlg.textValue()
        if success and new_tab_name != "":
            self.TheorytabWidget.setTabText(index, new_tab_name)
            # self.theories[old_name].name = new_tab_name
            # self.theories[new_tab_name] = self.theories.pop(old_name)
            # self.current_theory = new_tab_name

    def handle_thTabCloseRequested(self, index):
        """Delete a theory tab from the current dataset"""
        th_name = self.TheorytabWidget.widget(index).name
        th = self.theories[th_name]
        th.Qprint("Close theory tab requested")
        th.request_stop_computations()
        self.set_no_limits(th_name)
        self.do_delete(th_name)  # call DataSet.do_delete
        self.TheorytabWidget.removeTab(index)

    def handle_itemSelectionChanged(self):
        """Define actions for when a file table is selected"""
        selection = self.DataSettreeWidget.selectedItems()
        if selection == []:
            self.selected_file = None
            self.highlight_series()
            return
        for f in self.files:
            if f.file_name_short == selection[0].text(0):
                self.parent_application.disconnect_curve_drag()
                self.selected_file = f
                self.highlight_series()
                self.populate_inspector()
                self.parent_application.handle_actionShiftTriggered()

    def highlight_series(self):
        """Highligh the data series of the selected file"""
        self.do_plot()  # remove current series highlight
        file = self.selected_file
        thname = self.current_theory
        if thname:
            th = self.theories[thname]
        else:
            th = None
        if file is not None:
            dt = file.data_table
            if th:
                tt = th.tables[file.file_name_short]
            for i in range(dt.MAX_NUM_SERIES):
                for nx in range(self.nplots):
                    view = self.parent_application.multiviews[nx]
                    if i < view.n and file.active:
                        dt.series[nx][i].set_marker(".")
                        # dt.series[nx][i].set_linestyle(":")
                        dt.series[nx][i].set_markerfacecolor(
                            dt.series[nx][i].get_markeredgecolor()
                        )
                        dt.series[nx][i].set_markeredgecolor("peachpuff")
                        dt.series[nx][i].set_markersize(self.marker_size + 3)
                        dt.series[nx][i].set_markeredgewidth(2)
                        dt.series[nx][i].set_zorder(
                            self.parent_application.zorder
                        )  # put series on top
                        if th:
                            if th.active:
                                tt.series[nx][i].set_color("k")
                                tt.series[nx][i].set_path_effects(
                                    [
                                        pe.Stroke(
                                            linewidth=self.th_line_width + 3,
                                            foreground="chartreuse",
                                        ),
                                        pe.Normal(),
                                    ]
                                )
                                tt.series[nx][i].set_zorder(
                                    self.parent_application.zorder
                                )

            self.parent_application.zorder += 1
        self.parent_application.update_plot()

    def populate_inspector(self):
        """Fill the data inspector table"""
        file = self.selected_file
        if not file:
            self.parent_application.inspector_table.setRowCount(0)
            self.parent_application.DataInspectordockWidget.setWindowTitle("File:")
            return
        if self.parent_application.DataInspectordockWidget.isHidden():
            return
        dt = file.data_table
        nrow = dt.num_rows
        ncol = dt.num_columns
        inspec_tab = self.parent_application.inspector_table
        inspec_tab.file_repr = file
        inspec_tab.setRowCount(nrow)
        inspec_tab.setColumnCount(ncol)
        for i in range(nrow):
            for j in range(ncol):
                item = QTableWidgetItem("%.3e" % dt.data[i, j])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                inspec_tab.setItem(i, j, item)  # dt.setItem(row, column, item)
        ds_index = self.parent_application.DataSettabWidget.currentIndex()
        self.parent_application.DataInspectordockWidget.setWindowTitle(
            'File: "%s" in %s'
            % (
                file.file_name_short,
                self.parent_application.DataSettabWidget.tabText(ds_index),
            )
        )
        inspec_tab.resizeColumnsToContents()
        inspec_tab.resizeRowsToContents()
        # Update shift factors
        for i in range(DataTable.MAX_NUM_SERIES):
            self.parent_application.update_shifts(0, 0, i)

    def handle_itemChanged(self, item, column):
        """Detect when an item has been selected in the dataset"""
        if column == 0:
            self.change_file_visibility(
                item.text(0), item.checkState(column) == Qt.Checked
            )

    def handle_sortIndicatorChanged(self, column, order):
        """Sort files according to the selected parameter (column) and replot"""
        # if column == 0: #do not sort file name
        #     return
        if self.DataSettreeWidget.topLevelItemCount() > 0:
            # sort iff there are some files in the dataset
            sort_param = self.DataSettreeWidget.headerItem().text(column)
            rev = True if order == Qt.AscendingOrder else False
            if rev:
                sort_param = sort_param + ",reverse"
            self.do_sort(sort_param)
            self.do_plot()
            self.set_table_icons(self.table_icon_list)

    def Qshow_all(self):
        """Show all the files in this dataset, except those previously hiden"""
        self.do_show_all("")
        for i in range(self.DataSettreeWidget.topLevelItemCount()):
            file_name = self.DataSettreeWidget.topLevelItem(i).text(0)
            if file_name in self.inactive_files:
                self.DataSettreeWidget.topLevelItem(i).setCheckState(0, Qt.Unchecked)
            else:
                self.DataSettreeWidget.topLevelItem(i).setCheckState(0, Qt.Checked)

    def resizeEvent(self, evt=None):
        """Resize dataset"""
        hd = self.DataSettreeWidget.header()
        w = self.DataSettreeWidget.width()
        w /= hd.count()
        for i in range(hd.count()):
            hd.resizeSection(i, w)
            # hd.setTextAlignment(i, Qt.AlignHCenter)

    def handle_itemDoubleClicked(self, item, column):
        """Edit item entry upon double click"""
        # if column>0:
        #     param = self.DataSettreeWidget.headerItem().text(column) #retrive parameter name
        #     file_name_short = item.text(0) #retrive file name
        #     header = "Edit Parameter"
        #     message = "Do you want to edit %s of \"%s\"?"%(param, file_name_short)
        #     answer = QMessageBox.question(self, header, message)
        #     if answer == QMessageBox.Yes:
        #         old_value = item.text(column) #old parameter value
        #         message = "New value of %s"%param
        #         new_value, success = QInputDialog.getDouble(self, header, message, float(old_value))
        #         if success:
        #             for file in self.files:
        #                 if file.file_name_short == file_name_short:
        #                     file.file_parameters[param] = new_value #change value in DataSet
        #             self.DataSettreeWidget.blockSignals(True) #avoid triggering 'itemChanged' signal that causes a false checkbox change
        #             item.setText(column, str(new_value)) #change table label
        #             self.DataSettreeWidget.blockSignals(False)
        # else:
        file_name_short = item.text(0)
        for file in self.files:
            if file.file_name_short == file_name_short:
                d = EditFileParametersDialog(self, file)
                if d.exec_():
                    for p in d.param_dict:
                        if isinstance(file.file_parameters[p], str):
                            file.file_parameters[p] = d.param_dict[p].text()
                        else:
                            try:
                                file.file_parameters[p] = float(d.param_dict[p].text())
                            except Exception as e:
                                print(e)
                        for i in range(self.DataSettreeWidget.columnCount()):
                            if p == self.DataSettreeWidget.headerItem().text(i):
                                item.setText(i, str(file.file_parameters[p]))
                    # theory xmin/max
                    try:
                        file.theory_xmin = float(d.th_xmin.text())
                    except ValueError:
                        file.theory_xmin = "None"
                    try:
                        file.theory_xmax = float(d.th_xmax.text())
                    except ValueError:
                        file.theory_xmax = "None"
                    # theory logspace and Npoints
                    try:
                        file.th_num_pts = float(d.th_num_pts.text())
                    except ValueError:
                        pass
                    try:
                        file.th_num_pts = max(int(d.th_num_pts.text()), 2)
                    except ValueError:
                        pass
                    file.theory_logspace = d.th_logspace.isChecked()
                    file.with_extra_x = d.with_extra_x.isChecked() and (
                        file.theory_xmin != "None" or file.theory_xmax != "None"
                    )

    def handle_actionNew_Theory(self):
        """Create new theory and do fit"""
        self.actionNew_Theory.setDisabled(True)
        if self.cbtheory.currentIndex() == 0:
            # by default, open first theory in the list
            th_name = self.cbtheory.itemText(1)
        else:
            th_name = self.cbtheory.currentText()
        self.cbtheory.setCurrentIndex(0)  # reset the combobox selection
        if th_name != "":
            self.new_theory(th_name)
        self.actionNew_Theory.setDisabled(False)

    def new_theory(self, th_name, th_tab_id="", calculate=True, show=True):
        """Create a new theory from name"""
        if not self.files:
            return
        if self.current_theory:
            self.set_no_limits(self.current_theory)  # remove the xy-range limits
        self.theory_actions_disabled(False)  # enable theory buttons
        newth = self.do_new(th_name, calculate)

        # add new theory tab
        if th_tab_id == "":
            th_tab_id = newth.name
            th_tab_id = "".join(
                c for c in th_tab_id if c.isupper()
            )  # get the upper case letters of th_name
            th_tab_id = "%s%d" % (th_tab_id, self.num_theories)  # append number

        # hide all theory curves
        ntab = self.TheorytabWidget.count()
        for i in range(ntab):
            th_to_hide = self.TheorytabWidget.widget(i)
            th_to_hide.do_hide()
        # add theory tab
        self.TheorytabWidget.blockSignals(
            True
        )  # avoid trigger handle_thCurrentChanged()
        index = self.TheorytabWidget.addTab(newth, th_tab_id)
        self.TheorytabWidget.setCurrentIndex(index)  # set new theory tab as curent tab
        self.TheorytabWidget.setTabToolTip(index, th_name)  # set new-tab tool tip
        self.TheorytabWidget.blockSignals(False)
        if show:
            newth.update_parameter_table()
            newth.do_show("")
        return newth
