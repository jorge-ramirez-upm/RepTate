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
# Copyright (2017-2020): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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

RouseTime file for creating a new theory
"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
import rouse_ctypes_helper as rh


class TheoryRouseTime(CmdBase):
    """Fit Rouse modes to a time dependent relaxation function
    
    * **Function**
        Continuous Rouse model (valid for "large" :math:`N`):
        
        .. math::
            G(t) = G_0 \\dfrac 1 N \\sum_{p=1}^N \\exp\\left(\\dfrac{-2p^2t}{N^2\\tau_0}\\right)
    
    * **Parameters**
        - :math:`G_0 = ck_\\mathrm  B T`: "modulus"
        - :math:`\\tau_0`: relaxation time of an elementary segment
        - :math:`M_0`: molar mass of an elementary segment
        
        where
            - :math:`c`: number of segments per unit volume
            - :math:`k_\\mathrm  B`: Boltzmann constant
            - :math:`T`: temperature
            - :math:`N=M_w/M_0`: number of segments par chain
            - :math:`M_w`: weight-average molecular mass
    """
    thname = "Rouse"
    description = "Rouse model"
    citations = ["Rouse P.E. Jr, J. Chem. Phys. 1953, 21, 1272"]
    doi = ["http://dx.doi.org/10.1063/1.1699180"]

    def __new__(cls, name='', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUITheoryRouseTime(
            name, parent_dataset,
            axarr) if (CmdBase.mode == CmdMode.GUI) else CLTheoryRouseTime(
                name, parent_dataset, axarr)


class BaseTheoryRouseTime:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/Gt/Theory/theory.html#rouse-time'
    single_file = False  # False if the theory can be applied to multiple files simultaneously
    thname = TheoryRouseTime.thname
    citations = TheoryRouseTime.citations
    doi = TheoryRouseTime.doi

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate  # main theory function
        self.has_modes = False  # True if the theory has modes
        self.parameters["G0"] = Parameter(
            "G0",
            1e6,
            "Modulus c*kB*T/N",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0)
        self.parameters["tau0"] = Parameter(
            "tau0",
            1e-3,
            "segment relaxation time",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0)
        self.parameters["M0"] = Parameter(
            "M0",
            0.2,
            "segment molar mass",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0.01)

        # f = self.theory_files()[0]
        # t_data = f.data_table.data[:, 0]
        # tmin = min(t_data[np.nonzero(t_data)])
        # tmax = max(t_data)
        # self.parameters["logtmin"] = Parameter(
        #     "logtmin",
        #     np.log10(tmin),
        #     "Log of time range minimum",
        #     ParameterType.real,
        #     opt_type=OptType.const)
        # self.parameters["logtmax"] = Parameter(
        #     "logtmax",
        #     np.log10(tmax),
        #     "Log of time range maximum",
        #     ParameterType.real,
        #     opt_type=OptType.const)
        # self.parameters["points"] = Parameter(
        #     "points",
        #     20,
        #     "number of theory points per decade",
        #     ParameterType.real,
        #     opt_type=OptType.const)


    def calculate(self, f=None):
        """RouseTime function that returns the square of y
        
        [description]
        
        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        # logtmin = self.parameters["logtmin"].value
        # logtmax = self.parameters["logtmax"].value
        # points = self.parameters["points"].value
        # t = np.logspace(logtmin, logtmax, points*(logtmax - logtmin))
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        G0 = self.parameters["G0"].value
        tau0 = self.parameters["tau0"].value
        M0 = self.parameters["M0"].value
        try:
            Mw = float(f.file_parameters["Mw"])
        except (ValueError, KeyError):
            self.Qprint("Invalid Mw value")
            return
        try:
            gamma = float(f.file_parameters["gamma"])
            if (gamma==0):
                gamma=1
        except:
            gamma = 1

        t = ft.data[:, 0]
        params = [G0, tau0, Mw / M0, t]

        tt.data[:, 0] = t
        tt.data[:, 1] = gamma*rh.approx_rouse_time(params)


class CLTheoryRouseTime(BaseTheoryRouseTime, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # This class usually stays empty


class GUITheoryRouseTime(BaseTheoryRouseTime, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # add widgets specific to the theory here:


####################################################################
####################################################################


class TheoryRouseFrequency(CmdBase):
    """Fit Rouse modes to a frequency dependent relaxation function
    
    * **Function**
        Continuous Rouse model (valid for "large" :math:`N`):
        
        .. math::
          G'(\\omega) &= G_0 \\dfrac 1 N \\sum_{p=1}^N \\dfrac{(\\omega\\tau_p)^2} {1 +  (\\omega\\tau_p)^2}\\\\
          G''(\\omega) &= G_0 \\dfrac 1 N \\sum_{p=1}^N \\dfrac{\\omega\\tau_p} {1 +  (\\omega\\tau_p)^2}\\\\
          \\tau_p &= \\dfrac{N^2 \\tau_0 }{ 2 p^2}

    * **Parameters**
        - :math:`G_0 = ck_\\mathrm  B T`: "modulus"
        - :math:`\\tau_0`: relaxation time of an elementary segment
        - :math:`M_0`: molar mass of an elementary segment
        
        where
            - :math:`c`: number of segments per unit volume
            - :math:`k_\\mathrm  B`: Boltzmann constant
            - :math:`T`: temperature
            - :math:`N=M_w/M_0`: number of segments par chain
            - :math:`M_w`: weight-average molecular mass
    """
    thname = "Rouse"
    description = "Rouse model"
    citations = ["Rouse P.E. Jr, J. Chem. Phys. 1953, 21, 1272"]
    doi = ["http://dx.doi.org/10.1063/1.1699180"]

    def __new__(cls, name='', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUITheoryRouseFrequency(name, parent_dataset, axarr) if (
            CmdBase.mode == CmdMode.GUI) else CLTheoryRouseFrequency(
                name, parent_dataset, axarr)


class BaseTheoryRouseFrequency:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/LVE/Theory/theory.html#rouse-frequency'
    single_file = False  # False if the theory can be applied to multiple files simultaneously
    thname = TheoryRouseFrequency.thname
    citations = TheoryRouseFrequency.citations
    doi = TheoryRouseFrequency.doi

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate
        self.has_modes = False
        # self.parameters["logwmin"] = Parameter(
        #     "logwmin",
        #     -5,
        #     "Log of frequency range minimum",
        #     ParameterType.real,
        #     opt_type=OptType.nopt)
        # self.parameters["logwmax"] = Parameter(
        #     "logwmax",
        #     4,
        #     "Log of frequency range maximum",
        #     ParameterType.real,
        #     opt_type=OptType.nopt)
        self.parameters["G0"] = Parameter(
            "G0",
            1e6,
            "Modulus c*kB*T/N",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0)
        self.parameters["tau0"] = Parameter(
            "tau0",
            1e-3,
            "Segment relaxation time",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0)
        self.parameters["M0"] = Parameter(
            "M0",
            0.2,
            "Segment molar mass",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0)

    def calculate(self, f=None):
        """RouseFrequency function"""
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        G0 = self.parameters["G0"].value
        tau0 = self.parameters["tau0"].value
        M0 = self.parameters["M0"].value
        try:
            Mw = float(f.file_parameters["Mw"])
        except (ValueError, KeyError):
            self.Qprint("Invalid Mw value")
            return

        omega = ft.data[:, 0]
        params = [G0, tau0, Mw / M0, omega]
        gp, gpp = rh.approx_rouse_frequency(params)

        tt.data[:, 0] = omega
        tt.data[:, 1] = gp
        tt.data[:, 2] = gpp


class CLTheoryRouseFrequency(BaseTheoryRouseFrequency, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # This class usually stays empty


class GUITheoryRouseFrequency(BaseTheoryRouseFrequency, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # add widgets specific to the theory here:
