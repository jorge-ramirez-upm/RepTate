# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Daniel Read, d.j.read@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module TobitaBatch

"""
import numpy as np
#np.random.random() uses the Mersenne Twister pseudorandom number generator 
from Polybits import Polybits
from PolyMassRg import PolyMassRg
from PolyCleanUp import PolyCleanUp
from BinsAndBob import BinsAndBob


class TobitaBatch(BinsAndBob, PolyMassRg, PolyCleanUp, Polybits):
    """
    Routines for making one LDPE polymer using the tobita batch algorithm
    """
    tobbatchnumber = 1
    #private variables used by this Class
    # var
    # scount, bcount, rlevel : integer
    # fin_conv, tau, beta, Cs, Cb : double
    def __init__(self):
        pass

    def tobbatchstart(self, pfin_conv, ptau, pbeta, pCs, pCb, n):
        self.bobinit(n) #OK: does not modify n
        np.random.seed() # random seed

        # passed variables
        self.fin_conv = pfin_conv
        self.tau = ptau
        self.beta = pbeta
        self.Cs = pCs
        self.Cb = pCb

        self.tobitabatcherrorflag = False

    def tobbatch(self, n, n1):
        # var
        # cur_conv, seg_len, len1,len2,jtot, gfact :double
        # m,m1,first, anum, nsegs :integer

        self.scount = 0
        self.bcount = 0
        cur_conv = self.getconv1(self.fin_con) 
        m, success = self.request_arm()
        if success:  #don't do anything if arms not available
            self.br_poly[n].first_end = m
            self.arm_pool[m].up = m
            self.arm_pool[m].down = m
            seg_len = self.calclength(cur_conv)
            self.arm_pool[m].arm_len = seg_len
            self.arm_pool[m].arm_conv = cur_conv
            self.rlevel = 0
            self.tobita_grow(1, m, cur_conv, True)

        m1, success = self.request_arm()
        if success: #don't do anything if arms not available
            self.arm_pool[m].L1 = -m1
            self.arm_pool[m1].R2 = m
            self.armupdown(m, m1)
            seg_len = self.calclength(cur_conv) 
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
            len1, nsegs = self.mass_segs(first)
            self.br_poly[n].num_br = self.bcount
            self.br_poly[n].tot_len = len1
            len2, jtot, gfact = self.mass_rg2(first, 1.0)
            self.br_poly[n].gfactor = gfact

            #check to see whether to save the polymer
            self.bobcount(n, n1)  #OK: do not change n, n1
            return True
        else:
            return False


    def tobita_grow(self, dir, m, cur_conv, sc_tag):
        """dir,m:integer cur_conv: double sc_tag: boolean"""
        # var
        # m1,m2 :integer
        # seg_len,new_conv,rnd :double
        # sigma,lambd,pref,Psigma,Plambd,Pbeta :double

        self.rlevel += 1  #recursion level
        if (self.rlevel > 5000) or self.tobitabatcherrorflag:
            #  need to decide what to do if you make molecules too big
            self.tobitabatcherrorflag = True
            self.rlevel = 100000
            return

        if not self.arms_avail:   # don't do anything if arms aren't available
            return

        seg_len = self.scilength(cur_conv)
        if sc_tag and (seg_len < self.arm_pool[m].arm_len):
            self.arm_pool[m].arm_len = seg_len   # scission event
            self.arm_pool[m].scission = True
        seg_len = self.brlength(cur_conv)

        if seg_len < self.arm_pool[m].arm_len: # a branch point
            self.bcount += 1
            m1, success = self.request_arm() # return success=False if arms not available
            if success: 
                self.armupdown(m, m1)
                m2, success = self.request_arm()
                if success:
                    self.armupdown(m,m2)
                    if (dir > 0): #going to the right
                        self.arm_pool[m].R1 = m1
                        self.arm_pool[m1].L2 = -m    #I think it might be useful if
                                                      #1 is connected to 2 all the time
                                                      # sign(L1) etc indicates direction of subsequent segment.
                        self.arm_pool[m1].arm_len = self.arm_pool[m].arm_len - seg_len
                        self.arm_pool[m].arm_len = seg_len
                        self.arm_pool[m1].arm_conv = cur_conv
                        self.arm_pool[m1].scission = self.arm_pool[m].scission
                        self.arm_pool[m].scission = False
                        new_conv = self.getconv2(cur_conv)
                        seg_len = self.calclength(new_conv)
                        self.arm_pool[m2].arm_len = seg_len
                        self.arm_pool[m2].arm_conv = new_conv
                        self.arm_pool[m1].L1 = m2
                        self.arm_pool[m2].L2 = m1
                        self.arm_pool[m].R2 = m2
                        self.arm_pool[m2].L1 = -m
                        self.tobita_grow(1, m2, new_conv, True)
                        self.tobita_grow(dir, m1, cur_conv, False)
                    else:  #going to the left
                        self.arm_pool[m].L1 = -m1
                        self.arm_pool[m1].R2 = m
                        self.arm_pool[m1].arm_len = self.arm_pool[m].arm_len - seg_len
                        self.arm_pool[m].arm_len = seg_len
                        self.arm_pool[m1].arm_conv = cur_conv
                        self.arm_pool[m1].scission = self.arm_pool[m].scission
                        self.arm_pool[m].scission = False
                        new_conv = self.getconv2(cur_conv)
                        seg_len = self.calclength(new_conv)
                        self.arm_pool[m2].arm_len = seg_len
                        self.arm_pool[m2].arm_conv = new_conv
                        self.arm_pool[m1].R1 = m2
                        self.arm_pool[m2].L2 = -m1
                        self.arm_pool[m].L2 = m2
                        self.arm_pool[m2].L1 = m
                        self.tobita_grow(1, m2, new_conv, True)
                        self.tobita_grow(dir, m1, cur_conv, False)
                    # end of arm m2 available
                # end of arm m1 available
            # end of it's a branchpoint
        else: # non side-branching condition - deal with end of chain
            if self.arm_pool[m].scission: # the end of the chain is a scission point
                if np.random.random() < 0.50: # and there is more growth at the scission point
                    new_conv = self.getconv2(cur_conv)
                    m1, success = self.request_arm() # success=False if arm not available
                    if success: 
                        self.armupdown(m, m1)
                        seg_len = self.calclength(new_conv)
                        self.arm_pool[m1].arm_len = seg_len
                        self.arm_pool[m1].arm_conv = new_conv
                        if dir > 0:
                            self.arm_pool[m].R1 = m1
                            self.arm_pool[m1].L2 = -m
                        else:
                            self.arm_pool[m].L1 = m1
                            self.arm_pool[m1].L2 = m
                        self.tobita_grow(1, m1, new_conv, True)
                    # end check for arm available
                # end of more growth from scission point
            # end of scission at chain end
            # chain end possibilities depend on the direction
            elif dir > 0:  #  growing to the right
                sigma = self.Cs * cur_conv / (1.0 - cur_conv) # calculate scission event population
                lambd = self.Cb * cur_conv / (1.0 - cur_conv)  # calculate branching population
                pref = self.tau + self.beta + sigma + lambd
                Pbeta = self.beta/pref         # prob termination by combination
                rnd = np.random.random()
                if rnd < Pbeta: #prob for termination by combination
                    m1, success = self.request_arm() # success=False if arm not available
                    if success:
                        self.armupdown(m, m1)
                        seg_len = self.calclength(cur_conv)
                        self.arm_pool[m1].arm_len = seg_len
                        self.arm_pool[m1].arm_conv = cur_conv
                        self.arm_pool[m].R1 = -m1
                        self.arm_pool[m1].R2 = -m
                        self.tobita_grow(-1, m1, cur_conv, True)
                    # end self.request_arm check
                # otherwise, end of chain: do nothing
            # end of right growth
            else: # must be left growth
                sigma = self.Cs * cur_conv / (1.0 - cur_conv) # calculate scission event population
                lambd = self.Cb * cur_conv / (1.0 - cur_conv)  # calculate branching population
                pref = self.tau + self.beta + sigma + lambd
                Plambd = lambd/pref     # prob reaction from polymer transfer (branching)
                Psigma = sigma/pref # prob reaction from scission site
                rnd = np.random.random()
                if rnd < Plambd: # grew from a branch
                    self.bcount += 1
                    new_conv = self.getconv1(cur_conv)
                    m1, success = self.request_arm()
                    if success: # check arm availability
                        self.armupdown(m, m1)
                        m2, success = self.request_arm()
                        if success:
                            self.armupdown(m, m2)
                            seg_len = self.calclength(new_conv)
                            self.arm_pool[m1].arm_len = seg_len
                            self.arm_pool[m1].arm_conv = new_conv
                            self.arm_pool[m].L1 = m1
                            self.arm_pool[m1].L2 = m
                            self.tobita_grow(1, m1, new_conv, True)
                            seg_len = self.calclength(new_conv)
                            self.arm_pool[m2].arm_len = seg_len
                            self.arm_pool[m2].arm_conv = new_conv
                            self.arm_pool[m].L2 = -m2
                            self.arm_pool[m2].R1 = m
                            self.arm_pool[m1].L1 = -m2
                            self.arm_pool[m2].R2 = m1
                            self.tobita_grow(-1, m2, new_conv, True)
                        # end self.request_arm m2 check
                    # end self.request_arm m1 check
                elif rnd < (Psigma + Plambd): # grew from scission
                    new_conv = self.getconv1(cur_conv)
                    if np.random.random() <= 0.50:
                        m1, success = self.request_arm()
                        if success: # check arm availability
                            self.armupdown(m, m1)
                            seg_len = self.calclength(new_conv)
                            self.arm_pool[m1].arm_len = seg_len
                            self.arm_pool[m1].arm_conv = new_conv
                            self.arm_pool[m].L1 = m1
                            self.arm_pool[m1].L2 = m
                            self.tobita_grow(1, m1, new_conv, True)
                        # end self.request_arm check
                    else:
                        m2, success = self.request_arm()
                        if success: # check arm availability
                            self.armupdown(m, m2)
                            seg_len = self.calclength(new_conv)
                            self.arm_pool[m2].arm_len = seg_len
                            self.arm_pool[m2].arm_conv = new_conv
                            self.arm_pool[m].L2 = -m2
                            self.arm_pool[m2].R1 = m
                            self.tobita_grow(-1, m2, new_conv, True)
                        # end self.request_arm check
                # grew from initiation : do nothing
            # end of left-growth chain end possibilities
        # end of all chain-end possibilities
        self.rlevel -= 1

    def calclength(self, conv):
        """Calculates initial length of a segment grown at conversion "conv" """
        # var
        # rnd,sigma,lambd,pref :double
        rnd = np.random.random()
        if rnd == 0.0:
            rnd = 1.0
        sigma = self.Cs * conv/(1.0 - conv) # calculate scission event population
        lambd = self.Cb * conv/(1.0 - conv) # calculate branching population
        pref = self.tau + self.beta + sigma + lambd
        r = -np.log(rnd) / pref
        if r < 1000.0:
            r = np.trunc(r) + 1
        return r

    def scilength(self, conv):
        """Calculate length between scission-points of a segment grown at conversion "conv" """
        # var
        # rnd,eta  :double
        rnd = np.random.random()
        if rnd == 0.0:
            rnd = 1.0
        eta = self.Cs * np.log((1.0 - conv) / (1.0 - self.fin_conv)) + 1.0e-80
        r = -np.log(rnd)/eta
        if r < 1000.0:
            r = np.trunc(r) + 1
        return r

    def brlength(self, conv):
        """Calculate length between branch-points of a segment grown at conversion "conv" """
        # var
        # rnd,rho :double
        rnd = np.random.random()
        if rnd == 0.0:
            rnd = 1.0
        rho = self.Cb * np.log((1.0 - conv) / (1.0 - self.fin_conv))
        r = -np.log(rnd)/rho
        return r

    def getconv1(self, cur_conv):
        """Calculate conversion of older segment"""
        return np.random.random() * cur_conv

    def getconv2(self, cur_conv):
        """Calculate conversion of newer segment growing from scission or branchpoint"""
        # var
        # rnd :double
        rnd = np.random.random()
        return 1.0 - (1.0 - cur_conv) * np.exp(-rnd * np.log((1.0 - cur_conv) / (1.0 - self.fin_conv)))
