#include "../include/LP2R.h"

/**
  *\file
  *\brief Tube relaxation part of relaxation
  *
  * Given some frequency w, returns G'(w), G"(w), epsilon'(w), epsilon"(w)
  *
  * Assume G(t)/G_0 = mu(t) R(t), with mu and R determined by exponential
  * weighted integral of changes in phi and phi_ST
  *
  * R(t) is slowly relaxing. Extend R(t) to infinity analytically.
  *
  * Dielectric relaxation is considered to be proportional to mu(t)
  */


/**
  * \brief analytical result from extending R(t) to time infinity.
  *
  * \param[in] tk : discrete time interval at which contribution from the integral is sought.
  * \param[in] td : time at which mu(t) first goes to zero
  * \param[in] w : frequency
  * \param[out] rint1 : int( (a+x)/((a+x)^2 + b x^2) dx/sqrt(x), x=1..inf); I2(a,b) in Eqn B6 in the manuscript
  * \param[out] rint2 : int( sqrt(x)/((a+x)^2 + b x^2) dx, x=1..inf); I1(a,b) in Eqn B7 in the manuscript
  */

void symbint(const double tk, const double td, const double w, double &rint1, double &rint2)
{
double a=tk/td; double b=w*w*tk*tk;
double alpha=sqrt(1.0+b);
double beta=sqrt(1.0+alpha);
double gamma=sqrt(a*(alpha-1.0));
double delta=sqrt(a*(alpha+1.0));
double rt2=sqrt(2.0);

double t1=log((rt2*gamma + a + alpha)/(a+alpha - rt2*gamma));
double t2=atan(2.0*rt2*alpha*delta/(delta*delta + gamma*gamma - 2.0*alpha*alpha));

rint1=-gamma*beta*t1 - 2.0*sqrt(a)*(1.0+alpha)*t2;
rint2=beta*gamma*(1.0+alpha)*t1/b - 2.0*sqrt(a)*t2;
t1=1.0/(2.0*rt2*alpha*beta*a);
rint1*=t1;
rint2*=t1;
}


/**
  * \brief Calculate tube escape contrubution to relaxation moduli
  *
  *
  * \param[in] w : frequency at which result is required
  * \param[out] gp : elastic modulus G'
  * \param[out] g2p : viscous modulus G"
  * \param[out] ep : dielectric storage modulus epsilon'
  * \param[out] e2p : dielectric loss modulus epsilon"
  */
void GStarSlow(const double w, double &gp, double &g2p, double &ep, double &e2p)
{
using namespace LP2R_NS;
gp=g2p=ep=e2p=0.0;
double dphi, dphiST, tk, tm, tkm, tv;

double wsq=w*w;
int n=t_ar.size();

for(int k=1; k<n; k++){ // loop over phi
 dphi=phi_ar[k-1] - phi_ar[k]; tk=t_ar[k];
   for(int m=1; m<n; m++){ // loop over phi_ST
 dphiST=pow(phi_ST_ar[m-1], Alpha) -pow(phi_ST_ar[m], Alpha); tm=t_ar[m];
 tkm=tk*tm/(tk+tm);
 tv=tkm/(1.0 + wsq*tkm*tkm);
 gp+=tv*tkm*dphi*dphiST;
 g2p+=tv*dphi*dphiST;
                          }
double rint1, rint2;
symbint(tk,t_ar[n-1], w, rint1, rint2);
rint1*=0.50*pow(phi_ST_ar[n-1], Alpha);
rint2*=0.50*pow(phi_ST_ar[n-1], Alpha);
gp+=rint2*tk*tk*dphi;
g2p+=rint1*tk*dphi;
tv=tk/(1.0+wsq*tk*tk);
ep+=tv*tk*dphi;
e2p+=tv*dphi;
                      }
gp*=wsq; g2p*=w; ep*=wsq; e2p*=w;


}
