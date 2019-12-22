#include <stdio.h>
#include <math.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_roots.h>
#include <gsl/gsl_complex.h>
#include <gsl/gsl_complex_math.h>


//#define Power  gsl_pow_uint // CAUTION - only works for integer powers
#define Power  gsl_pow_int // CAUTION - only works for integer powers
//#define Power  pow
#define Log  log
#define Sqrt sqrt
//#define ArcTanh atanh
//#define double float

struct function_params
{
  double Nt, mu;
};


//double Log( double x);
//double Sqrt( double x);


double solve (double Ns, void *params);
double solve_deriv (double Ns,   void *params);
void solve_fdf (double x, void *params, double *y, double *dy);
double real_ans( double x);
double rootExpansion( double Nt, double mu);
double brent(  void *params );
double newton(  void *params ) ;
double A (double Ns,   void *params);

double landscape( double Nt, double mu, double epsilon);



double landscape( double Nt, double mu, double epsilon)
{
  double root=0.0;
  struct function_params params ;
  double a, b, c;

  //load params
  params.Nt= Nt;
  params.mu = mu;



  //find turning point
  if ( params.mu  <  1.13001){
    root = newton( &params);
  }else{
    root = brent( &params);
  }

  
  //root=66.70713310;
  //printf("Root=%f\n", root );

  //==find guassian params a,b,c;
  
  a = A (root, &params);
  b = solve ( root, &params);
  c= -0.5 * solve_deriv ( root, &params);
  //printf("a,b,c = %.9f %.9f %.9f\n",a,b,c);
  

  return -(log(Nt-1) * (Nt-0.5) - 0.5*log(-2.0 * c) -a -b*b/4.0/c)
  -epsilon*(Nt-1) 
      - mu *( 4.9025961683277826370) ;


//-(log(Nt-1) * (Nt-0.5) - 0.5*log(-2.0 * c) -a -b*b/4.0/c) - epsilon*(Nt-1) 
    //- mu *( -4.9025961683277826370) ; // 4.902... = (2 + (9*Pi*ArcTan(Sqrt(-1 + (9*Pi)/16.)))/(8.*Sqrt(-1 + (9*Pi)/16.))

}

double brent(  void *params ) 
{
  int status;
  int iter = 0, max_iter = 100;
  const gsl_root_fsolver_type *T;
  gsl_root_fsolver *s;
  double r = 0;
  double x_lo = 3.0, x_hi = 5.0;
  gsl_function F;
  struct function_params *p 
    = (struct function_params *) params;
  
  
  F.function = &solve;
  F.params = p;
     
  x_hi= p->Nt / 2.0 * (1.2) ;


  //printf("%f %f\n",x_lo, x_hi);

  T = gsl_root_fsolver_brent;
  s = gsl_root_fsolver_alloc (T);
  gsl_root_fsolver_set (s, &F, x_lo, x_hi);
     
  //printf ("using %s method\n", 	  gsl_root_fsolver_name (s));
  
  //printf ("%5s [%9s, %9s] %9s %10s %9s\n",	  "iter", "lower", "upper", "root", 	  "err", "err(est)");
  
  do
    {
      iter++;
      status = gsl_root_fsolver_iterate (s);
      r = gsl_root_fsolver_root (s);
      x_lo = gsl_root_fsolver_x_lower (s);
      x_hi = gsl_root_fsolver_x_upper (s);
      status = gsl_root_test_interval (x_lo, x_hi,
				       0, 0.001);
      
      /*
      if (status == GSL_SUCCESS)
	//printf ("Converged:\n");
	*/
      
	//printf ("%5d [%.7f, %.7f] %.7f %+.7f %.7f\n",	      iter, x_lo, x_hi,	      r, r - r_expected, 	      x_hi - x_lo);
    }
      
       while (status == GSL_CONTINUE && iter < max_iter);
  
  gsl_root_fsolver_free (s);
  
  return r;
}


double newton(  void *params ) 
{
  int status;
  int iter = 0, max_iter = 100;
  const gsl_root_fdfsolver_type *T;
  gsl_root_fdfsolver *s;
  double x0, x = 5.0;
  gsl_function_fdf FDF;
  struct function_params *p 
    = (struct function_params *) params;
  
  
  
  FDF.f = &solve;
  FDF.df = &solve_deriv;
  FDF.fdf = &solve_fdf;
  FDF.params = p;
  

  x= rootExpansion( p->Nt, p->mu);
  //printf("%f\n",x);
  
  //printf("%f %f\n", solve(x, &params ), solve_deriv( x, &params  )); 



  //==Newton=============
  T = gsl_root_fdfsolver_newton;
  s = gsl_root_fdfsolver_alloc (T);
  gsl_root_fdfsolver_set (s, &FDF, x);
  
  //printf ("using %s method\n", 	  gsl_root_fdfsolver_name (s));
  
  //printf ("%-5s %10s %10s %10s\n",	  "iter", "root", "err", "err(est)");
  do
    {
      iter++;
      status = gsl_root_fdfsolver_iterate (s);
      x0 = x;
      x = gsl_root_fdfsolver_root (s);
      status = gsl_root_test_delta (x, x0, 0, 1e-3);

      /*
      if (status == GSL_SUCCESS)
	printf ("Converged:\n");
      */
      
      //printf ("%5d %10.7f %+10.7f %10.7f\n",	      iter, x, x , x - x0);
    }
  while (status == GSL_CONTINUE && iter < max_iter);
  
  gsl_root_fdfsolver_free (s);
  return x;

}



/*
int main (void)
{
  int i;
  struct function_params params = {1000.0, 10.0};

  
  for(i = 1  ;   i <= 40   ;   i++){
    printf("%f %f %f\n", i*1.0, solve(1.0*i, &params ), solve_deriv( 1.0*i, &params  )); 
  }
  
  printf("%f\n", rootExpansion( 1.0, 1.0));
  return 0;
}
*/

double solve (double Ns, void *params)
{
  
  struct function_params *p 
    = (struct function_params *) params;
  
  double Nt = p->Nt;
  double mu = p->mu;
 
  //double M_PI = 3.1415926535897932385;

    return (1/(-1 + Ns) + 1/(Ns - Nt))/2. + mu*(-1 + (48*Power(Ns,3))/(16*Power(Ns,3) - 9*Power(Nt,2)*M_PI)) + 
   (9*mu*Power(Nt,2)*M_PI*(-64*Power(Ns,3) + 9*Power(Nt,2)*M_PI)
    * 4.0 * real_ans ( 1 - (9*Power(Nt,2)*M_PI)/(16.*Power(Ns,3)) )
    )/(4.*Power(16*Power(Ns,3) - 9*Power(Nt,2)*M_PI,2)) + 
      Log(-1 + Ns) - Log(-Ns + Nt);



}


double solve_deriv (double Ns,   void *params)
{
  
  struct function_params *p 
    = (struct function_params *) params;
  
  double Nt = p->Nt;
  double mu = p->mu;

  //double Pi = 3.1415926535897932385;
  

  return
    2/(-1 + Ns) - (-0.5 + Ns)/Power(-1 + Ns,2) + 2/(-Ns + Nt) - (0.5 - Ns + Nt)/Power(-Ns + Nt,2) + 
    mu*((-2187*Power(Nt,4)*Power(M_PI,2))/(512.*Power(Ns,7)*Power(1 - (9*Power(Nt,2)*M_PI)/(16.*Power(Ns,3)),2)) - 
	(135*Power(Nt,2)*M_PI)/(16.*Power(Ns,4)*(1 - (9*Power(Nt,2)*M_PI)/(16.*Power(Ns,3)))) + 



	(19683*Power(Nt,6)*Power(M_PI,3)*
	 real_ans(1 - (9*Power(Nt,2)*M_PI)/(16.*Power(Ns,3)))
	 )/
	(8192.*Power(Ns,10)*Power(1 - (9*Power(Nt,2)*M_PI)/(16.*Power(Ns,3)),3)) + 


	(243*Power(Nt,4)*Power(M_PI,2)*
	 real_ans(1 - (9*Power(Nt,2)*M_PI)/(16.*Power(Ns,3)))
	 )/
	(32.*Power(Ns,7)*Power(1 - (9*Power(Nt,2)*M_PI)/(16.*Power(Ns,3)),2)) + 

	
	(27*Power(Nt,2)*M_PI*
	real_ans(1 - (9*Power(Nt,2)*M_PI)/(16.*Power(Ns,3)))
	)/
	(4.*Power(Ns,4)*(1 - (9*Power(Nt,2)*M_PI)/(16.*Power(Ns,3))))
	);
  
}




void solve_fdf (double x, void *params, 
	       double *y, double *dy)
{
  struct function_params *p 
    = (struct function_params *) params;
  
  
  *y = solve(x, p );
  *dy =  solve_deriv( x, p  );
}


double real_ans( double x)
{
  //uses complex numbers to return  sqrt(x)*aTanh( sqrt(x) ) which is always real (as long as x<1)

  gsl_complex z;

  z = gsl_complex_sqrt_real (x);


  return GSL_REAL ( gsl_complex_mul( z,  gsl_complex_arctanh( z ) ) );

}


/*
double Power( double x, int i)
{

  return pow( x,i);
  //  if( i==2 ) return ;
}
*/

double rootExpansion( double Nt, double mu)
{

  //double Pi = 3.1415926535897932385;

  return (-2*Nt*(2*Nt - 9*M_PI)*(16*(-1 + mu)*Power(Nt,2) + 72*(2 + 7*mu)*Nt*M_PI - 81*(4 + 5*mu)*Power(M_PI,2)) 


	  + 
	  9*mu*Nt*M_PI*(128*Power(Nt,2) - 180*Nt*M_PI + 405*Power(M_PI,2))
	 
	  //*Sqrt(4 - (18*M_PI)/Nt)*ArcTanh(Sqrt(1 - (9*M_PI)/(2.*Nt)))
	  *2.0*real_ans(1 - (9*M_PI)/(2.*Nt))

	  )


    /



    (4*(2*Nt - 9*M_PI)*(16*Power(Nt,2) - 36*(4 + 15*mu)*Nt*M_PI + 81*(4 + 3*mu)*Power(M_PI,2)) 
     
     
     + 
     54*mu*M_PI*(32*Power(Nt,2) + 81*Power(M_PI,2))
	  *2.0*real_ans(1 - (9*M_PI)/(2.*Nt))

     //*Sqrt(4 - (18*M_PI)/Nt)*ArcTanh(Sqrt(1 - (9*M_PI)/(2.*Nt)))
     )

    ;

}

double A (double Ns,   void *params)
{
  
  struct function_params *p 
    = (struct function_params *) params;
  
  double Nt = p->Nt;
  double mu = p->mu;

  //double Pi = 3.1415926535897932385;
  

  return
  mu*(2*Ns + 

      (9*Power(Nt,2)*M_PI
       *real_ans(1 - (9*Power(Nt,2)*M_PI)/(16.*Power(Ns,3)))
       )/
      (8.*Power(Ns,2)*(1 - (9*Power(Nt,2)*M_PI)/(16.*Power(Ns,3))))


      )


    + (-0.5 + Ns)*Log(-1 + Ns) + 
    (0.5 - Ns + Nt)*Log(-Ns + Nt);

}
