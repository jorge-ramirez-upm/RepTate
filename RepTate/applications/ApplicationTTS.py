# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License.
"""Module ApplicationTTS

Module for handling small angle oscillatory shear experiments and applying the
time-temperature superposition principle.

"""
from CmdBase import CmdBase, CmdMode
from Application import Application
from QApplicationWindow import QApplicationWindow
from View import View
from FileType import TXTColumnFile
import numpy as np


class ApplicationTTS(CmdBase):
    """Application to Analyze Linear Viscoelastic Data

    [description]
    """
    name = "TTS"
    description = "Linear Viscoelasticity"
    extension = 'osc'

    def __new__(cls, name="TTS", parent=None):
        """[summary]

        [description]

        Keyword Arguments:
            name {[type]} -- [description] (default: {"TTS"})
            parent {[type]} -- [description] (default: {None})

        Returns:
            [type] -- [description]
        """
        if CmdBase.mode == CmdMode.GUI:
            return GUIApplicationTTS(name, parent)
        else:
            return CLApplicationTTS(name, parent)


class BaseApplicationTTS:
    """[summary]

    [description]
    """

    def __init__(self, name="TTS", parent=None):
        """[summary]

        [description]

        Keyword Arguments:
            name {[type]} -- [description] (default: {"TTS"})
            parent {[type]} -- [description] (default: {None})
        """
        from TheoryTTS import TheoryWLFShift
        from TheoryTTS_Test import TheoryWLFShiftTest
        from TheoryTTS_Automatic import TheoryTTSShiftAutomatic
        super().__init__(name, parent)

        # VIEWS
        self.views["log(G',G''(w))"] = View(
            name="log(G',G''(w))",
            description="log Storage,Loss moduli",
            x_label="log($\omega$)",
            y_label="log(G'($\omega$),G''($\omega$))",
            x_units="rad/s",
            y_units="Pa",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogG1G2,
            n=2,
            snames=["G'(w)", "G''(w)"],
            index=0)
        self.views["G',G''(w)"] = View(
            "G',G''(w)",
            "Storage,Loss moduli",
            "$\omega$",
            "G'($\omega$),G''($\omega$)",
            "rad/s",
            "Pa",
            True,
            True,
            self.viewG1G2,
            2, ["G'(w)", "G''(w)"],
            index=1)
        self.views["etastar"] = View(
            "etastar",
            "Complex Viscosity",
            "$\omega$",
            "$|\eta^*(\omega)|$",
            "rad/s",
            "Pa.s",
            True,
            True,
            self.viewEtaStar,
            1, ["eta*(w)"],
            index=2)
        self.views["delta"] = View(
            "delta",
            "delta",
            "$\omega$",
            "$\delta(\omega)$",
            "rad/s",
            "-",
            True,
            True,
            self.viewDelta,
            1, ["delta(w)"],
            index=3)
        self.views["tan(delta)"] = View(
            "tan(delta)",
            "tan(delta)",
            "$\omega$",
            "tan($\delta$)",
            "rad/s",
            "-",
            True,
            True,
            self.viewTanDelta,
            1, ["tan(delta((w))"],
            index=4)

        #set multiviews
        self.multiviews = [
            self.views["log(G',G''(w))"]
        ]  #default view order in multiplot views, set only one item for single view
        self.nplots = len(self.multiviews)

        # FILES
        ftype = TXTColumnFile(
            "OSC files", "osc",
            "Small-angle oscillatory masurements from the Rheometer",
            ['w', 'G\'', 'G\'\''], ['Mw', 'T'], ['rad/s', 'Pa', 'Pa'])
        self.filetypes[ftype.extension] = ftype

        # THEORIES
        self.theories[TheoryTTSShiftAutomatic.thname] = TheoryTTSShiftAutomatic
        self.theories[TheoryWLFShift.thname] = TheoryWLFShift
        self.theories[TheoryWLFShiftTest.thname] = TheoryWLFShiftTest

        #set the current view
        self.set_views()

    def viewLogG1G2(self, dt, file_parameters):
        """[summary]

        [description]
        
        Arguments:
            dt {[type]} -- [description]
            file_parameters {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = np.log10(dt.data[:, 0])
        x[:, 1] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 1])
        y[:, 1] = np.log10(dt.data[:, 2])
        return x, y, True

    def viewG1G2(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            dt {[type]} -- [description]
            file_parameters {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = dt.data[:, 0]
        x[:, 1] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        y[:, 1] = dt.data[:, 2]
        return x, y, True

    def viewEtaStar(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            dt {[type]} -- [description]
            file_parameters {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = np.sqrt(dt.data[:, 1]**2 + dt.data[:, 2]**2) / dt.data[:, 0]
        return x, y, True

    def viewDelta(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            dt {[type]} -- [description]
            file_parameters {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = np.arctan2(dt.data[:, 2], dt.data[:, 1]) * 180 / np.pi
        return x, y, True

    def viewTanDelta(self, dt, file_parameters):
        """[summary]
        
        [description]
        
        Arguments:
            dt {[type]} -- [description]
            file_parameters {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 2] / dt.data[:, 1]
        return x, y, True


class CLApplicationTTS(BaseApplicationTTS, Application):
    """[summary]
    
    [description]
    """

    def __init__(self, name="TTS", parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"TTS"})
            parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)


class GUIApplicationTTS(BaseApplicationTTS, QApplicationWindow):
    """[summary]
    
    [description]
    """

    def __init__(self, name="TTS", parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"TTS"})
            parent {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent)
