/*
collapse_star_arm.cpp : This file is part bob-rheology (bob) 
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
 
// freeze_arm_len : 3 star or linear
#include "../../../include/bob.h"
#include "../relax.h"
#include <math.h>
#include<stdio.h>
void collapse_star_arm(int m, int n)
{
extern arm * arm_pool;
extern double Alpha;
double tmpvar=arm_pool[n].tau_collapse*pow(arm_pool[n].phi_collapse,2.0*Alpha);

int n1=arm_pool[n].nxtbranch1; int n2=arm_pool[n].nxtbranch2;

 if((n1 == -1) || (n2 == -1)) { if(n1 == -1) {
      int r1=arm_pool[n2].relax_end; 
      if(arm_pool[r1].collapsed) {arm_pool[n].prune=true;}
      else {arm_pool[r1].extra_drag+=tmpvar; arm_pool[n].prune=true;} }
    else {
      int r1=arm_pool[n1].relax_end;
      if(arm_pool[r1].collapsed) {arm_pool[n].prune=true;}
      else {arm_pool[r1].extra_drag+=tmpvar; arm_pool[n].prune=true;} } }
 else {
   int r1=arm_pool[n1].relax_end; int r2=arm_pool[n2].relax_end;
   if((arm_pool[r1].collapsed) && (arm_pool[r2].collapsed))
    {arm_pool[n].prune=true;}
   else {
     if((!arm_pool[r1].collapsed) && (!arm_pool[r2].collapsed)) {
       double tmpvar1=arm_pool[r1].arm_len_end - arm_pool[r1].z;
       double tmpvar2=arm_pool[r2].arm_len_end - arm_pool[r2].z;
        if(tmpvar1 > tmpvar2) {arm_pool[r1].extra_drag+=tmpvar;}
        else {arm_pool[r2].extra_drag +=tmpvar;}
        arm_pool[n].prune=true; }
     else {
       if(arm_pool[r1].collapsed) {
         if(!arm_pool[r2].compound)
          {arm_pool[r2].extra_drag+=tmpvar; arm_pool[n].prune=true;}
         else {
           if(share_arm(m,n,n1,n2) == 1) 
             {arm_pool[r2].extra_drag+=tmpvar; arm_pool[n].prune=true;} } }
       else { if(!arm_pool[r1].compound) {
              arm_pool[r1].extra_drag+=tmpvar; arm_pool[n].prune=true;}
              else {
           if(share_arm(m,n,n2,n1) == 1)
             {arm_pool[r1].extra_drag+=tmpvar; arm_pool[n].prune=true;} } }
      }
    }
  }

}

