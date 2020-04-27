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
"""Module TheoryDTDStars

Dynamics Tube Dilution for Stars
"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from scipy.integrate import quad
from scipy.special import gammaln

import dtd_ctypes_helper as dtdh


class TheoryDTDStarsFreq(CmdBase):
    """Fit DTD Theory for stars.
    Theory of stress relaxation in star polymer melts with no adjustable parameters beyond those measurable in linear melts
    
    * **Function**
        See `Milner-McLeish (1997) <http://www.che.psu.edu/faculty/milner/group/eprints/1997/Macromolecules1997Milner.pdf>`_
        and
        `Larson et al. (2003) <http://www.personal.reading.ac.uk/~sms06al2/papers/definit.pdf>`_ for details.

    * **Parameters**
       - ``G0`` :math:`\\equiv G_N^0`: Plateau modulus
       - ``tau_e`` :math:`\\equiv \\tau_\\mathrm e = \\left(\\dfrac{M_\mathrm e^\\mathrm G}{M_0}\\right)^2  \\dfrac{\\zeta b^2}{3\\pi^2k_\\mathrm B T}`: 
         Entanglement equilibration time
       - ``Me`` :math:`\\equiv M_\mathrm e^\mathrm G = \\dfrac 4 5 \\dfrac{\\rho R T} {G_N^0}`: Entanglement molecular weight
       - ``alpha``: Dilution exponent

       where:
         - :math:`\\rho`: polymer density
         - :math:`\\zeta`: monomeric friction coefficient
         - :math:`b`: monomer-based segment length
         - :math:`k_\\mathrm B T`: thermal energy
         - :math:`M_0`: molar mass of an elementary segment
    """
    thname = "DTD Stars"
    description = "Dynamic Tube Dilution for stars, frequency domain"
    citations = ["Milner S.T. and McLeish T.C.B., Macromolecules 1997, 30, 2159-2166"]
    doi = ["http://dx.doi.org/10.1021/ma961559f"]
    
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
        return GUITheoryDTDStarsFreq(
            name, parent_dataset,
            axarr) if (CmdBase.mode == CmdMode.GUI) else CLTheoryDTDStarsFreq(
                name, parent_dataset, axarr)


class BaseTheoryDTDStarsFreq:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/LVE/Theory/theory.html#dynamic-dilution-equation-for-stars'
    single_file = False  # False if the theory can be applied to multiple files simultaneously
    thname = TheoryDTDStarsFreq.thname
    citations = TheoryDTDStarsFreq.citations
    doi = TheoryDTDStarsFreq.doi

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
        self.parameters["G0"] = Parameter(
            "G0",
            1e1,
            "Modulus c*kB*T/N",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0)
        self.parameters["tau_e"] = Parameter(
            "tau_e",
            2e-6,
            "Entanglement relaxation time",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0)
        self.parameters["Me"] = Parameter(
            "Me",
            5.0,
            "Entanglement Molecular Weight",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0)
        self.parameters["alpha"] = Parameter(
            "alpha",
            1.0,
            "Dilution parameter",
            ParameterType.real,
            opt_type=OptType.const,
            min_value=0)

        self.get_material_parameters()

        self.G0 = self.parameters["G0"].value
        self.tau_e = self.parameters["tau_e"].value
        self.Me = self.parameters["Me"].value
        self.alpha = self.parameters["alpha"].value
        self.Z = 1
        self.w = 0

    def calculate(self, f=None):
        """DTDStarsFreq function that returns the square of y
        
        [description]
        
        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        self.G0 = self.parameters["G0"].value
        self.tau_e = self.parameters["tau_e"].value
        self.Me = self.parameters["Me"].value
        self.alpha = self.parameters["alpha"].value
        try:
            Mw = float(f.file_parameters["Mw"])
        except (ValueError, KeyError):
            self.Qprint("Invalid Mw value")
            return
        # self.Z = int(np.rint(Mw / self.Me))
        omega = ft.data[:, 0]
        params = [self.G0, self.alpha, self.tau_e, Mw / self.Me, omega]
        gp, gpp, success = dtdh.calculate_dtd_freq(params, self.eps)
        if not success:
            self.Qprint("Too many steps in routine qtrap")
            return
        tt.data[:, 0] = omega
        tt.data[:, 1] = gp[:]
        tt.data[:, 2] = gpp[:]


class CLTheoryDTDStarsFreq(BaseTheoryDTDStarsFreq, Theory):
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


class GUITheoryDTDStarsFreq(BaseTheoryDTDStarsFreq, QTheory):
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


#############################################################################################
#############################################################################################


class TheoryDTDStarsTime(CmdBase):
    """Fit DTD Theory for stars
    
    * **Function**
        See `Milner-McLeish (1997) <http://www.che.psu.edu/faculty/milner/group/eprints/1997/Macromolecules1997Milner.pdf>`_
        and
        `Larson et al. (2003) <http://www.personal.reading.ac.uk/~sms06al2/papers/definit.pdf>`_ for details.

    * **Parameters**
       - ``G0`` :math:`\\equiv G_N^0`: Plateau modulus
       - ``tau_e`` :math:`\\equiv \\tau_\\mathrm e = \\left(\\dfrac{M_\mathrm e^\\mathrm G}{M_0}\\right)^2  \\dfrac{\\zeta b^2}{3\\pi^2k_\\mathrm B T}`: 
         Entanglement equilibration time
       - ``Me`` :math:`\\equiv M_\mathrm e^\mathrm G = \\dfrac 4 5 \\dfrac{\\rho R T} {G_N^0}`: Entanglement molecular weight
       - ``alpha``: Dilution exponent
       
       where:
         - :math:`\\rho`: polymer density
         - :math:`\\zeta`: monomeric friction coefficient
         - :math:`b`: monomer-based segment length
         - :math:`k_\\mathrm B T`: thermal energy
         - :math:`M_0`: molar mass of an elementary segment
    """
    thname = "DTD Stars"
    description = "Dynamic Tube Dilution for stars, time domain"
    citations = ["Milner S.T. and McLeish T.C.B., Macromolecules 1997, 30, 2159-2166"]
    doi = ["http://dx.doi.org/10.1021/ma961559f"]
    
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
        return GUITheoryDTDStarsTime(
            name, parent_dataset,
            axarr) if (CmdBase.mode == CmdMode.GUI) else CLTheoryDTDStarsTime(
                name, parent_dataset, axarr)


class BaseTheoryDTDStarsTime:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/Gt/Theory/theory.html#dtd-stars-time'
    single_file = False  # False if the theory can be applied to multiple files simultaneously
    thname = TheoryDTDStarsTime.thname
    citations = TheoryDTDStarsTime.citations
    doi = TheoryDTDStarsTime.doi

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
        self.parameters["G0"] = Parameter(
            "G0",
            1e1,
            "Modulus c*kB*T/N",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0)
        self.parameters["tau_e"] = Parameter(
            "tau_e",
            2e-6,
            "Entanglement relaxation time",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0)
        self.parameters["Me"] = Parameter(
            "Me",
            5.0,
            "Entanglement Molecular Weight",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0)
        self.parameters["alpha"] = Parameter(
            "alpha",
            1.0,
            "Dilution parameter",
            ParameterType.real,
            opt_type=OptType.const,
            min_value=0)

        self.get_material_parameters()

        self.G0 = self.parameters["G0"].value
        self.tau_e = self.parameters["tau_e"].value
        self.Me = self.parameters["Me"].value
        self.alpha = self.parameters["alpha"].value

    def calculate(self, f=None):
        """DTDStarsTime function that returns the square of y
        
        [description]
        
        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        self.G0 = self.parameters["G0"].value
        self.tau_e = self.parameters["tau_e"].value
        self.Me = self.parameters["Me"].value
        self.alpha = self.parameters["alpha"].value
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
        # self.Z = int(np.rint(Mw / self.Me))
        times = ft.data[:, 0]
        params = [self.G0, self.alpha, self.tau_e, Mw / self.Me, times]
        gt, success = dtdh.calculate_dtd_time(params, self.eps)
        if not success:
            self.Qprint("Too many steps in routine qtrap")
            return
        tt.data[:, 0] = times
        tt.data[:, 1] = gamma*gt[:]


class CLTheoryDTDStarsTime(BaseTheoryDTDStarsTime, Theory):
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

    # This class usually stays empty


class GUITheoryDTDStarsTime(BaseTheoryDTDStarsTime, QTheory):
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
