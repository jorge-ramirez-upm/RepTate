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
"""Module TheoryBobLVE

BobLVE file calculates the LVE of a given polymer configuration
by Chinmay Das et al.
"""
import os
import numpy as np
import RepTate
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Theory import Theory
from RepTate.gui.QTheory import QTheory
from RepTate.gui import bob_LVE
import time

import ctypes
from RepTate.theories.BobCtypesHelper import BobCtypesHelper, BobError
from PySide6.QtWidgets import QApplication, QToolBar
from PySide6.QtWidgets import QDialog, QFormLayout, QWidget, QLineEdit, QLabel, QComboBox, QDialogButtonBox, QFileDialog, QMessageBox, QTextEdit
from PySide6.QtGui import QDesktopServices, QIcon
from PySide6.QtCore import QUrl, Signal, QSize


class TheoryBobLVE(CmdBase):
    """Analyse the relaxation of polymers read from a polymer configuration file
    using BoB v2.5 (Chinmay Das and Daniel Read).
    These files can be generated from the React application in RepTate.

    The original documentation of BoB can be found here: `<https://sourceforge.net/projects/bob-rheology/files/bob-rheology/bob2.3/bob2.3.pdf/download>`_.
    """
    thname = 'BOB'
    description = 'Branch-On-Branch rheology'
    citations = ['Das C. et al., J. Rheol. 2006, 50, 207-234']
    doi = ["http://dx.doi.org/10.1122/1.2167487"]

    def __new__(cls, name='', parent_dataset=None, axarr=None):
        """Create an instance of the GUI or CL class"""
        return GUITheoryBobLVE(
            name, parent_dataset,
            axarr) if (CmdBase.mode == CmdMode.GUI) else CLTheoryBobLVE(
                name, parent_dataset, axarr)


class BaseTheoryBobLVE:
    """Base class for both GUI and CL"""
    html_help_file = 'https://reptate.readthedocs.io/manual/Applications/LVE/Theory/theory.html#bob-lve'
    single_file = True  # False if the theory can be applied to multiple files simultaneously
    thname = TheoryBobLVE.thname
    citations = TheoryBobLVE.citations
    doi = TheoryBobLVE.doi 

    signal_param_dialog = Signal(object)

    def __init__(self, name='ThBobLVE', parent_dataset=None, axarr=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate  # main theory function
        self.has_modes = False  # True if the theory has modes
        self.signal_param_dialog.connect(self.launch_param_dialog)
        self.polyconf_file_out = None  # full path of target polyconf file
        self.bch = BobCtypesHelper(self)
        self.autocalculate = False
        self.freqint = 1.1 # BoB theory points spaced by log10(freqint)
        self.do_priority_seniority = False
        self.inp_counter = 0 # counter for the 'virtual' input file for BoB
        self.virtual_input_file = [] # 'virtual' input file for BoB

    def request_stop_computations(self):
        """Called when user wants to terminate the current computation"""
        self.Qprint('<font color=red><b>Stop current calculation requested</b></font>')
        self.bch.set_flag_stop_bob(ctypes.c_bool(True))

    def do_error(self, line=""):
        """This theory calculate the error by interpolating the theory solution"""
        self.do_error_interpolated(line="")

    def calculate(self, f=None):
        """Create polymer configuration file and calculate distribution characteristics"""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        self.freqmin = f.data_table.mincol(0)
        self.freqmax = f.data_table.maxcol(0)
        #show form
        self.success_dialog = None
        self.argv = None

        self.signal_param_dialog.emit(self)
        while self.success_dialog is None:  # wait for the end of QDialog
            # TODO: find a better way to wait for the dialog thread to finish
            time.sleep(0.5)
        if not self.success_dialog:
            self.Qprint('Operation cancelled')
            return
        QApplication.processEvents()
        self.bch.link_c_callback()
        self.bch.set_do_priority_seniority(ctypes.c_bool(self.do_priority_seniority))
        # Run BoB C++ code
        self.start_time_cal = time.time()
        try:
            omega, gp, gpp = self.bch.return_bob_lve(self.argv)
        except BobError:
            self.Qprint('Operation cancelled')
            return

        #copy results to RepTate data file
        if omega:
            tt.num_columns = ft.num_columns
            tt.num_rows = len(omega)
            tt.data = np.zeros((tt.num_rows, tt.num_columns))
            tt.data[:, 0] = omega[:]
            tt.data[:, 1] = gp[:]
            tt.data[:, 2] = gpp[:]

    def do_fit(self, line=''):
        self.Qprint("Fitting not allowed in this theory")

class CLTheoryBobLVE(BaseTheoryBobLVE, Theory):
    """CL Version"""

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, axarr)

    # This class usually stays empty


class GUITheoryBobLVE(BaseTheoryBobLVE, QTheory):
    """GUI Version"""

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, axarr)
        # temp_dir = os.path.join('theories', 'temp')
        # #create temp folder if does not exist
        # if not os.path.exists(temp_dir):
        #     os.makedirs(temp_dir)
        self.selected_file = None
        self.setup_dialog()
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        self.btn_prio_senio = tb.addAction(QIcon(':/Icon8/Images/new_icons/priority_seniority.png'), 'Calculate Priority and Seniority (can take some time)')
        self.btn_prio_senio.setCheckable(True)
        self.btn_prio_senio.setChecked(self.do_priority_seniority)

        # BoB LVE do not calculate priority & seniority (leave it to React)
        # uncomment below for the possiblity to calculate priority & seniority in BoB LVE
        
        # self.thToolsLayout.insertWidget(0, tb)
        self.btn_prio_senio.triggered.connect(self.handle_btn_prio_senio)

    def handle_btn_prio_senio(self, checked):
        """Change do_priority_seniority"""
        self.do_priority_seniority = checked

    def get_file_name(self):
        """Open a dialog to choose a file containing the polymer configuration for BoB"""
        # file browser window
        options = QFileDialog.Options()
        dir_start = os.path.join(RepTate.root_dir, "data", "React")
        dilogue_name = "Select a Polymer Configuration File"
        ext_filter = "Data Files (*.dat)"
        selected_file, _ = QFileDialog.getOpenFileName(
            self, dilogue_name, dir_start, ext_filter, options=options)
        self.selected_file = selected_file
        self.d.selected_file.setText(os.path.basename(selected_file))

    def num_file_lines(self, fname):
        """Return the number of lines in the file `fname`"""
        with open(fname) as f:
            i = 0
            for _, l in enumerate(f):
                i += 1 
            return i + 1

    def setup_dialog(self):
        """Load the form dialog from bob_LVE.py"""
        self.dialog = QDialog(self)
        self.dialog.ui = bob_LVE.Ui_Dialog()
        self.dialog.ui.setupUi(self.dialog)
        self.d = self.dialog.ui
        self.d.pb_pick_file.clicked.connect(self.get_file_name)
        self.d.selected_file.setStyleSheet("color : blue ;")
        # connect button OK
        self.d.pb_ok.clicked.connect(self.handle_pb_ok)
        self.d.pb_ok.setDefault(True)
        # connect button Cancel
        self.d.pb_cancel.clicked.connect(self.dialog.reject)
        # connect button Help
        self.d.pb_help.clicked.connect(
            self.handle_help_button)

    def handle_pb_ok(self):
        """Define the OK button role. If something is wrong, keep the dialog open"""
        if self.selected_file is None:
            QMessageBox.warning(
                self, 'Select Input Polyconf',
                'Please select a file for BoB to read the polymer configuration')
        else:    
            self.dialog.accept()

    def handle_help_button(self):
        """When Help button of dialog box is clicked, show BoB manual (pdf)"""
        bob_manual_pdf = 'docs%ssource%smanual%sApplications%sReact%sbob2.3.pdf' % (
            (os.sep, ) * 5)
        QDesktopServices.openUrl(QUrl.fromLocalFile(bob_manual_pdf))

    def create_bob_input_file(self, nlines, inpf):
        """Create a file containing the input BoB parameters from the form dialog"""
        # with open(inpf, 'w') as tmp:
        #     #1 memory
        #     npol = max(nlines, float(self.d.n_polymers.text()))
        #     nseg = max(nlines, float(self.d.n_segments.text()))

        #     tmp.write('%d %d\n' % (npol, nseg))
        #     #2 alpha
        #     tmp.write('%.6g\n' % float(self.d.alpha.text()))
        #     #3 dummy "1"
        #     tmp.write('1\n')
        #     # 4 M0, Ne, density
        #     M0 = float(self.d.m0.text())
        #     Ne = float(self.d.ne.text())
        #     density = float(self.d.density.text())
        #     tmp.write('%.6g %.6g %.6g\n' % (M0, Ne, density))
        #     #5 tau_e, T
        #     taue = float(self.d.taue.text())
        #     temperature = float(self.d.temperature.text())
        #     tmp.write('%.6g %.6g\n' % (taue, temperature))
        #     #6 write "0" so BoB reads a polyconf file
        #     tmp.write('0\n')
        tmp = []
        #1 memory
        npol = max(nlines, float(self.d.n_polymers.text()))
        nseg = max(nlines, float(self.d.n_segments.text()))
        tmp.append(npol)
        tmp.append(nseg)
        #2 alpha
        tmp.append(float(self.d.alpha.text()))
        #3 dummy "1"
        tmp.append(1)
        # 4 M0, Ne, density
        M0 = float(self.d.m0.text())
        Ne = float(self.d.ne.text())
        density = float(self.d.density.text())
        tmp.append(M0)
        tmp.append(Ne)
        tmp.append(density)
        #5 tau_e, T
        taue = float(self.d.taue.text())
        temperature = float(self.d.temperature.text())
        tmp.append(taue)
        tmp.append(temperature)
        #6 write "0" so BoB reads a polyconf file
        tmp.append(0)
        self.virtual_input_file = tmp

    def launch_param_dialog(self):
        """Show a dialog to get the filename of the polymer configuration.
        This function is called via a Signal for multithread compatibility"""
        if not self.dialog.exec_():
            self.success_dialog = False
            return
        conffile = self.selected_file
        if not self.is_ascii(conffile):
            # ok_path = os.path.join('theories', 'temp', 'target_polyconf.dat')
            # copy2(conffile, ok_path)
            # conffile = ok_path
            self.Qprint("<font color=orange><b>\"%s\" contains non-ascii characters. BoB might not like it...</b></font>" % conffile)
            print("\"%s\" contains non-ascii characters. BoB might not like it..." % conffile)
        if conffile == '' or os.path.splitext(conffile)[1] == '':
            self.Qprint("<font color=red><b>Set the output filepath to write the polyconf file</b></font>")
            return
        nlines = self.num_file_lines(conffile)
        # inpf = os.path.join('theories', 'temp', 'temp_inpf.dat') 
        inpf = 'inpf.dat' # dummy name, use virtual files now
        self.create_bob_input_file(nlines, inpf)

        # BoB main arguments
        self.argv = ["./bob", "-i", inpf, "-c", conffile]
        self.success_dialog = True

    def is_ascii(self, s):
        """Check if `s` contains non ASCII characters"""
        try:
            s.encode('ascii')
            return True
        except UnicodeEncodeError:
            return False