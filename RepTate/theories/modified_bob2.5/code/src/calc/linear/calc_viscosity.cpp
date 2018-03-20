/*
calc_viscosity.cpp : This file is part bob-rheology (bob) 
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
void calc_viscosity(int ndata, double *tp, double *phip, double *phip_ST)
{
  // calculate viscosity : go to low frequency till viscosity is constant
  double ff[5], eta[5];
  int cont = 0;
  int num_try = 0;
  double freq, phnow, phstnow, tnow, tmpvar, tmpvar1;
  extern double Alpha, G_0_unit, unit_time;

  ff[0] = 1e-10;
  for (int i = 1; i < 5; i++)
  {
    ff[i] = ff[i - 1] / 2.0;
  }
  while ((cont == 0) && (num_try < 30))
  {
    num_try++;
    for (int i = 0; i < 5; i++)
    {
      freq = ff[i];
      eta[i] = 0.0;
      for (int j = 0; j < ndata; j++)
      {
        phnow = 0.50 * (phip[j - 1] + phip[j]);
        phstnow = 0.50 * (phip_ST[j - 1] + phip_ST[j]);
        tnow = tp[j];
        tmpvar = tnow / (1.0 + freq * freq * tnow * tnow);
        tmpvar1 = phnow * Alpha * pow(phstnow, Alpha) * (phip_ST[j - 1] - phip_ST[j]) / phstnow +
                  pow(phstnow, Alpha) * (phip[j - 1] - phip[j]);
        eta[i] += tmpvar * tmpvar1;
      }
      eta[i] = G_0_unit * eta[i] * unit_time;
    }
    tmpvar = 0.0;
    for (int i = 1; i < 5; i++)
    {
      tmpvar += (eta[i] - eta[i - 1]) * (eta[i] - eta[i - 1]);
    }
    if ((tmpvar / eta[3]) < 1e-12)
    {
      cont = 1;
    }
    else
    {
      for (int i = 0; i < 5; i++)
      {
        ff[i] = ff[i] / 2.0;
      }
    }
  }

  double sx = 0.0;
  double sy = 0.0;
  double sxx = 0.0;
  double sxy = 0.0;
  for (int i = 0; i < 5; i++)
  {
    sx += ff[i];
    sy += eta[i];
    sxx += ff[i] * ff[i];
    sxy += eta[i] * ff[i];
  }
  extern FILE *infofl;
  if (num_try > 19)
  {
    fprintf(infofl, "Warning : viscosity estimate may not be reliable \n");
  }
  fprintf(infofl, "zero-shear viscosity = %le \n", (sxx * sy - sxy * sx) / (5.0 * sxx - sx * sx));
}
