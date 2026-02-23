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
"""Module to import pasted data

"""
import sys
import os
import io
import numpy as np
from PySide6.QtWidgets import QApplication, QDialog
import RepTate

if getattr(sys, "frozen", False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    PATH = sys._MEIPASS
else:
    PATH = os.path.dirname(os.path.abspath(__file__))
from RepTate.gui.Ui_ImportPastedMainWindow import Ui_Dialog as Ui_ImportPastedMainWindow


class ImportFromPastedWindow(QDialog, Ui_ImportPastedMainWindow):
    def __init__(self, parent=None, ftype=None):
        super().__init__()
        self.setupUi(self)
        self.col_names = ftype.col_names
        self.col_units = ftype.col_units
        self.file_param = ftype.basic_file_parameters
        self.num_cols = len(self.col_names)
        txt = ""
        if self.file_param:
            txt += (
                "Parameters values describing the data can be added to the first line as:<br><b>%s=val;</b><br>"
                % ("=val;".join(self.file_param))
            )
        col_labels = [
            "%s [%s]" % (name, unit)
            for name, unit in zip(self.col_names, self.col_units)
        ]
        txt += "The first <b>%d</b> columns should contain values for:<br><b>%s</b>" % (
            len(self.col_names),
            ", ".join(col_labels),
        )
        self.label_columns.setText(txt)

    def set_fname_dialog(self, fname):
        self.file_name_label.setText(fname)

    def get_data(self):
        pasted_txt = self.paste_box.toPlainText()
        flag_nan = False
        is_first_line = True
        first_line_has_param = False
        all_data = np.empty((0, self.num_cols))
        param_read = {}
        buf = io.StringIO(pasted_txt)
        for line in buf:
            if is_first_line:
                is_first_line = False
                params_set = line.split(";")
                for param in params_set:
                    p = param.split("=")
                    if len(p) > 1:
                        pname = p[0]
                        pval = p[1]
                        if pname in self.file_param:
                            try:
                                param_read[pname] = float(pval)
                                first_line_has_param = True
                            except ValueError:
                                pass
                if first_line_has_param:
                    continue

            vals = line.split()
            data_row = []
            for i in range(self.num_cols):
                try:
                    data_row.append(float(vals[i]))
                except (ValueError, IndexError):
                    data_row.append(np.nan)

            if all(val is np.nan for val in data_row):
                # Line contain no values. Skip this line.
                continue
            else:
                if any(val is np.nan for val in data_row):
                    flag_nan = True
                all_data = np.vstack([all_data, data_row])
        x = all_data[:, 0]
        y = all_data[:, 1]
        if self.num_cols > 2:
            z = all_data[:, 2]
        else:
            z = []
        if self.num_cols > 3:
            z2 = all_data[:, 3]
        else:
            z2 = []

        return {
            "nrows": len(all_data),
            "flag_nan": flag_nan,
            "param_read": param_read,
            "fname": self.file_name_label.text(),
            "x": x,
            "y": y,
            "z": z,
            "z2": z2,
        }


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.exit(app.exec())
