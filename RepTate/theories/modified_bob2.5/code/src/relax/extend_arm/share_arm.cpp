/*
share_arm.cpp : This file is part bob-rheology (bob) 
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

// polymer m : n collapsed : n1 collapsed earlier : n2 relaxing in compound arm
#include "../../../include/bob.h"
#include "../relax.h"
#include <stdio.h>
#include <cstdlib>
#include <math.h>
int share_arm(int m, int n, int n1, int n2)
{
  extern std::vector<arm> arm_pool;
  extern double Alpha;

  int ret_val = 0;
  int r2 = arm_pool[n2].relax_end;
  int r1 = arm_pool[n1].relax_end;
  double t_a = 0.0;
  double t_b = 0.0;
  double t_c = 0.0;
  double tt;
  double len_r2 = arm_pool[r2].arm_len_end;
  double len_n = arm_pool[n].arm_len_end;

  double zouter = arm_pool[n].arm_len;
  int k1 = arm_pool[n].next_friction;
  int k2 = arm_pool[n].nxt_relax;
  while (k1 != -1)
  {
    tt = arm_pool[k1].tau_collapse * pow(arm_pool[k1].phi_collapse, 2.0 * Alpha);
    t_a += tt;
    t_b += tt * zouter;
    zouter += arm_pool[k2].arm_len;
    k2 = arm_pool[k2].nxt_relax;
    k1 = arm_pool[k1].next_friction;
  }
  tt = arm_pool[r1].tau_collapse * pow(arm_pool[r1].phi_collapse, 2.0 * Alpha);
  t_a += tt;
  t_b += tt * zouter;

  zouter = arm_pool[r2].arm_len;
  k1 = arm_pool[r2].next_friction;
  k2 = arm_pool[r2].nxt_relax;
  while (k1 != -1)
  {
    tt = arm_pool[k1].tau_collapse * pow(arm_pool[k1].phi_collapse, 2.0 * Alpha);
    t_a -= tt;
    t_c += tt * zouter;
    zouter += arm_pool[k2].arm_len;
    k2 = arm_pool[k2].nxt_relax;
    k1 = arm_pool[k1].next_friction;
  }
  double tb1 = -t_b - t_c - t_a * (len_r2 - len_n);
  double tc1 = -t_c * len_n + len_r2 * (t_b - t_a * len_n);
  double xx = quad_solve_spl(t_a, tb1, tc1);
  if ((xx < arm_pool[n2].arm_len) &&
      ((arm_pool[r2].arm_len_end - arm_pool[r2].z) > xx))
  {
    int na = request_arm();
    int n0 = inner_arm_compound(n);
    if ((arm_pool[n2].L1 == n0) || (arm_pool[n2].L2 == n0))
    {
      arm_pool[n2].L1 = na;
      arm_pool[n2].L2 = -1;
      arm_pool[na].R1 = n2;
      arm_pool[na].R2 = -1;
      arm_pool[na].L1 = n0;
      arm_pool[na].L2 = n1;
      if (arm_pool[n0].R1 == n2)
      {
        arm_pool[n0].R1 = na;
      }
      else
      {
        arm_pool[n0].R2 = na;
      }
      if (arm_pool[n1].R1 == n2)
      {
        arm_pool[n1].R1 = na;
      }
      else
      {
        arm_pool[n1].R2 = na;
      }
    }
    else
    {
      arm_pool[n2].R1 = na;
      arm_pool[n2].R2 = -1;
      arm_pool[na].L1 = n2;
      arm_pool[na].L2 = -1;
      arm_pool[na].R1 = n0;
      arm_pool[na].R2 = n1;
      if (arm_pool[n0].L1 == n2)
      {
        arm_pool[n0].L1 = na;
      }
      else
      {
        arm_pool[n0].L2 = na;
      }
      if (arm_pool[n1].L1 == n2)
      {
        arm_pool[n1].L1 = na;
      }
      else
      {
        arm_pool[n1].L2 = na;
      }
    }
    arm_pool[na].arm_len = xx;
    arm_pool[na].vol_fraction = xx * arm_pool[n2].vol_fraction / arm_pool[n2].arm_len;
    arm_pool[n2].vol_fraction = (1.0 - xx / arm_pool[n2].arm_len) *
                                arm_pool[n2].vol_fraction;
    arm_pool[n].collapsed = false;
    arm_pool[n].freeze_arm_len_eff = false;
    gobble_arm(m, n, na, n1);
    arm_pool[n].nxtbranch1 = na;
    arm_pool[n].nxtbranch2 = -1;
    arm_pool[n2].arm_len -= xx;
    arm_pool[r2].arm_len_end -= xx;
    int nd = arm_pool[n2].down;
    arm_pool[n2].down = na;
    arm_pool[na].up = n2;
    arm_pool[na].down = nd;
    arm_pool[nd].up = na;
    arm_pool[r2].nxtbranch1 = na;
    arm_pool[r2].nxtbranch2 = -1;
    arm_pool[na].nxt_relax = -1;
    arm_pool[na].prune = false;
    arm_pool[na].ghost = false;
    arm_pool[na].collapsed = false;
    arm_pool[na].phi_collapse = -1.0;

    if (arm_pool[r2].arm_len_eff > arm_pool[r2].arm_len_end)
    {
      arm_pool[r2].arm_len_eff = arm_pool[r2].arm_len_end;
    }
  }
  else
  {
    ret_val = 1;
  }

  return (ret_val);
}
