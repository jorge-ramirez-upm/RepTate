/*
get_name.cpp : This file is part bob-rheology (bob) 
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
 
// delete empty space or newline at the begining. 
// read characters till the next newline. Replace newline by null
#include <ctype.h>
#include <stdio.h>
#include <string.h>
void get_name(char *word, int n)
{
int k=0; int c='\n';
while(isspace(c = fgetc(stdin)) || (c=='\n'));
*word++=c; 
      while(c !='\n')
       {
        c=fgetc(stdin);
        if(c != '\n') *word++ = c;
        k++; if(k >= n) {printf("Too many characters to read!\n"); c='\n';}
       }
        *word='\0';
}
