/*
polygencoupledComb.cpp : This file is part bob-rheology (bob) 
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
// coupled comb
polymer polygencoupledComb(int arm_typeb, double m_bbone, double pdi_bbone, 
   int arm_typea, double m_arm, double pdi_arm, double dnarm)
{
extern arm * arm_pool;
polymer cur_poly; 
double cur_bbone, cur_arm; extern MTRand mtrand1;
cur_bbone=poly_get_arm(arm_typeb, m_bbone, pdi_bbone);

double dnarm1 = poisson(dnarm) + 0.20; int n_arm=(int) floor(dnarm1);
if((dnarm1 - (double) n_arm) > 0.50) {n_arm++;}
n_arm++;   // we want one more attachment point.


int couplepoint=mtrand1.randInt(n_arm-1) + 1; // [1, n_arm]
int storearm=-1;
double * junc=new double [n_arm];
rand_on_line(cur_bbone, n_arm, junc);

int n0=request_arm(); cur_poly.first_end=n0;
arm_pool[n0].L1=arm_pool[n0].L2=-1; arm_pool[n0].arm_len=junc[0];

cur_arm=poly_get_arm(arm_typea, m_arm, pdi_arm);

int n1=request_arm();
arm_pool[n1].L1=arm_pool[n1].L2=-1; arm_pool[n1].arm_len=cur_arm;
arm_pool[n1].R1=n0; arm_pool[n0].R1=n1;
arm_pool[n0].down=n1; arm_pool[n1].up=n0; arm_pool[n1].down=n0;
arm_pool[n0].up=n1;
if(couplepoint == 1){storearm=n1;}
int n0p,n1p, n0pa, n1pa, nd;
for (int k=1; k<n_arm; k++)
{
n0p=request_arm();
arm_pool[n0p].L1=n0; arm_pool[n0p].L2=n1; arm_pool[n0].R2=n0p; arm_pool[n1].R2=n0p;
arm_pool[n0p].arm_len=junc[k] - junc[k-1];
cur_arm=poly_get_arm(arm_typea, m_arm, pdi_arm);
n1p=request_arm();
arm_pool[n1p].L1=arm_pool[n1p].L2=-1; 
arm_pool[n1p].R1=n0p; arm_pool[n0p].R1=n1p;
arm_pool[n1p].arm_len=cur_arm;
nd=arm_pool[n0].down;
if(couplepoint == (k+1)){storearm=n1p;}
arm_pool[n0].down=n0p; arm_pool[n0p].up=n0;
arm_pool[n0p].down=n1p; arm_pool[n1p].up=n0p;
arm_pool[n1p].down=nd; arm_pool[nd].up=n1p;
n0=n0p; n1=n1p;
}
n0p=request_arm();
arm_pool[n0p].L1=n0; arm_pool[n0p].L2=n1; 
arm_pool[n0].R2=n0p; arm_pool[n1].R2=n0p;
arm_pool[n0p].R1=arm_pool[n0p].R2=-1;
arm_pool[n0p].arm_len=cur_bbone - junc[n_arm - 1];
nd=arm_pool[n0].down;
arm_pool[n0].down=n0p; arm_pool[n0p].up=n0;
arm_pool[n0p].down=nd; arm_pool[nd].up=n0p;
delete [] junc;

dnarm1 = poisson(dnarm) + 0.20; 
int n_arm1=(int) floor(dnarm1); if((dnarm1 - (double) n_arm1) > 0.50) {n_arm1++;}
n_arm1 ++;
junc=new double [n_arm1];

cur_bbone=poly_get_arm(arm_typeb, m_bbone, pdi_bbone);
rand_on_line(cur_bbone, n_arm1, junc);
couplepoint=mtrand1.randInt(n_arm1-1) ; // [0, n_arm1-1]
if(storearm != -1){
arm_pool[storearm].arm_len=0.001;
n0p=request_arm(); n1p=request_arm();
arm_pool[storearm].L1=n0p; arm_pool[storearm].L2=n1p;
arm_pool[n0p].R1=storearm; arm_pool[n0p].R2=n1p; arm_pool[n0p].L1=arm_pool[n0p].L2=-1;
arm_pool[n1p].L1=storearm; arm_pool[n1p].L2=n0p; arm_pool[n1p].R1=arm_pool[n1p].R2=-1;

if(couplepoint == 0){ arm_pool[n0p].arm_len=junc[0];}
else{ arm_pool[n0p].arm_len=junc[couplepoint]-junc[couplepoint -1];}
if(couplepoint != (n_arm1-1) ){arm_pool[n1p].arm_len=junc[couplepoint+1]-junc[couplepoint];}
else{arm_pool[n1p].arm_len=cur_bbone - junc[n_arm1-1]; }
nd=arm_pool[storearm].down;
arm_pool[storearm].down=n0p; arm_pool[n0p].up=storearm;
arm_pool[n0p].down=n1p; arm_pool[n1p].up=n0p; arm_pool[n1p].down=nd; arm_pool[nd].up=n1p;

if(couplepoint != 0){
n0=n0p; 
cur_arm=poly_get_arm(arm_typea, m_arm, pdi_arm);
n1=request_arm(); arm_pool[n1].arm_len=cur_arm; arm_pool[n1].L1=arm_pool[n1].L2=-1;
arm_pool[n1].R1=n0; arm_pool[n0].L1=n1;
nd=arm_pool[n0].down;
arm_pool[n0].down=n1; arm_pool[n1].up=n0;
arm_pool[n1].down=nd; arm_pool[nd].up=n1; 

for(int k=couplepoint-1; k> 0; k--)
{
n0pa=request_arm();
arm_pool[n0pa].R1=n0; arm_pool[n0pa].R2=n1; arm_pool[n0].L2=n0pa; arm_pool[n1].R2=n0pa;
arm_pool[n0pa].arm_len=junc[k] - junc[k-1];
cur_arm=poly_get_arm(arm_typea, m_arm, pdi_arm);
n1pa=request_arm();
arm_pool[n1pa].L1=arm_pool[n1pa].L2=-1; 
arm_pool[n1pa].R1=n0pa; arm_pool[n0pa].L1=n1pa;
arm_pool[n1pa].arm_len=cur_arm;
nd=arm_pool[n0].down;
arm_pool[n0].down=n0pa; arm_pool[n0pa].up=n0;
arm_pool[n0pa].down=n1pa; arm_pool[n1pa].up=n0pa;
arm_pool[n1pa].down=nd; arm_pool[nd].up=n1pa;
n0=n0pa; n1=n1pa;
}
n0pa=request_arm(); arm_pool[n0pa].arm_len=junc[0];
arm_pool[n0pa].L1=arm_pool[n0pa].L1=-1;
arm_pool[n0pa].R1=n0; arm_pool[n0pa].R2=n1;
arm_pool[n0].L2=n0pa; arm_pool[n1].R2=n0pa;
nd=arm_pool[n0].down;
arm_pool[n0].down=n0pa; arm_pool[n0pa].up=n0;
arm_pool[n0pa].down=nd; arm_pool[nd].up=n0pa;
}

if(couplepoint != (n_arm-1)){
n0=n1p; 
cur_arm=poly_get_arm(arm_typea, m_arm, pdi_arm);
n1=request_arm(); arm_pool[n1].arm_len=cur_arm; arm_pool[n1].L1=arm_pool[n1].L2=-1;
arm_pool[n1].R1=n0; arm_pool[n0].R1=n1;
nd=arm_pool[n0].down;
arm_pool[n0].down=n1; arm_pool[n1].up=n0;
arm_pool[n1].down=nd; arm_pool[nd].up=n1; 
for(int k=couplepoint +1; k<n_arm1; k++)
{
n0p=request_arm();
arm_pool[n0p].L1=n0; arm_pool[n0p].L2=n1; arm_pool[n0].R2=n0p; arm_pool[n1].R2=n0p;
arm_pool[n0p].arm_len=junc[k] - junc[k-1];
cur_arm=poly_get_arm(arm_typea, m_arm, pdi_arm);
n1p=request_arm();
arm_pool[n1p].L1=arm_pool[n1p].L2=-1; 
arm_pool[n1p].R1=n0p; arm_pool[n0p].R1=n1p;
arm_pool[n1p].arm_len=cur_arm;
nd=arm_pool[n0].down;
arm_pool[n0].down=n0p; arm_pool[n0p].up=n0;
arm_pool[n0p].down=n1p; arm_pool[n1p].up=n0p;
arm_pool[n1p].down=nd; arm_pool[nd].up=n1p;
n0=n0p; n1=n1p;
}
n0p=request_arm();
arm_pool[n0p].L1=n0; arm_pool[n0p].L2=n1; 
arm_pool[n0].R2=n0p; arm_pool[n1].R2=n0p;
arm_pool[n0p].R1=arm_pool[n0p].R2=-1;
arm_pool[n0p].arm_len=cur_bbone - junc[n_arm1 - 1];
int nd=arm_pool[n0].down;
arm_pool[n0].down=n0p; arm_pool[n0p].up=n0;
arm_pool[n0p].down=nd; arm_pool[nd].up=n0p;

}

}  
delete [] junc;


poly_start(&cur_poly);
return(cur_poly);
}
