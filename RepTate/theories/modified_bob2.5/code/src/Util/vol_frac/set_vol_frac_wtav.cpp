/*
set_vol_frac_wtav.cpp : This file is part bob-rheology (bob) 
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
 
/* Set the volume fraction of polymers of species 'n_component' which
occupies 'blend_frac' fraction of the total weight and are in location
between 'n_start' and 'n_end' */

#include "../../../include/bob.h"
#include <stdio.h>
void set_vol_frac_wtav(int n_start, int n_end, int n_component, 
   double blend_frac)
{
extern std::vector <arm> arm_pool; extern std::vector <polymer> branched_poly;
extern FILE * infofl;
double total_mass = 0.0;
double mol_mass,tmpvar;
int cur_num; cur_num=n_end-n_start;

for (int i=n_start; i<n_end; i++)
 {
   int n1=branched_poly[i].first_end;
   mol_mass=arm_pool[n1].arm_len;
   total_mass+=arm_pool[n1].arm_len;
   int n2=arm_pool[n1].down;
   while(n2 != n1)
    {
     total_mass+=arm_pool[n2].arm_len; 
     mol_mass+=arm_pool[n2].arm_len; n2=arm_pool[n2].down;
    }

tmpvar=blend_frac/(((double) cur_num) * mol_mass);
    n1=branched_poly[i].first_end;
   arm_pool[n1].vol_fraction=arm_pool[n1].arm_len*tmpvar;
   n2=arm_pool[n1].down;
   while(n2 != n1)
    {
     arm_pool[n2].vol_fraction=arm_pool[n2].arm_len*tmpvar;
     n2=arm_pool[n2].down;
    }
 }

fprintf(infofl,"component  %d : Total mass = %e \n", n_component, total_mass);



}





