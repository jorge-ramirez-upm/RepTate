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
"""Module TheoryRoliePoly

Module for the Rolie-Poly theory for the non-linear flow of entangled polymers.

"""

import os
import numpy as np
from scipy.integrate import odeint
from typing import Any, ClassVar, cast
from RepTate.core.Parameter import Parameter, ParameterType, OptType
from RepTate.core.typing import AxesArray, FileLike
from RepTate.gui.QTheory import QTheory, EndComputationRequested
from RepTate.core.DataTable import DataTable
from PySide6.QtWidgets import (
    QToolBar,
    QToolButton,
    QMenu,
    QSpinBox,
    QMessageBox,
    QFileDialog,
)
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

from math import sqrt
import RepTate
import time
from RepTate.applications.ApplicationLAOS import ApplicationLAOS
from RepTate.theories.theory_helpers import FlowMode, EditModesDialog, FeneMode


class TheoryRoliePoly(QTheory):
    """Rolie-Poly theory
    MORE DETAILED DOCUMENTATION IS MISSING
    """

    thname: ClassVar[str] = "Rolie-Poly"
    description: ClassVar[str] = "Rolie-Poly constitutive equation"
    citations: ClassVar[list[str]] = ["Likhtman, A.E. & Graham, R.S., J. Non-Newtonian Fluid Mech., 2003, 114, 1-12"]
    doi: ClassVar[list[str]] = ["http://dx.doi.org/10.1016/S0377-0257(03)00114-9"]
    html_help_file: ClassVar[str] = "http://reptate.readthedocs.io/manual/Applications/NLVE/Theory/theory.html#rolie-poly-equation"
    single_file: ClassVar[bool] = False

    def __init__(self, name: str = "", parent_dataset: Any = None, axarr: AxesArray | None = None) -> None:
        """**Constructor**"""
        super().__init__(name, parent_dataset, axarr)
        self.function = self.RoliePoly
        self.has_modes = True
        self.parameters["beta"] = Parameter(
            name="beta",
            value=0.5,
            description="CCR coefficient",
            type=ParameterType.real,
            opt_type=OptType.nopt,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["delta"] = Parameter(
            name="delta",
            value=-0.5,
            description="CCR exponent",
            type=ParameterType.real,
            opt_type=OptType.nopt,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["lmax"] = Parameter(
            name="lmax",
            value=10.0,
            description="Maximum extensibility",
            type=ParameterType.real,
            opt_type=OptType.nopt,
            display_flag=False,
            min_value=1.01,
            quantity="dimensionless",
            internal_unit="-",
            display_unit="-",
        )
        self.parameters["nmodes"] = Parameter(
            name="nmodes",
            value=2,
            description="Number of modes",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False,
        )
        self.parameters["nstretch"] = Parameter(
            name="nstretch",
            value=2,
            description="Number of strecthing modes",
            type=ParameterType.integer,
            opt_type=OptType.const,
            display_flag=False,
        )

        nmodes_value: Any = self.parameters["nmodes"].value
        for i in range(nmodes_value):
            self.parameters["G%02d" % i] = Parameter(
                name="G%02d" % i,
                value=1000.0,
                description="Modulus of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.nopt,
                display_flag=False,
                min_value=0,
                quantity="stress",
                internal_unit="Pa",
                display_unit="Pa",
            )
            self.parameters["tauD%02d" % i] = Parameter(
                name="tauD%02d" % i,
                value=10.0,
                description="Terminal time of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.nopt,
                display_flag=False,
                min_value=0,
                quantity="time",
                internal_unit="s",
                display_unit="s",
            )
            self.parameters["tauR%02d" % i] = Parameter(
                name="tauR%02d" % i,
                value=0.5,
                description="Rouse time of mode %02d" % i,
                type=ParameterType.real,
                opt_type=OptType.opt,
                min_value=1e-12,
                quantity="time",
                internal_unit="s",
                display_unit="s",
            )

        self.view_LVEenvelope = False
        auxseries = self.ax.plot([], [], label="")
        self.LVEenvelopeseries = auxseries[0]
        self.LVEenvelopeseries.set_marker("")
        self.LVEenvelopeseries.set_linestyle("--")
        self.LVEenvelopeseries.set_visible(self.view_LVEenvelope)
        self.LVEenvelopeseries.set_color("green")
        self.LVEenvelopeseries.set_linewidth(5)
        self.LVEenvelopeseries.set_label("")

        self.MAX_MODES = 40
        self.with_fene = FeneMode.none
        self.init_flow_mode()

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))

        if not isinstance(parent_dataset.parent_application, ApplicationLAOS):
            self.tbutflow = QToolButton()
            menu_button_popup: Any = getattr(QToolButton, "MenuButtonPopup")
            self.tbutflow.setPopupMode(menu_button_popup)
            menu = QMenu(self)
            self.shear_flow_action = menu.addAction(QIcon(":/Icon8/Images/new_icons/icon-shear.png"), "Shear Flow")
            self.extensional_flow_action = menu.addAction(QIcon(":/Icon8/Images/new_icons/icon-uext.png"), "Extensional Flow")
            if self.flow_mode == FlowMode.shear:
                self.tbutflow.setDefaultAction(self.shear_flow_action)
            else:
                self.tbutflow.setDefaultAction(self.extensional_flow_action)
            self.tbutflow.setMenu(menu)
            tb.addWidget(self.tbutflow)
            self.shear_flow_action.triggered.connect(self.select_shear_flow)
            self.extensional_flow_action.triggered.connect(self.select_extensional_flow)

            self.read_gdot_action = tb.addAction(
                QIcon(":/Icon8/Images/new_icons/icons8-file-gdot.png"),
                "Read gdot from file",
            )
            self.read_gdot_action.setCheckable(True)

        else:
            self.function = self.RoliePolyLAOS

        self.tbutmodes = QToolButton()
        menu_button_popup = getattr(QToolButton, "MenuButtonPopup")
        self.tbutmodes.setPopupMode(menu_button_popup)
        menu = QMenu(self)
        self.get_modes_action = menu.addAction(QIcon(":/Icon8/Images/new_icons/icons8-broadcasting.png"), "Get Modes")
        self.edit_modes_action = menu.addAction(QIcon(":/Icon8/Images/new_icons/icons8-edit-file.png"), "Edit Modes")
        # self.plot_modes_action = menu.addAction(
        #     QIcon(':/Icon8/Images/new_icons/icons8-scatter-plot.png'),
        #     "Plot Modes")
        self.save_modes_action = menu.addAction(QIcon(":/Icon8/Images/new_icons/icons8-save-Maxwell.png"), "Save Modes")
        self.tbutmodes.setDefaultAction(self.get_modes_action)
        self.tbutmodes.setMenu(menu)
        tb.addWidget(self.tbutmodes)
        # Show LVE button
        self.linearenvelope = tb.addAction(QIcon(":/Icon8/Images/new_icons/lve-icon.png"), "Show Linear Envelope")
        self.linearenvelope.setCheckable(True)
        self.linearenvelope.setChecked(False)
        # Finite extensibility button
        self.with_fene_button = tb.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-infinite.png"),
            "Finite Extensibility",
        )
        self.with_fene_button.setCheckable(True)
        # SpinBox "nmodes"
        self.spinbox = QSpinBox()
        nmodes_value = self.parameters["nmodes"].value
        self.spinbox.setRange(0, nmodes_value)  # min and max number of modes
        self.spinbox.setSuffix(" stretch")
        self.spinbox.setToolTip("Number of stretching modes")
        self.spinbox.setValue(nmodes_value)  # initial value
        tb.addWidget(self.spinbox)

        # Save to flowsolve button
        self.flowsolve_btn = tb.addAction(
            QIcon(":/Icon8/Images/new_icons/icons8-save-flowsolve.png"),
            "Save Parameters To FlowSolve",
        )
        self.flowsolve_btn.setCheckable(False)

        self.thToolsLayout.insertWidget(0, tb)

        self.get_modes_action.triggered.connect(self.get_modes_reptate)
        self.edit_modes_action.triggered.connect(self.edit_modes_window)
        # self.plot_modes_action.triggered.connect(self.plot_modes_graph)
        self.save_modes_action.triggered.connect(self.save_modes)
        self.linearenvelope.triggered.connect(self.show_linear_envelope)
        self.spinbox.valueChanged.connect(self.handle_spinboxValueChanged)
        self.with_fene_button.triggered.connect(self.handle_with_fene_button)
        self.flowsolve_btn.triggered.connect(self.handle_flowsolve_btn)

    def handle_flowsolve_btn(self) -> None:
        """Save theory parameters in FlowSolve format"""

        # Get filename of RepTate project to open
        fpath, _ = QFileDialog.getSaveFileName(
            self,
            "Save Parameters to FowSolve",
            os.path.join(RepTate.root_dir, "data"),
            "FlowSolve (*.fsrep)",
        )
        if fpath == "":
            return

        with open(fpath, "w") as f:
            # verdata = RepTate._version.get_versions()
            # version = verdata["version"].split("+")[0]
            # date = verdata["date"].split("T")[0]
            # build = verdata["version"]
            version = RepTate.__version__.split("+")[0]
            date = ""
            try:
                build = RepTate.__version__.split("+")[1]
            except IndexError:
                build = ""
            header = "#flowGen input\n"
            header += "# Generated with RepTate %s %s (build %s)\n" % (
                version,
                date,
                build,
            )
            header += "# At %s on %s\n" % (
                time.strftime("%X"),
                time.strftime("%a %b %d, %Y"),
            )
            f.write(header)

            f.write("\n#param global\n")
            f.write("constit roliepoly\n")
            # f.write('# or multip (for pompom) or polydisperse (for polydisperse Rolie-Poly)\n')

            f.write("\n#param constitutive\n")
            n: Any = self.parameters["nmodes"].value
            nR: Any = self.parameters["nstretch"].value

            # sort taud ascending order
            td = np.zeros(n)
            for i in range(n):
                td[i] = self.parameters["tauD%02d" % i].value
            args = np.argsort(td)

            modulus = "modulus"
            taud = "taud"
            tauR = "tauR"
            lmax = "lambdaMax"
            for i, arg in enumerate(args):
                modulus += " %.6g" % self.parameters["G%02d" % arg].value
                taud += " %.6g" % self.parameters["tauD%02d" % arg].value
                if n - i <= nR:
                    tauR += " %.6g" % self.parameters["tauR%02d" % arg].value
                    lmax += " %.6g" % self.parameters["lmax"].value
            f.write("%s\n%s\n%s\n" % (modulus, taud, tauR))
            if self.with_fene == FeneMode.with_fene:  # don't output lmax at all for infinite ex
                f.write("%s\n" % lmax)
            f.write("beta %.6g\n" % self.parameters["beta"].value)
            f.write("delta %.6g\n" % self.parameters["delta"].value)
            f.write("firstStretch %d\n" % (1 + n - nR))  # +1 as flowsolve uses 1-n index not 0-n-1

            f.write("\n#end")

        QMessageBox.information(self, "Success", 'Wrote FlowSolve parameters in "%s"' % fpath)

    def handle_with_fene_button(self, checked: Any) -> None:
        if checked:
            self.with_fene = FeneMode.with_fene
            self.with_fene_button.setChecked(True)
            self.with_fene_button.setIcon(QIcon(":/Icon8/Images/new_icons/icons8-facebook-f.png"))
            self.parameters["lmax"].display_flag = True
            self.parameters["lmax"].opt_type = OptType.nopt
        else:
            self.with_fene = FeneMode.none
            self.with_fene_button.setChecked(False)
            self.with_fene_button.setIcon(QIcon(":/Icon8/Images/new_icons/icons8-infinite.png"))
            self.parameters["lmax"].display_flag = False
            self.parameters["lmax"].opt_type = OptType.const
        self.update_parameter_table()
        self.parent_dataset.handle_actionCalculate_Theory()

    def handle_spinboxValueChanged(self, value: Any) -> None:
        nmodes: Any = self.parameters["nmodes"].value
        self.set_param_value("nstretch", min(nmodes, value))
        if self.autocalculate:
            self.parent_dataset.handle_actionCalculate_Theory()

    def Qhide_theory_extras(self, show: Any) -> None:
        """Uncheck the LVE button. Called when curent theory is changed"""
        if show:
            self.LVEenvelopeseries.set_visible(self.linearenvelope.isChecked())
        else:
            self.LVEenvelopeseries.set_visible(False)

    def show_linear_envelope(self, state: Any) -> None:
        self.extra_graphic_visible(state)
        # self.LVEenvelopeseries.set_visible(self.linearenvelope.isChecked())
        # self.plot_theory_stuff()
        # self.parent_dataset.parent_application.update_plot()

    def plot_theory_stuff(self) -> None:
        """Plot theory helpers"""
        if not isinstance(self.parent_dataset.parent_application, ApplicationLAOS):
            data_table_tmp: Any = DataTable(self.axarr)
            data_table_tmp.num_columns = 2
            data_table_tmp.num_rows = 100
            data_table_tmp.data = np.zeros((100, 2))

            times = np.logspace(-2, 3, 100)
            data_table_tmp.data[:, 0] = times
            nmodes: Any = self.parameters["nmodes"].value
            data_table_tmp.data[:, 1] = 0
            fparamaux: dict[str, Any] = {}
            fparamaux["gdot"] = 1e-8
            for i in range(nmodes):
                if self.stop_theory_flag:
                    break
                G: Any = self.parameters["G%02d" % i].value
                tauD: Any = self.parameters["tauD%02d" % i].value
                data_table_tmp.data[:, 1] += G * fparamaux["gdot"] * tauD * (1 - np.exp(-times / tauD))
            if self.flow_mode == FlowMode.uext:
                data_table_tmp.data[:, 1] *= 3.0
            view = self.parent_dataset.parent_application.current_view
            try:
                x, y, success = view.view_proc(data_table_tmp, fparamaux)
            except TypeError as e:
                print(e)
                return
            x, y = self.convert_view_data_to_display(x, y, view)
            self.LVEenvelopeseries.set_data(x[:, 0], y[:, 0])

    def select_shear_flow(self) -> None:
        self.flow_mode = FlowMode.shear
        self.tbutflow.setDefaultAction(self.shear_flow_action)

    def select_extensional_flow(self) -> None:
        self.flow_mode = FlowMode.uext
        self.tbutflow.setDefaultAction(self.extensional_flow_action)

    def get_modes_reptate(self) -> None:
        self.Qcopy_modes()

    def edit_modes_window(self) -> None:
        times, G, success = self.get_modes()
        if not success:
            self.logger.warning("Could not get modes successfully")
            return
        d = EditModesDialog(self, times, G, self.MAX_MODES)
        if d.exec_():
            nmodes = d.table.rowCount()
            self.set_param_value("nmodes", nmodes)
            self.set_param_value("nstretch", nmodes)
            success = True
            for i in range(nmodes):
                msg, success1 = self.set_param_value("tauD%02d" % i, d.table.item(i, 0).text())
                msg, success2 = self.set_param_value("G%02d" % i, d.table.item(i, 1).text())
                success *= success1 * success2
            if not success:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Some parameter(s) could not be updated.\nPlease try again.",
                )
            else:
                self.handle_actionCalculate_Theory()

    def set_extra_data(self, extra_data: Any) -> None:
        """Set extra data when loading project"""
        self.handle_with_fene_button(extra_data["with_fene"])
        nstretch_value: Any = self.parameters["nstretch"].value
        self.spinbox.setValue(nstretch_value)

    def get_extra_data(self) -> None:
        """Set extra_data when saving project"""
        self.extra_data["with_fene"] = self.with_fene == FeneMode.with_fene

    def init_flow_mode(self) -> None:
        """Find if data files are shear or extension"""
        try:
            f = self.theory_files()[0]
            if f.file_type.extension == "shear":
                self.flow_mode = FlowMode.shear
            else:
                self.flow_mode = FlowMode.uext
        except Exception as e:
            print("in RP init:", e)
            self.flow_mode = FlowMode.shear  # default mode: shear

    def destructor(self) -> None:
        """Called when the theory tab is closed"""
        self.extra_graphic_visible(False)
        # self.ax.lines.remove(self.LVEenvelopeseries)
        self.LVEenvelopeseries.remove()

    def show_theory_extras(self, show: Any = False) -> None:
        """Called when the active theory is changed"""
        self.Qhide_theory_extras(show)
        # self.extra_graphic_visible(self.linearenvelope.isChecked())

    def extra_graphic_visible(self, state: Any) -> None:
        """Change visibility of theory helpers"""
        self.LVEenvelopeseries.set_visible(state)
        self.parent_dataset.parent_application.update_plot()

    def get_modes(self) -> tuple[Any, Any, bool]:
        """Get the values of Maxwell Modes from this theory"""
        nmodes: Any = self.parameters["nmodes"].value
        tau = np.zeros(nmodes)
        G = np.zeros(nmodes)
        for i in range(nmodes):
            tau[i] = self.parameters["tauD%02d" % i].value
            G[i] = self.parameters["G%02d" % i].value
        return tau, G, True

    def set_modes(self, tau: Any, G: Any) -> bool:
        """Set the values of Maxwell Modes from another theory"""
        nmodes = len(tau)
        self.set_param_value("nmodes", nmodes)
        self.set_param_value("nstretch", nmodes)

        for i in range(nmodes):
            self.set_param_value("tauD%02d" % i, tau[i])
            self.set_param_value("G%02d" % i, G[i])
        return True

    def sigmadot_shear(self, sigma: Any, t: Any, p: Any) -> list[Any]:
        """Rolie-Poly differential equation under *shear* flow
        with stretching and finite extensibility if selected"""
        if self.stop_theory_flag:
            raise EndComputationRequested
        sxx, syy, sxy = sigma
        lmax, tauD, tauR, beta, delta, gammadot = p

        # If the deformation rate is read from the file
        if self.read_gdot_action.isChecked():
            gammadot = np.interp(t, self.t, self.gfile)

        # Create the vector with the time derivative of sigma
        trace_sigma = sxx + 2 * syy
        l_sq = trace_sigma / 3.0  # stretch^2
        if self.with_fene == FeneMode.with_fene:
            fene = self.calculate_fene(l_sq, lmax)
            aux1 = 2.0 * (1.0 - 1.0 / sqrt(l_sq)) / tauR * fene
        else:
            aux1 = 2.0 * (1.0 - 1.0 / sqrt(l_sq)) / tauR
        aux2 = beta * (l_sq**delta)

        return [
            2 * gammadot * sxy - (sxx - 1.0) / tauD - aux1 * (sxx + aux2 * (sxx - 1.0)),
            -1.0 * (syy - 1.0) / tauD - aux1 * (syy + aux2 * (syy - 1.0)),
            gammadot * syy - sxy / tauD - aux1 * (sxy + aux2 * sxy),
        ]

    def sigmadot_shear_nostretch(self, sigma: Any, t: Any, p: Any) -> list[Any]:
        """Rolie-Poly differential equation under shear flow, without stretching"""
        if self.stop_theory_flag:
            raise EndComputationRequested
        sxx, syy, sxy = sigma
        _, tauD, _, beta, _, gammadot = p

        # If the deformation rate is read from the file
        if self.read_gdot_action.isChecked():
            gammadot = np.interp(t, self.t, self.gfile)

        # Create the vector with the time derivative of sigma
        return [
            2.0 * gammadot * sxy - (sxx - 1.0) / tauD - 2.0 / 3.0 * gammadot * sxy * (sxx + beta * (sxx - 1)),
            -(syy - 1.0) / tauD - 2.0 / 3.0 * gammadot * sxy * (syy + beta * (syy - 1)),
            gammadot * syy - sxy / tauD - 2.0 / 3.0 * gammadot * sxy * (sxy + beta * sxy),
        ]

    def sigmadot_uext(self, sigma: Any, t: Any, p: Any) -> list[Any]:
        """Rolie-Poly differential equation under *uniaxial elongational* flow
        with stretching and finite extensibility if selecter"""
        if self.stop_theory_flag:
            raise EndComputationRequested
        sxx, syy = sigma
        lmax, tauD, tauR, beta, delta, epsilon_dot = p

        # If the deformation rate is read from the file
        if self.read_gdot_action.isChecked():
            epsilon_dot = np.interp(t, self.t, self.gfile)

        # Create the vector with the time derivative of sigma
        trace_sigma = sxx + 2 * syy
        l_sq = trace_sigma / 3.0  # stretch^2
        if self.with_fene == FeneMode.with_fene:
            fene = self.calculate_fene(l_sq, lmax)
            aux1 = 2.0 * (1.0 - 1.0 / sqrt(l_sq)) / tauR * fene
        else:
            aux1 = 2.0 * (1.0 - 1.0 / sqrt(l_sq)) / tauR
        aux2 = beta * (l_sq**delta)

        dsxx = 2.0 * epsilon_dot * sxx - (sxx - 1.0) / tauD - aux1 * (sxx + aux2 * (sxx - 1.0))
        dsyy = -epsilon_dot * syy - (syy - 1.0) / tauD - aux1 * (syy + aux2 * (syy - 1.0))
        return [dsxx, dsyy]

    def sigmadot_uext_nostretch(self, sigma: Any, t: Any, p: Any) -> list[Any]:
        """Rolie-Poly differential equation under elongation flow, wihtout stretching"""
        if self.stop_theory_flag:
            raise EndComputationRequested
        sxx, syy = sigma
        _, tauD, tauR, beta, delta, epsilon_dot = p

        # If the deformation rate is read from the file
        if self.read_gdot_action.isChecked():
            epsilon_dot = np.interp(t, self.t, self.gfile)

        # Create the vector with the time derivative of sigma
        trace_k_sigma = epsilon_dot * (sxx - syy)
        aux1 = 2.0 / 3.0 * trace_k_sigma
        return [
            2.0 * epsilon_dot * sxx - (sxx - 1.0) / tauD - aux1 * (sxx + beta * (sxx - 1.0)),
            -epsilon_dot * syy - (syy - 1.0) / tauD - aux1 * (syy + beta * (syy - 1.0)),
        ]

    def sigmadot_shearLAOS(self, sigma: Any, t: Any, p: Any) -> list[Any]:
        """Rolie-Poly differential equation under *shear* flow
        with stretching and finite extensibility if selected"""
        if self.stop_theory_flag:
            raise EndComputationRequested
        sxx, syy, sxy = sigma
        lmax, tauD, tauR, beta, delta, g0, w = p
        gammadot = g0 * w * np.cos(w * t)

        # Create the vector with the time derivative of sigma
        trace_sigma = sxx + 2 * syy
        l_sq = trace_sigma / 3.0  # stretch^2
        if self.with_fene == FeneMode.with_fene:
            fene = self.calculate_fene(l_sq, lmax)
            aux1 = 2.0 * (1.0 - 1.0 / sqrt(l_sq)) / tauR * fene
        else:
            aux1 = 2.0 * (1.0 - 1.0 / sqrt(l_sq)) / tauR
        aux2 = beta * (l_sq**delta)

        return [
            2 * gammadot * sxy - (sxx - 1.0) / tauD - aux1 * (sxx + aux2 * (sxx - 1.0)),
            -1.0 * (syy - 1.0) / tauD - aux1 * (syy + aux2 * (syy - 1.0)),
            gammadot * syy - sxy / tauD - aux1 * (sxy + aux2 * sxy),
        ]

    def sigmadot_shear_nostretchLAOS(self, sigma: Any, t: Any, p: Any) -> list[Any]:
        """Rolie-Poly differential equation under shear flow, without stretching"""
        if self.stop_theory_flag:
            raise EndComputationRequested
        sxx, syy, sxy = sigma
        _, tauD, _, beta, _, g0, w = p
        gammadot = g0 * w * np.cos(w * t)

        # Create the vector with the time derivative of sigma
        return [
            2.0 * gammadot * sxy - (sxx - 1.0) / tauD - 2.0 / 3.0 * gammadot * sxy * (sxx + beta * (sxx - 1)),
            -(syy - 1.0) / tauD - 2.0 / 3.0 * gammadot * sxy * (syy + beta * (syy - 1)),
            gammadot * syy - sxy / tauD - 2.0 / 3.0 * gammadot * sxy * (sxy + beta * sxy),
        ]

    def calculate_fene(self, l_square: Any, lmax: Any) -> Any:
        """calculate finite extensibility function value"""
        ilm2 = 1.0 / (lmax * lmax)  # 1/lambda_max^2
        l2_lm2 = l_square * ilm2  # (lambda/lambda_max)^2
        return (3.0 - l2_lm2) / (1.0 - l2_lm2) * (1.0 - ilm2) / (3.0 - ilm2)

    def RoliePoly(self, f: FileLike | None = None) -> None:
        """Calculate the theory"""
        file = cast(FileLike, f)
        ft = file.data_table
        tt = self.tables[file.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        # flow geometry and finite extensibility
        if self.flow_mode == FlowMode.shear:
            sigma0 = [1.0, 1.0, 0.0]  # sxx, syy, sxy
            pde_nostretch = self.sigmadot_shear_nostretch
            pde_stretch = self.sigmadot_shear
        elif self.flow_mode == FlowMode.uext:
            sigma0 = [1.0, 1.0]  # sxx, syy
            pde_nostretch = self.sigmadot_uext_nostretch
            pde_stretch = self.sigmadot_uext
        else:
            return

        # ODE solver parameters
        abserr = 1.0e-8
        relerr = 1.0e-6
        self.t = ft.data[:, 0]
        if file.file_type.extension == "shear":
            self.gfile = ft.data[:, 3]
        elif file.file_type.extension == "uext":
            self.gfile = ft.data[:, 2]
        self.t = np.concatenate([[0], self.t])
        self.gfile = np.concatenate([[self.gfile[0]], self.gfile])
        # sigma0 = [1.0, 1.0, 0.0]  # sxx, syy, sxy
        beta: Any = self.parameters["beta"].value
        delta: Any = self.parameters["delta"].value
        lmax: Any = self.parameters["lmax"].value
        flow_rate = float(file.file_parameters["gdot"])
        nmodes: Any = self.parameters["nmodes"].value
        nstretch: Any = self.parameters["nstretch"].value
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            tauD = self.parameters["tauD%02d" % i].value
            tauR = self.parameters["tauR%02d" % i].value
            p = [lmax, tauD, tauR, beta, delta, flow_rate]
            if i < nstretch:
                try:
                    sig = odeint(pde_stretch, sigma0, self.t, args=(p,), atol=abserr, rtol=relerr)
                except EndComputationRequested:
                    break
            else:
                try:
                    sig = odeint(
                        pde_nostretch,
                        sigma0,
                        self.t,
                        args=(p,),
                        atol=abserr,
                        rtol=relerr,
                    )
                except EndComputationRequested:
                    break

            sxx = np.delete(sig[:, 0], [0])
            syy = np.delete(sig[:, 1], [0])
            if self.flow_mode == FlowMode.shear:
                sxy = np.delete(sig[:, 2], [0])
                tt.data[:, 1] += self.parameters["G%02d" % i].value * sxy
            elif self.flow_mode == FlowMode.uext:
                tt.data[:, 1] += self.parameters["G%02d" % i].value * (sxx - syy)

            if self.with_fene == FeneMode.with_fene:
                ilm2 = 1.0 / (lmax * lmax)  # 1/lambda_max^2
                l_sq_arr = (sxx + 2.0 * syy) / 3.0  # array lambda^2
                l2_lm2_arr = l_sq_arr * ilm2  # array (lambda/lambda_max)^2
                fene_arr = (3.0 - l2_lm2_arr) / (1.0 - l2_lm2_arr) * (1.0 - ilm2) / (3.0 - ilm2)  # fene array
                tt.data[:, 1] *= fene_arr

    def RoliePolyLAOS(self, f: FileLike | None = None) -> None:
        """Calculate the theory for LAOS"""
        file = cast(FileLike, f)
        ft = file.data_table
        tt = self.tables[file.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        # flow geometry and finite extensibility
        sigma0 = [1.0, 1.0, 0.0]  # sxx, syy, sxy
        pde_nostretchLAOS = self.sigmadot_shear_nostretchLAOS
        pde_stretchLAOS = self.sigmadot_shearLAOS

        # ODE solver parameters
        abserr = 1.0e-8
        relerr = 1.0e-6
        beta: Any = self.parameters["beta"].value
        delta: Any = self.parameters["delta"].value
        lmax: Any = self.parameters["lmax"].value
        g0 = float(file.file_parameters["gamma"])
        w = float(file.file_parameters["omega"])
        nmodes: Any = self.parameters["nmodes"].value
        nstretch: Any = self.parameters["nstretch"].value
        t = ft.data[:, 0]
        tt.data[:, 1] = g0 * np.sin(w * t)
        t = np.concatenate([[0], t])
        for i in range(nmodes):
            if self.stop_theory_flag:
                break
            tauD = self.parameters["tauD%02d" % i].value
            tauR = self.parameters["tauR%02d" % i].value
            p = [lmax, tauD, tauR, beta, delta, g0, w]
            if i < nstretch:
                try:
                    sig = odeint(pde_stretchLAOS, sigma0, t, args=(p,), atol=abserr, rtol=relerr)
                except EndComputationRequested:
                    break
            else:
                try:
                    sig = odeint(
                        pde_nostretchLAOS,
                        sigma0,
                        t,
                        args=(p,),
                        atol=abserr,
                        rtol=relerr,
                    )
                except EndComputationRequested:
                    break

            sxx = np.delete(sig[:, 0], [0])
            syy = np.delete(sig[:, 1], [0])
            sxy = np.delete(sig[:, 2], [0])
            tt.data[:, 2] += self.parameters["G%02d" % i].value * sxy

            if self.with_fene == FeneMode.with_fene:
                ilm2 = 1.0 / (lmax * lmax)  # 1/lambda_max^2
                l_sq_arr = (sxx + 2.0 * syy) / 3.0  # array lambda^2
                l2_lm2_arr = l_sq_arr * ilm2  # array (lambda/lambda_max)^2
                fene_arr = (3.0 - l2_lm2_arr) / (1.0 - l2_lm2_arr) * (1.0 - ilm2) / (3.0 - ilm2)  # fene array
                tt.data[:, 2] *= fene_arr

    def set_param_value(self, name: Any, value: Any) -> tuple[str, bool]:
        """Set the value of a theory parameter"""
        if name == "nmodes":
            oldn: Any = self.parameters["nmodes"].value
            self.spinbox.setMaximum(int(value))
        message, success = super(TheoryRoliePoly, self).set_param_value(name, value)
        if not success:
            return message, success
        if name == "nmodes":
            nmodes: Any = self.parameters["nmodes"].value
            for i in range(nmodes):
                self.parameters["G%02d" % i] = Parameter(
                    name="G%02d" % i,
                    value=1000.0,
                    description="Modulus of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.nopt,
                    display_flag=False,
                    min_value=0,
                    quantity="stress",
                    internal_unit="Pa",
                    display_unit="Pa",
                )
                self.parameters["tauD%02d" % i] = Parameter(
                    name="tauD%02d" % i,
                    value=10.0,
                    description="Terminal time of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.nopt,
                    display_flag=False,
                    min_value=0,
                    quantity="time",
                    internal_unit="s",
                    display_unit="s",
                )
                self.parameters["tauR%02d" % i] = Parameter(
                    name="tauR%02d" % i,
                    value=0.5,
                    description="Rouse time of mode %02d" % i,
                    type=ParameterType.real,
                    opt_type=OptType.opt,
                    display_flag=True,
                    min_value=0,
                    quantity="time",
                    internal_unit="s",
                    display_unit="s",
                )
            if oldn > nmodes:
                for i in range(nmodes, oldn):
                    del self.parameters["G%02d" % i]
                    del self.parameters["tauD%02d" % i]
                    del self.parameters["tauR%02d" % i]
        return "", True
