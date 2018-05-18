/*
reptate_nlin.cpp : This file is part bob-rheology (bob) 
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

void reptate_nlin(int n)
{
  extern std::vector<polymer> branched_poly;
  extern std::vector<arm> arm_pool;
  extern std::vector<std::vector<double> > nlin_prio_phi_relax; // extern double nlin_dphi_true;

  int n1 = branched_poly[n].first_free;
  int n2 = arm_pool[n1].free_down;

  reptate_nlin_sngl_arm(n1);
  if (n1 != n2)
  {
    reptate_nlin_sngl_arm(n2);
  }

  // Consider material not visited by front having stretch time as current time
  n1 = branched_poly[n].first_end;
  n2 = arm_pool[n1].down;

  if (!arm_pool[n1].relaxing)
  {
    nlin_prio_phi_relax[arm_pool[n1].priority][0] += arm_pool[n1].vol_fraction;
    //   nlin_dphi_true+=arm_pool[n1].vol_fraction;
  }
  while (n2 != n1)
  {
    if (!arm_pool[n2].relaxing)
    {
      nlin_prio_phi_relax[arm_pool[n2].priority][0] += arm_pool[n2].vol_fraction;
      // nlin_dphi_true+=arm_pool[n2].vol_fraction;
    }
    n2 = arm_pool[n2].down;
  }
}
