/*
get_poly.cpp : This file is part bob-rheology (bob) 
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
#include "../../../include/bob.h"

void get_poly(void)
{
  extern int runmode, num_poly;
  extern FILE *conffl;
  extern char conffname[256];
  extern void get_poly_component(int, double);
  extern void polyread(void);
  extern void polywrite(void);
  int num_comp;
  int shouldread = 1;
  double blend_frac;
  if (runmode == 2)
  {
    printf("Do you want to generate the polymers or read from file ?\n");
    printf("Type in 1 for generating or 0 for reading from file ... ");
    scanf("%d", &shouldread);
    if (shouldread == 0)
    {
      printf("\n Type in the filename of the polymer configuration \n");
      extern void get_name(char *, int);
      get_name(conffname, 256);
      conffl = fopen(conffname, "r");
      if (conffl == NULL)
      {
        char s[256];
        sprintf(s, "Error opening configuration file %s \n", conffname);
        my_abort(s);
      }
      polyread();
    }
    else
    {
      conffl = fopen(conffname, "w");
      if (conffl == NULL)
      {
        my_abort((char *)"Error opening file to write configuration \n");
      }
      printf("How many components you want ? ");
      scanf("%d", &num_comp);
      num_poly = 0;
      if (num_comp < 1)
      {
        printf("At least one component is needed!\n");
        num_comp = 1;
      }

      if (num_comp == 1)
      {
        blend_frac = 1.0;
        get_poly_component(0, blend_frac);
      }
      else
      {
        for (int j1 = 0; j1 < num_comp; j1++)
        {
          printf("Weight fraction occupied by component %d ? ...", j1 + 1);
          scanf("%le", &blend_frac);
          get_poly_component(j1, blend_frac);
        }
      }
    }

  } // end interactive mode
  else
  {
    extern FILE *inpfl;
    // fscanf(inpfl, "%d", &num_comp);
    num_comp = (int) get_next_inp();
    if (num_comp == 0)
    {
      shouldread = 0;
      conffl = fopen(conffname, "r");
      if (conffl == NULL)
      {
        char s[256];
        sprintf(s, "Error opening configuration file %s \n", conffname);
        my_abort(s);
      }
      polyread();
    }
    else
    {
      conffl = fopen(conffname, "w");
      if (conffl == NULL)
      {
        char s[256];
        sprintf(s, "Error opening configuration file %s \n", conffname);
        my_abort(s);
      }

      num_poly = 0;
      for (int j1 = 0; j1 < num_comp; j1++)
      {
        // fscanf(inpfl, "%le", &blend_frac);
        blend_frac = get_next_inp();

        get_poly_component(j1, blend_frac);
      }
    }
  }
  if (shouldread != 0)
  {
    polywrite();
  }
  extern int CalcGPCLS, LateRouse;
  extern void gpcls(int, int, int, int);
  if (CalcGPCLS == 0)
  {
    if ((num_comp > 1) || (shouldread == 0))
    {
      gpcls(-1, 0, num_poly, 0);
    }
  }
  else
  {
    if (LateRouse == 0)
    { // we need to set up gfactor. So, call GPC module
      gpcls(-1, 0, num_poly, 0);
    }
  }

  fclose(conffl);
}
