/*
gasdev.cpp : This file is part bob-rheology (bob) 
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

// returns Gaussian random number with zero mean and unit variance
#include "../../../include/MersenneTwister.h"
#include <math.h>
double gasdev(void)
{
  extern MTRand mtrand1;
  double rsq, v1, v2;
  static double g = 1.0;
  static bool gaus_stored = false;

  if (gaus_stored)
  {
    gaus_stored = false;
    return (g);
  }
  else
  {
    rsq = -1.0;
    while ((rsq < 0.0) || (rsq > 1.0))
    {
      v1 = 2.0 * mtrand1() - 1.0;
      v2 = 2.0 * mtrand1() - 1.0;
      rsq = v1 * v1 + v2 * v2;
    }
    rsq = sqrt(-2.0 * log(rsq) / rsq);
    g = v2 * rsq;
    gaus_stored = true;
    return (v1 * rsq);
  }
}
