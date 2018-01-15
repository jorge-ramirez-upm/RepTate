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
from scipy import interp
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


        self.parameters["Mn"] = Parameter(
            "Mn", 1000, "Number-average molecular mass", ParameterType.real, opt_type=OptType.const)
        self.parameters["Mw"] = Parameter(
            "Mw", 1000, "Weight-average molecular mass", ParameterType.real, opt_type=OptType.const)
        self.parameters["Mz"] = Parameter(
            "Mz", 1, "z-average molecular mass", ParameterType.real, opt_type=OptType.const)
        self.parameters["PDI"] = Parameter(
            "PDI", 1, "Polydispersity index", ParameterType.real, opt_type=OptType.const)
        
        mmin = 0.1*self.parent_dataset.minpositivecol(0)
        mmax = 10*self.parent_dataset.maxcol(0)
        nbin = int(np.round(3*np.log10(mmax/mmin)))
        self.parameters["logmmin"] = Parameter("logmmin", np.log10(mmin), "Log of minimum molecular mass", ParameterType.real, opt_type=OptType.const, display_flag=False)
        self.parameters["logmmax"] = Parameter("logmmax", np.log10(mmax), "Log of maximum molecular mass", ParameterType.real, opt_type=OptType.const, display_flag=False)
        self.parameters["nbin"] = Parameter(name="nbin", value=nbin, description="Number of Maxwell modes", type=ParameterType.integer, opt_type=OptType.const, display_flag=False)
        # Interpolate modes from data
        bins = np.logspace(np.log10(mmin), np.log10(mmax), nbin)
        for f in self.parent_dataset.files:
            if f not in self.parent_dataset.inactive_files:
                break
        weight = np.abs(np.interp(bins, f.data_table.data[:,0], f.data_table.data[:,1]))
        for i in range(self.parameters["nbin"].value):
            self.parameters["logM%02d"%i] = Parameter("logM%02d"%i,np.log10(bins[i]),"Log molecular mass %d"%i, ParameterType.real, opt_type=OptType.const)
        
        self.setup_graphic_bins()

    def setup_graphic_bins(self):
        """[summary]
        
        [description]
        """
        nbin = self.parameters["nbin"].value
        self.zeros = np.zeros(nbin)
        self.bins = np.logspace(self.parameters["logmmin"].value, self.parameters["logmmax"].value, nbin)


        self.graphic_bins = self.ax.plot(self.bins, self.zeros)[0]
        self.graphic_bins.set_marker('D')
        self.graphic_bins.set_linestyle('')
        self.graphic_bins.set_visible(self.view_bins)
        self.graphic_bins.set_markerfacecolor('yellow')
        self.graphic_bins.set_markeredgecolor('black')
        self.graphic_bins.set_markeredgewidth(3)
        self.graphic_bins.set_markersize(8)
        self.graphic_bins.set_alpha(0.5)
        self.artist_bins = DraggableBinSeries(self.graphic_bins, DragType.horizontal, self.parent_dataset.parent_application.current_view.log_x, self.parent_dataset.parent_application.current_view.log_y, self.drag_bin)
        # self.plot_theory_stuff()

    def destructor(self):
        """Called when the theory tab is closed
        
        [description]
        """
        self.graphic_bins_visible(False)
        self.ax.lines.remove(self.graphic_bins) 

    def hide_theory_extras(self):
        """Called when the active theory is changed
        
        [description]
        """
        if CmdBase.mode == CmdMode.GUI:
            self.Qhide_theory_extras()
        self.graphic_bins_visible(False)

    def graphic_bins_visible(self, state):
        """[summary]
        
        [description]
        """
        self.view_bins = state
        self.graphic_bins.set_visible(state)
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
        for i in range(1, nbin - 1):
            self.set_param_value("logM%02d"%i, np.log10(newx[i]))
        self.set_param_value("logmmin", np.log10(newx[0]))
        self.set_param_value("logmmax", np.log10(newx[nbin - 1]))
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
        for i in range(n):
            Mw += f[i, 1]*f[i, 0] # w*M
            tempMz += f[i, 1]*f[i, 0]*f[i, 0] # w*M^2
            tempMn += f[i, 1]/f[i, 0] # w/M
        Mn = 1/tempMn
        Mz = tempMz/Mw
        PDI = Mw/Mn

        if line=="input":
            file_table = self.parent_dataset.DataSettreeWidget.topLevelItem(0)
            self.parent_dataset.DataSettreeWidget.blockSignals(True)
            file_table.setText(1, "%0.3g"%Mn)
            file_table.setText(2, "%0.3g"%Mw)
            file_table.setText(3, "%0.3g"%PDI)
            self.parent_dataset.DataSettreeWidget.blockSignals(False)

        if line=="discretized":
            self.set_param_value("Mn", Mn)
            self.set_param_value("Mw", Mw)
            self.set_param_value("Mz", Mz)
            self.set_param_value("PDI", PDI)

        if line == "":
            return Mn/1000, Mw/1000, PDI, Mz/Mw
        else:
            self.Qprint(
                "Characteristics of the %s MWD:\n"
                "Mn=%0.3g kg/mol, Mw=%0.3g kg/mol, Mw/Mn=%0.3g, Mz/Mw=%0.3g\n"
                %(line, Mn/1000, Mw/1000, PDI, Mz/Mw)
                )

    def add_to_bin(self, phi, edge_bins, wi, k, data_up, data_down):
        kk = k
        mup = data_up
        while True:
            mdown = max (edge_bins[kk - 1], data_down)
            phi[kk] += wi * (mup - mdown)
            mup = mdown
            kk = kk - 1
            if mdown == data_down:
                break
        
    def discretise_mwd(self, f=None):
        """Discretize a molecular weight distribution
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        """

        # sort M, w(M) with M increasing in ft
        ft = f.data_table.data[np.argsort(f.data_table.data[:,0])]
        n = ft[:, 0].size
        #normalize the weights w(M)
        ft[:,1] = ft[:,1]/np.sum(ft[:,1])
        self.calculate_moments(ft, "input")
        
        nbin = self.parameters["nbin"].value
        logbins = np.zeros(nbin)
        for i in range(nbin):
            logbins[i] = self.parameters["logM%02d"%i].value
        
        #create the edges of the bins
        edge_bins = np.zeros(nbin - 1)
        for k in range(nbin - 1):
            edge_bins[k] = (logbins[k + 1] + logbins[k]) / 2

        #create mid data point values
        mid_ft = np.zeros(n - 1)
        for j in range(n - 1):
            mid_ft[j] = (np.log10(ft[j + 1, 0]) + np.log10(ft[j, 0]))/2 #mid-values of logM
        
        low = mid_ft[0] - (mid_ft[1] - mid_ft[0])
        high = mid_ft[n - 2] + (mid_ft[n - 2] - mid_ft[n - 3])
        if low < edge_bins[0] or high > edge_bins[nbin - 2]: #must increase the number of bins
            self.handle_spinboxValueChanged(nbin + 1)
            self.discretise_mwd(f)
            return

        phi = np.zeros(nbin)
        for i in range(n - 1): # [1..n-2]
            #loop over the data points
            #add w[i]*(mid_ft[i]-mid_ft[i-1]) to bin[i] until mid_ft[i] > edge_bin[i]
            #interpolate: add the area belonging to bin[i]
            # (edge_bin[i] - mid_ft[i-1])*w[i] to bin[i]
            # (mid_ft[i-1] - edge_bin[i])*w[i] or less to bin[i+1]
            k = 0
            wi = ft[i, 1]
            while edge_bins[k] < mid_ft[i]:
                k += 1
            if i == 0: #case of the first bin
                low = mid_ft[0] - (mid_ft[1] - mid_ft[0])
                if low < 0:
                    low = mid_ft[0]/2
                self.add_to_bin(phi, edge_bins, wi, k, mid_ft[0], low)
                continue
            try:
                full_bin = mid_ft[i - 1] > edge_bins[k - 1]
            except:
                full_bin = False
            if full_bin:
                phi[k] += wi * (mid_ft[i] - mid_ft[i - 1])
            else:
                self.add_to_bin(phi, edge_bins, wi, k, mid_ft[i], mid_ft[i-1])

        #treat the last data point
        k = 0
        wi = ft[n - 1, 1]
        high = mid_ft[n - 2] + (mid_ft[n - 2] - mid_ft[n - 3])
        while edge_bins[k] < high:
            k += 1
        self.add_to_bin(phi, edge_bins, wi, k, high, mid_ft[n - 2])

        phi = phi/np.sum(phi) #normalize

        #copy weights and M into theory table
        logbins, phi = self.clean_zeros(logbins, phi, nbin) #remove the weight = 0
        tt = self.tables[f.file_name_short]
        tt.num_columns = 2
        tt.num_rows = len(phi) 
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        # weight = np.zeros(nbin-1)
        # mass = np.zeros(nbin-1)
        # for i in range(nbin-1):
        #     weight[i] = ((phi[i + 1] + phi[i]) / 2) / (logbins[i+1] - logbins[i])
        #     mass[i] = np.power(10, (logbins[i] + logbins[i + 1])/2 )
        # tt.data[:, 1] = phi/np.sum(phi)
        # weight = weight/np.sum(weight)
        # print (weight)
        # print(mass)
        # tt.data[:, 0] = mass
        # tt.data[:, 1] = weight
        tt.data[:, 0] = np.power(10, logbins)
        tt.data[:, 1] = phi/np.sum(phi)

        size = len(tt.data[:, 1])
        self.saved_th = np.zeros((size, 2))
        self.saved_th[:, 0] = np.power(10, logbins)
        self.saved_th[:, 1] = phi/np.sum(phi)
        self.calculate_moments(tt.data, "discretized")

    def plot_theory_stuff(self):
        """[summary]
        
        [description]
        """
        nbin = self.parameters["nbin"].value
        x = np.zeros(nbin)
        y = np.zeros(nbin)
        for i in range(nbin):
            x[i]= self.parameters["logM%02d"%i].value

        self.graphic_bins.set_data(np.power(10, x), y)

    def clean_zeros(self, bins, phi, nbin):
        """[summary]
        
        [description]
        
        Arguments:
            bins {[type]} -- [description]
            phi {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        zeros = []
        for i in range(nbin):
            if phi[i] == 0:
                zeros.append(i)
        return np.delete(bins, zeros), np.delete(phi, zeros)

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
        nbinold = self.parameters["nbin"].value
        mminold=self.parameters["logmmin"].value
        mmaxold=self.parameters["logmmax"].value
        for i in range(nbinold):
            del self.parameters["logM%02d"%i]
        self.set_param_value("nbin", value)
        mnew = np.logspace(mminold, mmaxold, value)
        for i in range(value):
            self.parameters["logM%02d"%i] = Parameter("logM%02d"%i, np.log10(mnew[i]),"Log molecular mass %d"%i, ParameterType.real, opt_type=OptType.const)
        
        self.do_calculate("")
        self.update_parameter_table()
    
    def Qhide_theory_extras(self):
        """Uncheck the view_bins_button button. Called when curent theory is changed
        
        [description]
        """
        self.view_bins_button.setChecked(False)

    def handle_view_bins_button_triggered(self, checked):
        """[summary]
        
        [description]
        """
        self.graphic_bins_visible(checked)

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
        fout.write("%10s %12s\n"%("M", "phi(M)"))
        k = 0
        for i in range(len(self.saved_th[:, 0])):
            fout.write("%10.3e %12.6e\n"%(self.saved_th[i, 0], self.saved_th[i, 1]))
            k += 1
        message = stars
        message += "Saved %d bins to \"%s\""%(k, out_file[0])

        self.Qprint(message)
