/**
  *\file
  *\brief Return glassy contribution of G' and G" at given frequency
  */

#include "../include/LP2R.h"

// kww.c
// Wuttke, Algorithms 5, 604-628 (2012), doi:10.3390/a5040604
extern "C" {
double kwws(const double, const double); 
double kwwc(const double, const double);
           }


/**
  * Glassy contribution to G' and G" 
  *
  * Used kww.c from Wuttke, Algorithms 5, 604-628 (2012), doi:10.3390/a5040604
  *
  * \param[in] w frequency of interest
  * \param[out] gp Glassy contribution in storage modulus G'(w) 
  * \param[out] g2p Glassy contribution in loss modulus G"(w) 
  */

void GStarGlass(const double w, double &gp, double &g2p)
{
using namespace LP2R_NS;

double omega=w*tau_glass;
gp=G_glass*omega*kwws(omega,beta_glass);
g2p=G_glass*omega*kwwc(omega,beta_glass);
}

