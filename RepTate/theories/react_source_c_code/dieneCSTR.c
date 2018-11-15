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
#include <stdio.h>

#include "dieneCSTR.h"
#include "binsandbob.h"
#include "polybits.h"
#include "polycleanup.h"
#include "polymassrg.h"
#include "calc_architecture.h"
#include "ran3.h"

dieneCSTR_global dCSTR_global = {.dieneCSTRnumber = 1, .dieneCSTRerrorflag = false};

/* local functions */
static void diene_grow(int dir, int m, double cur_conv, bool chopped);
static void calclength_past(double cur_conv, double *r_out);
static bool calclength_future(double cur_conv, double *r_out);
static void brlength(double *r_out);
static void getconv(double *new_conv_out);
static void getconv_future_reac_D(double cur_conv, double *new_conv);
static void getconv_past_reac_D(double cur_conv, double *new_conv);
static void getconv_past_reac_P(double cur_conv, double *new_conv);
static void getconv_future_reac_P(double cur_conv, double *new_conv);

/* local variables */
static double tau, kpM, kpLCB, kDLCB, kpD, keq, ks, D0, C0;
static double lc_past, lc_future, lb, conv_future_D, conv_past_D, conv_past_P, conv_future_P, p_free_diene, p_sum_diene, p_double_bond;
static double ldiene; // diene length is fixed to 1 monomer
static double s_kpM;
static double MINCONV; // converson time of collection (runtime)

static int bcount, rlevel;

void dieneCSTRstart(double _tau, double _kpM, double _kDLCB, double _kpLCB, double _kpD, double _keq, double _ks, double _D0, double _C0, double _ldiene, double t_collection, int n)
{
    double s, P, lb1, lb2, lb3, p_pendant_diene;

    bobinit(n);

    // passed variables //
    tau = _tau;
    kpM = _kpM;
    kDLCB = _kDLCB;
    kpLCB = _kpLCB;
    kpD = _kpD;
    keq = _keq;
    ks = _ks;
    D0 = _D0;
    C0 = _C0;
    ldiene = _ldiene;

    // calculated variables //
    s = 1.0 / tau;
    P = s * C0 / (s + keq);
    // average past arm length
    lc_past = kpM / (s + keq + ks);
    // average future arm length
    lc_future = kpM / (keq + ks);
    // average length before free-diene incorporation
    lb1 = kpM * (s + kpD * P) / (kpD * s * D0);
    // average length before once-reacted-diene incorporation
    lb2 = kpM * (s + kDLCB * P) * (s + kpD * P) / (kDLCB * kpD * P * s * D0);
    // average length before reincorporation after termination
    lb3 = kpM * (s + kpLCB * P) / (kpLCB * keq * P);
    // average length before either event
    lb = 1.0 / ((1.0 / lb1) + (1.0 / lb2) + (1.0 / lb3));

    // average conv before of once-reacted-diene future reaction
    conv_future_D = s / (kDLCB * P);
    // average conv once-reacted-diene was made
    conv_past_D = s / (s + kDLCB * P);
    // average conv a polymerising chain was terminated
    conv_past_P = s / (s + kpLCB * P);
    // average conv a terminated polymerising chain will be incorporated
    conv_future_P = s / (kpLCB * P);

    // proba free-diene incorporation
    p_free_diene = 1 / (1 + lb1 / lb2 + lb1 / lb3);

    // proba pendent-diene incorporation
    p_pendant_diene = 1 / (1 + lb2 / lb1 + lb2 / lb3);

    // sum p-diene
    p_sum_diene = p_free_diene + p_pendant_diene;

    // probability the chain end is terminated by a double bond
    p_double_bond = keq / (keq + ks);

    s_kpM = s / kpM;
    MINCONV = -t_collection * s;
    dCSTR_global.dieneCSTRerrorflag = false;
}

bool dieneCSTR(int n, int n1)
{
    double cur_conv, seg_len, len1, len2, jtot, gfact;
    int m, m1, first, anum, nsegs;
    bool is_chopped;

    bcount = 0;
    // pick a monomer convertion at random
    do
    {
        getconv(&cur_conv);
    } while (cur_conv < MINCONV);

    if (request_arm(&m))
    { // don't do anything if arms not available
        // -----m1-->--(X)----->--m----
        br_poly[n].first_end = m;
        arm_pool[m].up = m;
        arm_pool[m].down = m;
        // generate random arm length
        is_chopped = calclength_future(cur_conv, &seg_len);
        arm_pool[m].arm_len = seg_len;
        arm_pool[m].arm_conv = cur_conv;
        rlevel = 0;
        diene_grow(1, m, cur_conv, is_chopped);
    }
    if (request_arm(&m1))
    { // don't do anything if arms not available
        // -----m1-->--(X)----->--m----
        arm_pool[m].L1 = -m1;
        arm_pool[m1].R2 = m;
        armupdown(m, m1);
        calclength_past(cur_conv, &seg_len);
        arm_pool[m1].arm_len = seg_len;
        arm_pool[m1].arm_conv = cur_conv;
        rlevel = 0;
        diene_grow(-1, m1, cur_conv, false);
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

void diene_grow(int dir, int m, double cur_conv, bool chopped)
{

    double seg_len, new_conv, rnd;
    int m1, m2, m3, m4;
    int flag_diene_inc;
    bool is_chopped;

    rlevel++; //recursion level
    if (rlevel > pb_global_const.MAX_RLEVEL)
    {
        dCSTR_global.dieneCSTRerrorflag = true;
        rlevel--;
        return;
    }

    if (pb_global.arms_avail)
    { // don't do anything if arms aren't available
        // generate arm length before diene incorporation
        brlength(&seg_len);
        if (seg_len < arm_pool[m].arm_len)
        { // a branch point
            rnd = ran3(&iy3);
            if (rnd < p_free_diene)
            { // free-diene incorporation
                // connect it to two arms iff new_conv < 0
                getconv_future_reac_D(cur_conv, &new_conv);
                flag_diene_inc = 1;
            }
            else if (rnd < p_sum_diene)
            {
                // incorporation of once-reacted-diene
                // only if new_conv > MINCONV
                getconv_past_reac_D(cur_conv, &new_conv);
                flag_diene_inc = -1;
            }
            else
            {
                // incorporation of a terminated chain
                getconv_past_reac_P(cur_conv, &new_conv);
                // only if new_conv > MINCONV
                flag_diene_inc = 0;
            }
            if ((flag_diene_inc == 1) || (MINCONV < new_conv))
            {
                // true if free diene inc. or if inc. chain conversion is greater than MINCONV
                bcount++;
                if (request_arm(&m1))
                {
                    armupdown(m, m1);
                    if (request_arm(&m2))
                    {
                        armupdown(m, m2);
                        if (dir > 0)
                        {
                            // --m-->----B--->--m1-
                            //           ^
                            //           | m2
                            arm_pool[m].R1 = m1;
                            arm_pool[m1].L2 = -m;
                            arm_pool[m1].L1 = -m2;
                            arm_pool[m2].R2 = m1;
                            arm_pool[m].R2 = -m2;
                            arm_pool[m2].R1 = -m;
                        }
                        else
                        {
                            // --m1-->---B--->--m-
                            //           ^
                            //           | m2
                            arm_pool[m].L2 = -m1;
                            arm_pool[m1].R1 = m;
                            arm_pool[m].L1 = -m2;
                            arm_pool[m2].R2 = m;
                            arm_pool[m1].R2 = -m2;
                            arm_pool[m2].R1 = -m1;
                        }
                        arm_pool[m1].arm_len = arm_pool[m].arm_len - seg_len;
                        arm_pool[m].arm_len = seg_len;
                        arm_pool[m1].arm_conv = cur_conv;
                        diene_grow(dir, m1, cur_conv, chopped);
                        if (flag_diene_inc == 0)
                        {
                            // branching event is terminated chain incorporation (MINCONV < new_conv)
                            //  ----->----B--->---
                            //            ^
                            // ---m2-->---|
                            calclength_past(new_conv, &seg_len);
                            arm_pool[m2].arm_len = seg_len;
                            arm_pool[m2].arm_conv = new_conv;
                            diene_grow(-1, m2, new_conv, false);
                        }
                        else
                        {
                            // branching even is diene incorporation
                            arm_pool[m2].arm_len = ldiene;
                            arm_pool[m2].arm_conv = new_conv; // could be cur_conv
                            if ((MINCONV < new_conv) && (new_conv < 0))
                            {
                                bcount++;
                                // connect two arms to the diene
                                // ---->-----B--->----
                                //           ^
                                //           | m2
                                // --m3-->---B--->--m4--
                                if (request_arm(&m3))
                                {
                                    armupdown(m2, m3);
                                    if (request_arm(&m4))
                                    {
                                        armupdown(m2, m4);

                                        // generate arm length
                                        calclength_past(new_conv, &seg_len);
                                        arm_pool[m3].arm_len = seg_len;
                                        is_chopped = calclength_future(new_conv, &seg_len);
                                        arm_pool[m4].arm_len = seg_len;
                                        // assign conversion
                                        arm_pool[m3].arm_conv = new_conv;
                                        arm_pool[m4].arm_conv = new_conv;
                                        // connect new arms to diene
                                        arm_pool[m2].L2 = -m3;
                                        arm_pool[m2].L1 = m4;
                                        arm_pool[m3].R1 = m2;
                                        arm_pool[m3].R2 = m4;
                                        arm_pool[m4].L1 = -m3;
                                        arm_pool[m4].L2 = m2;

                                        diene_grow(-1, m3, new_conv, false);
                                        diene_grow(1, m4, new_conv, is_chopped);
                                    } // end arm available
                                }     // end arm available
                            }         // end link diene to two new arms
                        }             // end branching event was diene inc
                    }                 // end arm available
                }                     // end arm available
            }                         // end the branching event actually occured
        }                             // end of it's a branchpoint
        else
        {
            // deal with chain end. The only relevent event
            // is a double-bound terminated chain being later incorporated
            if ((dir > 0) && (!chopped))
            {
                if (ran3(&iy3) < p_double_bond)
                {
                    // chopped chains don't get incorporated
                    getconv_future_reac_P(cur_conv, &new_conv);
                    if (new_conv < 0)
                    {
                        bcount++;
                        // --->-m---B
                        //          |
                        // --->-m1--v-->--m2---
                        if (request_arm(&m1))
                        {
                            armupdown(m, m1);
                            if (request_arm(&m2))
                            {
                                armupdown(m, m2);

                                // generate arm length
                                calclength_past(new_conv, &seg_len);
                                arm_pool[m1].arm_len = seg_len;
                                is_chopped = calclength_future(new_conv, &seg_len);
                                arm_pool[m2].arm_len = seg_len;
                                // assign conversion
                                arm_pool[m1].arm_conv = new_conv;
                                arm_pool[m2].arm_conv = new_conv;
                                // connect new arms to m
                                arm_pool[m].R2 = -m1;
                                arm_pool[m].R1 = m2;
                                arm_pool[m1].R1 = -m;
                                arm_pool[m1].R2 = m2;
                                arm_pool[m2].L1 = -m1;
                                arm_pool[m2].L2 = -m;

                                diene_grow(-1, m1, new_conv, false);
                                diene_grow(1, m2, new_conv, is_chopped);
                            } // end arm available
                        }     // end arm available
                    }
                }
            }
        }
    } //end check for arms available
    rlevel--;
}

void calclength_past(double cur_conv, double *r)
{
    // Calculates initial length of a segment grown at conversion "conv"
    // chop arm if too long in the past
    double rnd, l_tmp;
    rnd = ran3(&iy3);
    if (rnd == 0.0)
    {
        rnd = 1.0;
    }
    l_tmp = -lc_past * log(rnd);
    if (MINCONV < (cur_conv - l_tmp * s_kpM))
    {
        *r = l_tmp;
    }
    else
    {
        // chop arm
        *r = (cur_conv - MINCONV) / s_kpM;
    }
}

bool calclength_future(double cur_conv, double *r)
{
    // Calculates future length of a segment grown at conversion "conv". Cut the arm if exceeds conv=0
    double rnd, l_tmp;
    rnd = ran3(&iy3);
    if (rnd == 0.0)
    {
        rnd = 1.0;
    }
    l_tmp = -lc_future * log(rnd);
    if ((cur_conv + l_tmp * s_kpM) < 0)
    {
        *r = l_tmp;
        return false;
    }
    else
    {
        *r = -cur_conv / s_kpM;
        return true;
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

void getconv_future_reac_D(double cur_conv, double *new_conv)
{
    // new_conv is the conversion at which a once reacted diene at con cur_conv reacts again
    double rnd;

    rnd = ran3(&iy3);
    if (rnd == 0.0)
    {
        rnd = 1.0;
    }
    *new_conv = cur_conv - conv_future_D * log(rnd);
}

void getconv_past_reac_D(double cur_conv, double *new_conv)
{
    // new_conv is the conversion at which a twice-reacted diene was once-reacted
    double rnd;

    rnd = ran3(&iy3);
    if (rnd == 0.0)
    {
        rnd = 1.0;
    }
    *new_conv = cur_conv + conv_past_D * log(rnd);
}

void getconv_past_reac_P(double cur_conv, double *new_conv)
{
    // new_conv is the conversion at which incorporated macromer was created
    double rnd;

    rnd = ran3(&iy3);
    if (rnd == 0.0)
    {
        rnd = 1.0;
    }
    *new_conv = cur_conv + conv_past_P * log(rnd);
}

void getconv_future_reac_P(double cur_conv, double *new_conv)
{
    // new_conv is the conversion at which incorporated macromer was created
    double rnd;

    rnd = ran3(&iy3);
    if (rnd == 0.0)
    {
        rnd = 1.0;
    }
    *new_conv = cur_conv - conv_future_P * log(rnd);
}
