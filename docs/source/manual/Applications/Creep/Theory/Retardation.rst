-----------------------
Retardation modes 
-----------------------

.. toctree::
   :maxdepth: 2

Summary
-------

.. automodule:: RepTate.theories.TheoryRetardationModes.TheoryRetardationModesTime

Description
-----------
      
Fit of creep experimental data with a set of :math:`N` discrete equidistant Retardation modes. 
The number of modes can be selected by pressing the Up/Down arrows in the theory window. 
The relaxation times of the Retardation modes are equally distributed in logarithmic scale between 
a minimum time, :math:`t_\text{min}`, and a maximum time, :math:`t_\text{max}`,
which can be fixed or set free by ticking the corresponding checkboxes. 
The position of :math:`t_\text{min}` and :math:`t_\text{max}` 
can be changed by dragging the leftmost and rightmost modes with the mouse.
The vertical position of the modes can be changed by dragging the yellow points.

Each mode contributes to the material compliance through the following formula:

.. math::
    J_i(t) = J_i \left[ 1 - \exp\left(\frac{-t}{\tau_i}\right) \right]

with :math:`J_i` the compliance and :math:`\tau_i` the characteristic relaxation time of 
the mode :math:`i` (inverse of the frequency). 

In addition to the contribution of the retardation modes, there is contribution from an instantaneous compliance :math:`J_0` (given by the parameter ``logJini`` = :math:`\log(J_0)`) and a contribution from the terminal viscosity of the material :math:`t/\eta_0` (given by the parameter ``logeta0`` = :math:`\log(\eta_0)`). 

The parameters of the theory are the number of modes (which is fixed by the user and 
is not minimized), :math:`t_\text{min}`, :math:`t_\text{max}`, a value of :math:`J_i` for each mode (in logarithmic scale), and the values of :math:`J_0` and :math:`\eta_0`.

.. warning::
    The theory can only be applied to one file per data set. 
    If more than one file is active in the current data set,
    the theory will be applied to the first one in the list of active files.

.. note::
    *   Roughly one mode per decade should be enough for the purpose of using the modes 
        in flow simulations.
    *   Also for flow simulations, do not use modes much faster than the fastest flow rate in the simulation.




