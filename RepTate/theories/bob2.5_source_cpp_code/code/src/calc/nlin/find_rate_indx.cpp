/*
find_rate_indx.cpp : This file is part bob-rheology (bob) 
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
 
#include <math.h>
int find_rate_indx(double t_stretch)
{
extern double cur_time, StretchBinWidth;
extern int NumNlinStretch;
int rate_indx;
double t_ratio;
if(t_stretch >= cur_time){rate_indx=0;}
else{
t_ratio=cur_time/t_stretch;
rate_indx=(int) floor(log(t_ratio)/log(StretchBinWidth));
if(rate_indx >= NumNlinStretch){rate_indx=NumNlinStretch-1;}
}

return rate_indx;
}

