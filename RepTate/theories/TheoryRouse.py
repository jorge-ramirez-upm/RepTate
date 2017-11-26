# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module TheoryRouseTime

Module for the Rouse theory for the relaxation modulus.

""" 
from Theory import *

class TheoryRouseTime(Theory, CmdBase):
    """Fit Rouse modes to a time depenendent relaxation function"""
    thname="RouseTime"
    description="Fit Rouse modes to time dependent function"
    citations=""

    def __init__(self, name="ThRouseTime", parent_dataset=None, ax=None):
        super(TheoryRouseTime, self).__init__(name, parent_dataset, ax)
        self.function = self.RouseTime

    def RouseTime(self, f=None):
        pass   

class TheoryRouseFrequency(Theory, CmdBase):
    """Fit Maxwell modes to a frequency dependent relaxation function"""
    thname="RouseFrequency"
    description="Fit Maxwell modes to frequency dependent function"

    def __init__(self, name="ThMaxwellFrequency", parent_dataset=None, ax=None):
        super(TheoryRouseFrequency, self).__init__(name, parent_dataset, ax)
        self.function = self.RouseFrequency
        self.has_modes = True
        self.parameters["logwmin"]=Parameter("logwmin", -5, "Log of frequency range minimum", ParameterType.real, True)
        self.parameters["logwmax"]=Parameter("logwmax", 4, "Log of frequency range maximum", ParameterType.real, True)
        self.parameters["nmodes"]=Parameter("nmodes", 5, "Number of Rouse modes", ParameterType.integer, False)
        for i in range(self.parameters["nmodes"].value):
            self.parameters["logG%d"%i]=Parameter("logG%d"%i,5.0,"Log of Mode %d amplitude"%i, ParameterType.real, True)

    def set_param_value(self, name, value):
        if (name=="nmodes"):
            oldn=self.parameters["nmodes"].value
        super(TheoryRouseFrequency, self).set_param_value(name, value)
        if (name=="nmodes"):
            for i in range(self.parameters["nmodes"].value):
                self.parameters["logG%d"%i]=Parameter("logG%d"%i,5.0,"Log of Mode %d amplitude"%i, ParameterType.real, True)
            if (oldn>self.parameters["nmodes"].value):
                for i in range(self.parameters["nmodes"].value,oldn):
                    del self.parameters["logG%d"%i]

    def get_modes(self):
        nmodes=self.parameters["nmodes"].value
        freq=np.logspace(self.parameters["logwmin"].value, self.parameters["logwmax"].value, nmodes)
        tau=1.0/freq
        G=np.zeros(nmodes)
        for i in range(nmodes):
            G[i]=np.power(10, self.parameters["logG%d"%i].value)
        return tau, G

    def set_modes(self, tau, G):
        print("set_modes not allowed in this theory (%s)"%self.name)
