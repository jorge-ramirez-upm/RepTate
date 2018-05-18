extern void get_poly_component(int, double);

// util
extern void polyread(void);
extern void polywrite(void);
extern void arm_start(int);
extern void attach_arm(int, int, int, int, int);
extern int fold_rd(int, int);
extern int fold_wrt(int, int);
extern void genProto(int, int);
extern polymer polygenProto(int, int *, int *, int *, int *, int *, double *, double *);
extern double poly_get_arm(int, double, double);
extern void polyout(int);
extern void poly_start(polymer *);
extern void print_arm_type(int, double, double);
extern void user_get_arm_type(int *, double *, double *);

// Tobita
extern void genTobita(int, int);
extern polymer polygenTobita(double, double, double, double, double);

// mpe
extern void genMPE(int, int);
extern polymer polygenMPE(double, double);
extern void genMPE_wtav(int, int);
extern polymer polygen_wtav(int, double, double);

// gel
extern void genGEL_wtav(int, int);
extern void genstargel(int, int);
extern polymer polygenstargel(double, int, double, double);

// model
extern void genLin(int, int);
extern polymer polygenLin(double);
extern void genStar(int, int);
extern void genStar_asym(int, int);
extern polymer polygenStar(int, double, double);
extern polymer polygenStar_asym(int, double, double, int, double, double);
extern void genH(int, int);
extern polymer polygenH(int, double, double, int, double, double);

extern void genComb(int, int);
extern polymer polygenComb(int, double, double, int, double, double, double);
extern void genComb_fxd(int, int);
extern polymer polygenComb_fxd(int, double, double, int, double, double, int);
extern void gencoupledComb(int, int);
extern polymer polygencoupledComb(int, double, double, int, double, double, double);

extern void genCayley(int, int);
extern polymer polygenCayley(int, int *, double *, double *);
extern void genCayley4(int, int);
extern polymer polygenCayley4(int, int *, double *, double *);
extern void genCayleyLIN(int, int);
extern polymer polygenCayleyLIN(int, int *, double *, double *);

// user
extern void genUDF(int, int);
extern polymer polygenUDF(int *, double *, double *);
extern void genfromfile(int, int *, double);
