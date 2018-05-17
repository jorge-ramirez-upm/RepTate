/*
polygenMPE.cpp : This file is part bob-rheology (bob) 
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
#include <stdio.h>
#include <math.h>
void MPE_add_branch(int n, double branch_prob, double logprobs)
{
extern MTRand mtrand1; extern std::vector <arm> arm_pool;
extern double N_e;

int n1=request_arm(); int n2=request_arm();
arm_pool[n].R1=n1; arm_pool[n].R2=n2;
arm_pool[n1].L1=n; arm_pool[n1].L2=n2;
arm_pool[n2].L1=n; arm_pool[n2].L2=n1;
int nd=arm_pool[n].down;
arm_pool[n].down=n1; arm_pool[n1].up=n;
arm_pool[n1].down=n2; arm_pool[n2].up=n1;
arm_pool[n2].down=nd; arm_pool[nd].up=n2;

double seg_len=flory_distb(logprobs)/N_e; arm_pool[n1].arm_len=seg_len;
       seg_len=flory_distb(logprobs)/N_e; arm_pool[n2].arm_len=seg_len;
if(mtrand1() >= branch_prob)
 {arm_pool[n1].R1=-1; arm_pool[n1].R2=-1;}
else
 MPE_add_branch(n1,  branch_prob,  logprobs);

if(mtrand1() >= branch_prob)
 {arm_pool[n2].R1=-1; arm_pool[n2].R2=-1;}
else
 MPE_add_branch(n2,  branch_prob,  logprobs);

}

polymer polygenMPE(double prop_prob, double mono_prob)
{
extern MTRand mtrand1;
extern std::vector <arm> arm_pool;
extern double N_e;
polymer cur_poly;
double tmpvar = prop_prob*mono_prob;
double branch_prob= prop_prob * ( 1.0 - mono_prob)/(1.0 - tmpvar);
double logprobs=log(tmpvar);

 double seg_len=flory_distb(logprobs)/N_e;
if(mtrand1() >= branch_prob)
{
 cur_poly=polygenLin(seg_len);
}
else
{
 int n1=request_arm(); cur_poly.first_end=n1;
 arm_pool[n1].L1=arm_pool[n1].L2=-1;arm_pool[n1].arm_len=seg_len;
 arm_pool[n1].up=n1; arm_pool[n1].down=n1;
 MPE_add_branch(n1,branch_prob,logprobs);
}
poly_start(&cur_poly);
return(cur_poly);
}
