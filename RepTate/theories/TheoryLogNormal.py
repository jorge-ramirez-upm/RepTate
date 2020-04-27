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
"""Module TheoryLogNormal
"""
import numpy as np
from math import gamma, pi
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable


class TheoryLogNormal(CmdBase):
    """[summary]
    
    [description]
    """
    thname = 'LogNormal'
    description = 'LogNormal distribution'
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
        return GUITheoryLogNormal(
            name, parent_dataset,
            axarr) if (CmdBase.mode == CmdMode.GUI) else CLTheoryLogNormal(
                name, parent_dataset, axarr)


class BaseTheoryLogNormal:
    """Log-Normal distribution: the logarithm of the molecular weight is normally distributed
    
    * **Function**
        .. math::
            W(M) = W_0 \\frac{1}{\\sqrt{2\\pi\\sigma^2}} \\frac{1}{M} \\exp\\left[ - \\frac{\\left(\\ln{M}-\\ln{M_0}\\right)^2}{2\\sigma^2} \\right]
    
    * **Parameters**
       - ``logW0`` :math:`\\equiv\\log_{10}(W_0)`: Normalization constant.
       - ``logM0`` :math:`\\equiv\\log_{10}(M_0)`
       - ``sigma`` :math:`\\equiv\\sigma`
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/MWD/Theory/theory.html#log-normal-distribution'
    single_file = False  # False if the theory can be applied to multiple files simultaneously
    thname = TheoryLogNormal.thname
    citations = TheoryLogNormal.citations
    doi = TheoryLogNormal.doi

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.LogNormal  # main theory function
        self.has_modes = False  # True if the theory has modes
        self.parameters['logW0'] = Parameter(
            name='logW0',
            value=5,
            description='Normalization constant',
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters['logM0'] = Parameter(
            name='logM0',
            value=5,
            description='Log mean molecular weight',
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters['sigma'] = Parameter(
            name='sigma',
            value=1,
            description='Standard deviation',
            type=ParameterType.real,
            opt_type=OptType.opt,
            min_value=0)

    def LogNormal(self, f=None):
        """LogNormal function
        
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
        W0 = np.power(10.0, self.parameters["logW0"].value)
        M0 = np.power(10.0, self.parameters["logM0"].value)
        sigma = self.parameters["sigma"].value

        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]
        tt.data[:, 1] = W0 / sigma / np.sqrt(2 * pi) / tt.data[:, 0] * np.exp(
            -(np.log(tt.data[:, 0]) - np.log(M0))**2 / 2 / sigma**2)

    def do_error(self, line):
        super().do_error(line)
        if (line == ""):
            self.Qprint('''<h3>Characteristics of the fitted MWD</h3>''')
            M0 = np.power(10.0, self.parameters["logM0"].value)
            sigma = self.parameters["sigma"].value
            Mn = M0 * np.exp(sigma**2 / 2)
            Mw = M0 * np.exp(3 * sigma**2 / 2)
            Mz = M0 * np.exp(5 * sigma**2 / 2)
            # table='''<table border="1" width="100%">'''
            # table+='''<tr><th>Mn</th><th>Mw</th><th>Mz</th><th>D</th></tr>'''
            # table+='''<tr><td>%6.3gk</td><td>%6.3gk</td><td>%6.3gk</td><td>%7.3g</td></tr>'''%(Mn / 1000, Mw / 1000, Mz/1000 , Mw/Mn)
            # table+='''</table><br>'''
            table = [['%-12s' % 'Mn (kg/mol)', '%-12s' % 'Mw (kg/mol)', '%-9s' % 'Mw/Mn', '%-9s' % 'Mz/Mw'],]
            table.append(['%-12.3g' % (Mn / 1000), '%-12.3g' % (Mw / 1000), '%-9.3g' % (Mw / Mn), '%-9.3g' % (Mz / Mw)])
            self.Qprint(table)


class CLTheoryLogNormal(BaseTheoryLogNormal, Theory):
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


class GUITheoryLogNormal(BaseTheoryLogNormal, QTheory):
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
