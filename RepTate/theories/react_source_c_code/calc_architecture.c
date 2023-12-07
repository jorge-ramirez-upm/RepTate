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

// Copyright (2017-2023): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds


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
// Seniority: To calculate this for a given segment, count the number of
// strands to the furthest chain end on each side of the segments, then take the smaller of the two values.

// Priority: To calculate this for a given segment, count the number of chain ends
// attached to each side of the strand, and then take the smaller of the two values.

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "polybits.h"
#include "calc_architecture.h"
#define N_PS 10000

static void bin_prio_vs_senio(int npol);
static void bin_br_pts(int npoly, int ndistr);

static double sphi_avsenio_v_prio[N_PS];
static double sphi_avprio_v_senio[N_PS];

static double avsenio_v_prio[N_PS];
static double avprio_v_senio[N_PS];

static double avarmlen_v_senio[N_PS];
static double avarmlen_v_prio[N_PS];

static double proba_prio[N_PS];
static double proba_senio[N_PS];

static int n_armlen_v_senio[N_PS];
static int n_armlen_v_prio[N_PS];

static double lgmin;
static double lgmax;
static double lgstep;

static int n_polymer;
static int max_prio;
static int max_senio;

int num_armwt_bin;
bool do_prio_senio = false;
bool flag_stop_all = false;

void set_do_prio_senio(bool b)
{
    do_prio_senio = b;
}
void set_flag_stop_all(bool b)
{
    flag_stop_all = b;
}

void print_arch_stats(int n1)
{
    double n = 1.0 * react_dist[n1].npoly;
    printf("lin=%.3g, star=%.3g, H=%.3g, 7arm=%.3g, comb=%.3g, other=%.3g\n",
           react_dist[n1].nlin / n, react_dist[n1].nstar / n, react_dist[n1].nH / n, react_dist[n1].n7arm / n, react_dist[n1].ncomb / n, react_dist[n1].nother / n);
    printf("sumStat=%d, npoly=%d\n", react_dist[n1].nlin + react_dist[n1].nstar + react_dist[n1].nH + react_dist[n1].n7arm + react_dist[n1].ncomb + react_dist[n1].nother, react_dist[n1].npoly);
}
void senio_prio(int npoly, int ndistr)
{
    double wt = br_poly[npoly].tot_len * react_dist[ndistr].monmass;
    if ((wt <= react_dist[ndistr].arch_maxwt) && (react_dist[ndistr].arch_minwt <= wt))
    {
        calc_seniority(npoly);
        calc_priority(npoly);
        if (br_poly[npoly].max_prio > max_prio)
        {
            max_prio = br_poly[npoly].max_prio;
        }
        if (br_poly[npoly].max_senio > max_senio)
        {
            max_senio = br_poly[npoly].max_senio;
        }
        save_architect(npoly, ndistr);
        react_dist[ndistr].nsaved_arch++;
        bin_prio_vs_senio(npoly);
    }
}

void bin_arm_length(int npoly, int ndistr)
{
    double wt = br_poly[npoly].tot_len * react_dist[ndistr].monmass;
    if ((wt <= react_dist[ndistr].arch_maxwt) && (react_dist[ndistr].arch_minwt <= wt))
    {
        double warm;
        int ibin, first, m;

        bin_br_pts(npoly, ndistr); // bin number of branch points
        first = br_poly[npoly].first_end;
        m = first;
        while (!flag_stop_all)
        {
            warm = arm_pool[m].arm_len * react_dist[ndistr].monmass;
            ibin = trunc((log10(warm) - lgmin) / lgstep) + 1;
            ibin = fmin(fmax(1, ibin), num_armwt_bin);
            react_dist[ndistr].numin_armwt_bin[ibin] += 1;
            m = arm_pool[m].down;
            if (m == first)
            {
                break;
            }
        }
    }
}

void bin_br_pts(int npoly, int ndistr)
{
    int num_br;
    num_br = br_poly[npoly].num_br;
    if (num_br > react_dist[ndistr].max_num_br)
    {
        react_dist[ndistr].max_num_br = num_br;
    }
    if (num_br < (pb_global_const.MAX_NBR + 1))
    {
        react_dist[ndistr].numin_num_br_bin[num_br] += 1;
    }
}

void init_bin_prio_vs_senio(int ndistr)
{
    int i;
    for (i = 0; i < N_PS; i++)
    {
        sphi_avprio_v_senio[i] = 0;
        sphi_avsenio_v_prio[i] = 0;

        avprio_v_senio[i] = 0;
        avsenio_v_prio[i] = 0;

        avarmlen_v_senio[i] = 0;
        avarmlen_v_prio[i] = 0;

        n_armlen_v_senio[i] = 0;
        n_armlen_v_prio[i] = 0;

        proba_senio[i] = 0;
        proba_prio[i] = 0;
    }
    n_polymer = 0;
    max_prio = 0;
    max_senio = 0;

    // initialise architecture statistics:
    react_dist[ndistr].wlin = 0;
    react_dist[ndistr].wstar = 0;
    react_dist[ndistr].wH = 0;
    react_dist[ndistr].w7arm = 0;
    react_dist[ndistr].wcomb = 0;
    react_dist[ndistr].wother = 0;
    react_dist[ndistr].nlin = 0;
    react_dist[ndistr].nstar = 0;
    react_dist[ndistr].nH = 0;
    react_dist[ndistr].n7arm = 0;
    react_dist[ndistr].ncomb = 0;
    react_dist[ndistr].nother = 0;

    // initialise arm length statistics
    lgmax = log10(react_dist[ndistr].arch_maxwt * 1.01);
    lgmin = log10(react_dist[ndistr].monmass / 1.01);
    num_armwt_bin = (lgmax - lgmin) * 10;
    lgstep = (lgmax - lgmin) / (1.0 * num_armwt_bin);
    for (i = 0; i < num_armwt_bin + 1; i++)
    {
        react_dist[ndistr].numin_armwt_bin[i] = 0;
    }
    react_dist[ndistr].num_armwt_bin = num_armwt_bin;

    // initialise branch point statistics
    for (i = 0; i < pb_global_const.MAX_NBR + 1; i++)
    {
        react_dist[ndistr].numin_num_br_bin[i] = 0;
    }
    react_dist[ndistr].max_num_br = 0;
}

void bin_prio_vs_senio(int npoly)
{
    int first, m, s, p;
    double totlen, phi;
    first = br_poly[npoly].first_end;
    m = first;
    totlen = br_poly[npoly].tot_len;

    while (!flag_stop_all)
    {
        p = arm_pool[m].prio;
        s = arm_pool[m].senio;
        phi = arm_pool[m].arm_len / totlen;
        // average prio vs senio
        avprio_v_senio[s] += phi * p;
        sphi_avprio_v_senio[s] += phi;

        // average senio vs prio
        avsenio_v_prio[p] += phi * s;
        sphi_avsenio_v_prio[p] += phi;

        // average arm length vs senio
        avarmlen_v_senio[s] += arm_pool[m].arm_len;
        n_armlen_v_senio[s]++;

        // average arm length vs prio
        avarmlen_v_prio[p] += arm_pool[m].arm_len;
        n_armlen_v_prio[p]++;

        // probability of prio p
        proba_prio[p] += phi;

        // probability of senio s
        proba_senio[s] += phi;

        m = arm_pool[m].down;
        if (m == first)
        {
            n_polymer++;
            break;
        }
    }
}

double return_avarmlen_v_senio(int s, int dist)
{
    if (n_armlen_v_senio[s] != 0)
        return avarmlen_v_senio[s] / n_armlen_v_senio[s] * react_dist[dist].monmass;
    else
        return 0;
}

double return_avarmlen_v_prio(int p, int dist)
{
    if (n_armlen_v_prio[p] != 0)
        return avarmlen_v_prio[p] / n_armlen_v_prio[p] * react_dist[dist].monmass;
    else
        return 0;
}

double return_avprio_v_senio(int s)
{
    if (sphi_avprio_v_senio[s] != 0)
        return avprio_v_senio[s] / sphi_avprio_v_senio[s];
    else
        return 0;
}

double return_avsenio_v_prio(int p)
{
    if (sphi_avsenio_v_prio[p] != 0)
        return avsenio_v_prio[p] / sphi_avsenio_v_prio[p];
    else
        return 0;
}

double return_proba_prio(int p)
{
    if (n_polymer != 0)
        return proba_prio[p] / n_polymer;
    else
        return 0;
}
double return_proba_senio(int s)
{
    if (n_polymer != 0)
        return proba_senio[s] / n_polymer;
    else
        return 0;
}

int return_max_prio(void)
{
    return max_prio;
}

int return_max_senio(void)
{
    return max_senio;
}

void save_architect(int npol, int ndist)
{
    int narm, first, m;
    int mL1, mL2, mR1, mR2;
    double wt;

    wt = br_poly[npol].tot_len * react_dist[ndist].monmass;
    narm = br_poly[npol].armnum;
    if (narm == 1)
    {
        react_dist[ndist].nlin++;
        react_dist[ndist].wlin += wt;
    }
    else if (narm == 3)
    {
        react_dist[ndist].nstar++;
        react_dist[ndist].wstar += wt;
    }
    else if (narm == 5)
    {
        react_dist[ndist].nH++;
        react_dist[ndist].wH += wt;
    }
    else if (narm == 7)
    {
        react_dist[ndist].n7arm++;
        react_dist[ndist].w7arm += wt;
    }
    else
    {
        first = br_poly[npol].first_end;
        m = first;
        while (!flag_stop_all)
        {
            mL1 = abs(arm_pool[m].L1);
            mL2 = abs(arm_pool[m].L2);
            mR1 = abs(arm_pool[m].R1);
            mR2 = abs(arm_pool[m].R2);
            if (arm_pool[m].senio > 1)
            {
                if (((arm_pool[mL1].senio != 1) && (arm_pool[mL2].senio != 1)) || ((arm_pool[mR1].senio != 1) && (arm_pool[mR2].senio != 1)))
                {
                    // it is not a comb
                    react_dist[ndist].nother++;
                    react_dist[ndist].wother += wt;
                    return;
                }
            }
            m = arm_pool[m].down;
            if (m == first)
                break;
        }
        react_dist[ndist].ncomb++;
        react_dist[ndist].wcomb += wt;
    }
}

void calc_seniority(int n)
{
    int first, m, sen_level, mL1, mL2, mR1, mR2, senL1, senL2, senR1, senR2, maxL, maxR, nassigned, armnum;
    first = br_poly[n].first_end;
    m = first;
    nassigned = 0;
    armnum = br_poly[n].armnum;
    while (!flag_stop_all)
    {
        // loop over all arms and determine if free-end (seniority=1)
        // if not, assign 0 (not determined)
        if ((arm_pool[m].L1 == 0 && arm_pool[m].L2 == 0) || (arm_pool[m].R1 == 0 && arm_pool[m].R2 == 0))
        {
            // it is a free end
            arm_pool[m].senio = 1;
            nassigned++;
            if (nassigned == armnum)
            {
                br_poly[n].max_senio = 1;
                return;
            }
        }
        else
        {
            arm_pool[m].senio = 0;
        }
        m = arm_pool[m].down;
        if (m == first)
            break;
    }

    m = first;
    sen_level = 2;
    while (!flag_stop_all)
    {
        if (arm_pool[m].senio == 0)
        {
            // seniority not yet determined
            mL1 = abs(arm_pool[m].L1);
            mL2 = abs(arm_pool[m].L2);
            mR1 = abs(arm_pool[m].R1);
            mR2 = abs(arm_pool[m].R2);

            senL1 = arm_pool[mL1].senio;
            senL2 = arm_pool[mL2].senio;
            maxL = (senL1 > senL2) ? senL1 : senL2;

            senR1 = arm_pool[mR1].senio;
            senR2 = arm_pool[mR2].senio;
            maxR = (senR1 > senR2) ? senR1 : senR2;

            if ((senL1 != 0 && senL2 != 0 && maxL == (sen_level - 1)) || (senR1 != 0 && senR2 != 0 && maxR == (sen_level - 1)))
            {
                arm_pool[m].senio = sen_level;
                nassigned++;
                if (nassigned == armnum)
                {
                    br_poly[n].max_senio = sen_level;
                    return;
                }
            }
        }
        m = arm_pool[m].down;
        if (m == first)
        {
            sen_level++;
        }
    }
}

void calc_priority(int n)
{
    int first, m, prio_level, mL1, mL2, mR1, mR2, prL1, prL2, prR1, prR2, nassigned, armnum;
    first = br_poly[n].first_end;
    m = first;
    nassigned = 0;
    armnum = br_poly[n].armnum;
    while (!flag_stop_all)
    {
        // loop over all arms and determine if free-end (priority=1)
        // if not, assign 0 (not determined)
        if ((arm_pool[m].L1 == 0 && arm_pool[m].L2 == 0) || (arm_pool[m].R1 == 0 && arm_pool[m].R2 == 0))
        {
            // it is a free end
            arm_pool[m].prio = 1;
            nassigned++;
            if (nassigned == armnum)
            {
                br_poly[n].max_prio = 1;
                return;
            }
        }
        else
        {
            arm_pool[m].prio = 0;
        }
        m = arm_pool[m].down;
        if (m == first)
            break;
    }

    m = first;
    prio_level = 2;
    while (!flag_stop_all)
    {
        if (arm_pool[m].prio == 0)
        {
            // priority not yet determined
            mL1 = abs(arm_pool[m].L1);
            mL2 = abs(arm_pool[m].L2);
            mR1 = abs(arm_pool[m].R1);
            mR2 = abs(arm_pool[m].R2);

            prL1 = arm_pool[mL1].prio;
            prL2 = arm_pool[mL2].prio;

            prR1 = arm_pool[mR1].prio;
            prR2 = arm_pool[mR2].prio;

            if ((prL1 != 0 && prL2 != 0 && ((prL1 + prL2) == prio_level)) || (prR1 != 0 && prR2 != 0 && ((prR1 + prR2) == prio_level)))
            {
                arm_pool[m].prio = prio_level;
                nassigned++;
                if (nassigned == armnum)
                {
                    br_poly[n].max_prio = prio_level;
                    return;
                }
            }
        }
        m = arm_pool[m].down;
        if (m == first)
        {
            prio_level++;
        }
    }
}
