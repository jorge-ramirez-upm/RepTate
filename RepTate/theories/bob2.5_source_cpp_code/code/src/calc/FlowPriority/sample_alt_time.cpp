/*
sample_alt_time.cpp : This file is part bob-rheology (bob) 
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
#include <math.h>
void sample_alt_time(void)
{
extern polymer * branched_poly;
extern polycopy * br_copy;
extern double  cur_time;
extern double phi_ST;
extern double PSquare;
extern double Alpha;
extern arm * arm_pool;
extern void alt_time_assign(int, int, int, int);
extern int nlin_relaxing_arm(int, double);
extern int num_poly;
for(int i=0; i<num_poly; i++){
 if(branched_poly[i].alive){
int n1=branched_poly[i].first_end;
int orig_narm=br_copy[i].narm;
  if(!arm_pool[n1].compound){   //extra check suggested by Chinmay
if((arm_pool[n1].collapsed) || (arm_pool[n1].ghost) || (arm_pool[n1].prune)){
             alt_time_assign(i, n1, arm_pool[n1].relax_end, orig_narm); }
  } // end check suggested by Chinmay
else{
if(arm_pool[n1].compound){
  double zz=arm_pool[n1].z;
  int na=nlin_relaxing_arm(n1, zz);
if(na != n1){ // n1 has collapsed
         alt_time_assign(i, n1, arm_pool[n1].relax_end, orig_narm);
int nb=arm_pool[n1].nxt_relax;
while(nb != na){ // Check nb and assign time
         alt_time_assign(i, nb, arm_pool[nb].relax_end, orig_narm);
   nb=arm_pool[nb].nxt_relax;
               }
if((arm_pool[n1].arm_len_end - zz) < 1.0e-1){ // we are near full retraction
  // capture it before it goes out of list
   alt_time_assign(i, na, arm_pool[na].relax_end, orig_narm); } 
            }

                         }
    }

int n2=arm_pool[n1].down;
while(n2 != n1){
if((arm_pool[n2].collapsed) || (arm_pool[n2].ghost) || (arm_pool[n2].prune)){
   alt_time_assign(i, n2, arm_pool[n2].relax_end, orig_narm); }
else{
if(arm_pool[n2].compound){
  double zz=arm_pool[n2].z;
  int na=nlin_relaxing_arm(n2, zz);
if(na != n2){ // n2 has collapsed
         alt_time_assign(i, n2,arm_pool[n2].relax_end, orig_narm);
int nb=arm_pool[n2].nxt_relax;
while(nb != na){ // Check nb and assign time
         alt_time_assign(i, nb,arm_pool[nb].relax_end,  orig_narm);
   nb=arm_pool[nb].nxt_relax;
               }
if((arm_pool[n2].arm_len_end - zz) < 1.0e-1){ // we are near full retraction
  // capture it before it goes out of list
   alt_time_assign(i, na, arm_pool[na].relax_end, orig_narm); }
            }

                         }


    }
n2=arm_pool[n2].down;
               }
                           } // branched_poly[i].alive
 else{
  if(br_copy[i].active == 0){
 //  br_copy[i].active=-1;
    for(int j=0; j< br_copy[i].narm; j++){
      if(br_copy[i].assigned_trelax[j] != 0){
                   br_copy[i].assigned_trelax[j]=0;
                   br_copy[i].relax_end[j]=-500;
                   br_copy[i].trelax[j]=cur_time;
                   br_copy[i].zeta[j]=2.0*pow(phi_ST,Alpha)*cur_time/3.0/PSquare;
                                            }
                                        }
                            }
     }
                             }

}

void alt_time_assign(int i, int n1, int nrelax, int orig_narm)
{
extern polycopy * br_copy;
extern double  cur_time;
extern double phi_ST;
extern double Alpha;
extern double PSquare;
for(int k=0; k<orig_narm; k++){
    if(br_copy[i].armindx[k]==n1){
      if(br_copy[i].assigned_trelax[k] != 0){
          br_copy[i].assigned_trelax[k]=0;
          br_copy[i].relax_end[k]=nrelax;
          br_copy[i].trelax[k]=cur_time; 
          br_copy[i].zeta[k]=2.0*pow(phi_ST,Alpha)*cur_time/3.0/PSquare;
                                            }
                             } }
}

