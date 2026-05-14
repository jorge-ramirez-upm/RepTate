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
# Copyright (2017-2026): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module TheoryLikhtmanMcLeish2002

Module that defines the Likhtman-McLeish theory for melts of linear monodisperse entangled
polymers.

"""

import os
import numpy as np
from numpy import interp
from RepTate.gui.QTheory import QTheory
from RepTate.core.Parameter import Parameter, ParameterType, OptType
from RepTate.core.DraggableArtists import DragType, DraggableHLine, DraggableVLine
from PySide6.QtWidgets import QToolBar, QLabel, QLineEdit, QMessageBox
from PySide6.QtGui import QIcon, QDoubleValidator
from PySide6.QtCore import QSize


class _NoFitOnDrag(object):
    def handle_actionMinimize_Error(self):
        pass


class TheoryLikhtmanMcLeish2002(QTheory):
    """Fit Likhtman-McLeish theory for linear rheology of linear entangled polymers

    * **Parameters**
       - ``tau_e`` : Rouse time of one entanglement segment (of length :math:`M_e`).
       - ``Ge`` : Entanglement modulus.
       - ``Me`` : Entanglement molecular weight.
       - ``c_nu`` : Constraint release parameter.
    """

    thname = "Likhtman-McLeish"
    description = "Likhtman-McLeish theory for linear entangled polymers"
    citations = ["Likhtman A.E. and McLeish T.C.B., Macromolecules 2002, 35, 6332-6343"]
    doi = ["http://dx.doi.org/10.1021/ma0200219"]
    html_help_file = "http://reptate.readthedocs.io/manual/Applications/LVE/Theory/theory.html#likhtman-mcleish-theory"
    single_file = False

    def __init__(self, name="", parent_dataset=None, ax=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, ax)
        self.function = self.LikhtmanMcLeish2002

        self.parameters["tau_e"] = Parameter(
            "tau_e",
            2e-6,
            "Rouse time of one Entanglement",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=1e-7,
            max_value=1e2,
            # Theory calculations use seconds internally.
            quantity="time",
            internal_unit="s",
            display_unit="s",
        )
        self.parameters["Ge"] = Parameter(
            "Ge",
            1e6,
            "Entanglement modulus",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=1e3,
            max_value=1e7,
            quantity="stress",
            internal_unit="Pa",
            display_unit="Pa",
        )
        self.parameters["Me"] = Parameter(
            "Me",
            5,
            "Entanglement molecular weight",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0.4,
            max_value=50.0,
            quantity="molar_mass",
            internal_unit="kg/mol",
            display_unit="kg/mol",
        )
        self.parameters["c_nu"] = Parameter(
            name="c_nu",
            value=0.1,
            description="Constraint Release parameter",
            type=ParameterType.discrete_real,
            opt_type=OptType.const,
            discrete_values=[0, 0.01, 0.03, 0.1, 0.3, 1, 3, 10],
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["linkMeGe"] = Parameter(
            name="linkMeGe",
            value=False,
            description="Link values of Ge & Me through rho and T",
            type=ParameterType.boolean,
            opt_type=OptType.const,
            display_flag=False,
        )
        self.parameters["rho0"] = Parameter(
            name="rho0",
            value=1.0,
            description="Density of the polymer melt",
            type=ParameterType.real,
            opt_type=OptType.const,
            display_flag=False,
            quantity="density",
            internal_unit="g/cm3",
            display_unit="g/cm3",
        )

        dir_path = os.path.dirname(os.path.realpath(__file__))
        f = np.load(os.path.join(dir_path, "linlin.npz"), allow_pickle=True)
        self.Zarray = f["Z"]
        self.cnuarray = f["cnu"]
        self.data = f["data"]

        if not self.get_material_parameters():
            # Estimate initial values of the theory
            w = self.parent_dataset.files[0].data_table.data[:, 0]
            Gp = self.parent_dataset.files[0].data_table.data[:, 1]
            Gpp = self.parent_dataset.files[0].data_table.data[:, 2]

            Gpp_Gp = Gpp / Gp
            ind = len(Gpp_Gp) - np.argmax(np.flipud(Gpp_Gp) < 0.8)
            if ind < len(w):
                taue = 1.0 / w[ind]
                Ge = Gp[ind]
                self.set_param_value("tau_e", taue)
                self.set_param_value("Ge", Ge)

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        self.ge_taue_helper_action = tb.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-visible.png"),
            "Show Ge and tau_e helpers",
        )
        self.ge_taue_helper_action.setCheckable(True)
        self.linkMeGeaction = tb.addAction(QIcon(":/Icon8/Images/new_icons/linkGeMe.png"), "Link Me-Ge")
        self.linkMeGeaction.setCheckable(True)
        self.linkMeGeaction.setChecked(False)
        self.lblrho = QLabel(self)
        tb.addWidget(self.lblrho)
        self.txtrho = QLineEdit()
        self.txtrho.setReadOnly(True)
        self.txtrho.setDisabled(True)
        dvalidator = QDoubleValidator()  # prevent letters etc.
        self.txtrho.setValidator(dvalidator)
        self.update_rho0_toolbar()
        tb.addWidget(self.txtrho)
        self.thToolsLayout.insertWidget(0, tb)

        self.linkMeGeaction.triggered.connect(self.linkMeGeaction_change)
        self.txtrho.textEdited.connect(self.handle_txtrho_edited)
        self.ge_taue_helper_action.triggered.connect(self.ge_taue_helper_visible)

        self._drag_no_fit = _NoFitOnDrag()
        self.ge_helper_line = self.ax.axhline(
            1.0,
            color="darkgreen",
            linestyle="--",
            marker="o",
            visible=False,
            picker=5,
            zorder=5,
        )
        self.taue_helper_line = self.ax.axvline(
            1.0,
            color="darkorange",
            linestyle="--",
            marker="o",
            visible=False,
            picker=5,
            zorder=5,
        )
        helper_label_box = {
            "boxstyle": "round,pad=0.2",
            "facecolor": "white",
            "edgecolor": "none",
            "alpha": 0.65,
        }
        self.ge_helper_label = self.ax.annotate(
            "Ge",
            xy=(0.98, 1.0),
            xycoords=("axes fraction", "data"),
            xytext=(-4, 4),
            textcoords="offset points",
            ha="right",
            va="bottom",
            color="darkgreen",
            fontsize="medium",
            bbox=helper_label_box,
            visible=False,
            zorder=6,
        )
        self.taue_helper_label = self.ax.annotate(
            "1/tau_e",
            xy=(1.0, 0.98),
            xycoords=("data", "axes fraction"),
            xytext=(4, -4),
            textcoords="offset points",
            ha="left",
            va="top",
            color="darkorange",
            fontsize="medium",
            bbox=helper_label_box,
            visible=False,
            zorder=6,
        )
        self.ge_helper_drag = DraggableHLine(
            self.ge_helper_line,
            DragType.vertical,
            self.drag_ge_helper,
            self._drag_no_fit,
        )
        self.taue_helper_drag = DraggableVLine(
            self.taue_helper_line,
            DragType.horizontal,
            self.drag_taue_helper,
            self._drag_no_fit,
        )
        self.plot_theory_stuff()

    def linkMeGeaction_change(self, checked):
        self.set_param_value("linkMeGe", checked)
        if checked:
            self.txtrho.setReadOnly(False)
            self.txtrho.setDisabled(False)
            p = self.parameters["Ge"]
            p.opt_type = OptType.const
        else:
            self.txtrho.setReadOnly(True)
            self.txtrho.setDisabled(True)
            p = self.parameters["Ge"]
            p.opt_type = OptType.opt
        self.update_parameter_table()
        if self.autocalculate:
            self.handle_actionCalculate_Theory()

    def handle_txtrho_edited(self, new_text):
        try:
            val = float(new_text)
        except ValueError:
            QMessageBox.warning(self, "Error", 'Could not convert "%s" to float' % new_text)
            self.txtrho.setText("%.4g" % self.parameters["rho0"].display_value())
        else:
            message, success = self.set_param_value_from_display("rho0", val)
            if not success:
                QMessageBox.warning(self, "Error", message)
                self.txtrho.setText("%.4g" % self.parameters["rho0"].display_value())
                return
            if self.autocalculate:
                self.handle_actionCalculate_Theory()

    def update_rho0_toolbar(self):
        """Update rho0 toolbar widgets from the parameter display metadata."""
        rho0 = self.parameters["rho0"]
        self.lblrho.setText("<P><b>%s</b></P></br>" % rho0.display_label())
        self.txtrho.setText("%.4g" % rho0.display_value())
        validator = self.txtrho.validator()
        if validator is not None:
            validator.setBottom(rho0.display_value(0))
            validator.setTop(rho0.display_value(10))

    def handle_parameter_metadata_changed(self):
        """Refresh auxiliary widgets after the theory parameter dialog changes units."""
        self.update_rho0_toolbar()
        self.plot_theory_stuff()

    def _axis_supports(self, axis_spec, quantity):
        return axis_spec.quantity == quantity

    def _parameter_value_to_plot_axis(self, value, axis_spec):
        if axis_spec.transform == "log10":
            if value <= 0.0:
                return None
            value = np.log10(value)
        return axis_spec.convert_from_internal(value).item()

    def _plot_axis_to_parameter_value(self, value, axis_spec):
        value = axis_spec.convert_to_internal(value).item()
        if axis_spec.transform == "log10":
            value = np.power(10.0, value)
        return value

    def _ge_plot_y(self):
        view = self.current_view()
        if not self._axis_supports(view.y_axis, "stress"):
            return None
        return self._parameter_value_to_plot_axis(self.parameters["Ge"].value, view.y_axis)

    def _taue_plot_x(self):
        view = self.current_view()
        if view.x_axis.quantity not in ("angular_frequency", "frequency"):
            return None
        taue = self.parameters["tau_e"].value
        if taue <= 0.0:
            return None
        return self._parameter_value_to_plot_axis(1.0 / taue, view.x_axis)

    def plot_theory_stuff(self):
        """Update the graphical parameter helpers for the current view."""
        ge_y = self._ge_plot_y()
        helpers_visible = self.ge_taue_helper_action.isChecked()
        ge_visible = helpers_visible and ge_y is not None
        if ge_y is not None:
            self.ge_helper_line.set_ydata([ge_y, ge_y])
            self.ge_helper_label.xy = (0.98, ge_y)
        self.ge_helper_line.set_visible(ge_visible and self.active)
        self.ge_helper_label.set_visible(ge_visible and self.active)

        taue_x = self._taue_plot_x()
        taue_visible = helpers_visible and taue_x is not None
        if taue_x is not None:
            self.taue_helper_line.set_xdata([taue_x, taue_x])
            self.taue_helper_label.xy = (taue_x, 0.98)
        self.taue_helper_line.set_visible(taue_visible and self.active)
        self.taue_helper_label.set_visible(taue_visible and self.active)

    def ge_taue_helper_visible(self, checked):
        self.plot_theory_stuff()
        self.parent_dataset.parent_application.update_plot()

    def drag_ge_helper(self, dx, dy):
        view = self.current_view()
        if not self._axis_supports(view.y_axis, "stress"):
            return
        y = self.ge_helper_line.get_ydata()[0]
        Ge = self._plot_axis_to_parameter_value(y, view.y_axis)
        if Ge <= 0.0:
            return
        self.set_param_value("Ge", Ge)
        self.do_calculate("")
        self.update_parameter_table()
        self.plot_theory_stuff()

    def drag_taue_helper(self, dx, dy):
        view = self.current_view()
        if view.x_axis.quantity not in ("angular_frequency", "frequency"):
            return
        x = self.taue_helper_line.get_xdata()[0]
        omega = self._plot_axis_to_parameter_value(x, view.x_axis)
        if omega <= 0.0:
            return
        self.set_param_value("tau_e", 1.0 / omega)
        self.do_calculate("")
        self.update_parameter_table()
        self.plot_theory_stuff()

    def show_theory_extras(self, show=False):
        self.plot_theory_stuff()
        if not show:
            self.ge_helper_line.set_visible(False)
            self.taue_helper_line.set_visible(False)
            self.ge_helper_label.set_visible(False)
            self.taue_helper_label.set_visible(False)
        self.parent_dataset.parent_application.update_plot()

    def destructor(self):
        self.ge_helper_drag.disconnect()
        self.taue_helper_drag.disconnect()
        self.ge_helper_label.remove()
        self.taue_helper_label.remove()
        self.ge_helper_line.remove()
        self.taue_helper_line.remove()

    def set_extra_data(self, _):
        """Restore the check state of button and text value"""
        self.update_rho0_toolbar()
        checked = self.parameters["linkMeGe"].value
        self.linkMeGeaction.setChecked(checked)
        self.linkMeGeaction_change(checked)

    def LikhtmanMcLeish2002(self, f=None):
        """Get the theory results from precalculated data"""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        taue = self.parameters["tau_e"].value
        Ge = self.parameters["Ge"].value
        Me = self.parameters["Me"].value
        cnu = self.parameters["c_nu"].value
        rho0 = self.parameters["rho0"].value
        linkMeGe = self.parameters["linkMeGe"].value
        Mw = float(f.file_parameters["Mw"])
        T = float(f.file_parameters["T"]) + 273.15
        if linkMeGe:
            Ge = 1000.0 * rho0 * T * 8.314 / Me  # *5/4 (Pity... With this factor it works much better)

        indcnu = (np.where(self.cnuarray == cnu))[0][0]
        indcnu1 = 1 + indcnu * 2
        indcnu2 = indcnu1 + 1

        Z = Mw / Me
        if Z < 3:
            # self.Qprint("WARNING: Mw of %s is too small"%(f.file_name_short))
            Z = 3
        if Z < self.Zarray[0]:
            indZ0 = 0
        else:
            indZ0 = (np.where(self.Zarray < Z))[0][-1]
        if Z > self.Zarray[-1]:
            indZ1 = len(self.Zarray) - 1
        else:
            indZ1 = (np.where(self.Zarray > Z))[0][0]
        table0 = self.data[indZ0]
        table1 = self.data[indZ1]

        vec = np.append(table0[:, 0], table1[:, 0])
        vec = np.sort(vec)
        vec = np.unique(vec)
        table = np.zeros((len(vec), 3))
        table[:, 0] = vec
        w1 = (Z - self.Zarray[indZ0]) / (self.Zarray[indZ1] - self.Zarray[indZ0])
        table[:, 1] = (1.0 - w1) * interp(vec, table0[:, 0], table0[:, indcnu1]) + w1 * interp(vec, table1[:, 0], table1[:, indcnu1])
        table[:, 2] = (1.0 - w1) * interp(vec, table0[:, 0], table0[:, indcnu2]) + w1 * interp(vec, table1[:, 0], table1[:, indcnu2])

        tt.data[:, 1] = interp(tt.data[:, 0], table[:, 0] / taue, Ge * table[:, 1])
        tt.data[:, 2] = interp(tt.data[:, 0], table[:, 0] / taue, Ge * table[:, 2])

    def do_error(self, line):
        """Report the error of the current theory

        Report the error of the current theory on all the files, taking into account the current selected xrange and yrange.

        File error is calculated as the mean square of the residual, averaged over all points in the file. Total error is the mean square of the residual, averaged over all points in all files.
        """
        super().do_error(line)
        taue = self.parameters["tau_e"].value
        Me = self.parameters["Me"].value
        tab_data = [
            ["%-18s" % "File", "%-18s" % "Z", "%-18s" % "tauR", "%-18s" % "tauD"],
        ]
        C1 = 1.69
        C2 = 4.17
        C3 = -1.55
        for f in self.theory_files():
            Z = float(f.file_parameters["Mw"]) / Me
            tauR = taue * Z**2
            if Z != 0:
                tauD = 3 * taue * Z**3 * (1.0 - 2 * C1 / np.sqrt(Z) + C2 / Z + C3 / np.power(Z, 1.5))
            else:
                tauD = 0
            tab_data.append(
                [
                    "%-18s" % f.file_name_short,
                    "%18.4g" % Z,
                    "%18.4g" % tauR,
                    "%    18.4g" % tauD,
                ]
            )
        self.Qprint(tab_data)
