/*
gpchist.cpp : This file is part bob-rheology (bob) 
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

// Calculate histograph and dump in file
#include <math.h>
#include <stdio.h>
#include "./gpcls.h"

void gpchist(int ncomp, int n_cur_comp, int number_based,
             double *mass_ar, double *gfac_ar, double *branch_ar, double *wt_frac)
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

    dumpgpcres(ncomp, nnn, wtbin, brbin, gbin, lgmin, lgstep);
  }
  delete[] wtbin;
  delete[] brbin;
  delete[] gbin;
}
