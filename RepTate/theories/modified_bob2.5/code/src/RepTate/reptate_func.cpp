// RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
// --------------------------------------------------------------------------------------------------------

// Authors:
//     Jorge Ramirez, jorge.ramirez@upm.es
//     Victor Boudara, victor.boudara@gmail.com
//     Chinmay Das, chinmaydas@yahoo.com

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
//    THE FOLLOWING IS FOR REPTATE COMPATIBILITY
#include <stdio.h>
#include <cstdlib>
#include <exception>
#include <math.h>
#include "../../include/bob.h"
#include "../calc/topology/gpcls.h"
#include "reptate_func.h"

// flag stop bob calculation
void set_flag_stop_bob(bool b){
    extern bool flag_stop_bob;
    flag_stop_bob = b;
}

// callback function: print to Python
pyprint_func *print_to_python;
pyprint_func *print_err_to_python;
// callback function: get double from Python
pyget_double *get_freqmin;
pyget_double *get_freqmax;
pyget_double *get_freqint;

void set_do_priority_seniority(bool b){
    do_priority_seniority = b;
}

void def_pyprint_func(pyprint_func F)
{
    // a normal bob output printed to Python
    print_to_python = F;
}
void def_pyprint_err_func(pyprint_func F)
{
    // used to print a error message to Python
    print_err_to_python = F;
}
void def_get_freqmin(pyget_double F)
{
    // get a double from Python
    get_freqmin = F;
}
void def_get_freqmax(pyget_double F)
{
    // get a double from Python
    get_freqmax = F;
}
void def_get_freqint(pyget_double F)
{
    // get a double from Python
    get_freqint = F;
}

void my_abort(char *s)
{
    if (reptate_flag)
    {
        print_err_to_python(s);
        throw std::exception();
    }
    else
    {
        printf("%s", s);
        abort();
    }
}

static double mn_out = 1, mw_out = 1;

void get_mn_mw(double *mn, double *mw)
{
    *mn = mn_out;
    *mw = mw_out;
}

void return_gpcls(int nbin, int ncomp, int ni, int nf, double *lgmid_out, double *wtbin_out, double *brbin_out, double *gbin_out)
{
    try
    {
        extern int max_poly;
        extern int max_arm;
        extern int num_poly;
        extern int GPCNumBin;
        GPCNumBin = nbin;
        extern std::vector<polymer> branched_poly;
        int n_cur_comp = nf - ni;
        double *mass_ar = new double[n_cur_comp];
        double *gfac_ar = new double[n_cur_comp];
        double *branch_ar = new double[n_cur_comp];
        double *wtfrac_ar = new double[n_cur_comp];
        for (int i = ni; i < nf; i++)
        {
            mass_ar[i - ni] = gpc_calc_mass(i);
            wtfrac_ar[i - ni] = gpc_calc_wtfrac(i);
            gfac_ar[i - ni] = gpc_calc_gfac(i);
            branch_ar[i - ni] = (double)gpc_num_br(i);
        }

        for (int i = ni; i < nf; i++)
        {
            branched_poly[i].molmass = mass_ar[i - ni];
            branched_poly[i].gfac = gfac_ar[i - ni];
            branched_poly[i].wtfrac = wtfrac_ar[i - ni];
        }

        double mwav, mnav, pdi;
        mwav = mnav = 0.0;
        double cur_wt_fraction = 0.0;

        for (int i = ni; i < nf; i++)
        {
            cur_wt_fraction += wtfrac_ar[i - ni];
        }

        for (int i = ni; i < nf; i++)
        {
            mnav += wtfrac_ar[i - ni] / mass_ar[i - ni];
            mwav += wtfrac_ar[i - ni] * mass_ar[i - ni];
        }

        mnav = cur_wt_fraction / mnav;
        mwav = mwav / cur_wt_fraction;

        pdi = mwav / mnav;

        mn_out = mnav;
        mw_out = mwav;

        if (ncomp < 0)
        { // global average
            // printf("GPC module for entire system  : \n");
        }
        else
        {
            // printf("GPC module for component %d  : \n", ncomp);
        }
        // printf("Mw = %e ,   Mn =  %e, PDI = %e \n", mwav, mnav, pdi);

        extern int ForceGPCTrace;
        if ((ForceGPCTrace != 0) && ((pdi - 1.0) < 1.0e-4))
        {
            printf("Too small PDI for useful GPC trace. \n");
            printf("  You can force GPC trace output by setting ForceGPCTrace in bob.rc\n");
        }
        else
        { // Calculate histograms.
            if (n_cur_comp < 20)
            {
                printf("Too few polymers for GPC histogram. \n");
            }
            else
            {
                return_gpchist(ncomp, n_cur_comp, mass_ar, gfac_ar, branch_ar, wtfrac_ar,
                               lgmid_out, wtbin_out, brbin_out, gbin_out);
            }
        }
        delete[] mass_ar;
        delete[] gfac_ar;
        delete[] branch_ar;
        delete[] wtfrac_ar;
    }
    catch (const std::exception &)
    {
        return;
    }
}

void return_gpchist(int ncomp, int n_cur_comp,
                    double *mass_ar, double *gfac_ar, double *branch_ar, double *wt_frac,
                    double *lgmid_out, double *wtbin_out, double *brbin_out, double *gbin_out)
{
    try
    {
        extern int GPCNumBin;
        extern double mass_mono;
        int nnn = GPCNumBin;
        if (nnn > (n_cur_comp / 5))
        {
            nnn = n_cur_comp / 5;
        }
        if (nnn < 2)
        {
            nnn = 2;
        }
        double *wtbin = new double[nnn];
        double *brbin = new double[nnn];
        double *gbin = new double[nnn];
        for (int i = 0; i < nnn; i++)
        {
            wtbin[i] = brbin[i] = gbin[i] = 0.0;
        }

        double massmin = 1.0e20;
        double massmax = 0.0;
        for (int i = 0; i < n_cur_comp; i++)
        {
            if (massmin > mass_ar[i])
            {
                massmin = mass_ar[i];
            }
            if (massmax < mass_ar[i])
            {
                massmax = mass_ar[i];
            }
        }

        if ((massmax - massmin) < 0.01)
        {
            printf("Polymers are too monodisperse for GPC histogram \n");
        }
        else
        {
            double lgmin = log10(massmin);
            double lgmax = log10(massmax);
            double lgstep = (lgmax - lgmin) / ((double)nnn);

            int indx;
            double wttot = 0.0;
            for (int i = 0; i < n_cur_comp; i++)
            {
                indx = (int)floor((log10(mass_ar[i]) - lgmin) / lgstep);
                indx++;
                if (indx > (nnn - 1))
                {
                    indx = nnn - 1;
                }

                // Changing here Oct 5 2008
                /* 
wtbin[indx]+=mass_ar[i]*wt_frac[i]; wttot+=mass_ar[i]*wt_frac[i];
brbin[indx]+=branch_ar[i]*wt_frac[i] * mass_mono * 500.0;
gbin[indx]+=gfac_ar[i]*mass_ar[i]*wt_frac[i];  */

                wtbin[indx] += wt_frac[i];
                wttot += wt_frac[i];
                brbin[indx] += branch_ar[i] * wt_frac[i] * mass_mono * 500.0 / (mass_ar[i]);
                gbin[indx] += gfac_ar[i] * wt_frac[i];
            }

            for (int i = 1; i < nnn; i++)
            {
                if (wtbin[i] > 1.0e-12)
                {
                    gbin[i] = gbin[i] / wtbin[i];
                }
                if (wtbin[i] > 1.0e-12)
                {
                    brbin[i] = brbin[i] / wtbin[i];
                }
                wtbin[i] = wtbin[i] / (lgstep * wttot);
            }
            for (int i = 1; i < nnn; i++)
            {
                double lgmid = lgmin + (((double)i) + 0.5) * lgstep;
                lgmid_out[i] = exp(lgmid * log(10.0));
                wtbin_out[i] = wtbin[i];
                brbin_out[i] = brbin[i];
                gbin_out[i] = gbin[i];
            }
        }
        delete[] wtbin;
        delete[] brbin;
        delete[] gbin;
    }
    catch (const std::exception &)
    {
        return;
    }
}
