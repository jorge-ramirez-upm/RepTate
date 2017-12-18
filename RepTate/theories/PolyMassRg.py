# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Daniel Read, d.j.read@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module PolyMassRg
provides routines for cleaning up connectivity of branched polymers

"""
import numpy as np
from PolyBits import PolyBits

class PolyMassRg(PolyBits):

    def __init__(self):
        super().__init__()

    def mass_segs(self, first): #TODO: return values lentot, segtot, check all calls
        # var
        # next: integer
        lentot = self.arm_pool[first].arm_len
        segtot = 1
        next = self.arm_pool[first].down
        while next != first:
            lentot = lentot + self.arm_pool[next].arm_len
            segtot = segtot + 1
            next = self.arm_pool[next].down
            if next == 0:
                next = first
        return lentot, segtot

    def mass_rg1(self, m, cur_c):
    # TODO cur_c variable seems useless, remove it?
        # var
        # mc,m1,m2: integer
        # h1,h2,j1,j2,len1,len2,lenc,hc,jc: double
        mc = np.abs(m) # sign of m gives direction
        if mc == 0: # do not count current segment
            lentot = 0.0
            htot = 0.0
            jtot = 0.0
            return lentot, htot, jtot
        if m > 0: #positive direction
            m1 = self.arm_pool[mc].R1
            m2 = self.arm_pool[mc].R2
        else:
            m1 = self.arm_pool[mc].L1         
            m2 = self.arm_pool[mc].L2
        len1, h1, j1 = self.mass_rg1(m1, cur_c)
        len2, h2, j2 = self.mass_rg1(m2, cur_c)
        lenc = self.arm_pool[mc].arm_len
        hc = lenc/2.0
        jc = lenc/3.0
        lentot = lenc + len1 + len2
        htot = (lenc*hc + lenc*(len1 + len2) + len1*h1 + len2*h2)/lentot
        jtot = (lenc*lenc*jc + len1*len1*j1 + len2*len2*j2 + 2.0*(len1*len2*(h1 + h2) + len1*lenc*(h1 + hc) + len2*lenc*(h2 + hc)))/(lentot*lentot)
        return lentot, htot, jtot

    def mass_rg2(self, m, cur_c): #TODO: return values lentot, htot, jtot. check all calls
        # var
        # mc,m1,m2: integer
        # h1,h2,j1,j2,len1,len2,lenc,hc,jc: double
        mc = np.abs(m) #sign of m gives direction
        if mc == 0: #do not count current segment
            lentot = 0.0
            jtot = 0.0
            gfact = 0.0
            return lentot, jtot, gfact
        m1 = self.arm_pool[mc].L1
        m2 = self.arm_pool[mc].L2
        len1, h1, j1 = self.mass_rg1(m1, cur_c)
        len2, h2, j2 = self.mass_rg1(m2, cur_c)
        lenc, hc, jc = self.mass_rg1(mc, cur_c)
        lentot = lenc + len1 + len2
        jtot = (lenc*lenc*jc + len1*len1*j1 + len2*len2*j2 + 2.0*(len1*len2*(h1 + h2) + len1*lenc*(h1 + hc) + len2*lenc*(h2 + hc)))/(lentot*lentot)
        gfact = 3*jtot/lentot
        return lentot, jtot, gfact
    