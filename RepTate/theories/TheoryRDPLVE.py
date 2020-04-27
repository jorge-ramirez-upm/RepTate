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
"""Module TheoryRDPLVE

Template file for creating a new theory
"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from PyQt5.QtWidgets import QToolBar, QToolButton, QMenu, QStyle, QSpinBox, QTableWidget, QDialog, QVBoxLayout, QHBoxLayout, QDialogButtonBox, QTableWidgetItem, QMessageBox, QLabel, QLineEdit, QRadioButton, QButtonGroup, QFileDialog
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices, QDoubleValidator
from PyQt5.QtCore import Qt
from TheoryRolieDoublePoly import Dilution, GcorrMode, GetMwdRepate, EditMWDDialog, EditModesDialog
from math import sqrt
from collections import OrderedDict


class TheoryRDPLVE(CmdBase):
    """Rolie-Double-Poly equation for the linear predictions of polydispere entangled linear polymers

    * **Function**
        .. math::
            \\begin{eqnarray}
            G'(\\omega) & = & \\sum_{i=1}^{n_{modes}}\\sum_{j=1}^{n_{modes}} G \\phi_i \\phi_j \\frac{(\\omega\\tau)^2}{1+(\\omega\\tau)^2} \\\\
            G''(\\omega) & = & \\sum_{i=1}^{n_{modes}}\\sum_{j=1}^{n_{modes}} G \\phi_i \\phi_j \\frac{\\omega\\tau}{1+(\\omega\\tau)^2}
            \\end{eqnarray}
        
        where, :math:`\\tau = (\\tau_{\\text D,i}^{-1} + \\tau_{\\text D, j}^{-1})^{-1}`, and,
        if the "modulus correction" button is clicked, :math:`G=G_N^0 \\times g(Z_\\text{eff})`, with :math:`g` the Likthman-McLeish CLF correction function,
        otherwise :math:`G=G_N^0`

    * **Parameters**
       - ``nmodes`` : number of molecular mass components.
       - ``G_N^0`` : Plateau modulus
       - ``phi0i`` : Volume fraction of component :math:`i`
       - ``tauD0i`` : Reptation time of component :math:`i`

    
    [description]
    """
    thname = 'RDP LVE'
    description = 'Linear ViscoElastic predictions of the Rolie-Double-Poly model'
    citations = []

    def __new__(cls, name='', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUITheoryRDPLVE(
            name, parent_dataset,
            axarr) if (CmdBase.mode == CmdMode.GUI) else CLTheoryRDPLVE(
                name, parent_dataset, axarr)


class BaseTheoryRDPLVE:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/LVE/Theory/theory.html#rolie-double-poly-lve'
    single_file = True  # False if the theory can be applied to multiple files simultaneously
    thname = TheoryRDPLVE.thname
    citations = TheoryRDPLVE.citations

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate  # main theory function
        self.has_modes = False  # True if the theory has modes
        self.parameters["GN0"] = Parameter(
            name="GN0",
            value=1000.0,
            description="Plateau modulus",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0)
        self.parameters["Me"] = Parameter(
            name="Me",
            value=1e4,
            description="Entanglement molecular mass",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False)
        self.parameters["tau_e"] = Parameter(
            name="tau_e",
            value=0.01,
            description="Entanglement relaxation time",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False)
        self.parameters["nmodes"] = Parameter(
            name="nmodes",
            value=2,
            description="Number of Maxwell modes",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False,
            min_value=1)
        nmode = self.parameters["nmodes"].value
        for i in range(nmode):
            self.parameters["phi%02d" % i] = Parameter(
                name="phi%02d" % i,
                value=1. / nmode,
                description="Volume fraction of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.nopt,
                display_flag=False,
                min_value=0,
                max_value=1)
            self.parameters["tauD%02d" % i] = Parameter(
                name="tauD%02d" % i,
                value=100.0,
                description="Terminal time of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.nopt,
                display_flag=False,
                min_value=0)
        self.with_gcorr = GcorrMode.none
        self.MWD_m = [100, 1000]
        self.MWD_phi =  [0.5, 0.5]
        self.Zeff = []
        self.MAX_MODES = 200

    def set_extra_data(self, extra_data):
        """Set extra data when loading project"""
        self.MWD_m = extra_data['MWD_m']
        self.MWD_phi = extra_data['MWD_phi']
        self.Zeff = extra_data['Zeff']

        # G button
        if extra_data['with_gcorr']:
            self.with_gcorr == GcorrMode.with_gcorr
            self.with_gcorr_button.setChecked(True)

    def get_extra_data(self):
        """Set extra_data when saving project"""
        self.extra_data['MWD_m'] = self.MWD_m
        self.extra_data['MWD_phi'] = self.MWD_phi
        self.extra_data['Zeff'] = self.Zeff
        self.extra_data['with_gcorr'] = self.with_gcorr == GcorrMode.with_gcorr

    def get_modes(self):
        """Get the values of Maxwell Modes from this theory"""
        nmodes = self.parameters["nmodes"].value
        tau = np.zeros(nmodes)
        G = np.zeros(nmodes)
        GN0 = self.parameters["GN0"].value
        for i in range(nmodes):
            tau[i] = self.parameters["tauD%02d" % i].value
            G[i] = GN0 * self.parameters["phi%02d" % i].value
        return tau, G, True

    def fZ(self, z):
        """CLF correction function Likthman-McLeish (2002)"""
        return 1 - 2 * 1.69 / sqrt(z) + 4.17 / z - 1.55 / (z * sqrt(z))

    def gZ(self, z):
        """CLF correction function for modulus Likthman-McLeish (2002)"""
        return 1 - 1.69 / sqrt(z) + 2.0 / z - 1.24 / (z * sqrt(z))

    def set_modes_from_mwd(self, m, phi):
        """[summary]
        
        [description]
        
        Returns:
            - [type] -- [description]
        """
        Me = self.parameters["Me"].value
        taue = self.parameters["tau_e"].value
        res = Dilution(m, phi, taue, Me, self).res
        if res[0] == False:
            self.Qprint("Could not set modes from MDW")
            return
        _, phi, taus, taud = res
        nmodes = len(phi)
        self.set_param_value("nmodes", nmodes)
        for i in range(nmodes):
            self.set_param_value("phi%02d" % i, phi[i])
            self.set_param_value("tauD%02d" % i, taud[i])
        self.Qprint("Got %d modes from MWD" % nmodes)
        self.update_parameter_table()
        self.Qprint('<font color=green><b>Press "Calculate" to update theory</b></font>')
        self.parent_dataset.handle_actionCalculate_Theory()

    def set_param_value(self, name, value):
        """[summary]
        
        [description]
        
        Arguments:
            - name {[type]} -- [description]
            - value {[type]} -- [description]
        """
        if (name == "nmodes"):
            oldn = self.parameters["nmodes"].value
        message, success = super().set_param_value(name, value)
        if not success:
            return message, success
        if (name == "nmodes"):
            for i in range(self.parameters["nmodes"].value):
                self.parameters["phi%02d" % i] = Parameter(
                    name="phi%02d" % i,
                    value=0.0,
                    description="Volume fraction of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.nopt,
                    display_flag=False,
                    min_value=0)
                self.parameters["tauD%02d" % i] = Parameter(
                    name="tauD%02d" % i,
                    value=100.0,
                    description="Terminal time of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.nopt,
                    display_flag=False,
                    min_value=0)
            if (oldn > self.parameters["nmodes"].value):
                for i in range(self.parameters["nmodes"].value, oldn):
                    del self.parameters["phi%02d" % i]
                    del self.parameters["tauD%02d" % i]
        return '', True


    def calculate(self, f=None):
        """Template function that returns the square of y
        
        [description]
        
        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        nmodes = self.parameters['nmodes'].value
        taud = []
        phi = []
        for i in range(nmodes):
            taud.append(self.parameters['tauD%02d' % i].value)
            phi.append(self.parameters['phi%02d' % i].value)

        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            G = self.parameters['GN0'].value
            if self.with_gcorr == GcorrMode.with_gcorr:
                # G = G * sqrt(self.fZ(self.Zeff[i]))
                G = G * self.gZ(self.Zeff[i])
            for j in range(nmodes):
                tau = 1. / (1. / taud[i] + 1. / taud[j])
                wT = tt.data[:, 0] * tau
                wTsq = wT**2
                tt.data[:, 1] += G * phi[i] * phi[j] * wTsq / (1 + wTsq)
                tt.data[:, 2] += G * phi[i] * phi[j] * wT / (1 + wTsq)

class CLTheoryRDPLVE(BaseTheoryRDPLVE, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # This class usually stays empty


class GUITheoryRDPLVE(BaseTheoryRDPLVE, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))

        self.tbutmodes = QToolButton()
        self.tbutmodes.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        self.get_modes_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-broadcasting.png'),
            "Get Modes (MWD app)")
        self.get_modes_data_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-broadcasting.png'),
            "Get Modes (MWD data)")
        self.edit_modes_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-edit-file.png'),
            "Edit Modes")
        # self.plot_modes_action = menu.addAction(
        #     QIcon(':/Icon8/Images/new_icons/icons8-scatter-plot.png'),
        #     "Plot Modes")
        self.save_modes_action = menu.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-save-Maxwell.png'),
            "Save Modes")
        self.tbutmodes.setDefaultAction(self.get_modes_action)
        self.tbutmodes.setMenu(menu)
        tb.addWidget(self.tbutmodes)
        #Modulus correction button
        self.with_gcorr_button = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-circled-g-filled.png'),
            'Modulus Correction')
        self.with_gcorr_button.setCheckable(True)

        self.thToolsLayout.insertWidget(0, tb)

        connection_id = self.get_modes_action.triggered.connect(
            self.get_modes_reptate)
        connection_id = self.get_modes_data_action.triggered.connect(
            self.edit_mwd_modes)
        connection_id = self.edit_modes_action.triggered.connect(
            self.edit_modes_window)
        connection_id = self.with_gcorr_button.triggered.connect(
            self.handle_with_gcorr_button)
        connection_id = self.save_modes_action.triggered.connect(
            self.save_modes)

    def handle_with_gcorr_button(self, checked):
        if checked:
            if len(self.Zeff) > 0:
                # if Zeff contains something
                self.with_gcorr = GcorrMode.with_gcorr
            else:
                self.Qprint('<font color=orange><b>Modulus correction needs Z from MWD</b></font>')
                self.with_gcorr_button.setChecked(False)
                return
        else:
            self.with_gcorr = GcorrMode.none
        self.parent_dataset.handle_actionCalculate_Theory()

    def Qhide_theory_extras(self, show):
        """Called when curent theory is changed
        
        [description]
        """
        self.parent_dataset.actionMinimize_Error.setDisabled(show)
        self.parent_dataset.actionShow_Limits.setDisabled(show)
        self.parent_dataset.actionVertical_Limits.setDisabled(show)
        self.parent_dataset.actionHorizontal_Limits.setDisabled(show)

    def get_modes_reptate(self):
        apmng = self.parent_dataset.parent_application.parent_manager
        get_dict = {}
        for app in apmng.applications.values():
            app_index = apmng.ApplicationtabWidget.indexOf(app)
            app_tab_name = apmng.ApplicationtabWidget.tabText(app_index)
            for ds in app.datasets.values():
                ds_index = app.DataSettabWidget.indexOf(ds)
                ds_tab_name = app.DataSettabWidget.tabText(ds_index)
                for th in ds.theories.values():
                    th_index = ds.TheorytabWidget.indexOf(th)
                    th_tab_name = ds.TheorytabWidget.tabText(th_index)
                    if th.thname == 'Discretize MWD':
                        get_dict["%s.%s.%s" % (app_tab_name, ds_tab_name,
                                               th_tab_name)] = th.get_mwd

        if get_dict:
            d = GetMwdRepate(self, get_dict, 'Select Discretized MWD')
            if (d.exec_() and d.btngrp.checkedButton() != None):
                _, success1 = self.set_param_value("tau_e", d.taue_text.text())
                _, success2 = self.set_param_value("Me", d.Me_text.text())
                if not success1 * success2:
                    self.Qprint("Could not understand Me or taue, try again")
                    return
                item = d.btngrp.checkedButton().text()
                m, phi = get_dict[item]()

                self.MWD_m = np.copy(m)
                self.MWD_phi = np.copy(phi)
                self.set_modes_from_mwd(m, phi)
        else:
            # no theory Discretise MWD found
            QMessageBox.warning(
                    self, 'Get MW distribution',
                    'No \"Discretize MWD\" theory found')
        # self.parent_dataset.handle_actionCalculate_Theory()

    def edit_modes_window(self):
        nmodes = self.parameters["nmodes"].value
        phi = np.zeros(nmodes)
        taud = np.zeros(nmodes)
        for i in range(nmodes):
            phi[i] = self.parameters["phi%02d" % i].value
            taud[i] = self.parameters["tauD%02d" % i].value
        param_dic = OrderedDict()
        param_dic["phi"] = phi
        param_dic["tauD"] = taud
        d = EditModesDialog(self, param_dic, self.MAX_MODES)
        if d.exec_():
            nmodes = d.table.rowCount()
            self.set_param_value("nmodes", nmodes)
            # self.set_param_value("nstretch", nmodes)
            success = True
            for i in range(nmodes):
                msg, success1 = self.set_param_value("phi%02d" % i,
                                                     d.table.item(i, 0).text())
                msg, success2 = self.set_param_value("tauD%02d" % i,
                                                     d.table.item(i, 1).text())
                success *= success1 * success2
            if not success:
                QMessageBox.warning(
                    self, 'Error',
                    'Some parameter(s) could not be updated.\nPlease try again.'
                )
            else:
                self.handle_actionCalculate_Theory()

    def edit_mwd_modes(self):
        d = EditMWDDialog(self, self.MWD_m, self.MWD_phi, 200)
        if d.exec_():
            nmodes = d.table.rowCount()
            m = []
            phi = []
            _, success1 = self.set_param_value("tau_e", d.taue_text.text())
            _, success2 = self.set_param_value("Me", d.Me_text.text())
            if not success1 * success2:
                self.Qprint("Could not understand Me or taue, try again")
                return
            for i in range(nmodes):
                try:
                    m.append(float(d.table.item(i, 0).text()))
                    phi.append(float(d.table.item(i, 1).text()))
                except ValueError:
                    self.Qprint("Could not understand line %d, try again" %
                                (i + 1))
                    return
            self.MWD_m = np.copy(m)
            self.MWD_phi = np.copy(phi)
            self.set_modes_from_mwd(m, phi)