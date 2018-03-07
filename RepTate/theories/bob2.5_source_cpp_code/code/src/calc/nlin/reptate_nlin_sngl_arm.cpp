/*
reptate_nlin_sngl_arm.cpp : This file is part bob-rheology (bob) 
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
 
#include "../../../include/bob.h"
#include "./nlin.h"
#include <math.h>

void reptate_nlin_sngl_arm(int n) {
extern arm * arm_pool;
extern double ** nlin_prio_phi_relax; // extern double nlin_dphi_true;
double z0=arm_pool[n].z;
int nsplit, cur_prio, rate_indx;
double dz, t_stretch, zz;

double dz1=0; double cumulative_z=arm_pool[n].arm_len; int n0=n; int n1=n;
while(cumulative_z < z0){dz1+=arm_pool[n0].arm_len; n1=n0;
                         n0=arm_pool[n0].nxt_relax;
                        if(n0 == -1){cumulative_z=z0+tiny;}
                        else{ cumulative_z+=arm_pool[n0].arm_len;} }
dz=arm_pool[n0].arm_len - (z0 - dz1);   zz=z0;

if(dz > 1.0e-12){ cur_prio=arm_pool[n0].priority;
nsplit=(int) ceil(dz/0.10); dz=dz/((double) nsplit);
 for(int i=0; i<nsplit; i++){ zz+=dz;
 if(n0 == n){t_stretch=zz*zz;}
 else{t_stretch=interp_rouse_time(&arm_pool[n0].compound_fit_zeff[0], &arm_pool[n0].compound_fit_time[0], \
   arm_pool[n0].compound_store_data_num, zz); }
 rate_indx=find_rate_indx(t_stretch);
 nlin_prio_phi_relax[cur_prio][rate_indx]+=dz; // nlin_dphi_true+=dz; 
                                 } }

n0=arm_pool[n0].nxt_relax;
while(n0 != -1){ dz=arm_pool[n0].arm_len;

if(dz > 1.0e-12){
cur_prio=arm_pool[n0].priority;
nsplit=(int) ceil(dz/0.10); dz=dz/((double) nsplit);
 for(int i=0; i<nsplit; i++){ zz+=dz;
t_stretch=interp_rouse_time(&arm_pool[n0].compound_fit_zeff[0], &arm_pool[n0].compound_fit_time[0], \
   arm_pool[n0].compound_store_data_num, zz);
rate_indx=find_rate_indx(t_stretch);
 nlin_prio_phi_relax[cur_prio][rate_indx]+=dz;
//  nlin_dphi_true+=dz; 
                     } }

n0=arm_pool[n0].nxt_relax;
               }

}

