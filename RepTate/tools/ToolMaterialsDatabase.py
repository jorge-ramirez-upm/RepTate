# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Tool and Experiments
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
# Copyright (2018): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module ToolMaterialsDatabase

MaterialsDatabase Viewer
"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Tool import Tool
from QTool import QTool
from DataTable import DataTable
from PyQt5.QtWidgets import QComboBox, QLabel, QToolBar, QLineEdit, QAction
from PyQt5.QtGui import QStandardItem, QFont, QIcon

materials_database = np.load('tools/materials_database.npy').item()
materials_user_database = np.load('tools/user_database.npy').item()

class ToolMaterialsDatabase(CmdBase):
    """[summary]
    
    [description]
    """
    toolname = 'Materials Database'
    description = 'Materials Database Explorer'
    citations = ''

    def __new__(cls, name='', parent_app=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUIToolMaterialsDatabase(name, parent_app) if (CmdBase.mode == CmdMode.GUI) else CLToolMaterialsDatabase(name, parent_app)


class BaseToolMaterialsDatabase:
    """[summary]
    
    [description]
    """
    #help_file = 'http://reptate.readthedocs.io/en/latest/manual/Tools/MaterialsDatabase.html'
    toolname = ToolMaterialsDatabase.toolname
    citations = ToolMaterialsDatabase.citations

    def __init__(self, name='', parent_app=None):
        """
        **Constructor**
        
            - name {[type]} -- [description] (default: {''})
        Keyword Arguments:
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_app)
        self.parameters['name'] = Parameter(name='name', description='Name of polymer', type=ParameterType.string, display_flag=False)
        self.parameters['long'] = Parameter(name='long', description='Long name of polymer', type=ParameterType.string, display_flag=False)
        self.parameters['author'] = Parameter(name='author', description='Who added the data to the database?', type=ParameterType.string, display_flag=False)
        self.parameters['date'] = Parameter(name='date', description='Date when the data was added', type=ParameterType.string, display_flag=False)
        self.parameters['source'] = Parameter(name='source', description='Source of the data', type=ParameterType.string, display_flag=False)
        self.parameters['comment'] = Parameter(name='comment', description='Additional comments', type=ParameterType.string, display_flag=False)
        self.parameters['B1'] = Parameter(name='B1', description='WLF TTS parameter 1')
        self.parameters['B2'] = Parameter(name='B2', description='WLF TTS parameter 2')
        self.parameters['logalpha'] = Parameter(name='logalpha', description='Log_10 of the thermal expansion coefficient at 0 °C')
        self.parameters['CTg'] = Parameter(name='CTg', description='Molecular weight dependence of Tg')
        self.parameters['tau_e'] = Parameter(name='tau_e', description='Entanglement time')
        self.parameters['Ge'] = Parameter(name='Ge', description='Entanglement modulus')
        self.parameters['Me'] = Parameter(name='Me', description='Entanglement molecular weight')
        self.parameters['c_nu'] = Parameter(name='c_nu', description='Constraint release parameter')
        self.parameters['rho0'] = Parameter(name='rho0', description='Density of the polymer melt (kg/m3) at 0 °C')
        self.parameters['chem'] = Parameter(name='chem', description='Repeating unit', type=ParameterType.string)
        self.parameters['M0'] = Parameter(name='M0', description='Mass of Repeating unit (g/mol)')
        self.parameters['C_inf'] = Parameter(name='C_inf', description='Characteristic ratio')

    def destructor(self):
        """[summary]
        
        [description]
        
        Arguments:

        """
        pass

    def calculate(self, x, y, ax=None, color=None):
        """MaterialsDatabase function that returns the square of the y, according to the view        
        """
        return x, y


class CLToolMaterialsDatabase(BaseToolMaterialsDatabase, Tool):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_app=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_app)

    # This class usually stays empty


class GUIToolMaterialsDatabase(BaseToolMaterialsDatabase, QTool):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_app=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_app)
        self.update_parameter_table()
        self.parent_application.update_all_ds_plots()

    # add widgets specific to the Tool here:
        self.active = False
        self.applytotheory = False
        self.actionActive.setVisible(False)
        self.actionApplyToTheory.setVisible(False)
        self.cbmaterial = QComboBox()
        self.cbmaterial.setToolTip("Choose a Material from the database")
        model = self.cbmaterial.model()
        i = 0
        for polymer in materials_database.keys():
            item = QStandardItem(polymer)
            item.setToolTip(materials_database[polymer].data['long'])
            model.appendRow(item)
            i += 1
        self.cbmaterial.insertSeparator(i)
        for polymer in materials_user_database.keys():
            item = QStandardItem(polymer)
            item.setToolTip(materials_user_database[polymer].data['long'])
            model.appendRow(item)
        self.tb.addWidget(self.cbmaterial)
        self.actionNew = QAction(QIcon(':/Icon8/Images/new_icons/icons8-add-file.png'), "New Material", self)
        self.tb.addAction(self.actionNew)
        self.actionEdit = QAction(QIcon(':/Icon8/Images/new_icons/icons8-edit-property.png'), "Edit/View Material Properties", self)
        self.tb.addAction(self.actionEdit)
        self.actionSave = QAction(QIcon(':/Icon8/Images/new_icons/icons8-save.png'), "Save User Material Database", self)
        self.tb.addAction(self.actionSave)

        self.labelPolymer = QLabel("None")
        self.labelPolymer.setFont(QFont("Times",weight=QFont.Bold))
        self.verticalLayout.insertWidget(1, self.labelPolymer)
        connection_id = self.cbmaterial.currentIndexChanged.connect(self.change_material)

        self.tbMwT = QToolBar()
        lbl1 = QLabel("Mw (kDa)")
        lbl1.setFont(QFont("Times",weight=QFont.Bold))
        self.tbMwT.addWidget(lbl1)
        self.editMw = QLineEdit("1")
        self.editMw.setStyleSheet("QLineEdit { background: rgb(255, 255, 205);}");
        self.editMw.setFixedWidth(60)
        self.tbMwT.addWidget(self.editMw)
        lbl2 = QLabel("T (°C)")
        lbl2.setFont(QFont("Times",weight=QFont.Bold))
        self.tbMwT.addWidget(lbl2)
        self.editT = QLineEdit("0")
        self.editT.setStyleSheet("QLineEdit { background: rgb(255, 255, 205);}");
        self.editT.setFixedWidth(40)
        self.tbMwT.addWidget(self.editT)
        self.verticalLayout.insertWidget(2, self.tbMwT)

        self.change_material()

    def change_material(self):
        selected_material_name = self.cbmaterial.currentText()
        self.labelPolymer.setText(materials_database[selected_material_name].data['long'])
        for k in materials_database[selected_material_name].data.keys():
            self.set_param_value(k, materials_database[selected_material_name].data[k])
        self.update_parameter_table()