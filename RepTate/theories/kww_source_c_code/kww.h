/* kww.h:
 *   Calculation of the Kohlrausch-Williams-Watts spectrum, i.e.
 *   Laplace-Fourier transform of the stretched exponential function exp(-t^b).
 *   Frequently used to describe relaxation in disordered systems.
 * 
 * Copyright:
 *   (C) 2009 Joachim Wuttke
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
 * Website:
 *   http://apps.jcns.fz-juelich.de/doku/sc/kww
 *
 * Reference:
 *   Wuttke, http://arxiv.org/abs/0911.4796
 */

#ifndef __KWW_H__
#define __KWW_H__
#undef __BEGIN_DECLS
#undef __END_DECLS
#ifdef __cplusplus
# define __BEGIN_DECLS extern "C" {
# define __END_DECLS }
#else
# define __BEGIN_DECLS /* empty */
# define __END_DECLS /* empty */
#endif
__BEGIN_DECLS

/*****************************************************************************/
/*  High-level calls                                                         */
/*****************************************************************************/

/* \int_0^\infty dt cos(w*t) exp(-t^beta) */
double kwwc( const double w, const double beta );

/* \int_0^\infty dt sin(w*t) exp(-t^beta) */
double kwws( const double w, const double beta );

/* \int_0^w dw' kwwc(w') */
double kwwp( const double w, const double beta );


/*****************************************************************************/
/*  Low-level calls                                                          */
/*****************************************************************************/

/* low-w expansion */
double kwwc_low( const double w, const double beta );
double kwws_low( const double w, const double beta );
double kwwp_low( const double w, const double beta );

/* high-w expansion */
double kwwc_hig( const double w, const double beta );
double kwws_hig( const double w, const double beta );
double kwwp_hig( const double w, const double beta );

/* mid-w integration */
double kwwc_mid( const double w, const double beta );
double kwws_mid( const double w, const double beta );
double kwwp_mid( const double w, const double beta );

__END_DECLS
#endif /* __KWW_H__ */
