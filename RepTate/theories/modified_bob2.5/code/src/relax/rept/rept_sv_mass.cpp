/*
rept_sv_mass.cpp : This file is part bob-rheology (bob) 
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
#include "../relax.h"
void rept_sv_mass(int m)
{
  extern std::vector<polymer> branched_poly;
  extern std::vector<arm> arm_pool;

  int n1 = branched_poly[m].first_free;
  int n2 = arm_pool[n1].free_down;
  if (n1 == n2)
  {
    if (!arm_pool[n1].ghost)
      sv_mass(m, n1);
  }
  else
  {
    if (!arm_pool[n1].ghost)
      sv_mass(m, n1);
    if (!arm_pool[n2].ghost)
      sv_mass(m, n2);
  }

  n1 = branched_poly[m].first_end;
  n2 = arm_pool[n1].down;
  if (!arm_pool[n1].relaxing)
  {
    branched_poly[m].relaxed_frac += arm_pool[n1].vol_fraction;
  }
  while (n2 != n1)
  {
    if (!arm_pool[n2].relaxing)
    {
      branched_poly[m].relaxed_frac += arm_pool[n2].vol_fraction;
    }
    n2 = arm_pool[n2].down;
  }
}
