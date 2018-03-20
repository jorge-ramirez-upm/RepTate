/*
pm_shear.cpp : This file is part bob-rheology (bob) 
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
void pm_shear(double x, double * y, double * dydx, 
   double tauS, double tauB, double gdot, int q){
double axy, axx, ptrace, aux, nustar;

if( (y[0] >= q) || (q == 1)){y[0]=(double) q; dydx[0]=0.0;}
else{
 if( y[0] < 1.0){y[0]=1.0; dydx[0]=0.0; }
 else{nustar=2.0/((double) (q-1));
   axy=gdot*tauB * (1.0 - exp(-x/tauB));
   axx=2.0*(gdot*gdot)*(tauB*tauB)*(1.0 - exp(-x/tauB))
   + 1.0 - 2.0 * (gdot*gdot) * tauB * x * exp(-x / tauB);
        ptrace= axx + 2.0;
        aux = tauS / exp(nustar * (y[0] - 1.0));
        if((aux * gdot) < 0.001){dydx[0]= 0.0;}
	else{dydx[0]=y[0]*gdot*axy/ptrace-(y[0]-1.0)*exp(nustar*(y[0]-1.0))/tauS;}
     }
   }
}
