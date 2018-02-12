#ifndef BINSANDBOB_H
#define BINSANDBOB_H

#include <stdbool.h>
#include "react_structs.h"

extern void molbin(int);
extern void multimolbin(int reqbins, double *weights, int *dist, int ndists);
extern void bobinit(int n);
extern void bobcount(int m, int n);
extern void polyconfwrite(int, char *fname);
unsigned long long multipolyconfwrite(char *fname, double *weights, int *dists, int n_inmix);
// extern void multipolyconfwrite(char *fname, double *weights, bool *inmix, int *numsaved_out);
extern double return_binsandbob_multi_avbr(int i);
extern double return_binsandbob_multi_avg(int i);
extern double return_binsandbob_multi_lgmid(int i);
extern double return_binsandbob_multi_wmass(int i);
extern double return_binsandbob_multi_wt(int i);
extern void set_react_dist_monmass(int i, double monmass);
extern void set_react_dist_M_e(int i, double M_e);

extern binsandbob_global bab_global;

#endif
