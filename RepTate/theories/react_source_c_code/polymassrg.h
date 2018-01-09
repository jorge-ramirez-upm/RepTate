#ifndef POLYMASSRG_H
#define POLYMASSRG_H

void mass_segs(int first, double *lentot_out, int *segtot_out);
void mass_rg1(int m, double cur_c, double *lentot_out, double *htot_out, double *jtot_out);
void mass_rg2(int m, double cur_c, double *lentot_out, double *jtot_out, double *gfact_out);

#endif
