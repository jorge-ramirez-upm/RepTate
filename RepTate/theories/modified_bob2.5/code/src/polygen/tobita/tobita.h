extern double calclength(double, double, double, double, double);
extern double scilength(double, double, double);
extern double brlength(double, double, double);
extern double getconv1(double);
extern double getconv2(double, double);

extern void tobita_grow(int dir, int m, double cur_conv, bool sc_tag, 
int * rlevel, double cs, double cb, double fin_conv,
 double tau, double beta, int* bcount);

extern void tobita_clean(polymer *);
extern void tobita_arm_clean(int, int *, int *);
extern void tobita_swap_arm(int, int);
