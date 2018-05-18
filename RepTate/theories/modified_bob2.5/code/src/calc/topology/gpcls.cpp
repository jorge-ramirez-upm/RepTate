/*
gpcls.cpp : This file is part bob-rheology (bob) 
bob-2.5 : rheology of Branch-On-Branch polymers
Copyright (C) 2006-2011, 2012 C. Das, D.J. Read, T.C.B. McLeish
 
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details. You can find a copy
  of the license at <http://www.gnu.org/licenses/gpl.txt>
*/

/* Calculate GPC LS data for component ncomp with polymers from ni to nf */
/* number_based tell us if the polymers are created with number averaged
     or weight averaged fashion */
#include <stdio.h>
#include <math.h>
#include "../../../include/bob.h"
#include "./gpcls.h"

void gpcls(int ncomp, int ni, int nf, int number_based)
{
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

  extern FILE *infofl;
  if (ncomp < 0)
  { // global average
    fprintf(infofl, "GPC module for entire system  : \n");
  }
  else
  {
    fprintf(infofl, "GPC module for component %d  : \n", ncomp);
  }
  fprintf(infofl, "Mw = %e ,   Mn =  %e, PDI = %e \n", mwav, mnav, pdi);

  extern int ForceGPCTrace;
  if ((ForceGPCTrace != 0) && ((pdi - 1.0) < 1.0e-4))
  {
    fprintf(infofl, "Too small PDI for useful GPC trace. \n");
    fprintf(infofl, "  You can force GPC trace output by setting ForceGPCTrace in bob.rc\n");
  }
  else
  { // Calculate histograms.
    if (n_cur_comp < 20)
    {
      fprintf(infofl, "Too few polymers for GPC histogram. \n");
    }
    else
    {
      gpchist(ncomp, n_cur_comp, number_based, mass_ar, gfac_ar, branch_ar, wtfrac_ar);
    }
  }
  delete[] mass_ar;
  delete[] gfac_ar;
  delete[] branch_ar;
  delete[] wtfrac_ar;
}
