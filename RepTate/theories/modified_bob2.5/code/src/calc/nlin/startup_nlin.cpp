/*
startup_nlin.cpp : This file is part bob-rheology (bob) 
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
#include <stdlib.h>
void startup_nlin(void)
{
extern int max_prio_var, NumNlinStretch;
extern double NlinAvDt;
extern double ** nlin_prio_phi_relax;
extern double ** nlin_prio_phi_held;
extern double ** assign_ar_2d_double(int, int);
nlin_prio_phi_relax=assign_ar_2d_double(max_prio_var, NumNlinStretch);
nlin_prio_phi_held=assign_ar_2d_double(max_prio_var, NumNlinStretch);

extern int nlin_collect_data; nlin_collect_data=-1;
extern int DefinedMaxwellModes;

extern int num_maxwell, nlin_nxt_data; num_maxwell=nlin_nxt_data=0;
extern double nlin_t_min, nlin_t_max;
extern double * t_maxwell; 
if(DefinedMaxwellModes == 0){ FILE * ftmp=fopen("maxwell.dat","r");
if(ftmp != NULL){fscanf(ftmp,"%d", &num_maxwell); 
double jnk;
t_maxwell=new double[num_maxwell];
for(int i=0; i<num_maxwell; i++){fscanf(ftmp,"%lf %lf",&t_maxwell[i],&jnk);}
fclose(ftmp);}
if(num_maxwell > 0){
nlin_t_min=t_maxwell[0]/NlinAvDt;
nlin_t_max=t_maxwell[0]*NlinAvDt;
                   }
else{ nlin_t_min=1.0e32; nlin_t_max=1.0e32;} }
else{
num_maxwell=100; // Enough modes
t_maxwell=new double[num_maxwell];
extern double TStart, MaxwellInterval; t_maxwell[0]=100.0*TStart;
for(int j=1; j<num_maxwell; j++){t_maxwell[j]=t_maxwell[j-1]*MaxwellInterval;}
nlin_t_min=t_maxwell[0]/NlinAvDt;
nlin_t_max=t_maxwell[0]*NlinAvDt; }

extern FILE * nlin_outfl;
nlin_outfl=fopen("nlin_modes.dat","w");

}
