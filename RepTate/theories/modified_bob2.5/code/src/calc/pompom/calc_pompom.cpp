/*
calc_pompom.cpp : This file is part bob-rheology (bob) 
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
#include <stdio.h>
#include "../../RepTate/reptate_func.h"

void calc_pompom(int shearcode, int kmax, double gdot, double tmin, double tmax,
                 double *xp, double *yp, double *stress, double *N1)
{
  double dlx = (log(tmax) - log(tmin)) / ((double)(kmax - 1));
  for (int i = 0; i < kmax; i++)
  {
    xp[i] = exp(log(tmin) + ((double)i) * dlx);
    stress[i] = N1[i] = 0.0;
  }

  double gm, g0, tauB, tauS, stretchrate, axx, ayy, axy;
  int q, num_maxwell, num_modes;

  // changes from bob v2.6
  double stretchrateSV;
  double tauB1;
  int ferr;
  //

  // FILE *maxfl = fopen("maxwell.dat", "r");
  // FILE *nlinfl = fopen("nlin_modes.dat", "r");

  // fscanf(maxfl, "%d", &num_maxwell);
  num_maxwell = max_mode_maxwell;
  int counter = 0;
  for (int im = 0; im < num_maxwell; im++)
  {
    // fscanf(maxfl, "%lf %lf", &tauB, &gm);
    tauB = maxwell_time[im];
    gm = maxwell_modulus[im];
    
    // ferr = fscanf(nlinfl, "%lf %d", &tauB1, &num_modes);
    // if (ferr != 2)
    // {
    //   num_modes = 1;
    // } // missing data, fudge sensibly
    if (vector_nlin_outfl[counter].size() != 2)
    {
      num_modes = 1;
      ferr = 1;
    }
    else{
      tauB1 = vector_nlin_outfl[counter][0];
      num_modes = int(vector_nlin_outfl[counter][1]);
      ferr = 2;
    }
    counter++;

    for (int jm = 0; jm < num_modes; jm++)
    {
      if (ferr == 2)
      {
        // fscanf(nlinfl, "%d %lf %lf", &q, &g0, &stretchrate);
        q = vector_nlin_outfl[counter][0];
        g0 = vector_nlin_outfl[counter][1];
        stretchrate = vector_nlin_outfl[counter][2];
        counter++;
        //
        stretchrateSV = stretchrate;
      }
      else
      {
        q = 1;
        g0 = 1.0;
        stretchrate = stretchrateSV;
      }
      g0 = g0 * gm;
      tauS = tauB / stretchrate;

      double x1 = 0.0;
      double x2 = tmax;
      double ystart = 1.0;
      double eps = 1.0e-4;
      double h1 = 0.01 / gdot;
      if (h1 > (tmin / 2.0))
      {
        h1 = tmin / 2.0;
      }
      if (h1 < (tauS / 100.0))
      {
        h1 = tauS / 100.0;
      }
      double hmin = h1 / 100.0;
      if (shearcode == 0)
      {
        odeint(ystart, x1, x2, eps, h1, hmin, tauS, tauB, gdot, q, kmax, xp, yp, pm_shear);
        for (int k = 0; k < kmax; k++)
        {
          axy = gdot * tauB * (1.0 - exp(-xp[k] / tauB));
          axx = 2.0 * gdot * gdot * tauB * tauB * (1.0 - exp(-xp[k] / tauB)) + 1.0 - 2.0 * gdot * gdot * tauB * xp[k] * exp(-xp[k] / tauB);
          // printf("%e %e \n",xp[k],yp[k]);
          /* yp[k]=1.0;  check */
          stress[k] += 3.0 * g0 * yp[k] * yp[k] * axy / (axx + 2.0);
          N1[k] += 3.0 * g0 * yp[k] * yp[k] * (axx - 1.0) / (axx + 2.0);
        }
      }
      else
      {
        odeint(ystart, x1, x2, eps, h1, hmin, tauS, tauB, gdot, q, kmax, xp, yp, pm_uext);
        for (int k = 0; k < kmax; k++)
        {
          /* yp[k]=1.0; check */
          if (((2.0 * gdot * tauB - 1.0) * xp[k] / tauB) > 60.0)
          {
            axx = 1.0;
            ayy = 0.0;
          }
          else
          {
            axx = (1.0 - 2.0 * gdot * tauB * exp((2 * gdot * tauB - 1.0) * xp[k] / tauB)) / (1.0 - 2 * gdot * tauB);
            ayy = (1.0 + gdot * tauB * exp(-(1.0 + gdot * tauB) * xp[k] / tauB)) / (1.0 + gdot * tauB);
          }
          if (axx > 1.0e30)
          {
            stress[k] += 3.0 * g0 * yp[k] * yp[k];
          }
          else
          {
            stress[k] += 3.0 * g0 * yp[k] * yp[k] * (axx - ayy) / (axx + 2.0 * ayy);
          }
        }
      }
    }
  }

  // fclose(maxfl);
  // fclose(nlinfl);
}
