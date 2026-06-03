==========================
Tutorial Creep Application
==========================

.. toctree::
   :maxdepth: 2

This short tutorial shows how to load the bundled creep examples and inspect the
main creep-compliance views. It does not require fitting a theory.

Load Creep Data
---------------

#.  Start RepTate and create a new Creep application.

#.  Open one of the example files in ``data/Creep``:

    * ``Maxwell.creep``
    * ``CM3_Creep.creep``
    * ``CM3_CreepRecovery.creep``

    The Creep application reads text files with the ``.creep`` extension. The
    file parameters include the applied ``stress`` and may also include
    parameters such as ``Mw`` and ``T``. The data columns used by the application
    are time ``t`` and strain ``strain``.

Inspect Views
-------------

Use the ``View`` selector to switch between the creep representations:

* ``gamma(t)`` plots the measured strain as a function of time.
* ``log(gamma(t))`` plots ``log10(t)`` against ``log10(abs(gamma))``.
* ``J(t)`` plots the creep compliance, calculated as
  :math:`J(t)=\gamma(t)/\sigma_0`, where :math:`\sigma_0` is the applied
  ``stress`` file parameter.
* ``log(J(t))`` shows the same compliance on logarithmic transformed axes.
* ``t/J(t)`` plots time divided by compliance, which is useful for inspecting
  the approach to steady viscosity.

The ``i-Rheo`` views transform the compliance data to obtain
:math:`G'(\omega)` and :math:`G''(\omega)`. When one of these views is selected,
RepTate shows extra controls for the steady-state viscosity and the time range
used by the transformation; the oversampled i-Rheo view also shows the
oversampling control.

Fit retardation modes
---------------------

#.  Select a single creep data file in the data set. The ``Retardation Modes``
    theory is initialized from the first active file, so keep only the file you
    want to fit active when setting up the theory.

#.  In the theory selector, choose ``Retardation Modes`` and create the theory.
    The initial modes are distributed logarithmically between the smallest
    positive time and the largest time in the selected file.

#.  Use the mode spinbox in the theory toolbar to change the number of modes.
    The theory documentation recommends roughly one mode per decade as a useful
    starting point for modes intended for flow simulations.

#.  Click ``Calculate`` to evaluate the current parameters, or ``Minimize Error``
    to fit the instantaneous compliance ``logJini``, terminal viscosity
    ``logeta0``, the time range ``logtmin``/``logtmax``, and the mode compliance
    values ``logJ00``, ``logJ01``, etc.

#.  When the mode markers are visible, drag the yellow points to adjust the mode
    compliances. Dragging the leftmost and rightmost modes changes the fitted
    time range.
