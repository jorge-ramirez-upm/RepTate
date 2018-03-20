/*
polygen_wtav.cpp : This file is part bob-rheology (bob) 
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
 
#include "../../../include/MersenneTwister.h"
#include "../../../include/bob.h"
void add_wt_right(int n, double logprob, double b_u, double b_d, int dir)
{ // dir >0 => downstream
extern MTRand mtrand1; extern arm * arm_pool;
extern double N_e;

int n1=request_arm(); int n2=request_arm();
arm_pool[n].R1=n1; arm_pool[n].R2=n2;
arm_pool[n1].L1=n; arm_pool[n1].L2=n2;
arm_pool[n2].L1=n; arm_pool[n2].L2=n1;
int nd=arm_pool[n].down;
arm_pool[n].down=n1; arm_pool[n1].up=n;
arm_pool[n1].down=n2; arm_pool[n2].up=n1;
arm_pool[n2].down=nd; arm_pool[nd].up=n2;
arm_pool[n1].arm_len=flory_distb(logprob)/N_e;
arm_pool[n2].arm_len=flory_distb(logprob)/N_e;

if(dir > 0){
if(mtrand1() >= b_d) {arm_pool[n1].R1=-1; arm_pool[n1].R2=-1;}
else{add_wt_right(n1, logprob, b_u,b_d, 1);}
           }
else{
if(mtrand1() >= b_u) {arm_pool[n1].R1=-1; arm_pool[n1].R2=-1;}
else{add_wt_right(n1, logprob, b_u,b_d, -1);}
           }


if(mtrand1() >= b_u) {arm_pool[n2].R1=-1; arm_pool[n2].R2=-1;}
else{add_wt_right(n2, logprob, b_u, b_d, -1);}
}

void add_wt_left(int n, double logprob, double bp)
{
extern MTRand mtrand1; extern arm * arm_pool;
extern double N_e;

int n1=request_arm(); int n2=request_arm();
arm_pool[n].L1=n1; arm_pool[n].L2=n2;
arm_pool[n1].R1=n; arm_pool[n1].R2=n2;
arm_pool[n2].R1=n; arm_pool[n2].R2=n1;
int nd=arm_pool[n].down;
arm_pool[n].down=n1; arm_pool[n1].up=n;
arm_pool[n1].down=n2; arm_pool[n2].up=n1;
arm_pool[n2].down=nd; arm_pool[nd].up=n2;
arm_pool[n1].arm_len=flory_distb(logprob)/N_e;
arm_pool[n2].arm_len=flory_distb(logprob)/N_e;
if(mtrand1() >= bp) {arm_pool[n1].L1=-1; arm_pool[n1].L2=-1;}
else{add_wt_left(n1, logprob, bp);}
if(mtrand1() >= bp) {arm_pool[n2].L1=-1; arm_pool[n2].L2=-1;}
else{add_wt_left(n2, logprob, bp);}
}


polymer polygen_wtav(int ptype, double logprob, double b_u)
{
polymer cur_poly;
extern double N_e;
double b_d;
extern MTRand mtrand1;
extern arm * arm_pool;
int n1=request_arm();  cur_poly.first_end=n1;
arm_pool[n1].L1=arm_pool[n1].L2=arm_pool[n1].R1=arm_pool[n1].R2=-1;
arm_pool[n1].arm_len=(flory_distb(logprob)+flory_distb(logprob))/N_e;

 arm_pool[n1].up=n1; arm_pool[n1].down=n1;
if(ptype == 0) { b_d=2.0*b_u;}
else{b_d = b_u;}
if(mtrand1() < b_u) {add_wt_left(n1,logprob, b_u);}
if(mtrand1() < b_d) {add_wt_right(n1,logprob,b_u,b_d,1);}
if((arm_pool[n1].L1 == -1) && (arm_pool[n1].R1 == -1)){ //linear
int n2=request_arm();double seglen=arm_pool[n1].arm_len;
arm_pool[n1].up=n2; arm_pool[n1].down=n2;
arm_pool[n2].up=n1; arm_pool[n2].down=n1;
arm_pool[n1].R1=n2; arm_pool[n2].L1=n1;
arm_pool[n1].arm_len=arm_pool[n2].arm_len=0.50*seglen;
}

poly_start(&cur_poly);
return(cur_poly);
}
