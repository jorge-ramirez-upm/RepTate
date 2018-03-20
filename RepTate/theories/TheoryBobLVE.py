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
# Copyright (2017): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
from CmdBase import CmdBase, CmdMode
from enum import Enum
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from collections import OrderedDict
import time

import bob_LVE  # dialog
from BobCtypesHelper import BobCtypesHelper
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog, QFormLayout, QWidget, QLineEdit, QLabel, QComboBox, QDialogButtonBox, QFileDialog, QMessageBox, QTextEdit
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QDesktopServices
from PyQt5.QtCore import QUrl, pyqtSignal
from shutil import copy2


class TheoryBobLVE(CmdBase):
    """[summary]
    
    [description]
    """
    thname = 'BobLVETheory'
    description = 'BobLVE Theory'
    citations = ''

    def __new__(cls, name='ThBobLVE', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'ThBobLVE'})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUITheoryBobLVE(
            name, parent_dataset,
            axarr) if (CmdBase.mode == CmdMode.GUI) else CLTheoryBobLVE(
                name, parent_dataset, axarr)


class BaseTheoryBobLVE:
    """[summary]
    
    [description]
    """
    #help_file = ''
    single_file = True  # False if the theory can be applied to multiple files simultaneously
    signal_param_dialog = pyqtSignal(object)

    def __init__(self, name='ThBobLVE', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'ThBobLVE'})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate  # main theory function
        self.has_modes = False  # True if the theory has modes
        self.signal_param_dialog.connect(self.launch_param_dialog)
        self.polyconf_file_out = None  # full path of target polyconf file

    def get_modes(self):
        """[summary]
        
        [description]
        
        Returns:
            - [type] -- [description]
        """
        pass

    def do_error(self, line=""):
        """[summary]
        
        [description]
        
        Returns:
            - [type] -- [description]
        """
        pass

    def set_modes(self):
        """[summary]
        
        [description]
        
        Arguments:

        """
        pass

    def destructor(self):
        """[summary]
        
        [description]
        
        Arguments:

        """
        pass

    def calculate(self, f=None):
        """Create polymer configuration file and calculate distribution characteristics
        
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
        #show form
        self.success_dialog = None
        self.argv = None

        self.signal_param_dialog.emit(self)
        while self.success_dialog is None:  # wait for the end of QDialog
            # TODO: find a better way to wait for the dialog thread to finish
            time.sleep(0.5)
        if not self.success_dialog:
            self.Qprint('Operation canceled')
            return
        QApplication.processEvents()

        # Run BoB C++ code
        bch = BobCtypesHelper(self)
        omega, gp, gpp = bch.return_bob_lve(self.argv)

        #copy results to RepTate data file
        if omega:
            # print(omega, gp, gpp)

            tt.num_columns = ft.num_columns
            tt.num_rows = len(omega)
            tt.data = np.zeros((tt.num_rows, tt.num_columns))
            tt.data[:, 0] = omega[:]
            tt.data[:, 1] = gp[:]
            tt.data[:, 2] = gpp[:]


class CLTheoryBobLVE(BaseTheoryBobLVE, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='ThBobLVE', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'ThBobLVE'})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # This class usually stays empty


class GUITheoryBobLVE(BaseTheoryBobLVE, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='ThBobLVE', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'ThBobLVE'})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        temp_dir = os.path.join('theories', 'temp')
        #create temp folder if does not exist
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        self.setup_dialog()

    def get_file_path(self):
        """Open a dialog to choose a file containing the polymer configuration for BoB"""
        # file browser window
        options = QFileDialog.Options()
        dir_start = "data/React/"
        dilogue_name = "Select a Polymer Configuration File"
        ext_filter = "Data Files (*.dat)"
        selected_file, _ = QFileDialog.getOpenFileName(
            self, dilogue_name, dir_start, ext_filter, options=options)
        return selected_file

    def num_file_lines(self, fname):
        """Return the number of lines in the file `fname`"""
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def setup_dialog(self):
        """Load the form dialog from bob_LVE.py"""
        self.dialog = QDialog(self)
        self.dialog.ui = bob_LVE.Ui_Dialog()
        self.dialog.ui.setupUi(self.dialog)
        self.d = self.dialog.ui

    def create_bob_input_file(self, nlines, inpf):
        """Create a file containing the input BoB parameters from the form dialog"""
        with open(inpf, 'w') as tmp:
            #1 memory
            npol = max(nlines, float(self.d.n_polymers.text()))
            nseg = max(nlines, float(self.d.n_segments.text()))

            tmp.write('%d %d\n' % (npol, nseg))
            #2 alpha
            tmp.write('%f\n' % float(self.d.alpha.text()))
            #3 dummy "1"
            tmp.write('1\n')
            # 4 M0, Ne, density
            M0 = float(self.d.m0.text())
            Ne = float(self.d.ne.text())
            density = float(self.d.density.text())
            tmp.write('%f %f %f\n' % (M0, Ne, density))
            #5 tau_e, T
            taue = float(self.d.taue.text())
            temperature = float(self.d.temperature.text())
            tmp.write('%f %f\n' % (taue, temperature))
            #6 number of component(s) in blend = 0
            tmp.write('0\n')

    def launch_param_dialog(self):
        """Show a dialog to get the filename of the polymer configuration.
        This function is called via a pyqtSignal for multithread compatibility"""
        if not self.dialog.exec_():
            self.success_dialog = False
            return
        conffile = self.get_file_path()
        if not self.is_ascii(conffile):
            ok_path = os.path.join('theories', 'temp', 'target_polyconf.dat')
            copy2(conffile, ok_path)
            conffile = ok_path
        if conffile == '':
            return
        nlines = self.num_file_lines(conffile)
        inpf = os.path.join('theories', 'temp', 'temp_inpf.dat')
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