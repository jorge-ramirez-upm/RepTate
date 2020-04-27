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
# Copyright (2018): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module TheoryWLF

WLF file for creating a new theory
"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable


class TheoryWLF(CmdBase):
    """Time-temperature superposition based on a Williams-Landel-Ferry (WLF) equation with two parameters.
    
    * **Function**
        .. math::
            \\begin{eqnarray}
            \\omega(T_r) &= & a_T \\omega(T) \\\\
            G(T_r) &= & b_T G(T) \\\\
            \\log_{10} a_T &= & \\frac{-B_1 (T-T_r)}{(B_2+T_r)(B_2+T)} \\\\
            b_T &= & \\frac{\\rho(T_r)T_r}{\\rho(T)T} = \\frac{(1+\\alpha T)(T_r+273.15)}{(1+\\alpha T_r)(T+273.15)} \\\\
            T_g &= &T_g^\\infty - \\frac{C_{T_g}}{M_w}
            \\end{eqnarray}
    
    * **Parameters**
       - :math:`T_r`: Reference temperature to which the experimental data will be shifted.
       - :math:`B_1`: Material parameter, corresponding to :math:`C_1\cdot C_2`, with :math:`C_1` and :math:`C_2` being the standard WLF material parameters.
       - :math:`B_2`: Material parameter, corresponding to :math:`C_2-T_r`, :math:`C_2` being the standard WLF material parameter.
       - logalpha: Decimal logarithm of the thermal expansion coefficient of the polymer at 0 °C.
       - :math:`C_{T_g}`: Material parameter that describes the dependence of :math:`T_g` with :math:`M_w`.
       - dx12: Fraction of 1-2 (vynil) units (valid for polybutadiene).
    """
    thname = 'WLF'
    description = 'Williams-Landel-Ferry'
    citations = []
    doi = []

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
        return GUITheoryWLF(
            name, parent_dataset,
            axarr) if (CmdBase.mode == CmdMode.GUI) else CLTheoryWLF(
                name, parent_dataset, axarr)


class BaseTheoryWLF:
    """[summary]
    
    [description]
    """
    #help_file = ''
    single_file = False  # False if the theory can be applied to multiple files simultaneously
    thname = TheoryWLF.thname
    citations = TheoryWLF.citations

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.WLF
        self.parameters["Tr"] = Parameter(
            name="Tr",
            value=25,
            description="Reference T to WLF shift the data to",
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters["B1"] = Parameter(
            name="B1",
            value=850,
            description="Material parameter B1 for WLF Shift",
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters["B2"] = Parameter(
            name="B2",
            value=126,
            description="Material parameter B2 for WLF Shift",
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters["logalpha"] = Parameter(
            name="logalpha",
            value=-3.18,
            description="Log_10 of the thermal expansion coefficient at 0 °C",
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters["CTg"] = Parameter(
            name="CTg",
            value=14.65,
            description="Molecular weight dependence of Tg",
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters["dx12"] = Parameter(
            name="dx12",
            value=0,
            description="Fraction 1,2 vinyl units (for PBd)",
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters["vert"] = Parameter(
            name="vert",
            value=True,
            description="Shift vertically",
            type=ParameterType.boolean,
            opt_type=OptType.const,
            display_flag=False)
        self.parameters["iso"] = Parameter(
            name="iso",
            value=True,
            description="Isofrictional state",
            type=ParameterType.boolean,
            opt_type=OptType.const,
            display_flag=False)

        self.get_material_parameters()

    def WLF(self, f=None):
        """WLF function         
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        
        Tr = self.parameters["Tr"].value
        B1 = self.parameters["B1"].value
        B2 = self.parameters["B2"].value
        alpha = np.power(10.0, self.parameters["logalpha"].value)
        CTg = self.parameters["CTg"].value
        iso = self.parameters["iso"].value
        vert = self.parameters["vert"].value

        Mw = f.file_parameters["Mw"]
        
        tt.data[:, 0] = ft.data[:, 0]

        if iso:
            B2 += CTg / Mw # - 68.7 * dx12
            Trcorrected = Tr - CTg / Mw # + 68.7 * dx12
        else:
            Trcorrected = Tr
        tt.data[:, 1] = np.power(10.0, -B1 *(ft.data[:, 0] - Trcorrected) /(B2 + Trcorrected) /(B2 + ft.data[:, 0]))
        tt.data[:, 2] = (1 + alpha * ft.data[:, 0]) * (Tr + 273.15) / (1 + alpha * Tr) / (
                ft.data[:, 0] + 273.15)


class CLTheoryWLF(BaseTheoryWLF, Theory):
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


class GUITheoryWLF(BaseTheoryWLF, QTheory):
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
