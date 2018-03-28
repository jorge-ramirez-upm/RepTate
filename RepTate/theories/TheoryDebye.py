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
"""Module TheoryDebye

Debye theory for neutron scattering from ideal polymer chains
"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices

class TheoryDebye(CmdBase):
    """[summary]
    
    [description]
    """
    thname = 'DebyeTheory'
    description = 'Debye theory for neutron scattering from ideal polymer chains'
    citations = ''

    def __new__(cls, name='ThDebye', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'ThDebye'})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUITheoryDebye(
            name, parent_dataset,
            axarr) if (CmdBase.mode == CmdMode.GUI) else CLTheoryDebye(
                name, parent_dataset, axarr)


class BaseTheoryDebye:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/en/latest/manual/Applications/SANS/Theory/Debye.html'
    single_file = False  # False if the theory can be applied to multiple files simultaneously

    def __init__(self, name='ThDebye', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'ThDebye'})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculateDebye  # main theory function
        self.has_modes = False  # True if the theory has modes
        self.parameters['Contrast'] = Parameter(
            name='Contrast',
            value=0.4203,
            description='???????',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['C_gyr'] = Parameter(
            name='C_gyr',
            value=62.3,
            description='???????',
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters['M_mono'] = Parameter(
            name='M_mono',
            value=0.104,
            description='???????',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['Bckgrnd'] = Parameter(
            name='Bckgrnd',
            value=0.26,
            description='???????',
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters['Chi'] = Parameter(
            name='Chi',
            value=1E-4,
            description='???????',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['Lambda'] = Parameter(
            name='Lambda',
            value=1,
            description='???????',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters["stretched"] = Parameter(
            name="stretched",
            value=False,
            description="????????",
            type=ParameterType.boolean,
            opt_type=OptType.const,
            display_flag=False)
        self.parameters["non-ideal"] = Parameter(
            name="non-ideal",
            value=False,
            description="????????",
            type=ParameterType.boolean,
            opt_type=OptType.const,
            display_flag=False)
            
    def calculateDebye(self, f=None):
        """Debye function that returns the square of y
        
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

        try:
            Mw = float(f.file_parameters["Mw"])
            Phi = float(f.file_parameters["Phi"])
        except (ValueError, KeyError):
            self.Qprint("Invalid Mw or Phi value")
            return

        Contr = self.parameters["Contrast"].value
        CRg = self.parameters["C_gyr"].value
        Mmono = self.parameters["M_mono"].value
        Bck = self.parameters["Bckgrnd"].value
        Chi = self.parameters["Chi"].value
        Lambda = self.parameters["Lambda"].value
        stretched = self.parameters["stretched"].value
        nonideal = self.parameters["non-ideal"].value

        tt.data[:, 0] = ft.data[:, 0]
        
        Rg = np.sqrt(CRg * Mw)
        if (stretched):
            Rg*=Lambda
        RgQsq = Rg * Rg * ft.data[:, 0] * ft.data[:, 0]
        debFn = 2.0 / RgQsq / RgQsq * (RgQsq + np.exp(-RgQsq) - 1.0)
        if (nonideal):
            tt.data[:, 1] = Contr * 1 / (1 / (Mw / Mmono * Phi * (1.0 - Phi) * debFn) - 2 * Chi) + Bck
        else:
            tt.data[:, 1] = Contr * Mw / Mmono * Phi * (1.0 - Phi) * debFn + Bck
        
        if (stretched):
            self.Qprint("%12s %8.4g %8.4g"%(f.file_name_short,Mw, Lambda * np.sqrt(CRg * Mw)))
        else:
            self.Qprint("%12s %8.4g %8.4g"%(f.file_name_short,Mw, np.sqrt(CRg * Mw)))

class CLTheoryDebye(BaseTheoryDebye, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='ThDebye', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'ThDebye'})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # This class usually stays empty


class GUITheoryDebye(BaseTheoryDebye, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='ThDebye', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {'ThDebye'})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # add widgets specific to the theory here:
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        self.tbutstretched = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-socks.png'), 'Stretched')
        self.tbutstretched.setCheckable(True)
        self.tbutstretched.setChecked(False)
        self.tbutnonideal = tb.addAction(
            QIcon(':/Images/Images/new_icons/icons8-broom.png'), 'Non-Ideal Mix')
        self.tbutnonideal.setCheckable(True)
        self.tbutnonideal .setChecked(False)
        self.thToolsLayout.insertWidget(0, tb)

        #connections signal and slots
        connection_id = self.tbutstretched.triggered.connect(
            self.handle_tbutstretched_triggered)
        connection_id = self.tbutnonideal.triggered.connect(
            self.handle_tbutnonideal_triggered)

    def handle_tbutstretched_triggered(self, checked):
        """[summary]
        
        [description]
        """
        self.set_param_value("stretched", checked)

    def handle_tbutnonideal_triggered(self, checked):
        """[summary]
        
        [description]
        """
        self.set_param_value("non-ideal", checked)
