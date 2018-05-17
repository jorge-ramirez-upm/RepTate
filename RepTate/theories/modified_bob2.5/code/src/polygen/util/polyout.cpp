/*
polyout.cpp : This file is part bob-rheology (bob) 
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
#include <cstdlib>
void polyout(int m)
{
extern std::vector <arm> arm_pool;
extern std::vector <polymer> branched_poly;
extern double cur_time;
extern FILE * debugfl;

int n1=branched_poly[m].first_end;
int n2=arm_pool[n1].down;
if(debugfl == NULL) {debugfl=fopen("debg.dat","w");}
fprintf(debugfl,"%e \n",cur_time);
fprintf(debugfl, "%d \n", m);
fprintf(debugfl, "%d %d %e %e %e %e %d %d \n", n1,arm_pool[n1].nxt_relax,
   arm_pool[n1].z, arm_pool[n1].arm_len_eff, 
     arm_pool[n1].arm_len_end,arm_pool[n1].extra_drag,
arm_pool[n1].nxtbranch1,arm_pool[n1].nxtbranch2);
while(n2 != n1)
{

fprintf(debugfl, "%d %d %e %e %e %e %d %d\n", n2,arm_pool[n2].nxt_relax,
   arm_pool[n2].z, arm_pool[n2].arm_len_eff, 
     arm_pool[n2].arm_len_end, arm_pool[n2].extra_drag,
arm_pool[n2].nxtbranch1,arm_pool[n2].nxtbranch2);

n2=arm_pool[n2].down;
}

}
