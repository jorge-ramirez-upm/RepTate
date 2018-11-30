/*
genfromfile.cpp : This file is part bob-rheology (bob) 
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

/* User defined polymer : The skeletal code */

#include "../../../include/bob.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void genfromfile(int ni, int *nf, double blend_frac)
{
  extern FILE *infofl;
  extern FILE *inpfl;

  char polyfname[256];
  extern int getline(FILE *, char *);
  extern void get_name(char *, int);
  extern int runmode;
  int err;
  if (runmode == 2)
  {
    printf("\n Type in file name from which to read polymers \n");
    get_name(polyfname, 256);
  }
  else
  {
    extern bool reptate_flag;
    if (reptate_flag)
    {
      /* case 0: send filename containing polyconf input 
         case 1: send polycode for prototype (max 9 caracters) */
      int code = 0;
      get_string(polyfname, code);
    }
    else
    {
      err = getline(inpfl, polyfname);
      if (err == -1)
      {
        my_abort((char *)"Failed to get file name in genfromfile.cpp \n");
      }
    }
    
  }

  extern void removewhitespace(char *);
  removewhitespace(polyfname);
  FILE *tmpfl = fopen(polyfname, "r");
  if (tmpfl == NULL)
  {
    char s[256];
    sprintf(s, "Non existent file %-10.20s \n quitting now : genfromfile.cpp ... \n", polyfname);
    my_abort(s);
  }

  extern char polycode[10];
  int ncur_comp;
  extern std::vector<arm> arm_pool;
  extern std::vector<polymer> branched_poly;

  int segnum, LL1, LL2, RR1, RR2, nsv, n1;
  nsv = 0;
  double seglen, volfrac, N_e_dummy;
  char tmpcar[256];
  err = getline(tmpfl, tmpcar);
  int nnk = strlen(tmpcar);
  if (nnk < 9)
  {
    for (int k2 = 0; k2 < nnk; k2++)
    {
      polycode[k2] = tmpcar[k2];
    }
    polycode[nnk] = '\0';
  }
  else
  {
    for (int k2 = 0; k2 < 9; k2++)
    {
      polycode[k2] = tmpcar[k2];
    }
    polycode[9] = '\0';
  }
  //  fscanf(tmpfl,"%s",&polycode);
  fscanf(tmpfl, "%le", &N_e_dummy);
  fscanf(tmpfl, "%d", &ncur_comp);
  nf[0] = ni + ncur_comp;
  extern bool reptate_flag;
  if (!reptate_flag)
    fprintf(infofl, "Reading %d polymers form %-10.20s \n", ncur_comp, polyfname);
  for (int i = ni; i < nf[0]; i++)
  {
    fscanf(tmpfl, "%d", &segnum);
    for (int j = 0; j < segnum; j++)
    {
      fscanf(tmpfl, "%d %d %d %d %le %le", &LL1, &LL2, &RR1, &RR2, &seglen, &volfrac);
      volfrac = volfrac * blend_frac;
      int n = request_arm();
      if (j == 0)
      {
        nsv = n;
        branched_poly[i].first_end = n;
        arm_pool[n].up = n;
        arm_pool[n].down = n;
      }
      arm_pool[n].L1 = fold_rd(LL1, nsv);
      arm_pool[n].L2 = fold_rd(LL2, nsv);
      arm_pool[n].R1 = fold_rd(RR1, nsv);
      arm_pool[n].R2 = fold_rd(RR2, nsv);
      n1 = arm_pool[nsv].up;
      arm_pool[nsv].up = n;
      arm_pool[n].down = nsv;
      arm_pool[n].up = n1;
      arm_pool[n1].down = n;
      arm_pool[n].arm_len = seglen;
      arm_pool[n].vol_fraction = volfrac;
    }
    poly_start(&branched_poly[i]);
  }
  fclose(tmpfl);
}
