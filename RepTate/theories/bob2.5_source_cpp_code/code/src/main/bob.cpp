/*
bob.cpp : This file is part of bob-rheology (bob) 
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
 
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include "../../include/bob.h"
#include "../../include/MersenneTwister.h"
#include "../../include/global.h"

extern "C" int main(int, char **);

int main(int argc, char *argv[]) {
infofl=fopen("info.txt","w");    rcread();
int cont_exec=parser(argc, argv);
if(cont_exec == 1) {printf("Parser failed \n"); abort();}

if(cont_exec == 0){ user_interface(); poly_stat();
if(GenPolyOnly != 0){ 

if((Snipping != 0) && (CalcNlin != 0)){
   fprintf(infofl, "Following relaxation to calculate linear rheology\n");
                                      }
if((Snipping == 0) && (CalcNlin != 0)){
   fprintf(infofl, "Following relaxation to calculate linear rheology\n");
   fprintf(infofl, "and saving segment relaxation times for nonlinear flow \n");
                                      }
if(CalcNlin == 0){
   fprintf(infofl, "Following relaxation to calculate nonlinear flow predictions\n");
                                      }

/* ******************** Snipping  ********************  */
#ifdef NBETA
if((Snipping == 0) || (CalcNlin==0)){
 SnipTime=SnipTime/unit_time;
fprintf(infofl, "SnipTime (Sim unit ) = %e \n",SnipTime); }
if(CalcNlin == 0){ 
FILE * fprio=fopen("savedprio.dat","r");    //reading in previous savedprio.dat
if(fprio == NULL){printf("Was expecting file savedprio.dat here \n"); 
printf("Please run with CalcNlin=no  first. \n"); abort(); }
for(int i=0; i<num_poly; i++){
int n1=branched_poly[i].first_end; int n2=arm_pool[n1].down;
  fscanf(fprio,"%d %lf %lf %lf", &arm_pool[n1].priority, &arm_pool[n1].str_time,
                    &arm_pool[n1].armtaus, &arm_pool[n1].armzeta);
   arm_pool[n1].priority-=1;
while(n2 != n1){
  fscanf(fprio,"%d %lf %lf %lf", &arm_pool[n2].priority, &arm_pool[n2].str_time,
                    &arm_pool[n2].armtaus, &arm_pool[n2].armzeta); 
  arm_pool[n2].priority-=1;
                n2=arm_pool[n2].down;}
                             }
 fclose(fprio);


if(FlowPriority == 0){
   for(int i=0; i<num_poly; i++){
      extern void calc_flow_priority(int); calc_flow_priority(i);
                                }
                 } 
fprio=fopen("savedprio.dat","w");   // re-writing the savedprio.dat file after altitude
for(int i=0; i<num_poly; i++){
int n1=branched_poly[i].first_end; int n2=arm_pool[n1].down;
fprintf(fprio,"%d %e %e %e\n",arm_pool[n1].priority+1, arm_pool[n1].str_time,
                    arm_pool[n1].armtaus, arm_pool[n1].armzeta);
while(n2 != n1){
fprintf(fprio,"%d %e %e %e\n",arm_pool[n2].priority+1, arm_pool[n2].str_time,
                    arm_pool[n2].armtaus, arm_pool[n2].armzeta);
n2=arm_pool[n2].down; } }
fclose(fprio);
                 }
br_copy=new polycopy[num_poly];
for(int i=0; i<num_poly; i++){
int nnp=1;
int n1=branched_poly[i].first_end; int n2=arm_pool[n1].down;
 while(n2 != n1){nnp++; n2=arm_pool[n2].down;}
 br_copy[i].narm=nnp;
 br_copy[i].active=0;
 br_copy[i].armindx= new int[nnp];
 br_copy[i].priority= new int[nnp];
 br_copy[i].assigned_trelax= new int[nnp];
 br_copy[i].trelax= new double[nnp];
 br_copy[i].zeta= new double[nnp];
 br_copy[i].relax_end = new int[nnp];
 br_copy[i].assigned_taus= new int[nnp];
 br_copy[i].taus= new double[nnp];

 nnp=0; br_copy[i].armindx[nnp]=n1; arm_pool[n1].copy_num=nnp;
        br_copy[i].priority[nnp]=1;
        br_copy[i].assigned_trelax[nnp]=-1; br_copy[i].trelax[nnp]=0.0;
        br_copy[i].relax_end[nnp]=-200;
        br_copy[i].assigned_taus[nnp]=-1;
        br_copy[i].taus[nnp]=0.0;
        br_copy[i].zeta[nnp]=0.0;
       // br_copy[i].relax_end[nnp]=n1;
 n2=arm_pool[n1].down;
 while(n2 != n1){nnp++; br_copy[i].armindx[nnp]=n2; arm_pool[n2].copy_num=nnp;
     br_copy[i].assigned_trelax[nnp]=-1; br_copy[i].trelax[nnp]=0.0;
        br_copy[i].relax_end[nnp]=-300;
        br_copy[i].assigned_taus[nnp]=-1;
        br_copy[i].taus[nnp]=0.0;
        br_copy[i].zeta[nnp]=0.0;
      //  br_copy[i].relax_end[nnp]=n2;
     br_copy[i].priority[nnp]=1; n2=arm_pool[n2].down;}
                             }

if(CalcNlin == 0){startup_nlin();}

#endif
/* ******************** Snipping  ********************  */
FILE * phifl=fopen("supertube.dat","w");
fprintf(phifl,"%e %e %e  %e \n",0.0,1.0,1.0,1.0);
int ndata=2; int num_alive=time_step(0);
fprintf(phifl,"%e %e %e  %e \n",cur_time,phi,phi_ST,phi_true);

if((CalcNlin != 0) && (Snipping == 0)){ 
                   extern void sample_alt_time(void); sample_alt_time();
                   extern void sample_alt_taus(void); sample_alt_taus();
                 }

   while(num_alive > 0) { 

#ifdef NBETA
if(CalcNlin == 0){
if(nlin_collect_data == -1){
  if(cur_time > nlin_t_min){init_var_nlin(); } }
else{if(cur_time > nlin_t_max){output_nlin();}}}
#endif
      num_alive=time_step(1); ndata++;

if((CalcNlin != 0) && (Snipping == 0)){ 
                   extern void sample_alt_time(void); sample_alt_time(); 
                   extern void sample_alt_taus(void); sample_alt_taus();
                                      }

      if(cur_time > 1e30){ warnmsgs(101);
for (int i=0; i< num_poly; i++){ if (branched_poly[i].alive) {polyout(i);} }
             num_alive=0;}
       if(phi_true < 0.0) { // numerical precision can give small negative phi
         phi_true=0.0;
         if((num_alive >0) && (phi_true < -1.0e-6 )){ warnmsgs(102);
for (int i=0; i< num_poly; i++){ if (branched_poly[i].alive) {polyout(i);} }
num_alive=0; } }
    if( (num_alive >0) && (phi_true > 0.0)) {
      fprintf(phifl,"%e %e %e %e  \n",cur_time,phi,phi_ST,phi_true); }
    else {
      num_alive=0;
      fprintf(phifl,"%e %e %e %e  \n",cur_time,0.0,0.0,0.0); }
    }
if( (CalcNlin != 0) && (Snipping == 0) ){
  extern void calcsnipprio(void); calcsnipprio(); }
fclose(phifl);
lin_rheology(ndata);
#ifdef NBETA
if((CalcNlin != 0) && (Snipping == 0)){extern void dumpsnipprio(void); dumpsnipprio();}
if(CalcNlin == 0){fclose(nlin_outfl); pompom();}
#endif
 }
}

end_code();
}
