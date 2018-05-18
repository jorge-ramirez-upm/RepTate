/*
calc_snip_priority.cpp : This file is part bob-rheology (bob) 
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

// Calculate priority of polymer n
// If PrioMode != 0, neglect hanging bits less than one entanglement.
#include "../../../include/bob.h"
#include <stdlib.h>
#include <stdio.h>
void calc_snip_priority(int n)
{

  extern std::vector<arm> arm_pool;
  extern std::vector<polymer> branched_poly;
  extern void set_snip_prio(int, int);
  int n1 = branched_poly[n].first_end;
  set_snip_prio(n, n1);
  int n2 = arm_pool[n1].down;
  while (n2 != n1)
  {
    set_snip_prio(n, n2);
    n2 = arm_pool[n2].down;
  }
}

void set_snip_prio(int n, int n1)
{
  extern std::vector<arm> arm_pool;
  extern std::vector<polymer> branched_poly;
  //  extern int PrioMode;
  if (arm_pool[n1].relaxing)
  {
    arm_pool[n1].priority = 1;
  }
  else
  {

    set_tmpflag_left(n, n1);
    int mL = 0;
    int n0 = branched_poly[n].first_free;
    if (arm_pool[n0].tmpflag)
    {
      if ((!arm_pool[n0].ghost) && (!arm_pool[n0].prune) && (!arm_pool[n0].collapsed))
      {
        mL++;
      }
    }
    int nd = arm_pool[n0].free_down;
    while (nd != n0)
    {
      if (arm_pool[nd].tmpflag)
      {
        if ((!arm_pool[nd].ghost) && (!arm_pool[nd].prune) && (!arm_pool[nd].collapsed))
        {
          mL++;
        }
      }
      nd = arm_pool[nd].free_down;
    }
    if (mL == 0)
    {
      mL = 1;
    }

    set_tmpflag_right(n, n1);
    int mR = 0;
    n0 = branched_poly[n].first_free;
    if (arm_pool[n0].tmpflag)
    {
      if ((!arm_pool[n0].ghost) && (!arm_pool[n0].prune) && (!arm_pool[n0].collapsed))
      {
        mR++;
      }
    }
    nd = arm_pool[n0].free_down;
    while (nd != n0)
    {
      if (arm_pool[nd].tmpflag)
      {
        if ((!arm_pool[nd].ghost) && (!arm_pool[nd].prune) && (!arm_pool[nd].collapsed))
        {
          mR++;
        }
      }
      nd = arm_pool[nd].free_down;
    }
    if (mR == 0)
    {
      mR = 1;
    }

    if (mL < mR)
    {
      arm_pool[n1].priority = mL;
    }
    else
    {
      arm_pool[n1].priority = mR;
    }
  }
}
