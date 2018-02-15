# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License.
"""Module Application_frs

Module for handling FRS experiments and simulations.

"""
from Application import Application


class ApplicationFRS_I(Application):
    """Application to FRS Intensity simulations
    
    [description]
    """
    name = "FRS_I"
    description = "FRS Intensity"

    def __init__(self, name="FRS_I", parent=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"FRS_I"})
            parent {[type]} -- [description] (default: {None})
        """
        super(ApplicationFRS_I, self).__init__(name, parent)

        # VIEWS
        self.views["I(t)"] = View(
            name="I(t)",
            description="FRS Intensity decay",
            x_label="t",
            y_label="I(t)",
            x_units="s",
            y_units="-",
            log_x=True,
            log_y=True,
            view_proc=self.viewIt,
            n=1,
            snames=["I(t)"])
        self.views["log[I(t)]"] = View(
            name="log[I(t)]",
            description="log FRS Intensity decay",
            x_label="log(t)",
            y_label="log(I(t))",
            x_units="s",
            y_units="-",
            log_x=False,
            log_y=False,
            view_proc=self.viewLogIt,
            n=1,
            snames=["log(I(t))"])

        #set multiviews
        self.multiviews = [self.views['I(t)']]
        self.nplots = len(self.multiviews)

        # FILES
        ftype = TXTColumnFile("I(t) FRS files", "FRS_INTENSITY",
                              "I(t) decay from FRS", ['t', 'I'],
                              ['d', 'Na', 'ka', 'Ns', 'ka', 'Keq', 'beta'],
                              ['s', 'Pa'])
        self.filetypes[ftype.extension] = ftype

        #Theories
        self.add_common_theories()

    def viewIt(self, dt, file_parameters):
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
        y[:, 0] = dt.data[:, 1]
        return x, y, True

    def viewLogIt(self, dt, file_parameters):
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
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 1])
        return x, y, True
