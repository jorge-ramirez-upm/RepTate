# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License.
"""Module TheoryRoliePoly

Module for the Rolie-Poly theory for the non-linear flow of entangled polymers.

"""
import numpy as np
from scipy.integrate import ode, odeint
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from PyQt5.QtWidgets import QToolBar, QToolButton, QMenu, QStyle, QSpinBox, QTableWidget, QDialog, QVBoxLayout, QDialogButtonBox, QTableWidgetItem
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import Qt
from Theory_rc import *
from enum import Enum


class FlowMode(Enum):
    """Defines the flow geometry used
    
    Parameters can be:
        shear: Shear flow
        uext: Uniaxial extension flow
    """
    shear = 0
    uext = 1


class EditModesDialog(QDialog):
    def __init__(self, parent=None, times=None, G=None):
        super(EditModesDialog, self).__init__(parent)

        self.setWindowTitle("Edit Maxwell modes")
        layout = QVBoxLayout(self)
        nmodes = len(times)

        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, 40)  # min and max number of modes
        self.spinbox.setSuffix(" modes")
        self.spinbox.setValue(nmodes)  #initial value
        layout.addWidget(self.spinbox)

        self.table = QTableWidget()
        self.table.setRowCount(nmodes)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["tau", "G"])
        for i in range(nmodes):
            tau = "%g" % times[i]
            mod = "%g" % G[i]
            self.table.setItem(i, 0, QTableWidgetItem(tau))
            self.table.setItem(i, 1, QTableWidgetItem(mod))

        layout.addWidget(self.table)
        #self.btngrp = QButtonGroup()

        #for item in th_dict.keys():
        #    rb = QRadioButton(item, self)
        #    layout.addWidget(rb)
        #    self.btngrp.addButton(rb)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged)

    def handle_spinboxValueChanged(self, value):
        nrow_old = self.table.rowCount()
        self.table.setRowCount(value)
        for i in range(nrow_old, value):  #create extra rows with defaut values
            self.table.setItem(i, 0, QTableWidgetItem("10"))
            self.table.setItem(i, 1, QTableWidgetItem("1000"))

    # static method to create the dialog and return (date, time, accepted)
    #@staticmethod
    #def getMaxwellModesProvider(self, parent = None, th_dict = {}):
    #    dialog = GetModesDialog(parent, th_dict)
    #    result = dialog.exec_()
    #    return (self.btngrp.checkedButton().text(), result == QDialog.Accepted)


class TheoryRoliePoly(CmdBase):
    """Rolie-Poly
    
    [description]
    """
    thname = "RoliePoly"
    description = "RoliePoly"
    citations = "Likhtman, A.E. & Graham, R.S.\n\
Simple constitutive equation for linear polymer melts derived from molecular theory: Rolie-Poly equation\n\
J. Non-Newtonian Fluid Mech., 2003, 114, 1-12"

    def __new__(cls, name="ThRoliePoly", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryRoliePoly(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryRoliePoly(
                name, parent_dataset, ax)


class BaseTheoryRoliePoly:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/en/latest/manual/Theories/NLVE/RoliePoly.html'
    single_file = False

    def __init__(self, name="ThRoliePoly", parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThRoliePoly"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.RoliePoly
        self.has_modes = True
        self.parameters["beta"] = Parameter(
            name="beta",
            value=0.5,
            description="CCR coefficient",
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters["delta"] = Parameter(
            name="delta",
            value=-0.5,
            description="CCR exponent",
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters["lmax"] = Parameter(
            name="lmax",
            value=10.0,
            description="Maximum extensibility",
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters["nmodes"] = Parameter(
            name="nmodes",
            value=2,
            description="Number of modes",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False)
        self.parameters["nstretch"] = Parameter(
            name="nstretch",
            value=2,
            description="Number of strecthing modes",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False)
        for i in range(self.parameters["nmodes"].value):
            self.parameters["G%02d" % i] = Parameter(
                name="G%02d" % i,
                value=1000.0,
                description="Modulus of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.nopt,
                display_flag=False,
                bracketed=True,
                min_value=0)
            self.parameters["tauD%02d" % i] = Parameter(
                name="tauD%02d" % i,
                value=10.0,
                description="Terminal time of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.nopt,
                display_flag=False,
                bracketed=True,
                min_value=0)
            self.parameters["tauR%02d" % i] = Parameter(
                name="tauR%02d" % i,
                value=0.5,
                description="Rouse time of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.opt,
                bracketed=True,
                min_value=0)

        self.view_LVEenvelope = False
        auxseries = self.ax.plot([], [], label='')
        self.LVEenvelopeseries = auxseries[0]
        self.LVEenvelopeseries.set_marker('')
        self.LVEenvelopeseries.set_linestyle('--')
        self.LVEenvelopeseries.set_visible(self.view_LVEenvelope)
        self.LVEenvelopeseries.set_color('green')
        self.LVEenvelopeseries.set_linewidth(5)
        self.LVEenvelopeseries.set_label('')

        self.MAX_MODES = 40
        self.flow_mode = FlowMode.shear

    def destructor(self):
        """Called when the theory tab is closed
        
        [description]
        """
        self.extra_graphic_visible(False)
        self.ax.lines.remove(self.LVEenvelopeseries)

    def show_theory_extras(self, show=False):
        """Called when the active theory is changed
        
        [description]
        """
        if CmdBase.mode == CmdMode.GUI:
            self.Qhide_theory_extras(show)
        self.extra_graphic_visible(show)

    def extra_graphic_visible(self, state):
        """[summary]
        
        [description]
        """
        self.LVEenvelopeseries.set_visible(state)
        self.parent_dataset.parent_application.update_plot()

    def get_modes(self):
        """[summary]
        
        [description]
        
        Returns:
            [type] -- [description]
        """
        nmodes = self.parameters["nmodes"].value
        tau = np.zeros(nmodes)
        G = np.zeros(nmodes)
        for i in range(nmodes):
            tau[i] = self.parameters["tauD%02d" % i].value
            G[i] = self.parameters["G%02d" % i].value
        return tau, G

    def set_modes(self, tau, G):
        """[summary]
        
        [description]
        
        Arguments:
            tau {[type]} -- [description]
            G {[type]} -- [description]
        """
        nmodes = len(tau)
        self.set_param_value("nmodes", nmodes)
        self.set_param_value("nstretch", nmodes)

        for i in range(nmodes):
            self.set_param_value("tauD%02d" % i, tau[i])
            self.set_param_value("G%02d" % i, G[i])
            self.set_param_value("tauR%02d" % i, 0.5)

    def sigmadot_shear(self, sigma, t, p):
        """Rolie-Poly differential equation under shear flow
        
        [description]
        
        Arguments:
            sigma {array} -- vector of state variables, sigma = [sxx, syy, sxy]
            t {float} -- time
            p {array} -- vector of the parameters, p = [tauD, tauR, beta, delta, gammadot]
        """
        sxx, syy, sxy = sigma
        tauD, tauR, beta, delta, gammadot = p

        # Create the vector with the time derivative of sigma
        trace_sigma = sxx + 2 * syy
        aux1 = 2 * (1 - np.sqrt(3. / trace_sigma)) / tauR
        aux2 = beta * (trace_sigma / 3)**delta
        return [
            2 * gammadot * sxy - (sxx - 1.) / tauD - aux1 * (sxx + aux2 *
                                                             (sxx - 1.)),
            -1.0 * (syy - 1.) / tauD - aux1 * (syy + aux2 * (syy - 1.)),
            gammadot * syy - sxy / tauD - aux1 * (sxy + aux2 * sxy)
        ]

    def sigmadot_shear_nostretch(self, sigma, t, p):
        """Rolie-Poly differential equation under shear flow, without stretching
        
        [description]
        
        Arguments:
            sigma {array} -- vector of state variables, sigma = [sxx, syy, sxy]
            t {float} -- time
            p {array} -- vector of the parameters, p = [tauD, tauR, beta, delta, gammadot]
        """
        sxx, syy, sxy = sigma
        tauD, tauR, beta, delta, gammadot = p

        # Create the vector with the time derivative of sigma
        trace_sigma = sxx + 2 * syy
        aux1 = 2.0 * (1 - np.sqrt(3.0 / trace_sigma)) / tauR
        aux2 = beta * (trace_sigma / 3.0)**delta
        return [
            2.0 * gammadot * sxy -
            (sxx - 1.0) / tauD - 2.0 / 3.0 * gammadot * sxy * (sxx + beta *
                                                               (sxx - 1)),
            -(syy - 1.0) / tauD - 2.0 / 3.0 * gammadot * sxy * (syy + beta *
                                                                (syy - 1)),
            gammadot * syy - sxy / tauD - 2.0 / 3.0 * gammadot * sxy *
            (sxy + beta * sxy)
        ]

    def sigmadot_uext(self, sigma, t, p):
        """Rolie-Poly differential equation under uniaxial elongational flow

        [description]

        Arguments:
            sigma {array} -- vector of state variables, sigma = [sxx, syy]
            t {float} -- time
            p {array} -- vector of the parameters, p = [tauD, tauR, beta, delta, gammadot]
        """
        sxx, syy = sigma
        tauD, tauR, beta, delta, epsilon_dot = p

        # Create the vector with the time derivative of sigma
        trace_sigma = sxx + 2 * syy
        aux1 = 2.0 * (1.0 - np.sqrt(3.0 / trace_sigma)) / tauR
        aux2 = beta * np.power(trace_sigma / 3.0, delta)
        dsxx = 2.0 * epsilon_dot * sxx - (sxx - 1.0) / tauD - aux1 * (
            sxx + aux2 * (sxx - 1.0))
        dsyy = -epsilon_dot * syy - (syy - 1.0) / tauD - aux1 * (syy + aux2 *
                                                                 (syy - 1.0))
        return [dsxx, dsyy]

    def sigmadot_uext_nostretch(self, sigma, t, p):
        """Rolie-Poly differential equation under elongation flow, wihtout stretching
        
        [description]
        
        Arguments:
            sigma {array} -- vector of state variables, sigma = [sxx, syy]
            t {float} -- time
            p {array} -- vector of the parameters, p = [tauD, tauR, beta, delta, epsilon_dot]
        """
        sxx, syy = sigma
        tauD, tauR, beta, delta, epsilon_dot = p

        # Create the vector with the time derivative of sigma
        trace_k_sigma = epsilon_dot * (sxx - syy)
        aux1 = 2.0 / 3.0 * trace_k_sigma
        return [
            2.0 * epsilon_dot * sxx - (sxx - 1.0) / tauD - aux1 *
            (sxx + beta * (sxx - 1.0)), -epsilon_dot * syy -
            (syy - 1.0) / tauD - aux1 * (syy + beta * (syy - 1.0))
        ]

    def RoliePoly(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        #flow geometry
        if self.flow_mode == FlowMode.shear:
            pde_stretch = self.sigmadot_shear
            pde_nostretch = self.sigmadot_shear_nostretch
            sigma0 = [1.0, 1.0, 0.0]  # sxx, syy, sxy
        elif self.flow_mode == FlowMode.uext:
            pde_stretch = self.sigmadot_uext
            pde_nostretch = self.sigmadot_uext_nostretch
            sigma0 = [1.0, 1.0]  # sxx, syy
        else:
            return

        # ODE solver parameters
        abserr = 1.0e-8
        relerr = 1.0e-6
        t = ft.data[:, 0]
        t = np.concatenate([[0], t])
        # sigma0 = [1.0, 1.0, 0.0]  # sxx, syy, sxy
        beta = self.parameters["beta"].value
        delta = self.parameters["delta"].value
        gammadot = float(f.file_parameters["gdot"])
        nmodes = self.parameters["nmodes"].value
        nstretch = self.parameters["nstretch"].value
        for i in range(nmodes):
            tauD = self.parameters["tauD%02d" % i].value
            tauR = self.parameters["tauR%02d" % i].value
            p = [tauD, tauR, beta, delta, gammadot]
            if i < nstretch:
                sig = odeint(
                    pde_stretch,
                    sigma0,
                    t,
                    args=(p, ),
                    atol=abserr,
                    rtol=relerr)
            else:
                sig = odeint(
                    pde_nostretch,
                    sigma0,
                    t,
                    args=(p, ),
                    atol=abserr,
                    rtol=relerr)
            if self.flow_mode == FlowMode.shear:
                sxy = np.delete(sig[:, 2], [0])
                tt.data[:, 1] += self.parameters["G%02d" % i].value * sxy
            elif self.flow_mode == FlowMode.uext:
                sxx = np.delete(sig[:, 0], [0])
                syy = np.delete(sig[:, 1], [0])
                tt.data[:, 1] += self.parameters["G%02d" % i].value * (
                    sxx - syy)

    def set_param_value(self, name, value):
        """[summary]
        
        [description]
        
        Arguments:
            name {[type]} -- [description]
            value {[type]} -- [description]
        """
        if (name == "nmodes"):
            oldn = self.parameters["nmodes"].value
        super(BaseTheoryRoliePoly, self).set_param_value(name, value)
        if (name == "nmodes"):
            for i in range(self.parameters["nmodes"].value):
                self.parameters["G%02d" % i] = Parameter(
                    name="G%02d" % i,
                    value=1000.0,
                    description="Modulus of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.nopt,
                    display_flag=False,
                    bracketed=True,
                    min_value=0)
                self.parameters["tauD%02d" % i] = Parameter(
                    name="tauD%02d" % i,
                    value=10.0,
                    description="Terminal time of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.nopt,
                    display_flag=False,
                    bracketed=True,
                    min_value=0)
                self.parameters["tauR%02d" % i] = Parameter(
                    name="tauR%02d" % i,
                    value=0.5,
                    description="Rouse time of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.opt,
                    display_flag=True,
                    bracketed=True,
                    min_value=0)
            if (oldn > self.parameters["nmodes"].value):
                for i in range(self.parameters["nmodes"].value, oldn):
                    del self.parameters["G%02d" % i]
                    del self.parameters["tauD%02d" % i]
                    del self.parameters["tauR%02d" % i]
        return True


class CLTheoryRoliePoly(BaseTheoryRoliePoly, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name="ThRoliePoly", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)


class GUITheoryRoliePoly(BaseTheoryRoliePoly, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self, name="ThRoliePoly", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))

        self.tbutflow = QToolButton()
        self.tbutflow.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        self.shear_flow_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-garden-shears.png'),
            "Shear Flow")
        self.extensional_flow_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-socks.png'),
            "Extensional Flow")
        self.tbutflow.setDefaultAction(self.shear_flow_action)
        self.tbutflow.setMenu(menu)
        tb.addWidget(self.tbutflow)

        self.tbutmodes = QToolButton()
        self.tbutmodes.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        self.get_modes_action = menu.addAction(self.style().standardIcon(
            getattr(QStyle, 'SP_DialogYesButton')), "Get Modes")
        self.edit_modes_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-edit-file.png'),
            "Edit Modes")
        self.plot_modes_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-scatter-plot.png'),
            "Plot Modes")
        self.tbutmodes.setDefaultAction(self.get_modes_action)
        self.tbutmodes.setMenu(menu)
        tb.addWidget(self.tbutmodes)

        self.linearenvelope = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-visible.png'),
            'Show Linear Envelope')
        self.linearenvelope.setCheckable(True)
        self.linearenvelope.setChecked(False)

        self.spinbox = QSpinBox()
        self.spinbox.setRange(0, self.MAX_MODES)  # min and max number of modes
        self.spinbox.setSuffix(" Rmodes")
        self.spinbox.setToolTip("Number of stretching modes")
        self.spinbox.setValue(self.parameters["nmodes"].value)  #initial value
        tb.addWidget(self.spinbox)
        self.show_help_button = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-user-manual.png'),
            'Online Manual')

        self.thToolsLayout.insertWidget(0, tb)

        connection_id = self.shear_flow_action.triggered.connect(
            self.select_shear_flow)
        connection_id = self.extensional_flow_action.triggered.connect(
            self.select_extensional_flow)
        connection_id = self.get_modes_action.triggered.connect(
            self.get_modes_reptate)
        connection_id = self.edit_modes_action.triggered.connect(
            self.edit_modes_window)
        connection_id = self.plot_modes_action.triggered.connect(
            self.plot_modes_graph)
        connection_id = self.linearenvelope.triggered.connect(
            self.show_linear_envelope)
        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged)
        connection_id = self.show_help_button.triggered.connect(
            self.handle_show_help)

    def handle_show_help(self):
        try:
            help_file = self.help_file
        except AttributeError as e:
            print('in "handle_show_help":', e)
            return
        QDesktopServices.openUrl(QUrl.fromUserInput((help_file)))

    def handle_spinboxValueChanged(self, value):
        nmodes = self.parameters["nmodes"].value
        self.set_param_value("nstretch", min(nmodes, value))

    def Qhide_theory_extras(self, state):
        """Uncheck the LVE button. Called when curent theory is changed
        
        [description]
        """
        self.linearenvelope.setChecked(state)

    def show_linear_envelope(self, state):
        self.extra_graphic_visible(state)
        # self.LVEenvelopeseries.set_visible(self.linearenvelope.isChecked())
        # self.plot_theory_stuff()
        # self.parent_dataset.parent_application.update_plot()

    def plot_theory_stuff(self):
        """[summary]
        
        [description]
        """
        data_table_tmp = DataTable(self.axarr)
        data_table_tmp.num_columns = 2
        data_table_tmp.num_rows = 100
        data_table_tmp.data = np.zeros((100, 2))

        times = np.logspace(-2, 3, 100)
        data_table_tmp.data[:, 0] = times
        nmodes = self.parameters["nmodes"].value
        data_table_tmp.data[:, 1] = 0
        fparamaux = {}
        fparamaux["gdot"] = 1e-6
        for i in range(nmodes):
            G = self.parameters["G%02d" % i].value
            tauD = self.parameters["tauD%02d" % i].value
            data_table_tmp.data[:, 1] += G * tauD * (
                1 - np.exp(-times / tauD)) * 1e-6
        if self.flow_mode == FlowMode.uext:
            data_table_tmp.data[:, 1] *= 3.0
        view = self.parent_dataset.parent_application.current_view
        try:
            x, y, success = view.view_proc(data_table_tmp, fparamaux)
        except TypeError as e:
            print(e)
            return
        self.LVEenvelopeseries.set_data(x[:, 0], y[:, 0])

    def select_shear_flow(self):
        self.flow_mode = FlowMode.shear
        self.tbutflow.setDefaultAction(self.shear_flow_action)

    def select_extensional_flow(self):
        self.flow_mode = FlowMode.uext
        self.tbutflow.setDefaultAction(self.extensional_flow_action)

    def get_modes_reptate(self):
        self.Qcopy_modes()

    def edit_modes_window(self):
        times, G = self.get_modes()
        d = EditModesDialog(self, times, G)
        if d.exec_():
            nmodes = d.table.rowCount()
            self.set_param_value("nmodes", nmodes)
            self.set_param_value("nstretch", nmodes)

            for i in range(nmodes):
                self.set_param_value("tauD%02d" % i,
                                     float(d.table.item(i, 0).text()))
                self.set_param_value("G%02d" % i,
                                     float(d.table.item(i, 1).text()))
                self.set_param_value("tauR%02d" % i, 0.5)
                pass

    def plot_modes_graph(self):
        pass
