/*
quad_solve_spl.cpp : This file is part bob-rheology (bob) 
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

/** Returns the smallest positive root of a quadratic equation :
  a*x^2 + b*x + c == 0.
 If the roots are complex, returns only the real part **/
#include <math.h>
double quad_solve_spl(double a, double b, double c)
{
  double bp, cp, disc, res;
  if (fabs(a) > 1.0e-16)
  {
    bp = b / (2.0 * a);
    cp = c / a;
    disc = bp * bp - cp;
    if (disc > 1.0e-16)
    {
      disc = sqrt(disc);
      res = -bp - disc;
      if (res < 0.0)
      {
        res = -bp + disc;
      }
      return res;
    }
    else
      return -bp;
  }
  else
    res = -c / b;
  return res;
}
