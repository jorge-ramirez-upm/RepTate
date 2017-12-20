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

MAX_ARM = 1000000
MAX_POL = 1000000
MAX_REACT = 11
MAX_BOB_BINS = 5000
MAX_MWD_BINS = 1000


arm_pool = [Arm() for i in range(MAX_ARM)] #array of Arm;
br_poly = [Polymer() for i in range(MAX_POL)] #array of polymer;
react_dist = [ReactResults(MAX_MWD_BINS, MAX_BOB_BINS) for i in range(MAX_REACT)] #array[1..maxreact] of reactresults;
#integer
first_in_pool = 0
first_poly_in_pool = 0
first_dist_in_pool = 0
mmax = 0
num_react = 0
arms_left = 0
#boolean
react_pool_initialised = False
react_pool_declared = False
arms_avail = True    #these flags simply record
polys_avail = True   #availability of arms
dists_avail = True

def react_pool_init():
    global first_in_pool, mmax, arms_left, first_poly_in_pool, first_dist_in_pool, react_pool_initialised
    
    if react_pool_initialised:
        return
    for i in range(MAX_ARM):
        arm_pool[i].L1 = i - 1
        arm_pool[i].R1 = i + 1
    arm_pool[0].L1 = 0
    arm_pool[MAX_ARM - 1].R1 = 0
    first_in_pool = 0
    mmax = 0
    arms_left = MAX_ARM

    for i in range(MAX_POL - 1):
        br_poly[i].nextpoly = i + 1
    br_poly[MAX_POL - 1].nextpoly = 0
    first_poly_in_pool = 0

    for i in range(MAX_REACT):
        react_dist[i].next = i + 1
        react_dist[i].nummwdbins = 100
        react_dist[i].numbobbins = 100
        react_dist[i].boblgmin = 1.0
        react_dist[i].boblgmax = 9.0
        react_dist[i].bobbinmax = 2
        react_dist[i].simnumber = 0
    react_dist[MAX_REACT - 1].next = 0
    first_dist_in_pool = 0

    react_pool_initialised = True

def pool_reinit():
    global mmax

    mini = np.min((mmax + 1, MAX_ARM))
    for i in range(mini): 
        arm_pool[i].L1 = i - 1
        arm_pool[i].R1 = i + 1

    arm_pool[0].L1 = 0
    arm_pool[MAX_ARM - 1].R1 = 0
    first_in_pool = 0
    mmax = 0

def request_arm():
    global arms_avail, first_in_pool, mmax, arms_left

    m = first_in_pool
    if arm_pool[m].R1 != 0:
        first_in_pool = arm_pool[m].R1
        mmax = mmax if mmax > m else m
        arm_pool[first_in_pool].L1 = 0
        arm_pool[m].L1 = 0
        arm_pool[m].L2 = 0
        arm_pool[m].R1 = 0
        arm_pool[m].R2 = 0
        arm_pool[m].up = 0
        arm_pool[m].down = 0
        arm_pool[m].ended = False
        arm_pool[m].endfin = False
        arm_pool[m].scission = False
        arms_left -= 1
        return m, True
    elif arm_pool[m].R1 == 0:
        # need to decide what to do if you run out of arms!
        arms_avail = False
        return m, False

def return_arm(m):
    global first_in_pool, arms_avail, arms_left

    arm_pool[first_in_pool].L1 = m
    arm_pool[m].L1 = 0
    arm_pool[m].L2 = 0
    arm_pool[m].R1 = first_in_pool
    arm_pool[m].R2 = 0
    arm_pool[m].up = 0
    arm_pool[m].down = 0
    arm_pool[m].ended = False
    arm_pool[m].endfin = False
    arm_pool[m].scission = False
    first_in_pool = m
    arms_avail = True
    arms_left += 1

def request_poly():
    global polys_avail, first_poly_in_pool

    m = first_poly_in_pool
    if br_poly[m].nextpoly == 0:
        # need to decide what to do if you run out of polymers!
        polys_avail = False;
        return m, False
    else:
        first_poly_in_pool = br_poly[m].nextpoly
        br_poly[m].nextpoly = 0
        br_poly[m].saved = True
        return m, True

def return_poly_arms(n):
    first = br_poly[n].first_end
    if first != 0:
        m1 = first
        while True:
            mc = arm_pool[m1].down
            return_arm(m1)
            m1 = mc
            if m1 == first: 
                break
    br_poly[n].saved = False

def return_poly(n):
    global first_poly_in_pool, polys_avail

    #first return all arms of the polymer
    if br_poly[n].saved:
        return_poly_arms(n)
    #then return polymer record to the pool
    br_poly[n].nextpoly = first_poly_in_pool
    first_poly_in_pool = n
    polys_avail = True

def request_dist():
    global dists_avail, first_dist_in_pool

    m = first_dist_in_pool
    if react_dist[m].next == 0:
        # need to decide what to do if you run out of distributions!
        dists_avail = False
        m = 0
        return m, False
    else:
        first_dist_in_pool = react_dist[m].next
        react_dist[m].next = 0
        react_dist[m].first_poly = 0
        react_dist[m].nummwdbins = 100
        react_dist[m].numbobbins = 100
        react_dist[m].boblgmin = 1.0
        react_dist[m].boblgmax = 9.0
        react_dist[m].bobbinmax = 2
        react_dist[m].polysaved = False
        react_dist[m].simnumber += 1
        return m, True

def return_dist(n):
    global first_dist_in_pool, dists_avail

    if n == 0:
        return
    # first return all polymers of the distribution
    m1 = react_dist[n].first_poly
    while m1 != 0:
        mc = br_poly[m1].nextpoly
        return_poly(m1)
        m1 = mc
    # then return distribution record to the pool
    react_dist[n].next = first_dist_in_pool
    first_dist_in_pool = n
    dists_avail = True
    react_dist[n].polysaved = False

def return_dist_polys(n):
    # return all polymers of the distribution
    m1 = react_dist[n].first_poly
    while m1 != 0:
        mc = br_poly[m1].nextpoly
        return_poly(m1)
        m1 = mc
    react_dist[n].first_poly = 0
    react_dist[n].polysaved = False
    react_dist[n].simnumber += 1

def armupdown(m, m1):
    arm_pool[m1].down = arm_pool[m].down
    arm_pool[m].down = m1
    arm_pool[m1].up = m
    arm_pool[arm_pool[m1].down].up = m1
