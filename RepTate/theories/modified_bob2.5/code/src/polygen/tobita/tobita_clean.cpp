/*
tobita_clean.cpp : This file is part bob-rheology (bob) 
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
#include "./tobita.h"
#include <stdio.h>
void tobita_clean(polymer *cur_poly)
{
  extern std::vector<arm> arm_pool;
  int kk = 1;
  int n0 = cur_poly[0].first_end;
  arm_pool[n0].tmpflag = false;
  int nmin = n0;
  int nmax = n0;
  int nd = arm_pool[n0].down;
  if (nmin > nd)
  {
    nmin = nd;
  }
  if (nmax < nd)
  {
    nmax = nd;
  }
  while (nd != n0)
  {
    arm_pool[nd].tmpflag = true;
    nd = arm_pool[nd].down;
    kk++;
    if (nmin > nd)
    {
      nmin = nd;
    }
    if (nmax < nd)
    {
      nmax = nd;
    }
  }
  n0 = cur_poly[0].first_end;
  arm_pool[n0].tmpflag = false;
  int *tmp_pool = new int[kk];
  kk = 0;
  int found_it;
  int nk;

  tobita_arm_clean(n0, &kk, tmp_pool);

  while (kk != 0)
  {
    found_it = -1;
    for (int i = 0; i < kk; i++)
    {
      if (tmp_pool[i] == nmax)
      {
        found_it = 0;
        return_arm(tmp_pool[i]);
      }
      if ((found_it == 0) && (i != (kk - 1)))
      {
        tmp_pool[i] = tmp_pool[i + 1];
      }
    }
    if (found_it == 0)
    {
      kk--;
      nmax--;
    }
    else
    { // the arm is in the polymer
      n0 = cur_poly[0].first_end;
      nk = tmp_pool[kk - 1];
      if (n0 == nmax)
      {
        tobita_swap_arm(nk, n0);
        kk--;
        nmax--;
        return_arm(n0);
        cur_poly[0].first_end = nk;
      }
      else
      {
        nd = arm_pool[n0].down;
        while (nd != nmax)
        {
          nd = arm_pool[nd].down;
        }
        tobita_swap_arm(nk, nd);
        kk--;
        nmax--;
        return_arm(nd);
      }
    }
  }

  n0 = cur_poly[0].first_end;
  nd = arm_pool[n0].down;
  if (n0 == nd)
  { // we have a linear
    nd = request_attached_arm(n0);
    arm_pool[nd].arm_len = arm_pool[n0].arm_len / 2.0;
    arm_pool[n0].arm_len = arm_pool[n0].arm_len / 2.0;
    arm_pool[n0].L1 = arm_pool[n0].L2 = arm_pool[n0].R2 = -1;
    arm_pool[n0].R1 = nd;
    arm_pool[nd].L1 = n0;
    arm_pool[nd].L2 = arm_pool[nd].R1 = arm_pool[nd].R2 = -1;
  }

  n0 = cur_poly[0].first_end;
  nd = arm_pool[n0].down;
  extern double N_e;
  arm_pool[n0].arm_len = arm_pool[n0].arm_len / N_e;
  while (nd != n0)
  {
    arm_pool[nd].arm_len = arm_pool[nd].arm_len / N_e;
    nd = arm_pool[nd].down;
  }

  delete[] tmp_pool;
}
// assign attributes of arm n to m
void tobita_swap_arm(int m, int n)
{
  extern std::vector<arm> arm_pool;
  arm_pool[m].arm_len = arm_pool[n].arm_len;
  int nt = arm_pool[n].up;
  arm_pool[m].up = nt;
  arm_pool[nt].down = m;
  nt = arm_pool[n].down;
  arm_pool[m].down = nt;
  arm_pool[nt].up = m;
  nt = arm_pool[n].L1;
  arm_pool[m].L1 = nt;
  if (nt != -1)
  {
    if (arm_pool[nt].L1 == n)
    {
      arm_pool[nt].L1 = m;
    }
    if (arm_pool[nt].L2 == n)
    {
      arm_pool[nt].L2 = m;
    }
    if (arm_pool[nt].R1 == n)
    {
      arm_pool[nt].R1 = m;
    }
    if (arm_pool[nt].R2 == n)
    {
      arm_pool[nt].R2 = m;
    }
  }
  nt = arm_pool[n].L2;
  arm_pool[m].L2 = nt;
  if (nt != -1)
  {
    if (arm_pool[nt].L1 == n)
    {
      arm_pool[nt].L1 = m;
    }
    if (arm_pool[nt].L2 == n)
    {
      arm_pool[nt].L2 = m;
    }
    if (arm_pool[nt].R1 == n)
    {
      arm_pool[nt].R1 = m;
    }
    if (arm_pool[nt].R2 == n)
    {
      arm_pool[nt].R2 = m;
    }
  }
  nt = arm_pool[n].R1;
  arm_pool[m].R1 = nt;
  if (nt != -1)
  {
    if (arm_pool[nt].L1 == n)
    {
      arm_pool[nt].L1 = m;
    }
    if (arm_pool[nt].L2 == n)
    {
      arm_pool[nt].L2 = m;
    }
    if (arm_pool[nt].R1 == n)
    {
      arm_pool[nt].R1 = m;
    }
    if (arm_pool[nt].R2 == n)
    {
      arm_pool[nt].R2 = m;
    }
  }
  nt = arm_pool[n].R2;
  arm_pool[m].R2 = nt;
  if (nt != -1)
  {
    if (arm_pool[nt].L1 == n)
    {
      arm_pool[nt].L1 = m;
    }
    if (arm_pool[nt].L2 == n)
    {
      arm_pool[nt].L2 = m;
    }
    if (arm_pool[nt].R1 == n)
    {
      arm_pool[nt].R1 = m;
    }
    if (arm_pool[nt].R2 == n)
    {
      arm_pool[nt].R2 = m;
    }
  }
}
