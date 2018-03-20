/*
pm_uext.cpp : This file is part bob-rheology (bob) 
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
void pm_uext(double x, double * y, double * dydx, 
   double tauS, double tauB, double gdot, int q){

double ayy, axx, ptrace, aux, nustar,  tmpvar;

if( (y[0] >= q) || (q == 1)){y[0]=(double) q; dydx[0]=0.0;}
else{
   nustar=2.0/((double) (q-1));
 if( ((2.0*gdot*tauB -1.0)*x/tauB) > 60.0){ axx=1.0; ayy=0.0;}
 else{
tmpvar=1.0 - 2.0*gdot*tauB;
if(fabs(tmpvar) < 1.0e-3){axx=1.0+2.0*gdot*x; }
else{
  axx=(1.0 - 2.0*gdot*tauB*exp(-tmpvar*x/tauB) )/ tmpvar;}

  ayy=(1.0 + gdot*tauB*exp(-(1.0 + gdot*tauB)*x/tauB) )/(1.0 + gdot*tauB); }
 
        ptrace= axx + 2.0*ayy;
        aux = tauS / exp(nustar * (y[0] - 1.0));

        if((aux * gdot) < 0.001){dydx[0]= 0.0;}
	else{dydx[0]=y[0]*gdot*(axx-ayy)/ptrace - (y[0] - 1.0)*exp(nustar*(y[0]-1.0))/tauS;}
   }
}
