/*
tobitautil.cpp : This file is part bob-rheology (bob) 
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

#include "../../../include/MersenneTwister.h"
#include <math.h>
double getconv1(double cur_conv)
{
  extern MTRand mtrand1;
  double new_conv = cur_conv * mtrand1();
  return new_conv;
}

double getconv2(double cur_conv, double fin_conv)
{
  extern MTRand mtrand1;
  double new_conv = 1.0 -
                    (1.0 - cur_conv) * exp(-mtrand1() * log((1.0 - cur_conv) / (1.0 - fin_conv)));
  return new_conv;
}

double brlength(double conv, double cb, double fin_conv)
{
  extern MTRand mtrand1;
  double rho = cb * log((1.0 - conv) / (1.0 - fin_conv));
  double r = (log(1.0 / mtrand1())) / rho;
  return r;
}

double scilength(double conv, double cs, double fin_conv)
{
  extern MTRand mtrand1;
  double eta = cs * log((1.0 - conv) / (1.0 - fin_conv));
  double r = (log(1.0 / mtrand1())) / eta;
  if (r < 1000.0)
  {
    r = ceil(r);
  }
  return r;
}

double calclength(double conv, double cs, double cb, double tau, double beta)
{
  extern MTRand mtrand1;
  double sigma = cs * conv / (1.0 - conv);
  double lambda = cb * conv / (1.0 - conv);
  double pref = tau + beta + sigma + lambda;
  double r = (log(1.0 / mtrand1())) / pref;
  if (r < 1000.0)
  {
    r = ceil(r);
  }
  return r;
}
