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
// Seniority: To calculate this for a given segment, count the number of
// strands to the furthest chain end on each side of the segments, then take the smaller of the two values.

// Priority: To calculate this for a given segment, count the number of chain ends
// attached to each side of the strand, and then take the smaller of the two values.

#include <stdlib.h>
#include <stdio.h>
#include "polybits.h"
#include "calc_architecture.h"
#define N_PS 10000

bool do_prio_senio = false;
bool flag_stop_all = false;

static double prio_v_senio[N_PS];
static double nprio_v_senio[N_PS];
void bin_prio_vs_senio(int npol);

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
    calc_seniority(npoly);
    calc_priority(npoly);
    double wt = br_poly[npoly].tot_len * react_dist[ndistr].monmass;
    if ((wt <= react_dist[ndistr].arch_maxwt) && (react_dist[ndistr].arch_minwt <= wt))
    {
        save_architect(npoly, ndistr);
        react_dist[ndistr].nsaved_arch++;
    }
    bin_prio_vs_senio(npoly);
}

void init_bin_prio_vs_senio(void)
{
    int i;
    for (int i = 0; i < N_PS; i++)
    {
        prio_v_senio[i] = 0;
        nprio_v_senio[i] = 0;
    }
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
        phi = arm_pool[first].arm_len / totlen;
        prio_v_senio[s] += phi * p;
        nprio_v_senio[s] += phi;

        m = arm_pool[m].down;
        if (m == first)
            break;
    }
}

double return_prio_vs_senio(int s)
{
    if (nprio_v_senio[s] != 0)
        return prio_v_senio[s] / nprio_v_senio[s];
    else
        return 0;
}

void save_architect(int npol, int ndist)
{
    int narm, first, m;
    int mL1, mL2, mR1, mR2;
    narm = br_poly[npol].armnum;
    if (narm == 1)
    {
        react_dist[ndist].nlin++;
    }
    else if (narm == 3)
    {
        react_dist[ndist].nstar++;
    }
    else if (narm == 5)
    {
        react_dist[ndist].nH++;
    }
    else if (narm == 7)
    {
        react_dist[ndist].n7arm++;
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
                    return;
                }
            }
            m = arm_pool[m].down;
            if (m == first)
                break;
        }
        react_dist[ndist].ncomb++;
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
    int first, m, prio_level, mL1, mL2, mR1, mR2, prL1, prL2, prR1, prR2, maxL, maxR, nassigned, armnum;
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

/////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////

// void partial_senority(int, int, int, int, int *);
// void set_seniority(int n, int n1);
// void set_tmpflag(int n);

// void calc_seniority_bob(int n)
// {
//     int n1 = br_poly[n].first_end;
//     set_seniority(n, n1);
//     int n2 = arm_pool[n1].down;
//     while (n2 != n1)
//     {
//         set_seniority(n, n2);
//         n2 = arm_pool[n2].down;
//     }
// }

// void set_seniority(int n, int n1)
// {
//     if ((arm_pool[n].L1 == 0 && arm_pool[n].L2 == 0) || (arm_pool[n].R1 == 0 && arm_pool[n].R2 == 0))
//     {
//         arm_pool[n1].senio = 1;
//     }
//     else
//     {
//         int nL1 = abs(arm_pool[n1].L1);
//         int nL2 = abs(arm_pool[n1].L2);
//         int nR1 = abs(arm_pool[n1].R1);
//         int nR2 = abs(arm_pool[n1].R2);
//         int sL;
//         sL = 0;
//         partial_seniority(n, n1, nL1, nL2, &sL);
//         int sR;
//         sR = 0;
//         partial_seniority(n, n1, nR1, nR2, &sR);
//         if (sL <= sR)
//         {
//             arm_pool[n1].senio = sL;
//         }
//         else
//         {
//             arm_pool[n1].senio = sR;
//         }
//     }
// }

// void partial_seniority(int n, int n1, int nL1, int nL2, int *psL)
// {
//     int psL1, psL2;
//     psL1 = 0;
//     psL2 = 0;
//     set_tmpflag(n);
//     arm_pool[n1].tmpflag = false;
//     arm_pool[nL2].tmpflag = false;
//     if ((arm_pool[n].L1 == 0 && arm_pool[n].L2 == 0) || (arm_pool[n].R1 == 0 && arm_pool[n].R2 == 0))
//     {
//         psL1 = 1;
//     }
//     else
//     {
//         int nL1a = abs(arm_pool[nL1].L1);
//         int nL1b = abs(arm_pool[nL1].L2);
//         int nL1c = abs(arm_pool[nL1].R1);
//         int nL1d = abs(arm_pool[nL1].R2);
//         if ((nL1a == 0) || (nL1b == 0) || (nL1c == 0) || (nL1d == 0))
//         {
//             printf("inconsistent architechture in partial_seniority.cpp \n");
//         }
//         if (arm_pool[nL1a].tmpflag)
//         {
//             partial_seniority(n, nL1, nL1a, nL1b, &psL1);
//         }
//         else
//         {
//             partial_seniority(n, nL1, nL1c, nL1d, &psL1);
//         }
//     }

//     set_tmpflag(n);
//     arm_pool[nL1].tmpflag = false;
//     arm_pool[n1].tmpflag = false;
//     if ((arm_pool[n].L1 == 0 && arm_pool[n].L2 == 0) || (arm_pool[n].R1 == 0 && arm_pool[n].R2 == 0))
//     {
//         psL2 = 1;
//     }
//     else
//     {
//         int nL2a = abs(arm_pool[nL2].L1);
//         int nL2b = abs(arm_pool[nL2].L2);
//         int nL2c = abs(arm_pool[nL2].R1);
//         int nL2d = abs(arm_pool[nL2].R2);
//         if ((nL2a == 0) || (nL2b == 0) || (nL2c == 0) || (nL2d == 0))
//         {
//             printf("inconsistent architechture in partial_seniority.cpp \n");
//         }
//         if (arm_pool[nL2a].tmpflag)
//         {
//             partial_seniority(n, nL2, nL2a, nL2b, &psL2);
//         }
//         else
//         {
//             partial_seniority(n, nL2, nL2c, nL2d, &psL2);
//         }
//     }

//     if (psL1 >= psL2)
//     {
//         psL[0] = psL1 + 1;
//     }
//     else
//     {
//         psL[0] = psL2 + 1;
//     }
// }
// void set_tmpflag(int n)
// {
//   int n0 = br_poly[n].first_end;
//   arm_pool[n0].tmpflag = true;
//   int nd = arm_pool[n0].down;
//   while (nd != n0)
//   {
//     arm_pool[nd].tmpflag = true;
//     nd = arm_pool[nd].down;
//   }
// }