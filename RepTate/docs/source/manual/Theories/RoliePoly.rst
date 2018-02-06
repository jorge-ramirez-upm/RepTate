========================
Rolie-Poly equation
========================

.. toctree::
   :maxdepth: 2

The Rolie-Poly (\ **RO**\ use **LI**\ near **E**\ ntangled **POLY**\ mers) [Likhtman2003]_ constitutive 
equation is a single mode formulation of the full microscopic model [Graham2003]_
for linear entangled polymer chains with chain stretch and convective constraint release.

The equations solved by RepTate, for every stretching mode is:

.. math::
    \dfrac{\text d \boldsymbol{\sigma}}{\text dt} = \boldsymbol{\kappa}\cdot\boldsymbol{\sigma
    }+ \boldsymbol{\sigma}\cdot\boldsymbol{\kappa}^{T} - \dfrac{1}{\tau_\mathrm{d}}
    (\boldsymbol{\sigma}- \boldsymbol{I}) - \dfrac{2(1 - \sqrt{3/\mathrm{tr}\,
    \boldsymbol{\sigma}})}{\tau_\mathrm{R}} \left(  \boldsymbol{\sigma}+ \beta\left(
    \dfrac{\mathrm{tr}\, \boldsymbol{\sigma}}{3} \right) ^{\delta}(\boldsymbol{\sigma
    }- \boldsymbol{I}) \right),

and, for non-stretching modes, the equation for each mode is:

.. math::
    \dfrac{\text d \boldsymbol{\sigma}}{\text dt} = \boldsymbol{\kappa}\cdot\boldsymbol{\sigma
    }+ \boldsymbol{\sigma}\cdot\boldsymbol{\kappa}^{T} - \dfrac{1}{\tau_\mathrm{d}}
    (\boldsymbol{\sigma}- \boldsymbol{I}) - \dfrac{2}{3} \mathrm{tr}
    (\boldsymbol{\kappa}\cdot\boldsymbol{\sigma}) \big(\boldsymbol{\sigma}+
    \beta(\boldsymbol{\sigma}- \boldsymbol{I}) \big).





.. rubric:: References

.. [Likhtman2003] Likhtman, A. L. and R. S. Graham, *Simple
    constitutive equation for linear polymer melts derived from molecular theory:
    Rolie-Poly equation*, `J. Non-Newtonian Fluid Mech. 
    <https://doi.org/10.1016/S0377-0257(03)00114-9>`_, **114**, 1--12, 2003.

.. [Graham2003] Graham, R. S., A. E. Likhtman and T. C. B. McLeish, *Microscopic theory of linear, 
    entangled polymer chains under rapid deformation including chain stretch and convective constraint release*,
    `J. Rheol. 
    <https://doi.org/10.1122/1.1595099>`_, **47**, 1171--1200, 2003.