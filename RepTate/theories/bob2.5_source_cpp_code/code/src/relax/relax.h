// nonlinear routines visible outside
extern void nlin_retraction(int);
extern void sample_eff_arm_len(int);
extern void reptate_nlin(int);
extern void calc_nlin_phi_held(void);


//relax : extend_arm
extern void arm_len_end_extend(int ,int ,int ,int );
extern void collapse_star_arm(int, int);
extern void extend_arm(int,int);
extern void gobble_arm(int,int,int,int);
extern int inner_arm_compound(int);
extern void mk_ghost(int, int);
extern void del_ghost(int);
extern void prune_chain(int);
extern void semiconstrained_extend_arm(int ,int,int ,int);
extern void uncollapsed_extend(int , int );
int share_arm(int ,int,int ,int);

//relax : rept
extern void check_linearity(int);
extern bool try_reptate(int);
extern void rept_sv_mass(int);

//relax : retraction
extern void arm_retraction(int , int );
extern double quad_solve_spl(double, double, double);
extern double calc_eff_fric(int );

// vol_frac
extern void sv_mass(int, int);
