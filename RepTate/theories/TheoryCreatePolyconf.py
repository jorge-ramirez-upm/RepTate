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
"""Module TheoryCreatePolyconf

CreatePolyconf file for creating a polymer configuration file using BoB version 2.5
by Chinmay Das et al.
"""
import os
import numpy as np
from CmdBase import CmdBase, CmdMode
from enum import Enum
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from collections import OrderedDict
import time

import bob_gen_poly  # dialog
import ctypes
from BobCtypesHelper import BobCtypesHelper, BobError
from PyQt5.QtWidgets import QDialog, QFormLayout, QWidget, QLineEdit, QLabel, QComboBox, QDialogButtonBox, QFileDialog, QMessageBox, QTextEdit, QApplication, QToolBar
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QDesktopServices, QIcon
from PyQt5.QtCore import QUrl, pyqtSignal, QSize, Qt, QVariant
from shutil import copy2


class DistributionType(Enum):
    """Type of molecular weight distribution"""
    Monodisperse = 0
    Gaussian = 1
    LogNormal = 2
    Poisson = 3
    Flory = 4


class ArchitectureType(Enum):
    """Type of polymer architecture and expected parameters as input for BoB"""

    Linear = {'name': "Linear Polymer", 'def': [0, 'Distr.', 'Mw (g/mol)', 'PDI'], 'descr': "Linear polymer"}
    Star = {'name': "Star Polymer", 'def': [1, 'Distr.', 'Mw (g/mol)', 'PDI', '', 'Num. arm'], 'descr': "Star polymer"}
    AsymStar = {'name': "Asymetric Star", 'def': [
        2, 'Distr. long', 'Mw long (g/mol)', 'PDI long', '', 'Distr. short',
        'Mw short', 'PDI short'
    ], 'descr': "Star with two arms of equal length and the third arm having a different length. Only 3 arm stars are created"}
    H = {'name': "H Polymer", 'def': [
        3, 'Distr. side', 'Mw side (g/mol)', 'PDI side', '', 'Distr. cross',
        'Mw cross', 'PDI cross'
    ], 'descr': "H polymers have one cross-bar and four segments attached to the crossbar"}
    PoissComb = {'name': "Poisson Comb", 'def': [
        4, 'Distr. backbone', 'Mw backbone (g/mol)', 'PDI backbone', '',
        'Distr. side', 'Mw side (g/mol)', 'PDI side', '', 'Num. arm'
    ], 'descr': "Comb having Poisson distr.ributed number of side arms connected at random places on the backbone"}
    FixComb = {'name': "Fixed Comb", 'def': [
        5, 'Distr. backbone', 'Mw backbone (g/mol)', 'PDI backbone', '',
        'Distr. side', 'Mw side (g/mol)', 'PDI side', '', 'Num. arm'
    ], 'descr': "Comb having fixed number of side arms connected at random places on the backbone"}
    CouplComb = {'name': "Coupled Comb", 'def': [
        6, 'Distr. backbone', 'Mw backbone (g/mol)', 'PDI backbone', '',
        'Distr. side', 'Mw side (g/mol)', 'PDI side', '', 'Num. arm'
    ], 'descr': "Attach two \"Poisson combs\" at some random point along the two backbones"}
    ##########################
    #Caylay type is handled in a special way. The strings below are not actually used.
    Cayley3Arm = {'name': "Cayley 3-arm Core", 'def': [
        10, 'Num. generation', '', 'Distr. gen0', 'Mw gen0 (g/mol)', 'PDI gen0'
    ], 'descr': "Cayley trees with 3 arm star inner core"}
    CayleyLin = {'name': "Cayley Linear Core", 'def': [
        11, 'Num. generation', '', 'Distr. gen0', 'Mw gen0 (g/mol)', 'PDI gen0'
    ], 'descr': "Cayley trees with linear inner core"}
    Cayley4Arm = {'name': "Cayley 4-arm Core", 'def': [
        12, 'Num. generation', '', 'Distr. gen0', 'Mw gen0 (g/mol)', 'PDI gen0'
    ], 'descr': "Cayley trees with 4 arm star inner core"}
    ###########################
    MpeNum = {'name': "MPE num-average", 'def': [20, 'Mw (g/mol)', 'Branch/molecule'], 'descr': "Metallocene catalyzed polyethylene with number-based sampling"}
    MpeWt = {'name': "MPE weight-average", 'def': [21, 'Mw (g/mol)', 'Branch/molecule'], 'descr': "Metallocene catalyzed polyethylene with weight-based sampling"}
    Gel = {'name': "Gel", 'def': [25, 'Mn (g/mol)', 'Up Branch. proba.'], 'descr': "Gelation ensemble"}
    Proto = {'name': "Prototype", 'def': [40, 'Go to "Result" tab'], 'descr': "Polymer prototype from file (user defined)"}
    FromFile = {'name': "From File", 'def': [60, 'From file'], 'descr': "User supplied pre-generated polymers file"}


class TheoryCreatePolyconf(CmdBase):
    """Create polymer configuration files using BoB v2.5 (Chinmay Das and Daniel Read).
    The configuration file created with this theory can then be analysed
    in the BoB LVE theory, in the LVE application of RepTate.

    The original documentation of BoB can be found here: `<https://sourceforge.net/projects/bob-rheology/files/bob-rheology/bob2.3/bob2.3.pdf/download>`_.
    
    * **Parameters**
       - ``M0`` : Mass of a Monomer
       - ``Ne`` : Number of monomers in an entanglement length
       - ``Ratio`` : Ratio weight fraction occupied by component
       - ``Architecture`` : Polymer architecture type (e.g. Linear, Star, Comb, etc.)
       - ``Num. of polymer`` : Number of polymers to generate of the above architecture type
       - ``Num. generations`` : Number of generations (for Cayley architecture type only)
       - ``Distr.`` : Molecular weight distribution (e.g. Monodisperse, LogNormal, etc.)
       - ``Mw`` : Weight-average molecular weight
       - ``PDI`` : Polydispersity index (PDI :math:`=M_w/M_n`)
    """
    thname = 'BOB Architecture'
    description = 'Create and Save Polymer Configuration with BOB'
    citations = ['Das C. et al, J. Rheol. 2006, 50, 207-234']
    doi = ["http://dx.doi.org/10.1122/1.2167487"]

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
        return GUITheoryCreatePolyconf(name, parent_dataset, axarr) if (
            CmdBase.mode == CmdMode.GUI) else CLTheoryCreatePolyconf(
                name, parent_dataset, axarr)


class BaseTheoryCreatePolyconf:
    """[summary]
    
    [description]
    """
    help_file = 'https://reptate.readthedocs.io/manual/Applications/React/Theory/BoB_polyconf.html'
    single_file = True  # False if the theory can be applied to multiple files simultaneously
    thname = TheoryCreatePolyconf.thname
    citations = TheoryCreatePolyconf.citations
    doi = TheoryCreatePolyconf.doi

    signal_param_dialog = pyqtSignal(object)

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.reactname = "CreatePolyconf"
        self.function = self.calculate  # main theory function
        self.has_modes = False  # True if the theory has modes
        self.signal_param_dialog.connect(self.launch_param_dialog)
        self.parameters["nbin"] = Parameter(
            name="nbin",
            value=50,
            description="Number of molecular weight bins",
            type=ParameterType.integer,
            opt_type=OptType.const,
            min_value=1)
        self.polyconf_file_out = None  # full path of target polyconf file
        self.autocalculate = False
        self.bch = BobCtypesHelper(self)
        self.do_priority_seniority = False
        self.inp_counter = 0 # counter for the 'virtual' input file for BoB
        self.virtual_input_file = [] # 'virtual' input file for BoB
        self.proto_counter = 0 # counter for the 'virtual' proto file for BoB
        self.virtual_proto_file = [] # 'virtual' proto file for BoB
        self.from_file_filename = [] # file names of the "from file" type
        self.from_file_filename_counter = 0 # counter
        self.protoname = [] # list of proto/polycode names

    def request_stop_computations(self):
        """Called when user wants to terminate the current computation"""
        self.Qprint('<font color=red><b>Stop current calculation requested</b></font>')
        self.bch.set_flag_stop_bob(ctypes.c_bool(True))

    def do_error(self, line=""):
        """This theory does not calculate the error"""
        pass

    def calculate(self, f=None):
        """Create polymer configuration file and calculate distribution characteristics"""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        #show form
        self.success_dialog = None
        self.signal_param_dialog.emit(self)
        while self.success_dialog is None:  # wait for the end of QDialog
            time.sleep(
                0.5
            )  # TODO: find a better way to wait for the dialog thread to finish
        if not self.success_dialog:
            self.Qprint('Operation cancelled')
            return

        # Run BoB C++ code
        gpc_out = []
        QApplication.processEvents()
        self.bch.link_c_callback()
        self.bch.set_do_priority_seniority(ctypes.c_bool(self.do_priority_seniority))
        self.start_time_cal = time.time()
        try:
            mn, mw, gpc_out = self.bch.save_polyconf_and_return_gpc(
            self.argv, self.npol_tot)
        except BobError:
            self.Qprint('Operation cancelled')
            return

        #copy results to RepTate data file
        if gpc_out:
            if not self.is_ascii(self.polyconf_file_out):
                pass
                # #copy file to selected loaction
                # temp_polyconf = os.path.join('theories', 'temp',
                #                              'temp_polyconf.dat')
                # copy2(temp_polyconf, self.polyconf_file_out)

            try:
                self.Qprint("<br><b>Mn=%.3g, Mw=%.3g, PDI=%.3g</b>" % (mn, mw, mw / mn))
            except ZeroDivisionError:
                self.Qprint("<br><b>Mn=%.3g, Mw=%.3g</b>" % (mn, mw))
            self.Qprint("<br><b>Polymer configuration written in</b><i>\"%s\"</i><br>" %
                        self.polyconf_file_out)

            # copy results to data series
            lgmid_out, wtbin_out, brbin_out, gbin_out = gpc_out
            tt.num_columns = ft.num_columns
            tt.num_rows = len(lgmid_out)
            tt.data = np.zeros((tt.num_rows, tt.num_columns))
            tt.data[:, 0] = lgmid_out[:]
            tt.data[:, 1] = wtbin_out[:]
            tt.data[:, 2] = gbin_out[:]
            tt.data[:, 3] = brbin_out[:]


class CLTheoryCreatePolyconf(BaseTheoryCreatePolyconf, Theory):
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


class GUITheoryCreatePolyconf(BaseTheoryCreatePolyconf, QTheory):
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
        self.ncomponent = 1
        self.trash_indices = []
        self.dict_component = OrderedDict()
        self.setup_dialog()
        self.flag_prototype = 0

        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        self.btn_prio_senio = tb.addAction(QIcon(':/Icon8/Images/new_icons/priority_seniority.png'), 'Calculate Priority and Seniority (can take some time)')
        self.btn_prio_senio.setCheckable(True)
        self.btn_prio_senio.setChecked(self.do_priority_seniority)
        self.thToolsLayout.insertWidget(0, tb)

        self.btn_prio_senio.triggered.connect(self.handle_btn_prio_senio)

    def handle_btn_prio_senio(self, checked):
        """Change do_priority_seniority"""
        self.do_priority_seniority = checked

    def setup_dialog(self):
        """Create the dialog to setup the polymer configuration"""
        # create form
        self.dialog = QDialog(self)
        self.dialog.ui = bob_gen_poly.Ui_Dialog()
        self.dialog.ui.setupUi(self.dialog)
        self.d = self.dialog.ui
        self.d.pb_pick_file.clicked.connect(self.get_file_name)
        self.d.selected_file.setStyleSheet("color : blue ;")
        self.d.polymer_tab.setTabsClosable(True)
        # connect close tab
        self.d.polymer_tab.tabCloseRequested.connect(
            self.handle_close_polymer_tab)
        # connect button Apply
        self.d.pb_apply.clicked.connect(
            self.handle_apply_button)
        # connect button Help
        self.d.pb_help.clicked.connect(
            self.handle_help_button)
        # connect button OK
        self.d.pb_ok.clicked.connect(self.handle_pb_ok)
        # connect button Cancel
        self.d.pb_cancel.clicked.connect(self.dialog.reject)
        # connect button Add component
        self.d.add_button.clicked.connect(self.handle_add_component)
        # connect combobox architecture type
        self.d.cb_type.currentTextChanged.connect(
            self.handle_architecture_type_changed)
        # fill combobox
        i = 0
        for e in ArchitectureType:
            self.d.cb_type.addItem(e.value['name'], QVariant(e.name))
            self.d.cb_type.setItemData(i, e.value['descr'], Qt.ToolTipRole)
            i += 1
        # pre-fill the prototype text box
        self.d.proto_text.append("""FunStar
3
-1 -1 1 2 0 10000 1.0
0 2 -1 -1 2 12000 1.4
0 1 -1 -1 4 18000 2.0
FunH
5
-1 -1 1 2 2 10000 1.2
-1 -1 0 2 2 12000 1.01
0 1 3 4   2 25000 1.4
2 4 -1 -1 2 11000 1.1
2 3 -1 -1 2 13000 1.05
""")

    def handle_pb_ok(self):
        """Define the OK button role. If something is wrong, keep the dialog open"""
        if self.handle_apply_button():
            self.dialog.accept()

    def handle_apply_button(self):
        """When Apply button of dialog box is clicked,
        fill the "Result" widget with the data expected by BoB"""
        if self.polyconf_file_out is None:
            QMessageBox.warning(
                self, 'Select Output Polyconf',
                'Please select a file for BoB to save the polymer configuration'
            )
            return False
        ncomponents = self.d.polymer_tab.count()
        if ncomponents < 1:
            QMessageBox.warning(
                self, 'No polymers in the mix',
                'At least one component is needed\nSelect a polymer architecture and click \"Add\"'
            )
            return False
        self.from_file_filename_counter
        self.npol_tot = 0  # total number of polymers
        tb = self.d.text_box
        vinp = [] # self.virtual_input_file
        # remove all current text
        tb.clear()

        #1 memory line
        tb.append("%d %d" % (float(self.d.n_polymers.text()),
                             float(self.d.n_segments.text())))
        vinp.append(float(self.d.n_polymers.text()))
        vinp.append(float(self.d.n_segments.text()))
        #2 alpha (not used)
        tb.append("1.0")
        vinp.append(1.0)
        #3 "1" for BoB 'compatibility'
        tb.append("1")
        vinp.append(1)
        #4 M0, Ne, (density not used)
        tb.append("%.6g %.6g 0" % (float(self.d.m0.text()),
                               float(self.d.ne.text())))
        vinp.append(float(self.d.m0.text()))
        vinp.append(float(self.d.ne.text()))
        vinp.append(0)
        #5 tau_e, T (not used)
        tb.append("0 0")
        vinp.append(0)
        vinp.append(0)
        #6 number of component(s) in blend
        tb.append("%d" % len(self.dict_component))
        vinp.append(len(self.dict_component))

        #7.. the rest of the lines is specific to the architecture
        tot_ratio = self.sum_ratios(
        )  # summ all components ratios to define weights

        for pol_dict in self.dict_component.values():
            pol_type_list = ArchitectureType[pol_dict[
                "type"]].value['def']  # architecture type value
            #8.. weight
            try:
                w = float(pol_dict["Ratio"].text()) / tot_ratio
            except:
                w = "ERROR"
            tb.append("%.6g" % w)
            vinp.append(w)
            #9.. num. polymer and type
            # float -> int conversion needed for e.g. "1e6"
            npol = int(float(pol_dict["Num. of polymers"].text()))
            type_number = pol_type_list[0]
            tb.append("%d %d" % (npol, type_number))
            vinp.append(npol)
            vinp.append(type_number)
            self.npol_tot += npol

            if type_number in [10, 11, 12]:
                # Cayley tree type: handle varible number of generations
                ngen = pol_dict["Num. generation"]
                text = "%s\n" % ngen
                vinp.append(ngen)
                for i in range(ngen + 1):
                    text += self.poly_param_text(pol_dict, "Distr. gen%d" % i)
                    vinp.append(self.poly_param_text(pol_dict, "Distr. gen%d" % i))
                    text += self.poly_param_text(pol_dict,
                                                 "Mw gen%d (g/mol)" % i)
                    vinp.append(self.poly_param_text(pol_dict, "Mw gen%d (g/mol)" % i))
                    text += self.poly_param_text(
                        pol_dict, "PDI gen%d" %
                        i).rstrip()  # remove whitespace on right side
                    vinp.append(self.poly_param_text(pol_dict, "PDI gen%d" %i))
                    if i < ngen:
                        text += "\n"
            elif type_number == 40:
                #prototype polymer
                continue
            else:
                text = ""
                for attr in pol_type_list[
                        1:]:  # go over all attributes of the architecture type
                    text += self.poly_param_text(pol_dict, attr)
                    vinp.append(self.poly_param_text(pol_dict, attr))
                if type_number == 60:
                    # from file: remove the sting from virtual file
                    self.from_file_filename.append(vinp[-1])
                    vinp = vinp[:-1]
            text = text.rstrip()
            tb.append(text)  # remove whitespace on right side
        tb.append("\n")
        # set current tab to the Text box "result"
        self.d.tabWidget.setCurrentIndex(2)
        vinp = [float(y) for y in vinp if y != '\n']
        self.virtual_input_file = vinp
        return True

    def poly_param_text(self, pol_dict, attr):
        """Return a string containing the value of the parameter ``attr``
        or a  new line if ``attr`` is an empty string
        """
        if attr == "":
            text = "\n"
        else:
            try:
                val = pol_dict[attr].text()  # for QLineEdit (Mw, PDI, narm)
            except:
                val = DistributionType[pol_dict[
                    attr].currentText()].value  # for Dist QComboBox
            text = "%s " % val
        return text

    def sum_ratios(self):
        """Return the (float) sum of the ratio of all polymer components
        or 1 if there are none"""
        s = 0.0
        for pol_dict in self.dict_component.values():
            try:
                s += float(pol_dict["Ratio"].text())
            except ValueError:
                print("ERROR in Ratio conversion")
        if s == 0.0:
            s = 1.0
        return s

    def handle_help_button(self):
        """When Help button of dialog box is clicked, show BoB manual (pdf)"""
        bob_manual_pdf = 'docs%ssource%smanual%sApplications%sReact%sbob2.3.pdf' % (
            (os.sep, ) * 5)
        QDesktopServices.openUrl(QUrl.fromLocalFile(bob_manual_pdf))

    def handle_architecture_type_changed(self, current_name):
        """Activate/Desactivate the 'ngeneration' widgets
        specific to the Cayley types.
        Called when the combobox 'Architecture' is changed"""
        is_cayley = "Cayley" in current_name
        self.d.ngeneration_label.setDisabled(not is_cayley)
        self.d.sb_ngeneration.setDisabled(not is_cayley)

    def handle_add_component(self):
        """Add a tab with new polymer component in the dialog box"""
        pol_type = self.d.cb_type.currentData() # enum type name
        # re-use numbering of closed tabs (if any)
        if self.trash_indices:
            ind = min(self.trash_indices)
            self.trash_indices.remove(ind)
            pol_id = "%s.%s" % (pol_type, ind)
        else:
            pol_id = "%s.%s" % (pol_type, self.ncomponent)
            self.ncomponent += 1
        # define a new tab widget
        tab_widget, success = self.create_new_tab(pol_id, pol_type)
        index = self.d.polymer_tab.addTab(tab_widget, pol_id)
        if success:
            # if success, set new tab as active one
            self.d.polymer_tab.setCurrentIndex(index)
            tip = ArchitectureType[pol_type].value['descr']
            self.d.polymer_tab.setTabToolTip(index, tip)
        else:
            self.handle_close_polymer_tab(index)

    def create_new_tab(self, pol_id, pol_type):
        """Return a new widget containing a form with all the parameters
        specific to the polymer type ``pol_type``
        """
        widget = QWidget(self)
        layout = QFormLayout()
        pol_dict = OrderedDict([
            ("type", pol_type),
        ])  # Arch. enum type number

        val_double = QDoubleValidator()
        val_double.setBottom(0)  #set smallest double allowed in the form

        e1 = QLineEdit()
        e1.setValidator(val_double)
        e1.setMaxLength(6)
        e1.setText(self.d.ratio.text())
        e1.setToolTip('Ratio weight fraction occupied by this polymer type')
        label = QLabel("Ratio")
        label.setToolTip('Ratio weight fraction occupied by this polymer type')
        layout.addRow(label, e1)
        pol_dict["Ratio"] = e1

        e2 = QLineEdit()
        e2.setValidator(val_double)
        e2.setText(self.d.number.text())
        e2.setToolTip('Number of polymers of this type')
        label2 = QLabel("Num. of polymers")
        label2.setToolTip('Number of polymers of this type')
        layout.addRow(label2, e2)
        pol_dict["Num. of polymers"] = e2
        success = self.set_extra_lines(pol_type, layout, pol_dict)

        self.dict_component[pol_id] = pol_dict
        widget.setLayout(layout)
        if success:
            return widget, True
        else:
            return widget, False

    def set_extra_lines(self, pol_type, layout, pol_dict):
        """Add extra parameter lines related to the polymer architecture ``pol_type``
        to the form layout
        """
        # return a list with the expected input parameters
        pol_attr = ArchitectureType[pol_type].value['def']

        if pol_attr[0] in [10, 11, 12]:
            #handle the Cayley tree types
            ngen = self.d.sb_ngeneration.value()
            pol_dict["Num. generation"] = ngen
            for i in range(ngen + 1):
                self.add_new_qline("Mw gen%d (g/mol)" % i, "1e4", layout,
                                   pol_dict, tip='Molecular weight of generation %d' % i)
                self.add_new_qline("PDI gen%d" % i, "1.2", layout, pol_dict, tip='Polydispersity index of generation %d' % i)
                self.add_cb_distribution("Distr. gen%d" % i, layout, pol_dict, tip='Molecular weight distribution of generation %d' % i)

        elif pol_attr[0] == 40:
            #type 40: give a text box that must be saved to a temp file
            label = pol_attr[1]
            layout.addRow(QLabel(''), QLabel(label))
            pol_dict[label] = label
            self.flag_prototype += 1
            self.d.proto_text.setDisabled(False)
            self.d.proto_label.setDisabled(False)

        elif pol_attr[0] == 60:
            #handle the "from file" type
            attr = pol_attr[1]
            fpath = self.get_file_path()
            if fpath == '':
                return False
            if not self.is_ascii(fpath):
                # # copy file
                # ok_path = os.path.join('theories', 'temp', 'my_polyconf.dat')
                # copy2(fpath, ok_path)
                # fpath = ok_path
                self.Qprint("<font color=orange><b>\"%s\" contains non-ascii characters. BoB might not like it...</b></font>" % fpath)
                print("\"%s\" contains non-ascii characters. BoB might not like it..." % fpath)
            self.add_new_qline(attr, fpath, layout, pol_dict, editable=False)
        else:
            for attr in pol_attr[1:]:
                if "arm" in attr:
                    if pol_attr[0] in [4, 6]:
                        # comb Poisson distribution (double)
                        self.add_new_qline(attr, "4.2", layout, pol_dict, tip='Average number of arms per molecules')
                    else:
                        #star or comb with fixed number of arms (integer)
                        self.add_new_qline(attr, "3", layout, pol_dict,
                                           QIntValidator(), tip='Number of arms per molecule (integer)')
                if "Mw" in attr:
                    # add Mw line
                    self.add_new_qline(attr, "1e4", layout, pol_dict, tip='Weight-average molecular weight')
                elif "Mn" in attr:
                    # add Mn line
                    self.add_new_qline(attr, "1e4", layout, pol_dict, tip='Number-average molecular weight')
                elif "PDI" in attr:
                    #add PDI line
                    self.add_new_qline(attr, "1.2", layout, pol_dict, tip='Polydispersity index')
                elif "Dist" in attr:
                    # add distribution combobox
                    self.add_cb_distribution(attr, layout, pol_dict, tip='Molecular weight distribution')
                elif "/mol" in attr:
                    # add branch/molecule line
                    self.add_new_qline(attr, "0.1", layout, pol_dict, tip='Number of branch per molecule')
                elif "proba" in attr:
                    # add branching proba line
                    self.add_new_qline(attr, "0.2", layout, pol_dict, tip='Branching probability')
                elif attr == '':
                    continue
        return True  # success

    def get_file_path(self):
        """Select a polyconf file for BoB to read"""
        # file browser window
        options = QFileDialog.Options()
        dir_start = "data/React/"
        dilogue_name = "Select a Polymer Configuration File"
        ext_filter = "Data Files (*.dat)"
        selected_file, _ = QFileDialog.getOpenFileName(
            self, dilogue_name, dir_start, ext_filter, options=options)
        return selected_file

    def add_new_qline(self,
                      name,
                      default_val,
                      layout,
                      pol_dict,
                      validator=QDoubleValidator(), tip='', editable=True):
        """Add a new line to the form layout containing a QLabel widget
        for the parameter name and a QLineEdit to change the parameter value"""
        validator.setBottom(0)  #set smallest double allowed in the form
        e = QLineEdit()
        e.setValidator(validator)
        e.setText("%s" % default_val)
        e.setToolTip(tip)
        e.setReadOnly(not editable)
        label = QLabel(name)
        label.setToolTip(tip)
        layout.addRow(label, e)
        pol_dict[name] = e

    def add_cb_distribution(self, name, layout, pol_dict, tip=''):
        """Add a new line to the form layout containing a QLabel widget
        for the parameter name and a QComboBox to change the parameter value"""
        cb = QComboBox()
        for dtype in DistributionType:  # list the distribution names
            cb.addItem(dtype.name)
        cb.setCurrentIndex(2)  # log-normal by default
        cb.setToolTip(tip)
        label = QLabel(name)
        label.setToolTip(tip)
        layout.addRow(label, cb)
        pol_dict[name] = cb

    def handle_close_polymer_tab(self, index):
        """Close a tab and delete dictionary entry
        Called when the close-tab button is clicked"""
        name = self.d.polymer_tab.tabText(index)
        ind = int(''.join(c for c in name if c.isdigit()))  #get the tab number
        del self.dict_component[name]
        self.d.polymer_tab.removeTab(index)
        self.trash_indices.append(ind)
        if "Prototype" in name:
            self.flag_prototype -= 1
            if self.flag_prototype == 0:
                self.d.proto_text.setDisabled(True)
                self.d.proto_label.setDisabled(True)

    def launch_param_dialog(self):
        """Show the dialog to set-up number of the polymer components in the mix
        and all the relevant parameters for each component.
        This function is called via a pyqtSignal for multithread compatibility"""
        if self.dialog.exec_():
            # # create temporary file for BoB input
            # temp_dir = os.path.join('theories', 'temp')
            # #create temp folder if does not exist
            # if not os.path.exists(temp_dir):
            #     os.makedirs(temp_dir)

            # # path to 'bob_inp.dat'
            # temp_inp = os.path.join(temp_dir, 'bob_inp.dat')
            temp_inp = 'bob_inp.dat' # dummy name, virtual files used now
            self.dump_text_to_file(temp_inp, self.d.text_box)

            if self.flag_prototype > 0:
                # path to 'poly.proto'
                temp_proto = os.path.join(temp_dir, 'poly.proto')
                self.dump_text_to_file(temp_proto, self.d.proto_text)
                tmp = self.d.proto_text.toPlainText().split()
                self.protoname = []
                self.virtual_proto_file = [] 
                for x in tmp:
                    try:
                        self.virtual_proto_file.append(float(x))
                    except ValueError:
                        self.protoname.append(x)
                if len(self.protoname) < self.flag_prototype:
                    # weak check on length of protofile
                    self.Qprint("Error in the prototype file")
                    return

            # ask where to save the polymer config file
            out_file = self.polyconf_file_out
            tmp1, tmp2 = os.path.splitext(out_file)
            if tmp2 == '':
                self.Qprint("<font color=red><b>Set the output filepath to write the polyconf file</b></font>")
            else:
                if self.polyconf_file_out is not None:
                    if not self.is_ascii(self.polyconf_file_out):
                        # to avoid path name troubles
                        # out_file = os.path.join(temp_dir, 'temp_polyconf.dat') # commented: avoid create files
                        self.Qprint("<font color=orange><b>\"%s\" contains non-ascii characters. BoB might not like it...</b></font>" % out_file)
                        print("\"%s\" contains non-ascii characters. BoB might not like it..." % out_file)
                    # BoB main arguments
                    self.argv = ["./bob", "-i", temp_inp, "-c", out_file, "-p"]
                    if self.flag_prototype > 0:
                        self.argv.append('-x')
                        self.argv.append(temp_proto)
                    self.success_dialog = True
                    return
        self.success_dialog = False

    def dump_text_to_file(self, temp_file, text_widget):
        """NOT USED ANYMORE. Use virtual files only.
        Dump the content of the "result" tab of the dialog box
        into a file ``temp_file``"""
        pass
        # with open(temp_file, 'w') as tmp:
        #     tmp.write(str(text_widget.toPlainText()))

    def get_file_name(self):
        """Launch a dialog for selecting a file where to save the
        result of the polymer configuration created by BoB.
        Return a string with a filename"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontConfirmOverwrite
        dir_start = os.path.join('data', 'React', 'BoB_polyconf.dat')
        dilogue_name = 'Save BoB Polymer Configuration'
        ext_filter = 'Data Files (*.dat)'
        out_file = QFileDialog.getSaveFileName(
            self, dilogue_name, dir_start, ext_filter, options=options)
        self.polyconf_file_out = out_file[0]
        self.d.selected_file.setText(os.path.basename(out_file[0]))

    def is_ascii(self, s):
        """Check if `s` contains non ASCII characters"""
        try:
            s.encode('ascii')
            return True
        except UnicodeEncodeError:
            return False
