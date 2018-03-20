/*
interp_rouse_time.cpp : This file is part bob-rheology (bob) 
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
 
#include <math.h>
#include <stdio.h>
double interp_rouse_time(double *za, double *ta, int n, double z){
double t;
extern double cur_time;
if(n == 0){return cur_time;}
else{

if(z <= (za[0]+1.0e-12)){t=ta[0];}
else{
if(z >= (za[n-1]-1.0e-12)){t=ta[n-1];}
else{
int k1, k2=1; k1=0;
for(int i=1; i<n; i++){ if(k1 ==0){if(z < za[i]){k1=1; k2=i;}} }
if(k1 == 0){printf("Non e possibile!! \n");}

// z between za[k2-1] and za[k2]
double dz=za[k2]-za[k2-1];
if((z - za[k2-1]) > 1.0e-6){
t=exp(log(ta[k2-1]) + (log(ta[k2]) - log(ta[k2-1])) * (z - za[k2-1])/dz );}
else{
     t=ta[k2-1];
    }

// The following lines are for debugging - they should never be satisfied!
if( (t > ta[k2]) && (t > ta[k2-1])){printf("interp : k2=%d, z1=%e, z2=%e, z=%e \n",k2,za[k2-1],za[k2],z);
          printf("       t1=%e, t2=%e,  t=%e \n",ta[k2-1],ta[k2],t);
 for(int k5=0; k5<n; k5++){printf(" %e %e ", za[k5],ta[k5]);}
  printf("\n");}
if( (t < ta[k2]) && (t < ta[k2-1])){printf("interp : z1=%e, z2=%e, z=%e \n",za[k2-1],za[k2],z);
          printf("       t1=%e, t2=%e,  t=%e \n",ta[k2-1],ta[k2],t); }

}}

return t;
}
}

