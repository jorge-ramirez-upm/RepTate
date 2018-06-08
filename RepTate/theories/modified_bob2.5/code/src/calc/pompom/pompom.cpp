/*
pompom.cpp : This file is part bob-rheology (bob) 
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

#include "./pompom.h"
#define kkmax 101
#include <stdlib.h>
#include "../../RepTate/reptate_func.h"

void pompom(void)
{
  extern double CalcEtaStar(double);
  double eta_lin;
  extern FILE *infofl;

  FILE *NLoutfl = NULL;
  FILE *NLinpfl = fopen("nlin.inp", "r");
  extern int OutMode;
  char fname[80];
  char extn[80];
  int nrate, shearcode;
  double rate, tmin, tmax;
  double xp[kkmax], yp[kkmax], stress[kkmax], N1[kkmax];
  int kmax = 101;

  if (NLinpfl == NULL)
  {
    nrate = 10;
  }
  else
  {
    fscanf(NLinpfl, "%d", &nrate);
  }
  if (OutMode == 1)
  {
    NLoutfl = fopen("nonlin.agr", "w");
    extern void graceheadernlin(FILE *);
    graceheadernlin(NLoutfl);
  }

  for (int irt = 0; irt < nrate; irt++)
  {
    if (NLinpfl == NULL)
    {
      tmin = 1.0e-3;
      tmax = 1.0e4;
      if ((irt == 0) || (irt == 5))
      {
        rate = 0.01;
      }
      else
      {
        rate = rate * 5.0;
      }
      shearcode = irt / 5;
      tmax = 10.0 / rate;
    }
    else
    {
      fscanf(NLinpfl, "%d %lf %lf %lf", &shearcode, &rate, &tmin, &tmax);
    }
    calc_pompom(shearcode, kmax, rate, tmin, tmax, xp, yp, stress, N1);
    eta_lin = CalcEtaStar(rate);
    if (shearcode == 0)
    {
      extern bool reptate_flag;
      if (reptate_flag){
        char line[256];
        sprintf(line,"<b>Shear thinning at %9.4g s<sup>-1</sup>: %9.4g</b><br>", rate, (stress[kmax - 2] / rate) / (eta_lin));
        print_to_python(line);
      }

      fprintf(infofl, "shear thinning at %e /s : %e \n", rate, (stress[kmax - 2] / rate) / (eta_lin));
      strcpy(fname, "shear");
      inttochar(irt, extn);
      strcat(fname, extn);
      switch (OutMode)
      {
      case 2:
        strcpy(extn, ".shear");
        break;
      default:
        strcpy(extn, ".dat");
        break;
      }
      strcat(fname, extn);
      if (OutMode != 1)
      {
        NLoutfl = fopen(fname, "w");
      }
      if (OutMode == 2)
      {
        fprintf(NLoutfl, "gdot=%10.4e;\n", rate);
        for (int ik = 0; ik < kmax - 1; ik++)
        {
          fprintf(NLoutfl, "%e %e %e %e %e\n", xp[ik], stress[ik], N1[ik], rate, 1.0);
        }
      }
      else
      {
        if (OutMode == 1)
        {
          for (int ik = 0; ik < kmax - 1; ik++)
          {
            fprintf(NLoutfl, "%e %e\n", xp[ik], stress[ik] / rate);
          }
          if (OutMode == 1)
          {
            fprintf(NLoutfl, "& \n");
          }
        }
        else
        {
          for (int ik = 0; ik < kmax - 1; ik++)
          {
            fprintf(NLoutfl, "%e %e %e %e\n", xp[ik], stress[ik], N1[ik], rate);
          }
        }
      }
      if (OutMode != 1)
      {
        fclose(NLoutfl);
      }
    }

    else
    {
      if (reptate_flag){
        char line[256];
        sprintf(line,"<b>Extension hardening at %9.4g s<sup>-1</sup>: %9.4g</b><br>", rate, (stress[kmax - 2] / rate) / (3.0 * eta_lin));
        print_to_python(line);
      }
      fprintf(infofl, "Extension hardening at %e /s : %e \n", rate, (stress[kmax - 2] / rate) / (3.0 * eta_lin));
      strcpy(fname, "extn");
      inttochar(irt, extn);
      strcat(fname, extn);
      if (OutMode == 2)
      {
        strcpy(extn, ".uext");
      }
      else
      {
        strcpy(extn, ".dat");
      }
      strcat(fname, extn);
      if (OutMode != 1)
      {
        NLoutfl = fopen(fname, "w");
      }
      if (OutMode == 2)
      {
        fprintf(NLoutfl, "gdot=%10.4e;\n", rate);
        for (int ik = 0; ik < kmax - 1; ik++)
        {
          fprintf(NLoutfl, "%e %e %e %e \n", xp[ik], stress[ik], rate, 1.0);
        }
        // fprintf(NLoutfl,"%e %e %e %e \n",xp[ik],stress[ik]/rate,rate, 1.0);}
      }
      else
      {
        if (OutMode == 1)
        {
          for (int ik = 0; ik < kmax - 1; ik++)
          {
            fprintf(NLoutfl, "%e %e\n", xp[ik], stress[ik] / rate);
          }
        }
        else
        {
          for (int ik = 0; ik < kmax - 1; ik++)
          {
            fprintf(NLoutfl, "%e %e %e \n", xp[ik], stress[ik], rate);
          }
        }

        if (OutMode == 1)
        {
          fprintf(NLoutfl, "& \n");
        }
      }
      if (OutMode != 1)
      {
        fclose(NLoutfl);
      }
    }
  }
  if (NLinpfl != NULL)
  {
    fclose(NLinpfl);
  }
  if (OutMode == 1)
  {
    fclose(NLoutfl);
  }
}
