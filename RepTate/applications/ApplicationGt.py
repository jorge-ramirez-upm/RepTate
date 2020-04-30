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
"""Module ApplicationGt

Module for the analysis of stress relaxation data from simulations and experiments.

"""
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Application import Application
from RepTate.gui.QApplicationWindow import QApplicationWindow
from RepTate.core.View import View
from RepTate.core.FileType import TXTColumnFile
import numpy as np
from scipy import interpolate

from PyQt5.QtWidgets import QSpinBox, QPushButton, QHBoxLayout, QLineEdit, QLabel, QSizePolicy
from PyQt5.QtGui import QDoubleValidator
import RepTate.theories.schwarzl_ctypes_helper as sch
from math import log10, sin, cos

class ApplicationGt(CmdBase):
    """Application to Analyze Stress Relaxation Data

    """
    appname = "Gt"
    description = "Relaxation modulus"
    extension = "gt"

    def __new__(cls, name="Gt", parent=None):
        """[summary]

        [description]

        Keyword Arguments:
            - name {[type]} -- [description] (default: {"Gt"})
            - parent {[type]} -- [description] (default: {None})

        Returns:
            - [type] -- [description]
        """
        return GUIApplicationGt(
            name,
            parent) if (CmdBase.mode == CmdMode.GUI) else CLApplicationGt(
                name, parent)


class BaseApplicationGt:
    """[summary]

    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/Gt/Gt.html'
    appname = ApplicationGt.appname

    def __init__(self, name="Gt", parent=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {"Gt"})
            - parent {[type]} -- [description] (default: {None})
        """
        from TheoryMaxwellModes import TheoryMaxwellModesTime
        from TheoryRouse import TheoryRouseTime
        from TheoryDTDStars import TheoryDTDStarsTime
        from TheoryShanbhagMaxwellModes import TheoryShanbhagMaxwellModesTime

        super().__init__(name, parent)

        # time range for view conversion to frequency domain
        self.tmin_view = -np.inf
        self.tmax_view = np.inf

        # VIEWS
        self.views["log(G(t))"] = View(
            name="log(G(t))",
            description="log Relaxation modulus",
            x_label="log(t)",
            y_label="log(G)",
            x_units="s",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogGt,
            n=1,
            snames=["log(G)"])
        self.views["i-Rheo G',G''"] = View(
            name="i-Rheo G',G''",
            description="G', G'' from i-Rheo transformation of G(t)",
            x_label="$\omega$",
            y_label="G',G''",
            x_units="rad/s",
            y_units="Pa",
            log_x=True,
            log_y=True,
            view_proc=self.viewiRheo,
            n=2,
            snames=["G'","G''"])
        self.views["i-Rheo-Over G',G''"] = View(
            name="i-Rheo-Over G',G''",
            description=
            "G', G'' from i-Rheo transformation of G(t) with Oversampling",
            x_label="$\omega$",
            y_label="G',G''",
            x_units="rad/s",
            y_units="Pa",
            log_x=True,
            log_y=True,
            view_proc=self.viewiRheoOver,
            n=2,
            snames=["G'","G''"])
        self.views["Schwarzl G',G''"] = View(
            name="Schwarzl G',G''",
            description="G', G'' from Schwarzl transformation of G(t)",
            x_label="$\omega$",
            y_label="G',G''",
            x_units="rad/s",
            y_units="Pa",
            log_x=True,
            log_y=True,
            view_proc=self.viewSchwarzl_Gt,
            n=2,
            snames=["G'","G''"])
        self.views["G(t)"] = View(
            name="G(t)",
            description="Relaxation modulus",
            x_label="t",
            y_label="G",
            x_units="s",
            y_units="Pa",
            log_x=True,
            log_y=True,
            view_proc=self.viewGt,
            n=1,
            snames=["G"])
        self.OVER = 100  # initial oversampling
        self.MIN_OVER = 1  # min oversampling
        self.MAX_OVER = 10000  # max oversampling

        #set multiviews
        self.multiviews = [
            self.views["log(G(t))"], self.views["i-Rheo G',G''"]
        ]  #default view order in multiplot views, set only one item for single view
        self.nplots = len(self.multiviews)

        #set multiviews
        self.nplots = 2
        self.multiviews = []
        for i in range(self.nplot_max):
            # set views in the same order as declared above
            self.multiviews.append(list(self.views.values())[i])
        self.multiplots.reorg_fig(self.nplots)

        # FILES
        ftype = TXTColumnFile("G(t) files", "gt", "Relaxation modulus",
                              ['t', 'Gt'], ['Mw', 'gamma'], ['s', 'Pa'])
        self.filetypes[ftype.extension] = ftype

        # THEORIES
        self.theories[TheoryMaxwellModesTime.thname] = TheoryMaxwellModesTime
        self.theories[TheoryRouseTime.thname] = TheoryRouseTime
        self.theories[TheoryDTDStarsTime.thname] = TheoryDTDStarsTime
        self.theories[TheoryShanbhagMaxwellModesTime.thname] = TheoryShanbhagMaxwellModesTime

        self.add_common_theories()

        #set the current view
        self.set_views()

    def viewGt(self, dt, file_parameters):
        """Relaxation modulus :math:`G(t)` vs time :math:`t` (both in logarithmic scale)
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        try:
            gamma = float(file_parameters["gamma"])
            if (gamma==0):
                gamma=1
        except:
            gamma = 1
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]/gamma
        return x, y, True

    def viewLogGt(self, dt, file_parameters):
        """Logarithm of the relaxation modulus :math:`G(t)` vs logarithm of time :math:`t`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        try:
            gamma = float(file_parameters["gamma"])
            if (gamma==0):
                gamma=1
        except:
            gamma = 1
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 1]/gamma)
        return x, y, True

    def viewSchwarzl_Gt(self, dt, file_parameters):
        """Schwarzl transformation: numerical calculation of the storage modulus :math:`G'(\\omega)` and loss modulus
        :math:`G''(\\omega)` from the relaxation modulus :math:`G(t)`
        """
        data_x, data_y = self.get_xy_data_in_xrange(dt)
        n = len(data_x)
        try:
            gamma = float(file_parameters["gamma"])
            if (gamma==0):
                gamma=1
        except:
            gamma = 1
        data_y /= gamma
        x = np.zeros((n, 2))
        y = np.zeros((n, 2))

        wp, Gp, wpp, Gpp = sch.do_schwarzl_gt(
            n, data_y, data_x)  #call the C function

        x[:, 0] = wp[:]
        x[:, 1] = wpp[:]
        y[:, 0] = Gp[:]
        y[:, 1] = Gpp[:]
        return x, y, True

    def viewiRheo(self, dt, file_parameters):
        """i-Rheo Fourier transformation of the relaxation modulus :math:`G(t)` to obtain the storage modulus :math:`G'(\\omega)` and loss modulus :math:`G''(\\omega)` (no oversamplig).
        """
        data_x, data_y = self.get_xy_data_in_xrange(dt)
        xunique, indunique = np.unique(data_x, return_index=True)
        n = len(xunique)
        yunique=data_y[indunique]
        data_x = xunique
        data_y = yunique
        try:
            gamma = float(file_parameters["gamma"])
            if (gamma==0):
                gamma=1
        except:
            gamma = 1
        data_y /= gamma
        x = np.zeros((n, 2))
        y = np.zeros((n, 2))

        if len(data_x)<2:
            f = interpolate.interp1d(
                data_x,
                data_y,
                kind='zero',
                assume_sorted=True,
                fill_value='extrapolate')
        elif len(data_x)<3:
            f = interpolate.interp1d(
                data_x,
                data_y,
                kind='linear',
                assume_sorted=True,
                fill_value='extrapolate')
        elif len(data_x)<4:
            f = interpolate.interp1d(
                data_x,
                data_y,
                kind='quadratic',
                assume_sorted=True,
                fill_value='extrapolate')
        else:
            f = interpolate.interp1d(
                data_x,
                data_y,
                kind='cubic',
                assume_sorted=True,
                fill_value='extrapolate')
        g0 = f(0)
        ind1 = np.argmax(data_x > 0)
        t1 = data_x[ind1]
        g1 = data_y[ind1]
        tinf = np.max(data_x)
        if tinf<=0 or t1<=0:
            return x, y, False
        wp = np.logspace(log10(1 / tinf), log10(1 / t1), n)
        x[:, 0] = wp[:]
        x[:, 1] = wp[:]

        coeff = (data_y[ind1 + 1:] - data_y[ind1:-1]) / (
            data_x[ind1 + 1:] - data_x[ind1:-1])
        for i, w in enumerate(wp):

            y[i, 0] = g0 + sin(w * t1) * (g1 - g0) / w / t1 + np.dot(
                coeff, -np.sin(w * data_x[ind1:-1]) +
                np.sin(w * data_x[ind1 + 1:])) / w

            y[i, 1] = -(1 - cos(w * t1)) * (g1 - g0) / w / t1 - np.dot(
                coeff,
                np.cos(w * data_x[ind1:-1]) -
                np.cos(w * data_x[ind1 + 1:])) / w

        return x, y, True

    def viewiRheoOver(self, dt, file_parameters):
        """i-Rheo Fourier transformation of the relaxation modulus :math:`G(t)` to obtain the storage modulus :math:`G'(\\omega)` and loss modulus :math:`G''(\\omega)` (with user selected oversamplig).
        """
        data_x, data_y = self.get_xy_data_in_xrange(dt)
        xunique, indunique = np.unique(data_x, return_index=True)
        n = len(xunique)
        yunique=data_y[indunique]
        data_x = xunique
        data_y = yunique
        try:
            gamma = float(file_parameters["gamma"])
            if (gamma==0):
                gamma=1
        except:
            gamma = 1
        data_y /= gamma
        x = np.zeros((n, 2))
        y = np.zeros((n, 2))

        f = interpolate.interp1d(
            data_x,
            data_y,
            kind='cubic',
            assume_sorted=True,
            fill_value='extrapolate')
        g0 = f(0)
        ind1 = np.argmax(data_x > 0)
        t1 = data_x[ind1]
        g1 = data_y[ind1]
        tinf = np.max(data_x)
        wp = np.logspace(np.log10(1 / tinf), np.log10(1 / t1), n)
        x[:, 0] = wp[:]
        x[:, 1] = wp[:]

        # Create oversampled data
        xdata = np.zeros(1)
        xdata[0] = data_x[ind1]
        for i in range(ind1 + 1, n):
            tmp = np.logspace(
                log10(data_x[i - 1]), log10(data_x[i]),
                self.OVER + 1)
            xdata = np.append(xdata, tmp[1:])
        ydata = f(xdata)

        coeff = (ydata[1:] - ydata[:-1]) / (xdata[1:] - xdata[:-1])
        for i, w in enumerate(wp):
            y[i, 0] = g0 + sin(w * t1) * (g1 - g0) / w / t1 + np.dot(
                coeff, -np.sin(w * xdata[:-1]) + np.sin(w * xdata[1:])) / w

            y[i, 1] = -(1 - cos(w * t1)) * (g1 - g0) / w / t1 - np.dot(
                coeff,
                np.cos(w * xdata[:-1]) - np.cos(w * xdata[1:])) / w
        return x, y, True

    def get_xy_data_in_xrange(self, dt):
        """Return the x and y data that with t in [self.tmin_view, self.tmax_view]"""
        #get indices of data in xrange
        args = np.where(np.logical_and(dt.data[:, 0] >= self.tmin_view, dt.data[:, 0] <= self.tmax_view))
        x_in_range = dt.data[:, 0][args]
        y_in_range = dt.data[:, 1][args]
        return x_in_range, y_in_range

class CLApplicationGt(BaseApplicationGt, Application):
    """[summary]

    [description]
    """

    def __init__(self, name="Gt", parent=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {"Gt"})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)

    def show_sb_oversampling(self):
        pass

    def hide_sb_oversampling(self):
        pass


class GUIApplicationGt(BaseApplicationGt, QApplicationWindow):
    """[summary]

    [description]
    """

    def __init__(self, name="Gt", parent=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {"Gt"})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)

        self.add_oversampling_widget()
        self.set_oversampling_widget_visible(False)

        self.add_xrange_widget_view()
        self.set_xrange_widgets_view_visible(False)

    def add_oversampling_widget(self):
        """Add spinbox for the oversampling ratio"""
        self.sb_oversampling = QSpinBox()
        self.sb_oversampling.setRange(self.MIN_OVER, self.MAX_OVER)
        self.sb_oversampling.setValue(self.OVER)
        self.sb_oversampling.valueChanged.connect(self.change_oversampling)

        self.viewLayout.insertWidget(2, self.sb_oversampling)

    def add_xrange_widget_view(self):
        """Add widgets below the view combobox to select the
        x-range applied to view transformation"""
        hlayout = QHBoxLayout()

        hlayout.addStretch()
        #xmin
        self.xmin_view = QLineEdit("-inf")
        self.xmin_view.textChanged.connect(self.change_xmin)
        self.xmin_view.setValidator(QDoubleValidator())
        self.xmin_view.setMaximumWidth(35)
        self.xmin_view.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.xmin_label = QLabel("<b>log(t<sub>min</sub>)</b>")
        hlayout.addWidget(self.xmin_label)
        hlayout.addWidget(self.xmin_view)
        #space
        hlayout.addSpacing(5)
        #xmax
        self.xmax_view = QLineEdit("inf")
        self.xmax_view.textChanged.connect(self.change_xmax)
        self.xmax_view.setValidator(QDoubleValidator())
        self.xmax_view.setMaximumWidth(35)
        self.xmax_view.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.xmax_label = QLabel(" <b>log(t<sub>max</sub>)</b>")
        hlayout.addWidget(self.xmax_label)
        hlayout.addWidget(self.xmax_view)
        #push button to refresh view
        self.pb = QPushButton("GO")
        self.pb.setMaximumWidth(25)
        self.pb.clicked.connect(self.update_all_ds_plots)
        hlayout.addWidget(self.pb)
        self.hlayout_view = hlayout
        self.ViewDataTheoryLayout.insertLayout(1, self.hlayout_view)

    def change_xmin(self, text):
        """Update the value of t_min"""
        if text in "-np.inf -inf":
            self.tmin_view = -np.inf
        else:
            try:
                self.tmin_view = 10**float(text)
            except:
                pass

    def change_xmax(self, text):
        """Update the value of t_max"""
        if text in "np.inf inf":
            self.tmax_view = np.inf
        else:
            try:
                self.tmax_view = 10**float(text)
            except:
                pass

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
        self.xmax_label.setVisible(state)
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
