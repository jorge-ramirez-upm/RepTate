from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTreeWidget, QMessageBox

class SubQTreeWidget(QTreeWidget):
    """Subclass of QTreeWidget that allows to select nothing in the DataSet 
    by clicking in the white area of the DataSet, and allows to delete a data table item"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_dataset = parent

    """Allow to select nothing in the DataSet by clicking in the white area of the DataSet"""
    def mousePressEvent(self, event):
        self.clearSelection()
        QTreeWidget.mousePressEvent(self, event)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.delete()
        else:
            QTreeWidget.keyPressEvent(self, event)

    def delete(self):
        """Delete the currently selected items"""
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
        for ind in index_to_rm: #remove the table widget
            self.takeTopLevelItem(ind)
