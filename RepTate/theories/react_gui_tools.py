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
import os
import numpy as np
import ctypes as ct
import react_ctypes_helper as rch
#BoB form
from PyQt5.QtWidgets import QDialog, QToolBar, QVBoxLayout, QHBoxLayout, QDialogButtonBox, QLineEdit, QGroupBox, QFormLayout, QLabel, QFileDialog, QRadioButton, QSpinBox, QGridLayout, QSizePolicy, QSpacerItem, QScrollArea, QWidget, QCheckBox, QMessageBox, QFrame, QPlainTextEdit
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QIcon, QDesktopServices
from PyQt5.QtCore import QSize, Qt, QUrl
import psutil


def launch_mix_dialog(parent_theory):
    """Launch a dialog box to select the React-Mix theory parameters"""
    dialog = ParameterReactMix(parent_theory)
    if dialog.exec_():
        parent_theory.success_dialog = True
    else:
        parent_theory.success_dialog = False


def launch_mulmet_dialog(parent_theory):
    """Launch a dialog box to select the Multi-Metallocene theory parameters"""
    dialog = ParameterMultiMetCSTR(parent_theory)
    if dialog.exec_():
        parent_theory.success_dialog = True
    else:
        parent_theory.success_dialog = False


def request_more_polymer(parent_theory):
    """Generic function called when run out of polymers"""
    success_increase_memory = None
    new_max, success_increase_memory = handle_increase_records(
        parent_theory, 'polymer')
    if not success_increase_memory:
        message = '<b>Ran out of storage for polymer records.</b> Options to avoid this are:<br>'
        message += '(1) Reduce number of polymers requested</b>'
        message += '(2) Close some other theories'
        parent_theory.Qprint(message)
    else:
        parent_theory.Qprint(
            'Number of polymers was increased to %.4g' % new_max)

    parent_theory.success_increase_memory = success_increase_memory


def request_more_arm(parent_theory):
    """Generic function called when run out of arms"""
    success_increase_memory = None
    new_max, success_increase_memory = handle_increase_records(
        parent_theory, 'arm')
    if not success_increase_memory:
        message = '<b>Ran out of storage for arm records.</b> Options to avoid this are:<br>'
        message += '(1) Reduce number of polymers requested<br>'
        message += '(2) Adjust BoB parameters so that fewer polymers are saved<br>'
        message += '(3) Close some other theories<br>'
        message += '(4) Adjust parameters to avoid gelation'
        parent_theory.Qprint(message)
        # i = numtomake
        # rch.tCSTR_global.tobitaCSTRerrorflag = True
    else:
        parent_theory.Qprint(
            'Number of arms was increased to %.4g' % new_max)
    parent_theory.success_increase_memory = success_increase_memory


def request_more_dist(parent_theory):
    """Generic function called when run out of distributions"""
    success_increase_memory = None
    new_max, success_increase_memory = handle_increase_records(
        parent_theory, 'dist')
    if success_increase_memory:
        rch.link_react_dist()  #re-link the python array with the C array
        parent_theory.Qprint(
            'Number of dist. was increased to %.4g' % new_max)
        parent_theory.handle_actionCalculate_Theory()
    else:
        parent_theory.Qprint(
            '<b>Too many theories open for internal storage.<b> Please close a theory or increase records"'
        )
def set_extra_data(parent_theory, extra_data):
    try:
        if extra_data['prio_senio_checked'] == 1:
            handle_btn_prio_senio(parent_theory, True)
    except Exception as e:
        print("set_extra_data", e)

def get_extra_data(parent_theory):
    try:
        parent_theory.extra_data['prio_senio_checked'] = int(parent_theory.do_priority_seniority)
    except Exception as e:
        print("get_extra_data", e)

def initialise_tool_bar(parent_theory):
    """Add icons in theory toolbar"""
    #disable buttons
    parent_theory.parent_dataset.actionMinimize_Error.setDisabled(True)
    # parent_theory.parent_dataset.actionCalculate_Theory.setDisabled(True)
    # parent_theory.parent_dataset.actionShow_Limits.setDisabled(True)
    # parent_theory.parent_dataset.actionVertical_Limits.setDisabled(True)
    parent_theory.parent_dataset.actionHorizontal_Limits.setDisabled(True)

    ######toolbar
    tb = QToolBar()
    tb.setIconSize(QSize(24, 24))
    parent_theory.thToolsLayout.insertWidget(0, tb)

    #BOB settings buttons
    parent_theory.bob_settings_button = tb.addAction(
        QIcon(':/Icon8/Images/new_icons/icons8-BoB-settings.png'),
        'Edit BoB Binning Settings')
    parent_theory.save_bob_configuration_button = tb.addAction(
        QIcon(':/Icon8/Images/new_icons/icons8-save-BoB.png'),
        'Save Polymer Configuration for BoB')

    # seniority priority
    parent_theory.btn_prio_senio = tb.addAction(QIcon(':/Icon8/Images/new_icons/priority_seniority.png'), 'Calculate Priority and Seniority (can take some time)')
    parent_theory.btn_prio_senio.setCheckable(True)
    parent_theory.btn_prio_senio.setChecked(parent_theory.do_priority_seniority)
    parent_theory.old_views = []

    #signals
    connection_id = parent_theory.bob_settings_button.triggered.connect(
        parent_theory.handle_edit_bob_settings)
    connection_id = parent_theory.save_bob_configuration_button.triggered.connect(
        parent_theory.handle_save_bob_configuration)
    parent_theory.btn_prio_senio.triggered.connect(parent_theory.handle_btn_prio_senio)

def handle_btn_prio_senio(parent_theory, checked):
    """Change do_priority_seniority"""
    parent_theory.do_priority_seniority = checked
    app = parent_theory.parent_dataset.parent_application
    app.viewComboBox.blockSignals(True)
    if checked and (app.viewComboBox.count() < len(app.views)):
        app.nplots = min(app.nplot_max, app.nplots + 1)
        app.multiviews[app.nplots - 1] = app.views[app.extra_view_names[0]]
        for view_name in app.extra_view_names:
            app.viewComboBox.addItems([app.views[view_name].name,])
            app.viewComboBox.setItemData(app.viewComboBox.count() - 1, app.views[view_name].description, Qt.ToolTipRole)
        app.multiplots.reorg_fig(app.nplots)
    elif (not checked) and (app.viewComboBox.count() == len(app.views)):
        ps_view = False
        for i, view in enumerate(app.multiviews):
            if view.name in app.extra_view_names:
                app.multiviews[i] = app.views[app.viewComboBox.itemText(i)]
                ps_view = True
        if ps_view:
            app.nplots = max(1, app.nplots - 1)
            app.multiplots.reorg_fig(app.nplots)
        for _ in app.extra_view_names:
            app.viewComboBox.removeItem(app.viewComboBox.count() - 1)
    parent_theory.parent_dataset.toggle_vertical_limits(checked)
    app.viewComboBox.blockSignals(False)

def show_theory_extras(parent_theory, show):
    """Change the number of plots when current theory is changed
    Show/Hide the extra plot"""
    app = parent_theory.parent_dataset.parent_application
    app.viewComboBox.blockSignals(True)
    hide = not show
    if show and parent_theory.do_priority_seniority:
        #show extra figure
        app.nplots = min(app.nplot_max, app.nplots + 1)
        if parent_theory.old_views:
            app.multiviews = parent_theory.old_views
        else:
            app.multiviews[app.nplots - 1] = app.views[app.extra_view_names[0]]
        if app.viewComboBox.count() < len(app.views):
            for view_name in app.extra_view_names:
                app.viewComboBox.addItems([app.views[view_name].name,])
                app.viewComboBox.setItemData(app.viewComboBox.count() - 1, app.views[view_name].description, Qt.ToolTipRole)
        app.multiplots.reorg_fig(app.nplots)
    elif hide and parent_theory.do_priority_seniority and parent_theory.active:
        #remove extra figure
        app.nplots = max(1, app.nplots - 1)
        app.multiplots.reorg_fig(app.nplots)
        parent_theory.old_views = [v for v in app.multiviews]
        new_multiviews = [v for v in app.multiviews]
        
        current_view_name = app.viewComboBox.currentText()
        for i, view in enumerate(app.multiviews):
            # remove extra view names from viewcombobox
            if view.name in app.extra_view_names:
                new_multiviews[i] = app.views[app.viewComboBox.itemText(i)]
                if view.name == current_view_name:
                    app.current_view = new_multiviews[i]
                    app.viewComboBox.setCurrentIndex(i)
                    current_view_name = ''

        app.multiviews = [v for v in new_multiviews]
        if app.viewComboBox.count() == len(app.views):
            for _ in range(len(app.extra_view_names)):
                app.viewComboBox.removeItem(app.viewComboBox.count() - 1)
    app.viewComboBox.blockSignals(False)

def theory_buttons_disabled(parent_theory, state):
    """
    Enable/Disable theory buttons, typically called at the start and stop of a calculation.
    This is relevant in multithread mode only.
    """
    parent_theory.bob_settings_button.setDisabled(state)
    parent_theory.save_bob_configuration_button.setDisabled(state)

def handle_save_mix_configuration(parent_theory):
    """
    Launch a dialog to select a filename where to save the polymer configurations.
    Then call the C routine 'multipolyconfwrite' that the data into the selected file
    """
    if not parent_theory.calcexists:
        msg = "<font color=green><b>No simulation performed yet. Press \"Calculate\"</b></font>"
        parent_theory.Qprint(msg)
        return

    dist_state_check = False
    for i in range(parent_theory.n_inmix):
        dist = parent_theory.dists[i]
        dist_state_check = dist_state_check or (
            parent_theory.theory_simnumber[i] !=
            rch.react_dist[dist].contents.simnumber)
    if dist_state_check:
        message = 'Simulations have changed since last calculation. Redo calculation first'
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Error")
        msgbox.setText(message)
        msgbox.exec_()
        return

    dialog = EditMixSaveParamDialog(parent_theory)
    if not dialog.exec_():
        return

    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    dir_start = "data/React/multipolyconf.dat"
    dilogue_name = "Save"
    ext_filter = "Data Files (*.dat)"
    out_file = QFileDialog.getSaveFileName(
        parent_theory, dilogue_name, dir_start, options=options)
    if out_file[0] == "":
        parent_theory.Qprint('Invalid filename')
        return
    # output polymers
    b_out_file = out_file[0].encode('utf-8')

    c_weights = (ct.c_double * parent_theory.n_inmix)()
    c_dists = (ct.c_int * parent_theory.n_inmix)()
    for i in range(parent_theory.n_inmix):
        c_weights[i] = ct.c_double(float(parent_theory.weights[i]))
        c_dists[i] = ct.c_int(int(parent_theory.dists[i]))
    n_out = rch.multipolyconfwrite(
        ct.c_char_p(b_out_file), c_weights, c_dists,
        ct.c_int(parent_theory.n_inmix))

    message = "<hr>Saved %d polymers in %s" % (n_out, out_file[0])
    parent_theory.Qprint(message)


def handle_save_bob_configuration(parent_theory):
    """
    Launch a dialog to select a filename where to save the polymer configurations.
    Then call the C routine 'polyconfwrite' that the data into the selected file
    """
    if parent_theory.simexists:
        ndist = parent_theory.ndist
        rch.react_dist[ndist].contents.M_e = parent_theory.parameters[
            'Me'].value
        rch.react_dist[ndist].contents.monmass = parent_theory.parameters[
            'mon_mass'].value

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_start = "data/React/polyconf.dat"
        dilogue_name = "Save"
        ext_filter = "Data Files (*.dat)"
        out_file = QFileDialog.getSaveFileName(
            parent_theory, dilogue_name, dir_start, options=options)
        if out_file[0] == "":
            return
        # output polymers
        b_out_file = out_file[0].encode('utf-8')
        rch.polyconfwrite(ct.c_int(ndist), ct.c_char_p(b_out_file))
        message = "<hr>Saved %d polymers in %s" % (
            rch.react_dist[ndist].contents.nsaved, out_file[0])
    else:
        message = "<font color=green><b>No simulation performed yet. Press \"Calculate\"</b></font>"
    parent_theory.Qprint(message)


def handle_edit_bob_settings(parent_theory):
    """Launch a dialog and modify the BoB binning settings if the user press "OK", else nothing happend."""
    if parent_theory.simexists:
        ndist = parent_theory.ndist
        numbobbins = rch.react_dist[ndist].contents.numbobbins
        bobmax = np.power(10, rch.react_dist[ndist].contents.boblgmax)
        bobmin = np.power(10, rch.react_dist[ndist].contents.boblgmin)
        bobbinmax = rch.react_dist[ndist].contents.bobbinmax

        d = EditBobSettingsDialog(parent_theory, numbobbins, bobmax, bobmin,
                                bobbinmax)
        if d.exec_():
            try:
                numbobbins = int(d.e1.text())
                bobmax = float(d.e2.text())
                bobmin = float(d.e3.text())
                bobbinmax = int(d.e4.text())
            except ValueError:
                pass
            rch.react_dist[ndist].contents.numbobbins = ct.c_int(numbobbins)
            rch.react_dist[ndist].contents.boblgmax = ct.c_double(np.log10(bobmax))
            rch.react_dist[ndist].contents.boblgmin = ct.c_double(np.log10(bobmin))
            rch.react_dist[ndist].contents.bobbinmax = ct.c_int(bobbinmax)
    else:
        message = "<font color=green><b>No simulation performed yet. Press \"Calculate\"</b></font>"
        parent_theory.Qprint(message)



def handle_increase_records(parent_theory, name):
    """Launch a dialog asking if the user what to allocate more memory for arms, polymers, or distribution.
        'name' should be "arm", "polymer", or "dist".
        Return the new max value or zero if max value not changed
    """
    if name == "arm":
        current_max = rch.pb_global_const.maxarm
        f = rch.increase_arm_records_in_arm_pool
        size_of = 75e-6  #size of an 'arm' structure (MB) in C
    elif name == "polymer":
        current_max = rch.pb_global_const.maxpol
        f = rch.increase_polymer_records_in_br_poly
        size_of = 45e-6  #size of a 'polymer' structure (MB) in C
    elif name == "dist":
        current_max = rch.pb_global_const.maxreact
        f = rch.increase_dist_records_in_react_dist
        size_of = 60097e-6  #size of a 'dist' structure (MB) in C
    else:
        return 0, False
    d = IncreaseRecordsDialog(parent_theory, current_max, name,
                              size_of)  #create the dialog
    if d.exec_():
        if d.r1.isChecked():
            new_max = int(np.ceil(current_max * 1.5))
        if d.r2.isChecked():
            new_max = int(current_max * 2)
        if d.r3.isChecked():
            new_max = int(current_max * 5)
        success = f(
            ct.c_int(new_max)
        )  #call C routine to allocate more memory (using 'realloc')
        if not success:
            parent_theory.Qprint(
                "Allocation of new memory failed. %d %s records in memory" %
                (current_max, name))
        return new_max, success
    else:
        return 0, False


###################


class ParameterReactMix(QDialog):
    """Create form to input the Mix parameters"""

    def __init__(self, parent_theory):
        super().__init__(parent_theory)
        self.parent_theory = parent_theory
        self.opened_react_theories = []
        self.list_all_open_react_theories()
        self.make_lines()
        self.createFormGroupBox(self.opened_react_theories)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Apply
                                     | QDialogButtonBox.Ok
                                     | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept_)
        buttonBox.rejected.connect(self.reject)
        apply_button = buttonBox.button(QDialogButtonBox.Apply)
        apply_button.clicked.connect(self.handle_apply)

        #insert widgets
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.scroll)
        self.mainLayout.addWidget(buttonBox)
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Enter Mix Parameters")

    def accept_(self):
        """
        Triggered when 'OK' button is pushed. Call 'get_lines()'
        
        """
        self.compute_weights()
        self.get_lines()
        self.accept()

    def compute_weights(self):
        """Update the 'weight' column based on the 'ratio' values"""
        sum_ratio = 0
        self.parent_theory.ratios = [] 
        self.parent_theory.include = [] 
        for i in range(len(self.opened_react_theories)):
            # IF 'is included?' is checked and Ratio > 0
            is_checked = self.lines[i][3].isChecked()
            ratio = float(self.lines[i][4].text())
            self.parent_theory.ratios.append(ratio)
            self.parent_theory.include.append(int(is_checked))
            if is_checked and ratio > 0:
                sum_ratio += ratio

        for i in range(len(self.opened_react_theories)):
            is_checked = self.lines[i][3].isChecked()
            ratio = float(self.lines[i][4].text())
            if is_checked and ratio > 0:
                weight = ratio / sum_ratio
                self.lines[i][5].setText('%.7g' % weight)
            else:
                self.lines[i][3].setChecked(False)
                self.lines[i][5].setText('0')

    def handle_apply(self):
        """
        Update the values of 'is checked?' and 'weight' columns.
        Triggered when 'Apply' button is pushed.
        
        """
        self.compute_weights()

    def make_lines(self):
        """Create the input-parameter-form lines with default parameter values"""
        dvalidator = QDoubleValidator()  #prevent letters etc.
        dvalidator.setBottom(0)  #minimum allowed value
        self.lines = []
        for i, th in enumerate(self.opened_react_theories):
            line = []
            ndist = th.ndist
            ds = th.parent_dataset
            app = ds.parent_application
            manager = app.parent_manager

            #find application tab-name
            app_index = manager.ApplicationtabWidget.indexOf(app)
            app_tab_name = manager.ApplicationtabWidget.tabText(app_index)
            #find dataset tab-name
            ds_index = app.DataSettabWidget.indexOf(ds)
            ds_tab_name = app.DataSettabWidget.tabText(ds_index)
            #find theory tab-name
            th_index = ds.TheorytabWidget.indexOf(th)
            th_tab_name = ds.TheorytabWidget.tabText(th_index)

            label = QLabel('%s/%s/%s' % (app_tab_name, ds_tab_name,
                                         th_tab_name))
            label.setWordWrap(True)
            line.append(label)
            line.append(QLabel(
                '%.4g' % rch.react_dist[ndist].contents.npoly))  #no. generated
            line.append(
                QLabel('%.4g' %
                       rch.react_dist[ndist].contents.nsaved))  #no. saved
            checkbox = QCheckBox()
            try:
                checkbox.setChecked(bool(self.parent_theory.include[i]))
            except IndexError:
                checkbox.setChecked(True)
            line.append(checkbox)  #is included? - checked by default
            qledit = QLineEdit()
            qledit.setValidator(dvalidator)
            try:
                qledit.setText('%s' % self.parent_theory.ratios[i])
            except IndexError:
                qledit.setText('1')
            line.append(qledit)  #ratio
            line.append(QLabel('-'))  #weight
            self.lines.append(line)

    def get_lines(self):
        """Called when 'OK' is pressed"""
        self.parent_theory.dists = []
        self.parent_theory.weights = []
        self.parent_theory.theory_names = []
        self.parent_theory.theory_simnumber = []

        for i in range(len(self.opened_react_theories)):
            if self.lines[i][3].isChecked():
                ndist = self.opened_react_theories[i].ndist
                self.parent_theory.dists.append(ndist)  #get ndist
                self.parent_theory.weights.append(
                    self.lines[i][5].text())  #get weight
                self.parent_theory.theory_names.append(
                    self.lines[i][0].text())  #get theory name
                simnumber = rch.react_dist[ndist].contents.simnumber
                self.parent_theory.theory_simnumber.append(
                    simnumber)  #get theory simulation number
        self.parent_theory.n_inmix = len(
            self.parent_theory.weights
        )  #get number of included theories in mix

    def createFormGroupBox(self, theory_list):
        """Create a form to set the new values of mix parameters"""
        inner = QWidget()
        layout = QGridLayout()
        layout.setSpacing(10)

        label = QLabel('<b>App/Dataset/Theory</b>')
        label.setWordWrap(True)
        layout.addWidget(label, 0, 1)

        label = QLabel('<b>No. generated</b>')
        label.setWordWrap(True)
        layout.addWidget(label, 0, 2)

        label = QLabel('<b>No. saved</b>')
        label.setWordWrap(True)
        layout.addWidget(label, 0, 3)

        label = QLabel('<b>Include?<</b>')
        label.setWordWrap(True)
        layout.addWidget(label, 0, 4)

        label = QLabel('<b>Ratio<</b>')
        label.setWordWrap(True)
        layout.addWidget(label, 0, 5)

        label = QLabel('<b>Weight fraction<</b>')
        label.setWordWrap(True)
        layout.addWidget(label, 0, 6)

        for i in range(len(theory_list)):
            layout.addWidget(QLabel('<b>%d</b>' % (i + 1)), i + 1, 0)
            for j in range(len(self.lines[0])):
                layout.addWidget(self.lines[i][j], i + 1, j + 1)
        inner.setLayout(layout)

        #Scroll Area Properties
        self.scroll = QScrollArea()
        self.scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(inner)

    def list_all_open_react_theories(self):
        """List all opened React theories in RepTate, excluding the Mix theories"""
        self.opened_react_theories = []
        current_manager = self.parent_theory.parent_dataset.parent_application.parent_manager

        for app in current_manager.applications.values():  
        #list all opened apps
            if app.appname == 'React':  
                #select only React application
                for ds in app.datasets.values():  #loop over datasets
                    for th in ds.theories.values():  #loop over theories
                        if th.reactname not in ['ReactMix', 'CreatePolyconf'] and th.simexists:  # exclude React Mix and CreatePolyconf theories
                            self.opened_react_theories.append(th)


###################


class EditMixSaveParamDialog(QDialog):
    """Create the form used to set distribution parameters of mix when saving"""

    def __init__(self, parent_theory):
        super().__init__(parent_theory)
        self.parent_theory = parent_theory
        self.createFormGroupBox(parent_theory)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok
                                     | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept_)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.scroll)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle('Distribution parameters check')

    def accept_(self):
        self.get_lines()
        self.accept()

    def get_lines(self):
        for i, dist in enumerate(
                self.parent_theory.dists):  #loop over the distributions in mix
            monmass = float(self.lines[i][1].text())
            Me = float(self.lines[i][2].text())
            rch.set_react_dist_monmass(ct.c_int(dist), ct.c_double(monmass))
            rch.set_react_dist_M_e(ct.c_int(dist), ct.c_double(Me))

    def createFormGroupBox(self, parent_theory):
        """Create a form to set the new values of the parameters"""

        inner = QWidget()
        layout = QGridLayout()
        layout.setSpacing(10)

        vlayout = QVBoxLayout()
        qmessage = QLabel(
            '<p>Please check the values of monomer mass and Me used for each distribution in the mix.</p>\
<p>Note that BoB is not yet able to deal with mixtures of polymers with different Me.</p>'
        )
        qmessage.setWordWrap(True)
        vlayout.addWidget(qmessage)
        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        vlayout.addWidget(hline)
        layout.addLayout(vlayout, 0, 0, 1, -1)  #span all the columns

        layout.addWidget(QLabel('<b>App/Theory</b>'), 1, 1)
        layout.addWidget(QLabel('<b>Monomer Mass</b>'), 1, 2)
        label = QLabel('<b>M<sub>e</sub></b>')
        label.setMinimumWidth(
            100)  # prevent too small size of the QLineEdit when resizing
        layout.addWidget(label, 1, 3)

        self.lines = []
        dvalidator = QDoubleValidator()  #prevent letters etc.
        dvalidator.setBottom(0)  #minimum allowed value
        for i, dist in enumerate(
                parent_theory.dists):  #loop over the distributions in mix
            layout.addWidget(QLabel('<b>%d</b>' % (i + 1)), i + 2, 0)
            line = []

            line.append(QLabel(parent_theory.theory_names[i]))

            qline = QLineEdit()
            qline.setValidator(dvalidator)
            qline.setText("%.4g" % rch.react_dist[dist].contents.monmass)
            line.append(qline)

            qline = QLineEdit()
            qline.setValidator(dvalidator)
            qline.setText("%.4g" % rch.react_dist[dist].contents.M_e)
            line.append(qline)

            self.lines.append(line)  #save lines
            for j in range(3):
                layout.addWidget(self.lines[i][j], i + 2, j + 1)
        inner.setLayout(layout)

        #Scroll Area Properties
        self.scroll = QScrollArea()
        # self.scroll.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(inner)


###########################


class ParameterMultiMetCSTR(QDialog):
    """Create form to input the MultiMetCSTR parameters"""

    def __init__(self, parent_theory):
        super().__init__(parent_theory)
        self.parent_theory = parent_theory
        self.NUMCAT_MAX = parent_theory.NUMCAT_MAX  #maximum number of catalysts
        self.make_lines(parent_theory.pvalues)
        self.createFormGroupBox(parent_theory.numcat)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok
                                     | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept_)
        buttonBox.rejected.connect(self.reject)

        hwidget = QWidget()
        hlayout = QHBoxLayout()
        #set spinBox ncatalyst
        hlayout.addWidget(QLabel('<b>No. of catalysts</b>'))
        self.sb_ncatalyst = QSpinBox()
        self.sb_ncatalyst.setMinimum(1)
        self.sb_ncatalyst.setMaximum(self.NUMCAT_MAX)
        self.sb_ncatalyst.setValue(parent_theory.numcat)
        self.sb_ncatalyst.valueChanged.connect(
            self.handle_sb_ncatalyst_valueChanged)
        hlayout.addWidget(self.sb_ncatalyst)
        #set time const box
        hlayout.addStretch()
        hlayout.addWidget(QLabel('<b>Time constant</b>'))
        dvalidator = QDoubleValidator()  #prevent letters etc.
        dvalidator.setBottom(0)  #minimum allowed value
        self.time_const = QLineEdit()
        self.time_const.setValidator(dvalidator)
        self.time_const.setText('%s' % parent_theory.time_const)
        hlayout.addWidget(self.time_const)
        #set monomer concentration box
        hlayout.addStretch()
        hlayout.addWidget(QLabel('<b>Monomer conc.</b>'))
        dvalidator = QDoubleValidator()  #prevent letters etc.
        dvalidator.setBottom(0)  #minimum allowed value
        self.monomer_conc = QLineEdit()
        self.monomer_conc.setValidator(dvalidator)
        self.monomer_conc.setText('%s' % parent_theory.monomer_conc)
        hlayout.addWidget(self.monomer_conc)
        #set horizontal layout
        hwidget.setLayout(hlayout)

        #insert widgets
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(hwidget)
        self.mainLayout.addWidget(self.scroll)
        self.mainLayout.addStretch()
        self.mainLayout.addWidget(buttonBox)
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Enter Metallocene Polymerisation Parameters")

    def accept_(self):
        """
        Triggered when 'OK' button is pushed. Call 'get_lines()'
        
        """
        self.get_lines()
        self.accept()

    def make_lines(self, source):
        """Create the input-parameter-form lines with default parameter values"""
        dvalidator = QDoubleValidator()  #prevent letters etc.
        dvalidator.setBottom(0)  #minimum allowed value
        qledit = QLineEdit()
        qledit.setValidator(dvalidator)
        qledit.setText('0.0')  #new lines contain zeros
        self.lines = []
        for i in range(self.NUMCAT_MAX):
            line = []
            for j in range(5):
                qledit = QLineEdit()
                qledit.setValidator(dvalidator)
                qledit.setText(source[i][j])
                line.append(qledit)
            self.lines.append(line)

    def save_lines(self):
        """Save the current form values.
        Called when the number of lines in the form is changed.
        """
        self.lines_saved = [['0' for j in range(5)]
                            for i in range(self.NUMCAT_MAX)]
        for i in range(self.NUMCAT_MAX):
            for j in range(5):
                self.lines_saved[i][j] = self.lines[i][j].text()

    def get_lines(self):
        """Save input parameters. Called when 'OK' is pressed"""
        self.parent_theory.numcat = self.sb_ncatalyst.value()
        self.parent_theory.time_const = float(self.time_const.text())
        self.parent_theory.monomer_conc = float(self.monomer_conc.text())
        for i in range(self.NUMCAT_MAX):
            for j in range(5):
                self.parent_theory.pvalues[i][j] = self.lines[i][j].text()

    def handle_sb_ncatalyst_valueChanged(self, ncatalyst):
        """Handle a change of the number of catalysts.
        Destroy the form and create new one with the selected number of line
        Keep the values previously entered
        """
        self.save_lines()
        self.mainLayout.removeWidget(self.scroll)
        self.scroll.deleteLater()
        self.scroll = None
        self.make_lines(self.lines_saved)
        self.createFormGroupBox(ncatalyst)
        self.mainLayout.insertWidget(
            1, self.scroll)  #insert above OK/Cancel buttons

    def createFormGroupBox(self, ncatalyst):
        """Create a form to set the new values of polymerisation parameters"""
        inner = QWidget()

        layout = QGridLayout()
        layout.setSpacing(10)

        layout.addWidget(
            QLabel('<center><b>Catalyst conc.</center></b>'), 0, 1)
        layout.addWidget(QLabel('<center><b>K<sub>p</sub></b></center>'), 0, 2)
        layout.addWidget(QLabel('<center><b>K<sup>=</sup></b></center>'), 0, 3)
        layout.addWidget(QLabel('<center><b>K<sup>s</sup></b></center>'), 0, 4)
        layout.addWidget(
            QLabel('<center><b>K<sub>pLCB</sub></b></center>'), 0, 5)
        for i in range(ncatalyst):
            layout.addWidget(QLabel('<b>%d</b>' % (i + 1)), i + 1, 0)
            for j in range(5):
                layout.addWidget(self.lines[i][j], i + 1, j + 1)
        inner.setLayout(layout)

        #Scroll Area Properties
        self.scroll = QScrollArea()
        self.scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(inner)


###############################################


class EditBobSettingsDialog(QDialog):
    """Create the form that is used to modify the BoB binning settings"""

    def __init__(self, parent_theory, numbobbins, bobmax, bobmin, bobbinmax):
        super().__init__(parent_theory)
        self.createFormGroupBox(numbobbins, bobmax, bobmin, bobbinmax)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok
                                     | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("Edit")

    def createFormGroupBox(self, numbobbins, bobmax, bobmin, bobbinmax):
        """Create a form to set the new values of the BoB binning parameters"""
        self.formGroupBox = QGroupBox("Edit BoB Binning Settings")
        layout = QFormLayout()

        val_double = QDoubleValidator()
        val_double.setBottom(1)  #set smalled double allowed in the form
        val_int = QIntValidator()
        val_int.setBottom(0)  #set smalled int allowed in the form
        val_int.setTop(rch.pb_global_const.maxbobbins
                       )  #set largest int allowed in the form

        self.e1 = QLineEdit()
        self.e1.setValidator(val_int)
        self.e1.setMaxLength(6)
        self.e1.setText("%d" % numbobbins)

        self.e2 = QLineEdit()
        self.e2.setValidator(val_double)
        self.e2.setText("%.2e" % bobmax)

        self.e3 = QLineEdit()
        self.e3.setValidator(val_double)
        self.e3.setText("%.2e" % bobmin)

        self.e4 = QLineEdit()
        self.e4.setValidator(val_int)
        self.e4.setMaxLength(6)
        self.e4.setText("%d" % bobbinmax)

        layout.addRow(QLabel("Number of bins for Bob:"), self.e1)
        layout.addRow(QLabel("Maximum bin Mw (g/mol):"), self.e2)
        layout.addRow(QLabel("Minimum bin Mw (g/mol):"), self.e3)
        layout.addRow(QLabel("Maximum no. of polymers per bin:"), self.e4)
        self.formGroupBox.setLayout(layout)


###########################


class IncreaseRecordsDialog(QDialog):
    """
    Dialog containing radio buttons to choose a new memory size for the records of "name" 
    """

    def __init__(self, parent_theory, current_max, name, size_of):
        super().__init__()
        self.createExclusiveGroup(current_max, name, size_of)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok
                                     | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("More %s records?" % name)

    def createExclusiveGroup(self, current_max, name, size_of):
        """Create the radio buttons choices"""
        self.formGroupBox = QWidget()
        size = int(size_of * np.ceil(0.5 * current_max))
        if size < 1:
            size = 1
            char = '<'
        else:
            char = ''
        self.r1 = QRadioButton("%.4g (1.5x) requests %s%dMB of RAM" %
                               (np.ceil(1.5 * current_max), char, size))
        size = int(size_of * current_max)
        if size < 1:
            size = 1
            char = '<'
        else:
            char = ''
        self.r2 = QRadioButton("%.4g (2x) requests %s%dMB of RAM" %
                               (2 * current_max, char, size))
        size = int(size_of * 4 * current_max)
        if size < 1:
            size = 1
            char = '<'
        else:
            char = ''
        self.r3 = QRadioButton("%.4g (5x) requests %s%dMB of RAM" %
                               (5 * current_max, char, size))
        self.r1.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(
            QLabel('<b>Current number of %s records: %.4g</b>' %
                   (name, current_max)))
        layout.addWidget(QLabel('Increase to:'))
        layout.addWidget(self.r1)
        layout.addWidget(self.r2)
        layout.addWidget(self.r3)
        layout.addWidget(
            QLabel("(%dMB of RAM available)" %
                   (psutil.virtual_memory()[1] / 2.**20
                    )))  # size of free RAM avaliable
        layout.addWidget(QLabel("Or press Cancel."))
        self.formGroupBox.setLayout(layout)
