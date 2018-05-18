/*
reptateheadergtp.cpp : This file is part bob-rheology (bob) 
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
void reptateheadergtp(FILE *fid)
{
  extern double temp;
  fprintf(fid, "T = %e; origin=Bob;\n", temp - 273.0);
  fprintf(fid, "w        G'     G'' \n");
  fprintf(fid, "rad/s    Pa     Pa  \n");
}
