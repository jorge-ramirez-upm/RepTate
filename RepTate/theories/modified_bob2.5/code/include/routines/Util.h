// armpool
extern int request_arm(void);
extern void return_arm(int);
extern int request_attached_arm(int);
extern void remove_arm_from_list(int);
extern void set_tmpflag(int);
extern void unset_tmpflag(int);
extern void set_tmpflag_left(int, int);
extern void set_tmpflag_right(int, int);
extern void set_tmpflag_travel(int);

// help
extern void errmsg(int);
extern void warnmsgs(int);
extern void warnmsgstring(int, char *);

// random
extern double gasdev(void);
extern double armlen_gaussian(double, double);
extern double armlen_lognormal(double, double);
extern double armlen_semiliving(double, double);
extern double flory_distb(double);
extern double gammln(double);
extern double poisson(double);
extern void rand_on_line(double, int, double *);

// vol_frac
extern double frac_unrelaxed(void);
extern double free_arm_relax_amount(int);
extern void set_vol_frac(int, int, int, double);
extern void set_vol_frac_wtav(int, int, int, double);
extern void sv_mass(int, int);
