# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module ApplicationReact

React module

""" 
from CmdBase import CmdBase, CmdMode
from Application import Application
from QApplicationWindow import QApplicationWindow
from View import View
from FileType import TXTColumnFile
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# IMPORT THEORIES
# Import theories specific to the Application e.g.:
# from TheoryLDPEBatch import TheoryTobitaBatch


class ApplicationReact(CmdBase):
    """[summary]
    
    [description]
    """
    name = 'React'
    description = 'React Application' #used in the command-line Reptate

    def __new__(cls, name='React', parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'React'})
            parent {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUIApplicationReact(name, parent) if (CmdBase.mode == CmdMode.GUI) else CLApplicationReact(name, parent)

class BaseApplicationReact:
    """[summary]
    
    [description]
    """
    def __init__(self, name='React', parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'React'})
            parent {[type]} -- [description] (default: {None})
        """
        from TheoryLDPEBatch import TheoryTobitaBatch

        super().__init__(name, parent)

        # VIEWS
        # set the views that can be selected in the view combobox
        # the order is defined by the index, index 0 is the defaut view
        self.views["w(M)"]=View(name="w(M)", description="Molecular weight distribution", x_label="M", y_label="w(M)", 
                                x_units="g/mol", y_units="-", log_x=True, log_y=False, view_proc=self.view_wM, n=1, 
                                snames=["w(M)"], index=0)
        self.views["g(M)"]=View(name="g(M)", description="g(M)", x_label="M", y_label="g", 
                                x_units="g/mol", y_units="-", log_x=True, log_y=False, view_proc=self.view_gM, n=1, 
                                snames=["g(M)"], index=1)
        self.views['br/1000C']=View(name="br/1000C", description="br/1000C(M)", x_label="M", y_label="br/1000C(M)", 
                                x_units="g/mol", y_units="-", log_x=True, log_y=False, view_proc=self.view_br_1000C, n=1, 
                                snames=["br/1000C(M)"], index=2)
                                
        # FILES
        # set the type of files that ApplicationReact can open
        ftype = TXTColumnFile(name='React files', extension='reac', description='Reatc file', col_names=['M', 'w(M)', 'g', 'br/1000C'], basic_file_parameters=[], col_units=['g/mol', '-', '-', '-'])
        self.filetypes[ftype.extension] = ftype #add each the file type to dictionary

        # THEORIES
        # add the theories related to ApplicationReact to the dictionary, e.g.:
        self.theories[TheoryTobitaBatch.thname] = TheoryTobitaBatch


        #SPECIFIC FIGURE
        # plt.clf()
        # self.ax = self.figure.add_subplot(2, 1, 1)
        # self.ax2 = self.figure.add_subplot(2, 2, 3)
        # self.ax3 = self.figure.add_subplot(2, 2, 4)

    def view_wM(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            dt {[type]} -- [description]
            file_parameters {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True

    def view_gM(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            dt {[type]} -- [description]
            file_parameters {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 2]
        return x, y, True

    def view_br_1000C(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            dt {[type]} -- [description]
            file_parameters {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 3]
        return x, y, True


class CLApplicationReact(BaseApplicationReact, Application):
    """[summary]
    
    [description]
    """
    def __init__(self, name='React', parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'React'})
            parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)
        #usually this class stays empty

class GUIApplicationReact(BaseApplicationReact, QApplicationWindow):
    """[summary]
    
    [description]
    """
    def __init__(self, name='React', parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'React'})
            parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)

        #add the GUI-specific objects here:
        self.populate_views() #populate the view ComboBox
        