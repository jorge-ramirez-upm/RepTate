-------------------------------------
Debye modes (independent times)
-------------------------------------

.. automodule:: RepTate.theories.TheoryDebyeModesIndependent.TheoryDebyeModesIndependent

Description
-----------

This theory fits independent Debye relaxation modes. Each mode has its own
relaxation time :math:`\tau_i` and strength :math:`\Delta\epsilon_i`:

.. math::

    \epsilon' &= \epsilon_\infty + \sum_i
        \frac{\Delta\epsilon_i}{1+(\omega\tau_i)^2} \\
    \epsilon'' &= \sum_i
        \frac{\Delta\epsilon_i\omega\tau_i}{1+(\omega\tau_i)^2}.

The mode toolbar provides independent dragging, loading, saving, deletion,
and conservative simplification of the spectrum.

The theory is available as ``Debye modes (independent)``.
