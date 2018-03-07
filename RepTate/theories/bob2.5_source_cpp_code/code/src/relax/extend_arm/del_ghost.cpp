/*
del_ghost.cpp : This file is part bob-rheology (bob) 
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
 
//remove ghost entries from free arm list
#include <math.h>
#include "../../../include/bob.h"
void del_ghost(int m)
{ 
 extern polymer * branched_poly;
 extern arm * arm_pool;

 int n1=branched_poly[m].first_free;
 int n2=arm_pool[n1].free_down;
    while(n2 != n1)
     {
       if(arm_pool[n2].ghost)
        {
         int nf1=arm_pool[n2].free_down; int nf2=arm_pool[n2].free_up;
         arm_pool[nf2].free_down=nf1; arm_pool[nf1].free_up=nf2;
        }
       n2=arm_pool[n2].free_down;
     }
   if(arm_pool[n1].ghost)
     {
       int nf1=arm_pool[n1].free_down; int nf2=arm_pool[n1].free_up;
       arm_pool[nf2].free_down=nf1; arm_pool[nf1].free_up=nf2;
       branched_poly[m].first_free=nf1;
       if(nf1 == n1) branched_poly[m].alive=false;
     }
}
