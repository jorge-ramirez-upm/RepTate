/* kww.c:
 *   Calculation of the Kohlrausch-Williams-Watts spectrum, i.e.
 *   Laplace-Fourier transform of the stretched exponential function exp(-t^b).
 *   Frequently used to describe relaxation in disordered systems.
 * 
 * Copyright:
 *   (C) 2009, 2012 Joachim Wuttke
 * 
 * Licence:
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published
 *   by the Free Software Foundation; either version 3 of the License, or
 *   (at your option) any later version. Alternative licenses can be
 *   obtained through written agreement from the author.
 * 
 *   This program is distributed in the hope that it will be useful,
 *   but without any warranty; without even the implied warranty of
 *   merchantability or fitness for a particular purpose.
 *   See the GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program. If not, see <http://www.gnu.org/licenses/>.
 *
 * Author:
 *   Joachim Wuttke
 *   Forschungszentrum Jülich, Germany
 *   j.wuttke@fz-juelich.de
 *
 * Websites:
 *   http://apps.jcns.fz-juelich.de/doku/sc/kww
 *
 * Reference:
 *   Wuttke, http://arxiv.org/abs/0911.4796
 */

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <float.h> // OBSOLETE
#include <errno.h>
#include "kww.h"
#define PI           3.14159265358979323846L  /* pi */
#define PI_2         1.57079632679489661923L  /* pi/2 */
#define SQR(x) ((x)*(x))

int kww_algorithm, kww_num_of_terms, kww_debug=0; // for external analysis

/*****************************************************************************/
/*  Numeric precision and maximum number of terms                            */
/*****************************************************************************/

const double kww_delta=2.2e-16, kww_eps=5.5e-20;
const int max_terms=200;

/*****************************************************************************/
/*  Approximate limits of asymptotic regimes                                 */
/*****************************************************************************/

double kwwc_lim_low( const double b )
{
    if ( b>1.024 )
        return -0.8774954*b + 3.5873*b*b -2.083*b*b*b +0.3796*b*b*b*b;
    else
        return exp( -0.02194/b/b -4.130/b +2.966189 +0.030104*b +1.062*b*b );
}

double kwws_lim_low( const double b )
{
    if ( b>1.024 )
        return -1.68725*b + 4.8108*b*b -2.561*b*b*b +0.442*b*b*b*b;
    else
        return exp( -0.03208/b/b -4.314/b +3.516200 -0.50287*b +1.240*b*b );
}

double kwwp_lim_low( const double b )
{
    if ( b>1.085 )
        return -10.49909 +19.23618*b -9.234064*b*b +1.553016*b*b*b;
    else
        return exp( -0.02259971/b/b -4.099837/b +3.100445
                    -0.1838126*b +1.118149*b*b );
}


double kwwc_lim_hig( const double b )
{
    if ( b<0.82 )
        return exp( 0.006923209/b/b -1.321692/b -1.44582
                    +2.516339*b +0.2973773*b*b );
    else
        return exp( -0.746496154631 +6.057558*(b-.82) -3.41052*SQR(b-.82)
                    +0.7932314*pow(b-.82,3) );
}

double kwws_lim_hig( const double b )
{
    if ( b<0.82 )
        return exp( 0.07847516/b/b -2.585876/b +4.999414
                    -8.460926*b +6.289183*b*b );
    else
        return exp( -0.962597724393 +5.818057*(b-.82) -3.026212*SQR(b-.82)
                    +0.5485754*pow(b-.82,3) );
}

double kwwp_lim_hig( const double b )
{
    if ( b<0.82 )
        return exp( 0.003809101/b/b -1.955504/b -1.938468
                    +5.893199*b -2.197289*b*b );
    else
        return exp( -0.962597724393 +7.074977*(b-.82) -5.231151*SQR(b-.82)
                    +1.717068*pow(b-.82,3) );
}


/*****************************************************************************/
/*  Auxiliary functions for debugging                                        */
/*****************************************************************************/

void kww_hexprint_double( const char* name, const double x )
{
    union {
        double d;
        unsigned long u;
    } u;
    u.d = x;
    printf( "  %s = %24.18f [%lx]\n", name, x, u.u );
}

void kww_hexprint_quad( const char* name, const long double x )
{
    union {
        long double d;
        unsigned long long u;
    } u;
    u.d = x;
    printf( "  %s = %24.18Lf [%llx]", name, x, u.u );
}


/*****************************************************************************/
/*  High-level wrapper functions                                             */
/*****************************************************************************/

/* \int_0^\infty dt cos(w*t) exp(-t^beta) */
double kwwc( const double w_in, const double beta )
{
    double w, res;
    /* check input data */
    if ( beta<0.1 ) {
        fprintf( stderr, "kww: beta smaller than 0.1\n" );
        exit( EDOM );
    }
    if ( beta>2.0 ) {
        fprintf( stderr, "kww: beta larger than 2.0\n" );
        exit( EDOM );
    }
    /* it's an even function; the value at w=0 is well known */
    if ( w_in==0 )
        return tgamma(1.0/beta)/beta;
    w = fabs( w_in );
    /* special case: Gaussian for b=2 */
    if ( beta==2 )
        return sqrt(PI)/2*exp(-SQR((double)w)/4);
    /* try series expansion */
    if        ( w<kwwc_lim_low( beta ) ) {
        res = kwwc_low( w, beta );
        if ( res>0 )
            return res;
    } else if ( w>kwwc_lim_hig( beta ) ) {
        res = kwwc_hig( w, beta );
        if ( res>0 )
            return res;
    }
    /* fall back to numeric integration */
    res = kwwc_mid( w, beta );
    if ( res<0 ) {
        //JR CHANGES
        return 0;
/*        if( beta>1.9 )
            return 0; // must be tested by the user
        // otherwise it ought to be considered a bug
        fprintf( stderr, "kwwc: numeric integration failed for"
                 " omega=%25.18g, beta=%25.18g; error code %g\n",
                 w, beta, res );
        exit( ENOSYS );*/
    }
    return res;
}

/* \int_0^\infty dt sin(w*t) exp(-t^beta) */
double kwws( const double w_in, const double beta )
{
    double w, res;
    int sign_out;
    /* check input data */
    if ( beta<0.1 ) {
        fprintf( stderr, "kww: beta smaller than 0.1\n" );
        exit( EDOM );
    }
    if ( beta>2.0 ) {
        fprintf( stderr, "kww: beta larger than 2.0\n" );
        exit( EDOM );
    }
    /* it's an odd function */
    if ( w_in==0 )
        return 0;
    if ( w_in<0 ) {
        w = - w_in;
        sign_out = -1;
    } else {
        w = w_in;
        sign_out = 1;
    }
    /* try series expansion */
    if        ( w<kwws_lim_low( beta ) ) {
        res = kwws_low( w, beta );
        if ( res>0 )
            return sign_out*res;
    } else if ( w>kwws_lim_hig( beta ) ) {
        res = kwws_hig( w, beta );
        if ( res>0 )
            return sign_out*res;
    }
    /* fall back to numeric integration */
    res = kwws_mid( w, beta );
    if ( res<0 ) {
        // JR Changes
        return 0;
        /*
        fprintf( stderr, "kwws: numeric integration failed for"
                 " omega=%25.18g, beta=%25.18g; error code %g\n",
                 w, beta, res );
        exit( ENOSYS );
        */
    }
    return sign_out*res;
}

/* \int_0^w dw' \int_0^\infty dt cos(w'*t) exp(-t^beta) */
double kwwp( const double w_in, const double beta )
{
    double w, res;
    int sign_out;
    /* check input data */
    if ( beta<0.1 ) {
        fprintf( stderr, "kww: beta smaller than 0.1\n" );
        exit( EDOM );
    }
    if ( beta>2.0 ) {
        fprintf( stderr, "kww: beta larger than 2.0\n" );
        exit( EDOM );
    }
    /* it's an odd function */
    if ( w_in==0 )
        return 0;
    if ( w_in<0 ) {
        w = - w_in;
        sign_out = -1;
    } else {
        w = w_in;
        sign_out = 1;
    }
    /* try series expansions */
    if        ( w<kwwp_lim_low( beta ) ) {
        res = kwwp_low( w, beta );
        if ( res>0 )
            return sign_out*res;
    } else if ( w>kwwp_lim_hig( beta ) ) {
        res = kwwp_hig( w, beta );
        if ( res>0 )
            return sign_out*res;
    }
    /* fall back to numeric integration */
    res = kwwp_mid( w, beta );
    if ( res<0 ) {
        // JR CHANGES
        return 0;
        /*
        fprintf( stderr, "kwwp: numeric integration failed for"
                 " omega=%25.18g, beta=%25.18g; error code %g\n",
                 w, beta, res );
        exit( ENOSYS );
        */
    }
    return sign_out*res;
}


/*****************************************************************************/
/*  Low-level implementation: series expansion for low frequencies           */
/*****************************************************************************/

double kww_low( const double w, const double beta,
                const int kappa, const int mu )
{
    int kk;               // this is 2*k+kappa
    int isig=1;           // alternating sign
    long double S=0;      // summed series
    long double T=0;      // sum of absolute values
    long double u;        // precomputed common factors
    long double u_next=0; // - next value [initialized to avoid warning]
    long double gl;       // local variable

    // set diagnostic variable
    kww_algorithm = 1; 

    // check input
    if ( beta<0.1 || beta>2.0 ) {
        fprintf( stderr, "invalid call to kww_low: beta out of range\n" );
        exit( EDOM );
    }
    if ( w<=0 ) {
        fprintf( stderr, "invalid call to kww_low: w out of range\n" );
        exit( EDOM );
    }

    // sum the expansion
    kk = kappa;
    int i;
    for ( i=0; i<max_terms; ++i ) {
        kww_num_of_terms = i;
        // t_n must be computed in advance
        u = u_next;
        // use log gamma instead of gamma to avoid overflow
        gl = lgammal((long double)(kk+1)/(long double)beta)-
            lgammal((long double)kk+1)+(kk+mu)*logl((long double)w);
        if ( gl>DBL_MAX_EXP/2 )
            return -3; // gamma function overflow
        u_next = expl( gl );
        if( mu )
            u_next /= (kk+1);
        kk += 2;
        if( !i )
            continue;
        // now we use t_{n-1} to compute S_n
        S += isig*u;        
        T += u;
        // termination criteria
        if ( kww_eps*T+u_next <= kww_delta*S )
            return S / beta; // reached required precision
        else if ( kww_eps*T >= kww_delta*S )
            return -6; // too much cancellation
        else if ( beta<1 && u_next>u )
            return -5; // asymptotic expansion diverges too early
        else if ( S<DBL_MIN )
            return -7; // underflow
        isig = -isig;
    }
    return -9; // too many terms
}

double kwwc_low( const double w, const double beta )
{
    return kww_low( w, beta, 0, 0 );
}

double kwws_low( const double w, const double beta )
{
    return kww_low( w, beta, 1, 0 );
}

double kwwp_low( const double w, const double beta )
{
    return kww_low( w, beta, 0, 1 );
}

/*****************************************************************************/
/*  Low-level implementation: series expansion for high frequencies          */
/*****************************************************************************/

double kww_hig( const double w, const double beta,
                const int kappa, const int mu )
{
    int k;           // in computation of A_k w^k
    int isig=1;      // alternating sign
    int alternating; // has factor (-)^k
    long double b;        // either beta or 2-beta
    long double sinphi;   // to compute r from u
    long double truncfac; // for termination criterion
    long double rfac;     // for computation of remainder
    long double S=0;      // summed series
    long double Sabs;     // absolute value thereof
    long double T=0;      // sum of absolute values
    long double u;        // precomputed common factors
    long double u_next=0; // - next value [initialized to avoid warning]
    long double s;        // full term (with trigonometric factor)
    long double x, gl;    // local variables

    if( kww_debug & 8 ) {
        printf( "kww_hig: kappa %i mu %i deb %i\n", kappa, mu, kww_debug );
        kww_hexprint_double( "b", beta );
        kww_hexprint_double( "w", w );
    }

    // set diagnostic variable
    kww_algorithm = 3;

    // check input
    if ( beta<0.1 || beta>2.0 ) {
        fprintf( stderr, "invalid call to kww_hig: beta out of range\n" );
        exit( EDOM );
    }
    if ( w<=0 ) {
        fprintf( stderr, "invalid call to kww_hig: w out of range\n" );
        exit( EDOM );
    }

    // set some beta-dependent constants
    if ( beta<1 ) {
        b = beta;
        alternating = 1;
        sinphi = 1;
        truncfac = 1;
    } else {
        b = 2.0-beta;
        alternating = 0;
        sinphi = sinl( PI/2/(long double)beta );
        truncfac = powl( sinphi, -(long double)beta );
    }
    rfac = 1/sinphi;

    if( kww_debug & 2 ) {
        printf( "sinphi %20.14Le truncfac %20.14Le\n", sinphi, truncfac );
    }
    if( kww_debug & 1 )
        printf( "%3s %20s %20s %12s %12s %12s %12s %12s %12s %12s\n",
                "k+2", "S=sum(s)", "T=sum(|s|)",
                "s", "s/u", "u(k)", "u(k+1)", "rfac",
                "eps*T+u(k+1)*r", "delta*|S|" );

    // sum the expansion
    k=1-kappa;
    if( k )
        rfac *= truncfac;
    int i;
    for ( i=0; i<max_terms; ++i ) {
        kww_num_of_terms = i;
        // t_n must be computed in advance
        u = u_next;
        x = k*(long double)beta+1;
        // use log gamma instead of gamma to avoid overflow
        gl = lgammal(x)-lgammal((long double)k+1)+(mu-x)*logl((long double)w);
        if ( gl>DBL_MAX_EXP/2 )
            return -3; // gamma function overflow
        u_next = expl( gl );
        if( mu )
            u_next /= (k*beta);
        ++k;
        if( !i )
            continue;
        // now we use t_{n-1} to compute S_n (k is even 2 ahead)
        s = u * isig * ( kappa ? cosl(PI_2*(k-2)*b) : sinl(PI_2*(k-2)*b) );
        S += s;
        Sabs = fabsl(S);
        T += fabsl(s);
        rfac *= truncfac; // sin(phi)^(-1-k*beta)
        if( kww_debug & 1 )
            printf( "%3i %20.13Le %20.13Le %12.5Le %12.5Le %12.5Le %12.5Le"
                    " %12.5Le %12.5Le %12.5Le\n",
                    k, S, T, s, s/u, u, u_next, rfac,
                    kww_eps*T+u_next*rfac, kww_delta*Sabs );
        // termination criteria
        if ( kww_eps*T+u_next*rfac <= kww_delta*Sabs )
            return S; // reached required precision
        else if ( beta>1 && u_next*truncfac>u )
            return -5; // asymptotic expansion diverges too early
        else if ( Sabs<DBL_MIN )
            return -7; // underflow
        if ( alternating )
            isig = -isig;
    }
    return -9; // not converged
}

double kwwc_hig( const double w, const double beta )
{
    return kww_hig( w, beta, 0, 0 );
}

double kwws_hig( const double w, const double beta )
{
    return kww_hig( w, beta, 1, 0 );
}

double kwwp_hig( const double w, const double beta )
{
    double res = kww_hig( w, beta, 0, 1 );
    if ( res>=PI_2 ) {
        fprintf( stderr, "kwwp: invalid result %g <= 0\n", res );
        exit( ENOSYS );
    }
    return res<0 ? res : PI_2-res;
}


/*****************************************************************************/
/*  Low-level implementation: integration for intermediate frequencies       */
/*****************************************************************************/

#define max_iter_int 12
#define num_range 6
double kww_mid( const double w, const double beta,
                const int kind, const int mu )
// kind: 0 cos, 1 sin transform (precomputing arrays[2] depend on this)
{
    int iter;
    int kaux;
    int isig;
    int N;
    int j;               // range
    int diffmode;        // subtract Gaussian ?
    long double S=0;     // trapezoid sum
    long double S_last;  // - in last iteration
    long double s;       // term contributing to S
    long double T;       // sum of abs(s)
    // precomputed coefficients
    static int firstCall=1;
    static int iterDone[2][num_range]; // Nm,Np,ak,bk are precomputed up to this
    static int NN[num_range][max_iter_int];
    static long double *ak[2][num_range][max_iter_int];
    static long double *bk[2][num_range][max_iter_int];
    // auxiliary for computing ak and bk
    long double u;
    long double e;
    long double tk;
    long double chi;
    long double dchi;
    long double h;
    long double k;
    long double f;
    long double ahk;
    long double chk;
    long double dhk;
    double p;
    double q;
    const double Smin=2e-20; // to assess worst truncation error

    int nalloc_ak_bk = 0;
    int ii;

    // dynamic initialization upon first call
    if ( firstCall ) {
        for ( j=0; j<num_range; ++ j ) {
            iterDone[0][j] = -1;
            iterDone[1][j] = -1;
        }
        firstCall = 0;
    }

    // check input
    if ( !( kind==0 || kind==1 ) ) {
        fprintf( stderr, "invalid call to kww_mid: invalid kind\n" );
        exit( EDOM );
    } else if ( beta<0.1 || beta>2.0 ) {
        fprintf( stderr, "invalid call to kww_mid: beta out of range\n" );
        exit( EDOM );
    } else if ( w<=0 ) {
        fprintf( stderr, "invalid call to kww_mid: w out of range\n" );
        exit( EDOM );
    }

    // cosine transform needs special care for beta->2
    if ( kind==0 ) {
        if ( beta==2 )
            return sqrt(PI)/2*exp(-SQR(w)/4);
        diffmode = beta>1.75;
    } else {
        diffmode = 0;
    }

    // determine range, set p,q
    if        ( beta<0.15 ) {
        j=0; p=1.8; q=0.2;
    } else if ( beta<0.25 ) {
        j=1; p=1.6; q=0.4;
    } else if ( beta<1 ) {
        j=2; p=1.4; q=0.6;
    } else if ( beta<1.75 ) {
        j=3; p=1.0; q=0.2;
    } else if ( beta<1.95 ) {
        j=4; p=.75; q=0.2;
    } else {
        j=5; p=.15; q=0.4;
    }
        
    // iterative integration
    kww_algorithm = 2;
    kww_num_of_terms = 0;
    if( kww_debug & 4 ) 
        // do not iterate, inspect just one sum
        N = 100;
    else
        N = 40;

    if( kww_debug & 8 ) {
        printf( "kww_mid %i %i %i %i\n", kind, mu, N, kww_debug );
        kww_hexprint_double( "b", beta );
        kww_hexprint_double( "w", w );
    }
    for ( iter=0; iter<max_iter_int; ++iter ) {
        // static initialisation of NN, ak, bk for given 'iter'
        if ( iter>iterDone[kind][j] ) {
            if ( N>1e6 ){
                for (ii=0; ii < nalloc_ak_bk; ii++){
                    free(ak[kind][j][ii]);
                    free(bk[kind][j][ii]);
                }
                return -3; // integral limits overflow
            }
            NN[j][iter] = N;
            if ( !( ak[kind][j][iter]=malloc((sizeof(long double))*(2*N+1)) ) ||
                 !( bk[kind][j][iter]=malloc((sizeof(long double))*(2*N+1)) )) {
                fprintf( stderr, "kww: Workspace allocation failed\n" );
                for (ii=0; ii < nalloc_ak_bk; ii++){
                    if ( ii>iterDone[kind][j] ) {
                        free(ak[kind][j][ii]);
                        free(bk[kind][j][ii]);
                    }
                }
                exit( ENOMEM );
            }
            else{
                nalloc_ak_bk++;
            }
            h = logl( logl( 42*N/kww_delta/Smin ) / p ) / N; // 42=(pi+1)*10
            isig=1-2*(NN[j][iter]&1);
            if( kww_debug & 8 ) {
                printf( "init iter %i kind %i j %i siz %i\n",
                        iter, kind, j, 2*N+1 );
            }
            for ( kaux=-NN[j][iter]; kaux<=NN[j][iter]; ++kaux ) {
                k = kaux;
                if( !kind )
                    k -= 0.5;
                u = k*h;
                chi  = 2*p*sinhl(u) + 2*q*u;
                dchi = 2*p*coshl(u) + 2*q;
                if ( u==0 ) {
                    if ( k!=0 ){
                        for (ii=0; ii < nalloc_ak_bk; ii++){
                            if ( ii>iterDone[kind][j] ) {
                                free(ak[kind][j][ii]);
                                free(bk[kind][j][ii]);
                            }
                        }
                        return -4; // integration variable underflow
                    }
                    // special treatment to bridge singularity at u=0
                    ahk = PI/h/dchi;
                    dhk = 0.5;
                    chk = sin( ahk );
                } else {
                    if ( -chi>DBL_MAX_EXP/2 ){
                        for (ii=0; ii < nalloc_ak_bk; ii++){
                            if ( ii>iterDone[kind][j] ) {
                                free(ak[kind][j][ii]);
                                free(bk[kind][j][ii]);
                            }
                        }
                        return -5; // integral transformation overflow
                    }
                    e = expl( -chi );
                    ahk = PI/h * u/(1-e);
                    dhk = 1/(1-e) - u*e*dchi/SQR(1-e);
                    chk = e>1 ?
                        ( kind ? sinl( PI*k/(1-e) ) : cosl( PI*k/(1-e) ) ) :
                        isig * sinl( PI*k*e/(1-e) );
                }
                ak[kind][j][iter][kaux+NN[j][iter]] = ahk;
                bk[kind][j][iter][kaux+NN[j][iter]] = dhk * chk;
                isig = -isig;
            }
            iterDone[kind][j] = iter;
        }
        // integrate according to trapezoidal rule
        S_last = S;
        S = 0;
        T = 0;
        for ( kaux=-NN[j][iter]; kaux<=NN[j][iter]; ++kaux ) {
            tk = ak[kind][j][iter][kaux+NN[j][iter]] / w;
            f = expl(-powl(tk,(long double)beta));
            if ( diffmode )
                f -= expl(-SQR(tk));
            if ( mu )
                f /= tk;
            s = bk[kind][j][iter][kaux+NN[j][iter]] * f;
            S += s;
            T += fabsl(s);
            if( kww_debug & 2 )
                printf( "%2i %6i %12.4Lg %12.4Lg"
                        " %12.4Lg %12.4Lg %12.4Lg %12.4Lg\n", 
                        iter, kaux, ak[kind][j][iter][kaux+NN[j][iter]],
                        bk[kind][j][iter][kaux+NN[j][iter]], f, s, S, T );
        }
        if( kww_debug & 1 )
            printf( "%23.17Le  %23.17Le\n", S, T );
        kww_num_of_terms += 2*NN[j][iter]+1;
        if ( diffmode )
            S += w/sqrt(PI)/2*exp(-SQR(w)/4);
        if( kww_debug & 8 ) {
            printf( "iter %i N %i\n", iter, N );
            kww_hexprint_double( "S_new", S );
            kww_hexprint_double( "S_old", S_last );
        }
        // termination criteria
        if      ( kww_debug & 4 ){
            for (ii=0; ii < nalloc_ak_bk; ii++){
                free(ak[kind][j][ii]);
                free(bk[kind][j][ii]);
            }
            return -1; // we want to inspect just one sum
        }
        else if ( S < 0 && !diffmode ){
            for (ii=0; ii < nalloc_ak_bk; ii++){
                if ( ii>iterDone[kind][j] ) {
                    free(ak[kind][j][ii]);
                    free(bk[kind][j][ii]);
                }
            }
            return -6; // cancelling terms lead to negative S
        }
        else if ( kww_eps*T > kww_delta*fabs(S) ){
            for (ii=0; ii < nalloc_ak_bk; ii++){
                if ( ii>iterDone[kind][j] ) {
                    free(ak[kind][j][ii]);
                    free(bk[kind][j][ii]);
                }
            }
            return -2; // cancellation
        }
        else if ( iter && fabs(S-S_last) + kww_eps*T < kww_delta*fabs(S) ){
            for (ii=0; ii < nalloc_ak_bk; ii++){
                if ( ii>iterDone[kind][j] ) {
                    free(ak[kind][j][ii]);
                    free(bk[kind][j][ii]);
                }
            }
            return S * PI / w; // success (for factor pi/w see my eq. 48)
        }
        N *= 2; // retry with more points
    }
    for (ii=0; ii < nalloc_ak_bk; ii++){
        if ( ii>iterDone[kind][j] ) {
            free(ak[kind][j][ii]);
            free(bk[kind][j][ii]);
        }
    }
    return -9; // not converged
}

double kwwc_mid( const double w, const double beta )
{
    return kww_mid( w, beta, 0, 0 );
}

double kwws_mid( const double w, const double beta )
{
    return kww_mid( w, beta, 1, 0 );
}

double kwwp_mid( const double w, const double beta )
{
    return kww_mid( w, beta, 1, 1 );
}
