# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module SubQTreeWidget

Module that defines the a QTreeWidget that allows to select nothing.

""" 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QMessageBox

class SubQTreeWidget(QTreeWidget):
    """Subclass of QTreeWidget
    
    Subclass of QTreeWidget that allows to select nothing in the DataSet 
    by clicking in the white area of the DataSet, and allows to delete a data table item
    """
    def __init__(self, parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            parent {[type]} -- [description] (default: {None})
        """
        super().__init__(parent)
        self.parent_dataset = parent

    def mousePressEvent(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            event {[type]} -- [description]
        """
        self.clearSelection()
        QTreeWidget.mousePressEvent(self, event)
    
    def keyPressEvent(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            event {[type]} -- [description]
        """
        if event.key() == Qt.Key_Backspace:
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
                    for i in range(file.data_table.MAX_NUM_SERIES):
                        self.parent_dataset.parent_application.ax.lines.remove(file.data_table.series[i]) 
                    self.parent_dataset.files.remove(file)
                    break

            for th in self.parent_dataset.theories.values(): #remove corresponding theory lines
                print(th.tables)
                try:
                    table = th.tables[file_name_short]
                    for i in range(table.MAX_NUM_SERIES):
                        self.parent_dataset.parent_application.ax.lines.remove(table.series[i])  
                    del th.tables[file_name_short]
                except KeyError:
                    pass
        for ind in index_to_rm: 
            self.takeTopLevelItem(ind) #remove the table widget
        
        if self.topLevelItemCount() == 0:   
            self.parent_dataset.parent_application.dataset_actions_disabled(True) #desactivate buttons

