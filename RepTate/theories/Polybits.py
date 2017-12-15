# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Daniel Read, d.j.read@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module polybits
provides basic records for arms and polymers
required in all monte-carlo simulations of polymerisation
provides routines for requesting / returning arms to the arm-pool

TO USE THESE ROUTINES, FIRST CALL pool_inits
""" 
import numpy as np


class Arm:
    pass


class Polymer:
    pass


class ReactResults:
    def __init__(self, MAX_MWD_BINS, MAX_BOB_BINS):
        self.wt = np.zeros((MAX_MWD_BINS))
        self.avbr = np.zeros((MAX_MWD_BINS))
        self.wmass = np.zeros((MAX_MWD_BINS))
        self.avg = np.zeros((MAX_MWD_BINS))
        self.lgmid = np.zeros((MAX_MWD_BINS))

        self.numinbin = np.zeros((MAX_BOB_BINS))

class PolyBits:
    MAX_ARM = 1000000
    MAX_POL = 1000000
    MAX_REACT = 11
    MAX_BOB_BINS = 5000
    MAX_MWD_BINS = 1000

    def __init__(self):
        self.arm_pool = [Arm() for i in range(self.MAX_ARM)] #array of Arm;
        self.br_poly = [Polymer() for i in range(self.MAX_POL)] #array of polymer;
        self.react_dist = [ReactResults(self.MAX_MWD_BINS, self.MAX_BOB_BINS) for i in range(self.MAX_REACT)] #array[1..maxreact] of reactresults;
        #integer
        self.first_in_pool = 0
        self.first_poly_in_pool = 0
        self.first_dist_in_pool = 0
        self.mmax = 0
        self.num_react = 0
        self.arms_left = 0
        #boolean
        self.react_pool_initialised = False
        self.react_pool_declared = False
        self.arms_avail = True    #these flags simply record
        self.polys_avail = True   #availability of arms
        self.dists_avail = True

    def react_pool_init(self):
        if self.react_pool_initialised:
            return
        for i in range(self.MAX_ARM):
            self.arm_pool[i].L1 = i - 1
            self.arm_pool[i].R1 = i + 1
        self.arm_pool[0].L1 = 0
        self.arm_pool[self.MAX_ARM - 1].R1 = 0
        self.first_in_pool = 0
        self.mmax = 0
        self.arms_left = self.MAX_ARM

        for i in range(self.MAX_POL - 1):
            self.br_poly[i].nextpoly = i + 1
        self.br_poly[self.MAX_POL - 1].nextpoly = 0
        self.first_poly_in_pool = 0

        for i in range(self.MAX_REACT):
            self.react_dist[i].next = i + 1
            self.react_dist[i].nummwdbins = 100
            self.react_dist[i].numbobbins = 100
            self.react_dist[i].boblgmin = 1.0
            self.react_dist[i].boblgmax = 9.0
            self.react_dist[i].bobbinmax = 2
            self.react_dist[i].simnumber = 0
        self.react_dist[self.MAX_REACT - 1].next = 0
        self.first_dist_in_pool = 0

        self.react_pool_initialised = True

    def pool_reinit(self):
        mini = self.mmax + 1 if self.mmax + 1 < self.MAX_ARM else self.MAX_ARM
        for i in range(mini): 
            self.arm_pool[i].L1 = i - 1
            self.arm_pool[i].R1 = i + 1

        self.arm_pool[0].L1 = 0
        self.arm_pool[self.MAX_ARM - 1].R1 = 0
        self.first_in_pool = 0
        self.mmax = 0

    def request_arm(self):
        m = self.first_in_pool
        if self.arm_pool[m].R1 == 0:
            # need to decide what to do if you run out of arms!
            self.arms_avail = False
            return m, False
        else:
            self.first_in_pool = self.arm_pool[m].R1
            self.mmax = self.mmax if self.mmax > m else m
            self.arm_pool[self.first_in_pool].L1 = 0
            self.arm_pool[m].L1 = 0
            self.arm_pool[m].L2 = 0
            self.arm_pool[m].R1 = 0
            self.arm_pool[m].R2 = 0
            self.arm_pool[m].up = 0
            self.arm_pool[m].down = 0
            self.arm_pool[m].ended = False
            self.arm_pool[m].endfin = False
            self.arm_pool[m].scission = False
            self.arms_left -= 1
            return m, True

    def return_arm(self, m):
        self.arm_pool[self.first_in_pool].L1 = m
        self.arm_pool[m].L1 = 0
        self.arm_pool[m].L2 = 0
        self.arm_pool[m].R1 = self.first_in_pool
        self.arm_pool[m].R2 = 0
        self.arm_pool[m].up = 0
        self.arm_pool[m].down = 0
        self.arm_pool[m].ended = False
        self.arm_pool[m].endfin = False
        self.arm_pool[m].scission = False
        self.first_in_pool = m
        self.arms_avail = True
        self.arms_left += 1

    def request_poly(self):
        m = self.first_poly_in_pool
        if self.br_poly[m].nextpoly == 0:
            # need to decide what to do if you run out of polymers!
            self.polys_avail = False;
            return m, False
        else:
            self.first_poly_in_pool = self.br_poly[m].nextpoly
            self.br_poly[m].nextpoly = 0
            self.br_poly[m].saved = True
            return m, True

    def return_poly_arms(self, n):
        first = self.br_poly[n].first_end
        if first != 0:
            m1 = first
            while True:
                mc = self.arm_pool[m1].down
                self.return_arm(m1)
                m1 = mc
                if m1 == first: 
                    break
        self.br_poly[n].saved = False

    def return_poly(self, n):
        #first return all arms of the polymer
        if self.br_poly[n].saved:
            self.return_poly_arms(n)
        #then return polymer record to the pool
        self.br_poly[n].nextpoly = self.first_poly_in_pool
        self.first_poly_in_pool = n
        self.polys_avail = True

    def request_dist(self):
        m = self.first_dist_in_pool
        if self.react_dist[m].next == 0:
            # need to decide what to do if you run out of distributions!
            self.dists_avail = False
            m = 0
            return m, False
        else:
            self.first_dist_in_pool = self.react_dist[m].next
            self.react_dist[m].next = 0
            self.react_dist[m].first_poly = 0
            self.react_dist[m].nummwdbins = 100
            self.react_dist[m].numbobbins = 100
            self.react_dist[m].boblgmin = 1.0
            self.react_dist[m].boblgmax = 9.0
            self.react_dist[m].bobbinmax = 2
            self.react_dist[m].polysaved = False
            self.react_dist[m].simnumber += 1
            return m, True

    def return_dist(self, n):
        if n == 0:
            return
        # first return all polymers of the distribution
        m1 = self.react_dist[n].first_poly
        while m1 != 0:
            mc = self.br_poly[m1].nextpoly
            self.return_poly(m1)
            m1 = mc
        # then return distribution record to the pool
        self.react_dist[n].next = self.first_dist_in_pool
        self.first_dist_in_pool = n
        self.dists_avail = True
        self.react_dist[n].polysaved = False

    def return_dist_polys(self, n):
        # return all polymers of the distribution
        m1 = self.react_dist[n].first_poly
        while m1 != 0:
            mc = self.br_poly[m1].nextpoly
            self.return_poly(m1)
            m1 = mc
        self.react_dist[n].first_poly = 0
        self.react_dist[n].polysaved = False
        self.react_dist[n].simnumber += 1

    def armupdown(self, m, m1):
        self.arm_pool[m1].down = self.arm_pool[m].down
        self.arm_pool[m].down = m1
        self.arm_pool[m1].up = m
        self.arm_pool[self.arm_pool[m1].down].up = m1
