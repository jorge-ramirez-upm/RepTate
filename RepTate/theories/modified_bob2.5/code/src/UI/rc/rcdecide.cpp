/*
rcdecide.cpp : This file is part bob-rheology (bob) 
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
 
/* Decide what rc entry means */
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
void rcdecide(char * rccom, char * rcval)
{
extern int GenPolyOnly, OutMode, PrefMode, ReptScheme, CalcNlin, PrioMode;
extern int NumNlinStretch, DefinedMaxwellModes, CalcGPCLS, GPCNumBin, GPCPolyMult;

extern double Alpha, PSquare, TStart, DtMult, RetLim, FreqMax, FreqMin, FreqInterval;
extern double StretchBinWidth, NlinAvDt, MaxwellInterval, NlinAvInterval, cur_time;
extern FILE * infofl;
extern void warnmsgstring(int, char *);
extern int LateRouse, Snipping;
extern double LtRsFactor, SnipTime;
extern int FlowPriority;
extern int SlavePhiToPhiST;
extern double FlowTime;
extern int NlinPrep;

if(strlen(rcval) > 0){ int resolved_option=-1;

if(rccom[0]=='A'){resolved_option=1; 
            Alpha=atof(rcval); 
            fprintf(infofl,"Alpha = %e \n",Alpha);
                 }

if(rccom[0]=='C'){ resolved_option=1;
 if(rccom[4]=='G'){
   if( (rcval[0]=='Y') || (rcval[0]=='y')){CalcGPCLS=0;
// fprintf(infofl,"GPCLS : using flat molecular distribution for rheology\n"); 
fprintf(infofl,"Turning on GPC module\n");} }
 else{
  if( (rcval[0]=='Y') || (rcval[0]=='y')){CalcNlin=0;
   fprintf(infofl, "To calculate Nonlinear rheology \n"); }}
                 }

if(rccom[0]=='D'){resolved_option=1;
 if(rccom[1]=='e'){
 if( (rcval[0]=='Y') || (rcval[0]=='y')){DefinedMaxwellModes=0;
  fprintf(infofl,"Will use precalculated Maxwell modes\n"); }}
 else{ DtMult=atof(rcval); 
  fprintf(infofl,"DtMult = %e \n", DtMult); }
     }

if(rccom[0]=='F'){ resolved_option=1;
 if(rccom[4]=='M'){
  if(rccom[5]=='a'){FreqMax=atof(rcval);
    fprintf(infofl,"FreqMax = %e\n",FreqMax);}
  else{FreqMin=atof(rcval);
    fprintf(infofl,"FreqMin = %e\n",FreqMin);}
                  }
 else{ 
  if(rccom[4] == 'I'){
    FreqInterval=atof(rcval); 
    fprintf(infofl,"FreqInterval = %e\n",FreqInterval);}
  else{
if(rccom[4] == 'T'){
 FlowTime=atof(rcval); SnipTime=FlowTime;
                   }
else{
 if( (rcval[0]=='Y') || (rcval[0]=='y')){FlowPriority=0;
   fprintf(infofl,"Will use flow modified priority \n");}
    }
      }
   }
                 }

if(rccom[0]=='G'){resolved_option=1;
 if(rccom[1]=='e'){
 if( (rcval[0]=='Y') || (rcval[0]=='y')){GenPolyOnly=0;
   fprintf(infofl,"Will stop after generating polymers \n");}
                  }
 else{
  if(rccom[3]=='N'){GPCNumBin=atoi(rcval); 
         fprintf(infofl,"GPCNumBin = %d\n",GPCNumBin);}
  else{GPCPolyMult=atoi(rcval);
         fprintf(infofl,"GPCPolyMult = %d\n",GPCPolyMult);}
     } }

if(rccom[0]=='L'){resolved_option=1; 
if(rccom[2]=='t'){
if( (rcval[0]=='Y') || (rcval[0]=='y')){ LateRouse=0;
  fprintf(infofl,"Use independent Rouse relaxation at long times\n");}}
else{
LtRsFactor=atof(rcval);
LtRsFactor=3.980e-4 * LtRsFactor;
  fprintf(infofl,"Long time independent Rouse factor = %e\n", LtRsFactor);}}

if(rccom[0]=='M'){resolved_option=1; MaxwellInterval=atof(rcval);
  fprintf(infofl,"MaxwellInterval = %e \n",MaxwellInterval); }

if(rccom[0]=='N'){ resolved_option=1;
if(rccom[1]=='u'){
  NumNlinStretch=atoi(rcval);
  fprintf(infofl,"NumNlinStretch = %d \n",NumNlinStretch);
}
else{
if(rccom[4]=='A'){
 if(rccom[6]=='D'){NlinAvDt=atof(rcval);
    fprintf(infofl,"NlinAvDt = %e \n",NlinAvDt);}
 else{NlinAvInterval=atof(rcval);
    fprintf(infofl,"NlinAvInterval = %e \n",NlinAvInterval);}}
else{
  if( (rcval[0]=='y') || (rcval[0]=='Y')){NlinPrep=0; Snipping=0;} 
    }
                 }}

if(rccom[0]=='O'){resolved_option=1; OutMode=atoi(rcval);
    fprintf(infofl,"OutMode = %d \n",OutMode); }

if(rccom[0]=='P'){resolved_option=1;
if(rccom[1]=='S'){PSquare = atof(rcval);
    fprintf(infofl,"PSquare = %e \n", PSquare);}
else{
if(rccom[2]=='e'){PrefMode = atoi(rcval);
     fprintf(infofl,"PrefMode = %d \n",PrefMode);}
else{ if(rcval[0]=='e'){PrioMode=-1;
fprintf(infofl,"Priority is defined only for entangled segments \n");} }
    }
                 }

if(rccom[0]=='R'){resolved_option=1;
if(rccom[2]=='p'){ReptScheme=atoi(rcval);
fprintf(infofl,"ReptScheme = %d \n",ReptScheme);}
else{ RetLim = atof(rcval);
fprintf(infofl,"RetLim = %e \n",RetLim);
}}

if(rccom[0]=='S'){resolved_option=1; 
 if(rccom[1]=='t'){
StretchBinWidth=atof(rcval); 
fprintf(infofl,"StretchBinWidth = %e \n",StretchBinWidth); }
else{
 if(rccom[1]=='l'){
  if( (rcval[0]=='y') || (rcval[0]=='Y')){SlavePhiToPhiST=0;} 
                  }
 else{
  if(rccom[4]=='p'){ 
        if( (rcval[0]=='y') || (rcval[0]=='Y')){Snipping=0;} 
              fprintf(infofl,"Use snipping for priority \n"); }
  else{SnipTime=atof(rcval); fprintf(infofl,"Priority at time %e \n",SnipTime);}
     }
   }
}

if(rccom[0]=='T'){resolved_option=1; TStart=atof(rcval); cur_time=TStart;
fprintf(infofl,"TStart = %e \n",TStart);}


if(resolved_option==-1){warnmsgstring(101,rccom); }
                   }
else{ warnmsgstring(102,rccom); }
}

