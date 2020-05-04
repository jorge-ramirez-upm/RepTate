-----------------------
Carreau-Yasuda equation 
-----------------------

.. toctree::
   :maxdepth: 2

Summary
-------

.. autoclass:: RepTate.theories.TheoryCarreauYasuda.TheoryCarreauYasuda()
   
Description
-----------

Fit of the complex viscosity to the phenomenological Carreau-Yasuda equation. The equation used in the fit is:
   
.. math::
    \eta^*(\omega) = \eta_\infty + (\eta_0-\eta_\infty)\left( 1 + (\lambda\omega)^a \right)^{(n-1)/a}

In the equation, :math:`a` is a dimensionless parameter that describes the transition from the zero-shear rate region
to the power law region. It frequently takes the value 2. In some experimental data, it is safe to assume that :math:`\eta_\infty` is equal to zero.
    
.. warning::
    The fit only makes sense when applied using the ``logstar`` view (logarithm of the complex viscosity). The logarithm 
    is needed, due to the wide range of viscosity values.

.. warning::
    The theory can only be applied to one file per data set. 
    If more than one file is active in the current data set,
    the theory will be applied to the first one in the list of active files.
    