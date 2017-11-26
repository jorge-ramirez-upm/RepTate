# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module View

Module that defines the basic properties of a View, that will be used to represent
the data graphically.

""" 

class View(object):
    """Abstract class to describe a view"""

    def __init__(self, name="", description="", x_label="", y_label="", x_units="", y_units="", log_x=False, log_y=False, view_proc=None, n=1, snames=[]):
        """Constructor:
            
        Args:
            name            (str): View name
            description     (str): Description of view
            x_label         (str): X Axis label
            y_label         (str): Y Axis label
            x_units         (???): To be defined
            y_units         (???): To be defined
            log_x          (bool): X axis logarithmic?
            log_y          (bool): Y axis logarithmic?
            view_proc      (func): Function that creates the X, Y1, Y2 values of the view
            n               (int): Number of series that the view represents
            snames         (list): Names of the series represented by the view
        """
        self.name=name
        self.description=description
        self.x_label=x_label
        self.y_label=y_label
        self.x_units=x_units
        self.y_units=y_units
        self.log_x=log_x
        self.log_y=log_y
        self.view_proc=view_proc
        self.n=n
        self.snames=snames
