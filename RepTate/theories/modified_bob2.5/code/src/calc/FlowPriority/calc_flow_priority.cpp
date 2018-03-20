/*
calc_flow_priority.cpp : This file is part bob-rheology (bob) 
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
 
// Calculate priority of polymer n
#include "../../../include/bob.h"
#include <stdlib.h>
#include <stdio.h>
void calc_flow_priority(int n) {

 extern arm * arm_pool; extern polymer * branched_poly;
 extern void set_flow_prio(int);
 int n1=branched_poly[n].first_end; set_flow_prio(n1); 
 int n2=arm_pool[n1].down;
 while(n2 != n1){set_flow_prio(n2); n2=arm_pool[n2].down;} 
// reset priority starting from zero
n1=branched_poly[n].first_end; arm_pool[n1].priority-=1;
n2=arm_pool[n1].down;
while(n2 != n1){arm_pool[n2].priority-=1; n2=arm_pool[n2].down;}
}


void set_flow_prio(int n1)
{
 extern arm * arm_pool; 
 extern void flow_travel(int, int, int *);
int mL, mR; mL=mR=0;

if (arm_pool[n1].R1 == -1){arm_pool[n1].R1=-5;}
int RR1=arm_pool[n1].R1; 
flow_travel(RR1,n1, &mL);
if (arm_pool[n1].R1 == -5){arm_pool[n1].R1=-1;}

if (arm_pool[n1].L1 == -1){arm_pool[n1].L1=-5;}
int LL1=arm_pool[n1].L1; 
flow_travel(LL1,n1, &mR);
if (arm_pool[n1].L1 == -5){arm_pool[n1].L1=-1;}

if(mL==0){mL=1;}
if(mR==0){mR=1;}

if(mL < mR){ arm_pool[n1].priority=mL;}
else{arm_pool[n1].priority=mR;} 

}

void flow_travel(int n0, int n1, int * m)
{
 extern arm * arm_pool;
 extern void flow_lencal(int, int, int *, double, double *);
int LL1=arm_pool[n1].L1; int LL2=arm_pool[n1].L2;
int RR1=arm_pool[n1].R1; int RR2=arm_pool[n1].R2;
extern double SnipTime;
if( (LL1 == n0) || (LL2 == n0) ){// travel right
  if((RR1 == -1) && (RR2 == -1)){m[0]+=1;}
  else {  // not a free end
      if( (RR1 != -1) && (RR2 != -1)){
if ((arm_pool[RR1].armtaus < SnipTime) &&
  (arm_pool[RR2].armtaus < SnipTime) ){ m[0]+=2;}
if ((arm_pool[RR1].armtaus < SnipTime) &&
  (arm_pool[RR2].armtaus >= SnipTime) ){ //need to decide on side arm contrib.
     if ( arm_pool[RR1].str_time >= SnipTime){m[0]+=1;}
     else{
      int Llab=0; // int Rlab=0;
      double Llength=0.0; // double Rlength=0.0;
      flow_lencal(RR1,n1, &Llab, arm_pool[RR1].str_time, &Llength);
 double teq=arm_pool[RR1].armzeta*Llength;
   if ( teq >= SnipTime ) {m[0]+=1;}
         }
   flow_travel(n1, RR2, m);
                                        }
if ((arm_pool[RR1].armtaus >= SnipTime) &&
  (arm_pool[RR2].armtaus < SnipTime) ){ //need to decide on side arm contrib.
     if ( arm_pool[RR2].str_time >= SnipTime){m[0]+=1;}
     else{
      int Llab=0; //int Rlab=0;
      double Llength=0.0; //double Rlength=0.0;
      flow_lencal(RR2,n1, &Llab, arm_pool[RR2].str_time, &Llength);
 double teq=arm_pool[RR2].armzeta*Llength;
   if ( teq >= SnipTime ) {m[0]+=1;}
         }
   flow_travel(n1, RR1, m);
                                       }
if ((arm_pool[RR1].armtaus >= SnipTime) &&
  (arm_pool[RR2].armtaus >= SnipTime) ){
   flow_travel(n1, RR1, m);
   flow_travel(n1, RR2, m);
                                        }
                                     }   // end case both arms exist
       if( (RR1 != -1) && (RR2 == -1)){  // only RR1 exists
          if (arm_pool[RR1].armtaus >= SnipTime){flow_travel(n1, RR1, m);}
          else{m[0]+=1;}
                                      }
       if( (RR1 == -1) && (RR2 != -1)){  // only RR2 exists
          if (arm_pool[RR2].armtaus >= SnipTime){flow_travel(n1, RR2, m);}
          else{m[0]+=1;}
                                      }
       }  // end not a free end
                                }  // end travel right
else{ // travel left
  if((LL1 == -1) && (LL2 == -1)){m[0]+=1;}
  else {  // not a free end
      if( (LL1 != -1) && (LL2 != -1)){
if ((arm_pool[LL1].armtaus < SnipTime) &&
  (arm_pool[LL2].armtaus < SnipTime) ){ m[0]+=2;}
if ((arm_pool[LL1].armtaus < SnipTime) &&
  (arm_pool[LL2].armtaus >= SnipTime) ){ //need to decide on side arm contrib.
     if ( arm_pool[LL1].str_time >= SnipTime){m[0]+=1;}
     else{
      int Llab=0; //int Rlab=0;
      double Llength=0.0; //double Rlength=0.0;
      flow_lencal(LL1,n1, &Llab, arm_pool[LL1].str_time, &Llength);
 double teq=arm_pool[LL1].armzeta*Llength;
   if ( teq >= SnipTime ) {m[0]+=1;}
        }
   flow_travel(n1, LL2, m);
                                        }
if ((arm_pool[LL1].armtaus >= SnipTime) &&
  (arm_pool[LL2].armtaus < SnipTime) ){ //need to decide on side arm contrib.
     if ( arm_pool[LL2].str_time >= SnipTime){m[0]+=1;}
     else{
      int Llab=0; // int Rlab=0;
      double Llength=0.0; // double Rlength=0.0;
      flow_lencal(LL2,n1, &Llab, arm_pool[LL2].str_time, &Llength);
 double teq=arm_pool[LL2].armzeta*Llength;
   if ( teq >= SnipTime ) {m[0]+=1;}
         }
   flow_travel(n1, LL1, m);
                                       }
if ((arm_pool[LL1].armtaus >= SnipTime) &&
  (arm_pool[LL2].armtaus >= SnipTime) ){
   flow_travel(n1, LL1, m);
   flow_travel(n1, LL2, m);
                                        }
                                     }   // end case both arms exist
       if( (LL1 != -1) && (LL2 == -1)){  // only LL1 exists
          if (arm_pool[LL1].armtaus >= SnipTime){flow_travel(n1, LL1, m);}
          else{m[0]+=1;}
                                      }
       if( (LL1 == -1) && (LL2 != -1)){  // only LL2 exists
          if (arm_pool[LL2].armtaus >= SnipTime){flow_travel(n1, LL2, m);}
          else{m[0]+=1;}
                                      }
       }  // end not a free end
    }  //end travel left
}




void flow_lencal(int n0, int n1, int * endlab, double Time, double * zlength)
{
extern arm * arm_pool;
int LL1=arm_pool[n1].L1; int LL2=arm_pool[n1].L2;
int RR1=arm_pool[n1].R1; int RR2=arm_pool[n1].R2;

zlength[0]+=arm_pool[n1].arm_len; // add on current arm length

if( (LL1 == n0) || (LL2 == n0) ){// travel right
   if( (RR1 >= 0) && (RR2 >= 0) ){  // both arms exist
      if ( (arm_pool[RR1].str_time >= Time) && 
        (arm_pool[RR2].str_time >= Time) ){endlab[0]=1;}   // neither arm relaxed
      if ( (arm_pool[RR1].str_time < Time) &&
        (arm_pool[RR2].str_time < Time) ){endlab[0]=0;}   // both arms relaxed
      if ( (arm_pool[RR1].str_time >= Time) &&
    (arm_pool[RR2].str_time < Time) ){flow_lencal(n1,RR1, endlab, Time, zlength);}  // one arm relaxed
      if ( (arm_pool[RR1].str_time < Time) &&
    (arm_pool[RR2].str_time >= Time) ){flow_lencal(n1,RR2, endlab, Time, zlength);}  // one arm relaxed
                                 }
   if( (RR1 < 0) && (RR2 < 0) ){endlab[0]=0;}  // neither arm exists
   if( (RR1 >= 0) && (RR2 < 0) ){  // only RR1 exists
        if (arm_pool[RR1].str_time >= Time){flow_lencal(n1,RR1, endlab, Time, zlength);}
        else{endlab[0]=0;}
                                } // end RR1 exists
   if( (RR1 < 0) && (RR2 >= 0) ){  // only RR2 exists
        if (arm_pool[RR2].str_time >= Time){flow_lencal(n1,RR2, endlab, Time, zlength);}
        else{endlab[0]=0;}
                                } // end RR2 exists
                                }//end travel right
else{ // travel left
   if( (LL1 >= 0) && (LL2 >= 0) ){  // both arms exist
      if ( (arm_pool[LL1].str_time >= Time) &&
        (arm_pool[LL2].str_time >= Time) ){endlab[0]=1;}   // neither arm relaxed
      if ( (arm_pool[LL1].str_time < Time) &&
        (arm_pool[LL2].str_time < Time) ){endlab[0]=0;}   // both arms relaxed
      if ( (arm_pool[LL1].str_time >= Time) &&
    (arm_pool[LL2].str_time < Time) ){flow_lencal(n1,LL1, endlab, Time, zlength);}  // one arm relaxed
      if ( (arm_pool[LL1].str_time < Time) &&
    (arm_pool[LL2].str_time >= Time) ){flow_lencal(n1,LL2, endlab, Time, zlength);}  // one arm relaxed
                                 }
   if( (LL1 < 0) && (LL2 < 0) ){endlab[0]=0;}  // neither arm exists
   if( (LL1 >= 0) && (LL2 < 0) ){  // only LL1 exists
        if (arm_pool[LL1].str_time >= Time){flow_lencal(n1,LL1, endlab, Time, zlength);}
        else{endlab[0]=0;}
                                } // end LL1 exists
   if( (LL1 < 0) && (LL2 >= 0) ){  // only LL2 exists
        if (arm_pool[LL2].str_time >= Time){flow_lencal(n1,LL2, endlab, Time, zlength);}
        else{endlab[0]=0;}
                                } // end LL2 exists
    } // end travel left
}
