/*
poly_start.cpp : This file is part bob-rheology (bob) 
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
/* When created a polymer simply has the first end fixed and a bunch of
connected arms. This routine sets up the flags and other variables needed for
the relaxation. */

void poly_start(polymer* cur_poly)
{
extern arm * arm_pool;
cur_poly[0].alive=true; cur_poly[0].relaxed_frac=0.0;
cur_poly[0].rept_set=false; cur_poly[0].ghost_contrib=0.0;
int n1=cur_poly[0].first_end; arm_start(n1); int num_seg=1;
int n2=arm_pool[n1].down;
     while(n2 != n1)
      {
        arm_start(n2); num_seg++; n2=arm_pool[n2].down;
      }
     cur_poly[0].num_branch=num_seg;
     if(num_seg == 2)
        cur_poly[0].linear_tag=true;
     else
        cur_poly[0].linear_tag=false;

if(num_seg <= 3) // star or linear
{
 n1=cur_poly[0].first_end; arm_pool[n1].freeze_arm_len_eff=true; 
 n2=arm_pool[n1].down;
     while(n2 != n1)
      {
       arm_pool[n2].freeze_arm_len_eff=true; n2=arm_pool[n2].down;
      }
}

bool found_free=false;
     n1=cur_poly[0].first_end;
     if(arm_pool[n1].free_end)
      {
       cur_poly[0].first_free=n1; found_free=true;
       arm_pool[n1].free_up=n1; arm_pool[n1].free_down=n1;
      }
     n2=arm_pool[n1].down;
     while(n2 !=n1)
      {
        if(arm_pool[n2].free_end)
         {
            if(!found_free)
             {
              cur_poly[0].first_free=n2; found_free=true;
              arm_pool[n2].free_up=n2; arm_pool[n2].free_down=n2;
             }
            else
             {
               int n3=cur_poly[0].first_free;
               int n4=arm_pool[n3].free_up;
               arm_pool[n3].free_up=n2; arm_pool[n2].free_down=n3;
               arm_pool[n2].free_up=n4; arm_pool[n4].free_down=n2;
             }
         }
         n2=arm_pool[n2].down;
      }



}
