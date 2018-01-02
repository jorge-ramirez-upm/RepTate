#ifndef TOBITABATCH_H
#define TOBITABATCH_H

extern void tobbatchstart(double pfin_conv, double ptau, double pbeta, double pCs, double pCb, int n);
extern bool tobbatch(int, int); // returns false it we ran out of arm-storage

extern void tobita_grow(int dir, int m, double cur_conv, bool sc_tag);
extern void calclength(double conv, double *r_out);
extern void scilength(double conv, double *r_out);
extern void brlength(double conv, double *r_out);
extern void getconv1(double cur_conv, double *new_conv_out);
extern void getconv2(double cur_conv, double *new_conv_out);

typedef struct
{
    int tobbatchnumber;
    bool tobitabatcherrorflag;
} tobitabatch_global;

extern tobitabatch_global tb_global;

#endif
