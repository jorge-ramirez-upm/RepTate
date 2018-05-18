/*
inner_arm_compound.cpp : This file is part bob-rheology (bob) 
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

// For compound arm, find the inner-most arm
#include "../../../include/bob.h"
int inner_arm_compound(int n)
{
  extern std::vector<arm> arm_pool;
  int nnxt = arm_pool[n].nxt_relax;
  int nsv = n;
  while (nnxt != -1)
  {
    nsv = nnxt;
    nnxt = arm_pool[nsv].nxt_relax;
  }
  return (nsv);
}
