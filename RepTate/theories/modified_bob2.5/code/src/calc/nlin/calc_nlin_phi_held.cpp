/*
calc_nlin_phi_held.cpp : This file is part bob-rheology (bob) 
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
void calc_nlin_phi_held(void)
{
  extern std::vector<polymer> branched_poly;
  extern std::vector<arm> arm_pool;
  extern int num_poly;
  extern std::vector<std::vector<double> > nlin_prio_phi_held;
  int n1, n2;

  for (int i = 0; i < num_poly; i++)
  {
    if (branched_poly[i].alive)
    {
      n1 = branched_poly[i].first_free;
      n2 = arm_pool[n1].free_down;
      calc_free_arm_phi_held(n1);
      while (n2 != n1)
      {
        calc_free_arm_phi_held(n2);
        n2 = arm_pool[n2].free_down;
      }

      n1 = branched_poly[i].first_end;
      n2 = arm_pool[n1].down;
      if (!arm_pool[n1].relaxing)
      {
        nlin_prio_phi_held[arm_pool[n1].priority][0] += arm_pool[n1].arm_len;
      }
      while (n2 != n1)
      {
        if (!arm_pool[n2].relaxing)
        {
          nlin_prio_phi_held[arm_pool[n2].priority][0] += arm_pool[n2].arm_len;
        }
        n2 = arm_pool[n2].down;
      }
    }
  }
}
