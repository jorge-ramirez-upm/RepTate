#ifndef BOB_H
#define BOB_H

// header file for bob
#define pi 3.14159265358979323844
#define pi_pow_2 9.86960440108935861869
#define pi_pow_5 306.01968478528145324219

const char *const bob_version = "bob-2.5";
const char *const bob_date = "18 Nov 2011";
double const tiny = 1.0e-16;

void my_abort(char *s);

// flag to stop BoB calculations
extern bool flag_stop_bob;
extern "C" void set_flag_stop_bob(bool b);
// get virtual input file form python
typedef double pyget_double();
extern pyget_double *get_next_inp;
extern pyget_double *get_next_proto;
typedef void pyget_string(char *s, int i);
extern pyget_string *get_string;

#include "./class_def.h"
#include "./routines.h"
#include <vector>

#endif