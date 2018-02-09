#ifndef MULTIMETCSTR_H
#define MULTIMETCSTR_H

#include <stdbool.h>


extern void mulmetCSTRstart(double *kp, double *kdb, double *ks, double *kplcb, double *yconc, double tau, double mconc, int n, int ndist);
// extern void mulmetCSTRstart(double tau, double mconc, int n, int ndist);
extern bool mulmetCSTR(int n, int n1);     // returns false it we ran out of arm-storage

typedef struct
{
    int mulmetCSTRnumber;
    bool mulmetCSTRerrorflag;
} mulmetCSTR_global;

extern mulmetCSTR_global MMCSTR_global;

#endif