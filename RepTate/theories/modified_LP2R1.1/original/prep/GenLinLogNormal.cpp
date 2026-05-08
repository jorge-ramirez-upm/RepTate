#include "../include/LP2R.h"
/** \file
  * \brief Generate discrete representation of a logNormal distribution
  */


/**
  * Weight fraction in a specified molar mass range from a logNormal distribution
  * \param[in] Mw weight-averaged molar mass 
  * \param[in] PDI Polydispersity index
  * \param[in] M1 Lower limit of the molar mass range 
  * \param[in] M2 upper limit of the molar mass range
  * \param[out] MwBin weight averaged molar mass in this interval
  * \return weight fraction in the molar mass range.
  *
  * Negative M1 ==> (0, M2); Negative M2 ==> (M1, infinity)
  */

double LogNormalWt(const double Mw, const double PDI, const double M1, const double M2, double &MwBin)
{
double mu=log(Mw) - 1.50*log(PDI);
double sigma=sqrt(log(PDI));
double WtBin;
if(M1 < 0.0){ // (0, M2)
WtBin=0.5*erfc( (mu + sigma*sigma - log(M2))/(sqrt(2.0)*sigma) );
double t2=erfc( (mu + 2.0*sigma*sigma - log(M2))/(sqrt(2.0)*sigma) );
MwBin=0.50*Mw*t2/WtBin;  // t1=erfc(infinity)=0
            }
else{
 if(M2 < 0.0){ // (M1, infinity)
  WtBin=1.0 - 0.5*erfc( (mu + sigma*sigma - log(M1))/(sqrt(2.0)*sigma) );
  double t1=erfc( (mu + 2.0*sigma*sigma - log(M1))/(sqrt(2.0)*sigma) );
  MwBin=0.50*Mw*(2.0 - t1)/WtBin;
             }
 else{ // (M1, M2)
    double w1=0.5*erfc( (mu + sigma*sigma - log(M1))/(sqrt(2.0)*sigma) );
    double w2=0.5*erfc( (mu + sigma*sigma - log(M2))/(sqrt(2.0)*sigma) );
    WtBin=w2-w1;
    double t1=erfc( (mu + 2.0*sigma*sigma - log(M1))/(sqrt(2.0)*sigma) );
    double t2=erfc( (mu + 2.0*sigma*sigma - log(M2))/(sqrt(2.0)*sigma) );
    MwBin=0.50*Mw*(t2 - t1)/WtBin;
     }
    }
return WtBin;
}

/**
  * Generate polymers from a logNormal distribution characterized by molar mass mw and PDI pdi.\n
  * Special case: if either the number of discrete molar mass is one or PDI < 1, create 
  * a single polymer with the molar mass supplied.
  * \param[in] n number of discrete molar mass to represent the distribution
  * \param[in] mw weight averaged molar mass
  * \param[in] pdi Polydispersity index
  * \param[in] wtcomp weight fraction of this polymer componennt
  */
void GenLinLogNormal(const int n, const double mw, const double pdi, const double wtcomp)
{
using namespace LP2R_NS;
if((n <=1) || (pdi <= 1.0)){
C_LPoly * ptmp=new C_LPoly(mw, wtcomp, M_e);
LPoly.push_back(ptmp); npoly++;
return;
                           }

C_LPoly * ptmp;
double mu=log(mw)-1.50*log(pdi);
double sigma=sqrt(log(pdi));
double lnMlow=mu + sigma*sigma-2.63*sqrt(2.0)*sigma;
double lnMhigh=mu + sigma*sigma+2.63*sqrt(2.0)*sigma;
double wtBin, MwBin, M1, M2;
M2=exp(lnMlow);
wtBin=LogNormalWt(mw, pdi, -1, M2, MwBin);
ptmp=new C_LPoly(MwBin, wtBin*wtcomp, M_e);
LPoly.push_back(ptmp); npoly++;

double delta_lnM=(lnMhigh-lnMlow)/((double) (n-2));
for(int i=0; i< (n-2); i++){
 M1=exp(lnMlow + ((double) (i))*delta_lnM);
 M2=exp(lnMlow + ((double) (i+1))*delta_lnM);
wtBin=LogNormalWt(mw, pdi, M1, M2, MwBin);
ptmp=new C_LPoly(MwBin, wtBin*wtcomp, M_e);
LPoly.push_back(ptmp); npoly++;
                           }
M1=exp(lnMhigh);
wtBin=LogNormalWt(mw, pdi, M1, -1, MwBin);
ptmp=new C_LPoly(MwBin, wtBin*wtcomp, M_e);
LPoly.push_back(ptmp); npoly++;

}
