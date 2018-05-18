/*
rkck.cpp : This file is part bob-rheology (bob) 
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

void rkck(double y, double dydx, double x, double h, double *yout, double *yerr,
          double tauS, double tauB, double gdot, int q,
          void (*derivs)(double, double *, double *, double, double, double, int))

{
  static double a2 = 0.2, a3 = 0.3, a4 = 0.6, a5 = 1.0, a6 = 0.875, b21 = 0.2,
                b31 = 3.0 / 40.0, b32 = 9.0 / 40.0, b41 = 0.3, b42 = -0.9, b43 = 1.2,
                b51 = -11.0 / 54.0, b52 = 2.5, b53 = -70.0 / 27.0, b54 = 35.0 / 27.0,
                b61 = 1631.0 / 55296.0, b62 = 175.0 / 512.0, b63 = 575.0 / 13824.0,
                b64 = 44275.0 / 110592.0, b65 = 253.0 / 4096.0, c1 = 37.0 / 378.0,
                c3 = 250.0 / 621.0, c4 = 125.0 / 594.0, c6 = 512.0 / 1771.0,
                dc5 = -277.0 / 14336.0;
  double dc1 = c1 - 2825.0 / 27648.0, dc3 = c3 - 18575.0 / 48384.0,
         dc4 = c4 - 13525.0 / 55296.0, dc6 = c6 - 0.25;

  double ytemp, ak2, ak3, ak4, ak5, ak6;
  ytemp = y + b21 * h * dydx;
  (*derivs)(x + a2 * h, &ytemp, &ak2, tauS, tauB, gdot, q);
  ytemp = y + h * (b31 * dydx + b32 * ak2);
  (*derivs)(x + a3 * h, &ytemp, &ak3, tauS, tauB, gdot, q);
  ytemp = y + h * (b41 * dydx + b42 * ak2 + b43 * ak3);
  (*derivs)(x + a4 * h, &ytemp, &ak4, tauS, tauB, gdot, q);
  ytemp = y + h * (b51 * dydx + b52 * ak2 + b53 * ak3 + b54 * ak4);
  (*derivs)(x + a5 * h, &ytemp, &ak5, tauS, tauB, gdot, q);
  ytemp = y + h * (b61 * dydx + b62 * ak2 + b63 * ak3 + b64 * ak4 + b65 * ak5);
  (*derivs)(x + a6 * h, &ytemp, &ak6, tauS, tauB, gdot, q);
  yout[0] = y + h * (c1 * dydx + c3 * ak3 + c4 * ak4 + c6 * ak6);
  yerr[0] = h * (dc1 * dydx + dc3 * ak3 + dc4 * ak4 + dc5 * ak5 + dc6 * ak6);
}
