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
"""Module TheoryDebye

Debye theory for neutron scattering from ideal polymer chains
"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices


class TheoryDebye(CmdBase):
    """Fit a Debye function to the small angle neutron scattering data of ideal polymer chains. 
    
    * **Function**
        .. math::
            I(q) = \\frac {(b_H-b_D)^2}{V} N \\phi(1-\\phi) g_D(R_g,q) + \\mathrm{Bckgrnd}
        
        where:
          - :math:`N=M_w/M_\\mathrm{mono}` is the degree of polymerization of the chain (:math:`M_w` is a parameter of the experimental data)
          - :math:`\\phi` is the volume fraction of deuterated chains (read from the file)
          - :math:`g_D(R_g,q)` is the Debye function, given by
          
          .. math::
              g_D(R_g,q) = \\frac{2}{(q^2R_g^2)^2}\\left( q^2R_g^2 + exp(-q^2R_g^2) -1 \\right)
    
    * **Parameters**
       - Contrast: This sets the magnitude of the scattering and is equal to :math:`(b_H-b_D)^2/V` where :math:`b_{H/D}` is the scattering cross-section of the hydrogenous/deuterated monomer and :math:`V` is the monomer volume. 
       - :math:`C_{gyr}`: This sets the scale of the radius of gyration of the chain. For a given molecular weight, the radius of gyration is :math:`R_g^2=C_{gyr}M_w`. For many polymers, this value is available in the literature, but small adjustments may still be necessary to optimize the agreement with the experimental data.
       - :math:`M_\\mathrm{mono}`: The molecular weight of a single monomer (should be known from the chain chemistry).
       - Bckgrnd: This sets the level of the background scattering. It can, in principle, be computed from known incoherent scattering cross sections but, in practice, there are often many other unknown contributions and therefore fitting is necessary.
       - :math:`\\lambda`: It applies a simple strain measure by shifting the radius of gyration by a constant factor for all :math:`q` values, :math:`R_g\\to \\lambda R_g` (the **Stretched** button must be checked). This can be used to compare the microscopic deformation with the effect of a fully affine bulk deformation or to fit to the low :math:`q` data to produce an effective radius of gyration under flow. Compression perpendicular to the flow direction can be modelled by setting :math:`\\lambda<1`.
       - :math:`\\chi`: Parameter to model the effect of a weak interaction between the hydrogenous and the deuterated monomers on the scattering, modelled within the random phase approximation [3] (the **Non-Ideal Mix** button must be checked). The scattered intensity is calculated according to the function below, in which :math:`\\chi` is independent of :math:`M_w` and :math:`\\phi` but is expected to change with temperature. Typically, the effect of :math:`\\chi` is small, but this depends upon the temperature, degree of polymerization and deuterated fraction. For deuterated/hydrogenated polystyrene :math:`\\chi\\approx 1.7\cdot 10^{-4}` at 160 degrees C, and it is expected to be smaller with increasing temperature.
         
         .. math::
             I(q) = \\frac {(b_H-b_D)^2}{V} \\left( \\frac{1}{N \\phi(1-\\phi) g_D(R_g,q)}-2\\chi \\right)^{-1} + \\mathrm{Bckgrnd}     
    
    """
    thname = 'Debye'
    description = 'Debye theory for neutron scattering from ideal polymer chains'
    citations = ['Debye P., J. Phys. Chem. 1947, 51, 18-32']
    doi = ["http://dx.doi.org/10.1021/j150451a002"]

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
        return GUITheoryDebye(
            name, parent_dataset,
            axarr) if (CmdBase.mode == CmdMode.GUI) else CLTheoryDebye(
                name, parent_dataset, axarr)


class BaseTheoryDebye:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/SANS/Theory/theory.html#debye-function'
    single_file = False  # False if the theory can be applied to multiple files simultaneously
    thname = TheoryDebye.thname
    citations = TheoryDebye.citations
    doi = TheoryDebye.doi

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculateDebye  # main theory function
        self.has_modes = False  # True if the theory has modes
        self.parameters['Contrast'] = Parameter(
            name='Contrast',
            value=0.4203,
            description='Magnitude of the scattering',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['C_gyr'] = Parameter(
            name='C_gyr',
            value=62.3,
            description='Scale the radius of gyration',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['M_mono'] = Parameter(
            name='M_mono',
            value=0.104,
            description='Molecular weight of a monomer',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['Bckgrnd'] = Parameter(
            name='Bckgrnd',
            value=0.26,
            description='Level of background scattering',
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters['Chi'] = Parameter(
            name='Chi',
            value=1E-4,
            description='Effect of weak interaction between "<sup>2</sup>H and H"',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters['Lambda'] = Parameter(
            name='Lambda',
            value=1,
            description='Shift of the radius of gyration',
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters["stretched"] = Parameter(
            name="stretched",
            value=False,
            description="Is shifting the radius of gyration applied",
            type=ParameterType.boolean,
            opt_type=OptType.const,
            display_flag=False)
        self.parameters["non-ideal"] = Parameter(
            name="non-ideal",
            value=False,
            description="Is non-ideal mix",
            type=ParameterType.boolean,
            opt_type=OptType.const,
            display_flag=False)

    def calculateDebye(self, f=None):
        """Debye function that returns the square of y
        
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

        try:
            Mw = float(f.file_parameters["Mw"])
            Phi = float(f.file_parameters["Phi"])
        except (ValueError, KeyError):
            self.Qprint("Invalid Mw or Phi value")
            return

        Contr = self.parameters["Contrast"].value
        CRg = self.parameters["C_gyr"].value
        Mmono = self.parameters["M_mono"].value
        Bck = self.parameters["Bckgrnd"].value
        Chi = self.parameters["Chi"].value
        Lambda = self.parameters["Lambda"].value
        stretched = self.parameters["stretched"].value
        nonideal = self.parameters["non-ideal"].value

        tt.data[:, 0] = ft.data[:, 0]

        Rg = np.sqrt(CRg * Mw)
        if (stretched):
            Rg *= Lambda
        RgQsq = Rg * Rg * ft.data[:, 0] * ft.data[:, 0]
        debFn = 2.0 / RgQsq / RgQsq * (RgQsq + np.exp(-RgQsq) - 1.0)
        if (nonideal):
            tt.data[:, 1] = Contr * 1 / (1 /
                                         (Mw / Mmono * Phi *
                                          (1.0 - Phi) * debFn) - 2 * Chi) + Bck
        else:
            tt.data[:,
                    1] = Contr * Mw / Mmono * Phi * (1.0 - Phi) * debFn + Bck

    def do_error(self, line):
        super().do_error(line)
        if (line == ""):
            self.Qprint("")
            self.Qprint("%12s %8s %8s" % ("File", "Mw", "Rg"))
            CRg = self.parameters["C_gyr"].value
            Lambda = self.parameters["Lambda"].value
            stretched = self.parameters["stretched"].value
            nfiles = len(self.parent_dataset.files)
            for i in range(nfiles):
                f = self.parent_dataset.files[i]
                if (f.active):
                    Mw = float(f.file_parameters["Mw"])
                    if (stretched):
                        self.Qprint("%12s %8.4g %8.4g" %
                                    (f.file_name_short, Mw,
                                     Lambda * np.sqrt(CRg * Mw)))
                    else:
                        self.Qprint("%12s %8.4g %8.4g" %
                                    (f.file_name_short, Mw, np.sqrt(CRg * Mw)))


class CLTheoryDebye(BaseTheoryDebye, Theory):
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


class GUITheoryDebye(BaseTheoryDebye, QTheory):
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
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        self.tbutstretched = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-socks.png'), 'Stretched')
        self.tbutstretched.setCheckable(True)
        self.tbutstretched.setChecked(False)
        self.tbutnonideal = tb.addAction(
            QIcon(':/Images/Images/new_icons/icons8-broom.png'),
            'Non-Ideal Mix')
        self.tbutnonideal.setCheckable(True)
        self.tbutnonideal.setChecked(False)
        self.thToolsLayout.insertWidget(0, tb)

        #connections signal and slots
        connection_id = self.tbutstretched.triggered.connect(
            self.handle_tbutstretched_triggered)
        connection_id = self.tbutnonideal.triggered.connect(
            self.handle_tbutnonideal_triggered)

    def handle_tbutstretched_triggered(self, checked):
        """[summary]
        
        [description]
        """
        self.set_param_value("stretched", checked)

    def handle_tbutnonideal_triggered(self, checked):
        """[summary]
        
        [description]
        """
        self.set_param_value("non-ideal", checked)
