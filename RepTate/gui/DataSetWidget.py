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
"""Module DataSetWidget

Module that defines the a QTreeWidget that allows to select nothing.

""" 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QMessageBox

class DataSetWidget(QTreeWidget):
    """Subclass of QTreeWidget
    
    Subclass of QTreeWidget that allows to select nothing in the DataSet 
    by clicking in the white area of the DataSet, and allows to delete a data table item
    """
    def __init__(self, parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(parent)
        self.parent_dataset = parent

    def mousePressEvent(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        self.clearSelection()
        QTreeWidget.mousePressEvent(self, event)
    
    def keyPressEvent(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        if event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
            self.delete()
        else:
            QTreeWidget.keyPressEvent(self, event)

    def delete(self):
        """Delete the currently selected items
        
        [description]
        """
        selection = self.selectedItems()
        if selection == []:
            return
        index_to_rm = []
        for item in selection:
            index_to_rm.append(self.indexOfTopLevelItem(item)) #save indices to delete
            file_name_short = item.text(0)
            
            for file in self.parent_dataset.files: #remove files and lines
                if file.file_name_short == file_name_short:  
                    dt = file.data_table
                    for i in range(dt.MAX_NUM_SERIES):
                        for nx in range(self.parent_dataset.nplots):
                            self.parent_dataset.parent_application.axarr[nx].lines.remove(dt.series[nx][i]) 
                    self.parent_dataset.files.remove(file)
                    break

            for th in self.parent_dataset.theories.values(): #remove corresponding theory lines
                try:
                    tt = th.tables[file_name_short]
                    for i in range(tt.MAX_NUM_SERIES):
                        for nx in range(self.parent_dataset.nplots):
                            self.parent_dataset.parent_application.axarr[nx].lines.remove(tt.series[nx][i])  
                    del th.tables[file_name_short]
                except KeyError:
                    pass
        for ind in index_to_rm: 
            self.takeTopLevelItem(ind) #remove the table widget
        
        if self.topLevelItemCount() == 0:   
            self.parent_dataset.parent_application.dataset_actions_disabled(True) #desactivate buttons

