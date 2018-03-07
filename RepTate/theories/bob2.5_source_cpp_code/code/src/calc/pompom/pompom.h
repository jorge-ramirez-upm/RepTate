#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
extern void calc_pompom(int shearcode, int kmax, double gdot, double tmin, double tmax,
  double * xp, double * yp, double * stress, double * N1); 
extern void odeint(double ystart,double x1,double x2,double eps,double h1, double hmin, 
double tauS, double tauB, double gdot, int q, int kmax, 
double * xp, double * yp,
  void (*derivs) (double, double*, double*, double, double, double, int) );
extern void pm_shear(double x, double * y, double * dydx, 
   double tauS, double tauB, double gdot, int q);
extern void pm_uext(double x, double * y, double * dydx, 
   double tauS, double tauB, double gdot, int q);
extern void pompom(void) ;
extern void rkck(double y, double dydx, double x, double h, double* yout, double* yerr,
double tauS, double tauB, double gdot, int q,
void (*derivs) (double, double*, double *, double, double, double, int));
extern void rkqs(double * y, double dydx, double *  x, double  htry, double eps,
double yscal, double * hdid, double * hnext, double tauS, double tauB, double gdot, int q,
void (*derivs) (double, double *, double *, double, double, double, int) );
extern void inttochar(int, char* );
