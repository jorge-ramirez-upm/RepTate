/*
mk_ghost.cpp : This file is part bob-rheology (bob) 
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
 
// turn branched_poly[m].arm_pool[n] to ghost
#include <math.h>
#include "../../../include/bob.h"
#include "../relax.h"

void mk_ghost(int m, int n)
{ 
extern std::vector <polymer> branched_poly;
extern std::vector <arm> arm_pool;
extern double Alpha;

double tmpvar = arm_pool[n].tau_collapse * 
                pow(arm_pool[n].phi_collapse,2.0*Alpha);
arm_pool[n].ghost=true;
branched_poly[m].ghost_contrib+=tmpvar; sv_mass(m,n);
}

