# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module SubQTreeWidgetItem

Module that defines the a SubQTreeWidgetItem that allows to sort items in the DataSet

""" 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QTreeWidgetItem
#from Table import *

class SubQTreeWidgetItem(QTreeWidgetItem):
    """Subclass of QTreeWidgetItem for dataset items
    
    Each item of a dataset is a wrapper of the QTreeWidgetItem
    It contains the necessary tables and types and a redefinition of the '<' operator
    """
    series=0

    def __init__(self, parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            parent {[type]} -- [description] (default: {None})
        """
        QTreeWidgetItem.__init__(self, parent)

    def __init__(self, parent=None, itemlist=[], type=0):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            parent {[type]} -- [description] (default: {None})
            type {[type]} -- [description] (default: {0})
        """
        QTreeWidgetItem.__init__(self, parent, itemlist, type)

    def __init__(self, parent=None, itemlist=[], type=0, file_name_short="dummy", file_type=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            parent {[type]} -- [description] (default: {None})
            type {[type]} -- [description] (default: {0})
            file_name_short {[type]} -- [description] (default: {"dummy"})
            file_type {[type]} -- [description] (default: {None})
        """
        QTreeWidgetItem.__init__(self, parent, itemlist, type)
        # self.file_name_short = file_name_short
        #Table.__init__(self, file_name_short, file_type)

    def __lt__(self, otherItem):
        """Needed for sorting purposes
        
        Re-implement the less-than operator to sort the columns based on the float
        value of the cells, not the strig value
        
        Arguments:
            otherItem {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        column = self.treeWidget().sortColumn()
        try:
            return float( self.text(column) ) > float( otherItem.text(column) )
        except ValueError:
            return self.text(column) > otherItem.text(column)
