-----------------------
Maxwell modes 
-----------------------

.. toctree::
   :maxdepth: 2

Summary
-------

.. automodule:: RepTate.theories.TheoryMaxwellModes.TheoryMaxwellModesTime()

Description
-----------
      
Fit of step strain + relaxation data with a set of :math:`N` discrete Maxwell modes. 
The number of modes can be selected by pressing the Up/Down arrows in the theory window. 
The relaxation times of the Maxwell modes are equally distributed in logarithmic scale between 
a minimum time, :math:`t_\text{min}`, and a maximum time, :math:`t_\text{max}`,
which can be fixed or set free by ticking the corresponding checkboxes. 
The position of :math:`t_\text{min}` and :math:`t_\text{max}` 
can be changed by dragging the leftmost and rightmost modes with the mouse.
The vertical position of the modes can be changed by dragging the yellow points.

Each mode contributes to the relaxation modulus through the following formulas:

.. math::
    G_i(t) = G_i \exp (-t/\tau_i) 

with :math:`G_i` the modulus and :math:`\tau_i` the characteristic relaxation time of 
the mode :math:`i` (inverse of the frequency). 

The parameters of the theory are the number of modes (which is fixed by the user and 
is not minimized), :math:`t_\text{min}`, :math:`t_\text{max}`,
and a value of :math:`G_i` for each mode. 
:math:`G_i` is calculated in logarithmic scale.

.. warning::
    The theory can only be applied to one file per data set. 
    If more than one file is active in the current data set,
    the theory will be applied to the first one in the list of active files.

.. note::
    *   Roughly one mode per decade should be enough for the purpose of using the modes 
        in flow simulations.
    *   Also for flow simulations, do not use modes much faster than the fastest flow rate in the simulation.




