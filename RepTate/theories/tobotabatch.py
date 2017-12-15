# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Daniel Read, d.j.read@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module tobitabatch

"""
import random
from Polybits import Polybits


class Tobitabatch(Polybits):
    tobbatchnumber = 1

    def __init__(self):
        pass

    def tobbatchstart(self, pfin_conv, ptau, pbeta, pCs, pCb, n):
        self.bobinit(n) #TODO does this aims at modifying n?
        random.seed() #seed based on current time
        self.iy3 = -random.randrange(1000)

        # passed variables
        self.fin_conv = pfin_conv
        self.tau = ptau
        self.beta = pbeta
        self.Cs = pCs
        self.Cb = pCb

        self.tobitabatcherrorflag = False

    def tobbatch(self, n, n1):
        # var
        # cur_conv, seg_len, len1,len2,jtot, gfact :double;
        # m,m1,first, anum, nsegs :integer;

        self.scount = 0
        self.bcount = 0
        self.getconv1(self.fin_con, cur_conv) #TODO return value
        m, success = self.request_arm()
        if success:  #don't do anything if arms not available
            self.br_poly[n].first_end = m
            self.arm_pool[m].up = m 
            self.arm_pool[m].down = m
            self.calclength(cur_conv, seg_len)# TODO return value
            self.arm_pool[m].arm_len = seg_len
            self.arm_pool[m].arm_conv = cur_conv
            self.rlevel = 0
            self.tobita_grow(1, m, cur_conv, True)
        
        m1, success = self.request_arm()
        if success: #don't do anything if arms not available
            self.arm_pool[m].L1 = -m1
            self.arm_pool[m1].R2 = m
            self.armupdown(m, m1)
            self.calclength(cur_conv, seg_len) #TODO return value
            self.arm_pool[m1].arm_len = seg_len
            self.arm_pool[m1].arm_conv = cur_conv
            self.rlevel = 0
            self.tobita_grow(-1, m1, cur_conv, True) #end check for arm availability

        if self.arms_avail: # not true if we ran out of arms somewhere !
            self.polyclean(n)
            
            #renumber segments starting from zero
            m1 = self.br_poly[n].first_end
            first = m1
            anum = 0
            self.arm_pool[m1].armnum = anum
            m1 = self.arm_pool[m1].down
            while m1 != first:
                anum += 1
                self.arm_pool[m1].armnum = anum
                m1 = self.arm_pool[m1].down
            first = self.br_poly[n].first_end
            self.mass_segs(first, len1, nsegs) #TODO return value
            self.br_poly[n].num_br = bcount
            self.br_poly[n].tot_len = len1
            self.mass_rg2(first, 1.0, len2, jtot, gfact) #TODO return value
            self.br_poly[n].gfactor = gfact

            #check to see whether to save the polymer
            self.bobcount(n, n1)  #TODO return value??
            return True
        else:
            return False