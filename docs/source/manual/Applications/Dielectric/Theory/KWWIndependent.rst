----------------------------------
KWW modes (independent times)
----------------------------------

.. automodule:: RepTate.theories.TheoryKWWModesIndependent.TheoryKWWModesIndependent

Description
-----------

This theory fits dielectric spectroscopy data with independent KWW modes:

.. math::

    \epsilon'(\omega) &= \epsilon_\infty +
        \sum_i \Delta\epsilon_i K_c(\omega\tau_i,\beta) \\
    \epsilon''(\omega) &=
        \sum_i \Delta\epsilon_i K_s(\omega\tau_i,\beta)

The common stretching exponent :math:`\beta` is fitted together with the
independent relaxation times :math:`\tau_i` and strengths
:math:`\Delta\epsilon_i`. The mode toolbar provides the same loading,
dragging, deletion, and conservative simplification controls as the
Baumgaertel-Winter spectrum theory.

Unlike the standard ``KWW modes`` theory, the mode times are not constrained
to an equally spaced logarithmic frequency grid.

The theory is available in the Dielectric application as
``KWW modes (independent)``.

.. warning::
    The theory can only be applied to one file per data set.
