/*
polygenProto.cpp : This file is part bob-rheology (bob) 
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
polymer polygenProto(int narm, int *arm_type, int *LL1,
                     int *LL2, int *RR1, int *RR2, double *mass, double *pdi)
{

  polymer cur_poly;
  extern std::vector<arm> arm_pool;
  int n, n1, nsv;
  nsv = 0;
  for (int j = 0; j < narm; j++)
  {
    n = request_arm();
    if (j == 0)
    {
      nsv = n;
      cur_poly.first_end = n;
      arm_pool[n].up = n;
      arm_pool[n].down = n;
    }
    arm_pool[n].arm_len = poly_get_arm(arm_type[j], mass[j], pdi[j]);
    arm_pool[n].L1 = fold_rd(LL1[j], nsv);
    arm_pool[n].L2 = fold_rd(LL2[j], nsv);
    arm_pool[n].R1 = fold_rd(RR1[j], nsv);
    arm_pool[n].R2 = fold_rd(RR2[j], nsv);
    n1 = arm_pool[nsv].up;
    arm_pool[nsv].up = n;
    arm_pool[n].down = nsv;
    arm_pool[n].up = n1;
    arm_pool[n1].down = n;
  }
  poly_start(&cur_poly);
  return (cur_poly);
}
