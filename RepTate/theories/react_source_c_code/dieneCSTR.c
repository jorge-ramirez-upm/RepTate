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
#include <time.h>

#include "dieneCSTR.h"
#include "binsandbob.h"
#include "polybits.h"
#include "polycleanup.h"
#include "polymassrg.h"
#include "calc_architecture.h"
#include "ran3.h"

dieneCSTR_global dCSTR_global = {.dieneCSTRnumber = 1, .dieneCSTRerrorflag = false};

/* local functions */
static void diene_grow(int dir, int m, double cur_conv);
static void calclength(double *r_out);
static void brlength(double *r_out);
static void getconv(double *new_conv_out);
static void getconv_future_reac(double cur_conv, double *new_conv);
static void getconv_past_reac(double cur_conv, double *new_conv);

/* local variables */
static double tau, kpM, kDLCB, kpD, kd, kt, D0, C0;
static double lc, lb, conv_future, conv_past, p_free_diene, ldiene = 0;
static int bcount, rlevel;

void dieneCSTRstart(double _tau, double _kpM, double _kDLCB, double _kpD, double _kd, double _kt, double _D0, double _C0, int n)
{
    double s, P, lb1, lb2;

    bobinit(n);

    // passed variables //
    tau = _tau;
    kpM = _kpM;
    kDLCB = _kDLCB;
    kpD = _kpD;
    kd = _kd;
    kt = _kt;
    D0 = _D0;
    C0 = _C0;

    // calculated variables //
    s = 1.0 / tau;
    P = s * C0 / (s + kd);
    // average arm length
    lc = kpM / (s + kt + kd);
    // average length before free-diene incorporation
    lb1 = kpM * (s + kpD * P) / (kpD * s * D0);
    // average length before once-reacted-diene incorporation
    lb2 = kpM * (s + kDLCB * P) * (s + kpD * P) / (kDLCB * kpD * P * s * D0);
    // average length before either event
    lb = 1.0 / ((1.0 / lb1) + (1.0 / lb2));

    // average conv before of once-reacted-diene future reaction
    conv_future = s / (kDLCB * P);
    // average conv once-reacted-diene was made
    conv_past = s / (s + kDLCB * P);

    // proba free-diene incorporation
    p_free_diene = 1.0 / (1.0 + lb1 / lb2);

    dCSTR_global.dieneCSTRerrorflag = false;
}

bool dieneCSTR(int n, int n1)
{
    double cur_conv, seg_len, len1, len2, jtot, gfact;
    int m, m1, first, anum, nsegs;

    bcount = 0;
    // pick a monomer convertion at random
    getconv(&cur_conv);
    if (request_arm(&m))
    { // don't do anything if arms not available
        br_poly[n].first_end = m;
        arm_pool[m].up = m;
        arm_pool[m].down = m;
        // generate random arm length
        calclength(&seg_len);
        arm_pool[m].arm_len = seg_len;
        arm_pool[m].arm_conv = cur_conv;
        rlevel = 0;
        diene_grow(1, m, cur_conv);
    }
    if (request_arm(&m1))
    { // don't do anything if arms not available
        arm_pool[m].L1 = -m1;
        arm_pool[m1].R2 = m;
        armupdown(m, m1);
        calclength(&seg_len);
        arm_pool[m1].arm_len = seg_len;
        arm_pool[m1].arm_conv = cur_conv;
        rlevel = 0;
        diene_grow(-1, m1, cur_conv);
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

void diene_grow(int dir, int m, double cur_conv)
{

    int m1, m2, m3, m4;
    double seg_len, new_conv;

    rlevel++; //recursion level
    if ((rlevel > 1000) || dCSTR_global.dieneCSTRerrorflag)
    {
        dCSTR_global.dieneCSTRerrorflag = true;
        rlevel = 100000;
        return;
    }

    if (pb_global.arms_avail)
    { // don't do anything if arms aren't available
        // generate arm length before diene incorporation
        brlength(&seg_len);
        if (seg_len < arm_pool[m].arm_len)
        { // a branch point
            bcount++;
            if (request_arm(&m1))
            {
                armupdown(m, m1);
                if (request_arm(&m2))
                {
                    armupdown(m, m2);

                    arm_pool[m].R1 = m1;
                    arm_pool[m1].L2 = -m;
                    arm_pool[m1].arm_len = arm_pool[m].arm_len - seg_len;
                    arm_pool[m].arm_len = seg_len;
                    arm_pool[m1].arm_conv = cur_conv;

                    // diene arm
                    arm_pool[m2].arm_len = ldiene;
                    arm_pool[m2].arm_conv = cur_conv;
                    arm_pool[m1].L1 = m2;
                    arm_pool[m2].L2 = m1;
                    arm_pool[m].R2 = m2;
                    arm_pool[m2].L1 = -m;

                    diene_grow(dir, m1, cur_conv);

                    if (ran3(&iy3) < p_free_diene)
                    { // free-diene incorporation
                        // find if reacted before conv=0
                        getconv_future_reac(cur_conv, &new_conv);
                        if (new_conv > 0.0)
                        { // diene NOT reacted before conv=0
                            rlevel--;
                            return;
                        }
                    }
                    else
                    {
                        //incorporation of once-reacted-diene
                        getconv_past_reac(cur_conv, &new_conv);
                    }
                    // connect two arms to the diene
                    bcount++;
                    if (request_arm(&m3))
                    {
                        armupdown(m2, m3);
                        if (request_arm(&m4))
                        {
                            armupdown(m2, m4);

                            // generate arm length
                            calclength(&seg_len);
                            arm_pool[m3].arm_len = seg_len;
                            calclength(&seg_len);
                            arm_pool[m4].arm_len = seg_len;
                            // assign conversion
                            arm_pool[m3].arm_conv = new_conv;
                            arm_pool[m4].arm_conv = new_conv;
                            // connect new arms to diene
                            arm_pool[m2].R2 = -m3;
                            arm_pool[m2].R1 = m4;
                            arm_pool[m3].R1 = -m2;
                            arm_pool[m3].R2 = m4;
                            arm_pool[m4].L1 = -m3;
                            arm_pool[m4].L2 = -m2;

                            diene_grow(-1, m3, new_conv);
                            diene_grow(1, m4, new_conv);
                        } // end arm available
                    }     // end arm available
                }         // end arm available
            }             // end arm available
        }                 // end of it's a branchpoint
    }                     //end check for arms available
    rlevel--;
}

void calclength(double *r)
{
    // Calculates initial length of a segment grown at conversion "conv"
    double rnd;
    rnd = ran3(&iy3);
    if (rnd == 0.0)
    {
        rnd = 1.0;
    }
    *r = (-lc * log(rnd));
    if (*r < 1000.0)
    {
        *r = (int)(*r) + 1;
    }
}

void brlength(double *r)
{
    // Calculate length between branch-points of a segment grown at conversion "conv"
    double rnd;

    rnd = ran3(&iy3);
    if (rnd == 0.0)
    {
        rnd = 1.0;
    }
    *r = (-lb * log(rnd));
}

void getconv(double *new_conv)
{
    // Calculate conversion of older segment
    double rnd;

    rnd = ran3(&iy3);
    if (rnd == 0.0)
    {
        rnd = 1.0;
    }
    *new_conv = log(rnd);
}

void getconv_future_reac(double cur_conv, double *new_conv)
{
    // new_conv is the conversion at which a once reacted diene at con cur_conv reacts again
    double rnd;

    rnd = ran3(&iy3);
    if (rnd == 0.0)
    {
        rnd = 1.0;
    }
    *new_conv = cur_conv - conv_future * log(rnd);
}

void getconv_past_reac(double cur_conv, double *new_conv)
{
    // new_conv is the conversion at which a twice-reacted diene was once-reacted
    double rnd;

    rnd = ran3(&iy3);
    if (rnd == 0.0)
    {
        rnd = 1.0;
    }
    *new_conv = cur_conv + conv_past * log(rnd);
}
