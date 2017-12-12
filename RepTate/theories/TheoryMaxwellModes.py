# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module TheoryMaxwellModes

Module that defines theories related to Maxwell modes, in the frequency and time domains.

""" 
import numpy as np
from CmdBase import CmdBase, CmdMode
from DataTable import DataTable
from Parameter import Parameter, ParameterType, ShiftType
from Theory import Theory
from QTheory import QTheory
from PyQt5.QtWidgets import QWidget, QToolBar, QComboBox, QSpinBox, QAction, QStyle
from PyQt5.QtCore import QSize
from DraggableArtists import DragType, DraggableModesSeries

class TheoryMaxwellModesFrequency(CmdBase):
    """Fit Maxwell modes to a frequency dependent relaxation function
    
    [description]
    """
    thname="MaxwellModesFrequency"
    description="Fit Maxwell modes to frequency dependent function"

    def __new__(cls, name="ThMaxwellFrequency", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryMaxwellModesFrequency(name, parent_dataset, ax) if (CmdBase.mode==CmdMode.GUI) else CLTheoryMaxwellModesFrequency(name, parent_dataset, ax)
 
class BaseTheoryMaxwellModesFrequency:
    """[summary]
    
    [description]
    """
    single_file = True 

    def __init__(self, name="ThMaxwellFrequency", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.MaxwellModesFrequency
        self.has_modes = True
        self.MAX_MODES = 40
        self.view_modes = True
        wmin = self.parent_dataset.minpositivecol(0)
        wmax = self.parent_dataset.maxcol(0)
        nmodes=int(np.round(np.log10(wmax/wmin)))
        print(wmin, wmax, nmodes)
        self.parameters["logwmin"]=Parameter("logwmin", np.log10(wmin), "Log of frequency range minimum", ParameterType.real, True)
        self.parameters["logwmax"]=Parameter("logwmax", np.log10(wmax), "Log of frequency range maximum", ParameterType.real, True)
        self.parameters["nmodes"]=Parameter(name="nmodes", value=nmodes, description="Number of Maxwell modes", type=ParameterType.integer, min_flag=False, display_flag=False)
        # Interpolate modes from data
        w = np.logspace(np.log10(wmin), np.log10(wmax), nmodes)
        G = np.abs(np.interp(w, self.parent_dataset.files[0].data_table.data[:,0], self.parent_dataset.files[0].data_table.data[:,1]))
        for i in range(self.parameters["nmodes"].value):
            self.parameters["logG%02d"%i]=Parameter("logG%02d"%i,np.log10(G[i]),"Log of Mode %d amplitude"%i, ParameterType.real, True)
        
        # GRAPHIC MODES
        self.graphicmodes = []
        self.artistmodes = []
        self.setup_graphic_modes()

    def drag_mode(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            dx {[type]} -- [description]
            dy {[type]} -- [description]
        """
        nmodes=self.parameters["nmodes"].value
        self.set_param_value("logwmin", dx[0])
        self.set_param_value("logwmax", dx[nmodes-1])
        for i in range(nmodes):
            self.set_param_value("logG%02d"%i, dy[i])
        self.do_calculate("")
        self.update_parameter_table()

    def update_modes(self):
        """[summary]
        
        [description]
        """
        pass        
        
    def setup_graphic_modes(self):
        """[summary]
        
        [description]
        """
        nmodes=self.parameters["nmodes"].value
        w=np.logspace(self.parameters["logwmin"].value, self.parameters["logwmax"].value, nmodes)
        G=np.zeros(nmodes)
        for i in range(nmodes):
            G[i]=np.power(10, self.parameters["logG%02d"%i].value)

        self.graphicmodes = self.ax.plot(w, G)[0]
        self.graphicmodes.set_marker('D')
        self.graphicmodes.set_linestyle('')
        self.graphicmodes.set_visible(self.view_modes)
        self.graphicmodes.set_markerfacecolor('yellow')
        self.graphicmodes.set_markeredgecolor('black')
        self.graphicmodes.set_markeredgewidth(3)
        self.graphicmodes.set_markersize(8)
        self.graphicmodes.set_alpha(0.5)
        self.artistmodes = DraggableModesSeries(self.graphicmodes, DragType.special, self.parent_dataset.parent_application.current_view.log_x, self.parent_dataset.parent_application.current_view.log_y, self.drag_mode)
        self.plot_theory_stuff()


    def get_modes(self):
        """[summary]
        
        [description]
        
        Returns:
            [type] -- [description]
        """
        nmodes=self.parameters["nmodes"].value
        freq=np.logspace(self.parameters["logwmin"].value, self.parameters["logwmax"].value, nmodes)
        tau=1.0/freq
        G=np.zeros(nmodes)
        for i in range(nmodes):
            G[i]=np.power(10, self.parameters["logG%02d"%i].value)
        return tau, G

    def set_modes(self, tau, G):
        """[summary]
        
        [description]
        
        Arguments:
            tau {[type]} -- [description]
            G {[type]} -- [description]
        """
        print("set_modes not allowed in this theory (%s)"%self.name)

    def MaxwellModesFrequency(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        """
        ft=f.data_table
        tt=self.tables[f.file_name_short]
        tt.num_columns=ft.num_columns
        tt.num_rows=ft.num_rows
        tt.data=np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:,0]=ft.data[:,0]

        nmodes=self.parameters["nmodes"].value
        freq=np.logspace(self.parameters["logwmin"].value, self.parameters["logwmax"].value, nmodes)
        tau=1.0/freq

        for i in range(nmodes):
            wT=tt.data[:,0]*tau[i]
            wTsq=wT**2
            G=np.power(10, self.parameters["logG%02d"%i].value)
            tt.data[:,1]+=G*wTsq/(1+wTsq)
            tt.data[:,2]+=G*wT/(1+wTsq)

    def plot_theory_stuff(self):
        """[summary]
        
        [description]
        """
        if not self.view_modes:
            return
        data_table_tmp = DataTable(self.ax)
        data_table_tmp.num_columns = 3
        nmodes = self.parameters["nmodes"].value
        data_table_tmp.num_rows = nmodes
        data_table_tmp.data=np.zeros((nmodes, 3))
        freq=np.logspace(self.parameters["logwmin"].value, self.parameters["logwmax"].value, nmodes)
        data_table_tmp.data[:,0] = freq
        for i in range(nmodes):
            data_table_tmp.data[i,1] = data_table_tmp.data[i,2] = np.power(10, self.parameters["logG%02d"%i].value)
        view = self.parent_dataset.parent_application.current_view
        try:
            x, y, success = view.view_proc(data_table_tmp, None)
        except TypeError as e:
            print(e)
            return
        self.graphicmodes.set_data(x, y)

class CLTheoryMaxwellModesFrequency(BaseTheoryMaxwellModesFrequency, Theory):
    """[summary]
    
    [description]
    """
    def __init__(self, name="ThMaxwellFrequency", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        
class GUITheoryMaxwellModesFrequency(BaseTheoryMaxwellModesFrequency, QTheory):
    """[summary]
    
    [description]
    """
    def __init__(self, name="ThMaxwellFrequency", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        
        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24,24))
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, self.MAX_MODES) # min and max number of modes
        self.spinbox.setSuffix(" modes")
        self.spinbox.setValue(self.parameters["nmodes"].value) #initial value
        tb.addWidget(self.spinbox)
        self.modesaction = tb.addAction(self.style().standardIcon(getattr(QStyle, 'SP_DialogYesButton')), 'View modes')
        self.modesaction.setCheckable(True)
        self.modesaction.setChecked(True)
        self.thToolsLayout.insertWidget(0, tb)
        connection_id = self.spinbox.valueChanged.connect(self.handle_spinboxValueChanged)
        connection_id = self.modesaction.triggered.connect(self.modesaction_change)
        
    def modesaction_change(self):
        """[summary]
        
        [description]
        """
        self.view_modes = self.modesaction.isChecked()
        self.graphicmodes.set_visible(self.view_modes)
        self.do_calculate("")

    def handle_spinboxValueChanged(self, value):
        """[summary]
        
        [description]
        
        Arguments:
            value {[type]} -- [description]
        """
        """Handle a change of the parameter 'nmode'"""
        nmodesold=self.parameters["nmodes"].value
        wminold=self.parameters["logwmin"].value
        wmaxold=self.parameters["logwmax"].value
        wold=np.logspace(wminold, wmaxold, nmodesold)
        Gold=np.zeros(nmodesold)
        for i in range(nmodesold):
            Gold[i]=self.parameters["logG%02d"%i].value
            del self.parameters["logG%02d"%i]

        nmodesnew=value
        self.set_param_value("nmodes", nmodesnew)
        wnew=np.logspace(wminold, wmaxold, nmodesnew)
        
        Gnew = np.interp(wnew, wold, Gold)

        for i in range(nmodesnew):
            self.parameters["logG%02d"%i]=Parameter("logG%02d"%i,Gnew[i],"Log of Mode %d amplitude"%i, ParameterType.real, True)
        
        self.do_calculate("")
        self.update_parameter_table()


##################################################################################
#   MAXWELL MODES TIME
##################################################################################

class TheoryMaxwellModesTime(CmdBase):
    """Fit Maxwell modes to a time depenendent relaxation function
    
    [description]
    """
    thname="MaxwellModesTime"
    description="Fit Maxwell modes to time dependent function"
    citations=""
    def __new__(cls, name="ThMaxwellTime", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellTime"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryMaxwellModesTime(name, parent_dataset, ax) if (CmdBase.mode==CmdMode.GUI) else CLTheoryMaxwellModesTime(name, parent_dataset, ax)
      
class BaseTheoryMaxwellModesTime:
    """[summary]
    
    [description]
    """
    single_file = True 

    def __init__(self, name="ThMaxwellTime", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellTime"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.MaxwellModesTime
        self.has_modes = True
        self.MAX_MODES = 40
        self.view_modes = True
        tmin = self.parent_dataset.minpositivecol(0)
        tmax = self.parent_dataset.maxcol(0)
        nmodes=int(np.round(np.log10(tmax/tmin)))
        self.parameters["logtmin"]=Parameter("logtmin", np.log10(tmin), "Log of time range minimum", ParameterType.real, True)
        self.parameters["logtmax"]=Parameter("logtmax", np.log10(tmax), "Log of time range maximum", ParameterType.real, True)
        self.parameters["nmodes"]=Parameter(name="nmodes", value=nmodes, description="Number of Maxwell modes", type=ParameterType.integer, min_flag=False, display_flag=False)
        # Interpolate modes from data
        tau = np.logspace(np.log10(tmin), np.log10(tmax), nmodes)
        G = np.abs(np.interp(tau, self.parent_dataset.files[0].data_table.data[:,0], self.parent_dataset.files[0].data_table.data[:,1]))
        for i in range(self.parameters["nmodes"].value):
            self.parameters["logG%02d"%i]=Parameter("logG%02d"%i,np.log10(G[i]),"Log of Mode %d amplitude"%i, ParameterType.real, True)

        # GRAPHIC MODES
        self.graphicmodes = None
        self.artistmodes = None
        self.setup_graphic_modes()

    def drag_mode(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            dx {[type]} -- [description]
            dy {[type]} -- [description]
        """
        nmodes=self.parameters["nmodes"].value
        self.set_param_value("logtmin", dx[0])
        self.set_param_value("logtmax", dx[nmodes-1])
        for i in range(nmodes):
            self.set_param_value("logG%02d"%i, dy[i])
        self.do_calculate("")
        self.update_parameter_table()

    def update_modes(self):
        """[summary]
        
        [description]
        """
        pass

    def setup_graphic_modes(self):
        """[summary]
        
        [description]
        """
        nmodes=self.parameters["nmodes"].value
        tau=np.logspace(self.parameters["logtmin"].value, self.parameters["logtmax"].value, nmodes)
        G=np.zeros(nmodes)
        for i in range(nmodes):
            G[i]=np.power(10, self.parameters["logG%02d"%i].value)

        self.graphicmodes = self.ax.plot(tau, G)[0]
        self.graphicmodes.set_marker('D')
        self.graphicmodes.set_linestyle('')
        self.graphicmodes.set_visible(self.view_modes)
        self.graphicmodes.set_markerfacecolor('yellow')
        self.graphicmodes.set_markeredgecolor('black')
        self.graphicmodes.set_markeredgewidth(3)
        self.graphicmodes.set_markersize(8)
        self.graphicmodes.set_alpha(0.5)
        self.artistmodes = DraggableModesSeries(self.graphicmodes, DragType.special, self.parent_dataset.parent_application.current_view.log_x, self.parent_dataset.parent_application.current_view.log_y, self.drag_mode)
        self.plot_theory_stuff()


    def get_modes(self):
        """[summary]
        
        [description]
        
        Returns:
            [type] -- [description]
        """
        nmodes=self.parameters["nmodes"].value
        tau=np.logspace(self.parameters["logtmin"].value, self.parameters["logtmax"].value, nmodes)
        G=np.zeros(nmodes)
        for i in range(nmodes):
            G[i]=np.power(10, self.parameters["logG%02d"%i].value)
        return tau, G

    def set_modes(self, tau, G):
        """[summary]
        
        [description]
        
        Arguments:
            tau {[type]} -- [description]
            G {[type]} -- [description]
        """
        print("set_modes not allowed in this theory (%s)"%self.name)

    def MaxwellModesTime(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        """
        ft=f.data_table
        tt=self.tables[f.file_name_short]
        tt.num_columns=ft.num_columns
        tt.num_rows=ft.num_rows
        tt.data=np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:,0]=ft.data[:,0]

        nmodes=self.parameters["nmodes"].value
        tau=np.logspace(self.parameters["logtmin"].value, self.parameters["logtmax"].value, nmodes)

        for i in range(nmodes):
            expT_tau=np.exp(-tt.data[:,0]/tau[i])
            G=np.power(10, self.parameters["logG%02d"%i].value)
            tt.data[:,1]+=G*expT_tau

    def plot_theory_stuff(self):
        """[summary]
        
        [description]
        """
        if not self.view_modes:
            return
        data_table_tmp = DataTable(self.ax)
        data_table_tmp.num_columns = 2
        nmodes = self.parameters["nmodes"].value
        data_table_tmp.num_rows = nmodes
        data_table_tmp.data=np.zeros((nmodes, 2))
        tau=np.logspace(self.parameters["logtmin"].value, self.parameters["logtmax"].value, nmodes)
        data_table_tmp.data[:,0] = tau
        for i in range(nmodes):
            data_table_tmp.data[i,1] = np.power(10, self.parameters["logG%02d"%i].value)
        view = self.parent_dataset.parent_application.current_view
        try:
            x, y, success = view.view_proc(data_table_tmp, None)
        except TypeError as e:
            print(e)
            return
        self.graphicmodes.set_data(x, y)


class CLTheoryMaxwellModesTime(BaseTheoryMaxwellModesTime, Theory):
    """[summary]
    
    [description]
    """
    def __init__(self, name="ThMaxwellTime", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellTime"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        
class GUITheoryMaxwellModesTime(BaseTheoryMaxwellModesTime, QTheory):
    """[summary]
    
    [description]
    """
    def __init__(self, name="ThMaxwellTime", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellTime"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24,24))
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, self.MAX_MODES) # min and max number of modes
        self.spinbox.setSuffix(" modes")
        self.spinbox.setValue(self.parameters["nmodes"].value) #initial value
        tb.addWidget(self.spinbox)
        self.modesaction = tb.addAction(self.style().standardIcon(getattr(QStyle, 'SP_DialogYesButton')), 'View modes')
        self.modesaction.setCheckable(True)
        self.modesaction.setChecked(True)
        self.thToolsLayout.insertWidget(0, tb)
        connection_id = self.spinbox.valueChanged.connect(self.handle_spinboxValueChanged)
        connection_id = self.modesaction.triggered.connect(self.modesaction_change)
        

    def modesaction_change(self):
        """[summary]
        
        [description]
        """
        self.view_modes = self.modesaction.isChecked()
        self.graphicmodes.set_visible(self.view_modes)
        self.do_calculate("")

    def handle_spinboxValueChanged(self, value):
        """[summary]
        
        [description]
        
        Arguments:
            value {[type]} -- [description]
        """
        """Handle a change of the parameter 'nmode'"""
        nmodesold=self.parameters["nmodes"].value
        tminold=self.parameters["logtmin"].value
        tmaxold=self.parameters["logtmax"].value
        tauold=np.logspace(tminold, tmaxold, nmodesold)
        Gold=np.zeros(nmodesold)
        for i in range(nmodesold):
            Gold[i]=self.parameters["logG%02d"%i].value
            del self.parameters["logG%02d"%i]

        nmodesnew=value
        self.set_param_value("nmodes", nmodesnew)
        taunew=np.logspace(tminold, tmaxold, nmodesnew)
        
        Gnew = np.interp(taunew, tauold, Gold)

        for i in range(nmodesnew):
            self.parameters["logG%02d"%i]=Parameter("logG%02d"%i,Gnew[i],"Log of Mode %d amplitude"%i, ParameterType.real, True)
        
        self.do_calculate("")
        self.update_parameter_table()
