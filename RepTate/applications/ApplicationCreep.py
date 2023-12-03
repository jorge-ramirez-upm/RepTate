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
"""Module ApplicationCreep

Module for the analysis of data from Creep experiments

"""
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Application import Application
from RepTate.gui.QApplicationWindow import QApplicationWindow
from RepTate.core.View import View
from RepTate.core.FileType import TXTColumnFile
import numpy as np
from scipy import interpolate

from PySide6.QtWidgets import (
    QSpinBox,
    QPushButton,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QSizePolicy,
    QMessageBox,
)
from PySide6.QtGui import QDoubleValidator
from math import log10


class ApplicationCreep(CmdBase):
    """Application to Analyze Data from Creep experiments"""

    appname = "Creep"
    description = "Creep Experiments"
    extension = "creep"

    def __new__(cls, name="Creep", parent=None):
        """Create an instance of the GUI or CL class"""
        return (
            GUIApplicationCreep(name, parent)
            if (CmdBase.mode == CmdMode.GUI)
            else CLApplicationCreep(name, parent)
        )


class BaseApplicationCreep:
    """Base Class for both GUI and CL"""

    html_help_file = (
        "http://reptate.readthedocs.io/manual/Applications/Creep/Creep.html"
    )
    appname = ApplicationCreep.appname

    def __init__(self, name="Creep", parent=None):
        """**Constructor**"""
        from RepTate.theories.TheoryRetardationModes import TheoryRetardationModesTime

        super().__init__(name, parent)

        # time range for view conversion to frequency domain
        self.eta = 10000
        self.tmin_view = -np.inf
        self.tmax_view = np.inf

        # VIEWS
        self.views["log(gamma(t))"] = View(
            name="log(gamma(t))",
            description="log strain",
            x_label="log(t)",
            y_label="log($\gamma$)",
            x_units="s",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogStraint,
            n=1,
            snames=["log(gamma)"],
        )
        self.views["gamma(t)"] = View(
            name="gamma(t)",
            description="strain",
            x_label="t",
            y_label="$\gamma$",
            x_units="s",
            y_units="-",
            log_x=True,
            log_y=True,
            view_proc=self.viewStraint,
            n=1,
            snames=["gamma"],
        )
        self.views["log(J(t))"] = View(
            name="log(J(t))",
            description="creep compliance",
            x_label="log(t)",
            y_label="log(J)",
            x_units="s",
            y_units="$\mathrm{Pa}^{-1}$",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogJt,
            n=1,
            snames=["log(J)"],
        )
        self.views["J(t)"] = View(
            name="J(t)",
            description="creep compliance",
            x_label="t",
            y_label="J",
            x_units="s",
            y_units="$\mathrm{Pa}^{-1}$",
            log_x=True,
            log_y=True,
            view_proc=self.viewJt,
            n=1,
            snames=["J"],
        )
        self.views["t/J(t)"] = View(
            name="t/J(t)",
            description="t/creep compliance",
            x_label="t",
            y_label="t/J",
            x_units="s",
            y_units="Pa.s",
            log_x=True,
            log_y=True,
            view_proc=self.viewt_Jt,
            n=1,
            snames=["t/J"],
        )
        self.views["i-Rheo G',G''"] = View(
            name="i-Rheo G',G''",
            description="G', G'' from i-Rheo transformation of J(t)",
            x_label="$\omega$",
            y_label="G',G''",
            x_units="rad/s",
            y_units="Pa",
            log_x=True,
            log_y=True,
            view_proc=self.viewiRheo,
            n=2,
            snames=["G'", "G''"],
        )
        self.views["i-Rheo-Over G',G''"] = View(
            name="i-Rheo-Over G',G''",
            description="G', G'' from i-Rheo transformation of J(t) with Oversampling",
            x_label="$\omega$",
            y_label="G',G''",
            x_units="rad/s",
            y_units="Pa",
            log_x=True,
            log_y=True,
            view_proc=self.viewiRheoOver,
            n=2,
            snames=["G'", "G''"],
        )
        self.OVER = 100  # initial oversampling
        self.MIN_OVER = 1  # min oversampling
        self.MAX_OVER = 10000  # max oversampling

        # set multiviews
        self.nplots = 1
        self.multiviews = []
        for i in range(self.nplot_max):
            # set views in the same order as declared above
            self.multiviews.append(list(self.views.values())[i])
        self.multiplots.reorg_fig(self.nplots)

        # FILES
        ftype = TXTColumnFile(
            "Creep files",
            "creep",
            "Creep files",
            ["t", "strain"],
            ["stress", "Mw", "T"],
            ["s", "-", "Pa", "C"],
        )
        self.filetypes[ftype.extension] = ftype

        # THEORIES
        self.theories[TheoryRetardationModesTime.thname] = TheoryRetardationModesTime
        self.add_common_theories()

        # set the current view
        self.set_views()

    def viewLogStraint(self, dt, file_parameters):
        """Logarithm of the applied strain :math:`\\gamma(t)` vs logarithm of time :math:`t`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(np.abs(dt.data[:, 1]))
        return x, y, True

    def viewStraint(self, dt, file_parameters):
        """Applied strain :math:`\\gamma(t)` vs time :math:`t` (both axes in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True

    def viewLogJt(self, dt, file_parameters):
        """Logarithm of the compliance :math:`J(t)=\\gamma(t)/\\sigma_0` (where :math:`\\sigma_0` is the applied stress in the creep experiment) vs logarithm of time :math:`t`"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        sigma = float(file_parameters["stress"])
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(np.abs(dt.data[:, 1]) / sigma)
        return x, y, True

    def viewJt(self, dt, file_parameters):
        """Compliance :math:`J(t)=\\gamma(t)/\\sigma_0` (where :math:`\\sigma_0` is the applied stress in the creep experiment) vs time :math:`t` (both axes in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        sigma = float(file_parameters["stress"])
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1] / sigma
        return x, y, True

    def viewt_Jt(self, dt, file_parameters):
        """Time divided by compliance :math:`t/J(t)` vs time :math:`t` (both axes in logarithmic scale)"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        sigma = float(file_parameters["stress"])
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 0] / dt.data[:, 1] * sigma
        return x, y, True

    def viewiRheo(self, dt, file_parameters):
        """i-Rheo Fourier transformation of the compliance :math:`J(t)` to obtain the storage modulus :math:`G'(\\omega)` and loss modulus :math:`G''(\\omega)` (no oversamplig)."""
        error_msg, data_x, data_y = self.get_xy_data_in_xrange(dt)
        if error_msg is not None:
            QMessageBox.warning(self, 'Error', error_msg)
            return np.zeros((dt.num_rows, 2)), np.zeros((dt.num_rows, 2)), False
        xunique, indunique = np.unique(data_x, return_index=True)
        n = len(xunique)
        sigma = float(file_parameters["stress"])
        yunique = data_y[indunique] / sigma
        t = xunique
        j = yunique
        x = np.zeros((n, 2))
        y = np.zeros((n, 2))

        f = interpolate.interp1d(
            t, j, kind="cubic", assume_sorted=True, fill_value="extrapolate"
        )
        j0 = f([0])[0]
        ind1 = np.argmax(t > 0)
        t1 = t[ind1]
        j1 = j[ind1]
        tN = np.max(t)
        w = np.logspace(log10(1 / tN), log10(1 / t1), n)
        x[:, 0] = w[:]
        x[:, 1] = w[:]

        aux = (
            1j * w * j0
            + (1 - np.exp(-1j * w * t1)) * (j1 - j0) / t1
            + np.exp(-1j * w * tN) / self.eta
        )
        for i in range(ind1 + 1, n):
            aux += (
                (np.exp(-1j * w * t[i - 1]) - np.exp(-1j * w * t[i]))
                * (j[i] - j[i - 1])
                / (t[i] - t[i - 1])
            )
        Gstar = 1j * w / aux

        y[:, 0] = Gstar.real
        y[:, 1] = Gstar.imag

        return x, y, True

    def viewiRheoOver(self, dt, file_parameters):
        """i-Rheo Fourier transformation of the compliance :math:`J(t)` to obtain the storage modulus :math:`G'(\\omega)` and loss modulus :math:`G''(\\omega)` (with user selected oversamplig)."""
        error_msg, data_x, data_y = self.get_xy_data_in_xrange(dt)
        if error_msg is not None:
            QMessageBox.warning(self, 'Error', error_msg)
            return np.zeros((dt.num_rows, 2)), np.zeros((dt.num_rows, 2)), False
        xunique, indunique = np.unique(data_x, return_index=True)
        n = len(xunique)
        sigma = float(file_parameters["stress"])
        yunique = data_y[indunique] / sigma
        t = xunique
        j = yunique
        x = np.zeros((n, 2))
        y = np.zeros((n, 2))

        f = interpolate.interp1d(
            t, j, kind="cubic", assume_sorted=True, fill_value="extrapolate"
        )
        j0 = f([0])[0]
        ind1 = np.argmax(t > 0)
        t1 = t[ind1]
        j1 = j[ind1]
        tN = np.max(t)
        w = np.logspace(np.log10(1 / tN), np.log10(1 / t1), n)
        x[:, 0] = w[:]
        x[:, 1] = w[:]

        # Create oversampled data
        tover = np.zeros(1)
        tover[0] = t[ind1]
        for i in range(ind1 + 1, n):
            tmp = np.logspace(log10(t[i - 1]), log10(t[i]), self.OVER + 1)
            tover = np.append(tover, tmp[1:])
        jover = f(tover)
        nover = len(tover)

        aux = (
            1j * w * j0
            + (1 - np.exp(-1j * w * t1)) * (j1 - j0) / t1
            + np.exp(-1j * w * tN) / self.eta
        )
        for i in range(1, nover):
            aux += (
                (np.exp(-1j * w * tover[i - 1]) - np.exp(-1j * w * tover[i]))
                * (jover[i] - jover[i - 1])
                / (tover[i] - tover[i - 1])
            )
        Gstar = 1j * w / aux

        y[:, 0] = Gstar.real
        y[:, 1] = Gstar.imag

        return x, y, True

    def get_xy_data_in_xrange(self, dt):
        """Return the x and y data that with t in [self.tmin_view, self.tmax_view]"""
        success = self.set_xmin()
        success *= self.set_xmax()
        success *= self.set_eta()
        if success:
            # get indices of data in xrange
            filtered = np.logical_and(dt.data[:, 0] >= self.tmin_view, dt.data[:, 0] <= self.tmax_view)
            non_zeros = np.count_nonzero(filtered)
            if non_zeros < 1:
                # too few data between tmin and tmax
                return "Too few data points (%d) between t_min and t_max" % non_zeros, None, None
            args = np.where(filtered)
            x_in_range = dt.data[:, 0][args]
            y_in_range = dt.data[:, 1][args]
            return None, x_in_range, y_in_range
        else:
            return "Check values of eta, t_min and t_max ", None, None



class CLApplicationCreep(BaseApplicationCreep, Application):
    """CL Version"""

    def __init__(self, name="Creep", parent=None):
        """**Constructor**"""
        super().__init__(name, parent)

    def show_sb_oversampling(self):
        pass

    def hide_sb_oversampling(self):
        pass


class GUIApplicationCreep(BaseApplicationCreep, QApplicationWindow):
    """GUI Version"""

    def __init__(self, name="Creep", parent=None):
        """**Constructor**"""
        super().__init__(name, parent)

        self.add_oversampling_widget()
        self.set_oversampling_widget_visible(False)

        self.add_xrange_widget_view()
        self.set_xrange_widgets_view_visible(False)

    def add_oversampling_widget(self):
        """Add spinbox for the oversampling ratio"""
        self.sb_oversampling = QSpinBox()
        self.sb_oversampling.setToolTip("Value of the oversampling ratio")
        self.sb_oversampling.setRange(self.MIN_OVER, self.MAX_OVER)
        self.sb_oversampling.setValue(self.OVER)
        self.sb_oversampling.valueChanged.connect(self.change_oversampling)

        self.viewLayout.insertWidget(2, self.sb_oversampling)

    def add_xrange_widget_view(self):
        """Add widgets below the view combobox to select the
        x-range applied to view transformation"""
        hlayout = QHBoxLayout()

        hlayout.addStretch()
        # eta
        self.eta_view = QLineEdit("4")
        self.eta_view.setToolTip("Value of steady state viscosity")
        self.eta_view.editingFinished.connect(self.set_eta)
        self.eta_view.setMaximumWidth(35)
        self.eta_view.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.eta_label = QLabel("<b>log(eta)</b>")
        hlayout.addWidget(self.eta_label)
        hlayout.addWidget(self.eta_view)
        # space
        hlayout.addSpacing(5)
        # xmin
        self.xmin_view = QLineEdit("-inf")
        self.xmin_view.setToolTip("Discard data points below this value before i-Rheo transformation")
        self.xmin_view.editingFinished.connect(self.set_xmin)
        self.xmin_view.setMaximumWidth(35)
        self.xmin_view.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.xmin_label = QLabel("<b>log(t<sub>min</sub>)</b>")
        hlayout.addWidget(self.xmin_label)
        hlayout.addWidget(self.xmin_view)
        # space
        hlayout.addSpacing(5)
        # xmax
        self.xmax_view = QLineEdit("inf")
        self.xmax_view.setToolTip("Discard data points above this value before i-Rheo transformation")
        self.xmax_view.editingFinished.connect(self.set_xmax)
        self.xmax_view.setMaximumWidth(35)
        self.xmax_view.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.xmax_label = QLabel(" <b>log(t<sub>max</sub>)</b>")
        hlayout.addWidget(self.xmax_label)
        hlayout.addWidget(self.xmax_view)
        # push button to refresh view
        self.pb = QPushButton("GO")
        self.pb.setMaximumWidth(25)
        self.pb.clicked.connect(self.update_all_ds_plots)
        hlayout.addWidget(self.pb)
        self.hlayout_view = hlayout
        self.ViewDataTheoryLayout.insertLayout(1, self.hlayout_view)

    def set_eta(self):
        """Update the value of eta. Return success status"""
        text = self.eta_view.text()
        if text in ["-np.inf", "-inf"]:
            self.eta = -np.inf
        else:
            try:
                self.eta = 10 ** float(text)
                self.eta_view.setStyleSheet("QLineEdit { background: white;}")
                return True
            except:
                self.eta_view.setStyleSheet("QLineEdit { background: red;}")
                return False

    def set_xmin(self):
        """Update the value of t_min. Return success status"""
        text = self.xmin_view.text()
        if text in ["np.inf", "inf"]:
            self.tmin_view = -np.inf
        else:
            try:
                self.tmin_view = 10 ** float(text)
                if self.tmin_view >= self.tmax_view:
                    self.xmin_view.setStyleSheet("QLineEdit { background: red;}")
                    return False
                else:
                    self.xmin_view.setStyleSheet("QLineEdit { background: white;}")
            except:
                self.xmin_view.setStyleSheet("QLineEdit { background: red;}")
                return False
        return True

    def set_xmax(self):
        """Update the value of t_max. Return success status"""
        text = self.xmax_view.text()
        if text in ["np.inf", "inf"]:
            self.tmax_view = np.inf
        else:
            try:
                self.tmax_view = 10 ** float(text)
                if self.tmin_view >= self.tmax_view:
                    self.xmax_view.setStyleSheet("QLineEdit { background: red;}")
                    return False
                else:
                    self.xmax_view.setStyleSheet("QLineEdit { background: white;}")
            except:
                self.xmax_view.setStyleSheet("QLineEdit { background: red;}")
                return False
        return True

    def change_oversampling(self, val):
        """Change the value of the oversampling ratio.
        Called when the spinbox value is changed"""
        self.OVER = val

    def set_oversampling_widget_visible(self, state):
        """Show/Hide the extra widget "sampling ratio" """
        self.sb_oversampling.setVisible(state)

    def set_xrange_widgets_view_visible(self, state):
        """Show/Hide the extra widgets for xrange selection"""
        self.pb.setVisible(state)
        self.xmin_label.setVisible(state)
        self.eta_label.setVisible(state)
        self.xmax_label.setVisible(state)
        self.eta_view.setVisible(state)
        self.xmin_view.setVisible(state)
        self.xmax_view.setVisible(state)

    def set_view_tools(self, view_name):
        """Show/Hide extra view widgets depending on the current view"""
        if view_name in ["i-Rheo G',G''", "Schwarzl G',G''"]:
            self.set_xrange_widgets_view_visible(True)
            self.set_oversampling_widget_visible(False)
        elif view_name == "i-Rheo-Over G',G''":
            self.set_xrange_widgets_view_visible(True)
            self.set_oversampling_widget_visible(True)
        else:
            try:
                self.set_xrange_widgets_view_visible(False)
                self.set_oversampling_widget_visible(False)
            except AttributeError:
                pass
