/*
nlin_relaxing_arm.cpp : This file is part bob-rheology (bob) 
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
#include <stdio.h>
int nlin_relaxing_arm(int n, double z)
{
  extern std::vector<arm> arm_pool;
  int na = n;
  double dz = arm_pool[n].arm_len;
  while (dz < z)
  {
    if (arm_pool[na].nxt_relax != -1)
    {
      na = arm_pool[na].nxt_relax;
      dz += arm_pool[na].arm_len;
    }
    else
    {
      if ((z - dz) > 1.e-6)
      {
        printf("possible error in nlin_relaxing_arm \n");
      }
      dz = z + tiny;
    }
  }
  return na;
}
