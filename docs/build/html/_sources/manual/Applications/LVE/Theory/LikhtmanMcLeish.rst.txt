-----------------------
Likhtman-McLeish theory
-----------------------

.. toctree::
   :maxdepth: 2

Summary
-------

.. autoclass:: TheoryLikhtmanMcLeish2002.TheoryLikhtmanMcLeish2002()
   
Description
-----------

Full quantitative theory for the linear dynamics of entangled linear polymers, based on the tube model and considering contour length fluctuations, constraint release and longitudinal stress relaxation along the tube. 

The parameter :math:`c_\nu` is related to the number of chains that are needed to create one entanglement. :math:`c_\nu=0` means there is no constraint release. The recommended value is :math:`c_\nu=0.1`. This value gives slightly worse fitting than :math:`c_\nu=1`, but is more consistent with start-up shear experiments.

For full details about how the predictions are calculated, refer to :cite:`LM-Likhtman2002`. A set of predictions has been precalculated and stored in binary form in the RepTate distribution. There are predictions for different values of :math:`Z=M_w/M_e` = 2, 3, 4 ... 299, 300, 305, 310, ... 1000, and :math:`c_\nu` = 0, 0.01, 0.03, 0.1, 0.3, 1, 3, 10. The molecular weight of the sample is read from the data file. For values of :math:`Z` and :math:`c_\nu` in the precalculated range, RepTate reads the prediction directly from the precalculated data. For other values of :math:`Z` and :math:`c_\nu`, the prediction is interpolated. 

After the calculation is done, the values of the number of entanglements :math:`Z`, the Rouse time :math:`\tau_R` and the reptation time :math:`\tau_D` of the polymer are printed in the Log Window. These values are calculated according to the following formulas:

.. math::
    \tau_R = \tau_e Z^2
    
.. math::
    \tau_D = 3\tau_e Z^3 \left( 1 - \frac{2C_1}{\sqrt{Z}} + \frac{C_2}{Z} + \frac{C_3}{Z^{3/2}} \right)
    
with the constants :math:`C_1=1.69`, :math:`C_2=4.17` and :math:`C_3=-1.55`.

Recommendations
---------------

- The theory is able to fit several molecular weight samples of the same polymer at the same time. That is the recommended procedure to get the material parameters :math:`\tau_e`, :math:`G_e` and :math:`M_e`.

- The theory allows the user to link the values of :math:`G_e` and :math:`M_e` through the density :math:`\rho` (in g/cm3) by means of the standard expression:

.. math::
    G_e = \frac{1000\rho R T}{M_e}

The user must input the correct density. If available, :math:`\rho` is read from the Materials database. The theory fails to fit correctly the data when the values of :math:`G_e` and :math:`M_e` are linked in this way.    

.. rubric:: References

.. bibliography:: ../bibliography.bib
    :style: unsrt
    :keyprefix: LM-
    