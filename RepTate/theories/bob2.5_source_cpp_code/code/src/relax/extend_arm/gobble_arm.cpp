/*
gobble_arm.cpp : This file is part bob-rheology (bob) 
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
 
// polymer : m, arm n gobbles up n1 accumulating drag due to n2
#include <math.h>
#include "../../../include/bob.h"
#include "../relax.h"
#include <stdio.h>
void gobble_arm(int m, int n, int n1, int n2)
{ 
 extern polymer *  branched_poly;
 extern arm * arm_pool;
 extern double Alpha;
 int r2=arm_pool[n2].relax_end;
 arm_pool[n1].relax_end=n; arm_pool[n1].relaxing=true;
 arm_pool[n].compound=true; arm_pool[n].collapsed=false;
 arm_pool[n].phi_collapse = -1.0;

 int na=arm_pool[n].next_friction; int n3=na;
 if(na == -1) {arm_pool[n].next_friction = r2; arm_pool[r2].next_friction = -1;}
 else{
 while(na != -1){n3=na; na=arm_pool[na].next_friction;}
 arm_pool[n3].next_friction=r2;  arm_pool[r2].next_friction = -1;}

 int n0=inner_arm_compound(n); arm_pool[n0].nxt_relax=n1;
 double tmpvar=arm_pool[r2].tau_collapse*
              pow(arm_pool[r2].phi_collapse,2.0*Alpha);
  arm_pool[n].zeff_numer+= arm_pool[n].arm_len_end*tmpvar;
  arm_pool[n].zeff_denom+=tmpvar;
  arm_pool[n].extra_drag+=tmpvar;
  arm_pool[n].arm_len_end+= arm_pool[n1].arm_len;
    if(arm_pool[r2].ghost)
      branched_poly[m].ghost_contrib -=tmpvar;
    else
      arm_pool[r2].prune=true;

}
