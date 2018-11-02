// RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
// --------------------------------------------------------------------------------------------------------

// Authors:
//     Jorge Ramirez, jorge.ramirez@upm.es
//     Victor Boudara, victor.boudara@gmail.com
//     Daniel Read, d.j.read@leeds.ac.uk

// Useful links:
//     http://blogs.upm.es/compsoftmatter/software/reptate/
//     https://github.com/jorge-ramirez-upm/RepTate
//     http://reptate.readthedocs.io

// --------------------------------------------------------------------------------------------------------

// Copyright (2017): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds

// This file is part of RepTate.

// RepTate is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// RepTate is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with RepTate.  If not, see <http://www.gnu.org/licenses/>.

// --------------------------------------------------------------------------------------------------------
#include <stdlib.h>
#include <math.h>
#include "tobitaCSTR.h"
#include "binsandbob.h"
#include "polybits.h"
#include "polycleanup.h"
#include "polymassrg.h"
#include "calc_architecture.h"
#include "ran3.h"

tobitaCSTR_global tCSTR_global = {.tobCSTRnumber = 1, .tobitaCSTRerrorflag = false};

/* local functions */
static void tobita_grow(int dir, int m, double cur_conv, bool sc_tag);
static void calclength(double conv, double *r_out);
static void scilength(double conv, double *r_out);
static void brlength(double conv, double *r_out);
static void getconv1(double cur_conv, double *new_conv_out);
static void getconv2(double cur_conv, double *new_conv_out);
/* local variables */
static double tau, beta, sigma, lambda, Pbeta, Psigma, Plambda, siglam, Psiglam, pref;
static int scount, bcount, rlevel;

void tobCSTRstart(double ttau, double tbeta, double tsigma, double tlambda, int n)
{

    bobinit(n);

    // passed variables
    tau = ttau;
    beta = tbeta;
    sigma = tsigma;
    lambda = tlambda;

    siglam = sigma + lambda;
    pref = tau + beta + sigma + lambda;
    Plambda = lambda / pref; // prob reaction from polymer transfer (branching)
    Psigma = sigma / pref;   // prob reaction from scission site
    Psiglam = siglam / pref;
    Pbeta = beta / pref; // prob termination by combination

    tCSTR_global.tobitaCSTRerrorflag = false;
}

bool tobCSTR(int n, int n1)
{
    double cur_conv, seg_len, len1, len2, jtot, gfact;
    int m, m1, first, anum, nsegs;

    scount = 0;
    bcount = 0;
    getconv1(0.0, &cur_conv);
    if (request_arm(&m))
    { // don't do anything if arms not available
        br_poly[n]
            .first_end = m;
        arm_pool[m].up = m;
        arm_pool[m].down = m;
        calclength(cur_conv, &seg_len);
        arm_pool[m].arm_len = seg_len;
        arm_pool[m].arm_conv = cur_conv;
        rlevel = 0;
        tobita_grow(1, m, cur_conv, true);
    }
    if (request_arm(&m1))
    { // don't do anything if arms not available
        arm_pool[m].L1 = -m1;
        arm_pool[m1].R2 = m;
        armupdown(m, m1);
        calclength(cur_conv, &seg_len);
        arm_pool[m1].arm_len = seg_len;
        arm_pool[m1].arm_conv = cur_conv;
        rlevel = 0;
        tobita_grow(-1, m1, cur_conv, true);
    } // end check for arm availability

    if (pb_global.arms_avail)
    { // not true if we ran out of arms somewhere !
        polyclean(n);

        // renumber segments starting from zero
        m1 = br_poly[n].first_end;
        first = m1;
        anum = 0;
        arm_pool[m1].armnum = anum;
        m1 = arm_pool[m1].down;
        while (m1 != first)
        {
            anum++;
            arm_pool[m1].armnum = anum; // number of arms
            m1 = arm_pool[m1].down;
        }
        br_poly[n].armnum = anum + 1;
        first = br_poly[n].first_end;

        mass_segs(first, &len1, &nsegs);
        br_poly[n].num_br = bcount;
        br_poly[n].tot_len = len1;
        mass_rg2(first, 1.0, &len2, &jtot, &gfact);
        br_poly[n].gfactor = gfact;

        if (do_prio_senio)
        {
            senio_prio(n, n1);
        }
        bin_arm_length(n, n1);
        // check to see whether to save the polymer
        bobcount(n, n1);

        return true;
    }
    else
    {
        return false;
    }
}

void tobita_grow(int dir, int m, double cur_conv, bool sc_tag)
{

    int m1, m2;
    double seg_len, new_conv, rnd;

    rlevel++; //recursion level
    if ((rlevel > pb_global_const.MAX_RLEVEL) || tCSTR_global.tobitaCSTRerrorflag)
    {
        ///
        ///  need to decide what to do if you make molecules too big
        ///
        tCSTR_global.tobitaCSTRerrorflag = true;
        rlevel = 100000;
        return;
    }

    if (pb_global.arms_avail)
    { // don't do anything if arms aren't available

        scilength(cur_conv, &seg_len);
        if ((sc_tag) && (seg_len < arm_pool[m].arm_len))
        {
            arm_pool[m].arm_len = seg_len; // scission event
            arm_pool[m].scission = true;
        }
        brlength(cur_conv, &seg_len);
        if (seg_len < arm_pool[m].arm_len)
        { // a branch point
            bcount++;
            if (request_arm(&m1))
            { // return false if arms not available
                armupdown(m, m1);
                if (request_arm(&m2))
                {
                    armupdown(m, m2);
                    if (dir > 0)
                    { //going to the right
                        arm_pool[m].R1 = m1;
                        arm_pool[m1].L2 = -m; //I think it might be useful if
                                              //1 is connected to 2 all the time
                                              // sign(L1) etc indicates direction of subsequent segment.
                        arm_pool[m1].arm_len = arm_pool[m].arm_len - seg_len;
                        arm_pool[m].arm_len = seg_len;
                        arm_pool[m1].arm_conv = cur_conv;
                        arm_pool[m1].scission = arm_pool[m].scission;
                        arm_pool[m].scission = false;
                        getconv2(cur_conv, &new_conv);
                        calclength(new_conv, &seg_len);
                        arm_pool[m2].arm_len = seg_len;
                        arm_pool[m2].arm_conv = new_conv;
                        arm_pool[m1].L1 = m2;
                        arm_pool[m2].L2 = m1;
                        arm_pool[m].R2 = m2;
                        arm_pool[m2].L1 = -m;
                        tobita_grow(1, m2, new_conv, true);
                        tobita_grow(dir, m1, cur_conv, false);
                    }
                    else
                    { //going to the left
                        arm_pool[m].L1 = -m1;
                        arm_pool[m1].R2 = m;
                        arm_pool[m1].arm_len = arm_pool[m].arm_len - seg_len;
                        arm_pool[m].arm_len = seg_len;
                        arm_pool[m1].arm_conv = cur_conv;
                        arm_pool[m1].scission = arm_pool[m].scission;
                        arm_pool[m].scission = false;
                        getconv2(cur_conv, &new_conv);
                        calclength(new_conv, &seg_len);
                        arm_pool[m2].arm_len = seg_len;
                        arm_pool[m2].arm_conv = new_conv;
                        arm_pool[m1].R1 = m2;
                        arm_pool[m2].L2 = -m1;
                        arm_pool[m].L2 = m2;
                        arm_pool[m2].L1 = m;
                        tobita_grow(1, m2, new_conv, true);
                        tobita_grow(dir, m1, cur_conv, false);
                    }
                } // end of arm m1 available
            }     // end of arm m available
        }         // end of it's a branchpoint
        else
        { // non side-branching condition - deal with end of chain
            if (arm_pool[m].scission)
            { // the end of the chain is a scission point
                if (ran3(&iy3) < 0.50)
                { // and there is more growth at the scission point
                    getconv2(cur_conv, &new_conv);
                    if (request_arm(&m1))
                    { // returns false if arm not available
                        armupdown(m, m1);
                        calclength(new_conv, &seg_len);
                        arm_pool[m1].arm_len = seg_len;
                        arm_pool[m1].arm_conv = new_conv;
                        if (dir > 0)
                        {
                            arm_pool[m].R1 = m1;
                            arm_pool[m1].L2 = -m;
                        }
                        else
                        {
                            arm_pool[m].L1 = m1;
                            arm_pool[m1].L2 = m;
                        }
                        tobita_grow(1, m1, new_conv, true);
                    } // end check for arm available
                }     // end of more growth from scission point
            }         // end of scission at chain end
                      // chain end possibilities depend on the direction
            else if (dir > 0)
            { //  growing to the right
                rnd = ran3(&iy3);
                if (rnd < Pbeta)
                { //prob for termination by combination
                    if (request_arm(&m1))
                    { // false if arm not available
                        armupdown(m, m1);
                        calclength(cur_conv, &seg_len);
                        arm_pool[m1].arm_len = seg_len;
                        arm_pool[m1].arm_conv = cur_conv;
                        arm_pool[m].R1 = -m1;
                        arm_pool[m1].R2 = -m;
                        tobita_grow(-1, m1, cur_conv, true);
                    } // end request_arm check
                }     // otherwise, end of chain: do nothing
            }         // end of right growth
            else
            { // must be left growth
                rnd = ran3(&iy3);
                if (rnd < Plambda)
                { // grew from a branch
                    bcount++;
                    getconv1(cur_conv, &new_conv);
                    if (request_arm(&m1))
                    { // check arm availability
                        armupdown(m, m1);
                        if (request_arm(&m2))
                        {
                            armupdown(m, m2);
                            calclength(new_conv, &seg_len);
                            arm_pool[m1].arm_len = seg_len;
                            arm_pool[m1].arm_conv = new_conv;
                            arm_pool[m].L1 = m1;
                            arm_pool[m1].L2 = m;
                            tobita_grow(1, m1, new_conv, true);
                            calclength(new_conv, &seg_len);
                            arm_pool[m2].arm_len = seg_len;
                            arm_pool[m2].arm_conv = new_conv;
                            arm_pool[m].L2 = -m2;
                            arm_pool[m2].R1 = m;
                            arm_pool[m1].L1 = -m2;
                            arm_pool[m2].R2 = m1;
                            tobita_grow(-1, m2, new_conv, true);
                        } // end request_arm m2 check
                    }     // end request_arm m1 check
                }
                else if (rnd < Psiglam)
                { // grew from scission
                    getconv1(cur_conv, &new_conv);
                    if (ran3(&iy3) <= 0.50)
                    {
                        if (request_arm(&m1))
                        { // check arm availability
                            armupdown(m, m1);
                            calclength(new_conv, &seg_len);
                            arm_pool[m1].arm_len = seg_len;
                            arm_pool[m1].arm_conv = new_conv;
                            arm_pool[m].L1 = m1;
                            arm_pool[m1].L2 = m;
                            tobita_grow(1, m1, new_conv, true);
                        } // end request_arm check
                    }
                    else
                    {
                        if (request_arm(&m2))
                        { // check arm availability
                            armupdown(m, m2);
                            calclength(new_conv, &seg_len);
                            arm_pool[m2].arm_len = seg_len;
                            arm_pool[m2].arm_conv = new_conv;
                            arm_pool[m].L2 = -m2;
                            arm_pool[m2].R1 = m;
                            tobita_grow(-1, m2, new_conv, true);
                        } // end request_arm check
                    }
                } // grew from initiation : do nothing
            }     // end of left-growth chain end possibilities

        } // end of all chain-end possibilities

    } //end check for arms available

    rlevel--;
}

void calclength(double conv, double *r) //TODO: conv variable not used...
{
    // Calculates initial length of a segment grown at conversion "conv"
    double rnd;
    rnd = ran3(&iy3);
    if (rnd == 0.0)
    {
        rnd = 1.0;
    }
    *r = (-log(rnd) / pref);
    if (*r < 1000.0)
    {
        *r = (int)(*r) + 1;
    }
}

void scilength(double conv, double *r)
{
    // Calculate length between scission-points of a segment grown at conversion "conv"
    double rnd, eta;

    rnd = ran3(&iy3);
    if (rnd == 0.0)
    {
        rnd = 1.0;
    }
    eta = (sigma / siglam) * (1.0 - exp(siglam * conv)) + 1.0e-80; //scission density
    *r = (-log(rnd) / eta);
    if (*r < 1000.0)
    {
        *r = (int)(*r) + 1;
    }
}
void brlength(double conv, double *r)
{
    // Calculate length between branch-points of a segment grown at conversion "conv"
    double rnd, rho;

    rnd = ran3(&iy3);
    if (rnd == 0.0)
    {
        rnd = 1.0;
    }
    // rho = Cb*(1.0d0-exp(-(Cs+Cb)*log((1.0d0-conv)/(1.0d0-fin_conv))))/(Cs+Cb)  !branching density
    rho = (lambda / siglam) * (1.0 - exp(siglam * conv)) + 1.0e-80; //branching density
    *r = (-log(rnd) / rho);
}

void getconv1(double cur_conv, double *new_conv)
{
    // Calculate conversion of older segment
    double rnd;

    rnd = ran3(&iy3);
    if (rnd == 0.0)
    {
        rnd = 1.0;
    }
    *new_conv = cur_conv + log(rnd);
}

void getconv2(double cur_conv, double *new_conv)
{
    //Calculate conversion of newer segment growing from scission or branchpoint
    double rnd;
    rnd = ran3(&iy3);
    *new_conv = rnd * cur_conv;
}
