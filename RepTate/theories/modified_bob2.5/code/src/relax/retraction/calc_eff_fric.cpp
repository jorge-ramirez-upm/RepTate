/*
calc_eff_fric.cpp : This file is part bob-rheology (bob) 
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
 
// Calculate the effective friction of compound arm n
#include<math.h>
#include<stdio.h>
#include "../../../include/bob.h"
double calc_eff_fric(int n)
{
extern arm * arm_pool;
extern double Alpha;
int n1=arm_pool[n].next_friction;
int n2=arm_pool[n].nxt_relax;
double zeff=arm_pool[n].arm_len_eff;
double zouter=arm_pool[n].arm_len;
double drag=0.0;

while(n1 != -1){
drag+= arm_pool[n1].tau_collapse*
             pow(arm_pool[n1].phi_collapse,2.0*Alpha)*(zeff - zouter)/zeff;
zouter+=arm_pool[n2].arm_len;
n2=arm_pool[n2].nxt_relax;
n1=arm_pool[n1].next_friction;
               }
return(drag);

}
