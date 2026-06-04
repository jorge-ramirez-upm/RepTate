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
# Copyright (2017-2026): Jorge Ramirez, Victor Boudara, Universidad Politecnica de Madrid, University of Leeds
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
"""LP2R linear viscoelastic theory backed by the pybind11 solver."""

from typing import Any, ClassVar
import numpy as np
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
)

from RepTate.core.Parameter import OptType, Parameter, ParameterType
from RepTate.core.typing import ApplicationManagerLike, AxesArray, DataSetLike, FileLike
from RepTate.core.units import convert_array_to_internal, parse_column_label
from RepTate.gui.QTheory import QTheory
from RepTate.theories import _lp2r  # pyright: ignore[reportAttributeAccessIssue]
from RepTate.theories.theory_helpers import EditMWDDialog, GetMwdRepTate
from RepTate.tools.ToolMaterialsDatabase import (
    check_chemistry,
    get_single_parameter,
)

QAbstractItemView_any: Any = QAbstractItemView
QDialogButtonBox_any: Any = QDialogButtonBox


class LP2RAdvancedControlsDialog(QDialog):
    """Edit the LP2R resource-file style controls."""

    def __init__(self, parent, control_names):
        super().__init__(parent)
        self.parent_theory = parent
        self.edits = {}

        layout = QVBoxLayout()
        form = QFormLayout()
        for name in control_names:
            edit = QLineEdit()
            edit.setText("%g" % self.parent_theory.parameters[name].value)
            edit.setToolTip(self.parent_theory.parameters[name].description)
            self.edits[name] = edit
            form.addRow(name, edit)
        layout.addLayout(form)

        button_box = QDialogButtonBox_any(QDialogButtonBox_any.Ok | QDialogButtonBox_any.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        self.setLayout(layout)
        self.setWindowTitle("Advanced LP2R Controls")

    def values(self):
        return {name: float(edit.text()) for name, edit in self.edits.items()}


class LP2RLognormalComponentDialog(QDialog):
    """Edit one LP2R lognormal polymer component."""

    def __init__(self, parent, component=None):
        super().__init__(parent)
        self.setWindowTitle("LP2R Lognormal Component")
        component = component or {}

        layout = QVBoxLayout()
        form = QFormLayout()
        self.label_edit = QLineEdit(component.get("label", "Lognormal"))
        self.weight_edit = QLineEdit("%g" % component.get("weight", 1.0))
        self.npoly_edit = QLineEdit("%g" % component.get("npoly", 8))
        self.mw_edit = QLineEdit("%g" % component.get("Mw", 100.0))
        self.pdi_edit = QLineEdit("%g" % component.get("PDI", 1.05))
        form.addRow("Label", self.label_edit)
        form.addRow("Weight fraction", self.weight_edit)
        form.addRow("npoly", self.npoly_edit)
        form.addRow("Mw [kg/mol]", self.mw_edit)
        form.addRow("PDI", self.pdi_edit)
        layout.addLayout(form)

        button_box = QDialogButtonBox_any(QDialogButtonBox_any.Ok | QDialogButtonBox_any.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def component(self):
        return TheoryLP2RLVE.make_lognormal_component(
            weight=float(self.weight_edit.text()),
            npoly=int(float(self.npoly_edit.text())),
            mw=float(self.mw_edit.text()),
            pdi=float(self.pdi_edit.text()),
            label=self.label_edit.text().strip() or "Lognormal",
        )


class LP2RComponentsDialog(QDialog):
    """Display and edit the list of LP2R polymer components."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent_theory = parent
        self.components = parent.copy_lp2r_components(parent.lp2r_components)
        self.setWindowTitle("LP2R Components")

        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView_any.SelectRows)
        self.table.setSelectionMode(QAbstractItemView_any.SingleSelection)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Type", "Weight", "Label", "Source", "Summary"]
        )
        layout.addWidget(self.table)

        self.add_lognormal_button = QPushButton("Add lognormal")
        self.add_mwd_button = QPushButton("Add MWD")
        self.get_mwd_button = QPushButton("Get MWD (MWD app)")
        self.get_mwd_file_button = QPushButton("Get MWD (.gpc file)")
        self.remove_button = QPushButton("Remove")
        self.normalize_button = QPushButton("Normalize weights")
        self.add_lognormal_button.setIcon(
            QIcon(":/Images/Images/new_icons/icons8-plus.png")
        )
        self.add_mwd_button.setIcon(
            QIcon(":/Images/Images/new_icons/icons8-insert-table.png")
        )
        self.get_mwd_button.setIcon(
            QIcon(":/Images/Images/new_icons/icons8-categorize.png")
        )
        self.get_mwd_file_button.setIcon(
            QIcon(":/Icons/Images/new_icons/MWD.png")
        )
        self.remove_button.setIcon(
            QIcon(":/Images/Images/new_icons/icons8-minus.png")
        )
        self.normalize_button.setIcon(
            QIcon(":/Images/Images/new_icons/icons8-equal-sign.png")
        )

        add_buttons = QHBoxLayout()
        for button in (
            self.add_lognormal_button,
            self.add_mwd_button,
            self.get_mwd_button,
            self.get_mwd_file_button,
        ):
            add_buttons.addWidget(button)
        layout.addLayout(add_buttons)

        edit_buttons = QHBoxLayout()
        for button in (
            self.remove_button,
            self.normalize_button,
        ):
            edit_buttons.addWidget(button)
        layout.addLayout(edit_buttons)

        button_box = QDialogButtonBox_any(QDialogButtonBox_any.Ok | QDialogButtonBox_any.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        self.setLayout(layout)

        self.add_lognormal_button.clicked.connect(self.add_lognormal)
        self.add_mwd_button.clicked.connect(self.add_mwd)
        self.get_mwd_button.clicked.connect(self.get_mwd_reptate)
        self.get_mwd_file_button.clicked.connect(self.import_mwd_gpc)
        self.remove_button.clicked.connect(self.remove_selected)
        self.normalize_button.clicked.connect(self.normalize_weights)
        self.table.cellDoubleClicked.connect(lambda *_: self.edit_selected())
        self.refresh()

    def refresh(self):
        self.table.setRowCount(len(self.components))
        for row, component in enumerate(self.components):
            values = [
                component["kind"],
                "%.6g" % component["weight"],
                component.get("label", ""),
                component.get("source", ""),
                TheoryLP2RLVE.component_summary(component),
            ]
            for col, value in enumerate(values):
                self.table.setItem(row, col, QTableWidgetItem(value))
        self.table.resizeColumnsToContents()
        if self.components and self.table.currentRow() < 0:
            self.table.selectRow(0)

    def selected_row(self):
        indexes = self.table.selectionModel().selectedRows()
        if indexes:
            return indexes[0].row()
        row = self.table.currentRow()
        if 0 <= row < len(self.components):
            return row
        if len(self.components) == 1:
            return 0
        return None

    def add_lognormal(self):
        dialog = LP2RLognormalComponentDialog(self.parent_theory)
        if dialog.exec_():
            try:
                self.components.append(dialog.component())
            except ValueError as exc:
                QMessageBox.warning(self, "LP2R Components", str(exc))
                return
            self.refresh()

    def add_mwd(self):
        dialog = EditMWDDialog(self.parent_theory, [50.0, 120.0], [0.4, 0.6], 200)
        if dialog.exec_():
            component = self.parent_theory.component_from_mwd_dialog(dialog)
            if component is not None:
                self.components.append(component)
                self.refresh()

    def get_mwd_reptate(self):
        get_dict = self.parent_theory._collect_mwd_getters()
        if not get_dict:
            QMessageBox.warning(
                self, "Get MW distribution", 'No "Discretize MWD" theory found'
            )
            return

        dialog = GetMwdRepTate(self.parent_theory, get_dict, "Select Discretized MWD")
        if dialog.exec_() and dialog.btngrp.checkedButton() is not None:
            _, success1 = self.parent_theory.set_param_value(
                "tau_e", dialog.taue_text.text()
            )
            _, success2 = self.parent_theory.set_param_value(
                "Me", dialog.Me_text.text()
            )
            if not success1 * success2:
                self.parent_theory.Qprint("Could not understand Me or tau_e, try again")
                return
            item = dialog.btngrp.checkedButton().text()
            masses, weights = get_dict[item]()
            try:
                self.components.append(
                    TheoryLP2RLVE.make_mwd_component(
                        masses,
                        weights,
                        label=item,
                        source="RepTate",
                    )
                )
            except ValueError as exc:
                QMessageBox.warning(self, "LP2R Components", str(exc))
                return
            self.refresh()

    def import_mwd_gpc(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open MWD .gpc file",
            "",
            "GPC Files (*.gpc);;All Files (*)",
        )
        if not path:
            return
        try:
            masses, weights = TheoryLP2RLVE.read_gpc_mwd(path)
            self.components.append(
                TheoryLP2RLVE.make_mwd_component(
                    masses,
                    weights,
                    label=path.split("/")[-1].split("\\")[-1],
                    source="gpc",
                )
            )
        except ValueError as exc:
            QMessageBox.warning(self, "LP2R Components", str(exc))
            return
        self.refresh()

    def edit_selected(self):
        row = self.selected_row()
        if row is None:
            return
        component = self.components[row]
        if component["kind"] == "lognormal":
            dialog = LP2RLognormalComponentDialog(self.parent_theory, component)
            if dialog.exec_():
                try:
                    self.components[row] = dialog.component()
                except ValueError as exc:
                    QMessageBox.warning(self, "LP2R Components", str(exc))
                    return
        else:
            dialog = EditMWDDialog(
                self.parent_theory,
                component["masses"],
                component["weights"],
                200,
            )
            if dialog.exec_():
                updated = self.parent_theory.component_from_mwd_dialog(
                    dialog,
                    label=component.get("label", "MWD"),
                    source=component.get("source", "manual"),
                    weight=component.get("weight", 1.0),
                )
                if updated is not None:
                    self.components[row] = updated
        self.refresh()

    def remove_selected(self):
        row = self.selected_row()
        if row is None:
            return
        del self.components[row]
        self.refresh()

    def normalize_weights(self):
        try:
            self.components = TheoryLP2RLVE.normalize_component_weights(
                self.components
            )
        except ValueError as exc:
            QMessageBox.warning(self, "LP2R Components", str(exc))
            return
        self.refresh()

    def accept(self):
        try:
            self.components = TheoryLP2RLVE.validate_lp2r_components(self.components)
        except ValueError as exc:
            QMessageBox.warning(self, "LP2R Components", str(exc))
            return
        super().accept()


class TheoryLP2RLVE(QTheory):
    """Linear viscoelastic predictions from the LP2R solver.

    RepTate owns GUI state and parameter handling, while the pybind11 solver owns
    the numerical relaxation and spectra calculation.
    """

    thname: ClassVar[str] = "LP2R LVE"
    description: ClassVar[str] = "Linear rheology of polydisperse linear polymers"
    citations: ClassVar[list[str]] = ["Das, C. and Read, D. J., J. Rheol. 2023, 67, 693–721."]
    doi: ClassVar[list[str]] = ["https://doi.org/10.1122/8.0000605"]
    html_help_file: ClassVar[str] = "http://reptate.readthedocs.io/manual/Applications/LVE/Theory/theory.html"
    single_file: ClassVar[bool] = True
    DEFAULT_MW = 100.0
    DEFAULT_PDI = 1.03
    DEFAULT_NPOLY = 50
    ADVANCED_CONTROLS = [
        "alpha",
        "t_cr_start",
        "delta_cr",
        "b_zeta",
        "a_eq",
        "b_eq",
        "ret_pref",
        "ret_pref_0",
        "ret_switch_exponent",
        "rept_switch_factor",
        "rouse_switch_factor",
        "disentanglement_switch",
        "start_time",
        "time_ratio",
    ]

    def __init__(self, name: str = "", parent_dataset: DataSetLike | None = None, axarr: AxesArray | None = None) -> None:
        """Constructor."""
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate
        self.has_modes = False
        self.solver = None

        self.parameters["Mw"] = Parameter(
            name="Mw",
            value=self.DEFAULT_MW,
            description="Weight-average molar mass of the lognormal component",
            type=ParameterType.real,
            opt_type=OptType.nopt,
            min_value=0,
            display_flag=False,
            quantity="molar_mass",
            internal_unit="kg/mol",
            display_unit="kg/mol",
        )
        self.parameters["PDI"] = Parameter(
            name="PDI",
            value=self.DEFAULT_PDI,
            description="Polydispersity index of the lognormal component",
            type=ParameterType.real,
            opt_type=OptType.nopt,
            min_value=1.0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["n"] = Parameter(
            name="n",
            value=self.DEFAULT_NPOLY,
            description="Number of lognormal bins",
            type=ParameterType.integer,
            opt_type=OptType.const,
            min_value=1,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["MK"] = Parameter(
            name="MK",
            value=0.5,
            description="Kuhn molar mass",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            quantity="molar_mass",
            internal_unit="kg/mol",
            display_unit="kg/mol",
        )
        self.parameters["Me"] = Parameter(
            name="Me",
            value=5.0,
            description="Entanglement molar mass",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            quantity="molar_mass",
            internal_unit="kg/mol",
            display_unit="kg/mol",
        )
        self.parameters["G0"] = Parameter(
            name="G0",
            value=2.0e5,
            description="Plateau modulus",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            quantity="stress",
            internal_unit="Pa",
            display_unit="Pa",
        )
        self.parameters["tau_e"] = Parameter(
            name="tau_e",
            value=1.0e-5,
            description="Entanglement time",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            quantity="time",
            internal_unit="s",
            display_unit="s",
        )
        self.parameters["G_glass"] = Parameter(
            name="G_glass",
            value=1.0e9,
            description="Glass modulus",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            quantity="stress",
            internal_unit="Pa",
            display_unit="Pa",
        )
        self.parameters["tau_glass"] = Parameter(
            name="tau_glass",
            value=1.0e-8,
            description="Glass relaxation time",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            quantity="time",
            internal_unit="s",
            display_unit="s",
        )
        self.parameters["beta_glass"] = Parameter(
            name="beta_glass",
            value=0.7,
            description="Glass KWW exponent",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            max_value=1,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["freq_ratio"] = Parameter(
            name="freq_ratio",
            value=1.2,
            description="Ratio between consecutive calculated frequencies",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=1.0,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["alpha"] = Parameter(
            name="alpha",
            value=1.0,
            description="LP2R constraint-release alpha parameter",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["t_cr_start"] = Parameter(
            name="t_cr_start",
            value=1.0,
            description="Constraint-release start time",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["delta_cr"] = Parameter(
            name="delta_cr",
            value=0.30,
            description="Fractional tube-constraint drop at CR events",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["b_zeta"] = Parameter(
            name="b_zeta",
            value=2.0,
            description="LP2R B_zeta resource parameter",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["a_eq"] = Parameter(
            name="a_eq",
            value=2.0,
            description="LP2R A_eq resource parameter",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["b_eq"] = Parameter(
            name="b_eq",
            value=10.0,
            description="LP2R B_eq resource parameter",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["ret_pref"] = Parameter(
            name="ret_pref",
            value=0.189,
            description="Long-time arm-retraction prefactor",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["ret_pref_0"] = Parameter(
            name="ret_pref_0",
            value=0.020,
            description="Short-time arm-retraction prefactor",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["ret_switch_exponent"] = Parameter(
            name="ret_switch_exponent",
            value=0.42,
            description="Arm-retraction prefactor switch exponent",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["rept_switch_factor"] = Parameter(
            name="rept_switch_factor",
            value=1.664,
            description="CLF-to-reptation switch factor",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["rouse_switch_factor"] = Parameter(
            name="rouse_switch_factor",
            value=1.5,
            description="Minimum bare entanglements for entangled dynamics",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["disentanglement_switch"] = Parameter(
            name="disentanglement_switch",
            value=1.0,
            description="LP2R disentanglement switch",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["start_time"] = Parameter(
            name="start_time",
            value=1.0e-3,
            description="Start time for LP2R relaxation integration",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["time_ratio"] = Parameter(
            name="time_ratio",
            value=1.02,
            description="Ratio between consecutive LP2R relaxation time steps",
            type=ParameterType.real,
            opt_type=OptType.const,
            min_value=1.0,
            display_flag=False,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )

        self.get_material_parameters()
        self._read_default_component_params_from_first_file()
        self.autocalculate = False
        self.MWD_m = [50.0, 120.0]
        self.MWD_phi = [0.4, 0.6]
        self.lp2r_components = [self.default_lognormal_component()]

        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))

        self.edit_components_action = tb.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-edit-file.png"),
            "LP2R components",
        )

        self.advanced_controls_action = tb.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-maintenance.png"),
            "Advanced LP2R controls",
        )
        self.thToolsLayout.insertWidget(0, tb)
        self.edit_components_action.triggered.connect(self.edit_lp2r_components)
        self.advanced_controls_action.triggered.connect(self.edit_advanced_controls)

    def edit_advanced_controls(self):
        """Open a dialog for the LP2R resource-file style controls."""
        dialog = LP2RAdvancedControlsDialog(self, self.ADVANCED_CONTROLS)
        if dialog.exec_():
            try:
                values = dialog.values()
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Advanced LP2R controls",
                    "All LP2R controls must be numeric.",
                )
                return
            for name, value in values.items():
                self.parameters[name].value = value

    def edit_lp2r_components(self):
        """Open the LP2R polymer component manager."""
        dialog = LP2RComponentsDialog(self)
        if dialog.exec_():
            self.set_lp2r_components(dialog.components)

    def get_material_parameters(self):
        """Get common LP2R material parameters from the materials database."""
        success = super().get_material_parameters()
        if success:
            self._set_g0_from_material_ge()
        return success

    def _set_g0_from_material_ge(self):
        """Set LP2R G0 from the material database Ge value when available."""
        try:
            fparam = self.parent_dataset.files[0].file_parameters
            chem = fparam["chem"]
        except (AttributeError, IndexError, KeyError):
            return False
        dbindex = check_chemistry(chem)
        if dbindex < 0:
            return False
        ge, success = get_single_parameter(chem, "Ge", fparam, dbindex)
        if success:
            self.parameters["G0"].value = 0.8 * ge
            return True
        return False

    def _read_default_component_params_from_first_file(self):
        """Use valid first-file Mw/Mn/PDI values for the default component."""
        success = False
        self.parameters["Mw"].value = self.DEFAULT_MW
        self.parameters["PDI"].value = self.DEFAULT_PDI
        self.parameters["n"].value = self.DEFAULT_NPOLY
        try:
            fparam = self.parent_dataset.files[0].file_parameters
        except (AttributeError, IndexError):
            return success

        mw = self._positive_file_parameter(fparam, "Mw")
        mn = self._positive_file_parameter(fparam, "Mn")
        pdi = self._positive_file_parameter(fparam, "PDI")
        if pdi is not None and pdi < 1.0:
            pdi = None

        if pdi is None and mw is not None and mn is not None:
            derived_pdi = mw / mn
            if derived_pdi >= 1.0 and np.isfinite(derived_pdi):
                pdi = derived_pdi
        if mw is None and mn is not None and pdi is not None:
            derived_mw = mn * pdi
            if derived_mw > 0 and np.isfinite(derived_mw):
                mw = derived_mw

        if mw is not None:
            self.parameters["Mw"].value = mw
            success = True
        if pdi is not None:
            self.parameters["PDI"].value = pdi
            success = True
        return success

    @staticmethod
    def _positive_file_parameter(file_parameters, name):
        """Return a positive finite file parameter, otherwise None."""
        try:
            value = float(file_parameters[name])
        except (KeyError, TypeError, ValueError):
            return None
        if value > 0.0 and np.isfinite(value):
            return value
        return None

    def default_lognormal_component(self):
        """Return a default lognormal component from the visible Mw/PDI/n values."""
        npoly = self.parameter_int("n")
        mw = self.parameter_float("Mw")
        pdi = self.parameter_float("PDI")
        return self.make_lognormal_component(
            weight=1.0,
            npoly=npoly,
            mw=mw,
            pdi=pdi,
            label="Lognormal",
            source="parameters",
        )

    def current_lp2r_components(self):
        """Return LP2R components, syncing the default component from parameters."""
        components = self.copy_lp2r_components(self.lp2r_components)
        if (
            len(components) == 1
            and components[0].get("kind") == "lognormal"
            and components[0].get("source") == "parameters"
        ):
            return [self.default_lognormal_component()]
        return components

    @staticmethod
    def copy_lp2r_components(components):
        """Return a plain-Python deep copy of LP2R component dictionaries."""
        copied = []
        for component in components:
            new_component = dict(component)
            if "masses" in new_component:
                new_component["masses"] = list(new_component["masses"])
            if "weights" in new_component:
                new_component["weights"] = list(new_component["weights"])
            copied.append(new_component)
        return copied

    @staticmethod
    def make_lognormal_component(
        weight=1.0,
        npoly=8,
        mw=100.0,
        pdi=1.05,
        label="Lognormal",
        source="manual",
    ):
        """Create and validate a lognormal LP2R component."""
        component = {
            "kind": "lognormal",
            "weight": float(weight),
            "npoly": int(npoly),
            "Mw": float(mw),
            "PDI": float(pdi),
            "label": str(label or "Lognormal"),
            "source": str(source or "manual"),
        }
        return TheoryLP2RLVE.validate_lp2r_component(component)

    @staticmethod
    def make_mwd_component(
        masses,
        weights,
        weight=1.0,
        label="MWD",
        source="manual",
    ):
        """Create and validate a discrete-MWD LP2R component."""
        masses, weights = TheoryLP2RLVE._normalise_discrete_distribution(
            masses,
            weights,
        )
        component = {
            "kind": "mwd",
            "weight": float(weight),
            "masses": masses,
            "weights": weights,
            "label": str(label or "MWD"),
            "source": str(source or "manual"),
        }
        return TheoryLP2RLVE.validate_lp2r_component(component)

    @staticmethod
    def validate_lp2r_component(component):
        """Validate one LP2R component and return a normalized copy."""
        component = dict(component)
        kind = component.get("kind")
        if kind not in ("lognormal", "mwd"):
            raise ValueError("LP2R component kind must be lognormal or mwd")
        weight = float(component.get("weight", 1.0))
        if weight < 0:
            raise ValueError("LP2R component weight fractions must be non-negative")
        component["weight"] = weight
        component["label"] = str(component.get("label") or kind)
        component["source"] = str(component.get("source") or "manual")
        if kind == "lognormal":
            component["npoly"] = int(component.get("npoly", component.get("n", 8)))
            component["Mw"] = float(component.get("Mw", 100.0))
            component["PDI"] = float(component.get("PDI", 1.05))
            if component["npoly"] <= 0:
                raise ValueError("Lognormal npoly must be positive")
            if component["Mw"] <= 0:
                raise ValueError("Lognormal Mw must be positive")
            if component["PDI"] < 1.0:
                raise ValueError("Lognormal PDI must be at least 1")
        else:
            masses, weights = TheoryLP2RLVE._normalise_discrete_distribution(
                component.get("masses", []),
                component.get("weights", []),
            )
            component["masses"] = masses
            component["weights"] = weights
        return component

    @staticmethod
    def validate_lp2r_components(components):
        """Validate the full LP2R component list."""
        validated = [
            TheoryLP2RLVE.validate_lp2r_component(component)
            for component in components
        ]
        if not validated:
            raise ValueError("LP2R needs at least one polymer component")
        if sum(component["weight"] for component in validated) <= 0:
            raise ValueError("LP2R component weights must have positive total weight")
        return validated

    @staticmethod
    def normalize_component_weights(components):
        """Normalize component weight fractions to sum to one."""
        normalized = TheoryLP2RLVE.validate_lp2r_components(components)
        total = sum(component["weight"] for component in normalized)
        for component in normalized:
            component["weight"] /= total
        return normalized

    @staticmethod
    def component_summary(component):
        """Return a compact table summary for one LP2R component."""
        if component["kind"] == "lognormal":
            return "npoly=%d, Mw=%g, PDI=%g" % (
                component["npoly"],
                component["Mw"],
                component["PDI"],
            )
        return "%d MWD points" % len(component["masses"])

    @staticmethod
    def component_table(components):
        """Return an HTML-table-compatible summary of LP2R components."""
        table = [["#", "Type", "Weight", "Label", "Source", "Details"]]
        for i, component in enumerate(components, 1):
            table.append(
                [
                    str(i),
                    component["kind"],
                    "%.6g" % component["weight"],
                    component.get("label", ""),
                    component.get("source", ""),
                    TheoryLP2RLVE.component_summary(component),
                ]
            )
        return table

    @staticmethod
    def migrate_old_lp2r_state(extra_data=None, parameters=None):
        """Return components migrated from older LP2R hidden MWD state."""
        extra_data = extra_data or {}
        parameters = parameters or {}
        if "lp2r_components" in extra_data:
            return TheoryLP2RLVE.validate_lp2r_components(
                extra_data["lp2r_components"]
            )
        if "MWD_m" in extra_data and "MWD_phi" in extra_data:
            return [
                TheoryLP2RLVE.make_mwd_component(
                    extra_data["MWD_m"],
                    extra_data["MWD_phi"],
                    label="MWD",
                    source="legacy",
                )
            ]
        if "discrete_masses" in parameters and "discrete_weights" in parameters:
            masses_value = getattr(parameters["discrete_masses"], "value", parameters["discrete_masses"])
            weights_value = getattr(parameters["discrete_weights"], "value", parameters["discrete_weights"])
            masses, weights = TheoryLP2RLVE._parse_discrete_distribution(
                masses_value,
                weights_value,
            )
            return [
                TheoryLP2RLVE.make_mwd_component(
                    masses,
                    weights,
                    label="MWD",
                    source="legacy",
                )
            ]
        return None

    @staticmethod
    def read_gpc_mwd(path):
        """Read a RepTate .gpc file as kg/mol masses and normalized weights."""
        masses = []
        density = []
        mass_unit = "kg/mol"
        with open(path, "r", encoding="latin-1") as file_handle:
            for line in file_handle:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                fields = stripped.split()
                if len(fields) >= 2:
                    label, unit, _ = parse_column_label(
                        "%s %s" % (fields[0], fields[1])
                        if fields[0] == "M" and fields[1].startswith(("(", "["))
                        else fields[0]
                    )
                    if label == "M" and unit:
                        mass_unit = unit
                        continue
                if len(fields) < 2:
                    continue
                try:
                    mass = float(fields[0])
                    value = float(fields[1])
                except ValueError:
                    continue
                if mass > 0 and np.isfinite(mass) and np.isfinite(value):
                    masses.append(mass)
                    density.append(max(value, 0.0))
        if len(masses) < 1:
            raise ValueError("No MWD data found in .gpc file")

        order = np.argsort(masses)
        masses = convert_array_to_internal(
            np.asarray(masses, dtype=float)[order],
            mass_unit,
            "kg/mol",
        )
        density = np.asarray(density, dtype=float)[order]
        if len(masses) == 1:
            weights = np.ones(1)
        else:
            logm = np.log10(masses)
            widths = np.empty(len(masses))
            widths[1:-1] = 0.5 * (logm[2:] - logm[:-2])
            widths[0] = logm[1] - logm[0]
            widths[-1] = logm[-1] - logm[-2]
            weights = density * np.maximum(widths, 0.0)
        return TheoryLP2RLVE._normalise_discrete_distribution(masses, weights)

    def _clear_table(self, tt):
        """Leave the theory table empty after validation errors or cancellation."""
        tt.num_rows = 0
        tt.data = np.zeros((0, tt.num_columns))

    def _report_progress(self, progress, last_percent):
        """Report relaxation progress as GLaMM-style dash markers."""
        percent = int(100.0 * max(0.0, min(1.0, progress)))
        while percent >= last_percent + 10 and last_percent < 100:
            self.Qprint("-", end="")
            last_percent += 10
        return last_percent

    @staticmethod
    def _parse_number_list(value, name):
        """Parse a comma, semicolon, or whitespace separated list of floats."""
        tokens = str(value).replace(",", " ").replace(";", " ").split()
        if not tokens:
            raise ValueError("%s must contain at least one value" % name)
        try:
            return [float(token) for token in tokens]
        except ValueError as exc:
            raise ValueError("%s must contain only numbers" % name) from exc

    @classmethod
    def _parse_discrete_distribution(cls, masses_value, weights_value):
        """Parse and validate discrete mass and weight arrays."""
        masses = cls._parse_number_list(masses_value, "discrete_masses")
        weights = cls._parse_number_list(weights_value, "discrete_weights")
        if len(masses) != len(weights):
            raise ValueError("discrete_masses and discrete_weights must have the same length")
        if any(m <= 0 for m in masses):
            raise ValueError("discrete_masses values must be positive")
        if any(w <= 0 for w in weights):
            raise ValueError("discrete_weights values must be positive")
        if sum(weights) <= 0:
            raise ValueError("discrete_weights must have positive total weight")
        return masses, weights

    @staticmethod
    def _format_number_list(values):
        """Format numeric arrays for storage in string theory parameters."""
        return ", ".join("%.12g" % value for value in values)

    @classmethod
    def _normalise_discrete_distribution(cls, masses, weights):
        """Validate and normalize a discrete MWD in RepTate internal units."""
        masses = [float(mass) for mass in masses]
        weights = [float(weight) for weight in weights]
        if len(masses) != len(weights) or not masses:
            raise ValueError("MWD masses and weights must be non-empty and have the same length")
        if any(mass <= 0 for mass in masses):
            raise ValueError("MWD masses must be positive")
        if any(weight < 0 for weight in weights):
            raise ValueError("MWD weights must be non-negative")
        total_weight = sum(weights)
        if total_weight <= 0:
            raise ValueError("MWD weights must have positive total weight")
        return masses, [weight / total_weight for weight in weights]

    def set_discrete_distribution_from_mwd(self, masses, weights):
        """Append one LP2R MWD component from masses and weights."""
        component = self.make_mwd_component(masses, weights)
        self.add_lp2r_component(component)
        self.Qprint("Added LP2R MWD component with %d points" % len(component["masses"]))
        self.Qprint('<font color=green><b>Press "Calculate" to update theory</b></font>')

    def set_lp2r_components(self, components):
        """Set the full LP2R polymer component list."""
        self.lp2r_components = self.validate_lp2r_components(components)
        mwd_components = [
            component
            for component in self.lp2r_components
            if component["kind"] == "mwd"
        ]
        if mwd_components:
            self.MWD_m = np.copy(mwd_components[-1]["masses"])
            self.MWD_phi = np.copy(mwd_components[-1]["weights"])
        self.Qprint("LP2R has %d polymer component(s)" % len(self.lp2r_components))

    def add_lp2r_component(self, component):
        """Append one LP2R polymer component."""
        components = self.copy_lp2r_components(self.lp2r_components)
        components.append(component)
        self.set_lp2r_components(components)

    def normalize_lp2r_component_weights(self):
        """Normalize LP2R component weights on the current theory."""
        try:
            self.set_lp2r_components(
                self.normalize_component_weights(self.lp2r_components)
            )
        except ValueError as exc:
            QMessageBox.warning(self, "LP2R Components", str(exc))

    def _collect_mwd_getters(self):
        """Collect available Discretize MWD theory outputs from RepTate apps."""
        apmng: ApplicationManagerLike = self.parent_dataset.parent_application.parent_manager
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
                    if th.thname == "Discretize MWD":
                        get_dict[
                            "%s.%s.%s" % (app_tab_name, ds_tab_name, th_tab_name)
                        ] = th.get_mwd
        return get_dict

    def get_mwd_reptate(self):
        """Import discrete molecular weights from a Discretize MWD theory."""
        get_dict = self._collect_mwd_getters()
        if not get_dict:
            QMessageBox.warning(
                self, "Get MW distribution", 'No "Discretize MWD" theory found'
            )
            return

        dialog = GetMwdRepTate(self, get_dict, "Select Discretized MWD")
        if dialog.exec_() and dialog.btngrp.checkedButton() is not None:
            _, success1 = self.set_param_value("tau_e", dialog.taue_text.text())
            _, success2 = self.set_param_value("Me", dialog.Me_text.text())
            if not success1 * success2:
                self.Qprint("Could not understand Me or tau_e, try again")
                return
            item = dialog.btngrp.checkedButton().text()
            masses, weights = get_dict[item]()
            try:
                component = self.make_mwd_component(
                    masses,
                    weights,
                    label=item,
                    source="RepTate",
                )
                self.add_lp2r_component(component)
                self.Qprint(
                    "Added LP2R MWD component from %s with %d points"
                    % (item, len(component["masses"]))
                )
                self.Qprint(
                    '<font color=green><b>Press "Calculate" to update theory</b></font>'
                )
            except ValueError as exc:
                self.Qprint("<font color=red><b>%s</b></font>" % exc)

    def component_from_mwd_dialog(
        self,
        dialog,
        label="MWD",
        source="manual",
        weight=1.0,
    ):
        """Build an MWD component from an EditMWDDialog instance."""
        nmodes = dialog.table.rowCount()
        masses = []
        weights = []
        _, success1 = self.set_param_value("tau_e", dialog.taue_text.text())
        _, success2 = self.set_param_value("Me", dialog.Me_text.text())
        if not success1 * success2:
            self.Qprint("Could not understand Me or tau_e, try again")
            return None
        for i in range(nmodes):
            try:
                masses.append(float(dialog.table.item(i, 0).text()))
                weights.append(float(dialog.table.item(i, 1).text()))
            except (AttributeError, ValueError):
                self.Qprint("Could not understand line %d, try again" % (i + 1))
                return None
        try:
            return self.make_mwd_component(
                masses,
                weights,
                weight=weight,
                label=label,
                source=source,
            )
        except ValueError as exc:
            self.Qprint("<font color=red><b>%s</b></font>" % exc)
            return None

    def edit_mwd_data(self):
        """Append MWD data entered directly by the user."""
        dialog = EditMWDDialog(self, self.MWD_m, self.MWD_phi, 200)
        if dialog.exec_():
            component = self.component_from_mwd_dialog(dialog)
            if component is not None:
                self.add_lp2r_component(component)
                self.Qprint(
                    '<font color=green><b>Press "Calculate" to update theory</b></font>'
                )

    def import_mwd_gpc(self):
        """Append an MWD component imported from a RepTate .gpc file."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open MWD .gpc file",
            "",
            "GPC Files (*.gpc);;All Files (*)",
        )
        if not path:
            return
        try:
            masses, weights = self.read_gpc_mwd(path)
            component = self.make_mwd_component(
                masses,
                weights,
                label=path.split("/")[-1].split("\\")[-1],
                source="gpc",
            )
            self.add_lp2r_component(component)
        except ValueError as exc:
            QMessageBox.warning(self, "LP2R Components", str(exc))

    def _build_solver(self):
        """Create and configure a solver instance from the current parameters."""
        material = _lp2r.Material()
        m_kuhn = self.parameter_float("MK")
        m_e = self.parameter_float("Me")
        material.m_kuhn = m_kuhn * 1000.0
        material.m_e = m_e * 1000.0
        material.g0 = self.parameter_float("G0")
        material.tau_e = self.parameter_float("tau_e")
        material.g_glass = self.parameter_float("G_glass")
        material.tau_glass = self.parameter_float("tau_glass")
        material.beta_glass = self.parameter_float("beta_glass")

        controls = _lp2r.Controls()
        controls.alpha = self.parameter_float("alpha")
        controls.t_cr_start = self.parameter_float("t_cr_start")
        controls.delta_cr = self.parameter_float("delta_cr")
        controls.b_zeta = self.parameter_float("b_zeta")
        controls.a_eq = self.parameter_float("a_eq")
        controls.b_eq = self.parameter_float("b_eq")
        controls.ret_pref = self.parameter_float("ret_pref")
        controls.ret_pref_0 = self.parameter_float("ret_pref_0")
        controls.ret_switch_exponent = self.parameter_float("ret_switch_exponent")
        controls.rept_switch_factor = self.parameter_float("rept_switch_factor")
        controls.rouse_switch_factor = self.parameter_float("rouse_switch_factor")
        controls.disentanglement_switch = self.parameter_float("disentanglement_switch")
        controls.start_time = self.parameter_float("start_time")
        controls.time_ratio = self.parameter_float("time_ratio")

        solver = _lp2r.Solver(material, controls)
        components = self.validate_lp2r_components(self.current_lp2r_components())
        for component in components:
            if component["kind"] == "lognormal":
                solver.add_lognormal_component(
                    weight=component["weight"],
                    n=component["npoly"],
                    mw=component["Mw"] * 1000.0,
                    pdi=component["PDI"],
                )
            else:
                solver.add_discrete_component(
                    mass=[mass * 1000.0 for mass in component["masses"]],
                    weight=component["weights"],
                    component_weight=component["weight"],
                )
        return solver

    def set_extra_data(self, extra_data):
        """Set LP2R component state when loading a project."""
        self.extra_data = extra_data
        migrated = self.migrate_old_lp2r_state(extra_data, self.parameters)
        if migrated is not None:
            self.lp2r_components = migrated
        else:
            self.lp2r_components = [self.default_lognormal_component()]

    def get_extra_data(self):
        """Save LP2R component state into project extra data."""
        self.extra_data["lp2r_components"] = self.copy_lp2r_components(
            self.current_lp2r_components()
        )

    def request_stop_computations(self):
        """Called when the user wants to terminate the current computation."""
        if self.solver is not None:
            self.solver.cancel()
        super().request_stop_computations()

    def do_error(self, line=""):
        """Calculate error by interpolating the generated LP2R spectrum."""
        self.do_error_interpolated(line="")

    def _positive_abscissa_range(self, f: FileLike, label: str):
        """Return the positive finite range of the first file column."""
        data = np.asarray(f.data_table.data[:, 0], dtype=float)
        data = data[np.isfinite(data) & (data > 0)]
        if len(data) == 0:
            self.Qprint("<font color=red><b>LP2R needs positive %s</b></font>" % label)
            return None
        return float(np.min(data)), float(np.max(data))

    def _prepare_solver_for_calculation(self, tt):
        """Build the LP2R solver and run the relaxation stage."""
        try:
            components = self.validate_lp2r_components(self.current_lp2r_components())
        except ValueError as exc:
            self.Qprint("<font color=red><b>LP2R calculation stopped: %s</b></font>" % exc)
            self._clear_table(tt)
            return False
        if not self.is_fitting:
            self.Qprint("<b>LP2R components for current calculation</b>")
            self.Qprint(self.component_table(components))

        self.solver = self._build_solver()
        self.solver.prepare()
        last_progress = 0
        if not self.is_fitting:
            self.Qprint("LP2R relaxation:<br>  0% ", end="")
        while self.solver.step():
            if self.stop_theory_flag:
                self.solver.cancel()
                self._clear_table(tt)
                self.Qprint(
                    "<br><font color=red><b>LP2R calculation cancelled</b></font>"
                )
                return False
            if not self.is_fitting:
                last_progress = self._report_progress(
                    self.solver.progress(), last_progress
                )
        if self.solver.cancelled():
            self._clear_table(tt)
            self.Qprint(
                "<br><font color=red><b>LP2R calculation cancelled</b></font>"
            )
            return False
        if not self.is_fitting:
            while last_progress < 100:
                self.Qprint("-", end="")
                last_progress += 10
            self.Qprint(" 100%")
        return True

    def calculate(self, f: FileLike) -> None:
        """Calculate LP2R G' and G'' over the active LVE frequency range."""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns

        frequency_range = self._positive_abscissa_range(f, "frequencies")
        if frequency_range is None:
            self._clear_table(tt)
            return
        freq_min, freq_max = frequency_range
        freq_ratio = self.parameter_float("freq_ratio")
        if freq_ratio <= 1.0:
            self.Qprint("<font color=red><b>LP2R freq_ratio must be larger than 1</b></font>")
            self._clear_table(tt)
            return

        try:
            if not self._prepare_solver_for_calculation(tt):
                return
            result = self.solver.calculate_spectra(freq_min, freq_max, freq_ratio)
        except Exception as exc:
            self.Qprint("<font color=red><b>LP2R calculation failed: %s</b></font>" % exc)
            self._clear_table(tt)
            return
        finally:
            self.solver = None

        tt.num_rows = len(result.omega)
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = result.omega
        if tt.num_columns > 1:
            tt.data[:, 1] = result.gp
        if tt.num_columns > 2:
            tt.data[:, 2] = result.gpp


class TheoryLP2RDielectric(TheoryLP2RLVE):
    """LP2R type-A dielectric spectroscopy predictions."""

    thname: ClassVar[str] = "LP2R Dielectric"
    description: ClassVar[str] = "Dielectric rheology of polydisperse linear polymers"
    html_help_file: ClassVar[str] = "http://reptate.readthedocs.io/manual/Applications/Dielectric/Theory/theory.html"

    def calculate(self, f: FileLike) -> None:
        """Calculate LP2R epsilon' and epsilon'' over the active frequency range."""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns

        frequency_range = self._positive_abscissa_range(f, "frequencies")
        if frequency_range is None:
            self._clear_table(tt)
            return
        freq_min, freq_max = frequency_range
        freq_ratio = self.parameter_float("freq_ratio")
        if freq_ratio <= 1.0:
            self.Qprint("<font color=red><b>LP2R freq_ratio must be larger than 1</b></font>")
            self._clear_table(tt)
            return

        try:
            if not self._prepare_solver_for_calculation(tt):
                return
            result = self.solver.calculate_spectra(freq_min, freq_max, freq_ratio)
        except Exception as exc:
            self.Qprint("<font color=red><b>LP2R calculation failed: %s</b></font>" % exc)
            self._clear_table(tt)
            return
        finally:
            self.solver = None

        tt.num_rows = len(result.omega)
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = result.omega
        if tt.num_columns > 1:
            tt.data[:, 1] = result.epsilonp
        if tt.num_columns > 2:
            tt.data[:, 2] = result.epsilonpp


class TheoryLP2RGt(TheoryLP2RLVE):
    """LP2R relaxation modulus predictions."""

    thname: ClassVar[str] = "LP2R G(t)"
    description: ClassVar[str] = "Relaxation modulus of polydisperse linear polymers"
    html_help_file: ClassVar[str] = "http://reptate.readthedocs.io/manual/Applications/Gt/Theory/theory.html"

    def calculate(self, f: FileLike) -> None:
        """Calculate LP2R G(t)."""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns

        try:
            if not self._prepare_solver_for_calculation(tt):
                return
            result = self.solver.calculate_relaxation_modulus()
        except Exception as exc:
            self.Qprint("<font color=red><b>LP2R calculation failed: %s</b></font>" % exc)
            self._clear_table(tt)
            return
        finally:
            self.solver = None

        tt.num_rows = len(result.time)
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = result.time
        if tt.num_columns > 1:
            tt.data[:, 1] = result.gt
