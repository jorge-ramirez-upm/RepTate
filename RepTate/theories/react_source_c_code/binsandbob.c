#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "polybits.h"
#include "binsandbob.h"

binsandbob_global bab_global = {.multi_m_w = 0, .multi_m_n = 0, .multi_brav = 0, .multi_nummwdbins = 0};

static double *multi_wt, *multi_avbr, *multi_wmass, *multi_avg, *multi_lgmid;
static void init_binsandbob_arrays(void);

// call this procedure to calculate current averages
//  and MWD for polymers made in distribution n
void molbin(int n)
{
    int i, ibin;
    double wttot, m_w, m_n, brav, lgstep, lgmin, lgmax, cplen;

    react_dist[n].nummwdbins = fmin(react_dist[n].nummwdbins, pb_global_const.maxmwdbins);
    // first find largest and smallest polymer
    lgmax = 0.0;
    lgmin = 1.0e80;

    i = react_dist[n].first_poly;
    while (true)
    {
        cplen = br_poly[i].tot_len;
        lgmax = fmax(lgmax, cplen);
        lgmin = fmin(lgmin, cplen);
        i = br_poly[i].nextpoly;
        if (i == 0)
        {
            break;
        }
    }
    lgmax = log10((lgmax * 1.01) * react_dist[n].monmass);
    lgmin = log10((lgmin / 1.01) * react_dist[n].monmass);
    lgstep = (lgmax - lgmin) / react_dist[n].nummwdbins;

    //initialise bins and other counters
    for (ibin = 1; ibin <= react_dist[n].nummwdbins; ibin++)
    {
        react_dist[n].wt[ibin] = 0.0;
        react_dist[n].avbr[ibin] = 0.0;
        react_dist[n].avg[ibin] = 0.0;
        react_dist[n].wmass[ibin] = 0.0;
    }
    wttot = 0.0;
    m_w = 0.0;
    m_n = 0.0;
    brav = 0.0;

    // the assumption here is that polymers have been created on a weight basis
    i = react_dist[n].first_poly;
    while (true)
    {
        cplen = br_poly[i].tot_len * react_dist[n].monmass;
        ibin = trunc((log10(cplen) - lgmin) / lgstep) + 1;
        wttot = wttot + 1.0;
        m_w = m_w + cplen;
        m_n = m_n + 1.0 / cplen;
        brav = brav + br_poly[i].num_br / br_poly[i].tot_len;
        if ((ibin <= react_dist[n].nummwdbins) && (ibin > 0))
        {
            react_dist[n].wt[ibin] = react_dist[n].wt[ibin] + 1.0;
            react_dist[n].avbr[ibin] = react_dist[n].avbr[ibin] + br_poly[i].num_br;
            react_dist[n].avg[ibin] = react_dist[n].avg[ibin] + br_poly[i].gfactor;
            react_dist[n].wmass[ibin] = react_dist[n].wmass[ibin] + br_poly[i].tot_len;
        }
        i = br_poly[i].nextpoly;
        if (i == 0)
        {
            break;
        }
    }
    // finalise bin data - ready for plotting
    for (ibin = 1; ibin <= react_dist[n].nummwdbins; ibin++)
    {
        react_dist[n].avbr[ibin] = react_dist[n].avbr[ibin] / (react_dist[n].wmass[ibin] + 1.0e-80) * 500.0;
        react_dist[n].avg[ibin] = react_dist[n].avg[ibin] / (react_dist[n].wt[ibin] + 1.0e-80);
        react_dist[n].wt[ibin] = react_dist[n].wt[ibin] / lgstep / wttot;
        react_dist[n].lgmid[ibin] = lgmin + ibin * lgstep - 0.5 * lgstep;
    }
    react_dist[n].m_w = m_w / wttot;
    react_dist[n].m_n = wttot / m_n;
    react_dist[n].brav = brav / wttot * 500.0;
}

// call this procedure to calculate current averages
//  and MWD for all polymers made in all distributions
// with weights contained in weights array, and whether "in the mix" contained
// in inmix array
// void multimolbin(int reqbins, double *weights, bool *inmix)
void multimolbin(int reqbins, double *weights, int *dists, int n_inmix)
{
    int i, ibin, n, dist;
    double wttot, m_w, m_n, brav, lgstep, lgmin, lgmax, cplen, wtpoly;

    bab_global.multi_nummwdbins = fmin(reqbins, pb_global_const.maxmwdbins);

    // first find largest and smallest polymer
    lgmax = 0.0;
    lgmin = 1.0e80;

    for (n = 0; n < n_inmix; n++)
    {
        if (weights[n] > 0.0)
        {
            dist = dists[n];
            i = react_dist[dist].first_poly;
            while (true)
            {
                cplen = br_poly[i].tot_len * react_dist[dist].monmass;
                lgmax = fmax(lgmax, cplen);
                lgmin = fmin(lgmin, cplen);
                i = br_poly[i].nextpoly;
                if (i == 0)
                {
                    break;
                }
            }
        }
    }

    lgmax = log10(lgmax * 1.01);
    lgmin = log10(lgmin / 1.01);
    lgstep = (lgmax - lgmin) / bab_global.multi_nummwdbins;

    //initialise bins and other counters
    for (ibin = 1; ibin <= bab_global.multi_nummwdbins; ibin++)
    {
        multi_wt[ibin] = 0.0;
        multi_avbr[ibin] = 0.0;
        multi_avg[ibin] = 0.0;
        multi_wmass[ibin] = 0.0;
    }

    wttot = 0.0;
    m_w = 0.0;
    m_n = 0.0;
    brav = 0.0;

    // the assumption here is that polymers have been created on a weight basis
    for (n = 0; n < n_inmix; n++)
    {
        if (weights[n] > 0.0)
        {
            dist = dists[n];
            i = react_dist[dist].first_poly;
            wtpoly = weights[n] / react_dist[dist].npoly;
            while (true)
            {
                cplen = br_poly[i].tot_len * react_dist[dist].monmass;
                ibin = trunc((log10(cplen) - lgmin) / lgstep) + 1;
                wttot = wttot + wtpoly;
                m_w = m_w + cplen * wtpoly;
                m_n = m_n + wtpoly / cplen;
                brav = brav + br_poly[i].num_br / br_poly[i].tot_len * wtpoly;
                if ((ibin <= bab_global.multi_nummwdbins) && (ibin > 0))
                {
                    multi_wt[ibin] = multi_wt[ibin] + wtpoly;
                    multi_avbr[ibin] = multi_avbr[ibin] + br_poly[i].num_br * wtpoly;
                    multi_avg[ibin] = multi_avg[ibin] + br_poly[i].gfactor * wtpoly;
                    multi_wmass[ibin] = multi_wmass[ibin] + br_poly[i].tot_len * wtpoly;
                }
                i = br_poly[i].nextpoly;
                if (i == 0)
                {
                    break;
                }
            }
        }
    }

    // finalise bin data - ready for plotting
    for (ibin = 1; ibin <= bab_global.multi_nummwdbins; ibin++)
    {
        multi_avbr[ibin] = multi_avbr[ibin] / (multi_wmass[ibin] + 1.0e-80) * 500.0;
        multi_avg[ibin] = multi_avg[ibin] / (multi_wt[ibin] + 1.0e-80);
        multi_wt[ibin] = multi_wt[ibin] / lgstep / wttot;
        multi_lgmid[ibin] = lgmin + ibin * lgstep - 0.5 * lgstep;
    }

    bab_global.multi_m_w = m_w / wttot;
    bab_global.multi_m_n = wttot / m_n;
    bab_global.multi_brav = brav / wttot * 500.0;
}

// call this before making any polymers
void init_binsandbob_arrays()
{
    static bool is_initialized = false;

    if (!is_initialized)
    {
        multi_wt = (double *)malloc(sizeof(double) * (pb_global_const.maxmwdbins + 1));
        multi_avbr = (double *)malloc(sizeof(double) * (pb_global_const.maxmwdbins + 1));
        multi_wmass = (double *)malloc(sizeof(double) * (pb_global_const.maxmwdbins + 1));
        multi_avg = (double *)malloc(sizeof(double) * (pb_global_const.maxmwdbins + 1));
        multi_lgmid = (double *)malloc(sizeof(double) * (pb_global_const.maxmwdbins + 1));
        is_initialized = true;
    }
}

// call this before making any polymers
void bobinit(int n)
{
    int i;

    init_binsandbob_arrays();
    for (i = 1; i <= react_dist[n].numbobbins; i++)
    {
        react_dist[n].numinbin[i] = 0;
    }
    react_dist[n].nsaved = 0;
}

// checks to see whether or not to save this polymer (polymer m, from react_dist n)!
void bobcount(int m, int n)
{
    int ibin;

    ibin = trunc((log10(br_poly[m].tot_len * react_dist[n].monmass) - react_dist[n].boblgmin) / (react_dist[n].boblgmax - react_dist[n].boblgmin) * react_dist[n].numbobbins) + 1;
    ibin = fmin(fmax(1, ibin), react_dist[n].numbobbins);
    react_dist[n].numinbin[ibin] = react_dist[n].numinbin[ibin] + 1;
    if (react_dist[n].numinbin[ibin] <= react_dist[n].bobbinmax)
    { //  check to see whether to "save" the polymer
        br_poly[m].saved = true;
        br_poly[m].bin = ibin;
        react_dist[n].nsaved = react_dist[n].nsaved + 1;
    }
    else
    {
        br_poly[m].saved = false;
        br_poly[m].bin = 0;
        return_poly_arms(m);
    }
}

void polyconfwrite(int n, char *fname)
{
    int i, atally, numarms, anum;
    int first, tL1, tL2, tR1, tR2, m1, mc, npoly;
    //F:    TextFile;
    double enrich, polywt, armwt, armz, N_e;
    FILE *fp;

    fp = fopen(fname, "w");

    react_dist[n].N_e = react_dist[n].M_e / react_dist[n].monmass;
    // opening lines
    fprintf(fp, "reactpol\n");
    fprintf(fp, "%f\n", react_dist[n].N_e);
    fprintf(fp, "%d\n", react_dist[n].nsaved);

    atally = 0;

    // loop through polymers, writing output
    npoly = react_dist[n].npoly;
    N_e = react_dist[n].N_e;
    i = react_dist[n].first_poly;
    while (true)
    {
        if (br_poly[i].saved)
        {

            if (react_dist[n].numinbin[br_poly[i].bin] <= react_dist[n].bobbinmax)
            {
                enrich = 1.0;
            }
            else
            {
                enrich = react_dist[n].numinbin[br_poly[i].bin] / react_dist[n].bobbinmax;
            }
            polywt = enrich / npoly;

            if (br_poly[i].num_br == 0)
            { //it's a linear polymer
                fprintf(fp, "2\n");
                atally = atally + 2;
                first = br_poly[i].first_end;
                armwt = 0.5 * arm_pool[first].arm_len / br_poly[i].tot_len / npoly * enrich;
                armz = 0.5 * arm_pool[first].arm_len / N_e;
                fprintf(fp, "%7d %7d %7d %7d %20.13e %20.13e\n", -1, -1, 1, -1, armz, armwt);
                fprintf(fp, "%7d %7d %7d %7d %20.13e %20.13e\n", 0, -1, -1, -1, armz, armwt);
            }
            else
            { // it's a branched polymer
                numarms = 2 * br_poly[i].num_br + 1;
                fprintf(fp, "%d\n", numarms); //number of arms
                atally = atally + numarms;
                first = br_poly[i].first_end;

                //renumber segments starting from zero
                m1 = first;
                anum = 0;
                while (true)
                {
                    arm_pool[m1].armnum = anum;
                    m1 = arm_pool[m1].down;
                    anum = anum + 1;
                    if (m1 == first)
                    {
                        break;
                    }
                }
                // now do output - loop over arms
                m1 = first;
                while (true)
                {
                    armwt = arm_pool[m1].arm_len / br_poly[i].tot_len / npoly * enrich;
                    armz = arm_pool[m1].arm_len / N_e;
                    if (arm_pool[m1].L1 == 0)
                    {
                        tL1 = -1;
                    }
                    else
                    {
                        mc = abs(arm_pool[m1].L1);
                        tL1 = arm_pool[mc].armnum;
                    }
                    if (arm_pool[m1].L2 == 0)
                    {
                        tL2 = -1;
                    }
                    else
                    {
                        mc = abs(arm_pool[m1].L2);
                        tL2 = arm_pool[mc].armnum;
                    }
                    if (arm_pool[m1].R1 == 0)
                    {
                        tR1 = -1;
                    }
                    else
                    {
                        mc = abs(arm_pool[m1].R1);
                        tR1 = arm_pool[mc].armnum;
                    }
                    if (arm_pool[m1].R2 == 0)
                    {
                        tR2 = -1;
                    }
                    else
                    {
                        mc = abs(arm_pool[m1].R2);
                        tR2 = arm_pool[mc].armnum;
                    }
                    fprintf(fp, "%7d %7d %7d %7d %20.13e %20.13e\n", tL1, tL2, tR1, tR2, armz, armwt);

                    m1 = arm_pool[m1].down;

                    if (m1 == first)
                    { //end output loop over arms
                        break;
                    }
                }
            } // end of if (it's a linear or branched polymer )

        } //end of "if saved"
        i = br_poly[i].nextpoly;
        if (i == 0)
        {
            break;
        }

    } //end of loop over polymers

    fclose(fp);
}

// version for mixtures
void multipolyconfwrite(char *fname, double *weights, bool *inmix, int *numsaved_out)
{
    int i, atally, numarms, anum, n, nmix;
    int first, tL1, tL2, tR1, tR2, m1, mc, npoly;
    // F: TextFile;
    double enrich, polywt, armwt, armz, N_e, N_e_av, distwt;
    FILE *fp;

    fp = fopen(fname, "w");

    // count polymers over all distributions
    *numsaved_out = 0;
    nmix = 0;
    N_e_av = 0;

    for (n = 1; n <= 10; n++)
    {
        if (inmix[n - 1])
        {
            react_dist[n].N_e = react_dist[n].M_e / react_dist[n].monmass;
            N_e_av = N_e_av + react_dist[n].N_e;
            nmix++;
            *numsaved_out = (*numsaved_out) + react_dist[n].nsaved;
        }
    }
    N_e_av = N_e_av / nmix;

    // opening lines
    fprintf(fp, "reactmix\n");
    fprintf(fp, "%g\n", N_e_av);
    fprintf(fp, "%d\n", *numsaved_out);

    atally = 0;

    // now loop through distributions writing output
    for (n = 1; n <= 10; n++)
    {
        if (inmix[n - 1])
        {
            distwt = weights[n - 1];

            // loop through polymers, writing output
            npoly = react_dist[n].npoly;
            N_e = react_dist[n].N_e;
            i = react_dist[n].first_poly;
            while (true)
            {
                if (br_poly[i].saved)
                {
                    if (react_dist[n].numinbin[br_poly[i].bin] <= react_dist[n].bobbinmax)
                    {
                        enrich = 1.0;
                    }
                    else
                    {
                        enrich = react_dist[n].numinbin[br_poly[i].bin] / react_dist[n].bobbinmax;
                    }
                    polywt = enrich / npoly * distwt;

                    if (br_poly[i].num_br == 0)
                    { //it's a linear polymer
                        fprintf(fp, "2\n");
                        atally = atally + 2;
                        first = br_poly[i].first_end;
                        armwt = 0.5 * arm_pool[first].arm_len / br_poly[i].tot_len * polywt;
                        armz = 0.5 * arm_pool[first].arm_len / N_e;
                        fprintf(fp, "%7d %7d %7d %7d %20.13e %20.13e\n", -1, -1, 1, -1, armz, armwt);
                        fprintf(fp, "%7d %7d %7d %7d %20.13e %20.13e\n", 0, -1, -1, -1, armz, armwt);
                    }
                    else
                    { // it's a branched polymer
                        numarms = 2 * br_poly[i].num_br + 1;
                        fprintf(fp, "%d\n", numarms); //number of arms
                        atally = atally + numarms;
                        first = br_poly[i].first_end;

                        //renumber segments starting from zero
                        m1 = first;
                        anum = 0;
                        while (true)
                        {
                            arm_pool[m1].armnum = anum;
                            m1 = arm_pool[m1].down;
                            anum = anum + 1;
                            if (m1 == first)
                            {
                                break;
                            }
                        }
                        // now do output - loop over arms
                        m1 = first;
                        while (true)
                        {
                            armwt = arm_pool[m1].arm_len / br_poly[i].tot_len * polywt;
                            armz = arm_pool[m1].arm_len / N_e;
                            if (arm_pool[m1].L1 == 0)
                            {
                                tL1 = -1;
                            }
                            else
                            {
                                mc = abs(arm_pool[m1].L1);
                                tL1 = arm_pool[mc].armnum;
                            }
                            if (arm_pool[m1].L2 == 0)
                            {
                                tL2 = -1;
                            }
                            else
                            {
                                mc = abs(arm_pool[m1].L2);
                                tL2 = arm_pool[mc].armnum;
                            }
                            if (arm_pool[m1].R1 == 0)
                            {
                                tR1 = -1;
                            }
                            else
                            {
                                mc = abs(arm_pool[m1].R1);
                                tR1 = arm_pool[mc].armnum;
                            }
                            if (arm_pool[m1].R2 == 0)
                            {
                                tR2 = -1;
                            }
                            else
                            {
                                mc = abs(arm_pool[m1].R2);
                                tR2 = arm_pool[mc].armnum;
                            }
                            fprintf(fp, "%7d %7d %7d %7d %20.13e %20.13e\n", tL1, tL2, tR1, tR2, armz, armwt);

                            m1 = arm_pool[m1].down;

                            if (m1 == first)
                            {
                                break;
                            }
                        } //end output loop over arms

                    } // end of if (it's a linear or branched polymer )

                } //end of "if saved"
                i = br_poly[i].nextpoly;
                if (i == 0)
                {
                    break;
                } //end of loop over polymers
            }
        }
    } // end of loop over distributions

    fclose(fp);
}

double return_binsandbob_multi_avbr(int i)
{
    return multi_avbr[i];
}

double return_binsandbob_multi_avg(int i)
{
    return multi_avg[i];
}

double return_binsandbob_multi_lgmid(int i)
{
    return multi_lgmid[i];
}

double return_binsandbob_multi_wmass(int i)
{
    return multi_wmass[i];
}

double return_binsandbob_multi_wt(int i)
{
    return multi_wt[i];
}
