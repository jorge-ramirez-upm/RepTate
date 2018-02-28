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
 
class TheoryDTDStars(CmdBase):
    """Fit DTD Theory for stars
    

    """
    thname = "DTDStars"
    description = "Fit Dynamic Tube Dilution theory for stars"

    def __new__(cls, name='ThDTDStars', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThDTDStars'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryDTDStars(name, parent_dataset, axarr) if (
            CmdBase.mode == CmdMode.GUI) else CLTheoryDTDStars(
                name, parent_dataset, axarr)


class BaseTheoryDTDStars:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/en/latest/manual/Applications/LVE/Theory/theory.html#dtdstars'
    single_file = False  # False if the theory can be applied to multiple files simultaneously

    def __init__(self,
                 name='ThDTDStars',
                 parent_dataset=None,
                 axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThDTDStars'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate
        self.has_modes = True
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
            "entanglement relaxation time",
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
            
        self.G0 = self.parameters["G0"].value
        self.tau_e = self.parameters["tau_e"].value
        self.Me = self.parameters["Me"].value
        self.alpha = self.parameters["alpha"].value
        self.Z = 1
        self.w = 0

    def destructor(self):
        """[summary]
        
        [description]
        
        Arguments:

        """
        pass

    def Ueff(self, s):
        """
        Effective potential
        """
        return 3 * self.Z * (1 - (1 - s)**(1 + self.alpha) * (1 + (1 + self.alpha) * s)) / (1 + self.alpha) / (2 + self.alpha)
        
    def tau_early(self, s):
        """
        Relaxation time early
        """
        return 9 * np.pi**3 / 16 * self.tau_e * s**4 * self.Z**4
    
    def tau_late(self, s):
        """
        Relaxation time arm
        """
        return self.tau_e * self.Z**1.5 * np.sqrt(np.pi**5 / 6) * np.exp(self.Ueff(s))/ np.sqrt(s**2 * (1-s)**(2*self.alpha) + 
                    ((1 + self.alpha) / self.Z / 3)**(2 * self.alpha / (self.alpha + 1)) / (np.exp(gammaln(1 / (self.alpha + 1))))**2)

    def tau(self, s):
        """
        Relaxation time for segment s
        """
        eUe = np.exp(self.Ueff(s))
        te = self.tau_early(s)
        tl = self.tau_late(s)
        return te * eUe / (1 + eUe * te / tl)

    def Gp(self, s):
        """
        Integrand of the G'(w) function
        """
        sqrtau = self.tau(s)**2
        sqrw = self.w**2
        return (1 - s)**self.alpha * sqrw * sqrtau / (1 + sqrw * sqrtau)
    
    def Gpp(self, s):
        """
        Integrand of the G''(w) function
        """
        t = self.tau(s)
        sqrtau = t**2
        sqrw = self.w**2
        return (1 - s)**self.alpha * self.w * t / (1 + sqrw * sqrtau)

    def GppRouse(self, w):
        """
        G''(w) due to fast Rouse modes
        """
        return np.exp(-1 / w / self.Z**2 / self.tau_e) * np.sqrt(self.tau_e * w)
    
    def calculate(self, f=None):
        """DTDStars function that returns the square of y
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
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
        except ValueError:
            self.Qprint("Invalid Mw value")
            return
        
            
        self.Z = int(np.rint(Mw / self.Me))
        omega = ft.data[:, 0]

        tt.data[:, 0] = omega

        for i,w in enumerate(omega):
            self.w = w
            y, err = quad(self.Gp, 0, 1) 
            tt.data[i,1] = (1+self.alpha)*self.G0*y + self.G0*self.GppRouse(w)
            y, err = quad(self.Gpp, 0, 1)
            tt.data[i,2] = (1+self.alpha)*self.G0*y + self.G0*self.GppRouse(w)


class CLTheoryDTDStars(BaseTheoryDTDStars, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self,
                 name='ThDTDStars',
                 parent_dataset=None,
                 axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThDTDStars'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # This class usually stays empty


class GUITheoryDTDStars(BaseTheoryDTDStars, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self,
                 name='ThDTDStars',
                 parent_dataset=None,
                 axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThDTDStars'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # add widgets specific to the theory here:
