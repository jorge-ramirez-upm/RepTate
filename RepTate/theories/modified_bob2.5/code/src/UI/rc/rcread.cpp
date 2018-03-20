/*
rcread.cpp : This file is part bob-rheology (bob) 
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

/* Look for bob.rc. If exists read and try to decide if the lines are options 
 Continue gracefully if something is not understood. (throwing up warning) */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int rcread(void)
{
  int err;
  err = 1;
  char linedata[256], rccom[80], rcval[80];
  extern int getline(FILE *, char *);
  extern int splitrcopt(char *, char *, char *);
  extern void removewhitespace(char *);
  extern void rcdecide(char *, char *);
  extern void rcdefault(void);
  rcdefault();

  FILE *flrc = fopen("bob.rc", "r");
  extern FILE *infofl;
  if (flrc != NULL)
  {
    fprintf(infofl, "Found bob.rc \n");
    while (err != -1)
    {
      err = getline(flrc, linedata);
      if (err != -1)
      {
        err = splitrcopt(linedata, rccom, rcval);
        if (err != -1)
        {
          removewhitespace(rccom);
          removewhitespace(rcval);
          rcdecide(rccom, rcval);
        }
        err = 1;
      }
    }
    fclose(flrc);
    err = 0;
    fprintf(infofl, "End of rc file \n\n");
  }
  else
  {
    err = -1;
  }

  return err;
}
