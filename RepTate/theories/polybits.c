#include <stdlib.h>

#include "my_structs.h"
#include "polybits.h"

int maxbobbins = 5000;
int maxmwdbins = 1000;
int maxarm = 1000000; //  maxarm=10000000;
int maxpol = 1000000;
int maxreact = 11;

arm *arm_pool;
polymer *br_poly;
reactresults *react_dist;

int first_in_pool = 0;
int first_poly_in_pool = 0;
int first_dist_in_pool = 0;
int mmax = 0;
int num_react = 0;
int arms_left = 0;
bool react_pool_initialised = false;
bool react_pool_declared = false;
bool arms_avail = true;  // these flags simply record
bool polys_avail = true; // availability of arms
bool dists_avail = true;

// initialises pools - MUST BE CALLED FIRST TO USE THESE ROUTINES
void react_pool_init(void)
{
    if (!react_pool_initialised)
    {
        int i;
        arm_pool = (arm *)malloc(sizeof(arm) * (maxarm + 1));
        br_poly = (polymer *)malloc(sizeof(polymer) * (maxpol + 1));
        react_dist = (reactresults *)malloc(sizeof(reactresults) * (maxreact + 1));
        for (i = 1; i <= maxreact; i++)
        {
            react_dist[i].wt = (double *)malloc(sizeof(double) * (maxmwdbins + 1));
            react_dist[i].avbr = (double *)malloc(sizeof(double) * (maxmwdbins + 1));
            react_dist[i].wmass = (double *)malloc(sizeof(double) * (maxmwdbins + 1));
            react_dist[i].avg = (double *)malloc(sizeof(double) * (maxmwdbins + 1));
            react_dist[i].lgmid = (double *)malloc(sizeof(double) * (maxmwdbins + 1));
            react_dist[i].numinbin = (int *)malloc(sizeof(int) * (maxbobbins + 1));
        }
        for (i = 1; i <= maxarm; i++)
        {
            arm_pool[i].L1 = i - 1;
            arm_pool[i].R1 = i + 1;
        }
        arm_pool[1].L1 = 0;
        arm_pool[maxarm].R1 = 0;
        first_in_pool = 1;
        mmax = 0;
        arms_left = maxarm;

        for (i = 1; i <= maxpol - 1; i++)
        {
            br_poly[i].nextpoly = i + 1;
        }
        br_poly[maxpol].nextpoly = 0;
        first_poly_in_pool = 1;

        for (i = 1; i <= maxreact; i++)
        {
            react_dist[i].next = i + 1;
            react_dist[i].nummwdbins = 100;
            react_dist[i].numbobbins = 100;
            react_dist[i].boblgmin = 1.0;
            react_dist[i].boblgmax = 9.0;
            react_dist[i].bobbinmax = 2;
            react_dist[i].simnumber = 0;
        }
        react_dist[maxreact].next = 0;
        first_dist_in_pool = 1;
    }

    react_pool_initialised = true;
}

void pool_reinit(void)
{
    int i;
    for (i = 1; i <= MIN(mmax + 1, maxarm); i++)
    {
        arm_pool[i].L1 = i - 1;
        arm_pool[i].R1 = i + 1;
    }
    arm_pool[1].L1 = 0;
    arm_pool[maxarm].R1 = 0;
    first_in_pool = 1;
    mmax = 0;
}

bool request_arm(int *m_out)
{
    int m;
    m = (*m_out) = first_in_pool;
    if (arm_pool[m].R1 == 0)
    {
        ///  need to decide what to do if you run out of arms!
        ///
        //   if (MessageDlg('Ran out of arms, exit?',
        //      mtConfirmation, [mbYes, mbNo], 0) = mrYes) then
        //    exit;
        arms_avail = false;
        return false;
    }
    else
    {
        first_in_pool = arm_pool[m].R1;
        mmax = MAX(mmax, m);
        arm_pool[first_in_pool].L1 = 0;
        arm_pool[m].L1 = 0;
        arm_pool[m].L2 = 0;
        arm_pool[m].R1 = 0;
        arm_pool[m].R2 = 0;
        arm_pool[m].up = 0;
        arm_pool[m].down = 0;
        arm_pool[m].ended = false;
        arm_pool[m].endfin = false;
        arm_pool[m].scission = false;
        arms_left--;
        return true;
    }
}

void return_arm(int m)
{
    arm_pool[first_in_pool].L1 = m;
    arm_pool[m].L1 = 0;
    arm_pool[m].L2 = 0;
    arm_pool[m].R1 = first_in_pool;
    arm_pool[m].R2 = 0;
    arm_pool[m].up = 0;
    arm_pool[m].down = 0;
    arm_pool[m].ended = false;
    arm_pool[m].endfin = false;
    arm_pool[m].scission = false;
    first_in_pool = m;
    arms_avail = true;
    arms_left++;
}

bool request_poly(int *m_out)
{
    int m;
    m = *m_out = first_poly_in_pool;
    if (br_poly[m].nextpoly == 0)
    {
        ///  need to decide what to do if you run out of polymers!
        ///
        //   if (MessageDlg('Ran out of polymers, exit?',
        //      mtConfirmation, [mbYes, mbNo], 0) = mrYes) then
        //    exit;
        polys_avail = false;
        return false;
    }
    else
    {
        first_poly_in_pool = br_poly[m].nextpoly;
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
    br_poly[n].nextpoly = first_poly_in_pool;
    first_poly_in_pool = n;
    polys_avail = true;
}

bool request_dist(int *m_out)
{
    int m;
    m = *m_out = first_dist_in_pool;
    if (react_dist[m].next == 0)
    {
        ///  need to decide what to do if you run out of distributions!
        ///
        //   if (MessageDlg('Ran out of distributions, exit?',
        //      mtConfirmation, [mbYes, mbNo], 0) = mrYes) then
        //    exit;
        dists_avail = false;
        *m_out = 0;
        return false;
    }
    else
    {
        first_dist_in_pool = react_dist[m].next;
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

void return_distint(int n)
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
        react_dist[n].next = first_dist_in_pool;
        first_dist_in_pool = n;
        dists_avail = true;
        react_dist[n].polysaved = false;
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
}

void armupdown(int m, int m1)
{
    arm_pool[m1].down = arm_pool[m].down;
    arm_pool[m].down = m1;
    arm_pool[m1].up = m;
    arm_pool[arm_pool[m1].down].up = m1;
}
