----------------------
Havriliak-Negami modes
----------------------

.. toctree::
   :maxdepth: 2

Summary
-------

.. automodule:: RepTate.theories.TheoryHavriliakNegamiModes.TheoryHavriliakNegamiModesFrequency

Description
-----------

Fit dielectric spectroscopy data with a set of :math:`N` discrete
Havriliak-Negami modes. Each mode contributes a relaxation strength
:math:`\Delta\epsilon_i`, a characteristic time :math:`\tau_i`, and the common
shape parameters :math:`\alpha` and :math:`\gamma`.

The mode frequencies are equally distributed on a logarithmic scale between
a minimum frequency, :math:`\omega_\text{min}`, and a maximum frequency,
:math:`\omega_\text{max}`. RepTate stores these bounds as ``logwmin`` and
``logwmax`` and uses :math:`\tau_i=1/\omega_i`.

For a frequency :math:`\omega`, the implemented complex response is

.. math::

    \epsilon^*(\omega) =
        \epsilon_\infty +
        \sum_i
        \frac{\Delta\epsilon_i}
        {\left[1+\left(i\omega\tau_i\right)^\alpha\right]^\gamma}

The calculated :math:`\epsilon'` column is the real part of this response and
the calculated :math:`\epsilon''` column is minus the imaginary part, matching
the sign convention used in the implementation. The theory output keeps the
same frequency points as the input file.

The adjustable parameters exposed in the theory table are:

* ``einf``: unrelaxed permittivity, :math:`\epsilon_\infty`.
* ``alpha``: asymmetry parameter.
* ``gamma``: broadness parameter.
* ``logwmin`` and ``logwmax``: base-10 logarithms of the frequency range bounds,
  expressed in ``rad/s``.
* ``logDe00``, ``logDe01``, ...: base-10 logarithms of the mode strengths
  :math:`\Delta\epsilon_i`.

The number of modes, ``nmodes``, is controlled from the theory toolbar and is
not fitted directly. When the theory is created, the initial number of modes is
estimated from the frequency span of the data. The initial mode strengths are
interpolated from the first file in the data set. The ``View modes`` button
shows or hides the yellow mode markers; dragging the markers changes the
frequency range and mode strengths in the current view coordinates.

The Havriliak-Negami modes theory is available in the Dielectric application as
``Havriliak-Negami modes`` and is intended for ``.dls`` dielectric spectroscopy
files with columns :math:`\omega`, :math:`\epsilon'`, and
:math:`\epsilon''`.

.. warning::
    The theory can only be applied to one file per data set. 
    If more than one file is active in the current data set,
    the theory will be applied to the first one in the list of active files.




