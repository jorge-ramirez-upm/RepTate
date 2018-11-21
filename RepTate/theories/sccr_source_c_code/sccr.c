// RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
// --------------------------------------------------------------------------------------------------------

// Authors:
//     Jorge Ramirez, jorge.ramirez@upm.es
//     Victor Boudara, victor.boudara@gmail.com

// Useful links:
//     http://blogs.upm.es/compsoftmatter/software/reptate/
//     https://github.com/jorge-ramirez-upm/RepTate
//     http://reptate.readthedocs.io

// --------------------------------------------------------------------------------------------------------

// Copyright (2017): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds

// This file is part of RepTate.

// RepTate is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// RepTate is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with RepTate.  If not, see <http://www.gnu.org/licenses/>.

#include <math.h>

static int Z, N, SIZE;
static double prevt, dt, beta_rcr, cnu;
const double Rs = 2.0;

#define MIN(a,b) (((a)<(b))?(a):(b))
#define MAX(a,b) (((a)>(b))?(a):(b))
#define MAX4(a,b,c,d) MAX(MAX(a,b), MAX(c,d))
#define MIN4(a,b,c,d) MIN(MIN(a,b), MIN(c,d))

/*
    Convert k,i,j (3D array) indices to ind (1D array), considering the symmetry of the problem
     \  1 /  (j=i diagonal)
      \  /
     2 \/ 4
       /\
      /  \
     /  3 \ (j=N-i diagonal)
*/
int ind(int k, int i, int j) {
    if (j>=i && j>=(N-i)) { // 1st Quadrant
        int ind0 = k*SIZE;
        if (i<=N/2)
            return ind0 + i*(i+3)/2+j-N;
        else {
            if (N % 2 == 0)
                return ind0 - i*i/2+(2*N+1)*i/2 + j - N*(2+N)/4;
            else
                return ind0 - i*i/2+(2*N+1)*i/2 + j - pow((N+1)/2,2);
        }
    }
    else if (j>=i && j<(N-i)) { // 2nd Quadrant
        // Reflection of point on J=N-I line
        int auxi=N-j;
        int auxj=N-i;
        return ind(k, auxi, auxj);
    }
    else if (j<i && j<(N-i)) { // 3rd Quadrant
        // INVERSION OF THE POINT WITH RESPECT TO THE POINT (N/2, N/2)
        int auxi=N-i;
        int auxj=N-j;
        return ind(k, auxi, auxj);
    }
    else if (j<i && j>=(N-i)) { // 4th Quadrant
        // Reflection of point on K=I line
        int auxi=j;
        int auxj=i;
        return ind(k, auxi, auxj);
    }
}

int get_im(int i, int j){
    int im=i;
    int imin=i;
    if(j<imin) {
        im=j;
        imin=j;
    }
    if(N-i<imin) {
        im=i;
        imin=N-i;
    }
    if(N-j<imin)
        im=j;
    return im;
}

/*  1D diffusion coefficient (reptation + CLF)
    With cut-off for maximum D=a^2/6/tau_e */
double d1(double s) {
    double ad = 1.15;
    double w=0;
    double waux=1.0/M_PI/M_PI/3.0*(M_PI*M_PI/2.0-1.0/Z);
    s*=Z/N;
    if (s==0)
        w = waux;
    else if (s<ad*sqrt(Z))
        w=1.0/M_PI/M_PI/3.0*(ad*ad/s/s-1.0/Z);
    if (w>waux)
        w = waux;
    return w;
}

/* 1D diffusion coefficient (reptation + CLF) */
double d(i, j) {
    int sm=MIN4(i, j, N-i, N-j);
    return 1.0/3.0/M_PI/M_PI/Z+d1(sm);
}

int sccr_dy(double t, double gdot, double *y, double *yeq, double *yn, double *dy, double *normf, double *normfn) {
    int i, j, k, mm;
    int fkij, fkip1jp1, fkim1jm1, fkip1j, fkim1j, fkijp1, fkijm1, f0ij, f1ij, f2ij;
    
    if (t>prevt) {
        dt=t-prevt;
        prevt=t;
    }

    // Instantaneous number of entanglements (normalized arc length of primitive path)
    // And norm of f
    double zstar=0.0;
    for (j=0; j<=N; ++j) {
        normf[j]=y[ind(0,j,j)] + 2*y[ind(2,j,j)];
        zstar=zstar+sqrt(normf[j]);
    }
    zstar=zstar*Z/N;

    for (k=0;k<3;++k) {
        for (i=1;i<N;++i) {
            mm = MAX(N-i,i);
            for (j=mm;j<N;++j) {

                int im=get_im(i,j);

                fkij = ind(k,i,j);
                fkip1jp1 = ind(k,i+1,j+1);
                fkim1jm1 = ind(k,i-1,j-1);
                fkip1j = ind(k,i+1,j);
                fkim1j = ind(k,i-1,j);
                fkijp1 = ind(k,i,j+1);
                fkijm1 = ind(k,i,j-1);

                dy[fkij]=1.0/2.0/M_PI/M_PI*N/Z*N/Z*Rs* 
                        ((y[fkip1j]-y[fkim1j])/2.0*  // Retr (s)
                        (log(normf[i+1])-log(normf[i-1]))/2.0 
                        +y[fkij]*(log(normf[i+1])+log(normf[i-1])-2.0*log(normf[i])));

                dy[fkij]+=1.0/2.0/M_PI/M_PI*N/Z*N/Z*Rs* 
                        ((y[fkijp1]-y[fkijm1])/2.0*   // Retr (s')
                        (log(normf[j+1])-log(normf[j-1]))/2.0
                        +y[fkij]*(log(normf[j+1])+log(normf[j-1])-2.0*log(normf[j])));
        
                // Chain rule applied to Rept+CLF term
                dy[fkij]+=N/Z*N/Z/sqrt(normf[im])*(
                        (d(i+1,j+1)-d(i-1,j-1))/2.0*(y[fkip1jp1]-y[fkim1jm1])/2.0/sqrt(normf[im])	// CLF
                        +d(i,j)*(y[fkip1jp1]-y[fkim1jm1])/2.0*
                        (1.0/sqrt(normf[im+1])-1.0/sqrt(normf[im-1]))/2.0
                        +d(i,j)/sqrt(normf[im])*(y[fkip1jp1]+y[fkim1jm1]-2.0*y[fkij])
                        );
            }
        }
    } 
    
    // Get partially updated y to calculate retraction rate
    for (i=0;i<3*SIZE;++i)
        yn[i] = y[i] + dy[i]*dt;
    for (j=0; j<=N; ++j)
        normfn[j]=yn[ind(0,j,j)] + 2*yn[ind(2,j,j)];  
    double lam=0.0;
    if (dt>0) {
        for (i=1;i<N;++i)
            lam-=(normfn[i]-normf[i])/N/2.0/dt/sqrt(normf[i]);
    }
    
    for (k=0;k<3;++k) {
        for (i=1;i<N;++i) {
            mm = MAX(N-i,i);
            for (j=mm;j<N;++j) {

                fkij = ind(k,i,j);
                fkip1jp1 = ind(k,i+1,j+1);
                fkim1jm1 = ind(k,i-1,j-1);
                fkip1j = ind(k,i+1,j);
                fkim1j = ind(k,i-1,j);
                fkijp1 = ind(k,i,j+1);
                fkijm1 = ind(k,i,j-1);

                dy[fkij]+=N/Z*N/Z*1.5*(lam+1.0/3.0/beta_rcr/Z/Z/Z)*cnu*(Z/zstar) 
                    *((y[fkip1j]+y[fkim1j]-2.0*y[fkij]-yeq[fkip1j]-yeq[fkim1j]+2.0*yeq[fkij])  // CCR
                    /sqrt(normf[i])
                    +(y[fkip1j]-y[fkim1j]-yeq[fkip1j]+yeq[fkim1j])/2.0
                    *(1.0/sqrt(normf[i+1])-1.0/sqrt(normf[i-1]))/2.0
            
                    +(y[fkijp1]+y[fkijm1]-2.0*y[fkij]-yeq[fkijp1]-yeq[fkijm1]+2.0*yeq[fkij]) // CCR
                    /sqrt(normf[j])
                    +(y[fkijp1]-y[fkijm1]-yeq[fkijp1]+yeq[fkijm1])/2.0
                    *(1.0/sqrt(normf[j+1])-1.0/sqrt(normf[j-1]))/2.0);
            }
        }
    }
                    
    for (i=1;i<N;++i) {
        mm = MAX(N-i,i);
        for (j=mm;j<N;++j) {
            f0ij = ind(0,i,j);
            f1ij = ind(1,i,j);
            f2ij = ind(2,i,j);
            // Shear Flow
            dy[f0ij]+=2*gdot*y[f1ij];
            dy[f1ij]+=gdot*y[f2ij];
        }
    }
    return 1;
}