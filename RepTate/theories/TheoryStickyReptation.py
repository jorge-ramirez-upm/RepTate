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
"""Module TheoryStickyReptation

Template file for creating a new theory
"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from scipy import interpolate

class TheoryStickyReptation(CmdBase):
    """[summary]
    
    [description]
    """
    thname = 'StickyReptation'
    description = 'Sticky Reptation'
    citations = 'L. Leibler, M. Rubinstein and Ralph H. Colby, Macromolecules, 1991, 24, 4701-4704'
    doi = "http://dx.doi.org/10.1021/ma00016a034"

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
        return GUITheoryStickyReptation(
            name, parent_dataset,
            axarr) if (CmdBase.mode == CmdMode.GUI) else CLTheoryStickyReptation(
                name, parent_dataset, axarr)


class BaseTheoryStickyReptation:
    """[summary]
    
    [description]
    """
    #help_file = ''
    single_file = False  # False if the theory can be applied to multiple files simultaneously
    thname = TheoryStickyReptation.thname
    citations = TheoryStickyReptation.citations

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
        self.parameters['Ge'] = Parameter(
            name='Ge',
            value=10000,
            description='Entanglement modulus',
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters['tau_s'] = Parameter(
            name='tau_s',
            value=0.02,
            description='sticker time',
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters['Zs'] = Parameter(
            name='Zs',
            value=10,
            description='Number of stickers per chain',
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters['Ze'] = Parameter(
            name='Ze',
            value=10,
            description='Number of entanglements',
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters['alpha'] = Parameter(
            name='alpha',
            value=10,
            description='CLF parameter?',
            type=ParameterType.real,
            opt_type=OptType.const)


    def get_modes(self):
        """[summary]
        
        [description]
        
        Returns:
            - [type] -- [description]
        """
        pass

    def set_modes(self):
        """[summary]
        
        [description]
        
        Arguments:

        """
        pass

    def destructor(self):
        """[summary]
        
        [description]
        
        Arguments:

        """
        pass

    def g(self, x):
        mmax=100
        gx = np.zeros(len(x))
        for m in range(1, mmax):
            gx += (1-np.exp(-m**2*x))/m**2
        return gx

    def calculate(self, f=None):
        """Template function that returns the square of y
        
        [description]
        
        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]

        w = ft.data[:, 0]
        tmin = 0.1/max(w)
        tmax = 10/min(w)
        n = 100
        t=np.logspace(np.log10(tmin), np.log10(tmax), n)

        Ge = self.parameters['Ge'].value
        tau_s = self.parameters['tau_s'].value
        Zs = self.parameters['Zs'].value
        Ze = self.parameters['Ze'].value
        alpha = self.parameters['alpha'].value

        GSR = 0
        Z0 = min(Ze, Zs)
        Z1 = max(Ze, Zs)
        for q in range (1, int(Z0)+1):
            GSR += 0.2*np.exp(-t*q**2/tau_s/Zs**2)
        for q in range (int(Z0)+2, int(Z1)+1):
            GSR += np.exp(-t*q**2/tau_s/Zs**2)
        GSR *= Ge/Ze

        tau_rep=tau_s*Ze*Zs**2
        x = Ze*t/alpha/tau_rep
        Ut = t/tau_rep + alpha/Ze*self.g(x)
        GREP=0
        qmax=100
        for q in range (1, qmax, 2):
            GREP+=np.exp(-q**2*Ut)/q**2
        GREP=Ge*(GREP*8/np.pi**2)**2

        G = GSR + GREP

        f = interpolate.interp1d(
            t,
            G,
            kind='cubic',
            assume_sorted=True,
            fill_value='extrapolate')
        g0 = f(0)
        ind1 = np.argmax(t > 0)
        t1 = t[ind1]
        g1 = G[ind1]
        tinf = np.max(t)
        wp = np.logspace(np.log10(1 / tinf), np.log10(1 / t1), n)
        tt.num_columns = ft.num_columns
        tt.num_rows = n
        G1G2 = np.zeros((n, 3))
        G1G2[:, 0] = wp[:]

        coeff = (G[ind1 + 1:] - G[ind1:-1]) / (
            t[ind1 + 1:] - t[ind1:-1])
        for i, w in enumerate(wp):

            G1G2[i, 1] = g0 + np.sin(w * t1) * (g1 - g0) / w / t1 + np.dot(
                coeff, -np.sin(w * t[ind1:-1]) +
                np.sin(w * t[ind1 + 1:])) / w

            G1G2[i, 2] = -(1 - np.cos(w * t1)) * (g1 - g0) / w / t1 - np.dot(
                coeff,
                np.cos(w * t[ind1:-1]) -
                np.cos(w * t[ind1 + 1:])) / w

        # STORE THE FUNCTION IN SOME OTHER TEMPORARY ARRAY
        # INTERPOLATE IT SO THAT THE OMEGA RANGE AND POINTS ARE THE SAME AS IN THE EXPERIMENTAL DATA
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((ft.num_rows, ft.num_columns))
        f1 = interpolate.interp1d(
            wp,
            G1G2[:, 1],
            kind='cubic',
            assume_sorted=True,
            fill_value='extrapolate')
        f2 = interpolate.interp1d(
            wp,
            G1G2[:, 2],
            kind='cubic',
            assume_sorted=True,
            fill_value='extrapolate')
        tt.data[:, 0]= ft.data[:, 0]
        tt.data[:, 1]= f1(ft.data[:, 0])
        tt.data[:, 2]= f2(ft.data[:, 0])


class CLTheoryStickyReptation(BaseTheoryStickyReptation, Theory):
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


class GUITheoryStickyReptation(BaseTheoryStickyReptation, QTheory):
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
