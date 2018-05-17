/*
prune_chain.cpp : This file is part bob-rheology (bob) 
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
 
//pruning chain m
#include "../../../include/bob.h"
#include "../relax.h"
void prune_chain(int m) 
{
extern std::vector <arm> arm_pool;
extern std::vector <polymer> branched_poly;

int n=branched_poly[m].first_free;
int n1=arm_pool[n].free_down;
  if(n1 == n)  // only one free end  
  {
   if(arm_pool[n].prune) // get the polymer out of here!
    {
     if(!arm_pool[n].ghost) sv_mass(m,n);
     branched_poly[m].alive=false;
    }
  }
  else  // more than one branch
  {
    while(n1 != n)
     {
       if(arm_pool[n1].prune)
        {
          if(!arm_pool[n1].ghost) sv_mass(m,n1); 
          int nf1=arm_pool[n1].free_down; int nf2=arm_pool[n1].free_up;
          arm_pool[nf2].free_down=nf1; arm_pool[nf1].free_up=nf2;
          n1=nf1; 
        }
       else
          n1=arm_pool[n1].free_down;
     }
// we still need to check n 
     n1=arm_pool[n].free_down;
     if(n1==n) //rest of the arm got deleted :: again single arm linear
      {
        if(arm_pool[n].prune) // get the polymer out of here!
         {
          if(!arm_pool[n].ghost) sv_mass(m,n);
          branched_poly[m].alive=false;
         }
       }
      else  //n1 is different
       {
         if(arm_pool[n].prune)
          {
           if(!arm_pool[n].ghost) sv_mass(m,n);
           int nf1=arm_pool[n].free_down; int nf2=arm_pool[n].free_up;
           arm_pool[nf2].free_down=nf1; arm_pool[nf1].free_up=nf2;
           branched_poly[m].first_free=nf1;
          }
       }
     
  }

}
