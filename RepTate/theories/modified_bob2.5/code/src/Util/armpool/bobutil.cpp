/*
bobutil.cpp : This file is part bob-rheology (bob) 
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
#include <stdlib.h>
#include <string.h>
#include <math.h>

double **assign_ar_2d_double(int m, int n)
{
  double **ar = new double *[m];
  if (ar != NULL)
  {
    for (int i = 0; i < m; i++)
    {
      ar[i] = new double[n];
    }
  }
  else
  {
    printf("Failed to allocate 2d array \n");
  }
  return ar;
}

void delete_ar_2d_double(double **ar, int m)
{
  for (int i = 0; i < m; i++)
  {
    delete[] ar[i];
  }
  delete[] ar;
}

void inttochar(int np, char *xx)
{
  char zz[10];
  zz[0] = '\0';
  int i = 0;
  int ones = 0;
  int k = 0;
  int j = 0;
  while (np != 0)
  {
    ones = np % 10;
    zz[i] = (char)(ones + 48);
    np = np / 10;
    i++;
  }
  for (j = i - 1; j >= 0; j--)
  {
    xx[k] = zz[j];
    k++;
  }
  xx[i] = '\0';
}

int stringtoint(char *xx)
{
  int nn = 0;
  int bs;
  int len = strlen(xx);
  if (len == 0)
  {
    nn = 0;
  }
  else
  {
    for (int i = 0; i < len; i++)
    {
      bs = 1;
      for (int j = 0; j < (len - 1 - i); j++)
      {
        bs = bs * 10;
      }
      extern int chartoint(char yy);
      nn += bs * chartoint(xx[i]);
    }
  }
  return nn;
}

int chartoint(char xx)
{
  int nn = 0;
  switch (xx)
  {
  case '0':
    nn = 0;
    break;
  case '1':
    nn = 1;
    break;
  case '2':
    nn = 2;
    break;
  case '3':
    nn = 3;
    break;
  case '4':
    nn = 4;
    break;
  case '5':
    nn = 5;
    break;
  case '6':
    nn = 6;
    break;
  case '7':
    nn = 7;
    break;
  case '8':
    nn = 8;
    break;
  case '9':
    nn = 9;
    break;
  default:
    printf("char corresponding to non integer in chartoint \n");
    break;
  }
  return nn;
}
