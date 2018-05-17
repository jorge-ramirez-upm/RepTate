/*
genStar.cpp : This file is part bob-rheology (bob) 
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
#include <stdio.h>
void genStar(int ni, int nf)
{
 extern FILE* infofl; extern FILE * inpfl;
 extern double mass_mono;
 extern std::vector <polymer> branched_poly;
 extern int runmode;
 int arm_type, num_arm; double mass, pdi;
 if(runmode == 3){ fscanf(inpfl, "%d %lf %lf", &arm_type, &mass, &pdi);
//                    fscanf(inpfl, "%le %le", &mass, &pdi); 
                   fscanf(inpfl, "%d", &num_arm);}
 else{user_get_arm_type(&arm_type,&mass,&pdi); 
      printf(" How many arms the star has?  "); scanf("%d", &num_arm);}

 if((num_arm !=3) && (num_arm !=4) && (num_arm !=6) && (num_arm != 18)){
  fprintf(infofl, "Asked to generate %d armed star : unknown type\n", num_arm);
  fprintf(infofl, "Assuming 3 arm star... \n"); num_arm=3;
   }

 fprintf(infofl,"Selected %d arm Star ", num_arm);
 print_arm_type(arm_type, mass, pdi);

 mass=mass/mass_mono; if(arm_type != 0) {mass=mass/pdi;}
 double zeroarm=0.0;
 int armtypev[2]; armtypev[0]=0; armtypev[1]=arm_type;
 double massv[2]; massv[0]=0.0; massv[1]=mass;
 double pdiv[2]; pdiv[0]=0.0; pdiv[1]=pdi;
extern polymer polygenStar18(int , double , double );
 for (int i=ni; i<nf; i++)
  {
   switch(num_arm){
     case 3 : branched_poly[i]=polygenStar(arm_type,mass,pdi); break;
     case 4 : branched_poly[i]=polygenH(arm_type, mass, pdi, 0, zeroarm, pdi);
        break;
     case 6 : branched_poly[i]=polygenCayley(1,armtypev,massv,pdiv); break;
     case 18 : branched_poly[i]=polygenStar18(arm_type,mass,pdi); break;
                  }
  }
 fprintf(infofl,"created %d Star \n", nf-ni);
}

polymer polygenStar18(int arm_type, double mn_arm, double pdi)
{
extern std::vector <arm> arm_pool;
polymer cur_poly;
int nn[33];
for(int i=0; i<33; i++){nn[i]=request_arm(); arm_pool[nn[i]].arm_len=0.0;}
for(int i=15; i<33; i++){arm_pool[nn[i]].arm_len=poly_get_arm(arm_type, mn_arm, pdi);}
for(int i=1; i< 32; i++)
   {arm_pool[nn[i]].down=nn[i-1]; arm_pool[nn[i]].up=nn[i+1];}
arm_pool[nn[0]].down=nn[32]; arm_pool[nn[0]].up=nn[1];
arm_pool[nn[32]].down=nn[31]; arm_pool[nn[32]].up=nn[0];
cur_poly.first_end=nn[0];

attach_arm(nn[0], nn[3], nn[4], nn[1], nn[2]);
attach_arm(nn[1], nn[0], nn[2], nn[5], nn[6]);
attach_arm(nn[2], nn[0], nn[1], nn[7], nn[8]);
attach_arm(nn[3], nn[10], nn[9], nn[4], nn[0]);
attach_arm(nn[4], nn[11], nn[12], nn[3], nn[0]);
attach_arm(nn[5], nn[1], nn[6], nn[30], nn[13]);
attach_arm(nn[6], nn[1], nn[5], nn[15], nn[16]);
attach_arm(nn[7], nn[2], nn[8], nn[17], nn[18]);
attach_arm(nn[8], nn[2], nn[7], nn[20], nn[19]);
attach_arm(nn[9], nn[23], nn[14], nn[3], nn[10]);
attach_arm(nn[10], nn[25], nn[24], nn[3], nn[9]);
attach_arm(nn[11], nn[26], nn[27], nn[12], nn[4]);
attach_arm(nn[12], nn[28], nn[29], nn[11], nn[4]);
attach_arm(nn[13], nn[30], nn[5], nn[31], nn[32]);
attach_arm(nn[14], nn[22], nn[21], nn[9], nn[23]);
attach_arm(nn[15], nn[6], nn[16],-1, -1);
attach_arm(nn[16], nn[6], nn[15], -1, -1);
attach_arm(nn[17], nn[7], nn[18], -1, -1);
attach_arm(nn[18], nn[7], nn[17], -1, -1);
attach_arm(nn[19], nn[8], nn[20], -1, -1);
attach_arm(nn[20], nn[8], nn[19], -1, -1);
attach_arm(nn[21], -1,-1, nn[14], nn[22]);
attach_arm(nn[22], -1,-1, nn[14], nn[21]);
attach_arm(nn[23], -1,-1, nn[9], nn[14]);
attach_arm(nn[24], -1,-1, nn[25], nn[10]);
attach_arm(nn[25], -1,-1, nn[24], nn[10]);
attach_arm(nn[26], -1,-1, nn[27], nn[11]);
attach_arm(nn[27], -1,-1, nn[26], nn[11]);
attach_arm(nn[28], -1,-1, nn[12], nn[29]);
attach_arm(nn[29], -1,-1, nn[28], nn[12]);
attach_arm(nn[30], nn[5], nn[13], -1, -1);
attach_arm(nn[31], nn[13], nn[32], -1, -1);
attach_arm(nn[32], nn[31], nn[13], -1, -1);

poly_start(&cur_poly);
return(cur_poly);
}

