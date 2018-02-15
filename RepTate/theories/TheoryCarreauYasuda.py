# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License.
"""Module TheoryCarreauYasuda

Carreau-Yasuda equation for the complex viscosity
"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable


class TheoryCarreauYasuda(CmdBase):
    """[summary]
    
    [description]
    """
    thname = 'CarreauYasudaTheory'
    description = 'Carreau-Yasuda Theory'
    citations = ''

    def __new__(cls, name='ThCarreauYasuda', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThCarreauYasuda'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryCarreauYasuda(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryCarreauYasuda(
                name, parent_dataset, ax)


class BaseTheoryCarreauYasuda:
    """[summary]
    
    [description]
    """
    single_file = False  # False if the theory can be applied to multiple files simultaneously

    def __init__(self, name='ThCarreauYasuda', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThCarreauYasuda'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.function_CarreauYasuda  # main theory function
        self.has_modes = False  # True if the theory has modes

        self.parameters['eta0'] = Parameter(
            name='eta0',
            value=1000,
            description='zero shear rate viscosity',
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters['etainf'] = Parameter(
            name='etainf',
            value=0,
            description='infinite shear rate viscosity',
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters['lambda'] = Parameter(
            name='lambda',
            value=100,
            description='characteristic time',
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters['n'] = Parameter(
            name='n',
            value=0.2,
            description='characteristic exponent',
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters['a'] = Parameter(
            name='a',
            value=1.0,
            description='exponent a',
            type=ParameterType.real,
            opt_type=OptType.opt)

        # Estimate initial values of fitting parameters
        w0 = self.parent_dataset.files[0].data_table.data[0, 0]
        Gp0 = self.parent_dataset.files[0].data_table.data[0, 1]
        Gpp0 = self.parent_dataset.files[0].data_table.data[0, 2]
        eta0 = np.sqrt(Gp0**2 + Gpp0**2) / w0
        self.set_param_value("eta0", eta0)

        winf = self.parent_dataset.files[0].data_table.data[-1, 0]
        Gpinf = self.parent_dataset.files[0].data_table.data[-1, 1]
        Gppinf = self.parent_dataset.files[0].data_table.data[-1, 2]
        etainf = np.sqrt(Gpinf**2 + Gppinf**2) / winf
        self.set_param_value("etainf", etainf)

        w = self.parent_dataset.files[0].data_table.data[:, 0]
        Gp = self.parent_dataset.files[0].data_table.data[:, 1]
        Gpp = self.parent_dataset.files[0].data_table.data[:, 2]
        etastar = np.sqrt(Gp**2 + Gpp**2) / w

        ind0 = np.argmax(etastar < 0.5 * eta0)
        ind1 = len(etastar) - np.argmax(np.flipud(etastar) > 2.0 * etainf)
        wa = w[ind0]
        wb = w[ind1]
        etaa = etastar[ind0]
        etab = etastar[ind1]
        n = (np.log10(etab) - np.log10(etaa)) / (
            np.log10(wb) - np.log10(wa)) + 1
        self.set_param_value("n", n)

        #eta = K*w^(n-1)
        # K = etaa/wa^(n-1)
        # eta0 = K*w0^(n-1) = etaa*(w0/wa)^(n-1)
        # w0 = (eta0/K)^(1/(n-1)) = wa*(eta0/etaa)^(1/(n-1))
        # lambda = 1/w0 = 1/wa*(etaa/eta0)^(1/(n-1))
        lamda = 1.0 / wa * np.power(etaa / eta0, 1.0 / (n - 1))
        self.set_param_value("lambda", lamda)

    def function_CarreauYasuda(self, f=None):
        """Carreau-Yasuda equation for the complex viscosity
        
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
        tt.data[:, 0] = ft.data[:, 0]

        eta0 = self.parameters["eta0"].value
        etainf = self.parameters["etainf"].value
        lamda = self.parameters["lambda"].value
        n = self.parameters["n"].value
        a = self.parameters["a"].value

        tt.data[:, 1] = tt.data[:, 2] = 1 / np.sqrt(2.0) * (etainf + (
            eta0 - etainf) * np.power(1.0 + np.power(lamda * tt.data[:, 0], a),
                                      (n - 1.0) / a)) * tt.data[:, 0]


class CLTheoryCarreauYasuda(BaseTheoryCarreauYasuda, Theory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='ThCarreauYasuda', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThCarreauYasuda'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)


class GUITheoryCarreauYasuda(BaseTheoryCarreauYasuda, QTheory):
    """[summary]
    
    [description]
    """

    def __init__(self, name='ThCarreauYasuda', parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {'ThCarreauYasuda'})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
