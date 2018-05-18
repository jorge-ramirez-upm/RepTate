/*
fast_four_hist.cpp : This file is part bob-rheology (bob) 
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

//fast modes via histogram in Fourier space
#include <math.h>
#include <vector>

void fast_four_hist(double freq, double *gpfast, double *g2pfast)
{
  double gp, g2p, tmpvar, tmppow2, tmppow4;
  double freqsq = freq * freq;
  extern double N_e;
  extern std::vector<double> phi_hist;
  extern int zintmin, zintmax;
  extern void warnmsgs(int);
  if (freq < 0.0)
  {
    warnmsgs(404);
  }
  gpfast[0] = 0.0;
  g2pfast[0] = 0.0;

  for (int zi = zintmin; zi <= zintmax; zi++)
  {
    double phi_now = phi_hist[zi];
    if (phi_now >= 0.0)
    {
      double zz = (double)zi + 0.50; // assume flat distribution within bins
      gp = 0.0;
      g2p = 0.0;
      for (int i = 1; i < zi; i++)
      {
        tmpvar = (double)i / zz;
        tmppow2 = tmpvar * tmpvar;
        tmppow4 = tmppow2 * tmppow2;
        gp += 1.0 / (freqsq + tmppow4);
        g2p += tmppow2 / (freqsq + tmppow4);
      }
      int quit = 0;
      int k = zi;
      tmpvar = (double)k / zz;
      tmppow4 = 4.0 * tmpvar * tmpvar * tmpvar * tmpvar;
      double comp_term = 1.0 / (freqsq + tmppow4);
      comp_term = 0.00010 * comp_term;
      if (comp_term > 0.00010)
        comp_term = 0.00010;
      int max_term = (int)ceil(N_e * zz);
      while (quit == 0)
      {
        tmpvar = double(k) / zz;
        tmppow2 = tmpvar * tmpvar;
        tmppow4 = 4.0 * tmppow2 * tmppow2;
        tmpvar = 1.0 / (freqsq + tmppow4);
        gp += 5.0 * tmpvar;
        g2p += 10.0 * tmppow2 / (freqsq + tmppow4);
        if (tmpvar < comp_term)
          quit = 1;
        if (k >= max_term)
          quit = 1;
        k++;
      }
      gpfast[0] += gp * phi_now / (4.0 * zz);
      g2pfast[0] += g2p * phi_now / (4.0 * zz);
    }
  }
  gpfast[0] = freqsq * gpfast[0];
  g2pfast[0] = freq * g2pfast[0];
}
