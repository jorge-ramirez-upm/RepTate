/*
rcutil.cpp : This file is part bob-rheology (bob) 
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
 
/* look for equal sign in linedata[]. If exists, return 0 and
split left side of equal to rccom[] and right side to rcval[] */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int splitrcopt(char * linedata, char * rccom, char * rcval)
{
int len=strlen(linedata);
int err=-1; int eqpos=0;
for(int i=0; i<len; i++){if(linedata[i]=='='){err=0;eqpos=i;}}
if(err==0){
for(int i=0; i<eqpos; i++){rccom[i]=linedata[i];} rccom[eqpos]='\0';
for(int i=eqpos+1; i<len; i++){
 rcval[i-eqpos-1]=linedata[i];} rcval[len-eqpos-1]='\0'; }
return err;
}


/* if supplied with valid FILE fid, tries to read a line and fills
 line in linedata[]. return value -1 signals end of file or nonexistent fid*/
int getline(FILE * fid, char * linedata)
{
char aa[2]; int err=1; int k=0; linedata[0]='\0';
if(fid != NULL){
aa[0]='a';aa[1]='\0';
err=fscanf(fid, "%1c", &aa[0]);
if((aa[0] != '\n')){linedata[0]=aa[0]; k++;}
aa[0]='a';
while((aa[0] != '\n') && (err != -1)){
err=fscanf(fid, "%1c", &aa[0]);
if((aa[0] != '\n') && (err != -1)){linedata[k]=aa[0];k++;}
else{linedata[k]='\0';}
} }
else{ err=-1; }

return err;
}

/* remove white space (tab or space) from aa[] */
void removewhitespace(char * aa)
{
int len=strlen(aa);
char bb[80]; int k; k=0;
for(int i=0; i<len; i++){
if((aa[i] != ' ') && (aa[i] != '\t')){bb[k]=aa[i]; k++;}
                        }
for(int i=0; i<k; i++){aa[i]=bb[i];} aa[k]='\0';

}

