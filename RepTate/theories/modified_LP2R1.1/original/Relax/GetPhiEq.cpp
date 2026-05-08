#include "../include/LP2R.h"
/** 
  * \file
  * \brief
  * Tube diameter for CLF (phi_eq)
  *
  * When a certain tube will be accessible for CLF is stored in \c t_eq_ar as that information is
  * aquired. Always, this time is in the future. This routine interpolates the stored values to
  * return the tube diameter relevant for CLF at the current time.
  */

double GetPhiEq(void)
{
using namespace LP2R_NS;
double phi_eq1=1.0;
std::size_t n1=phi_eq_indx;
if(cur_time < 1){ // no interpolation
 while ( (n1 < t_eq_ar.size()) && (cur_time > t_eq_ar[n1])){ n1++;}
 if(n1 > 0){n1=n1-1;}
 phi_eq_indx=n1;
                }
else{
 while ( (n1 < t_eq_ar.size()) && (cur_time > t_eq_ar[n1])){ n1++;}
 if(n1 > 0){n1=n1-1;}
 phi_eq_indx=n1;
if(n1 > 5){ // Avoid problem with having zero as time at the beginning
 phi_eq1=phi_ST_ar[n1];
 double deltat=cur_time - t_eq_ar[n1];
 if(deltat > 1.0e-6){ //guard against having negative in log from finite precision
phi_eq1 += (phi_ST_ar[n1+1] - phi_ST_ar[n1])*log(cur_time/t_eq_ar[n1])/Log_DtMult;
                    }
          }
  else{phi_eq1=1.0;}
    }
return phi_eq1;
}
