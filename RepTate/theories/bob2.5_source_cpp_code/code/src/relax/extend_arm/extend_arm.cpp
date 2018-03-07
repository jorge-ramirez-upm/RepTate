/*
extend_arm.cpp : This file is part bob-rheology (bob) 
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
 
// For compound arm, calculate Z_eff. If allowed and needed, add inner segments
#include "../../../include/bob.h"
#include "../relax.h"
#include <iostream>
#include <cstdlib>
using namespace std;
void extend_arm(int m, int n)   // branched_poly[m].arm_pool[n]
{ 
extern arm * arm_pool;

  if(arm_pool[n].freeze_arm_len_eff) // n can not be extended
    {
      arm_pool[n].deltazeff=0.0;
      if(arm_pool[n].collapsed) collapse_star_arm(m,n);
    }
  else // !arm_pool[n].freeze_arm_len
    {
      if(!arm_pool[n].collapsed)
       {
         uncollapsed_extend(m,n);
       }
     else  // arm_pool[n].collapsed
       {
      int n1=arm_pool[n].nxtbranch1; int n2=arm_pool[n].nxtbranch2;
        if((n1==-1) || (n2==-1)) { collapse_star_arm(m,n); }
        else  // both n1 and n2 points to valid arm
         {
           if( (!arm_pool[n1].relaxing) && (!arm_pool[n2].relaxing) )
            { mk_ghost(m,n); }
           else
            {
              if(!arm_pool[n1].relaxing)
               {
                 semiconstrained_extend_arm(m,n,n1,n2);
               }
              else
               {
                 if(!arm_pool[n2].relaxing)
                  {
                    semiconstrained_extend_arm(m,n,n2,n1);
                  }
                 else
                  {  // both n1 and n2 are relaxing
                    collapse_star_arm(m,n);
                  }
               }
            }
         }
    }
   }
}
