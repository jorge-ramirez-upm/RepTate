/*
lin_rheology.cpp : This file is part bob-rheology (bob) 
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

#include <stdio.h>
#include <math.h>
#include "./lin_rheo.h"
#include "../../RepTate/reptate_func.h"

void lin_rheology(int ndata)
{
  // FILE *phifl;
  // phifl = fopen("supertube.dat", "r");
  double *tp = new double[ndata];
  double *phip = new double[ndata];
  double *phip_ST = new double[ndata];
  // double jnk;

  // for (int i = 0; i < ndata; i++)
  //   fscanf(phifl, "%le %le %le %le", &tp[i], &jnk, &phip_ST[i], &phip[i]);
  // fclose(phifl);
  for (int i = 0; i < ndata; i++)
  {
    tp[i] = vector_supertube[i][0];
    phip_ST[i] = vector_supertube[i][2];
    phip[i] = vector_supertube[i][3];
  }
  // Call routines to calculate response
  lin_time_resp(ndata, tp, phip, phip_ST);
  lin_freq_resp(ndata, tp, phip, phip_ST);
  calc_viscosity(ndata, tp, phip, phip_ST);
  extern double CalcEtaStar(double);
  extern FILE *infofl;
  extern bool reptate_flag;
  if (reptate_flag)
  {
    if (!flag_no_info_printed)
    {
      char line[256];
      sprintf(line, "<b>|complex-viscosity|(1.0e-6) = %9.4g</b><br>", CalcEtaStar(1.0e-6));
      print_to_python(line);
    }
  }
  else
    fprintf(infofl, "|complex-viscosity|(1.0e-6) = %e \n", CalcEtaStar(1.0e-6));
#ifdef NBETA
  extern int DefinedMaxwellModes;
  if (DefinedMaxwellModes != 0)
  {
    resolve_maxwell_modes(ndata, tp, phip, phip_ST);
  }
#endif

  delete[] tp;
  delete[] phip;
  delete[] phip_ST;
}
