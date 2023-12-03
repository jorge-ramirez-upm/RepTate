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
"""Module theory_helpers

Module that contains classes that are used in several theories

"""
import enum
import numpy as np
from PySide6.QtWidgets import (
    QSpinBox,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QDialogButtonBox,
    QTableWidgetItem,
    QMessageBox,
    QLabel,
    QLineEdit,
    QButtonGroup,
    QRadioButton,
)
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt
from RepTate.gui.SpreadsheetWidget import SpreadsheetWidget

"""
 _____                           
| ____|_ __  _   _ _ __ ___  ___ 
|  _| | '_ \| | | | '_ ` _ \/ __|
| |___| | | | |_| | | | | | \__ \
|_____|_| |_|\__,_|_| |_| |_|___/

Diverse Enumerations to set calculation modes
"""


class FlowMode(enum.Enum):
    """Defines the flow geometry used
    
    Parameters can be:
        - shear: Shear flow
        - uext: Uniaxial extension flow
    """

    shear = 0
    uext = 1


class FeneMode(enum.Enum):
    """Defines the finite extensibility function
    
    Parameters can be:
        - none: No finite extensibility
        - with_fene: With finite extensibility
    """

    none = 0
    with_fene = 1


class GcorrMode(enum.Enum):
    """Primitive path fluctuations reduce the terminal modulus due to shortened tube.
    Defines if we include that correction.

    Parameters can be:
        - none: No finite extensibility
        - with_gcorr: With finite extensibility
    """

    none = 0
    with_gcorr = 1


class NoquMode(enum.Enum):
    """Primitive path fluctuations reduce the terminal modulus due to shortened tube.
    Defines if we include that correction.

    Parameters can be:
        - none: No primitive path fluctuations
        - with_noqu: With primitive path fluctuation
    """

    none = 0
    with_noqu = 1


class SingleSpeciesMode(enum.Enum):
    """Uses a single average species to compute the nucleation rate.
    Defines if we include that approximation.

    Parameters can be:
        - none: use all modes
        - with_single: Just use a single mode
    """

    none = 0
    with_single = 1


"""
 ____  _       _                 
|  _ \(_) __ _| | ___   __ _ ___ 
| | | | |/ _` | |/ _ \ / _` / __|
| |_| | | (_| | | (_) | (_| \__ \
|____/|_|\__,_|_|\___/ \__, |___/
                       |___/     

Diverse dialogs to set/get/edit Maxwell modes, volume fractions, etc
"""


class EditModesDialog(QDialog):
    """
    Dialog to edit the amplitudes and relaxation times of a set of Maxwell modes
    """

    def __init__(self, parent=None, times=0, G=0, MAX_MODES=0):
        super(EditModesDialog, self).__init__(parent)

        self.setWindowTitle("Edit Maxwell modes")
        layout = QVBoxLayout(self)
        nmodes = len(times)

        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, MAX_MODES)  # min and max number of modes
        self.spinbox.setSuffix(" modes")
        self.spinbox.setValue(nmodes)  # initial value
        layout.addWidget(self.spinbox)

        self.table = SpreadsheetWidget()  # allows copy/paste
        self.table.setRowCount(nmodes)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["tauD", "G"])
        for i in range(nmodes):
            tau = "%g" % times[i]
            mod = "%g" % G[i]
            self.table.setItem(i, 0, QTableWidgetItem(tau))
            self.table.setItem(i, 1, QTableWidgetItem(mod))

        layout.addWidget(self.table)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged
        )

    def handle_spinboxValueChanged(self, value):
        nrow_old = self.table.rowCount()
        self.table.setRowCount(value)
        for i in range(nrow_old, value):  # create extra rows with defaut values
            self.table.setItem(i, 0, QTableWidgetItem("10"))
            self.table.setItem(i, 1, QTableWidgetItem("1000"))


class EditModesVolFractionsDialog(QDialog):
    """
    Dialog to edit the volume fractions and relaxation times for a polydisperse sample
    """

    def __init__(self, parent=None, param_dic={}, MAX_MODES=0):
        super().__init__(parent)

        self.setWindowTitle("Edit volume fractions and relaxation times")
        layout = QVBoxLayout(self)
        self.nparam = len(param_dic)
        pnames = list(param_dic.keys())
        nmodes = len(param_dic[pnames[0]])

        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, MAX_MODES)  # min and max number of modes
        self.spinbox.setSuffix(" modes")
        self.spinbox.setValue(nmodes)  # initial value
        layout.addWidget(self.spinbox)

        self.table = SpreadsheetWidget()  # allows copy/paste
        self.table.setRowCount(nmodes)
        self.table.setColumnCount(self.nparam)
        self.table.setHorizontalHeaderLabels(pnames)
        for i in range(nmodes):
            for j in range(self.nparam):
                self.table.setItem(
                    i, j, QTableWidgetItem("%g" % param_dic[pnames[j]][i])
                )
        layout.addWidget(self.table)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept_)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged
        )

    def accept_(self):
        sum = 0
        for i in range(self.table.rowCount()):
            sum += float(self.table.item(i, 0).text())
        if abs(sum - 1) < 0.02:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "phi must add up to 1")

    def handle_spinboxValueChanged(self, value):
        nrow_old = self.table.rowCount()
        self.table.setRowCount(value)
        for i in range(nrow_old, value):  # create extra rows with defaut values
            for j in range(self.nparam):
                self.table.setItem(i, j, QTableWidgetItem("0"))


class GetMwdRepTate(QDialog):
    """
    Dialog to get the MWD from RepTate
    """

    def __init__(self, parent=None, th_dict={}, title="title"):
        super().__init__(parent)

        self.setWindowTitle(title)
        layout = QVBoxLayout(self)

        validator = QDoubleValidator()
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Me"))
        self.Me_text = QLineEdit("%.3g" % parent.parameters["Me"].value)
        self.Me_text.setValidator(validator)
        hlayout.addWidget(self.Me_text)

        hlayout.addWidget(QLabel("taue"))
        self.taue_text = QLineEdit("%.3g" % parent.parameters["tau_e"].value)
        self.taue_text.setValidator(validator)
        hlayout.addWidget(self.taue_text)

        layout.addLayout(hlayout)

        self.btngrp = QButtonGroup()

        for item in th_dict.keys():
            rb = QRadioButton(item, self)
            layout.addWidget(rb)
            self.btngrp.addButton(rb)
        # default button selection
        rb = self.btngrp.buttons()[0]
        rb.setChecked(True)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


class EditMWDDialog(QDialog):
    """
    Dialog to edit the MWD
    """

    def __init__(self, parent=None, m=None, phi=None, MAX_MODES=0):
        super().__init__(parent)

        self.setWindowTitle("Input Molecular weight distribution")
        layout = QVBoxLayout(self)

        validator = QDoubleValidator()
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Me"))
        self.Me_text = QLineEdit("%.4g" % parent.parameters["Me"].value)
        self.Me_text.setValidator(validator)
        hlayout.addWidget(self.Me_text)

        hlayout.addWidget(QLabel("taue"))
        self.taue_text = QLineEdit("%.4g" % parent.parameters["tau_e"].value)
        self.taue_text.setValidator(validator)
        hlayout.addWidget(self.taue_text)

        layout.addLayout(hlayout)
        nmodes = len(phi)

        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, MAX_MODES)  # min and max number of modes
        self.spinbox.setSuffix(" modes")
        self.spinbox.setValue(nmodes)  # initial value
        layout.addWidget(self.spinbox)

        self.table = SpreadsheetWidget()  # allows copy/paste
        self.table.setRowCount(nmodes)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["M", "phi"])
        for i in range(nmodes):
            self.table.setItem(i, 0, QTableWidgetItem("%g" % m[i]))
            self.table.setItem(i, 1, QTableWidgetItem("%g" % phi[i]))

        layout.addWidget(self.table)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept_)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged
        )

    def accept_(self):
        sum = 0
        for i in range(self.table.rowCount()):
            sum += float(self.table.item(i, 1).text())
        if abs(sum - 1) < 0.02:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "phi must add up to 1")

    def handle_spinboxValueChanged(self, value):
        nrow_old = self.table.rowCount()
        self.table.setRowCount(value)
        for i in range(nrow_old, value):  # create extra rows with defaut values
            self.table.setItem(i, 0, QTableWidgetItem("0"))
            self.table.setItem(i, 1, QTableWidgetItem("1000"))


"""
  ___  _   _                   
 / _ \| |_| |__   ___ _ __ ___ 
| | | | __| '_ \ / _ \ '__/ __|
| |_| | |_| | | |  __/ |  \__ \
 \___/ \__|_| |_|\___|_|  |___/

 Classes that are used by several theories to help calculate the results.
"""


class Dilution:
    """
    Dilution effects
    """

    def __init__(self, m, phi, taue, Me, parent_theory):
        super().__init__()
        self.parent_theory = parent_theory
        self.res = self.relax_times_from_mwd(m, phi, taue, Me)

    def find_down_indx(self, tauseff, taud):
        """Find index i such that taud[i] < tauseff < taud[i+1]
        or returns -1 if tauseff < taud[0]
        or returns n-1 if tauseff > taud[n-1] (should not happen)
        """
        n = len(taud)
        down = n - 1
        while tauseff < taud[down]:
            if down == 0:
                down = -1
                break
            down -= 1
        return down

    def find_dilution(self, phi, taud, taus, interp=True):
        """Find the dilution factor phi_dil for a chain with bare stretch relax time `taus`"""
        n = len(phi)
        temp = -1
        phi_dil = 1
        tauseff = taus / phi_dil
        # m[0] < m[1] <  ... < m[n]
        while True:
            down = self.find_down_indx(tauseff, taud)
            if down == -1:
                # case tauseff < taud[0]
                phi_dil = 1
                break
            elif down == n - 1:
                # (just in case) tauseff > taud[n-1]
                phi_dil = phi[n - 1]
                break
            else:
                # change tauseff and check if 'down' is still the same
                if temp == down:
                    break
                temp = down
                phi_dil = 1.0
                for k in range(down):
                    phi_dil -= phi[k]
                if interp:
                    # x=0 if tauseff close to td[down], x=1 if tauseff close to td[down+1]
                    x = (tauseff - taud[down]) / (taud[down + 1] - taud[down])
                    # linear interpolation of phi_dil
                    phi_dil = phi_dil - x * phi[down]
                else:
                    phi_dil -= phi[down]
            tauseff = taus / phi_dil
        return phi_dil

    def sort_list(self, m, phi):
        """Ensure m[0] <= m[1] <=  ... <= m[n]"""
        if all(m[i] <= m[i + 1] for i in range(len(m) - 1)):
            # list aready sorted
            return m, phi
        args = np.argsort(m)
        m = list(np.array(m)[args])
        phi = list(np.array(phi)[args])
        return m, phi

    def relax_times_from_mwd(self, m, phi, taue, Me):
        """Guess relaxation times of linear rheology (taud) from molecular weight distribution.
        (i) Count short chains (M < 2*Me) as solvent
        (ii) The effective dilution at a given timescale t is equal to the sum of
        the volume fractions of all chains with relaxation time greater than t
        (iii) CLF makes use of the most diluted tube available at the CLF timescale
        """
        # m[0] < m[1] <  ... < m[n]
        m, phi = self.sort_list(m, phi)

        taus = []
        taus_short = []
        taud = []
        phi_short = []
        m_short = []
        phi_u = 0
        nshort = 0

        n = len(m)
        for i in range(n):
            z = m[i] / Me
            ts = z * z * taue
            if m[i] < 2.0 * Me:
                # short chains not entangled: use upper-convected Maxwell model
                nshort += 1
                phi_u += phi[i]
                taus_short.append(ts)
                phi_short.append(phi[i])
                m_short.append(m[i])
            else:
                taus.append(ts)

        # remove the short chains from the list of M and phi
        m = m[nshort:]
        phi = phi[nshort:]

        n = len(m)  # new size
        if n == 0:
            self.parent_theory.Qprint("All chains as solvent")
            return [False]
        if n == 1:
            return [True, phi, taus, [3 * z * ts,]]

        Zeff = [0] * n
        # renormalize the fraction of entangled chains
        Me /= 1 - phi_u
        taue /= (1 - phi_u) * (1 - phi_u)
        for i in range(n):
            phi[i] /= 1 - phi_u
            z = m[i] / Me
            taud.append(3.0 * z * z * z * taue)

        vphi = []
        interp = n > 2  # true if more than two species
        for i in range(n):
            # find dilution for the entangled chains
            if i == 0:
                phi_dil = 1
            else:
                phi_dil = self.find_dilution(phi, taud, taus[i], interp=interp)
            vphi.append(phi_dil)

        for i in range(n):
            z = m[i] / Me
            if z * vphi[i] < 1 and z > 1:
                # case where long chains are effectively untentangled
                # CR-Rouse approximated as last taud having z*vphi > 1
                taud_sticky_rep = taud[i - 1]
                for j in range(i, n):
                    taud[j] = taud_sticky_rep
                    Zeff[j] = 1.0
                break
            taud[i] = taud[i] * self.parent_theory.fZ(z * vphi[i])
            Zeff[i] = z * vphi[i]
        self.parent_theory.Zeff = np.array(Zeff)

        return [True, phi, taus, taud]
