#ifndef TOBITACSTR_H
#define TOBITACSTR_H

#include <stdbool.h>

void tobCSTRstart(double ttau,double  tbeta,double  tsigma, double  tlambda, int n);
bool tobCSTR(int n, int n1);     // returns false it we ran out of arm-storage

typedef struct
{
    int tobCSTRnumber;
    bool tobitaCSTRerrorflag;
} tobitaCSTR_global;

extern tobitaCSTR_global tCSTR_global;

#endif