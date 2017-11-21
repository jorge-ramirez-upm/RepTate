import sys
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QTableWidget, QApplication

class CustomQTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy):
            self.copy()
        elif event.matches(QKeySequence.Paste):
            self.paste()
        else:
            QTableWidget.keyPressEvent(self, event)
 
    def copy(self):
        """Copy the selected data of the dataInspector into the clipboard"""
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
            QApplication.clipboard().setText(text);

    def paste(self):
        text = QApplication.clipboard().text()
        if text=="":
            return
        rows = text.split("\r") #this is Excel's carriage return...
        for i in range(len(rows)):
            cols = rows[i].split("\t")
            for j in range(len(cols)):
                self.item(i, j).setText(cols[j])