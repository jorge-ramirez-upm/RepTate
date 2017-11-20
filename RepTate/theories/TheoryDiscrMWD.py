from Theory import *
from QTheory import *
import numpy as np
from scipy import interp
from PyQt5.QtWidgets import QToolBar, QSpinBox


class TheoryDiscrMWD(CmdBase):
    """Discretize a Molecular Weight Distribution"""
    thname = "MWDiscr"
    description = "Discretize a Molecular Weight Distribution"
    citations = ""
    def __new__(cls, name="MWDiscr", parent_dataset=None, ax=None):
        return GUITheoryDiscrMWD(name, parent_dataset, ax) if (CmdBase.mode==CmdMode.GUI) else CLTheoryDiscrMWD(name, parent_dataset, ax)

class BaseTheoryDiscrMWD:
    def __init__(self, name="ThDiscrMWD", parent_dataset=None, ax=None):
        super().__init__(name, parent_dataset, ax)
        self.function = self.DiscretiseMWD
        self.has_modes = False
        self.parameters["bpd"] = Parameter(
            "bpd", 10, "Number modes per decade", ParameterType.integer, False)
        self.parameters["Mn"] = Parameter(
            "Mn", 1000, "Number-average molecular mass", ParameterType.real, False)
        self.parameters["Mw"] = Parameter(
            "Mw", 1000, "Weight-average molecular mass", ParameterType.real, False)
        self.parameters["Mz"] = Parameter(
            "Mz", 1, "z-average molecular mass", ParameterType.real, False)
        self.parameters["PDI"] = Parameter(
            "PDI", 1, "Polydispersity index", ParameterType.real, False)

    def do_error(self, line):
        pass

    def calculate_moments(self, f, line=""):
        '''Calculate the moments Mn, Mw, and Mz of a molecular mass distribution'''
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

        self.set_param_value("Mn", Mn)
        self.set_param_value("Mw", Mw)
        self.set_param_value("Mz", Mz)
        self.set_param_value("PDI", PDI)
        print(
            "Characteristics of the %s MWD:\n"
            "Mn=%0.3g kg/mol, Mw=%0.3g kg/mol, Mw/Mn=%0.3g, Mz/Mw=%0.3g\n"
            %(line, Mn/1000, Mw/1000, PDI, Mz/Mw)
            )


    def DiscretiseMWD(self, f=None):
        """Discretize a molecular weight distribution"""

        # sort M, w(M) with M increasing in ft
        ft = f.data_table.data[np.argsort(f.data_table.data[:,0])]
        n = ft[:, 0].size
        #normalize the weights w(M)
        ft[:,1] = ft[:,1]/np.sum(ft[:,1])
        self.calculate_moments(ft, "input")

        #molar mass min and max 
        mmin = 0.1*np.min(ft[:, 0])
        mmax = 10*np.max(ft[:, 0])

        #create theory table (tt) and temp table
        nbin = int(np.ceil((np.log10(mmax/mmin))*self.parameters["bpd"].value))
        tt = self.tables[f.file_name_short]
        tt.num_columns = 2
        tt.num_rows = nbin
        tt.data = np.zeros((tt.num_rows, tt.num_columns))

        #bins equally spaced on logarithmic scale
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

        #find into which bin the data point belong
        inds = np.digitize(mid_ft, edge_bins, right=False) 
        '''returns indices of the bins to which each value in input array belongs
        edge_bins[inds[j]-1] <= mid_ft[j] < edge_bins[inds[j]]'''

        phi = np.zeros(nbin)
        nk = np.zeros(nbin)
        for j in range(n - 1):
            k = inds[j]
            dlogMj = np.log10(ft[j + 1, 0]) - np.log10(ft[j, 0])
            wj = (ft[j + 1, 1] + ft[j, 1]) / 2
            dlogMk = (np.log10(bins[k + 1])  - np.log10(bins[k - 1])) / 2
            phi[k] +=  wj*dlogMj/dlogMk #weight x width / bin_width
            nk[k] += 1

        # phi = np.choose(nk==0, (phi/nk * np.sum(nk)/nbin, phi)) #throws a warning
        sum_nk = np.sum(nk)
        for k in range (nbin):
            if nk[k]>0: 
                phi[k] = phi[k]/nk[k] * sum_nk/nbin

        #copy weights and M into theory table
        tt.data[:, 0] = bins
        tt.data[:, 1] = phi/np.sum(phi)

        self.calculate_moments(tt.data, "discretized")

class CLTheoryDiscrMWD(BaseTheoryDiscrMWD, Theory):
    def __init__(self, name="MWDiscr", parent_dataset=None, ax=None):
        super().__init__(name, parent_dataset, ax)
        
class GUITheoryDiscrMWD(BaseTheoryDiscrMWD, QTheory):
    def __init__(self, name="MWDiscr", parent_dataset=None, ax=None):
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

    # def nmode_non_editable(self):
    #     item = self.thParamTable.findItems("nmodes", Qt.MatchCaseSensitive, column=0)
    #     item.setDisabled(True)

    def handle_spinboxValueChanged(self, value):
        """Handle a change of the parameter 'bpd'"""
        self.set_param_value("bpd", value)
        item = self.thParamTable.findItems("bpd", Qt.MatchCaseSensitive, column=0)
        item[0].setText(1, "%g"%value)
        #self.do_fit("")

