/**
  * \file
  * \brief Internal Rouse and longitudinal modes (in units of G0)
  * \param [in] w Frequency
  * \param [out] gpf Internal Rouse and longitudinal mode contribution to G'
  * \param [out] g2pf Internal Rouse and longitudinal mode contribution to G"
  */
#include "../include/LP2R.h"
void GStarFastRouse(const double w, double &gpf, double &g2pf)
{
using namespace LP2R_NS;

gpf=g2pf=0.0;

double gp,g2p,tv,tv2,tv4;
double w2=w*w;
int zi=1;

for(int i1=0; i1<npoly; i1++){
if(!LPoly[i1]->relax_free_Rouse){
double zz=LPoly[i1]->Z_chain;
zi=(int) ceil(zz);
gp=g2p=0.0;
  
  for(int i=1; i<zi; i++){ // longitudinal contribution
      tv=(double)i/zz; tv2=tv*tv; tv4=tv2*tv2;
      gp+=1.0/(w2 + tv4); // multiply by w^2/(4*Z) later
      g2p+=tv2/(w2 + tv4); 
                         }

  int max_term=(int)ceil(N_e * zz);
  for(int i=zi; i<max_term; i++){ // internal Rouse modes
      tv=(double)i/zz; tv2=tv*tv; tv4=tv2*tv2;
      tv=1.0/(w2 + 4.0*tv4);
      gp+=5.0*tv;
      g2p+=10.0*tv2*tv;
                                }
gpf+=w2*gp*LPoly[i1]->wt /(4.0*zz);
g2pf+=w*g2p *LPoly[i1]->wt/(4.0*zz);

                               }
                             }
}
