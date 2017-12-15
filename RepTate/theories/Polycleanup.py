# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Daniel Read, d.j.read@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module Polyclean

"""
import numpy as np
from Polybits import Polybits

class polycleanup(Polybits):
   
    def polyclean(self, n):
        seg1 = self.br_poly[n].first_end
        self.armclean(seg1) 
        seg1 = -seg1
        self.armclean(seg1)

    
    def armclean(self, m):
        # var
        # mc,m1,m2,mc1,mc2,t1,t2,tc1,tc2,tup,tdown: integer;
        # begin
        mc = np.abs(m)
        if m > 0: #positive direction
            m1 = self.arm_pool[mc].R1;
            m2 = self.arm_pool[mc].R2;
        else: #negative direction
            m1 := arm_pool[mc].L1
            m2 := arm_pool[mc].L2
        if ((m1 <> 0) and (m2 <> 0)) then  //branchpoint - no need for cleaning
        begin
            armclean(m1);
            armclean(m2);
        end
        else
        if ((m1 <> 0) and (m2 = 0)) then       // < changed to <> by DJR