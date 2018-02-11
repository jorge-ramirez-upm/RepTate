#ifndef TOBITABATCH_H
#define TOBITABATCH_H

#include <stdbool.h>
#include "react_structs.h"

extern void tobbatchstart(double pfin_conv, double ptau, double pbeta, double pCs, double pCb, int n);
extern bool tobbatch(int, int); // returns false it we ran out of arm-storage

extern tobitabatch_global tb_global;

#endif
