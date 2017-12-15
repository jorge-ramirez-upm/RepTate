# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http:#blogs.upm.es/compsoftmatter/software/reptate/
# https:#github.com/jorge-ramirez-upm/RepTate
# http:#reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Daniel Read, d.j.read@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module PolyCleanUp
provides routines for cleaning up connectivity of branched polymers

"""
import numpy as np
from PolyBits import PolyBits

class PolyCleanUp(PolyBits):
    
    def __init__(self):
        super().__init__()
   
    def polyclean(self, n):
        seg1 = self.br_poly[n].first_end
        self.armclean(seg1) 
        seg1 = -seg1
        self.armclean(seg1)

    
    def armclean(self, m):
        # var
        # mc,m1,m2,mc1,mc2,t1,t2,tc1,tc2,tup,tdown: integer
        # begin
        mc = np.abs(m)
        if m > 0: #positive direction
            m1 = self.arm_pool[mc].R1
            m2 = self.arm_pool[mc].R2
        else: #negative direction
            m1 = self.arm_pool[mc].L1
            m2 = self.arm_pool[mc].L2   
        
        if (m1 != 0) and (m2 != 0):  #branchpoint - no need for cleaning
            self.armclean(m1)
            self.armclean(m2)
        
        elif (m1 != 0) and (m2 == 0):       # < changed to != by DJR
            mc1 = np.abs(m1)
            # add lengths together
            self.arm_pool[mc].arm_len = self.arm_pool[mc].arm_len + self.arm_pool[mc1].arm_len
            # reconnect current segment to opposite side of next segment
            if m1 > 0:
                t1 = self.arm_pool[mc1].R1
                t2 = self.arm_pool[mc1].R2
            else:
                t1 = self.arm_pool[mc1].L1
                t2 = self.arm_pool[mc1].L2
            tc1 = np.abs(t1)
            tc2 = np.abs(t2)
            if m > 0:
                self.arm_pool[mc].R1 = t1
                self.arm_pool[mc].R2 = t2
            else:
                self.arm_pool[mc].L1 = t1
                self.arm_pool[mc].L2 = t2
            if t1 > 0:
                self.arm_pool[tc1].L2 = -m  # as viewed from this segment, the sign of the current segment
                                            # is the opposite of its sign from where suroutine was originally called
                self.arm_pool[tc1].L1 = t2  # this should already be so!!
            elif t1 < 0: #specifically exclude case where t1=0
                self.arm_pool[tc1].R2 = -m
                self.arm_pool[tc1].R1 = t2  #this should already be so!!
            if t2 > 0:
                self.arm_pool[tc2].L1 = -m
                self.arm_pool[tc2].L2 = t1  #this should already be so!!
            elif t2 < 0: #specifically exclude case where t2=0
                self.arm_pool[tc2].R1 = -m
                self.arm_pool[tc2].R2 = t1 #this should already be so!!
            # reconnect up and down of removed segment
            tup = self.arm_pool[mc1].up
            tdown = self.arm_pool[mc1].down
            self.arm_pool[tup].down = tdown
            self.arm_pool[tdown].up = tup
            # return to pool
            self.return_arm(mc1)
            # re-call clean-up on m
            self.armclean(m)

        elif (m1 == 0) and (m2 != 0):
            mc2 = np.abs(m2)
            # add lengths together
            self.arm_pool[mc].arm_len = self.arm_pool[mc].arm_len + self.arm_pool[mc2].arm_len
            # reconnect current segment to opposite side of next segment
            if m2 > 0:
                t1 = self.arm_pool[mc2].R1
                t2 = self.arm_pool[mc2].R2
            else:
                t1 = self.arm_pool[mc2].L1
                t2 = self.arm_pool[mc2].L2
            tc1 = np.abs(t1)
            tc2 = np.abs(t2)
            if m > 0:
                self.arm_pool[mc].R1 = t1
                self.arm_pool[mc].R2 = t2
            else:
                self.arm_pool[mc].L1 = t1
                self.arm_pool[mc].L2 = t2
            if t1 > 0:
                self.arm_pool[tc1].L2 = -m # as viewed from this segment, the sign of the current segment
                                           # is the opposite of its sign from where suroutine was originally called
                self.arm_pool[tc1].L1 = t2 # this should already be so!!
            elif t1 < 0: #specifically exclude case where t1=0
                self.arm_pool[tc1].R2 = -m
                self.arm_pool[tc1].R1 = t2 #!this should already be so!!
            if t2 > 0:
                self.arm_pool[tc2].L1 =-m
                self.arm_pool[tc2].L2 = t1 # this should already be so!!
            elif t2 < 0: # specifically exclude case where t1=0
                self.arm_pool[tc2].R1 = -m
                self.arm_pool[tc2].R2 = t1 # !this should already be so!!

            # reconnect up and down of removed segment
            tup = self.arm_pool[mc2].up
            tdown = self.arm_pool[mc2].down
            self.arm_pool[tup].down = tdown
            self.arm_pool[tdown].up = tup
            # return to pool
            self.return_arm(mc2)
            # recall clean-up on m
            self.armclean(m)
