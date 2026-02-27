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
"""Module DataSetWidgetItem

Module that defines the a DataSetWidgetItem that allows to sort items in the DataSet

"""
from PySide6.QtWidgets import QTreeWidgetItem


class DataSetWidgetItem(QTreeWidgetItem):
    """Subclass of QTreeWidgetItem for dataset items
    
    Each item of a dataset is a wrapper of the QTreeWidgetItem
    It contains the necessary tables and types and a redefinition of the '<' operator
    """

    series = 0

    def __init__(self, parent=None):
        """**Constructor**"""
        QTreeWidgetItem.__init__(self, parent)

    def __init__(self, parent=None, itemlist=[], type=0):
        """**Constructor**"""
        QTreeWidgetItem.__init__(self, parent, itemlist, type)

    def __init__(
        self, parent=None, itemlist=[], type=0, file_name_short="dummy", file_type=None
    ):
        """**Constructor**"""
        QTreeWidgetItem.__init__(self, parent, itemlist, type)
        # self.file_name_short = file_name_short
        # Table.__init__(self, file_name_short, file_type)

    def __lt__(self, otherItem):
        """Needed for sorting purposes
        
        Re-implement the less-than operator to sort the columns based on the float
        value of the cells, not the strig value"""
        column = self.treeWidget().sortColumn()
        try:
            return float(self.text(column)) > float(otherItem.text(column))
        except ValueError:
            return self.text(column) > otherItem.text(column)
