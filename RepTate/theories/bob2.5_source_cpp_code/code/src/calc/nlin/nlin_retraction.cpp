/*
nlin_retraction.cpp : This file is part bob-rheology (bob) 
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
void nlin_retraction(int n)
{
extern arm * arm_pool;
double z0, dz, t_stretch; int rate_indx;

z0=arm_pool[n].z; dz=arm_pool[n].dz; 
int na=nlin_relaxing_arm(n, z0);

if(na == n){t_stretch=z0*z0;}
else{ t_stretch=interp_rouse_time(&arm_pool[na].compound_fit_zeff[0], \
&arm_pool[na].compound_fit_time[0], arm_pool[na].compound_store_data_num, z0);}
rate_indx=find_rate_indx(t_stretch);

extern double ** nlin_prio_phi_relax; // extern double nlin_dphi_true;
nlin_prio_phi_relax[arm_pool[na].priority][rate_indx]+=dz;
// nlin_dphi_true+=dz;

}



