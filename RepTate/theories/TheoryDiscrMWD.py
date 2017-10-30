from Theory import *
import numpy as np
from scipy import interp

class TheoryDiscrMWD(Theory, CmdBase):
    """Discretize a Molecular Weight Distribution"""
    thname = "MWDiscr"
    description = "Discretize a Molecular Weight Distribution"
    citations = ""

    def __init__(self, name="ThDiscrMWD", parent_dataset=None, ax=None):
        super(TheoryDiscrMWD, self).__init__(name, parent_dataset, ax)
        self.function = self.DiscretiseMWD
        self.has_modes = False
        self.parameters["binpd"] = Parameter(
            "binpd", 10, "Number modes per decade", ParameterType.integer, False)
        self.parameters["Mn"] = Parameter(
            "Mn", 1000, "Number-average molecular mass", ParameterType.real, False)
        self.parameters["Mw"] = Parameter(
            "Mw", 1000, "Weight-average molecular mass", ParameterType.real, False)
        self.parameters["Mz"] = Parameter(
            "Mz", 1, "z-average molecular mass", ParameterType.real, False)
        self.parameters["PDI"] = Parameter(
            "PDI", 1, "Polydispersity index", ParameterType.real, False)

    def calculate_moments(self, f, line=""):
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
            "\nCharacteristics of the %s MWD:\n"
            "Mn=%0.3g kg/mol, Mw=%0.3g kg/mol, Mw/Mn=%0.3g, Mz/Mw=%0.3g\n"
            %(line, Mn/1000, Mw/1000, PDI, Mz/Mw)
            )

    def do_error(self, line):
        pass

    def DiscretiseMWD(self, f=None):
        """
        Discretize a molecular weight distribution
        """
        # sort M, w(M) with M increasing intoft
        ft = f.data_table.data[np.argsort(f.data_table.data[:, 0])]
        #normalize the weights w(M)
        ft[:, 1] = ft[:, 1]/np.sum(ft[:, 1])
        self.calculate_moments(ft, "input")
        
        #molar mass min and max
        mmin = np.min(ft[:, 0])
        mmax = np.max(ft[:, 0])

        #create theory table (tt)
        nM = int(np.ceil((np.log10(mmax) - np.log10(mmin))*self.parameters["binpd"].value))
        tt = self.tables[f.file_name_short]
        tt.num_columns = 2
        tt.num_rows = nM
        tt.data = np.zeros((tt.num_rows, tt.num_columns))

        #(nM+1) bins equally distributed on logarithmic scale
        bins = np.zeros(nM + 1)
        for i in range(nM + 1):
            bins[i] = mmin*np.power(10, i/nM * np.log10(mmax/mmin))



        tt.data[:, 1], bins = np.histogram(
            ft[:, 0], bins=bins, range=(mmin, mmax), weights=ft[:, 1]
            )

        #Centered M
        for i in range(nM):
            tt.data[i, 0] = np.power(10, (np.log10(bins[i]) + np.log10(bins[i + 1]))/2)

        self.calculate_moments(tt.data, "discretized")
