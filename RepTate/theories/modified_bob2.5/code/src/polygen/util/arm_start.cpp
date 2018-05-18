/*
arm_start.cpp : This file is part bob-rheology (bob) 
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

//called via poly_start : set up arm variables correctly
#include <math.h>
#include "../../../include/bob.h"
void arm_start(int n)
{
  extern std::vector<arm> arm_pool;
  extern double phi;
  arm_pool[n].prune = false;
  arm_pool[n].ghost = false;
  arm_pool[n].collapsed = false;
  arm_pool[n].nxt_relax = -1;
  arm_pool[n].phi_collapse = -1.0;
  if ((arm_pool[n].L1 == -1 && arm_pool[n].L2 == -1) ||
      (arm_pool[n].R1 == -1 && arm_pool[n].R2 == -1))
  { // one end of n is free
    arm_pool[n].free_end = true;
    arm_pool[n].relaxing = true;
    arm_pool[n].relax_end = n;
    arm_pool[n].compound = false;
    arm_pool[n].z = 0.0;
    arm_pool[n].pot = 0.0;
    arm_pool[n].gamma2 = sqrt(1.50 * (pi_pow_5) *
                              (pow(arm_pool[n].arm_len, (double)3)) / phi);
    arm_pool[n].tau_K = 0.0;
    arm_pool[n].dz = 0.0;
    arm_pool[n].arm_len_eff = arm_pool[n].arm_len;
    arm_pool[n].arm_len_end = arm_pool[n].arm_len;
    arm_pool[n].deltazeff = 0.0;
    arm_pool[n].zeff_numer = 0.0;
    arm_pool[n].zeff_denom = 0.0;
    arm_pool[n].extra_drag = 0.0;
    arm_pool[n].next_friction = -1;
    if ((arm_pool[n].L1 == -1 && arm_pool[n].L2 == -1))
    {
      arm_pool[n].nxtbranch1 = arm_pool[n].R1;
      arm_pool[n].nxtbranch2 = arm_pool[n].R2;
    }
    else
    {
      arm_pool[n].nxtbranch1 = arm_pool[n].L1;
      arm_pool[n].nxtbranch2 = arm_pool[n].L2;
    }
  }
  else
  { //both ends are connected
    arm_pool[n].free_end = false;
    arm_pool[n].relaxing = false;
    arm_pool[n].relax_end = -1;
  }
}
