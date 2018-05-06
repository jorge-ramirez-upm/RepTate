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
"""Module TheoryLikhtmanMcLeish2002

Module that defines the Likhtman-McLeish theory for melts of linear monodisperse entangled
polymers.

"""
from os.path import sep
import numpy as np
from scipy import interp
from CmdBase import CmdBase, CmdMode
from Theory import Theory
from QTheory import QTheory
from Parameter import Parameter, ParameterType, OptType


class TheoryLikhtmanMcLeish2002(CmdBase):
    """Fit Likhtman-McLeish theory for linear rheology of linear entangled polymers
    
    [description]
    """
    thname = "Likhtman-McLeish"
    description = "Fit Likhtman-McLeish theory for linear rheology of linear entangled polymers"
    citations = "Likhtman A.E. and McLeish T.C.B., Macromolecules 2002, 35, 6332-6343"

    def __new__(cls, name="", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUITheoryLikhtmanMcLeish2002(name, parent_dataset, ax) if (
            CmdBase.mode == CmdMode.GUI) else CLTheoryLikhtmanMcLeish2002(
                name, parent_dataset, ax)


class BaseTheoryLikhtmanMcLeish2002:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/en/latest/manual/Applications/LVE/Theory/LikhtmanMcLeish.html'
    single_file = False
    thname = TheoryLikhtmanMcLeish2002.thname
    citations = TheoryLikhtmanMcLeish2002.citations
    
    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.LikhtmanMcLeish2002

        self.parameters["taue"] = Parameter(
            "taue",
            2e-6,
            "Rouse time of one Entanglement",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0.0,
            max_value=np.inf)
        self.parameters["Ge"] = Parameter(
            "Ge",
            1e6,
            "Entanglement modulus",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0.0,
            max_value=np.inf)
        self.parameters["Me"] = Parameter(
            "Me",
            5,
            "Entanglement molecular weight",
            ParameterType.real,
            opt_type=OptType.opt,
            min_value=0.0,
            max_value=np.inf)
        self.parameters["cnu"] = Parameter(
            name="cnu",
            value=0.1,
            description="Constraint Release parameter",
            type=ParameterType.discrete_real,
            opt_type=OptType.const,
            discrete_values=[0, 0.01, 0.03, 0.1, 0.3, 1, 3, 10])

        f = np.load("theories" + sep + "linlin.npz")
        self.Zarray = f['Z']
        self.cnuarray = f['cnu']
        self.data = f['data']

        # Estimate initial values of the theory
        w = self.parent_dataset.files[0].data_table.data[:, 0]
        Gp = self.parent_dataset.files[0].data_table.data[:, 1]
        Gpp = self.parent_dataset.files[0].data_table.data[:, 2]

        Gpp_Gp = Gpp / Gp
        ind = len(Gpp_Gp) - np.argmax(np.flipud(Gpp_Gp) < 0.8)
        if (ind < len(w)):
            taue = 1.0 / w[ind]
            Ge = Gp[ind]
            self.set_param_value("taue", taue)
            self.set_param_value("Ge", Ge)

    def LikhtmanMcLeish2002(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        taue = self.parameters["taue"].value
        Ge = self.parameters["Ge"].value
        Me = self.parameters["Me"].value
        cnu = self.parameters["cnu"].value
        Mw = float(f.file_parameters["Mw"])

        indcnu = (np.where(self.cnuarray == cnu))[0][0]
        indcnu1 = 1 + indcnu * 2
        indcnu2 = indcnu1 + 1

        Z = Mw / Me
        if (Z < 3):
            # self.Qprint("WARNING: Mw of %s is too small"%(f.file_name_short))
            Z = 3
        if Z < self.Zarray[0]:
            indZ0 = 0
        else:
            indZ0 = (np.where(self.Zarray < Z))[0][-1]
        if Z > self.Zarray[-1]:
            indZ1 = len(self.Zarray) - 1
        else:
            indZ1 = (np.where(self.Zarray > Z))[0][0]
        table0 = self.data[indZ0]
        table1 = self.data[indZ1]

        vec = np.append(table0[:, 0], table1[:, 0])
        vec = np.sort(vec)
        vec = np.unique(vec)
        table = np.zeros((len(vec), 3))
        table[:, 0] = vec
        w1 = (Z - self.Zarray[indZ0]) / (
            self.Zarray[indZ1] - self.Zarray[indZ0])
        table[:, 1] = (1.0 - w1) * interp(
            vec, table0[:, 0], table0[:, indcnu1]) + w1 * interp(
                vec, table1[:, 0], table1[:, indcnu1])
        table[:, 2] = (1.0 - w1) * interp(
            vec, table0[:, 0], table0[:, indcnu2]) + w1 * interp(
                vec, table1[:, 0], table1[:, indcnu2])

        tt.data[:, 1] = interp(tt.data[:, 0], table[:, 0] / taue,
                               Ge * table[:, 1])
        tt.data[:, 2] = interp(tt.data[:, 0], table[:, 0] / taue,
                               Ge * table[:, 2])


class CLTheoryLikhtmanMcLeish2002(BaseTheoryLikhtmanMcLeish2002, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)


class GUITheoryLikhtmanMcLeish2002(BaseTheoryLikhtmanMcLeish2002, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
