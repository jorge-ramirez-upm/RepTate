import numpy as np
from scipy import interp
from Theory import *

class TheoryWLFShift(Theory, CmdBase):
    """Basic theory for Time-Temperature Superposition, based on the WLF equation"""
    thname="WLFShift"
    description="Basic theory for Time-Temperature Superposition, based on the WLF equation"
    cite="TODO: Cite Dietmar Auhl paper?"

    def __init__(self, name="ThWLFShift", parent_dataset=None, ax=None):
        super(TheoryWLFShift, self).__init__(name, parent_dataset, ax)
        self.function = self.TheoryWLFShift
        self.parameters["C1"]=Parameter("C1", 6.85, "Material parameter C1 for WLF Shift", ParameterType.real, True)
        self.parameters["C2"]=Parameter("C2", 150, "Material parameter C2 for WLF Shift", ParameterType.real, True)
        self.parameters["rho0"]=Parameter("rho0", 0.95, "Density of polymer at 0 °C", ParameterType.real, False)
        self.parameters["C3"]=Parameter("C3", 0.69, "Density parameter TODO: Meaning of this?", ParameterType.real, False)
        self.parameters["T0"]=Parameter("T0", -50, "Temperature to shift WLF to, in °C", ParameterType.real, False)
        self.parameters["CTg"]=Parameter("CTg", 13, "Molecular weight dependence of Tg", ParameterType.real, False)
        self.parameters["dx12"]=Parameter("dx12", 0, "For PBd", ParameterType.real, False)

    def bT(self, T, T0, rho0, c3):
        return 

    def TheoryWLFShift(self, f=None):
        ft=f.data_table
        tt=self.tables[f.file_name_short]
        tt.num_columns=ft.num_columns
        tt.num_rows=ft.num_rows
        tt.data=np.zeros((tt.num_rows, tt.num_columns))

        T0=self.parameters["T0"].value
        C1=self.parameters["C1"].value
        C2=self.parameters["C2"].value
        C3=self.parameters["C3"].value
        rho0=self.parameters["rho0"].value
        CTg=self.parameters["CTg"].value
        dx12=self.parameters["dx12"].value

        T=f.file_parameters["T"]
        Mw=f.file_parameters["Mw"]

        C2 += CTg / Mw - 68.7 * dx12
        T0corrected = T0 - CTg / Mw + 68.7 * dx12
        tt.data[:,0] = ft.data[:,0]*np.power(10.0, -(T - T0corrected) * (C1 / (T + C2)))

        bT = (rho0 - T * C3 * 1E-3) * (T + 273.15) / ((rho0 - T0 * C3 * 1E-3) * (T0 + 273.15));
        tt.data[:,1] = ft.data[:,1] / bT;
        tt.data[:,2] = ft.data[:,2] / bT;
