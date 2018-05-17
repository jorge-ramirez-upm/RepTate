/*
armutil.cpp : This file is part bob-rheology (bob) 
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
#include <stdlib.h>
void pool_init(void)
{
  extern int first_avail_in_pool;
  extern arm *arm_pool;
  extern int max_arm;

  arm_pool = new arm[max_arm];
  if (arm_pool == NULL)
  {
    char s[256];
    sprintf(s, "ERROR : Could not allocate memory for arms. \nCurrent request was for %d arms. \nConsider reducing the number and try again. \n", max_arm);
    my_abort(s);
  }

  first_avail_in_pool = 0;
  for (int i = 0; i < max_arm; i++)
  {
    arm_pool[i].L1 = i - 1;
    arm_pool[i].R1 = i + 1;
  }
  arm_pool[max_arm - 1].R1 = -1;
}

int request_arm(void)
{
  extern int first_avail_in_pool;
  extern arm *arm_pool;

  int m = first_avail_in_pool;
  int nxt = arm_pool[m].R1;
  if (nxt == -1)
  {
    my_abort((char *)"Error : ran out of available arm in request_arm \n");
  }
  arm_pool[nxt].L1 = -1;
  first_avail_in_pool = nxt;
  arm_pool[m].L1 = arm_pool[m].L2 = arm_pool[m].R1 = arm_pool[m].R2 = -1;
  arm_pool[m].up = arm_pool[m].down = m;
  arm_pool[m].relax_end = -1;
  arm_pool[m].relaxing = false;
  return (m);
}

void return_arm(int m)
{
  extern int first_avail_in_pool;
  extern arm *arm_pool;
  int tmp = first_avail_in_pool;
  arm_pool[tmp].L1 = m;
  arm_pool[m].R1 = tmp;
  arm_pool[m].L1 = -1;
  first_avail_in_pool = m;
}

void set_tmpflag(int n)
{
  extern arm *arm_pool;
  extern polymer *branched_poly;
  int n0 = branched_poly[n].first_end;
  arm_pool[n0].tmpflag = true;
  int nd = arm_pool[n0].down;
  while (nd != n0)
  {
    arm_pool[nd].tmpflag = true;
    nd = arm_pool[nd].down;
  }
}

void unset_tmpflag(int n)
{
  extern arm *arm_pool;
  extern polymer *branched_poly;
  int n0 = branched_poly[n].first_end;
  arm_pool[n0].tmpflag = false;
  int nd = arm_pool[n0].down;
  while (nd != n0)
  {
    arm_pool[nd].tmpflag = false;
    nd = arm_pool[nd].down;
  }
}

// polymer n, everything on left of na are set true;
void set_tmpflag_left(int n, int na)
{
  extern arm *arm_pool;
  unset_tmpflag(n);
  arm_pool[na].tmpflag = true;

  int nL1 = arm_pool[na].L1;
  int nL2 = arm_pool[na].L2;
  if (nL1 != -1)
  {
    arm_pool[nL1].tmpflag = true;
  }
  if (nL2 != -1)
  {
    arm_pool[nL2].tmpflag = true;
  }

  if (nL1 != -1)
  {
    set_tmpflag_travel(nL1);
  }
  if (nL2 != -1)
  {
    set_tmpflag_travel(nL2);
  }

  arm_pool[na].tmpflag = false;
}

void set_tmpflag_right(int n, int na)
{
  extern arm *arm_pool;
  unset_tmpflag(n);
  arm_pool[na].tmpflag = true;

  int nR1 = arm_pool[na].R1;
  int nR2 = arm_pool[na].R2;
  if (nR1 != -1)
  {
    arm_pool[nR1].tmpflag = true;
  }
  if (nR2 != -1)
  {
    arm_pool[nR2].tmpflag = true;
  }

  if (nR1 != -1)
  {
    set_tmpflag_travel(nR1);
  }
  if (nR2 != -1)
  {
    set_tmpflag_travel(nR2);
  }

  arm_pool[na].tmpflag = false;
}

void set_tmpflag_travel(int na)
{
  extern arm *arm_pool;
  arm_pool[na].tmpflag = true;
  int nn = arm_pool[na].L1;
  if (nn != -1)
  {
    if (!arm_pool[nn].tmpflag)
    {
      set_tmpflag_travel(nn);
    }
  }
  nn = arm_pool[na].L2;
  if (nn != -1)
  {
    if (!arm_pool[nn].tmpflag)
    {
      set_tmpflag_travel(nn);
    }
  }
  nn = arm_pool[na].R1;
  if (nn != -1)
  {
    if (!arm_pool[nn].tmpflag)
    {
      set_tmpflag_travel(nn);
    }
  }
  nn = arm_pool[na].R2;
  if (nn != -1)
  {
    if (!arm_pool[nn].tmpflag)
    {
      set_tmpflag_travel(nn);
    }
  }
}

int request_attached_arm(int m)
{
  extern arm *arm_pool;
  int m1 = request_arm();
  arm_pool[m1].down = arm_pool[m].down;
  arm_pool[m].down = m1;
  arm_pool[m1].up = m;
  arm_pool[arm_pool[m1].down].up = m1;
  return m1;
}

void remove_arm_from_list(int m)
{
  extern arm *arm_pool;
  int nd = arm_pool[m].down;
  int nu = arm_pool[m].up;
  arm_pool[nu].down = nd;
  arm_pool[nd].up = nu;
}
