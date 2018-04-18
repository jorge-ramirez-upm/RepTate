-----------------------
Kolhrauch-Williams-Watts (KWW) modes 
-----------------------

.. toctree::
   :maxdepth: 2

Summary
-------

.. autoclass:: TheoryKWWModes.TheoryKWWModesFrequency()

Description
-----------

.. warning::
    NEEDS TO BE WRITTEN!
      
Fit of dielectric spectroscopy data with a set of :math:`N` discrete equidistant Debye modes. 
The number of modes can be selected by pressing the Up/Down arrows in the theory window. 
The frequencies of the Debye modes are equally distributed in logarithmic scale between 
a minimum frequency, :math:`\omega_\text{min}`, and a maximum frequency, :math:`\omega_\text{max}`,
which can be fixed or set free by ticking the corresponding checkboxes. 
The position of :math:`\omega_\text{min}` and :math:`\omega_\text{max}` 
can be changed by dragging the leftmost and rightmost modes with the mouse. 
The vertical position of the modes can be changed by dragging the yellow points.

Each mode contributes to the dielectric relaxation spectrum through the following formulas:

.. math::
    \epsilon_i'(\omega) &= \Delta\epsilon_i \frac{1}{1+ (\omega \tau_i)^2}\\
    \epsilon_i''(\omega) &= \Delta\epsilon_i \frac{\omega \tau_i}{1+ (\omega \tau_i)^2}

with :math:`\Delta\epsilon_i` the amplitude and :math:`\tau_i` the characteristic relaxation time of 
the mode :math:`i` (inverse of the frequency). 

The parameters of the theory are the number of modes (which is fixed by the user and 
is not minimized), :math:`\omega_\text{min}`, :math:`\omega_\text{max}`,
and a value of :math:`\Delta\epsilon_i` for each mode. 
:math:`\Delta\epsilon_i` is calculated in logarithmic scale.

.. warning::
    The theory can only be applied to one file per data set. 
    If more than one file is active in the current data set,
    the theory will be applied to the first one in the list of active files.




