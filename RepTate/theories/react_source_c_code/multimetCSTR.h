#ifndef MULTIMETCSTR_H
#define MULTIMETCSTR_H

#include <stdbool.h>
#include "react_structs.h"

extern void mulmetCSTRstart(double *kp, double *kdb, double *ks, double *kplcb, double *yconc, double tau, double mconc, int n, int ndist, int numcat_max);
extern bool mulmetCSTR(int n, int n1);     // returns false it we ran out of arm-storage

extern mulmetCSTR_global MMCSTR_global;

#endif