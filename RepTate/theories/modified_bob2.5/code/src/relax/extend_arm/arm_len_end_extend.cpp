/*
arm_len_end_extend.cpp : This file is part bob-rheology (bob) 
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

//n1 is relaxing but n2 is not
#include "../../../include/bob.h"
#include "../relax.h"
void arm_len_end_extend(int m, int n, int n1, int n2)
{
  extern std::vector<arm> arm_pool;

  int r1 = arm_pool[n1].relax_end;

  if (arm_pool[r1].collapsed)
  {
    if (arm_pool[n2].L1 == n1 || arm_pool[n2].L2 == n1)
    {
      arm_pool[n].nxtbranch1 = arm_pool[n2].R1;
      arm_pool[n].nxtbranch2 = arm_pool[n2].R2;
    }
    else
    {
      arm_pool[n].nxtbranch1 = arm_pool[n2].L1;
      arm_pool[n].nxtbranch2 = arm_pool[n2].L2;
    }

    gobble_arm(m, n, n2, n1);

  } // else nothing to do right now
}
