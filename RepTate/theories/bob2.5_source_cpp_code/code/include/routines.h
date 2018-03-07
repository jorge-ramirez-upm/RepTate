#include "./routines/Util.h"
#include "./routines/polygen.h"

// UI
extern int rcread(void);
extern int parser(int argc, char *argv[]);
extern void user_interface(void);


// calc
extern void lin_rheology(int);
extern void pompom(void);
extern void poly_stat(void);
extern void startup_nlin(void);
extern void init_var_nlin(void);
extern void output_nlin(void);

// relaxation
extern int time_step(int);

extern void end_code(void);


