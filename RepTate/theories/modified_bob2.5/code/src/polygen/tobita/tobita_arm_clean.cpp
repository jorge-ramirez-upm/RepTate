/*
tobita_arm_clean.cpp : This file is part bob-rheology (bob) 
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
#include "./tobita.h"


void tob_add_arm(int n, int n1, int na)
{
extern std::vector <arm> arm_pool;
if(na != -1){
if(arm_pool[na].L1 == n1){arm_pool[na].L1=n;}
if(arm_pool[na].L2 == n1){arm_pool[na].L2=n;}
if(arm_pool[na].R1 == n1){arm_pool[na].R1=n;}
if(arm_pool[na].R2 == n1){arm_pool[na].R2=n;}
}

}
void tobita_arm_clean(int n, int * kk, int * tmp_pool)
{
extern std::vector <arm> arm_pool;
int n1=arm_pool[n].L1; int n2=arm_pool[n].L2;
int na; 

if( (n1 != -1) || (n2 != -1)){
  if( (n1 != -1) && (n2 != -1)){ // brach point on left
if(arm_pool[n1].tmpflag){arm_pool[n1].tmpflag=false; tobita_arm_clean(n1, &kk[0], tmp_pool);}
if(arm_pool[n2].tmpflag){arm_pool[n2].tmpflag=false; tobita_arm_clean(n2, &kk[0], tmp_pool);}
                               }
  else{ if(n1 != -1){ if(arm_pool[n1].tmpflag){
   arm_pool[n].arm_len+=arm_pool[n1].arm_len;
   if( (arm_pool[n1].L1 == n) || (arm_pool[n1].L2 == n)){
     na=arm_pool[n1].R1; arm_pool[n].L1=na; tob_add_arm(n, n1, na);
     na=arm_pool[n1].R2; arm_pool[n].L2=na; tob_add_arm(n,n1,na); }  
   else{
       na=arm_pool[n1].L1; arm_pool[n].L1=na; tob_add_arm(n, n1, na);
       na=arm_pool[n1].L2; arm_pool[n].L2=na; tob_add_arm(n, n1, na);} 

   remove_arm_from_list(n1); tmp_pool[kk[0]]=n1; kk[0]++;
   tobita_arm_clean(n, &kk[0], tmp_pool); }
                    }
        else{ if(arm_pool[n2].tmpflag){
   arm_pool[n].arm_len+=arm_pool[n2].arm_len;
   if( (arm_pool[n2].L1 == n) || (arm_pool[n2].L2 == n))
      { na=arm_pool[n2].R1; arm_pool[n].L1=na; tob_add_arm(n, n2,na);
        na=arm_pool[n2].R2; arm_pool[n].L2=na; tob_add_arm(n, n2, na);}
   else{ na=arm_pool[n2].L1; arm_pool[n].L1=na; tob_add_arm(n, n2, na);
         na=arm_pool[n2].L2; arm_pool[n].L2=na; tob_add_arm(n, n2, na);}
   remove_arm_from_list(n2); tmp_pool[kk[0]]=n2; kk[0]++;
   tobita_arm_clean(n, &kk[0], tmp_pool); }
            }

      }
                             }


int n3=arm_pool[n].R1; int n4=arm_pool[n].R2;
if( (n3 != -1) || (n4 != -1)){
  if( (n3 != -1) && (n4 != -1)){ // brach point on right
if(arm_pool[n3].tmpflag){arm_pool[n3].tmpflag=false; tobita_arm_clean(n3, &kk[0], tmp_pool);}
if(arm_pool[n4].tmpflag){arm_pool[n4].tmpflag=false; tobita_arm_clean(n4, &kk[0], tmp_pool);}
                               }
  else{ if(n3 != -1){ if(arm_pool[n3].tmpflag){
   arm_pool[n].arm_len+=arm_pool[n3].arm_len;
   if( (arm_pool[n3].L1 == n) || (arm_pool[n3].L2 == n))
      {
     na=arm_pool[n3].R1; arm_pool[n].R1=na; tob_add_arm(n, n3, na);
     na=arm_pool[n3].R2; arm_pool[n].R2=na; tob_add_arm(n,n3,na); }  
   else{ na=arm_pool[n3].L1; arm_pool[n].R1=na; tob_add_arm(n, n3, na);
       na=arm_pool[n3].L2; arm_pool[n].R2=na; tob_add_arm(n, n3, na);} 
   remove_arm_from_list(n3); tmp_pool[kk[0]]=n3; kk[0]++;
   tobita_arm_clean(n, &kk[0], tmp_pool); }
                    }
        else{ if(arm_pool[n4].tmpflag){
   arm_pool[n].arm_len+=arm_pool[n4].arm_len;
   if( (arm_pool[n4].L1 == n) || (arm_pool[n4].L2 == n))
      { na=arm_pool[n4].R1; arm_pool[n].R1=na; tob_add_arm(n, n4, na);
     na=arm_pool[n4].R2; arm_pool[n].R2=na; tob_add_arm(n,n4,na); }  
   else{ na=arm_pool[n4].L1; arm_pool[n].R1=na; tob_add_arm(n, n4, na);
       na=arm_pool[n4].L2; arm_pool[n].R2=na; tob_add_arm(n, n4, na);} 
   remove_arm_from_list(n4); tmp_pool[kk[0]]=n4; kk[0]++;
   tobita_arm_clean(n, &kk[0], tmp_pool); }
            }

      }
                             }
}
