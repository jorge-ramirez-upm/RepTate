-----------------------
Maxwell modes 
-----------------------

.. toctree::
   :maxdepth: 2

Summary
-------

.. autoclass:: TheoryMaxwellModes.TheoryMaxwellModesFrequency

Description
-----------
      
Fit of linear viscoelastic data with a set of :math:`N` discrete equidistant Maxwell modes. 
The number of modes can be selected by pressing the Up/Down arrows in the theory window. 
The frequencies of the Maxwell modes are equally distributed in logarithmic scale between 
a minimum frequency, :math:`\omega_\text{min}`, and a maximum frequency, :math:`\omega_\text{max}`,
which can be fixed or set free by ticking the corresponding checkboxes. 
The position of :math:`\omega_\text{min}` and :math:`\omega_\text{max}` 
can be changed by dragging the green bars with the mouse. 
The vertical position of the modes can be changed by dragging the yellow points.

Each mode contributes to the linear viscoelastic spectrum through the following formulas:

.. math::
    G_i'(\omega) &= G_i \frac{(\omega \tau_i)^2}{1+ (\omega \tau_i)^2}\\
    G_i''(\omega) &= G_i \frac{\omega \tau_i}{1+ (\omega \tau_i)^2}

with :math:`G_i` the modulus and :math:`\tau_i` the characteristic relaxation time of 
the mode :math:`i` (inverse of the frequency). 

The parameters of the theory are the number of modes (which is fixed by the user and 
is not minimized), :math:`\omega_\text{min}`, :math:`\omega_\text{max}`,
and a value of :math:`G_i` for each mode. 
:math:`G_i` is calculated in logarithmic scale.

.. By pressing the red button at the right of the number of Maxwell modes, we can add some 
.. fixed Maxwell modes that will not be modified during minimization.

.. warning::
    The theory can only be applied to one file per data set. 
    If more than one file is active in the current data set,
    the theory will be applied to the first one in the list of active files.

.. note::
    *   Roughly one mode per decade should be enough for the purpose of using the modes 
        in flow simulations.
    *   Also for flow simulations, do not use modes much faster than the fastest flow rate in the simulation.
    *   For linear polymers, one mode close to the crossing point of :math:`G'` and :math:`G''`
        should be enough to fit the terminal time.




