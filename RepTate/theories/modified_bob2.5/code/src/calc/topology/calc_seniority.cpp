/*
calc_seniority.cpp : This file is part bob-rheology (bob) 
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
 
// calculate seniority of polymer n
// 25 Feb 2007
#include "../../../include/bob.h"
#include <stdlib.h>
#include <stdio.h>
void calc_seniority(int n) {
 extern std::vector <arm> arm_pool; extern std::vector <polymer> branched_poly;
 extern void set_seniority(int,int);
 int n1=branched_poly[n].first_end; set_seniority(n,n1);
 int n2=arm_pool[n1].down;
 while(n2 != n1){set_seniority(n,n2); n2=arm_pool[n2].down;}}

void set_seniority(int n, int n1) {
extern std::vector <arm> arm_pool;
if(arm_pool[n1].free_end){arm_pool[n1].seniority=1;}
else{
  int nL1=arm_pool[n1].L1; int nL2=arm_pool[n1].L2;
  int nR1=arm_pool[n1].R1; int nR2=arm_pool[n1].R2;
  extern void partial_seniority(int, int, int, int, int *);
  int sL; sL=0; partial_seniority(n,n1,nL1,nL2, &sL); 
  int sR; sR=0; partial_seniority(n,n1,nR1,nR2, &sR);
if(sL <= sR){arm_pool[n1].seniority = sL;}
else{arm_pool[n1].seniority = sR;} }}

void partial_seniority(int n, int n1, int nL1, int nL2, int * psL) {
extern std::vector <arm> arm_pool;
int psL1, psL2; psL1=0; psL2=0;
 set_tmpflag(n);
arm_pool[n1].tmpflag=false; arm_pool[nL2].tmpflag=false;
if(arm_pool[nL1].free_end){psL1=1;}
else{ int nL1a=arm_pool[nL1].L1; int nL1b=arm_pool[nL1].L2; 
int nL1c=arm_pool[nL1].R1; int nL1d=arm_pool[nL1].R2; 
if((nL1a==-1) || (nL1b==-1) || (nL1c==-1) || (nL1d ==-1))
   {printf("inconsistent architechture in partial_seniority.cpp \n");}
if(arm_pool[nL1a].tmpflag){partial_seniority(n,nL1,nL1a,nL1b,&psL1);}
else{partial_seniority(n,nL1,nL1c,nL1d,&psL1);} }

set_tmpflag(n); arm_pool[nL1].tmpflag=false; arm_pool[n1].tmpflag=false;
if(arm_pool[nL2].free_end){psL2=1;}
else{ int nL2a=arm_pool[nL2].L1; int nL2b=arm_pool[nL2].L2; 
int nL2c=arm_pool[nL2].R1; int nL2d=arm_pool[nL2].R2; 
if((nL2a==-1) || (nL2b==-1) || (nL2c==-1) || (nL2d ==-1))
   {printf("inconsistent architechture in partial_seniority.cpp \n");}
if(arm_pool[nL2a].tmpflag){partial_seniority(n,nL2,nL2a,nL2b,&psL2);}
else{partial_seniority(n,nL2,nL2c,nL2d,&psL2);} }

if(psL1 >= psL2){psL[0]=psL1 + 1;}
else{psL[0]=psL2 + 1;} }
