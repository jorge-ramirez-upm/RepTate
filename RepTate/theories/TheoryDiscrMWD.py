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
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QToolBar, QSpinBox

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
        self.parameters["bpd"] = Parameter(
            "bpd", 10, "Number modes per decade", ParameterType.integer, opt_type=OptType.const)
        self.parameters["Mn"] = Parameter(
            "Mn", 1000, "Number-average molecular mass", ParameterType.real, opt_type=OptType.const)
        self.parameters["Mw"] = Parameter(
            "Mw", 1000, "Weight-average molecular mass", ParameterType.real, opt_type=OptType.const)
        self.parameters["Mz"] = Parameter(
            "Mz", 1, "z-average molecular mass", ParameterType.real, opt_type=OptType.const)
        self.parameters["PDI"] = Parameter(
            "PDI", 1, "Polydispersity index", ParameterType.real, opt_type=OptType.const)

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

        #molar mass min and max 
        mmin = 0.1*np.min(ft[:, 0])
        mmax = 10*np.max(ft[:, 0])

        #bins equally spaced on logarithmic scale
        nbin = int(np.ceil((np.log10(mmax/mmin))*self.parameters["bpd"].value))
        bins = np.zeros(nbin)
        for k in range(nbin):  
            bins[k] = mmin*np.power(10, k/nbin * np.log10(mmax/mmin))

        #create the edges of the bins
        edge_bins = np.zeros(nbin - 1)
        for k in range(nbin - 1):
            edge_bins[k] = (np.log10(bins[k + 1]) + np.log10(bins[k])) / 2
        
        #create mid data point values
        mid_ft = np.zeros(n - 1)
        for j in range(n - 1):
            mid_ft[j] = (np.log10(ft[j + 1, 0]) + np.log10(ft[j, 0]))/2 #mid-values of logM


        phi = np.zeros(nbin)
        for i in range(n - 1): # [1..n-2]
            #loop over the data points
            #add w[i]*(mid_ft[i]-mid_ft[i-1]) to bin[i] until mid_ft[i] > edge_bin[i]
            #interpolate: add the area belonging to bin[i]
            # (edge_bin[i] - mid_ft[i-1])*w[i] to bin[i]
            # (mid_ft[i-1] - edge_bin[i])*w[i] to bin[i+1]

            k = 0
            wi = ft[i, 1]
            while edge_bins[k] < mid_ft[i]:
                k += 1
            if i == 0:
                low = mid_ft[0] - (mid_ft[1] - mid_ft[0])
                if low < 0:
                    low = mid_ft[0]/2
                self.add_to_bin(phi, edge_bins, wi, k, mid_ft[0], low)
                # phi[k] += wi * (mid_ft[1] - mid_ft[0]) #bin width taken as (log) distance to next point
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


                # kk = k
                # mup = mid_ft[i]
                # while True:
                #     mdown = max (edge_bins[kk - 1], mid_ft[i - 1])
                #     phi[kk] += wi * (mup - mdown)
                #     mup = mdown
                #     kk = kk - 1
                #     if mdown == mid_ft[i - 1]:
                #         break



                # phi[k] += wi * (mid_ft[i] - edge_bins[k - 1])
                # phi[k - 1] += wi * (edge_bins[k - 1] - edge_bins[k - 2])
                # phi[k - 2] += wi * (edge_bins[k - 2] - mid_ft[i - 1])

        # phi = phi/np.sum(phi)
        
        #copy weights and M into theory table
        # bins, phi = self.clean_zeros(bins, phi)
        tt = self.tables[f.file_name_short]
        tt.num_columns = 2
        tt.num_rows = len(phi)
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = bins
        tt.data[:, 1] = phi/np.sum(phi)
        print (np.sum( tt.data[:, 1]))
        self.calculate_moments(tt.data, "discretized")


        # #find into which bin the data point belong
        # inds = np.digitize(mid_ft, edge_bins, right=False) 
        # #returns indices of the bins to which each value in input array belongs
        # #edge_bins[inds[j]-1] <= mid_ft[j] < edge_bins[inds[j]]

        # nk = np.zeros(nbin)
        # for j in range(n - 1):
        #     k = inds[j]
        #     dlogMj = np.log10(ft[j + 1, 0]) - np.log10(ft[j, 0])
        #     wj = (ft[j + 1, 1] + ft[j, 1]) / 2
        #     dlogMk = (np.log10(bins[k + 1])  - np.log10(bins[k - 1])) / 2
        #     phi[k] +=  wj*dlogMj/dlogMk #weight x width / bin_width
        #     nk[k] += 1

        # sum_nk = np.sum(nk)        
        # for k in range(nbin):
        #     if nk[k]>0: 
        #         phi[k] = phi[k]/nk[k] * sum_nk/nbin
                


    def clean_zeros(self, bins, phi):
        """[summary]
        
        [description]
        
        Arguments:
            bins {[type]} -- [description]
            phi {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        a=0
        for i in range(len(phi)):
            if phi[i] != 0: break
            a += 1
        b = len(phi) 
        for i in range(len(phi)-1, 0, -1):
            if phi[i] != 0: break
            b -= 1
        zeros = []
        for i in range(a, b):
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
        self.spinbox.setRange(3, 30) # min and max number of modes
        self.spinbox.setSuffix(" modes per decade")
        self.spinbox.setValue(self.parameters["bpd"].value) #initial value
        tb.addWidget(self.spinbox)
        self.thToolsLayout.insertWidget(0, tb)
        connection_id = self.spinbox.valueChanged.connect(self.handle_spinboxValueChanged)

        #disable useless buttons for this theory
        self.parent_dataset.actionMinimize_Error.setDisabled(True)
        self.parent_dataset.actionShow_Limits.setDisabled(True)
        self.parent_dataset.actionVertical_Limits.setDisabled(True)
        self.parent_dataset.actionHorizontal_Limits.setDisabled(True)

    def handle_spinboxValueChanged(self, value):
        """Handle a change of the parameter 'bpd'
        
        [description]
        
        Arguments:
            value {[type]} -- [description]
        """
        self.set_param_value("bpd", value)
        item = self.thParamTable.findItems("bpd", Qt.MatchCaseSensitive, column=0)
        item[0].setText(1, "%g"%value)
        #self.do_fit("")
