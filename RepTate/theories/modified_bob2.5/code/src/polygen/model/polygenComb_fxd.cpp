/*
polygenComb_fxd.cpp : This file is part bob-rheology (bob) 
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
#include <math.h>

polymer polygenComb_fxd(int arm_typeb, double m_bbone, double pdi_bbone,
                        int arm_typea, double m_arm, double pdi_arm, int n_arm)
{
  extern std::vector<arm> arm_pool;
  polymer cur_poly;
  double cur_bbone, cur_arm;
  cur_bbone = poly_get_arm(arm_typeb, m_bbone, pdi_bbone);

  if (n_arm > 0)
  {
    double *junc = new double[n_arm];
    rand_on_line(cur_bbone, n_arm, junc);
    int n0 = request_arm();
    cur_poly.first_end = n0;
    arm_pool[n0].L1 = arm_pool[n0].L2 = -1;
    arm_pool[n0].arm_len = junc[0];

    cur_arm = poly_get_arm(arm_typea, m_arm, pdi_arm);

    int n1 = request_arm();
    arm_pool[n1].L1 = arm_pool[n1].L2 = -1;
    arm_pool[n1].arm_len = cur_arm;
    arm_pool[n1].R1 = n0;
    arm_pool[n0].R1 = n1;
    arm_pool[n0].down = n1;
    arm_pool[n1].up = n0;
    arm_pool[n1].down = n0;
    arm_pool[n0].up = n1;
    int n0p, n1p;
    for (int k = 1; k < n_arm; k++)
    {
      n0p = request_arm();
      arm_pool[n0p].L1 = n0;
      arm_pool[n0p].L2 = n1;
      arm_pool[n0].R2 = n0p;
      arm_pool[n1].R2 = n0p;
      arm_pool[n0p].arm_len = junc[k] - junc[k - 1];
      cur_arm = poly_get_arm(arm_typea, m_arm, pdi_arm);
      n1p = request_arm();
      arm_pool[n1p].L1 = arm_pool[n1p].L2 = -1;
      arm_pool[n1p].R1 = n0p;
      arm_pool[n0p].R1 = n1p;
      arm_pool[n1p].arm_len = cur_arm;
      int nd = arm_pool[n0].down;
      arm_pool[n0].down = n0p;
      arm_pool[n0p].up = n0;
      arm_pool[n0p].down = n1p;
      arm_pool[n1p].up = n0p;
      arm_pool[n1p].down = nd;
      arm_pool[nd].up = n1p;
      n0 = n0p;
      n1 = n1p;
    }
    n0p = request_arm();
    arm_pool[n0p].L1 = n0;
    arm_pool[n0p].L2 = n1;
    arm_pool[n0].R2 = n0p;
    arm_pool[n1].R2 = n0p;
    arm_pool[n0p].R1 = arm_pool[n0p].R2 = -1;
    arm_pool[n0p].arm_len = cur_bbone - junc[n_arm - 1];
    int nd = arm_pool[n0].down;
    arm_pool[n0].down = n0p;
    arm_pool[n0p].up = n0;
    arm_pool[n0p].down = nd;
    arm_pool[nd].up = n0p;
    delete[] junc;
  }
  else
  {
    cur_poly = polygenLin(cur_bbone);
  }

  poly_start(&cur_poly);
  return (cur_poly);
}
