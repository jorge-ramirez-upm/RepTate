/*
sv_mass.cpp : This file is part bob-rheology (bob) 
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

/* Save the weight fraction carried by (possibly compound) arm 'n' on polymer
 'm' which has collapsed and is being removed from free arm list */

#include "../../../include/bob.h"
void sv_mass(int m, int n)
{
  extern std::vector<arm> arm_pool;
  extern std::vector<polymer> branched_poly;

  int nnxt = arm_pool[n].nxt_relax;
  branched_poly[m].relaxed_frac += arm_pool[n].vol_fraction;
  while (nnxt != -1)
  {
    branched_poly[m].relaxed_frac += arm_pool[nnxt].vol_fraction;
    nnxt = arm_pool[nnxt].nxt_relax;
  }
}
