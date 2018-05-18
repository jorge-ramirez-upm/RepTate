/*
graceheadernlin.cpp : This file is part bob-rheology (bob) 
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
void graceheadernlin(FILE *fid)
{
  fprintf(fid, "# Grace project file \n");
  fprintf(fid, "# created by Bob2.4 \n");
  fprintf(fid, "@g0 on \n");
  fprintf(fid, "@g0 hidden false \n");
  fprintf(fid, "@g0 type XY \n");
  fprintf(fid, "@g0 stacked false \n");
  fprintf(fid, "@with g0 \n");
  fprintf(fid, "@     world 0.001, 1000, 0.001, 1000 \n");
  fprintf(fid, "@     stack world 0, 0, 0, 0 \n");
  fprintf(fid, "@     view 0.15, 0.1567, 0.887, 0.85 \n");
  fprintf(fid, "@     xaxes scale Logarithmic \n");
  fprintf(fid, "@     yaxes scale Logarithmic \n");
  fprintf(fid, "@     xaxis on \n");
  fprintf(fid, "@     xaxis label \"t (s) \" \n");
  fprintf(fid, "@     xaxis ticklabel format power \n");
  fprintf(fid, "@     xaxis ticklabel prec 0 \n");
  fprintf(fid, "@     xaxis tick minor ticks 0 \n");
  fprintf(fid, "@     yaxis on \n");
  fprintf(fid, "@     yaxis ticklabel format power \n");
  fprintf(fid, "@     yaxis ticklabel prec 0 \n");
  fprintf(fid, "@     yaxis tick minor ticks 0 \n");
  fprintf(fid, "@target G0.S0 \n");
  fprintf(fid, "@type xy \n");
}
