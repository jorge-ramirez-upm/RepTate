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

#include "react_structs.h"
#include "polybits.h"

polybits_global_const pb_global_const = {.maxbobbins = 5000, .maxmwdbins = 1000, .maxarm = 1000000, .maxpol = 1000000, .maxreact = 11};
polybits_global pb_global = {.first_in_pool = 0, .first_poly_in_pool = 0, .first_dist_in_pool = 0, .mmax = 0, .num_react = 0, .arms_left = 0, .react_pool_initialised = false, .react_pool_declared = false, .arms_avail = true, .polys_avail = true, .dists_avail = true};

arm *arm_pool;
polymer *br_poly;
reactresults *react_dist;

// initialises pools - MUST BE CALLED FIRST TO USE THESE ROUTINES
void react_pool_init(void)
{
    static bool is_initialized = false;
    if (!(pb_global.react_pool_initialised))
    {
        int i;
        if (!is_initialized)
        {
            arm_pool = (arm *)malloc(sizeof(arm) * (pb_global_const.maxarm + 1));
            br_poly = (polymer *)malloc(sizeof(polymer) * (pb_global_const.maxpol + 1));
            react_dist = (reactresults *)malloc(sizeof(reactresults) * (pb_global_const.maxreact + 1));
            for (i = 1; i <= pb_global_const.maxreact; i++)
            {
                react_dist[i].wt = (double *)malloc(sizeof(double) * (pb_global_const.maxmwdbins + 1));
                react_dist[i].avbr = (double *)malloc(sizeof(double) * (pb_global_const.maxmwdbins + 1));
                react_dist[i].wmass = (double *)malloc(sizeof(double) * (pb_global_const.maxmwdbins + 1));
                react_dist[i].avg = (double *)malloc(sizeof(double) * (pb_global_const.maxmwdbins + 1));
                react_dist[i].lgmid = (double *)malloc(sizeof(double) * (pb_global_const.maxmwdbins + 1));
                react_dist[i].numinbin = (int *)malloc(sizeof(int) * (pb_global_const.maxbobbins + 1));
                // hold architecture statistics:
                react_dist[i].nlin = 0;
                react_dist[i].nstar = 0;
                react_dist[i].nH = 0;
                react_dist[i].n5arm = 0;
                react_dist[i].n7arm = 0;
                react_dist[i].ncomb = 0;
                react_dist[i].nother = 0;
            }
            is_initialized = true;
        }
        for (i = 1; i <= pb_global_const.maxarm; i++)
        {
            arm_pool[i].L1 = i - 1;
            arm_pool[i].R1 = i + 1;
            arm_pool[i].prio = 0;
            arm_pool[i].senio = 0;
        }
        arm_pool[1].L1 = 0;
        arm_pool[pb_global_const.maxarm].R1 = 0;
        pb_global.first_in_pool = 1;
        pb_global.mmax = 0;
        pb_global.arms_left = pb_global_const.maxarm;

        for (i = 1; i <= pb_global_const.maxpol - 1; i++)
        {
            br_poly[i].nextpoly = i + 1;
            br_poly[i].max_prio = 0;
            br_poly[i].max_senio = 0;
        }
        br_poly[pb_global_const.maxpol].nextpoly = 0;
        pb_global.first_poly_in_pool = 1;

        for (i = 1; i <= pb_global_const.maxreact; i++)
        {
            react_dist[i].next = i + 1;
            react_dist[i].nummwdbins = 100;
            react_dist[i].numbobbins = 100;
            react_dist[i].boblgmin = 1.0;
            react_dist[i].boblgmax = 9.0;
            react_dist[i].bobbinmax = 2;
            react_dist[i].simnumber = 0;
            react_dist[i].polysaved = false;
        }
        react_dist[pb_global_const.maxreact].next = 0;
        pb_global.first_dist_in_pool = 1;
    }

    pb_global.react_pool_initialised = true;
}

void pool_reinit(void)
{
    int i;
    for (i = 1; i <= fmin(pb_global.mmax + 1, pb_global_const.maxarm); i++)
    {
        arm_pool[i].L1 = i - 1;
        arm_pool[i].R1 = i + 1;
        arm_pool[i].prio = 0;
        arm_pool[i].senio = 0;
    }
    arm_pool[1].L1 = 0;
    arm_pool[pb_global_const.maxarm].R1 = 0;
    pb_global.first_in_pool = 1;
    pb_global.mmax = 0;
}

bool request_arm(int *m_out)
{
    int m;
    m = (*m_out) = pb_global.first_in_pool;
    if (arm_pool[m].R1 == 0)
    {
        pb_global.arms_avail = false;
        return false;
    }
    else
    {
        pb_global.first_in_pool = arm_pool[m].R1;
        pb_global.mmax = fmax(pb_global.mmax, m);
        arm_pool[pb_global.first_in_pool].L1 = 0;
        arm_pool[m].L1 = 0;
        arm_pool[m].L2 = 0;
        arm_pool[m].R1 = 0;
        arm_pool[m].R2 = 0;
        arm_pool[m].up = 0;
        arm_pool[m].down = 0;
        arm_pool[m].ended = false;
        arm_pool[m].endfin = false;
        arm_pool[m].scission = false;
        pb_global.arms_left--;
        return true;
    }
}

void return_arm(int m)
{
    arm_pool[pb_global.first_in_pool].L1 = m;
    arm_pool[m].L1 = 0;
    arm_pool[m].L2 = 0;
    arm_pool[m].R1 = pb_global.first_in_pool;
    arm_pool[m].R2 = 0;
    arm_pool[m].up = 0;
    arm_pool[m].down = 0;
    arm_pool[m].ended = false;
    arm_pool[m].endfin = false;
    arm_pool[m].scission = false;
    pb_global.first_in_pool = m;
    pb_global.arms_avail = true;
    pb_global.arms_left++;
}

bool request_poly(int *m_out)
{
    int m;
    m = *m_out = pb_global.first_poly_in_pool;
    if (br_poly[m].nextpoly == 0)
    {
        pb_global.polys_avail = false;
        return false;
    }
    else
    {
        pb_global.first_poly_in_pool = br_poly[m].nextpoly;
        br_poly[m].nextpoly = 0;
        br_poly[m].saved = true;
        return true;
    }
}

void return_poly_arms(int n)
{
    int first, m1, mc;
    first = br_poly[n].first_end;
    if (first != 0)
    {
        m1 = first;
        while (true)
        {
            mc = arm_pool[m1].down;
            return_arm(m1);
            m1 = mc;
            if (m1 == first)
                break;
        }
    }
    br_poly[n].saved = false;
}

void return_poly(int n)
{
    // first return all arms of the polymer
    if (br_poly[n].saved)
    {
        return_poly_arms(n);
    }
    // then return polymer record to the pool
    br_poly[n].nextpoly = pb_global.first_poly_in_pool;
    pb_global.first_poly_in_pool = n;
    pb_global.polys_avail = true;
    br_poly[n].max_prio = 0;
    br_poly[n].max_senio = 0;
}

bool request_dist(int *m_out)
{
    int m;
    m = *m_out = pb_global.first_dist_in_pool;
    if (react_dist[m].next == 0)
    {
        pb_global.dists_avail = false;
        *m_out = 0;
        return false;
    }
    else
    {
        pb_global.first_dist_in_pool = react_dist[m].next;
        react_dist[m].next = 0;
        react_dist[m].first_poly = 0;
        react_dist[m].nummwdbins = 100;
        react_dist[m].numbobbins = 100;
        react_dist[m].boblgmin = 1.0;
        react_dist[m].boblgmax = 9.0;
        react_dist[m].bobbinmax = 2;
        react_dist[m].polysaved = false;
        react_dist[m].simnumber++;
        return true;
    }
}

void return_dist(int n)
{
    int m1, mc;
    if (n != 0)
    {
        // first return all polymers of the distribution
        m1 = react_dist[n].first_poly;
        while (m1 != 0)
        {
            mc = br_poly[m1].nextpoly;
            return_poly(m1);
            m1 = mc;
        }
        // then return distribution record to the pool
        react_dist[n].next = pb_global.first_dist_in_pool;
        pb_global.first_dist_in_pool = n;
        pb_global.dists_avail = true;
        react_dist[n].polysaved = false;
        // hold architecture statistics:
        react_dist[n].nlin = 0;
        react_dist[n].nstar = 0;
        react_dist[n].nH = 0;
        react_dist[n].n5arm = 0;
        react_dist[n].n7arm = 0;
        react_dist[n].ncomb = 0;
        react_dist[n].nother = 0;
    }
}

void return_dist_polys(int n)
{
    int m1, mc;
    // return all polymers of the distribution
    m1 = react_dist[n].first_poly;
    while (m1 != 0)
    {
        mc = br_poly[m1].nextpoly;
        return_poly(m1);
        m1 = mc;
    }
    react_dist[n].first_poly = 0;
    react_dist[n].polysaved = false;
    react_dist[n].simnumber++;
    // reset stats
    react_dist[n].nlin = 0;
    react_dist[n].nstar = 0;
    react_dist[n].nH = 0;
    react_dist[n].n5arm = 0;
    react_dist[n].n7arm = 0;
    react_dist[n].ncomb = 0;
    react_dist[n].nother = 0;
}

void armupdown(int m, int m1)
{
    arm_pool[m1].down = arm_pool[m].down;
    arm_pool[m].down = m1;
    arm_pool[m1].up = m;
    arm_pool[arm_pool[m1].down].up = m1;
}

// arm *return_arm_pool(int i)
// {
//     return &(arm_pool[i]);
// }

// polymer *return_br_poly(int i)
// {
//     return &(br_poly[i]);
// }

reactresults *return_react_dist(int i)
{
    return &(react_dist[i]);
}

void set_br_poly_nextpoly(int m, int nextpol)
{
    br_poly[m].nextpoly = nextpol;
}

bool increase_arm_records_in_arm_pool(int new_size)
{
    int current_size, i;

    current_size = pb_global_const.maxarm;
    arm *new_arm_pool;
    new_arm_pool = (arm *)realloc(arm_pool, sizeof(arm) * (new_size + 1));
    if (new_arm_pool == NULL) //failed to allocate new memory
    {
        return false;
    }
    arm_pool = new_arm_pool;
    for (i = current_size + 1; i <= new_size; i++)
    {
        return_arm(i);
    }
    pb_global_const.maxarm = new_size;
    pb_global.polys_avail = true;
    return true;
}

bool increase_polymer_records_in_br_poly(int new_size)
{
    int current_size, i;
    current_size = pb_global_const.maxpol;
    polymer *new_br_poly;
    new_br_poly = (polymer *)realloc(br_poly, sizeof(polymer) * (new_size + 1));
    if (new_br_poly == NULL) //failed to allocate new memory
    {
        return false;
    }
    br_poly = new_br_poly;
    for (i = current_size + 1; i <= new_size; i++)
    {
        br_poly[i].nextpoly = i + 1;
    }
    br_poly[current_size].nextpoly = current_size + 1;
    br_poly[new_size].nextpoly = 0;
    pb_global_const.maxpol = new_size;
    pb_global.polys_avail = true;
    return true;
}

bool increase_dist_records_in_react_dist(int new_size)
{
    int current_size, i;

    current_size = pb_global_const.maxreact;
    reactresults *new_react_dist;
    new_react_dist = (reactresults *)realloc(react_dist, sizeof(reactresults) * (new_size + 1));
    if (new_react_dist == NULL) //failed to allocate new memory
    {
        return false;
    }
    react_dist = new_react_dist;
    for (i = current_size + 1; i <= new_size; i++)
    {
        react_dist[i].wt = (double *)malloc(sizeof(double) * (pb_global_const.maxmwdbins + 1));
        react_dist[i].avbr = (double *)malloc(sizeof(double) * (pb_global_const.maxmwdbins + 1));
        react_dist[i].wmass = (double *)malloc(sizeof(double) * (pb_global_const.maxmwdbins + 1));
        react_dist[i].avg = (double *)malloc(sizeof(double) * (pb_global_const.maxmwdbins + 1));
        react_dist[i].lgmid = (double *)malloc(sizeof(double) * (pb_global_const.maxmwdbins + 1));
        react_dist[i].numinbin = (int *)malloc(sizeof(int) * (pb_global_const.maxbobbins + 1));

        react_dist[i].next = i + 1;
        react_dist[i].nummwdbins = 100;
        react_dist[i].numbobbins = 100;
        react_dist[i].boblgmin = 1.0;
        react_dist[i].boblgmax = 9.0;
        react_dist[i].bobbinmax = 2;
        react_dist[i].simnumber = 0;
        react_dist[i].polysaved = false;
    }
    react_dist[current_size].next = current_size + 1;
    react_dist[new_size].next = 0;
    pb_global.first_dist_in_pool = current_size;
    pb_global_const.maxreact = new_size;
    pb_global.dists_avail = true;
    return true;
}
