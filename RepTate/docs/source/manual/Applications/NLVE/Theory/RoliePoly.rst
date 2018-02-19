-------------------
Rolie-Poly equation
-------------------

.. toctree::
   :maxdepth: 2

The Rolie-Poly (\ **RO**\ use **LI**\ near **E**\ ntangled **POLY**\ mers) :cite:`RP-Likhtman2003` constitutive 
equation is a single mode formulation of the full microscopic model :cite:`RP-Graham2003`
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

.. bibliography:: ../bibliography.bib
    :style: unsrt
    :keyprefix: RP-