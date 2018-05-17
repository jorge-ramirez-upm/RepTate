#ifndef BOB_H
#define BOB_H

// header file for bob
#define pi 3.14159265358979323844
#define pi_pow_2 9.86960440108935861869
#define pi_pow_5 306.01968478528145324219

const char * const bob_version="bob-2.5";
const char * const bob_date="18 Nov 2011";
double const tiny=1.0e-16;

extern bool reptate_flag;
void my_abort(char *s);

#include "./class_def.h"
#include "./routines.h"


#endif