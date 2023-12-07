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
import sys
import os
import numpy as np
from RepTate.core.CmdBase import CmdBase
from RepTate.core.Parameter import Parameter, ParameterType
from RepTate.core.Tool import Tool
from RepTate.gui.QTool import QTool
from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
    QToolBar,
    QLineEdit,
    QMessageBox,
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QGroupBox,
    QFormLayout,
    QInputDialog,
    QTreeWidgetItemIterator
)
from PySide6.QtCore import QSize, QStandardPaths
from PySide6.QtGui import QStandardItem, QFont, QIcon, QAction, QColor, QDoubleValidator
from pathlib import Path
import RepTate.tools.polymer_data as polymer_data
from colorama import Fore

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    PATH = sys._MEIPASS
else:
    PATH = os.path.dirname(os.path.abspath(__file__))

# The following two lines are temporary. They can be removed after the database is pickeld with RepTate.ttols.polymer_data instead of polymer_data
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
# dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(PATH)
materials_database = np.load(
    os.path.join(PATH, "materials_database.npy"), allow_pickle=True
).item()

# search user material database in the (old) location "HOME"
home_path = str(Path.home())
file_user_database_old = os.path.join(home_path, "user_database.npy")
if os.path.exists(file_user_database_old):
    materials_user_database_old = np.load(file_user_database_old, allow_pickle=True).item()
else:
    materials_user_database_old = {}

# search user material database in the (new) location "AppData"
AppData_path = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
file_user_database = os.path.join(AppData_path, "user_database.npy")
if os.path.exists(file_user_database):
    materials_user_database = np.load(file_user_database, allow_pickle=True).item()
else:
    materials_user_database = {}

materials_user_database.update(materials_user_database_old)
materials_db = [materials_user_database, materials_database]


class EditMaterialParametersDialog(QDialog):
    """Create the form that is used to edit/modify the material parameters"""

    def __init__(self, parent, material, parameterdata):
        super().__init__(parent)
        self.parent_dataset = parent
        self.material = material
        self.createFormGroupBox(material, parameterdata)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("Edit Material Parameters")

    def createFormGroupBox(self, material, parameterdata):
        """Create a form to set the new values of the material parameters"""
        self.formGroupBox = QGroupBox(
            'Parameters of material "%s"' % material.data["name"]
        )
        layout = QFormLayout()

        parameters = material.data
        self.param_dict = {}
        self.p_new = []
        for i, pname in enumerate(material.data.keys()):
            self.p_new.append(QLineEdit())
            if isinstance(material.data[pname], str):  # the parameter is a string
                self.p_new[i].setText("%s" % material.data[pname])
            else:  # parameter is a number:
                self.p_new[i].setValidator(QDoubleValidator())  # prevent letters
                self.p_new[i].setText("%.4g" % material.data[pname])
            self.p_new[i].setToolTip(parameterdata[pname].description)
            if pname == "name":
                self.p_new[i].setReadOnly(True)
            layout.addRow("%s:" % pname, self.p_new[i])
            self.param_dict[pname] = self.p_new[i]
        self.formGroupBox.setLayout(layout)


def check_chemistry(chem):
    """Check if the file contains chemistry. If so, check if the chemistry appears in
    the user or general materials database.
        Arguments:
            - chem {str} -- Chemistry
        Returns:
            - code {integer} -- -1 (not found) 0 (found in user's) 1 (found in general database)
    """
    if chem in materials_user_database.keys():
        return 0
    elif chem in materials_database.keys():
        return 1
    else:
        return -1


def get_all_parameters(chem, theory, fparam, dbindex):
    """Gets all possible parameters from the corresponding materials database.
    The function check_chemistry must be involed before this one, to get chem and dbindex.
        Arguments:
            - chem {str} -- Chemistry
            - theory {Theory} -- A given theory
            - file_parameters {dict} -- Parameters of the file
            - dbindex {int} -- Index of the database to use (0 user, 1 general)
        Returns:
            - nothing
    """
    for p in theory.parameters.keys():
        if p in materials_db[dbindex][chem].data.keys():
            value, success = get_single_parameter(chem, p, fparam, dbindex)
            if success:
                theory.set_param_value(p, value)


def get_single_parameter(chem, param, fparam, dbindex):
    """Returns the parameter 'param' of the chemistry 'chem' using the database
    given by dbindex (0 user, 1 general) and taking into account the parameters
    of fparam (for example, T and Mw).
    The parameter 'param' must exist in the database. This is done when this function
    is invoked from get_all_parameters. If this function is invoked directly, the
    condition must be chedked beforehand.
        Arguments:
            - chem {str} -- Chemistry
            - param -- The theory parameter that we want to set
            - file_parameters {dict} -- Parameters of the file
            - dbindex {int} -- Index of the database to use (0 user, 1 general)
        Returns:
            - value -- The value of the parameter
            - success {bool} -- A success flag
    """
    if param == "tau_e":
        try:
            T = float(fparam["T"])
        except:  # T was not found in the file parameters
            return 0, False

        tau_e = materials_db[dbindex][chem].data["tau_e"]
        B1 = materials_db[dbindex][chem].data["B1"]
        B2 = materials_db[dbindex][chem].data["B2"]
        Te = materials_db[dbindex][chem].data["Te"]
        aT = np.power(10.0, -B1 * (Te - T) / (B2 + T) / (B2 + Te))
        tau_e /= aT
        # We don´t consider the effect of Tg in this estimate
        return tau_e, True
    elif param == "Ge":
        try:
            T = float(fparam["T"])
        except:  # T was not found in the file parameters
            return 0, False
        logalpha = materials_db[dbindex][chem].data["logalpha"]
        Ge = materials_db[dbindex][chem].data["Ge"]
        Te = materials_db[dbindex][chem].data["Te"]
        alpha = np.power(10.0, logalpha)
        bT = (1 + alpha * Te) * (T + 273.15) / (1 + alpha * T) / (Te + 273.15)
        Ge /= bT
        return Ge, True
    elif param == "rho0":
        try:
            T = float(fparam["T"])
        except:  # T was not found in the file parameters
            return 0, False
        rho0 = materials_db[dbindex][chem].data["rho0"]
        logalpha = materials_db[dbindex][chem].data["logalpha"]
        alpha = np.power(10.0, logalpha)
        rho = rho0 / (1.0 + alpha * T)
        return rho, True
    else:
        value = materials_db[dbindex][chem].data[param]
        return value, True


class ToolMaterialsDatabase(CmdBase):
    """A special Tool to store the material parameters. Many apps and theories rely on the
    parameters stored in this database. There are two copies of the database: i) a general one
    that is distributed with RepTate, is stored in the software installation folder and contains
    well established values of the parameters and ii) a user database that contains material
    parameters introduced by the user and is stored in the user HOME folder.
    """

    toolname = "Materials Database"
    description = "Materials Database Explorer"
    citations = []

    def __new__(cls, name="", parent_app=None):
        """Create an instance of the GUI"""
        return GUIToolMaterialsDatabase(name, parent_app)


class BaseToolMaterialsDatabase:
    """Base class for both GUI"""

    # html_help_file = 'http://reptate.readthedocs.io/manual/Tools/MaterialsDatabase.html'
    toolname = ToolMaterialsDatabase.toolname
    citations = ToolMaterialsDatabase.citations

    def __init__(self, name="", parent_app=None):
        """**Constructor**
        
        """
        super().__init__(name, parent_app)
        self.parameters["name"] = Parameter(
            name="name",
            description="Name of polymer",
            type=ParameterType.string,
            display_flag=False,
        )
        self.parameters["long"] = Parameter(
            name="long",
            description="Long name of polymer",
            type=ParameterType.string,
            display_flag=False,
        )
        self.parameters["author"] = Parameter(
            name="author",
            description="Who added the data to the database?",
            type=ParameterType.string,
            display_flag=False,
        )
        self.parameters["date"] = Parameter(
            name="date",
            description="Date when the data was added",
            type=ParameterType.string,
            display_flag=False,
        )
        self.parameters["source"] = Parameter(
            name="source",
            description="Source of the data",
            type=ParameterType.string,
            display_flag=False,
        )
        self.parameters["comment"] = Parameter(
            name="comment",
            description="Additional comments",
            type=ParameterType.string,
            display_flag=False,
        )
        self.parameters["B1"] = Parameter(name="B1", description="WLF TTS parameter 1")
        self.parameters["B2"] = Parameter(name="B2", description="WLF TTS parameter 2")
        self.parameters["logalpha"] = Parameter(
            name="logalpha",
            description="Log_10 of the thermal expansion coefficient at 0 °C",
        )
        self.parameters["CTg"] = Parameter(
            name="CTg", description="Molecular weight dependence of Tg"
        )
        self.parameters["tau_e"] = Parameter(
            name="tau_e", description="Entanglement time (s)"
        )
        self.parameters["Ge"] = Parameter(
            name="Ge", description="Entanglement modulus (Pa)"
        )
        self.parameters["Me"] = Parameter(
            name="Me", description="Entanglement molecular weight (kDa)"
        )
        self.parameters["c_nu"] = Parameter(
            name="c_nu", description="Constraint release parameter"
        )
        self.parameters["rho0"] = Parameter(
            name="rho0", description="Density of the polymer melt (g/cm3) at 0 °C"
        )
        self.parameters["chem"] = Parameter(
            name="chem", description="Repeating unit", type=ParameterType.string
        )
        self.parameters["Te"] = Parameter(
            name="Te",
            description="Temperature at which the tube parameters have been determined (°C)",
        )
        self.parameters["M0"] = Parameter(
            name="M0", description="Mass of Repeating unit (g/mol)"
        )
        self.parameters["MK"] = Parameter(
            name="MK", description="Molecular weight of Kuhn step (Da)"
        )
        self.parameters["C_inf"] = Parameter(
            name="C_inf", description="Characteristic ratio"
        )

        # Search for the chemistry in the first file of the first dataset (OR CURRENT DATASET?)
        self.init_chem = None
        if len(parent_app.datasets)>0:
            ds = parent_app.datasets[list(parent_app.datasets)[0]]
            if len(ds.files)>0:
                f = ds.files[0]
                if 'chem' in f.file_parameters:
                    self.init_chem=f.file_parameters['chem']

    def calculate(self, x, y, ax=None, color=None, file_parameters=[]):
        """Calculate some results related to the selected material or the file material"""
        self.calculate_stuff("", file_parameters)
        return x, y

    def do_calculate_stuff(self, line=""):
        """Given the values of Mw (in kDa) and T (in °C), as well as a flag for isofrictional state and vertical shift, it returns some calculations for the current chemistry.
Example:
    calculate_stuff 35.4 240 1 1

    Mw=35.4 T=240 isofrictional=True verticalshift=True"""
        items = line.split()
        if len(items) == 4:
            Mw = float(items[0])
            T = float(items[1])
            iso = bool(items[2])
            vert = bool(items[3])
            B1 = self.parameters["B1"].value
            B2 = self.parameters["B2"].value
            logalpha = self.parameters["logalpha"].value
            alpha = np.power(10.0, logalpha)
            CTg = self.parameters["CTg"].value
            tau_e = self.parameters["tau_e"].value
            Ge = self.parameters["Ge"].value
            Me = self.parameters["Me"].value
            c_nu = self.parameters["c_nu"].value
            rho0 = self.parameters["rho0"].value
            Te = self.parameters["Te"].value

            if iso:
                B2 += CTg / Mw  # - 68.7 * dx12
                Trcorrected = T - CTg / Mw  # + 68.7 * dx12
            else:
                Trcorrected = T

            aT = np.power(
                10.0, -B1 * (Te - Trcorrected) / (B2 + Trcorrected) / (B2 + Te)
            )
            if vert:
                bT = (1 + alpha * Te) * (T + 273.15) / (1 + alpha * T) / (Te + 273.15)
            else:
                bT = 1

            self.Qprint("<hr><h3>WLF TTS Shift Factors</h3>")
            # Need T1 (to shift from) and T2 (to shift to), if we want to report aT and bT
            self.Qprint("<b>C1</b> = %g" % (B1 / (B2 + T)))
            self.Qprint("<b>C2</b> = %g<br>" % (B2 + T))

            self.Qprint("<h3>Tube Theory parameters</h3>")
            Ge /= bT
            tau_e /= aT
            self.Qprint("<b>tau_e</b> = %g" % tau_e)
            self.Qprint("<b>Ge</b> = %g<br>" % Ge)

            self.Qprint("<h3>Other Results</h3>")
            CC1 = 1.69
            CC2 = 4.17
            CC3 = -1.55
            Z = Mw / Me
            tR = tau_e * Z * Z
            tD = (
                3
                * tau_e
                * Z ** 3
                * (1 - 2 * CC1 / np.sqrt(Z) + CC2 / Z + CC3 / Z ** 1.5)
            )
            self.Qprint("<b>Z</b> = %g" % Z)
            self.Qprint("<b>tau_R</b> = %g" % tR)
            self.Qprint("<b>tau_D</b> = %g<br>" % tD)
        else:
            print("Wrong number of parameters.")
            print("   Usage: calculate_stuff Mw T isofrictional verticalshift")

    def calculate_all(self, n, x, y, ax=None, color=None, file_parameters=[]):
        """Calculate the tool for all views - In MatDB, only first view is needed """
        newxy = []
        lenx = 1e9
        for i in range(n):
            self.Qprint("<b>Series %d</b>" % (i + 1))
            xcopy = x[:, i]
            ycopy = y[:, i]
            if i == 0:
                xcopy, ycopy = self.calculate(xcopy, ycopy, ax, color, file_parameters)
            newxy.append([xcopy, ycopy])
            lenx = min(lenx, len(xcopy))
        x = np.resize(x, (lenx, n))
        y = np.resize(y, (lenx, n))
        for i in range(n):
            x[:, i] = np.resize(newxy[i][0], lenx)
            y[:, i] = np.resize(newxy[i][1], lenx)
        return x, y




class GUIToolMaterialsDatabase(BaseToolMaterialsDatabase, QTool):
    """GUI Version"""

    def __init__(self, name="", parent_app=None):
        """**Constructor**"""
        super().__init__(name, parent_app)
        self.update_parameter_table()
        # self.parent_application.update_all_ds_plots()

        # add widgets specific to the Tool here:
        self.active = True
        self.applytotheory = False
        self.actionActive.setVisible(True)
        self.actionApplyToTheory.setVisible(False)
        self.cbmaterial = QComboBox()
        self.cbmaterial.setToolTip("Choose a Material from the database")
        self.model = self.cbmaterial.model()
        i = 0
        for polymer in materials_database.keys():
            item = QStandardItem(polymer)
            item.setToolTip(materials_database[polymer].data["long"])
            self.model.appendRow(item)
            i += 1
        self.num_materials_base = i
        # self.cbmaterial.insertSeparator(i)
        for polymer in materials_user_database.keys():
            item = QStandardItem(polymer)
            item.setToolTip(materials_user_database[polymer].data["long"])
            item.setForeground(QColor("red"))
            self.model.appendRow(item)
        self.tb.addWidget(self.cbmaterial)
        connection_id = self.cbmaterial.currentIndexChanged.connect(
            self.change_material
        )

        self.actionCalculate = QAction(
            QIcon(":/Icon8/Images/new_icons/icons8-ok.png"),
            "Calculate stuff with selected Mw/T",
            self,
        )
        self.tb.addAction(self.actionCalculate)
        self.actionNew = QAction(
            QIcon(":/Icon8/Images/new_icons/icons8-add-file.png"), "New Material", self
        )
        self.tb.addAction(self.actionNew)
        self.actionEdit = QAction(
            QIcon(":/Icon8/Images/new_icons/icons8-edit-property.png"),
            "Edit/View Material Properties",
            self,
        )
        self.tb.addAction(self.actionEdit)
        self.actionCopy = QAction(
            QIcon(":/Icon8/Images/new_icons/icons8-copy-96.png"),
            "Duplicate Material",
            self,
        )
        self.tb.addAction(self.actionCopy)
        self.actionDelete = QAction(
            QIcon(":/Icon8/Images/new_icons/icons8-delete-document-96.png"),
            "Delete Material",
            self,
        )
        self.tb.addAction(self.actionDelete)
        self.actionSave = QAction(
            QIcon(":/Icon8/Images/new_icons/icons8-save.png"),
            "Save User Material Database",
            self,
        )
        self.tb.addAction(self.actionSave)
        connection_id = self.actionCalculate.triggered.connect(self.calculate_stuff)
        connection_id = self.actionNew.triggered.connect(self.new_material)
        connection_id = self.actionEdit.triggered.connect(self.edit_material)
        connection_id = self.actionCopy.triggered.connect(self.copy_material)
        connection_id = self.actionDelete.triggered.connect(self.delete_material)
        connection_id = self.actionSave.triggered.connect(self.save_usermaterials)

        self.labelPolymer = QLabel("None")
        self.labelPolymer.setFont(QFont("Times", weight=QFont.Bold))
        self.verticalLayout.insertWidget(1, self.labelPolymer)

        self.tbMwT = QToolBar()
        self.tbMwT.setIconSize(QSize(24, 24))
        lbl1 = QLabel("Mw (kDa)")
        lbl1.setFont(QFont("Times", weight=QFont.Bold))
        self.tbMwT.addWidget(lbl1)
        self.editMw = QLineEdit("1")
        self.editMw.setStyleSheet("QLineEdit { background: rgb(255, 255, 205);}")
        self.editMw.setFixedWidth(40)
        self.tbMwT.addWidget(self.editMw)
        lbl2 = QLabel("T (°C)")
        lbl2.setFont(QFont("Times", weight=QFont.Bold))
        self.tbMwT.addWidget(lbl2)
        self.editT = QLineEdit("0")
        self.editT.setStyleSheet("QLineEdit { background: rgb(255, 255, 205);}")
        self.editT.setFixedWidth(40)
        self.tbMwT.addWidget(self.editT)
        self.verticalshift = self.tbMwT.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-vertical-shift.png"),
            "Vertical shift",
        )
        self.verticalshift.setCheckable(True)
        self.verticalshift.setChecked(True)
        self.isofrictional = self.tbMwT.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-iso.png"),
            "Shift to isofrictional state",
        )
        self.isofrictional.setCheckable(True)
        self.isofrictional.setChecked(True)
        self.shiftdata = self.tbMwT.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-vertical-shift-data.png"),
            "Shift all Files in the current Application"
        )
        self.verticalLayout.insertWidget(2, self.tbMwT)
        connection_id = self.isofrictional.triggered.connect(self.handle_vert_and_iso)
        connection_id = self.verticalshift.triggered.connect(self.handle_vert_and_iso)
        connection_id = self.shiftdata.triggered.connect(self.handle_shift_data)

        init_chem_index = self.cbmaterial.findText(self.init_chem)
        if init_chem_index>-1:
            self.cbmaterial.setCurrentIndex(init_chem_index)
        self.change_material()

    def handle_vert_and_iso(self):
        self.do_plot()

    def handle_shift_data(self):
        Tr = float(self.editT.text())
        chem = self.cbmaterial.currentText()
        msg = "Selected T=%g\nSelected material=%s\n"%(Tr, chem)
        msg += "Do you want to shift all Tables in the current Dataset "
        msg += "to the chosen temperature using the WLF parameters for the chosen material?"
        ans = QMessageBox.question(
            self,
            "Shift all data",
            msg,
            buttons=(QMessageBox.Yes | QMessageBox.No),
        )
        if ans != QMessageBox.Yes:
            return
        
        # Calculate shift factors 

        B1 = self.parameters["B1"].value
        B2 = self.parameters["B2"].value
        logalpha = self.parameters["logalpha"].value
        alpha = np.power(10.0, logalpha)
        CTg = self.parameters["CTg"].value
        iso = self.isofrictional.isChecked()
        vert = self.verticalshift.isChecked()

        # Get current dataset
        ds = self.parent_application.DataSettabWidget.currentWidget()
        if not ds:
            return

        # Loop over files
        for f in ds.files:
            # Get file Current Temperature
            Tf = f.file_parameters["T"]
            Mw = f.file_parameters["Mw"]
            if "iso" in f.file_parameters:
                iso_file = (f.file_parameters["iso"].upper() == "TRUE")
            elif "isof" in f.file_parameters:
                iso_file = (f.file_parameters["isof"].upper() == "TRUE")
            else:
                iso_file=False

            if iso and not iso_file:
                B2corrected = B2 + CTg / Mw  # - 68.7 * dx12
                Trcorrected = Tr - CTg / Mw  # + 68.7 * dx12
            else:
                B2corrected = B2
                Trcorrected = Tr

            aT = np.power(10.0, -B1 * (Tf - Trcorrected) / (B2corrected + Trcorrected) / (B2corrected + Tf))
            if vert:
                bT = (1 + alpha * Tf) * (Tr + 273.15) / (1 + alpha * Tr) / (Tf + 273.15)
            else:
                bT = 1

            # Loop over file type columns
            for i, c in enumerate(f.file_type.col_names):
                if c in ["t", "time"]: # Shift horizontally to the left
                    f.data_table.data[:, i] = f.data_table.data[:, i]/aT
                elif c in ["w"]: # Shift horizontally to the right
                    f.data_table.data[:, i] = f.data_table.data[:, i]*aT
                elif c in ["G'", "G''", "Gt", "sigma_xy", "N1", "sigma"]: # Shift vertically up
                    f.data_table.data[:, i] = f.data_table.data[:, i]*bT
        
            # Change file parameter T to target Temperature
            f.file_parameters["T"] = Tr

            it = QTreeWidgetItemIterator(ds.DataSettreeWidget)
            while it.value():
                if (it.value().text(0)==f.file_name_short):
                    for i in range(ds.DataSettreeWidget.columnCount()):
                        if "T" == ds.DataSettreeWidget.headerItem().text(i):
                            it.value().setText(i, str(f.file_parameters["T"]))
                it+=1;

        self.do_plot()
        


    def change_material(self):
        selected_material_name = self.cbmaterial.currentText()
        if self.cbmaterial.currentIndex() < self.num_materials_base:
            dbindex = 1
        else:
            dbindex = 0
        self.labelPolymer.setText(
            materials_db[dbindex][selected_material_name].data["long"]
        )
        for k in materials_db[dbindex][selected_material_name].data.keys():
            self.set_param_value(
                k, materials_db[dbindex][selected_material_name].data[k]
            )
        self.update_parameter_table()
        self.do_plot()

    def new_material(self):
        # Dialog to ask for short name. Repeat until the name is not in the user's database or CANCEL
        ok = False
        while not ok:
            name, ok = QInputDialog.getText(
                self, "New name", "Enter the short name of the new material:"
            )
            if not ok:
                return
            if name in materials_user_database:
                QMessageBox.warning(
                    self, "New name", "Error: The name already exists in your database"
                )
                ok = False

        # Create new material with empty  parameters and open the edit dialog
        newmaterial = polymer_data.polymer(
            name=name,
            long="Long Name",
            author="Author",
            date="dd/mm/yyyy",
            source="lab",
            comment="comment",
            B1=900,
            B2=100,
            logalpha=-3,
            CTg=0,
            tau_e=1.0e-6,
            Ge=1.0e6,
            Me=1.6,
            c_nu=0.1,
            rho0=1.0,
            chem="C6H6",
            Te=25,
            M0=0,
        )
        newmaterial.data["name"] = name
        materials_user_database[name] = newmaterial
        item = QStandardItem(name)
        item.setToolTip(materials_user_database[name].data["long"])
        item.setForeground(QColor("red"))
        self.model.appendRow(item)
        self.cbmaterial.setCurrentText(name)
        self.edit_material()

    """
    Edit the parameters of a user material.
        - dbindex {int} -- Index of the database to use (0 user, 1 general)
    """

    def edit_material(self):
        selected_material_name = self.cbmaterial.currentText()
        if self.cbmaterial.currentIndex() < self.num_materials_base:
            QMessageBox.warning(
                self,
                "Edit material parameters",
                "Error: Only user materials can be edited.",
            )
            return
        material = materials_user_database[selected_material_name]
        d = EditMaterialParametersDialog(self, material, self.parameters)
        if d.exec_():
            for p in d.param_dict:
                if isinstance(material.data[p], str):
                    material.data[p] = d.param_dict[p].text()
                else:
                    try:
                        material.data[p] = float(d.param_dict[p].text())
                    except Exception as e:
                        print(e)
                self.set_param_value(p, material.data[p])
            self.change_material()

    def save_usermaterials(self):
        AppData_path = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        file_user_database = os.path.join(AppData_path, "user_database.npy")
        np.save(file_user_database, materials_user_database)
        msg = "Saved user database in '%s'" % file_user_database
        QMessageBox.information(self, 'Saved', msg)

    def copy_material(self):
        # Dialog to ask for short name. Repeat until the name is not in the user's database or CANCEL
        name = ""
        ok = False
        while not ok:
            name, ok = QInputDialog.getText(
                self, "New name", "Enter the name of the new parameter:"
            )
            if not ok:
                return
            if name in materials_user_database:
                QMessageBox.warning(
                    self, "New name", "Error: The name already exists in your database"
                )
                ok = False
        # Create new user material with same parameters as source material and new NAME
        # newpar=
        selected_material_name = self.cbmaterial.currentText()
        if self.cbmaterial.currentIndex() < self.num_materials_base:
            dbindex = 1
        else:
            dbindex = 0
        aux = materials_db[dbindex][selected_material_name].data
        newmaterial = polymer_data.polymer(
            name=name,
            long=aux["long"],
            author="Alexei Likhtman",
            date="17/03/2006",
            source=aux["source"],
            comment=aux["comment"],
            B1=aux["B1"],
            B2=aux["B2"],
            logalpha=aux["logalpha"],
            CTg=aux["CTg"],
            tau_e=aux["tau_e"],
            Ge=aux["Ge"],
            Me=aux["Me"],
            c_nu=aux["c_nu"],
            rho0=aux["rho0"],
            chem=aux["chem"],
            Te=aux["Te"],
            M0=aux["M0"],
        )
        materials_user_database[name] = newmaterial
        item = QStandardItem(name)
        item.setToolTip(materials_user_database[name].data["long"])
        item.setForeground(QColor("red"))
        self.model.appendRow(item)

    def delete_material(self):
        # Check that the material is in the user database
        selected_material_name = self.cbmaterial.currentText()
        if self.cbmaterial.currentIndex() < self.num_materials_base:
            QMessageBox.warning(
                self,
                "Dekete material parameters",
                "Error: Only user materials can be deleted.",
            )
            return
        # Dialog to ask for confimarion
        ans = QMessageBox.question(
            self,
            "Delete material parameters",
            "Do you want to delete the material %s?" % selected_material_name,
            buttons=(QMessageBox.Yes | QMessageBox.No),
        )
        # Delete from ComboBox and User Material dictionary
        if ans == QMessageBox.Yes:
            self.cbmaterial.removeItem(self.cbmaterial.currentIndex())
            materials_user_database.pop(selected_material_name)

    def calculate_stuff(self, line="", file_parameters=[]):
        if "Mw" in file_parameters:
            Mw = float(file_parameters["Mw"])
        else:
            Mw = float(self.editMw.text())
        if Mw == 0:
            Mw = 1
        if "T" in file_parameters:
            T = float(file_parameters["T"])
        else:
            T = float(self.editT.text())
        B1 = self.parameters["B1"].value
        B2 = self.parameters["B2"].value
        logalpha = self.parameters["logalpha"].value
        alpha = np.power(10.0, logalpha)
        CTg = self.parameters["CTg"].value
        tau_e = self.parameters["tau_e"].value
        Ge = self.parameters["Ge"].value
        Me = self.parameters["Me"].value
        c_nu = self.parameters["c_nu"].value
        rho0 = self.parameters["rho0"].value
        Te = self.parameters["Te"].value
        iso = self.isofrictional.isChecked()
        vert = self.verticalshift.isChecked()

        if iso:
            B2 += CTg / Mw  # - 68.7 * dx12
            Trcorrected = T - CTg / Mw  # + 68.7 * dx12
        else:
            Trcorrected = T

        aT = np.power(10.0, -B1 * (Te - Trcorrected) / (B2 + Trcorrected) / (B2 + Te))
        if vert:
            bT = (1 + alpha * Te) * (T + 273.15) / (1 + alpha * T) / (Te + 273.15)
        else:
            bT = 1

        tab_data = [
            ["<b>Material &</b>", "<b>Temperature</b>"],
        ]
        tab_data.append(["<b>Chemistry</b>", self.parameters["long"].value])
        tab_data.append(["<b>Mw</b>", "%g" % Mw])
        tab_data.append(["<b>T</b>", "%g" % T])
        tab_data.append(["<b>WLF Shift</b>", "<b>Factors</b>"])
        tab_data.append(["<b>C1</b>", "%g" % (B1 / (B2 + T))])
        tab_data.append(["<b>C2</b>", "%g" % (B2 + T)])
        tab_data.append(["<b>Polymer &</b>", "<b>Tube dynamics</b>"])
        Ge /= bT
        tau_e /= aT
        tab_data.append(["<b>tau_e</b>", "%g" % tau_e])
        tab_data.append(["<b>Ge</b>", "%g" % Ge])
        CC1 = 1.69
        CC2 = 4.17
        CC3 = -1.55
        Z = Mw / Me
        tR = tau_e * Z * Z
        tD = 3 * tau_e * Z ** 3 * (1 - 2 * CC1 / np.sqrt(Z) + CC2 / Z + CC3 / Z ** 1.5)
        tab_data.append(["<b>Z</b>", "%g" % Z])
        tab_data.append(["<b>tau_R</b>", "%g" % tR])
        tab_data.append(["<b>tau_D</b>", "%g" % tD])
        self.Qprint(tab_data)
