#ifndef BINSANDBOB_H
#define BINSANDBOB_H

extern void molbin(int);
extern void multimolbin(int reqbins, double *weights, bool *inmix);
extern void bobinit(int n);
extern void bobcount(int m, int n);
extern void polyconfwrite(int, char *fname);
extern void multipolyconfwrite(char *fname, double *weights, bool *inmix, int *numsaved_out);

extern double *multi_wt, *multi_avbr, *multi_wmass, *multi_avg, *multi_lgmid;
extern double multi_m_w, multi_m_n, multi_brav;
extern int multi_nummwdbins;

#endif