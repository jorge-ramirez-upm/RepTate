/*
tobita_grow.cpp : This file is part bob-rheology (bob) 
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
#include "../../../include/MersenneTwister.h"
#include "./tobita.h"
#include <stdio.h>
void tobita_grow(int dir, int m, double cur_conv, bool sc_tag, int * rlevel, 
   double cs, double cb, double fin_conv,double tau, double beta, int* bcount) {
int m1, m2;
double new_conv, seg_len;
extern std::vector <arm> arm_pool;
extern MTRand mtrand1;
double sigma, psigma, lambda, plambda, pref;

rlevel[0]++; if(rlevel[0] > 1000){printf("tobita level : %d \n",rlevel[0]);errmsg(221);}
else{
seg_len=scilength(cur_conv, cs, fin_conv);
if(sc_tag && (seg_len < arm_pool[m].arm_len)){
   arm_pool[m].arm_len=seg_len; arm_pool[m].relaxing=true;}

seg_len=brlength(cur_conv,cb, fin_conv);

if(seg_len < arm_pool[m].arm_len){ // branch point
bcount[0]++;  m1=request_attached_arm(m); 

arm_pool[m1].arm_len=arm_pool[m].arm_len-seg_len; arm_pool[m].arm_len=seg_len; 
arm_pool[m1].z=cur_conv; arm_pool[m1].relaxing=arm_pool[m].relaxing; 
arm_pool[m].relaxing=false;
m2=request_attached_arm(m); 
new_conv=getconv2(cur_conv,fin_conv);
seg_len=calclength(new_conv, cs, cb, tau, beta);
arm_pool[m2].arm_len=seg_len; arm_pool[m2].z=new_conv; 
arm_pool[m2].relaxing=false;

if(dir > 0){arm_pool[m].R1=m1; arm_pool[m].R2=m2; 
arm_pool[m1].L2=m; arm_pool[m1].L1=m2; 
arm_pool[m2].L1=m; arm_pool[m2].L2=m1;
tobita_grow(1, m2, new_conv, true, &rlevel[0], cs, cb,fin_conv,tau,beta, &bcount[0]);
tobita_grow(dir, m1, cur_conv, false, &rlevel[0], cs, cb,fin_conv,tau,beta, &bcount[0]);
           }
else{ arm_pool[m].L1=m1;  arm_pool[m].L2=m2; 
arm_pool[m1].R2=m; arm_pool[m1].R1=m2; 
arm_pool[m2].L2=m1; arm_pool[m2].L1=m; 
tobita_grow(1, m2, new_conv, true, &rlevel[0], cs, cb,fin_conv,tau,beta, &bcount[0]);
tobita_grow(dir, m1, cur_conv, false, &rlevel[0], cs, cb,fin_conv,tau,beta, &bcount[0]);
    } }  // end work on branch point
else{ // nonside branch
if(arm_pool[m].relaxing){
  if(mtrand1() <= 0.50){
   new_conv=getconv2(cur_conv,fin_conv); m1=request_attached_arm(m); 
   seg_len=calclength(new_conv, cs, cb, tau, beta);
   arm_pool[m1].arm_len=seg_len; arm_pool[m1].z=new_conv;
   arm_pool[m1].relaxing=false;
if(dir > 0){arm_pool[m].R1=m1; arm_pool[m1].L2=m; }
else{arm_pool[m].L1=m1; arm_pool[m1].L2=m; }
tobita_grow(1, m1, new_conv, true, &rlevel[0], cs, cb,fin_conv,tau,beta, &bcount[0]);
                       }}
else{ if(dir > 0){
sigma=cs*cur_conv/(1.0 - cur_conv); lambda=cb*cur_conv/(1.0-cur_conv); 
pref=tau+beta+sigma+lambda; 
if(mtrand1() < (beta/pref)){
m1=request_attached_arm(m); 
seg_len=calclength(cur_conv, cs, cb, tau, beta);
arm_pool[m1].arm_len=seg_len; arm_pool[m1].z=cur_conv;
arm_pool[m].R1=m1;  arm_pool[m1].R2=m; 
tobita_grow(-1, m1, cur_conv, true, &rlevel[0], cs, cb,fin_conv,tau,beta, &bcount[0]);
                     }
         }
else{
sigma=cs*cur_conv/(1.0 - cur_conv); lambda=cb*cur_conv/(1.0-cur_conv); 
pref=tau+beta+sigma+lambda; 
plambda=lambda/pref; psigma=sigma/pref;
double randnum1=mtrand1();
if(randnum1 < plambda){bcount[0]++; new_conv=getconv1(cur_conv); 
m1=request_attached_arm(m); 
arm_pool[m1].arm_len=calclength(new_conv, cs, cb, tau, beta); arm_pool[m1].z=new_conv;
arm_pool[m1].relaxing=false;
arm_pool[m].L1=m1;  arm_pool[m1].L2=m; 
tobita_grow(1, m1, new_conv, true, &rlevel[0], cs, cb,fin_conv,tau,beta, &bcount[0]);
m2=request_attached_arm(m); 
arm_pool[m2].arm_len=calclength(new_conv, cs, cb, tau, beta); arm_pool[m2].z=new_conv;
arm_pool[m2].relaxing=false;
arm_pool[m].L2=m2;  arm_pool[m2].R1=m; 
arm_pool[m1].L1=m2; arm_pool[m2].R2=m1; 
tobita_grow(-1, m2, new_conv, true, &rlevel[0], cs, cb,fin_conv,tau,beta, &bcount[0]);
}
else{
if(randnum1 < (psigma + plambda)){ new_conv=getconv1(cur_conv); 
if(mtrand1() <= 0.50){
m1=request_attached_arm(m); 
arm_pool[m1].arm_len=calclength(new_conv, cs, cb, tau, beta); arm_pool[m1].z=new_conv;
arm_pool[m1].relaxing=false;
arm_pool[m].L1=m1;  arm_pool[m1].L2=m; 
tobita_grow(1, m1, new_conv, true, &rlevel[0], cs, cb,fin_conv,tau,beta, &bcount[0]);
                     }
else{
m2=request_attached_arm(m); 
arm_pool[m2].arm_len=calclength(new_conv, cs, cb, tau, beta); arm_pool[m2].z=new_conv;
arm_pool[m2].relaxing=false;
arm_pool[m].L2=m2;  arm_pool[m2].R1=m; 
tobita_grow(-1, m2, new_conv, true, &rlevel[0], cs, cb,fin_conv,tau,beta, &bcount[0]);
    }
                                  }
    }

}

}

}
rlevel[0]--; }
}
