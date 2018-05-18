/*
free_arm_relax_amount.cpp : This file is part bob-rheology (bob) 
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

/* For free arm n0 (possibly compound), find out how much material relaxed */
#include "../../../include/bob.h"
double free_arm_relax_amount(int n)
{
  extern std::vector<arm> arm_pool;
  double relax_amount = 0.0;
  int n0 = n;
  double dz = arm_pool[n0].z;

  while (dz > tiny)
  {
    if (dz > arm_pool[n0].arm_len)
    {
      relax_amount += arm_pool[n0].vol_fraction;
      dz = dz - arm_pool[n0].arm_len;
      n0 = arm_pool[n0].nxt_relax;
    }
    else
    {
      relax_amount += arm_pool[n0].vol_fraction * dz / arm_pool[n0].arm_len;
      n0 = -1;
    }
    if (n0 < 0)
      dz = -1.0;
  }

  return (relax_amount);
}
