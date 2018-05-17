/*
get_sys_size.cpp : This file is part bob-rheology (bob) 
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

// First find out number of polymers and arms
#include <stdio.h>
#include <cstdlib>
#include "../../../include/bob.h"
void get_sys_size(void)
{
  extern int runmode;
  extern int max_poly, max_arm;

  if (runmode == 2)
  {
    printf("\n");
    printf("Maximum number of polymer you want to consider ? ... ");
    scanf("%d", &max_poly);
    printf("Maximum total number of arms (each linear requires two arms) ?");
    scanf("%d", &max_arm);
    printf("\n");
  }
  else
  {
    extern FILE *inpfl;
    fscanf(inpfl, "%d %d", &max_poly, &max_arm);
  }

  // Do a quick check that numbers are consistent
  if (max_arm < (2 * max_poly))
  {
    if (runmode == 2)
    {
      printf("You don't mean to represent %d polymers with just %d arms!\n", max_poly, max_arm);
      printf("You have one more chance to put in maximum number of arms. \n");
      printf("You should input atleast %d arms for linears and more for branched. \n", 2 * max_poly);
      printf("Maximum number of arms ? ... ");
      scanf("%d", &max_arm);
    }
    else
    {
      max_arm = 2 * max_poly;
    }
  }

  // during relaxation, we might need to add one more arm per molecule.
  max_arm += max_poly;

  extern polymer *branched_poly;
  branched_poly = new polymer[max_poly];
  if (branched_poly == NULL)
  {
    my_abort((char *)"Error : Could not allocate polymers. \n");
  }

  extern void pool_init(void);
  pool_init();
}
