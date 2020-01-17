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
"""Module SpreadsheetWidget

Module that defines a QTableWidget that allows copy/paste of data.

""" 
import sys
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTableWidget, QApplication


class SpreadsheetWidget(QTableWidget):
    """Subclass of QTableWidget

    Subclass of QTableWidget that enables (i) to copy selected QTableWidget items to the clipboard
    in a tab-separated format and (ii) to paste the content of the clipboard into the QTableWidget
    """
    def __init__(self, parent=None):
        """[summary]

        [description]

        Keyword Arguments:
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(parent)
        delete_disabled = True # disable the possibility to delete rows
        file_repr = None # store the file object represented in the table

    def keyPressEvent(self, event):
        """[summary]

        [description]

        Arguments:
            event {[type]} -- [description]
        """
        if event.matches(QKeySequence.Copy):
            self.copy()
        elif event.matches(QKeySequence.Paste):
            self.paste()
        elif event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
            self.delete()
        else:
            QTableWidget.keyPressEvent(self, event)
    
    def delete(self):
        if self.delete_disabled:
            pass
        else:
            sel = self.selectedIndexes() #returns a list of all selected item indexes in the view
            if sel:
                row_list = []
                for ind in range(len(sel)):
                    row_list.append(sel[ind].row())
                row_list = list(set(row_list))
                self.file_repr.data_table.data = np.delete(self.file_repr.data_table.data, row_list, axis=0)
                self.file_repr.data_table.num_rows -= len(row_list)
                self.file_repr.parent_dataset.populate_inspector()
                self.file_repr.parent_dataset.do_plot() # TODO: we only need to update one data series, not the whole ds
    
    def copy(self):
        """Copy the selected data of the dataInspector into the clipboard

        [description]
        """
        sel = self.selectedIndexes() #returns a list of all selected item indexes in the view
        if sel:
            text = ""
            row0 = sel[0].row()
            for ind in range(len(sel)):
                row = sel[ind].row()
                col = sel[ind].column()
                if row != row0:
                    row0 = row
                    text = text.rstrip('\t') #remove tab at the end of line
                    text += '\n'
                text += self.item(row, col).text()
                text += '\t' #tab separated format
            text = text.rstrip('\t')
            QApplication.clipboard().setText(text)

    def paste(self):
        """[summary]

        [description]
        """
        text = QApplication.clipboard().text()
        if text == '':
            return
        # Replace commas if any
        text = text.replace(',', ' ')

        rows = text.splitlines() # split on newlines
        for i in range(len(rows)):
            cols = rows[i].split() # split on whitespaces
            for j in range(len(cols)):
                try:
                    self.item(i, j).setText(cols[j])
                except AttributeError:
                    #index out of range
                    #more data to paste than table entries
                    pass 
