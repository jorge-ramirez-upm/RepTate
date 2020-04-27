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
"""Module TheoryMaxwellModes

Module that defines theories related to Maxwell modes, in the frequency and time domains.

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


class TheoryMaxwellModesFrequency(CmdBase):
    """Fit a generalized Maxwell model to a frequency dependent relaxation function. 
    
    * **Function**
        .. math::
            \\begin{eqnarray}
            G'(\\omega) & = & \\sum_{1}^{n_{modes}} G_i \\frac{(\\omega\\tau_i)^2}{1+(\\omega\\tau_i)^2} \\\\
            G''(\\omega) & = & \\sum_{1}^{n_{modes}} G_i \\frac{\\omega\\tau_i}{1+(\\omega\\tau_i)^2}
            \\end{eqnarray}
    
    * **Parameters**
       - :math:`n_{modes}`: number of Maxwell modes equally distributed in logarithmic scale between :math:`\\omega_{min}` and :math:`\\omega_{max}`.
       - logwmin = :math:`\\log(\\omega_{min})`: decimal logarithm of the minimum frequency.
       - logwmax = :math:`\\log(\\omega_{max})`: decimal logarithm of the maximum frequency.
       - logGi = :math:`\\log(G_{i})`: decimal logarithm of the amplitude of Maxwell mode :math:`i`.
    
    """
    thname = "Maxwell Modes"
    description = "Maxwell modes, frequency dependent"
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
        return GUITheoryMaxwellModesFrequency(name, parent_dataset, ax) if (
            CmdBase.mode == CmdMode.GUI) else CLTheoryMaxwellModesFrequency(
                name, parent_dataset, ax)


class BaseTheoryMaxwellModesFrequency:
    """[summary] 
        
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/LVE/Theory/theory.html#maxwell-modes'
    single_file = True
    thname = TheoryMaxwellModesFrequency.thname
    citations = TheoryMaxwellModesFrequency.citations
    doi = TheoryMaxwellModesFrequency.doi 

    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**
                
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.MaxwellModesFrequency
        self.has_modes = True
        self.MAX_MODES = 40
        self.view_modes = True
        wmin = self.parent_dataset.minpositivecol(0)
        wmax = self.parent_dataset.maxcol(0)
        nmodes = int(np.round(np.log10(wmax / wmin)))

        self.parameters["logwmin"] = Parameter(
            "logwmin",
            np.log10(wmin),
            "Log of frequency range minimum",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=-10,
            max_value=10)
        self.parameters["logwmax"] = Parameter(
            "logwmax",
            np.log10(wmax),
            "Log of frequency range maximum",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=-10,
            max_value=10)
        self.parameters["nmodes"] = Parameter(
            name="nmodes",
            value=nmodes,
            description="Number of Maxwell modes",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False,
            min_value=1)
        # Interpolate modes from data
        w = np.logspace(np.log10(wmin), np.log10(wmax), nmodes)
        G = np.abs(
            np.interp(w, self.parent_dataset.files[0].data_table.data[:, 0],
                      self.parent_dataset.files[0].data_table.data[:, 1]))
        for i in range(self.parameters["nmodes"].value):
            self.parameters["logG%02d" % i] = Parameter(
                "logG%02d" % i,
                np.log10(G[i]),
                "Log of Mode %d amplitude" % i,
                ParameterType.real,
                opt_type=OptType.opt,
                min_value=-10,
                max_value=10)

        # GRAPHIC MODES
        self.graphicmodes = []
        self.artistmodes = []
        self.setup_graphic_modes()

    def set_param_value(self, name, value):
        """Change other parameters when nmodes is changed, else call parent function"""
        if name == 'nmodes':
            nmodesold = self.parameters["nmodes"].value
            wminold = self.parameters["logwmin"].value
            wmaxold = self.parameters["logwmax"].value
            wold = np.logspace(wminold, wmaxold, nmodesold)
            Gold = np.zeros(nmodesold)
            for i in range(nmodesold):
                Gold[i] = self.parameters["logG%02d" % i].value
                del self.parameters["logG%02d" % i]

            nmodesnew = int(value)
            message, success = super().set_param_value("nmodes", nmodesnew)
            wnew = np.logspace(wminold, wmaxold, nmodesnew)

            Gnew = np.interp(wnew, wold, Gold)

            for i in range(nmodesnew):
                self.parameters["logG%02d" % i] = Parameter(
                    "logG%02d" % i,
                    Gnew[i],
                    "Log of Mode %d amplitude" % i,
                    ParameterType.real,
                    opt_type=OptType.opt,
                    min_value=-10,
                    max_value=10)
            if CmdBase.mode == CmdMode.GUI:
                self.spinbox.blockSignals(True)
                self.spinbox.setValue(nmodesnew)
                self.spinbox.blockSignals(False)
        else:
            message, success = super().set_param_value(name, value)
        
        return message, success

    def drag_mode(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        nmodes = self.parameters["nmodes"].value
        if self.parent_dataset.parent_application.current_view.log_x:
            self.set_param_value("logwmin", np.log10(dx[0]))
            self.set_param_value("logwmax", np.log10(dx[nmodes - 1]))
        else:
            self.set_param_value("logwmin", dx[0])
            self.set_param_value("logwmax", dx[nmodes - 1])

        if self.parent_dataset.parent_application.current_view.log_y:
            for i in range(nmodes):
                self.set_param_value("logG%02d" % i, np.log10(dy[i]))
        else:
            for i in range(nmodes):
                self.set_param_value("logG%02d" % i, dy[i])

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
        w = np.logspace(self.parameters["logwmin"].value,
                        self.parameters["logwmax"].value, nmodes)
        G = np.zeros(nmodes)
        for i in range(nmodes):
            G[i] = np.power(10, self.parameters["logG%02d" % i].value)

        self.graphicmodes = self.ax.plot(w, G)[0]
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
            self.parent_dataset.parent_application, self.drag_mode)
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
        freq = np.logspace(self.parameters["logwmin"].value,
                           self.parameters["logwmax"].value, nmodes)
        tau = 1.0 / freq
        G = np.zeros(nmodes)
        for i in range(nmodes):
            G[i] = np.power(10, self.parameters["logG%02d" % i].value)
        return tau, G, True

    def MaxwellModesFrequency(self, f=None):
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

        nmodes = self.parameters["nmodes"].value
        freq = np.logspace(self.parameters["logwmin"].value,
                           self.parameters["logwmax"].value, nmodes)
        tau = 1.0 / freq

        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            wT = tt.data[:, 0] * tau[i]
            wTsq = wT**2
            G = np.power(10, self.parameters["logG%02d" % i].value)
            tt.data[:, 1] += G * wTsq / (1 + wTsq)
            tt.data[:, 2] += G * wT / (1 + wTsq)

    def plot_theory_stuff(self):
        """[summary]
        
        [description]
        """
        # if not self.view_modes:
        #     return
        data_table_tmp = DataTable(self.axarr)
        data_table_tmp.num_columns = 3
        nmodes = self.parameters["nmodes"].value
        data_table_tmp.num_rows = nmodes
        data_table_tmp.data = np.zeros((nmodes, 3))
        freq = np.logspace(self.parameters["logwmin"].value,
                           self.parameters["logwmax"].value, nmodes)
        data_table_tmp.data[:, 0] = freq
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            data_table_tmp.data[i, 1] = data_table_tmp.data[i, 2] = np.power(
                10, self.parameters["logG%02d" % i].value)
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


class CLTheoryMaxwellModesFrequency(BaseTheoryMaxwellModesFrequency, Theory):
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


class GUITheoryMaxwellModesFrequency(BaseTheoryMaxwellModesFrequency, QTheory):
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
        self.save_modes_action = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-save-Maxwell.png'),
            "Save Modes")            
        self.modesaction.setCheckable(True)
        self.modesaction.setChecked(True)
        self.thToolsLayout.insertWidget(0, tb)

        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged)
        connection_id = self.modesaction.triggered.connect(
            self.modesaction_change)
        connection_id = self.save_modes_action.triggered.connect(
            self.save_modes)

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
        # self.do_calculate("")

    def handle_spinboxValueChanged(self, value):
        """[summary]
        
        [description]
        
        Arguments:
            - value {[type]} -- [description]
        """
        """Handle a change of the parameter 'nmodes'"""
        self.set_param_value('nmodes', value)
        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()
        self.update_parameter_table()


##################################################################################
#   MAXWELL MODES TIME
##################################################################################


class TheoryMaxwellModesTime(CmdBase):
    """Fit a generalized Maxwell model to a time dependent relaxation function. 
    
    * **Function**
        .. math::
            \\begin{eqnarray}
            G(t) & = & \\sum_{i=1}^{n_{modes}} G_i \\exp (-t/\\tau_i)
            \\end{eqnarray}
    
    * **Parameters**
       - :math:`n_{modes}`: number of Maxwell modes equally distributed in logarithmic scale between :math:`\\omega_{min}` and :math:`\\omega_{max}`.
       - logtmin = :math:`\\log(t_{min})`: decimal logarithm of the minimum time.
       - logtmax = :math:`\\log(t_{max})`: decimal logarithm of the maximum time.
       - logGi = :math:`\\log(G_{i})`: decimal logarithm of the amplitude of Maxwell mode :math:`i`.
    
    """
    thname = "Maxwell Modes"
    description = "Maxwell modes, time dependent"
    citations = []

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
        return GUITheoryMaxwellModesTime(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryMaxwellModesTime(
                name, parent_dataset, ax)


class BaseTheoryMaxwellModesTime:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/Gt/Theory/theory.html#maxwell-modes'
    single_file = True
    thname = TheoryMaxwellModesTime.thname
    citations = TheoryMaxwellModesTime.citations

    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.MaxwellModesTime
        self.has_modes = True
        self.MAX_MODES = 40
        self.view_modes = True
        tmin = self.parent_dataset.minpositivecol(0)
        tmax = self.parent_dataset.maxcol(0)
        nmodes = int(np.round(np.log10(tmax / tmin)))

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
            description="Number of Maxwell modes",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False)
        # Interpolate modes from data
        tau = np.logspace(np.log10(tmin), np.log10(tmax), nmodes)
        G = np.abs(
            np.interp(tau, self.parent_dataset.files[0].data_table.data[:, 0],
                      self.parent_dataset.files[0].data_table.data[:, 1]))
        for i in range(self.parameters["nmodes"].value):
            self.parameters["logG%02d" % i] = Parameter(
                "logG%02d" % i,
                np.log10(G[i]),
                "Log of Mode %d amplitude" % i,
                ParameterType.real,
                opt_type=OptType.opt)

        # GRAPHIC MODES
        self.graphicmodes = None
        self.artistmodes = None
        self.setup_graphic_modes()

    def set_param_value(self, name, value):
        """Change other parameters when nmodes is changed, else call parent function"""
        if name == 'nmodes':
            nmodesold = self.parameters["nmodes"].value
            tminold = self.parameters["logtmin"].value
            tmaxold = self.parameters["logtmax"].value
            tauold = np.logspace(tminold, tmaxold, nmodesold)
            Gold = np.zeros(nmodesold)
            for i in range(nmodesold):
                Gold[i] = self.parameters["logG%02d" % i].value
                del self.parameters["logG%02d" % i]

            nmodesnew = value
            message, success = super().set_param_value("nmodes", nmodesnew)
            taunew = np.logspace(tminold, tmaxold, nmodesnew)

            Gnew = np.interp(taunew, tauold, Gold)

            for i in range(nmodesnew):
                self.parameters["logG%02d" % i] = Parameter(
                    "logG%02d" % i,
                    Gnew[i],
                    "Log of Mode %d amplitude" % i,
                    ParameterType.real,
                    opt_type=OptType.opt,
                    min_value=-10,
                    max_value=10)
            if CmdBase.mode == CmdMode.GUI:
                self.spinbox.setValue(value)
        else:
            message, success = super().set_param_value(name, value)
        
        return message, success

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
            self.set_param_value("logG%02d" % i, dy[i])
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
        G = np.zeros(nmodes)
        for i in range(nmodes):
            G[i] = np.power(10, self.parameters["logG%02d" % i].value)

        self.graphicmodes = self.ax.plot(tau, G)[0]
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
            self.parent_dataset.parent_application, self.drag_mode)
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
        G = np.zeros(nmodes)
        for i in range(nmodes):
            G[i] = np.power(10, self.parameters["logG%02d" % i].value)
        return tau, G, True

    def MaxwellModesTime(self, f=None):
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
            gamma = float(f.file_parameters["gamma"])
            if (gamma==0):
                gamma=1
        except:
            gamma = 1

        nmodes = self.parameters["nmodes"].value
        tau = np.logspace(self.parameters["logtmin"].value,
                          self.parameters["logtmax"].value, nmodes)

        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            expT_tau = np.exp(-tt.data[:, 0] / tau[i])
            G = np.power(10, self.parameters["logG%02d" % i].value)
            tt.data[:, 1] += G * expT_tau * gamma

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
                10, self.parameters["logG%02d" % i].value)
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


class CLTheoryMaxwellModesTime(BaseTheoryMaxwellModesTime, Theory):
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


class GUITheoryMaxwellModesTime(BaseTheoryMaxwellModesTime, QTheory):
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
        self.save_modes_action = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-save-Maxwell.png'),
            "Save Modes")            
        self.modesaction.setCheckable(True)
        self.modesaction.setChecked(True)
        self.thToolsLayout.insertWidget(0, tb)

        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged)
        connection_id = self.modesaction.triggered.connect(
            self.modesaction_change)
        connection_id = self.save_modes_action.triggered.connect(
            self.save_modes)

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
        """Handle a change of the parameter 'nmodes'
        
        Arguments:
            - value {[type]} -- [description]
        """
        self.set_param_value('nmodes', value)
        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()
        self.update_parameter_table()
