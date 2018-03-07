/*
warnmsgs.cpp : This file is part bob-rheology (bob) 
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
 
/* Throw warning messages. */
#include<stdio.h>
#include<string.h>
#include<stdlib.h>

void warnmsgs(int code)
{
extern int runmode;
if(runmode == 2){
switch(code){
case 401 : printf("Warning : stepsize smaller than minimum in odeint \n"); break;
case 402 : printf("Warning : Too many steps in odeint \n"); break;
case 403 : printf("Warning : stepsize underflow in rkqs \n"); break;
case 404 : printf("Warning : negative frequency in fast_four_hist \n"); break;
default : printf("unknown code %d in warnmsgs!\n",code); break;
            }
                }
else{
extern FILE * errfl;
if(errfl == NULL){errfl=fopen("bob.err","w"); }
switch(code){
case 401 : fprintf(errfl,"Warning : stepsize smaller than minimum in odeint \n"); break;
case 402 : fprintf(errfl,"Warning : Too many steps  in odeint \n"); break;
case 403 : fprintf(errfl, "Warning : stepsize underflow in rkqs \n"); break;
case 404 : fprintf(errfl, "Warning : negative frequency in fast_four_hist \n"); break;
default : fprintf(errfl,"unknown code %d in warnmsgs!\n",code); break;
            }
    }

}

void warnmsgstring(int code, char * wmsg)
{
extern int runmode;
if(runmode == 2){
switch(code){
case 101 : printf("Warning 101: rc option %s is not defined.\n",wmsg); break;
case 102 : printf("Warning 102: Empty value for rc option %s .\n",wmsg); break;
default : printf("unknown code %d in warnmsgstring!\n",code); break;
            }
                }
else{
extern FILE * errfl;
if(errfl == NULL){errfl=fopen("bob.err","w"); }
switch(code){
case 101 : fprintf(errfl,"Warning 101: rc option %s is not defined.\n",wmsg); break;
case 102 : fprintf(errfl,"Warning 102: Empty value for rc option %s .\n",wmsg); break;
default : fprintf(errfl,"unknown code %d in warnmsgstring!\n",code); break;
    }
}
}
