#ifndef _LinLin_H_
#define _LinLin_H_
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>

/**
  *\file
  *\brief Define classes and namespaces
  */

/**
  * Agreegate class to hold information about a linear polymer
  */

class C_LPoly{
public:
C_LPoly()=default;
C_LPoly(const double M, const double W, const double  M_e) :
 mass(M), wt(W), Z_chain(M/M_e), t_FRouse(Z_chain*Z_chain) {}

double mass=0.0; /**< molar mass of the polymer (g/mole) */
double wt=0.0; /**< Weight fraction associated with the polymer in the ensemble */
double Z_chain=0.0; /**< Number of entanglements in the chain. Z_chain=mass/M_e */
double z=0.0; /**< Escaped number of entanglements from either ends of the chain at current time */

bool alive=true; /**< Becomes false if the chain completely relaxes */
bool relax_free_Rouse=false; /**< True for unentangled chains */

bool rept_set=false; /**< Becomes true once further relaxation is assigned tobe via reptation */
double tau_d_0=1.0e22; /**< Reptation time for the zeroth mode; initialized to a large number */
double Z_rept=0.0; /**< Amount of chain that should relax by reptation */
double rept_wt=0.0; /**< Weight associated with reptation */
int p_max=0; /**< Highest reptation mode */
int p_next=0; /**< Next available reptation mode */

double t_FRouse; /**< Relaxation time by free Rouse relaxation (Z_chain^2) tau_e */
             };


/**
  * \brief Class to hold and retrieve partial sums of the form 1/p^2 \n
  *
  * Explicitly sum 1/p^2 till 1/499^2  \n
  * Higher terms are added as integrals as required. \n
  * Function call operator is overloaded to return partial sums
  */

class InvSqSum{ // sum(1/p^2)
double psum[500];
public:
  InvSqSum(){
   psum[0]=0.0; psum[1]=1.0;
   for(int i=2; i<500; i++){psum[i]=psum[i-1]+1.0/((double) (i*i));}
            }
  double intg_psum(int n1, int n2){
   double n1d=((double) n1); double n2d=((double) n2);
   double n1dsq=n1d*n1d; double n2dsq=n2d*n2d;
   double val=1.0/n1d - 1.0/n2d + 0.50*(1.0/n1dsq + 1.0/n2dsq);
     val+=(1.0/(n1d*n1dsq) - 1.0/(n2d*n2dsq))/6.0;
     return val;
                                  }
   double operator()(int Z){
     if(Z < 500){return psum[Z];}
     else{ return psum[499]+intg_psum(500,Z);}
                        }
   double operator()(int Z1, int Z2){
      double s1, s2;
      if(Z1 <= 500){s1=psum[Z1-1];}
      else{s1=psum[499]+intg_psum(500,Z1-1);}
      if(Z2 < 500){s2=psum[Z2];}
      else{s2=psum[499]+intg_psum(500,Z2);}
      return s2-s1;
                                 }

              };

#include "./LP2R_NS.h"
#include "./routines.h"


#endif
