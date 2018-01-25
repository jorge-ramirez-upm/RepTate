# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module TheoryDiscrMWD

Module that defines the theory to discretize a molecular weight distribution.

""" 
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
import numpy as np
from PyQt5.QtCore import Qt, QSize, QFile
from PyQt5.QtWidgets import QToolBar, QSpinBox, QFileDialog
from PyQt5.QtGui import QIcon
from DraggableArtists import DragType, DraggableBinSeries


class TheoryDiscrMWD(CmdBase):
    """Discretize a Molecular Weight Distribution
    
    [description]
    """
    thname = "MWDiscr"
    description = "Discretize a Molecular Weight Distribution"
    citations = ""

    def __new__(cls, name="MWDiscr", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"MWDiscr"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryDiscrMWD(name, parent_dataset, ax) if (CmdBase.mode==CmdMode.GUI) else CLTheoryDiscrMWD(name, parent_dataset, ax)

class BaseTheoryDiscrMWD:
    """[summary]
    
    [description]
    """
    single_file = True
    
    def __init__(self, name="ThDiscrMWD", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThDiscrMWD"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.discretise_mwd
        self.has_modes = False
        self.view_bins = True
        self.bins = None
        self.current_file = None

        self.parameters["Mn"] = Parameter(
            "Mn", 1000, "Number-average molecular mass", ParameterType.real, opt_type=OptType.const)
        self.parameters["Mw"] = Parameter(
            "Mw", 1000, "Weight-average molecular mass", ParameterType.real, opt_type=OptType.const)
        self.parameters["Mz"] = Parameter(
            "Mz", 1, "z-average molecular mass", ParameterType.real, opt_type=OptType.const)
        self.parameters["PDI"] = Parameter(
            "PDI", 1, "Polydispersity index", ParameterType.real, opt_type=OptType.const)
        
        mmin = self.parent_dataset.minpositivecol(0)
        mmax = self.parent_dataset.maxcol(0)
        nbin = int(np.round(3*np.log10(mmax/mmin))) # default: 3 bins per decade 
        self.parameters["logmmin"] = Parameter("logmmin", np.log10(mmin), "Log of minimum molecular mass", ParameterType.real, opt_type=OptType.const, display_flag=False)
        self.parameters["logmmax"] = Parameter("logmmax", np.log10(mmax), "Log of maximum molecular mass", ParameterType.real, opt_type=OptType.const, display_flag=False)
        self.parameters["nbin"] = Parameter(name="nbin", value=nbin, description="Number of molecular weight bins", type=ParameterType.integer, opt_type=OptType.const, display_flag=False)

        self.set_equally_spaced_bins()
        self.setup_graphic_bins()

    def set_equally_spaced_bins(self):
        """Find the first active file in the dataset and setup the bins"""
        for f in self.parent_dataset.files:
            if f.file_name_short not in self.parent_dataset.inactive_files:
                ft = f.data_table.data
                mmin = min(ft[:, 0])
                mmax = max(ft[:, 0])
                self.parameters["logmmin"].value = np.log10(mmin)
                self.parameters["logmmax"].value = np.log10(mmax)
                nbin = self.parameters["nbin"].value
                bins_edges = np.logspace(np.log10(mmin), np.log10(mmax), nbin + 1)
                for i in range(nbin + 1):
                    self.parameters["logM%02d"%i] = Parameter("logM%02d"%i, np.log10(bins_edges[i]), "Log of molecular mass", ParameterType.real, opt_type=OptType.const, display_flag=False)
                self.current_file = f
                break
   
    def set_param_value(self, name, new_value):
        """[summary]
        
        [description]
        
        Arguments:
            name {[type]} -- [description]
            value {[type]} -- [description]
        """
        if (name=="nbin"):
            nbinold = self.parameters["nbin"].value
        super().set_param_value(name, new_value)
        if (name=="nbin"):
            new_nbin = self.parameters["nbin"].value
            mminold = self.parameters["logmmin"].value
            mmaxold = self.parameters["logmmax"].value
            for i in range(nbinold + 1):
                del self.parameters["logM%02d"%i]
            mnew = np.logspace(mminold, mmaxold, new_nbin + 1)
            for i in range(new_nbin + 1):
                self.parameters["logM%02d"%i] = Parameter("logM%02d"%i, np.log10(mnew[i]),"Log molecular mass %d"%i, ParameterType.real, opt_type=OptType.const, display_flag=False)
            self.do_calculate("")

        if (name=='logmmin') or (name=='logmmax'): #make bins equally spaced again
            nbin = self.parameters["nbin"].value
            mmin = self.parameters["logmmin"].value
            mmax = self.parameters["logmmax"].value
            mnew = np.logspace(mmin, mmax, nbin + 1)
            for i in range(nbin + 1):
                self.parameters["logM%02d"%i] = Parameter("logM%02d"%i, np.log10(mnew[i]),"Log molecular mass %d"%i, ParameterType.real, opt_type=OptType.const, display_flag=False)
            self.do_calculate("")

    def setup_graphic_bins(self):
        """[summary]
        
        [description]
        """
        nbin = self.parameters["nbin"].value
        #marker at the Mw value of the bin
        self.Mw_bin = self.ax.plot(np.zeros(nbin), np.zeros(nbin))[0]
        self.Mw_bin.set_marker('|')
        self.Mw_bin.set_linestyle('')
        self.Mw_bin.set_visible(False)
        # self.Mw_bin.set_markerfacecolor('yellow')
        self.Mw_bin.set_markeredgecolor('black')
        self.Mw_bin.set_markeredgewidth(3)
        self.Mw_bin.set_markersize(14)
        self.Mw_bin.set_alpha(0.5)

        #setup the movable edge bin
        self.bins = np.logspace(self.parameters["logmmin"].value, self.parameters["logmmax"].value, nbin + 1)
        self.graphic_bins = self.ax.plot(self.bins, np.zeros(nbin + 1), picker=10)[0]
        self.graphic_bins.set_marker('d')
        self.graphic_bins.set_linestyle('')
        self.graphic_bins.set_visible(self.view_bins)
        self.graphic_bins.set_markerfacecolor('yellow')
        self.graphic_bins.set_markeredgecolor('black')
        self.graphic_bins.set_markeredgewidth(3)
        self.graphic_bins.set_markersize(11)
        self.graphic_bins.set_alpha(0.5)
        self.artist_bins = DraggableBinSeries(self.graphic_bins, DragType.horizontal, self.parent_dataset.parent_application.current_view.log_x, self.parent_dataset.parent_application.current_view.log_y, self.drag_bin)
        # self.plot_theory_stuff()


    def destructor(self):
        """Called when the theory tab is closed
        
        [description]
        """
        self.graphic_bins_visible(False)
        self.ax.lines.remove(self.graphic_bins)

    def show_theory_extras(self, show=False):
        """Called when the active theory is changed
        
        [description]
        """
        if CmdBase.mode == CmdMode.GUI:
            self.Qhide_theory_extras(show)
        self.graphic_bins_visible(show)

    def graphic_bins_visible(self, state):
        """[summary]
        
        [description]
        """
        self.view_bins = state
        self.graphic_bins.set_visible(state) #movable edge bins
        self.Mw_bin.set_visible(state) #Mw tick marks
        self.set_bar_plot(state) #bar plot

        if self.view_bins:
            self.artist_bins.connect()
        else:
            self.artist_bins.disconnect()
        # self.do_calculate("")
        self.parent_dataset.parent_application.update_plot()


    def drag_bin(self, newx, newy):
        """[summary]
        
        [description]
        
        Arguments:
            dx {[type]} -- [description]
            dy {[type]} -- [description]
        """
        nbin = self.parameters["nbin"].value
        newx = np.sort(newx)
        #check if point was dragged out of the limits
        # if yes put it 1% away from boundary
        if newx[0] < np.power(10, self.parameters["logmmin"].value):
            newx[1] *= 1.01
        if newx[-1] > np.power(10, self.parameters["logmmax"].value):
            newx[-2] /= 1.01
        for i in range(1, nbin): # exclude the min and max edges
            self.set_param_value("logM%02d"%i, np.log10(newx[i]))
        self.do_calculate("")
        self.update_parameter_table()

    def do_error(self, line):
        """[summary]
        
        [description]
        
        Arguments:
            line {[type]} -- [description]
        """
        pass

    def calculate_moments(self, f, line=""):
        """Calculate the moments Mn, Mw, and Mz of a molecular mass distribution
        
        [description]
        
        Arguments:
            f {[type]} -- [description]
        """
        n = f[:, 0].size
        Mw = 0
        tempMz = 0
        tempMn = 0
        temp_sum = 0

        for i in range(n):
            M = f[i, 0]
            w = f[i, 1]
            # M = np.power(10, (np.log10(f[i + 1, 0]) + np.log10(f[i, 0])) / 2 )
            Mw += w * M 
            tempMz += w * M * M # w*M^2
            tempMn += w / M # w/M
        Mn = 1/tempMn
        Mz = tempMz/Mw
        PDI = Mw/Mn

        if line=="input" and CmdBase.mode == CmdMode.GUI:
            file_table = self.parent_dataset.DataSettreeWidget.topLevelItem(0)
            self.parent_dataset.DataSettreeWidget.blockSignals(True)
            file_table.setText(1, "%0.3g"%(Mn/1000))
            file_table.setText(2, "%0.3g"%(Mw/1000))
            file_table.setText(3, "%0.3g"%PDI)
            self.parent_dataset.DataSettreeWidget.blockSignals(False)

        if line=="discretized":
            self.set_param_value("Mn", Mn/1000)
            self.set_param_value("Mw", Mw/1000)
            self.set_param_value("Mz", Mz/1000)
            self.set_param_value("PDI", PDI)

        if line == "":
            return Mn/1000, Mw/1000, PDI, Mz/Mw
        else:
            self.Qprint(
                "Characteristics of the %s MWD:\n"
                "%7s %7s %7s %7s\n"
                "\n%6.3gk %6.3gk %7.3g %7.3g\n"%(line,
                 "Mn", "Mw", "Mw/Mn", "Mz/Mw",
                  Mn/1000, Mw/1000, PDI, Mz/Mw) 
                )

    def discretise_mwd(self, f=None):
        """Discretize a molecular weight distribution
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        """

        # sort M, w with M increasing in ft
        f.data_table.data = f.data_table.data[np.argsort(f.data_table.data[:,0])]
        ft = f.data_table.data

        if f != self.current_file:
            self.set_equally_spaced_bins()

        #normalize area under the data points to compute the moments
        n = ft[:, 0].size
        temp_area = 0
        temp = np.zeros((n - 1, 2))
        for i in range(n - 1):
            dlogM = np.log10(ft[i + 1, 0]) - np.log10(ft[i, 0])
            mean_w = (ft[i, 1] + ft[i + 1, 1]) / 2
            temp_area += mean_w * dlogM
            temp[i, 0] = np.power(10, (np.log10(ft[i + 1, 0]) + np.log10(ft[i, 0])) / 2)
            temp[i, 1] = mean_w * dlogM
        temp[:, 1] /= temp_area
        self.calculate_moments(temp, "input")
        
        nbin = self.parameters["nbin"].value
        edge_bins = np.zeros(nbin + 1)
        for i in range(nbin + 1):
            edge_bins[i] = np.power(10, self.parameters["logM%02d"%i].value)
        
        #each M-bin is the Mw value of along the bin width
        out_mbins = np.zeros(nbin) #output M bins
        for i in range(nbin): 
            x = []
            y = []
            w_interp = np.interp([edge_bins[i], edge_bins[i + 1]], ft[:, 0], ft[:, 1], left=0, right=0) #interpolate out of range values to zero
            x.append(edge_bins[i])
            y.append(w_interp[0])
            for j in range(n):
                if edge_bins[i] <= ft[j, 0]  and ft[j, 0] < edge_bins[i + 1]:
                    x.append(ft[j, 0])
                    y.append(ft[j, 1])
            x.append(edge_bins[i + 1])
            y.append(w_interp[1])
            tempM = 0
            for j in range(len(x)):
                tempM += x[j] * y[j]
            out_mbins[i] = tempM / np.sum(y)

        #add area inder the curve to w_out and normalize by bin width
        w_out = np.zeros(nbin)
        for i in range(nbin): 
            x = []
            y = []
            w_interp = np.interp([edge_bins[i], edge_bins[i + 1]], ft[:, 0], ft[:, 1], left=0, right=0)
            x.append(edge_bins[i])
            y.append(w_interp[0])
            for j in range(n):
                if edge_bins[i] <= ft[j, 0]  and ft[j, 0] < edge_bins[i + 1]:
                    x.append(ft[j, 0])
                    y.append(ft[j, 1])
            x.append(edge_bins[i + 1])
            y.append(w_interp[1])
            w_out[i] = np.trapz(y, x=np.log10(x))/ (np.log10(edge_bins[i + 1]) - np.log10(edge_bins[i]) )

        # #copy weights and M into theory table
        tt = self.tables[f.file_name_short]
        tt.num_columns = 2
        tt.num_rows = len(w_out) 
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        # tt.data[:, 0] = out_mbins
        # tt.data[:, 1] = w_out

        #graphic stuff
        self.bin_height = w_out
        self.bin_edges = edge_bins
        
        #compute moments of discretized distribution
        self.saved_th = np.zeros((nbin, 2))
        self.saved_th[:, 0] = out_mbins
        for i in range(nbin):
            self.saved_th[i, 1] = (np.log10(edge_bins[i + 1]) - np.log10(edge_bins[i])) * w_out[i]
        self.saved_th[:, 1] /=  np.sum(self.saved_th[:, 1])
        self.calculate_moments(self.saved_th, "discretized")

    def plot_theory_stuff(self):
        """[summary]
        
        [description]
        """
        nbin = self.parameters["nbin"].value
        x = np.zeros(nbin + 1)
        y = np.zeros(nbin + 1)
        for i in range(nbin + 1):
            x[i]= self.parameters["logM%02d"%i].value
        self.graphic_bins.set_data(np.power(10, x), y)
        
        #set the bar plot
        self.set_bar_plot(True)

        #set the tick marks of for each bin Mw value
        self.Mw_bin.set_data(self.saved_th[:, 0], np.zeros(len(self.saved_th[:, 0])))
        self.Mw_bin.set_visible(True)

    def set_bar_plot(self, visible=True):
        """Hide/Show the bar plot"""
        nbin = self.parameters["nbin"].value
        try:
            self.bar_bins.remove() #remove existing bars, if any
        except:
            pass #no bar plot to remove
        if visible:
            edges = self.bin_edges[:-1] #remove last bin
            width = np.zeros(nbin)
            for i in range(nbin):
                width[i] = (self.bin_edges[i + 1] - self.bin_edges[i])
            self.bar_bins = self.ax.bar(edges, self.bin_height, width,  align='edge', color='grey', edgecolor='black', alpha=0.5)


class CLTheoryDiscrMWD(BaseTheoryDiscrMWD, Theory):
    """[summary]
    
    [description]
    """
    def __init__(self, name="MWDiscr", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"MWDiscr"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        
class GUITheoryDiscrMWD(BaseTheoryDiscrMWD, QTheory):
    """[summary]
    
    [description]
    """
    def __init__(self, name="MWDiscr", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"MWDiscr"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24,24))
        self.spinbox = QSpinBox()
        self.spinbox.setRange(3, 50) # min and max number of modes
        self.spinbox.setSuffix(" bins")
        self.spinbox.setValue(self.parameters["nbin"].value) #initial value
        tb.addWidget(self.spinbox)
        self.thToolsLayout.insertWidget(0, tb)
        #view bins button
        self.view_bins_button = tb.addAction(QIcon(':/Icon8/Images/new_icons/icons8-visible.png'), 'View modes')
        self.view_bins_button.setCheckable(True)
        self.view_bins_button.setChecked(True)
        self.thToolsLayout.insertWidget(0, tb)
        #save to file
        self.save_theory_results_button = tb.addAction(QIcon(':/Icon8/Images/new_icons/icons8-money-box.png'), 'Save Theory Results')
        self.thToolsLayout.insertWidget(0, tb)
   
        #connections signal and slots
        connection_id = self.view_bins_button.triggered.connect(self.handle_view_bins_button_triggered)
        connection_id = self.save_theory_results_button.triggered.connect(self.handle_save_theory_results)
        connection_id = self.spinbox.valueChanged.connect(self.handle_spinboxValueChanged)

        #disable useless buttons for this theory
        self.parent_dataset.actionMinimize_Error.setDisabled(True)
        self.parent_dataset.actionShow_Limits.setDisabled(True)
        self.parent_dataset.actionVertical_Limits.setDisabled(True)
        self.parent_dataset.actionHorizontal_Limits.setDisabled(True)

    def handle_spinboxValueChanged(self, value):
        """Handle a change of the parameter 'nbin'
        
        [description]
        
        Arguments:
            value {[type]} -- [description]
        """
        self.spinbox.setValue(value)
        self.set_param_value("nbin", value)
        self.update_parameter_table()
    
    def Qhide_theory_extras(self, state):
        """Uncheck the view_bins_button button. Called when curent theory is changed
        
        [description]
        """
        self.view_bins_button.setChecked(state)

    def handle_view_bins_button_triggered(self, checked):
        """[summary]
        
        [description]
        """
        self.graphic_bins_visible(checked)
        self.set_bar_plot(True) #leave the bar plot on
        self.parent_dataset.parent_application.update_plot()

    def handle_save_theory_results(self):
        """
        Launch a dialog to select a filename when to save the discretized distribution.
        """
        stars = '*************************\n'
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_start = "data/MWD/discretized.dat"
        dilogue_name = "Save"
        ext_filter = "Data Files (*.dat)"
        out_file = QFileDialog.getSaveFileName(self, dilogue_name, dir_start, options=options)
        if out_file[0] == "":
            return
        fout = open(out_file[0], 'w')

        # output polymers
        Mn, Mw, PDI, Mz_Mw = self.calculate_moments(self.saved_th, "")
        fout.write("Mn=%.3g;Mw=%.3g;PDI=%.3g;Mz/Mw=%.3g\n"%(Mn, Mw, PDI, Mz_Mw))
        fout.write("%-10s %12s\n"%("M", "phi(M)"))
        k = 0
        for i in range(len(self.saved_th[:, 0])):
            fout.write("%-10.3e %12.6e\n"%(self.saved_th[i, 0], self.saved_th[i, 1]))
            k += 1
        message = stars
        message += "Saved %d bins to \"%s\""%(k, out_file[0])

        self.Qprint(message)
