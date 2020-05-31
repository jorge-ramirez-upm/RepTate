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
# Copyright (2017-2020): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
import numpy as np
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication
import RepTate

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    PATH = sys._MEIPASS
else:
    PATH = os.path.dirname(os.path.abspath(__file__))
Ui_ImportPastedMainWindow, QMainWindowImportPasted = loadUiType(
    os.path.join(PATH, "import_from_pasted_dialog.ui")
)


class ImportFromPastedWindow(QMainWindowImportPasted, Ui_ImportPastedMainWindow):

    def __init__(self, parent=None, headers=["w", "G'", "G''"], file_param=["Mw", "T"]):
        super().__init__()
        self.setupUi(self)
        self.headers = headers
        self.file_param = file_param
        self.num_cols = len(headers)

    def get_data(self):
        pasted_txt = self.textbox.toPlainText()
        import io
        flag_nan = False
        is_first_line = True
        first_line_has_param = False
        x = []
        y = []
        z = []
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
            try:
                x.append(float(vals[0]))
            except (ValueError, IndexError):
                x.append(np.nan)
                flag_nan = True
            try:
                y.append(float(vals[1]))
            except (ValueError, IndexError):
                y.append(np.nan)
                flag_nan = True
            if self.num_cols > 2:
                try:
                    z.append(float(vals[2]))
                except (ValueError, IndexError):
                    z.append(np.nan)
                    flag_nan = True
        return {"flag_nan": flag_nan, "param_read": param_read, "x": np.array(x), "y": np.array(y), "z": np.array(z)}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
