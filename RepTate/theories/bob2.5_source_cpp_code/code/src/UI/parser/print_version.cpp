/*
print_version.cpp : This file is part bob-rheology (bob) 
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
#include "../../../include/bob.h"
void print_version(void)
{
printf("bob : Rheology of general Branch-On-Branch polymer\n");
printf("%s : dated %s\n", bob_version, bob_date);
printf("Known issues : \n");
printf("        :  In some places Alpha is hardcoded to 1.0 \n");
printf("        :  If a component occupies very small weight fraction \n");
printf("             and relaxes much slowly than rest of the material, \n");
printf("    the prediction may be wrong if they become non-self-entangled.\n"); 
printf("bug report : d.j.read@leeds.ac.uk \n");
}
