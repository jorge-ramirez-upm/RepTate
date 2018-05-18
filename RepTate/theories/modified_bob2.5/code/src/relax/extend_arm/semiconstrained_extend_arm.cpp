/*
semiconstrained_extend_arm.cpp : This file is part bob-rheology (bob) 
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

// polymer m, arm n : neighbours n1, n2
#include "../../../include/bob.h"
#include "../relax.h"
#include <iostream>
using namespace std;
void semiconstrained_extend_arm(int m, int n, int n1, int n2)
{ // n2.relaxing && !n1.relaxing
  extern std::vector<arm> arm_pool;
  int r2 = arm_pool[n2].relax_end;

  if (!arm_pool[r2].collapsed)
  {
    mk_ghost(m, n);
  }
  else
  {
    int n11, n12;
    if ((arm_pool[n1].L1 == n2) || (arm_pool[n1].L2 == n2))
    {
      n11 = arm_pool[n1].R1;
      n12 = arm_pool[n1].R2;
    }
    else
    {
      n11 = arm_pool[n1].L1;
      n12 = arm_pool[n1].L2;
    }

    if ((n11 == -1) || (n12 == -1))
      cout << "Error : semiconstrained_extend_arm : something wrong" << endl;

    gobble_arm(m, n, n1, n2);
    arm_pool[n].nxtbranch1 = n11;
    arm_pool[n].nxtbranch2 = n12;
  }
}
