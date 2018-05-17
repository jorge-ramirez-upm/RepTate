/*
fast_real_hist.cpp : This file is part bob-rheology (bob) 
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
 
// fast modes from histograms in real time
#include <math.h>
#include <vector>

double fast_real_hist(double tt)
{
 extern double N_e;
 extern std::vector <double> phi_hist;
 extern int zintmin,zintmax;
 double tmpvar, gtmp1, gtmp2, goft_fast;
 goft_fast=0.0;
  for(int zi=zintmin; zi <= zintmax; zi++) {
    double phi_now=phi_hist[zi];
    if(phi_now >= 0.0) {
      double zz=(double)zi + 0.50; gtmp1=0.0; gtmp2=0.0;
       for (int i=1; i<zi; i++) {
          tmpvar=(double)i/zz; tmpvar=tmpvar*tmpvar;
          gtmp1+=exp(-tmpvar*tt); }
       int k=zi; int quit=0;
       double comp_term = exp(-2.0*pow(((double)k/zz),2) * tt);
       comp_term = 0.0010*comp_term;
       int max_term = (int)ceil(N_e*zz);
       while(quit==0) {
          tmpvar=(double)k/zz; tmpvar=exp(-2.0*tmpvar*tmpvar*tt);
          gtmp2+=tmpvar;
          if(tmpvar <= comp_term) quit=1;
          if(k >= max_term) quit=1; k++; }
      goft_fast+=phi_now * (gtmp1 + 5.0*gtmp2)/ (4.0*zz);
     }
   }
return goft_fast;
 
}
