/*
resolve_maxwell_modes.cpp : This file is part bob-rheology (bob) 
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
void resolve_maxwell_modes(int ndata, 
            double * tp,double *  phip,double *  phip_ST) {
extern double Alpha, unit_time, G_0_unit;
double phnow, phstnow;

FILE * resfl=fopen("maxwell.dat","w");
// We will take the smallest time to be 100*tp[1] and largest tp[ndata -1]
double tspan=tp[ndata-1]/(100.0 * tp[1]);
// Maxwell times as multiples of 2 (about 3 per decade)
extern double MaxwellInterval;
int nummaxmode= (int) floor(log(tspan)/log(MaxwellInterval));
fprintf(resfl, "%d \n", nummaxmode+1);
int kk; double tau0, tau1, g0;
tau0=tp[1]*100.0; tau1=MaxwellInterval*tau0;
g0=0.0; kk=1;
while ((tp[kk] < (0.5*(tau0+tau1))) && (kk < ndata) )
{
phnow=0.50*(phip[kk-1]+phip[kk]); phstnow=0.50*(phip_ST[kk-1]+phip_ST[kk]);
g0+= (Alpha*phnow*pow(phstnow,Alpha)*(phip_ST[kk-1]-phip_ST[kk])/phstnow
 + pow(phstnow,Alpha)*(phip[kk-1]-phip[kk])); kk++;
}
fprintf(resfl, "%e %e\n", tau0*unit_time, g0*G_0_unit);
for (int j=1; j<=nummaxmode; j++)
{
g0=0.0; tau0=tau1; tau1=MaxwellInterval*tau0;
while ((tp[kk] < (0.5*(tau0+tau1))) && (kk < ndata) )
{
phnow=0.50*(phip[kk-1]+phip[kk]); phstnow=0.50*(phip_ST[kk-1]+phip_ST[kk]);
g0+= (Alpha*phnow*pow(phstnow,Alpha)*(phip_ST[kk-1]-phip_ST[kk])/phstnow
 + pow(phstnow,Alpha)*(phip[kk-1]-phip[kk])); kk++;
}
fprintf(resfl, "%e %e\n", tau0*unit_time, g0*G_0_unit);
}
fclose(resfl);

}
