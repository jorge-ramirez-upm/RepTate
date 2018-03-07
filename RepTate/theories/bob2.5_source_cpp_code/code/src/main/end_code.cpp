/*
end_code.cpp : This file is part of bob-rheology (bob) 
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
 
// deallocate memory; close open files;

#include <stdio.h>
#include <stdlib.h>
#include "../../include/bob.h"

void end_code(void)
{
extern FILE * infofl; extern FILE * errfl; extern FILE * debugfl;
if(infofl != NULL){fclose(infofl);}
if(errfl != NULL){fclose(errfl);}
if(debugfl != NULL){fclose(debugfl);}
extern arm * arm_pool;
extern polymer * branched_poly;
delete [] arm_pool; delete [] branched_poly;


}
