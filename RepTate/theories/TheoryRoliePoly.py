from Theory import *
import numpy as np

class TheoryRoliePoly(Theory, CmdBase):
    """Rolie-Poly"""
    thname="RoliePoly"
    description="RoliePoly"

    def __init__(self, name="ThRoliePoly", parent_dataset=None, ax=None):
        super(TheoryRoliePoly, self).__init__(name, parent_dataset, ax)
        self.thtype = TheoryType.line
        self.line_function = self.RoliePoly
        self.citations="Likhtman, A.E. & Graham, R.S. \
        Simple constitutive equation for linear polymer melts derived from molecular theory: Rolie-Poly equation \
        J. Non-Newtonian Fluid Mech., 2003, 114, 1-12"
        self.parameters["beta"]=0.0
        self.parameters["delta"]=-0.5
        self.parameters["lmax"]=10
        self.parameters["tauR"]=0.5



