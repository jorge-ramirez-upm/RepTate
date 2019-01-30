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
"""Module ApplicationNLVE

Module for handling data from start up of shear and extensional flow experiments.

"""
from CmdBase import CmdBase, CmdMode
from Application import Application
from QApplicationWindow import QApplicationWindow
from View import View
from FileType import TXTColumnFile
import numpy as np


class ApplicationNLVE(CmdBase):
    """Application to Analyze Start up of Nonlinear flow
    
    """
    appname = "NLVE"
    description = "Non-Linear Flow"
    extension = "shear uext bext pext"

    def __new__(cls, name="NLVE", parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"NLVE"})
            - parent {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUIApplicationNLVE(
            name,
            parent) if (CmdBase.mode == CmdMode.GUI) else CLApplicationNLVE(
                name, parent)


class BaseApplicationNLVE:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/NLVE/NLVE.html'
    appname = ApplicationNLVE.appname

    def __init__(self, name="NLVE", parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"LVE"})
            - parent {[type]} -- [description] (default: {None})
        """
        from TheoryRoliePoly import TheoryRoliePoly
        from TheoryUCM import TheoryUCM
        from TheoryGiesekus import TheoryGiesekus
        from TheoryPomPom import TheoryPomPom
        from TheoryRolieDoublePoly import TheoryRolieDoublePoly
        from TheoryBobNLVE import TheoryBobNLVE
        from TheoryPETS import TheoryPETS
        from TheorySCCR import TheorySCCR
        # from TheorySCCROLD import TheorySCCROLD

        super().__init__(name, parent)

        # VIEWS
        self.views["log(eta(t))"] = View(
            name="log(eta(t))",
            description="log transient viscosity",
            x_label="log(t)",
            y_label="log($\eta^+$)",
            x_units="s",
            y_units="Pa$\cdot$s",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogeta,
            n=1,
            snames=["log(eta)"])
        self.views["eta(t)"] = View(
            name="eta(t)",
            description="transient viscosity",
            x_label="t",
            y_label="$\eta^+$",
            x_units="s",
            y_units="Pa$\cdot$s",
            log_x=True,
            log_y=True,
            view_proc=self.vieweta,
            n=1,
            snames=["eta"])            
        self.views["log(sigma(gamma))"] = View(
            name="log(sigma(gamma))",
            description="log transient shear stress vs gamma",
            x_label="log($\gamma$)",
            y_label="log($\sigma^+$)",
            x_units="-",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogSigmaGamma,
            n=1,
            snames=["log(sigma)"])
        self.views["sigma(gamma)"] = View(
            name="sigma(gamma)",
            description="transient shear stress vs gamma",
            x_label="$\gamma$",
            y_label="$\sigma^+$",
            x_units="-",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewSigmaGamma,
            n=1,
            snames=["sigma"])            
        self.views["log(sigma(t))"] = View(
            name="log(sigma(t))",
            description="log transient shear stress vs time",
            x_label="log(t)",
            y_label="log($\sigma^+$)",
            x_units="s",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogSigmaTime,
            n=1,
            snames=["log(sigma)"])
        self.views["sigma(t)"] = View(
            name="sigma(t)",
            description="transient shear stress vs time",
            x_label="t",
            y_label="$\sigma^+$",
            x_units="s",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewSigmaTime,
            n=1,
            snames=["sigma"])
        self.views["Flow Curve"] = View(
            name="Flow Curve",
            description="Steady state shear stress vs flow rate",
            x_label="Flow rate",
            y_label="$\sigma$",
            x_units="s$^{-1}$",
            y_units="Pa",
            log_x=True,
            log_y=True,
            view_proc=self.view_flowcurve,
            n=1,
            snames=["sigma"],
            with_thline=False,
            filled=True)
        self.views["Steady_eta"] = View(
            name="Steady eta",
            description="Steady state shear viscosity vs flow rate",
            x_label="Flow rate",
            y_label="$\eta$",
            x_units="s$^{-1}$",
            y_units="Pa$\cdot$s",
            log_x=True,
            log_y=True,
            view_proc=self.view_steadyeta,
            n=1,
            snames=["psi1"],
            with_thline=False,
            filled=True)
        self.views["log(psi1(t))"] = View(
            name="log(psi1(t))",
            description="log transient 1st normal stress coefficient",
            x_label="log(t)",
            y_label="log($\psi_1^+$)",
            x_units="s",
            y_units="Pa$\cdot$s",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogpsi1,
            n=1,
            snames=["log(psi1)"])
        self.views["psi1(t)"] = View(
            name="psi1(t)",
            description="transient 1st normal stress coefficient",
            x_label="t",
            y_label="$\psi_1^+$",
            x_units="s",
            y_units="Pa$\cdot$s",
            log_x=True,
            log_y=True,
            view_proc=self.viewpsi1,
            n=1,
            snames=["psi1"])            
        self.views["log(N1(gamma))"] = View(
            name="log(N1(gamma))",
            description="log transient 1st normal stress difference vs gamma",
            x_label="log($\gamma$)",
            y_label="log($N_1^+$)",
            x_units="-",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogN1Gamma,
            n=1,
            snames=["log(N1)"])
        self.views["N1(gamma)"] = View(
            name="N1(gamma)",
            description="transient 1st normal stress vs gamma",
            x_label="$\gamma$",
            y_label="$N_1^+$",
            x_units="-",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewN1Gamma,
            n=1,
            snames=["N1"])            
        self.views["log(N1(t))"] = View(
            name="log(N1(t))",
            description="log transient 1st normal stress vs time",
            x_label="log(t)",
            y_label="log($N_1^+$)",
            x_units="s",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogN1Time,
            n=1,
            snames=["log(N1)"])
        self.views["N1(t)"] = View(
            name="N(t)",
            description="transient 1st normal stress vs time",
            x_label="t",
            y_label="$N_1^+$",
            x_units="s",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewN1Time,
            n=1,
            snames=["N1"])
        self.views["Steady_psi1"] = View(
            name="Steady Psi1",
            description="Steady state 1st normal stress coeff vs flow rate",
            x_label="Flow rate",
            y_label="$\psi_1$",
            x_units="s$^{-1}$",
            y_units="Pa$\cdot$s",
            log_x=True,
            log_y=True,
            view_proc=self.view_steadypsi1,
            n=1,
            snames=["psi1"],
            with_thline=False,
            filled=True)
        self.views["log(psi2(t))"] = View(
            name="log(psi2(t))",
            description="log transient 2nd normal stress coefficient",
            x_label="log(t)",
            y_label="log($\psi_2^+$)",
            x_units="s",
            y_units="Pa$\cdot$s",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogpsi2,
            n=1,
            snames=["log(psi2)"])
        self.views["psi2(t)"] = View(
            name="psi2(t)",
            description="transient 2nd normal stress coefficient",
            x_label="t",
            y_label="$\psi_2^+$",
            x_units="s",
            y_units="Pa$\cdot$s",
            log_x=True,
            log_y=True,
            view_proc=self.viewpsi2,
            n=1,
            snames=["psi2"])            
        self.views["log(N2(gamma))"] = View(
            name="log(N2(gamma))",
            description="log transient 2nd normal stress difference vs gamma",
            x_label="log($\gamma$)",
            y_label="log($N_2^+$)",
            x_units="-",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogN2Gamma,
            n=1,
            snames=["log(N2)"])
        self.views["N2(gamma)"] = View(
            name="N2(gamma)",
            description="transient 2nd normal stress vs gamma",
            x_label="$\gamma$",
            y_label="$N_2^+$",
            x_units="-",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewN2Gamma,
            n=1,
            snames=["N2"])            
        self.views["log(N2(t))"] = View(
            name="log(N2(t))",
            description="log transient 2nd normal stress vs time",
            x_label="log(t)",
            y_label="log($N_2^+$)",
            x_units="s",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogN2Time,
            n=1,
            snames=["log(N2)"])
        self.views["N2(t)"] = View(
            name="N2(t)",
            description="transient 2nd normal stress vs time",
            x_label="t",
            y_label="$N_2^+$",
            x_units="s",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewN2Time,
            n=1,
            snames=["N2"])
        self.views["Steady_psi2"] = View(
            name="Steady Psi2",
            description="Steady state 2nd normal stress coeff vs flow rate",
            x_label="Flow rate",
            y_label="$\psi_2$",
            x_units="s$^{-1}$",
            y_units="Pa$\cdot$s",
            log_x=True,
            log_y=True,
            view_proc=self.view_steadypsi2,
            n=1,
            snames=["psi2"],
            with_thline=False,
            filled=True)

        #set multiviews
        self.nplots = 1
        self.multiviews = []
        for i in range(self.nplot_max):
            # set views in the same order as declared above
            self.multiviews.append(list(self.views.values())[i])
        self.multiplots.reorg_fig(self.nplots)

        # FILES
        ftype = TXTColumnFile("Start-up of shear flow", "shear",
                              "Shear flow files", ['t', 'sigma_xy', 'N1', 'N2'], ['gdot', 'T'],
                              ['s', 'Pa$\cdot$s', 'Pa$\cdot$s', 'Pa$\cdot$s'])
        self.filetypes[ftype.extension] = ftype
        ftype = TXTColumnFile("Uniaxial Elongation flow", "uext",
                              "Uniaxial Elongation flow files", ['t', 'sigma_xy', 'N1', 'N2'], ['gdot', 'T'],
                              ['s', 'Pa$\cdot$s', 'Pa$\cdot$s', 'Pa$\cdot$s'])
        self.filetypes[ftype.extension] = ftype
        ftype = TXTColumnFile("Biaxial Elongation flow", "bext",
                              "Biaxial Elongation flow files", ['t', 'sigma_xy', 'N1', 'N2'], ['gdot', 'T'],
                              ['s', 'Pa$\cdot$s', 'Pa$\cdot$s', 'Pa$\cdot$s'])
        self.filetypes[ftype.extension] = ftype
        ftype = TXTColumnFile("Planar Elongation flow", "pext",
                              "Planar Elongation flow files", ['t', 'sigma_xy', 'N1', 'N2'], ['gdot', 'T'],
                              ['s', 'Pa$\cdot$s', 'Pa$\cdot$s', 'Pa$\cdot$s'])
        self.filetypes[ftype.extension] = ftype

        # THEORIES
        self.theories[TheoryRoliePoly.thname] = TheoryRoliePoly
        self.theories[TheoryUCM.thname] = TheoryUCM
        self.theories[TheoryGiesekus.thname] = TheoryGiesekus
        self.theories[TheoryPomPom.thname] = TheoryPomPom
        self.theories[TheoryRolieDoublePoly.thname] = TheoryRolieDoublePoly
        self.theories[TheoryBobNLVE.thname] = TheoryBobNLVE
        self.theories[TheoryPETS.thname] = TheoryPETS
        self.theories[TheorySCCR.thname] = TheorySCCR
        # self.theories[TheorySCCROLD.thname] = TheorySCCROLD
        self.add_common_theories()
        
        #set the current view
        self.set_views()

    def viewLogeta(self, dt, file_parameters):
        """Logarithm of the transient shear or extensional viscosity (depending on the experiment) :math:`\\eta(t)` vs logarithm of time :math:`t`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        flow_rate = float(file_parameters["gdot"])
        y[:, 0] = np.log10(dt.data[:, 1] / flow_rate)
        return x, y, True
        
    def vieweta(self, dt, file_parameters):
        """Transient shear or extensional viscosity (depending on the experiment) :math:`\\eta(t)` vs time :math:`t` (both axes in logarithmic scale by default)
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        flow_rate = float(file_parameters["gdot"])
        y[:, 0] = dt.data[:, 1] / flow_rate
        return x, y, True

    def viewLogSigmaTime(self, dt, file_parameters):
        """Logarithm of the transient shear or extensional stress (depending on the experiment) :math:`\\sigma(t)` vs logarithm of time :math:`t`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 1])
        return x, y, True

    def viewSigmaTime(self, dt, file_parameters):
        """Transient shear or extensional stress (depending on the experiment) :math:`\\sigma(t)` vs time :math:`t`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True
        
    def viewLogSigmaGamma(self, dt, file_parameters):
        """Logarithm of the transient shear or extensional stress (depending on the experiment) :math:`\\sigma(t)` vs logarithm of the strain :math:`\\gamma`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        flow_rate = float(file_parameters["gdot"])
        x[:, 0] = np.log10(dt.data[:, 0] * flow_rate)  #compute strain
        y[:, 0] = np.log10(dt.data[:, 1])
        return x, y, True
        
    def viewSigmaGamma(self, dt, file_parameters):
        """Transient shear or extensional stress (depending on the experiment) :math:`\\sigma(t)` vs strain :math:`\\gamma`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        flow_rate = float(file_parameters["gdot"])
        x[:, 0] = dt.data[:, 0] * flow_rate  #compute strain
        y[:, 0] = dt.data[:, 1]
        return x, y, True
        
    def view_flowcurve(self, dt, file_parameters):
        """ :math:`\\sigma(t_{\\to\\infty})` vs flow rate
        """
        flow_rate = float(file_parameters["gdot"])
        x = np.zeros((1, 1))
        y = np.zeros((1, 1))
        x[0, 0] = flow_rate
        y[0, 0] = dt.data[-1,1]
        return x, y, True

    def view_steadyeta(self, dt, file_parameters):
        """ :math:`\\eta(t_{\\to\\infty})` vs flow rate
        """
        flow_rate = float(file_parameters["gdot"])
        x = np.zeros((1, 1))
        y = np.zeros((1, 1))
        x[0, 0] = flow_rate
        y[0, 0] = dt.data[-1,1]/flow_rate
        return x, y, True

    def viewLogpsi1(self, dt, file_parameters):
        """Logarithm of the transient 1st normal stress coefficient :math:`\\psi_1(t)` vs logarithm of time :math:`t`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        flow_rate = float(file_parameters["gdot"])
        y[:, 0] = np.log10(dt.data[:, 2] / flow_rate**2)
        return x, y, True
        
    def viewpsi1(self, dt, file_parameters):
        """Transient 1st normal stress coefficient :math:`\\psi_1(t)` vs time :math:`t` (both axes in logarithmic scale by default)
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        flow_rate = float(file_parameters["gdot"])
        y[:, 0] = dt.data[:, 2] / flow_rate**2
        return x, y, True
        
    def viewLogN1Time(self, dt, file_parameters):
        """Logarithm of the 1st normal stress difference :math:`N_1(t)` vs logarithm of time :math:`t`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 2])
        return x, y, True

    def viewN1Time(self, dt, file_parameters):
        """Transient 1st normal stress difference :math:`N_1(t)` vs time :math:`t`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 2]
        return x, y, True
        
    def viewLogN1Gamma(self, dt, file_parameters):
        """Logarithm of the 1st normal stress difference :math:`N_1(t)` vs logarithm of the strain :math:`\\gamma`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        flow_rate = float(file_parameters["gdot"])
        x[:, 0] = np.log10(dt.data[:, 0] * flow_rate)  #compute strain
        y[:, 0] = np.log10(dt.data[:, 2])
        return x, y, True
        
    def viewN1Gamma(self, dt, file_parameters):
        """Transient 1st normal stress difference (depending on the experiment) :math:`N_1(t)` vs strain :math:`\\gamma`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        flow_rate = float(file_parameters["gdot"])
        x[:, 0] = dt.data[:, 0] * flow_rate  #compute strain
        y[:, 0] = dt.data[:, 2]
        return x, y, True

    def view_steadypsi1(self, dt, file_parameters):
        """ :math:`\\psi_1(t_{\\to\\infty})` vs flow rate
        """
        flow_rate = float(file_parameters["gdot"])
        x = np.zeros((1, 1))
        y = np.zeros((1, 1))
        x[0, 0] = flow_rate
        y[0, 0] = dt.data[-1,2]/flow_rate
        return x, y, True

    def viewLogpsi2(self, dt, file_parameters):
        """Logarithm of the 2nd normal stress coefficient :math:`\\psi_2(t)` vs logarithm of time :math:`t`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        flow_rate = float(file_parameters["gdot"])
        y[:, 0] = np.log10(dt.data[:, 3] / flow_rate)
        return x, y, True
        
    def viewpsi2(self, dt, file_parameters):
        """Transient 2nd normal stress coefficient :math:`\\psi_2(t)` vs time :math:`t` (both axes in logarithmic scale by default)
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        flow_rate = float(file_parameters["gdot"])
        y[:, 0] = dt.data[:, 3] / flow_rate
        return x, y, True
        
    def viewLogN2Time(self, dt, file_parameters):
        """Logarithm of the 2nd normal stress (depending on the experiment) :math:`N_2(t)` vs logarithm of time :math:`t`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 3])
        return x, y, True

    def viewN2Time(self, dt, file_parameters):
        """Transient 2nd normal stress difference :math:`N_2(t)` vs time :math:`t`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 3]
        return x, y, True
        
    def viewLogN2Gamma(self, dt, file_parameters):
        """Logarithm of the 2nd normal stress difference :math:`N_2(t)` vs logarithm of the strain :math:`\\gamma`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        flow_rate = float(file_parameters["gdot"])
        x[:, 0] = np.log10(dt.data[:, 0] * flow_rate)  #compute strain
        y[:, 0] = np.log10(dt.data[:, 3])
        return x, y, True
        
    def viewN2Gamma(self, dt, file_parameters):
        """Transient 2nd normal stress difference :math:`N_2(t)` vs strain :math:`\\gamma`
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        flow_rate = float(file_parameters["gdot"])
        x[:, 0] = dt.data[:, 0] * flow_rate  #compute strain
        y[:, 0] = dt.data[:, 3]
        return x, y, True

    def view_steadypsi2(self, dt, file_parameters):
        """ :math:`\\psi_2(t_{\\to\\infty})` vs flow rate
        """
        flow_rate = float(file_parameters["gdot"])
        x = np.zeros((1, 1))
        y = np.zeros((1, 1))
        x[0, 0] = flow_rate
        y[0, 0] = dt.data[-1,3]/flow_rate
        return x, y, True

class CLApplicationNLVE(BaseApplicationNLVE, Application):
    """[summary]
    
    [description]
    """

    def __init__(self, name="NLVE", parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"LVE"})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)


class GUIApplicationNLVE(BaseApplicationNLVE, QApplicationWindow):
    """[summary]
    
    [description]
    """

    def __init__(self, name="NLVE", parent=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"LVE"})
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)
