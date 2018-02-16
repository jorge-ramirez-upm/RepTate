# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# --------------------------------------------------------------------------------------------------------
#
# Authors:
#     Jorge Ramirez, jorge.ramirez@upm.es
#     Victor Boudara, victor.boudara@gmail.com
#
# Useful links:
#     http://blogs.upm.es/compsoftmatter/software/reptate/
#     https://github.com/jorge-ramirez-upm/RepTate
#     http://reptate.readthedocs.io
#
# --------------------------------------------------------------------------------------------------------
#
# Copyright (2017): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
#
# This file is part of RepTate.
#
# RepTate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RepTate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RepTate.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------------------------
"""Module TheoryRouseTime

Module for the Rouse theory for the relaxation modulus.

"""
from Theory import Theory
from Parameter import OptType


class TheoryRouseTime(Theory, CmdBase):
    """Fit Rouse modes to a time depenendent relaxation function
    
    [description]
    """
    thname = "RouseTime"
    description = "Fit Rouse modes to time dependent function"
    citations = ""

    def __init__(self, name="ThRouseTime", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThRouseTime"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super(TheoryRouseTime, self).__init__(name, parent_dataset, ax)
        self.function = self.RouseTime

    def RouseTime(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        """
        pass


class TheoryRouseFrequency(Theory, CmdBase):
    """Fit Rouse modes to a frequency depenendent relaxation function
    
    [description]
    """
    thname = "RouseFrequency"
    description = "Fit Maxwell modes to frequency dependent function"

    def __init__(self, name="ThMaxwellFrequency", parent_dataset=None,
                 ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThMaxwellFrequency"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super(TheoryRouseFrequency, self).__init__(name, parent_dataset, ax)
        self.function = self.RouseFrequency
        self.has_modes = True
        self.parameters["logwmin"] = Parameter(
            "logwmin",
            -5,
            "Log of frequency range minimum",
            ParameterType.real,
            opt_type=OptType.nopt)
        self.parameters["logwmax"] = Parameter(
            "logwmax",
            4,
            "Log of frequency range maximum",
            ParameterType.real,
            opt_type=OptType.nopt)
        self.parameters["nmodes"] = Parameter(
            "nmodes",
            5,
            "Number of Rouse modes",
            ParameterType.integer,
            opt_type=OptType.const)
        for i in range(self.parameters["nmodes"].value):
            self.parameters["logG%d" % i] = Parameter(
                "logG%d" % i,
                5.0,
                "Log of Mode %d amplitude" % i,
                ParameterType.real,
                opt_type=OptType.opt)

    def set_param_value(self, name, value):
        """[summary]
        
        [description]
        
        Arguments:
            name {[type]} -- [description]
            value {[type]} -- [description]
        """
        if (name == "nmodes"):
            oldn = self.parameters["nmodes"].value
        message, success = super(TheoryRouseFrequency, self).set_param_value(name, value)
        if not success:
            return message, success
        if (name == "nmodes"):
            for i in range(self.parameters["nmodes"].value):
                self.parameters["logG%d" % i] = Parameter(
                    "logG%d" % i,
                    5.0,
                    "Log of Mode %d amplitude" % i,
                    ParameterType.real,
                    opt_type=OptType.opt)
            if (oldn > self.parameters["nmodes"].value):
                for i in range(self.parameters["nmodes"].value, oldn):
                    del self.parameters["logG%d" % i]
        return '', True

    def get_modes(self):
        """[summary]
        
        [description]
        
        Returns:
            [type] -- [description]
        """
        nmodes = self.parameters["nmodes"].value
        freq = np.logspace(self.parameters["logwmin"].value,
                           self.parameters["logwmax"].value, nmodes)
        tau = 1.0 / freq
        G = np.zeros(nmodes)
        for i in range(nmodes):
            G[i] = np.power(10, self.parameters["logG%d" % i].value)
        return tau, G

    def set_modes(self, tau, G):
        """[summary]
        
        [description]
        
        Arguments:
            tau {[type]} -- [description]
            G {[type]} -- [description]
        """
        print("set_modes not allowed in this theory (%s)" % self.name)
