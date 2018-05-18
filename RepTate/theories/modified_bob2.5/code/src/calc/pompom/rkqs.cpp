/*
rkqs.cpp : This file is part bob-rheology (bob) 
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
#include <math.h>
void rkqs(double *y, double dydx, double *x, double htry, double eps,
          double yscal, double *hdid, double *hnext,
          double tauS, double tauB, double gdot, int q,
          void (*derivs)(double, double *, double *, double, double, double, int))
{
  double SAFETY = 0.9;
  double PGROW = -0.2;
  double PSHRNK = -0.25;
  double ERRCON = 1.89e-4;
  double h = htry;
  int cont = 0;
  double yerr, errmax, htemp, xnew, tmpmax, ytemp;
  extern void warnmsgs(int);

  while (cont == 0)
  {
    cont = 1;
    rkck(y[0], dydx, x[0], h, &ytemp, &yerr, tauS, tauB, gdot, q, derivs);
    errmax = fabs(yerr / yscal);
    errmax = errmax / eps;

    if (errmax > 1.0)
    {
      htemp = SAFETY * h * (exp(log(errmax) * PSHRNK));
      tmpmax = fabs(htemp);
      if (tmpmax < (0.1 * fabs(h)))
      {
        tmpmax = 0.1 * fabs(h);
      }
      if (h > 0.0)
      {
        h = fabs(tmpmax);
      }
      else
      {
        h = -fabs(tmpmax);
      }
      xnew = x[0] + h;
      if (xnew == x[0])
      {
        warnmsgs(403);
        h = 1.0e-8;
      }
      cont = 0;
    }
  }

  if (errmax > ERRCON)
  {
    hnext[0] = SAFETY * h * (exp(log(errmax) * PGROW));
  }
  else
  {
    hnext[0] = 5.0 * h;
  }

  hdid[0] = h;
  x[0] += h;
  y[0] = ytemp;
}
