#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>
#include "polybits.h"
#include "binsandbob.h"
#include "multimetCSTR.h"
#include "polymassrg.h"
#include "ran3.h"

mulmetCSTR_global MMCSTR_global = {.mulmetCSTRnumber = 1, .mulmetCSTRerrorflag = false};
long iy3;

/* local functions */
static void mulmet_grow(int dir, int m, int cur_cat);
static void calclength(int catnum, double *r);
static void getcat(int *catnum);
static bool init_local_arrays(int n);

/* local variables */
static int scount, bcount, rlevel, numcats;
static double *cpM=NULL, *Nx=NULL;             // array [1..10] of double;
static double **cpU=NULL, **cpD1=NULL, **cpD2=NULL; //array [1..10,1..10] of double;
static bool local_arrays_initialized = false;

void mulmetCSTRstart(double *kp, double *kdb, double *ks, double *kplcb, double *yconc, double tau, double mconc, int n, int ndist)
// void mulmetCSTRstart(double tau, double mconc, int n, int ndist)
{
    double *pM, *hsp, *pconc, *kpM; //array [1..10] of double;
    double **pU, **pD1, **pD2;      //array [1..10,1..10] of double;
    double s, h1, h2, sum;
    int i, j;

    numcats = n;
    if (!init_local_arrays(n))
    {
        printf("IN FILE 'multimetCSTR.c' IN FUNCTION 'init_local_arrays'");
        printf("ERROR DURRING MEMORY ALLOCATION");
        return;
    }
    //initialize function-local arrays
    pM = (double *)malloc(sizeof(double) * (n + 1));
    hsp = (double *)malloc(sizeof(double) * (n + 1));
    pconc = (double *)malloc(sizeof(double) * (n + 1));
    kpM = (double *)malloc(sizeof(double) * (n + 1));
    pU = (double **)malloc(sizeof(double *) * (n + 1));
    pD1 = (double **)malloc(sizeof(double *) * (n + 1));
    pD2 = (double **)malloc(sizeof(double *) * (n + 1));
    for (i = 0; i <= numcats; i++)
    {
        pU[i] = (double *)malloc(sizeof(double) * (n + 1));
        pD1[i] = (double *)malloc(sizeof(double) * (n + 1));
        pD2[i] = (double *)malloc(sizeof(double) * (n + 1));
    }
    bobinit(ndist);
    iy3 = time(NULL); //initialize seed

    // from reactor to simulation variables
    s = 1.0 / tau;
    sum = 0.0;
    h1 = 0.0;
    h2 = 0.0;
    for (i = 1; i <= n; i++)
    {
        hsp[i] = s + kdb[i - 1] + ks[i - 1];
        kpM[i] = kp[i - 1] * mconc;
        pconc[i] = yconc[i - 1] * kpM[i] / (hsp[i] + kpM[i]);
        h1 = h1 + pconc[i] * kplcb[i - 1];
        h2 = h2 + pconc[i] * kdb[i - 1];
        pM[i] = pconc[i] * kpM[i];
        sum = sum + pM[i];
    }

    // calculate probabilities and Nx
    for (i = 1; i <= n; i++)
    {
        pM[i] = pM[i] / sum;
        Nx[i] = kpM[i] * (s + h1) / (hsp[i] * (s + h1) + kplcb[i - 1] * h2);
        for (j = 1; j <= n; j++)
        {
            pU[i][j] = kplcb[i - 1] * kdb[j - 1] * pconc[j] / (hsp[i] * (s + h1) + kplcb[i - 1] * h2);
            pD1[i][j] = pU[i][j];
            pD2[i][j] = kplcb[i - 1] * kdb[j - 1] * pconc[i] / (hsp[j] * (s + h1) + kplcb[j - 1] * h2);
        }
    }

    // cumulative probabilities
    cpM[1] = pM[1];
    for (i = 2; i <= n - 1; i++)
    {
        cpM[i] = cpM[i - 1] + pM[i];
    }
    cpM[n] = 1.0; //just to make sure!

    for (i = 1; i <= n; i++)
    {
        cpU[i][1] = pU[i][1];
        cpD1[i][1] = pD1[i][1];
        for (j = 2; j <= n; j++)
        {
            cpU[i][j] = cpU[i][j - 1] + pU[i][j];
            cpD1[i][j] = cpD1[i][j - 1] + pD1[i][j];
        }
    }

    for (j = 1; j <= n; j++)
    {
        // NB this is cumulative in the other direction!
        cpD2[1][j] = cpD1[j][n] + pD2[1][j];
        for (i = 2; i <= n; i++)
        {
            cpD2[i][j] = cpD2[i - 1][j] + pD2[i][j];
        }
    }
    MMCSTR_global.mulmetCSTRerrorflag = false;
}

bool mulmetCSTR(int n, int n1)
{
    double seg_len1, seg_len2, len1, len2, jtot, gfact;
    int m, m1, first, cur_cat, anum, nsegs;

    scount = 0;
    bcount = 0;
    getcat(&cur_cat);
    if (request_arm(&m))
    { // don't do anything if arms not available
        br_poly[n].first_end = m;
        arm_pool[m].up = m;
        arm_pool[m].down = m;
        calclength(cur_cat, &seg_len1);
        calclength(cur_cat, &seg_len2);
        arm_pool[m].arm_len = seg_len1 + seg_len2;
        arm_pool[m].armcat = cur_cat;
        rlevel = 0;
        mulmet_grow(1, m, cur_cat);
        mulmet_grow(-1, m, cur_cat);
    }
    if (pb_global.arms_avail)
    { // not true if we ran out of arms somewhere !

        // polyclean(n);  // clean-up not necessary?

        // renumber segments starting from zero

        m1 = br_poly[n].first_end;
        first = m1;
        anum = 0;
        arm_pool[m1].armnum = anum;
        m1 = arm_pool[m1].down;
        while (m1 != first)
        {
            anum++;
            arm_pool[m1].armnum = anum;
            m1 = arm_pool[m1].down;
        }
        first = br_poly[n].first_end;
        mass_segs(first, &len1, &nsegs);
        br_poly[n].num_br = bcount;
        br_poly[n].tot_len = len1;
        mass_rg2(first, 1.0, &len2, &jtot, &gfact);
        br_poly[n].gfactor = gfact;

        // check to see whether to save the polymer
        bobcount(n, n1);
        return true;
    }
    else
    {
        return false;
    }
}

void mulmet_grow(int dir, int m, int cur_cat)
{
    int m1, m2, new_cat;
    double seg_len, rnd;

    rlevel++; //recursion level
    if ((rlevel > 5000) || MMCSTR_global.mulmetCSTRerrorflag)
    {
        MMCSTR_global.mulmetCSTRerrorflag = true;
        rlevel = 100000;
        return;
    }

    if (pb_global.arms_avail)
    { // don't do anything if arms aren't available
        if (dir < 0)
        { // it's the upstream direction
            rnd = ran3(&iy3);
            if (rnd <= cpU[cur_cat][numcats])
            { // if true, there's a branch
                bcount++;
                new_cat = 1;
                while (rnd > cpU[cur_cat][new_cat])
                {
                    new_cat++; // find what sort of branch
                }
                if (new_cat > numcats)
                {
                    new_cat = numcats;
                }
                if (request_arm(&m1))
                { // return false if arms not available
                    armupdown(m, m1);
                    if (request_arm(&m2))
                    {
                        armupdown(m, m2);
                        calclength(cur_cat, &seg_len);
                        arm_pool[m1].arm_len = seg_len; // m1 is continuation of current catalyst
                        arm_pool[m1].armcat = cur_cat;
                        calclength(new_cat, &seg_len);
                        arm_pool[m2].arm_len = seg_len; // m2 is taken from new catalyst
                        arm_pool[m2].armcat = new_cat;

                        //connections
                        arm_pool[m].L1 = -m1;
                        arm_pool[m1].R2 = m;
                        arm_pool[m].L2 = -m2;
                        arm_pool[m2].R1 = m;
                        arm_pool[m1].R1 = -m2;
                        arm_pool[m2].R2 = -m1;

                        mulmet_grow(-1, m1, cur_cat); // recursive calls for two new arms
                        mulmet_grow(-1, m2, new_cat);
                    }
                }
            }
        }
        else
        { // it's the downstream direction
            rnd = ran3(&iy3);
            if (rnd <= cpD1[cur_cat][numcats])
            { // if true, there's a branch, of type 1
                bcount++;
                new_cat = 1;
                while (rnd > cpD1[cur_cat][new_cat])
                {
                    new_cat++; // find what sort of branch
                }
                if (new_cat > numcats)
                {
                    new_cat = numcats;
                }
                if (request_arm(&m1))
                { // return false if arms not available
                    armupdown(m, m1);
                    if (request_arm(&m2))
                    {
                        armupdown(m, m2);
                        calclength(cur_cat, &seg_len);
                        arm_pool[m1].arm_len = seg_len; // m1 is continuation of current catalyst
                        arm_pool[m1].armcat = cur_cat;
                        calclength(new_cat, &seg_len);
                        arm_pool[m2].arm_len = seg_len; // m2 is taken from new catalyst
                        arm_pool[m2].armcat = new_cat;

                        //connections
                        arm_pool[m].R1 = m1;
                        arm_pool[m1].L2 = -m;
                        arm_pool[m].R2 = -m2;
                        arm_pool[m2].R1 = -m;
                        arm_pool[m1].L1 = -m2;
                        arm_pool[m2].R2 = m1;

                        // recursive calls for two new arms
                        mulmet_grow(1, m1, cur_cat);  // continued downstream
                        mulmet_grow(-1, m2, new_cat); // new catalyst upstream
                    }
                }
            }
            else if (rnd <= cpD2[numcats][cur_cat])
            { // if true, there's a branch, of type 2
                bcount++;
                new_cat = 1;
                while (rnd > cpD2[new_cat][cur_cat])
                {
                    new_cat++; // find what sort of branch
                }
                if (new_cat > numcats)
                {
                    new_cat = numcats;
                }
                if (request_arm(&m1))
                { // return false if arms not available
                    armupdown(m, m1);
                    if (request_arm(&m2))
                    {
                        armupdown(m, m2);
                        calclength(new_cat, &seg_len);
                        arm_pool[m1].arm_len = seg_len; // m1 is downstream direction of new catalyst
                        arm_pool[m1].armcat = new_cat;
                        calclength(new_cat, &seg_len);
                        arm_pool[m2].arm_len = seg_len; // m2 is upstream, taken from new catalyst
                        arm_pool[m2].armcat = new_cat;

                        //connections
                        arm_pool[m].R1 = m1;
                        arm_pool[m1].L2 = -m;
                        arm_pool[m].R2 = -m2;
                        arm_pool[m2].R1 = -m;
                        arm_pool[m1].L1 = -m2;
                        arm_pool[m2].R2 = m1;

                        // recursive calls for two new arms
                        mulmet_grow(1, m1, new_cat);  // continued downstream
                        mulmet_grow(-1, m2, new_cat); // new catalyst upstream
                    }
                }
            } // end if for downstream branching
        }     // end direction checks
    }         //end check for arms available
    rlevel--;
}

void calclength(int catnum, double *r)
{
    // Calculates initial length of a segment from catalyst catnum
    double rnd;
    rnd = ran3(&iy3);
    if (rnd == 0.0)
    {
        rnd = 1.0;
    }
    *r = -Nx[catnum] * log(rnd);
    *r = fmax((*r), 1.0);
}

void getcat(int *catnum)
{
    // Choose catalyst at random from polymerised monomers
    double rnd;
    rnd = ran3(&iy3);
    *catnum = 1;
    while (rnd > cpM[*catnum])
    {
        *catnum = (*catnum) + 1;
    }
}

bool init_local_arrays(int n)
{   
    int i, j;
    static int old_n = -1;
    if (old_n == n)
        return true;

    // realloc double *
    {
        double *temp_p;
        temp_p = (double *)realloc(cpM, sizeof(double) * (n + 1));
        if (temp_p == NULL) //failed to allocate new memory
            return false;
        else
            cpM = temp_p;
    }
    {
        double *temp_p;
        temp_p = (double *)realloc(Nx, sizeof(double) * (n + 1));
        if (temp_p == NULL) //failed to allocate new memory
            return false;
        else
            Nx = temp_p;
    }
    if (n < old_n)
    {
        //reduce the size
        for (i = 0; i <= old_n; i++)
        {
            {
                double *temp_p;
                temp_p = (double *)realloc(cpU[i], sizeof(double) * (n + 1));
                if (temp_p == NULL) //failed to allocate new memory
                    return false;
                else
                    cpU[i] = temp_p;
            }
            {
                double *temp_p;
                temp_p = (double *)realloc(cpD1[i], sizeof(double) * (n + 1));
                if (temp_p == NULL) //failed to allocate new memory
                    return false;
                else
                    cpD1[i] = temp_p;
            }
            {
                double *temp_p;
                temp_p = (double *)realloc(cpD2[i], sizeof(double) * (n + 1));
                if (temp_p == NULL) //failed to allocate new memory
                    return false;
                else
                    cpD2[i] = temp_p;
            }
        }
    }

    // realloc double **
    {
        double **temp_pp;
        temp_pp = (double **)realloc(cpU, sizeof(double *) * (n + 1));
        if (temp_pp == NULL) //failed to allocate new memory
            return false;
        else
            cpU = temp_pp;
    }
    {
        double **temp_pp;
        temp_pp = (double **)realloc(cpD1, sizeof(double *) * (n + 1));
        if (temp_pp == NULL) //failed to allocate new memory
            return false;
        else
            cpD1 = temp_pp;
    }
    {
        double **temp_pp;
        temp_pp = (double **)realloc(cpD2, sizeof(double *) * (n + 1));
        if (temp_pp == NULL) //failed to allocate new memory
            return false;
        else
            cpD2 = temp_pp;
    }
    if (n > old_n)
    {
        //reallocate (realloc) up to old_size
        for (i = 0; i <= old_n; i++)
        {
            {
                double *temp_p;
                temp_p = (double *)realloc(cpU[i], sizeof(double) * (n + 1));
                if (temp_p == NULL) //failed to allocate new memory
                    return false;
                else
                    cpU[i] = temp_p;
            }
            {
                double *temp_p;
                temp_p = (double *)realloc(cpD1[i], sizeof(double) * (n + 1));
                if (temp_p == NULL) //failed to allocate new memory
                    return false;
                else
                    cpD1[i] = temp_p;
            }
            {
                double *temp_p;
                temp_p = (double *)realloc(cpD2[i], sizeof(double) * (n + 1));
                if (temp_p == NULL) //failed to allocate new memory
                    return false;
                else
                    cpD2[i] = temp_p;
            }
        }
        for (i = old_n + 1; i <= n; i++)
        {
            //allocate (malloc) the new arrays
            cpU[i] = (double *)malloc(sizeof(double) * (n + 1));
            cpD1[i] = (double *)malloc(sizeof(double) * (n + 1));
            cpD2[i] = (double *)malloc(sizeof(double) * (n + 1));
        }
    }
    //initialize all values to '0.0'
    for (i = 0; i <= n; i++)
    {
        cpM[i] = 0.0;
        Nx[i] = 0.0;
        for (j = 0; j <= n; j++)
        {
            cpU[i][j] = 0.0;
            cpD1[i][j] = 0.0;
            cpD2[i][j] = 0.0;
        }
    }
    local_arrays_initialized = true;
    old_n = n;
    return true;
}