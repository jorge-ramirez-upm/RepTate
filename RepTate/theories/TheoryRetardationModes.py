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
"""Module TheoryRetardationModes

Module that defines theories related to Retardation modes, in the frequency and time domains.

"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from DataTable import DataTable
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from PyQt5.QtWidgets import QWidget, QToolBar, QComboBox, QSpinBox, QAction, QStyle
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from DraggableArtists import DragType, DraggableModesSeries


class TheoryRetardationModesTime(CmdBase):
    """Fit a discrete Retardation spectrum to time dependent creep data
    
    * **Function**
        .. math::
            \\gamma(t) = \\sigma_0 \\left( J_0 + \\sum_{1}^{n_{modes}} J_i \\left[ 1 - \\exp\\left(\\frac{-t}{\\tau_i}\\right) \\right] + \\frac{t}{\\eta_0} \\right)
    
        where:
          - :math:`\\sigma_0`: constant stress applied during the creep experiment.
    
    * **Parameters**
       - :math:`J_0`: Instantaneous compliance (``logJini``, in logarithmic scale).
       - :math:`\\eta_0`: Terminal viscosity (``logeta0``, in logarithmic scale).
       - :math:`n_{modes}`: number of Retardation modes equally distributed in logarithmic scale between :math:`t_{min}` and :math:`t_{max}`.
       - logtmin = :math:`\\log(t_{min})`: decimal logarithm of the minimum time range for the modes.
       - logtmax = :math:`\\log(t_{max})`: decimal logarithm of the maximum time.
       - logJi = :math:`\\log(J_{i})`: decimal logarithm of the compliance of Retardation mode :math:`i`.
    
    """
    thname = "Retardation Modes"
    description = "Fit Retardation modes to time dependent creep data"
    citations = []
    doi = []

    def __new__(cls, name="", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUITheoryRetardationModesTime(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryRetardationModesTime(
                name, parent_dataset, ax)


class BaseTheoryRetardationModesTime:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/Creep/Theory/theory.html#retardation-modes'
    single_file = True
    thname = TheoryRetardationModesTime.thname
    citations = TheoryRetardationModesTime.citations
    doi = TheoryRetardationModesTime.doi

    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.RetardationModesTime
        self.has_modes = True
        self.MAX_MODES = 40
        self.view_modes = True
        tmin = self.parent_dataset.minpositivecol(0)
        tmax = self.parent_dataset.maxcol(0)
        nmodes = int(np.round(np.log10(tmax / tmin)))

        self.parameters["logJini"] = Parameter(
            "logJini",
            -4.0,
            "Log of Instantaneous Compliance",
            ParameterType.real,
            opt_type=OptType.opt)
        self.parameters["logeta0"] = Parameter(
            "logeta0",
            0.0,
            "Log of Terminal Viscosity",
            ParameterType.real,
            opt_type=OptType.opt)
        self.parameters["logtmin"] = Parameter(
            "logtmin",
            np.log10(tmin),
            "Log of time range minimum",
            ParameterType.real,
            opt_type=OptType.opt)
        self.parameters["logtmax"] = Parameter(
            "logtmax",
            np.log10(tmax),
            "Log of time range maximum",
            ParameterType.real,
            opt_type=OptType.opt)
        self.parameters["nmodes"] = Parameter(
            name="nmodes",
            value=nmodes,
            description="Number of Retardation modes",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False)
        # Interpolate modes from data
        try:
            sigma = float(self.parent_dataset.files[0].file_parameters["stress"])
        except (ValueError, KeyError):
            self.Qprint("Invalid stress value")
            return
        tau = np.logspace(np.log10(tmin), np.log10(tmax), nmodes)
        J = np.abs(
            np.interp(tau, self.parent_dataset.files[0].data_table.data[:, 0],
                      self.parent_dataset.files[0].data_table.data[:, 1]))/sigma
        for i in range(self.parameters["nmodes"].value):
            self.parameters["logJ%02d" % i] = Parameter(
                "logJ%02d" % i,
                np.log10(J[i]),
                "Log of Mode %d amplitude" % i,
                ParameterType.real,
                opt_type=OptType.opt)

        # GRAPHIC MODES
        self.graphicmodes = None
        self.artistmodes = None
        self.setup_graphic_modes()

    def drag_mode(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        nmodes = self.parameters["nmodes"].value
        self.set_param_value("logtmin", dx[0])
        self.set_param_value("logtmax", dx[nmodes - 1])
        for i in range(nmodes):
            self.set_param_value("logJ%02d" % i, dy[i])
        self.do_calculate("")
        self.update_parameter_table()

    def update_modes(self):
        """[summary]
        
        [description]
        """
        pass

    def setup_graphic_modes(self):
        """[summary]
        
        [description]
        """
        nmodes = self.parameters["nmodes"].value
        tau = np.logspace(self.parameters["logtmin"].value,
                          self.parameters["logtmax"].value, nmodes)
        J = np.zeros(nmodes)
        for i in range(nmodes):
            J[i] = np.power(10, self.parameters["logJ%02d" % i].value)

        self.graphicmodes = self.ax.plot(tau, J)[0]
        self.graphicmodes.set_marker('D')
        self.graphicmodes.set_linestyle('')
        self.graphicmodes.set_visible(self.view_modes)
        self.graphicmodes.set_markerfacecolor('yellow')
        self.graphicmodes.set_markeredgecolor('black')
        self.graphicmodes.set_markeredgewidth(3)
        self.graphicmodes.set_markersize(8)
        self.graphicmodes.set_alpha(0.5)
        self.artistmodes = DraggableModesSeries(
            self.graphicmodes, DragType.special,
            self.parent_dataset.parent_application,
            self.drag_mode)
        self.plot_theory_stuff()

    def destructor(self):
        """Called when the theory tab is closed"""
        self.graphicmodes_visible(False)
        self.ax.lines.remove(self.graphicmodes)

    def show_theory_extras(self, show=False):
        """Called when the active theory is changed
        
        [description]
        """
        if CmdBase.mode == CmdMode.GUI:
            self.Qhide_theory_extras(show)
        self.graphicmodes_visible(show)

    def graphicmodes_visible(self, state):
        """[summary]
        
        [description]
        """
        self.view_modes = state
        self.graphicmodes.set_visible(self.view_modes)
        if self.view_modes:
            self.artistmodes.connect()
        else:
            self.artistmodes.disconnect()
        # self.do_calculate("")
        self.parent_dataset.parent_application.update_plot()

    def get_modes(self):
        """Get the values of Maxwell Modes from this theory"""
        nmodes = self.parameters["nmodes"].value
        tau = np.logspace(self.parameters["logtmin"].value,
                          self.parameters["logtmax"].value, nmodes)
        J = np.zeros(nmodes)
        for i in range(nmodes):
            J[i] = 1.0/np.power(10, self.parameters["logJ%02d" % i].value)
        return tau, J, True

    def RetardationModesTime(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        try:
            stress = float(f.file_parameters["stress"])
        except (ValueError, KeyError):
            self.Qprint("Invalid stress value")
            return
        nmodes = self.parameters["nmodes"].value
        J0 = np.power(10,self.parameters["logJini"].value)
        eta0 = np.power(10,self.parameters["logeta0"].value)
        tau = np.logspace(self.parameters["logtmin"].value,
                          self.parameters["logtmax"].value, nmodes)

        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            expT_tau = (1.0-np.exp(-tt.data[:, 0] / tau[i]))
            J = np.power(10, self.parameters["logJ%02d" % i].value)
            tt.data[:, 1] += stress * J * expT_tau
        tt.data[:, 1] += stress*(J0 + tt.data[:, 0]/eta0)

    def plot_theory_stuff(self):
        """[summary]
        
        [description]
        """
        if not self.view_modes:
            return
        data_table_tmp = DataTable(self.axarr)
        data_table_tmp.num_columns = 2
        nmodes = self.parameters["nmodes"].value
        data_table_tmp.num_rows = nmodes
        data_table_tmp.data = np.zeros((nmodes, 2))
        tau = np.logspace(self.parameters["logtmin"].value,
                          self.parameters["logtmax"].value, nmodes)
        data_table_tmp.data[:, 0] = tau
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            data_table_tmp.data[i, 1] = np.power(
                10, self.parameters["logJ%02d" % i].value)
        view = self.parent_dataset.parent_application.current_view
        try:
            x, y, success = view.view_proc(data_table_tmp, None)
        except TypeError as e:
            print(e)
            return
        self.graphicmodes.set_data(x, y)
        for i in range(data_table_tmp.MAX_NUM_SERIES):
            for nx in range(len(self.axarr)):
                self.axarr[nx].lines.remove(data_table_tmp.series[nx][i])


class CLTheoryRetardationModesTime(BaseTheoryRetardationModesTime, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)


class GUITheoryRetardationModesTime(BaseTheoryRetardationModesTime, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, self.MAX_MODES)  # min and max number of modes
        self.spinbox.setSuffix(" modes")
        self.spinbox.setValue(self.parameters["nmodes"].value)  #initial value
        tb.addWidget(self.spinbox)
        self.modesaction = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-visible.png'), 'View modes')
        self.modesaction.setCheckable(True)
        self.modesaction.setChecked(True)
        self.thToolsLayout.insertWidget(0, tb)

        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged)
        connection_id = self.modesaction.triggered.connect(
            self.modesaction_change)

    def Qhide_theory_extras(self, state):
        """Uncheck the modeaction button. Called when curent theory is changed
        
        [description]
        """
        self.modesaction.setChecked(state)

    def modesaction_change(self, checked):
        """[summary]
        
        [description]
        """
        self.graphicmodes_visible(checked)
        # self.view_modes = self.modesaction.isChecked()
        # self.graphicmodes.set_visible(self.view_modes)
        # if self.view_modes:
        #     self.artistmodes.connect()
        # else:
        #     self.artistmodes.disconnect()
        # self.do_calculate("")

    def handle_spinboxValueChanged(self, value):
        """Handle a change of the parameter 'nmode'
        
        Arguments:
            - value {[type]} -- [description]
        """
        nmodesold = self.parameters["nmodes"].value
        tminold = self.parameters["logtmin"].value
        tmaxold = self.parameters["logtmax"].value
        tauold = np.logspace(tminold, tmaxold, nmodesold)
        Gold = np.zeros(nmodesold)
        for i in range(nmodesold):
            Gold[i] = self.parameters["logJ%02d" % i].value
            del self.parameters["logJ%02d" % i]

        nmodesnew = value
        self.set_param_value("nmodes", nmodesnew)
        taunew = np.logspace(tminold, tmaxold, nmodesnew)

        Gnew = np.interp(taunew, tauold, Gold)

        for i in range(nmodesnew):
            self.parameters["logJ%02d" % i] = Parameter(
                "logJ%02d" % i,
                Gnew[i],
                "Log of Mode %d compliance" % i,
                ParameterType.real,
                opt_type=OptType.opt)

        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()
        self.update_parameter_table()
