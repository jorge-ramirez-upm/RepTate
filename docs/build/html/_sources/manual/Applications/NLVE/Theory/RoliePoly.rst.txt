.. _RoliePoly_equation-label:

-------------------
Rolie-Poly equation
-------------------

.. toctree::
   :maxdepth: 2

"Classic" Rolie-Poly model
--------------------------

The Rolie-Poly (\ **RO**\ use **LI**\ near **E**\ ntangled **POLY**\ mers) :cite:`NLVE-Likhtman2003` constitutive 
equation is a single mode formulation of the full microscopic model :cite:`NLVE-Graham2003`
for linear entangled polymer chains with chain stretch and convective constraint release.

The evolution equations for the conformation tensor, :math:`\boldsymbol{A}`, solved by RepTate for every stretching mode is:

.. math::
    \dfrac{\text D \boldsymbol{A}}{\text Dt} = \boldsymbol{\kappa}\cdot\boldsymbol{A
    }+ \boldsymbol{A}\cdot\boldsymbol{\kappa}^{T} - \dfrac{1}{\tau_\mathrm{d}}
    (\boldsymbol{A}- \boldsymbol{I}) - \dfrac{2(1 - \lambda^{-1})}{\tau_\mathrm{R}} \left(  \boldsymbol{A}+ \beta \lambda^{2\delta}(\boldsymbol{A
    }- \boldsymbol{I}) \right),

    
where the stretch ratio, :math:`\lambda`, is 

.. math::
    \lambda = \left( \frac 1 3 \text{tr}\, \boldsymbol{A} \right)^{1/2}

and, for non-stretching modes, the equation for each mode is:

.. math::
    \dfrac{\text D \boldsymbol{A}}{\text Dt} = \boldsymbol{\kappa}\cdot\boldsymbol{A
    }+ \boldsymbol{A}\cdot\boldsymbol{\kappa}^{T} - \dfrac{1}{\tau_\mathrm{d}}
    (\boldsymbol{A}- \boldsymbol{I}) - \dfrac{2}{3} \mathrm{tr}
    (\boldsymbol{\kappa}\cdot\boldsymbol{A}) \big(\boldsymbol{A}+
    \beta(\boldsymbol{A}- \boldsymbol{I}) \big).
    :label: non-stretching

Given :math:`n` modes :math:`(G_i, \tau_{\mathrm d, i}, \tau_{\mathrm R, i})`, the total stress is calculated as

.. math::
    \boldsymbol{\sigma}(t) = \sum_{i=1}^n G_i\, \boldsymbol{A}_i

Finite extensibility
--------------------

A non-Gaussian version of the Rolie–Poly constitutive equation, which accounts
for finite extensibility of polymer chains, can be written in the following form

.. math::
    \dfrac{\text D \boldsymbol{A}}{\text Dt} = \boldsymbol{\kappa}\cdot\boldsymbol{A
    }+ \boldsymbol{A}\cdot\boldsymbol{\kappa}^{T} - \dfrac{1}{\tau_\mathrm{d}}
    (\boldsymbol{A}- \boldsymbol{I}) - \dfrac{2(1 - \lambda^{-1})}{\tau_\mathrm{R}} 
    \text{fene}(\lambda) \left( \boldsymbol{A}+ \beta \lambda^{2\delta}(\boldsymbol{A
    }- \boldsymbol{I}) \right),

The nonlinear spring coefficient, :math:`\text{fene}(\lambda)`, is
approximated by the normalized Padé inverse Langevin function :cite:`NLVE-Cohen1991`

.. math::
   \text{fene}(\lambda) = \dfrac{3 - \lambda^2/\lambda_\text{max}^2}{1 - \lambda^2/\lambda_\text{max}^2}
   \dfrac{1 - 1/\lambda_\text{max}^2}{3 - 1/\lambda_\text{max}^2},
    
   
where :math:`\lambda_\text{max}` is the fixed maximum stretch ratio.

Given :math:`n` modes :math:`(G_i, \tau_{\mathrm d, i}, \tau_{\mathrm R, i})`, the total stress is calculated as

.. math::
    \boldsymbol{\sigma}(t) = \sum_{i=1}^n G_i\,  \text{fene}(\lambda_i)\, \boldsymbol{A}_i

with :math:`\lambda_i = \left( \frac 1 3 \text{tr}\,\boldsymbol{A}_i \right)^{1/2}`.

