-------------------------------------
Kohlrausch-Williams-Watts (KWW) modes
-------------------------------------

.. toctree::
   :maxdepth: 2

Summary
-------

.. automodule:: RepTate.theories.TheoryKWWModes.TheoryKWWModesFrequency

Description
-----------

Fit dielectric spectroscopy data with a set of :math:`N` discrete
Kohlrausch-Williams-Watts modes. Each mode is a Laplace-Fourier transform of 
a stretched-exponential
relaxation contribution with a relaxation strength :math:`\Delta\epsilon_i`,
a characteristic time :math:`\tau_i`, and a common stretching exponent
:math:`\beta`.

The mode frequencies are equally distributed on a logarithmic scale between
a minimum frequency, :math:`\omega_\text{min}`, and a maximum frequency,
:math:`\omega_\text{max}`. RepTate stores these bounds as ``logwmin`` and
``logwmax`` and uses :math:`\tau_i=1/\omega_i`.

For a frequency :math:`\omega`, the implemented frequency-domain response is
calculated as

.. math::

    \epsilon'(\omega) &= \epsilon_\infty
        + \sum_i \Delta\epsilon_i\,K_c(\omega\tau_i,\beta)\\
    \epsilon''(\omega) &=
        \sum_i \Delta\epsilon_i\,K_s(\omega\tau_i,\beta)

where :math:`K_c` and :math:`K_s` are the cosine and sine KWW transform
functions evaluated by the bundled ``libkww`` library. The theory output keeps
the same frequency points as the input file and fills the calculated
:math:`\epsilon'` and :math:`\epsilon''` columns.

The adjustable parameters exposed in the theory table are:

* ``einf``: unrelaxed permittivity, :math:`\epsilon_\infty`.
* ``beta``: stretched-exponential parameter, limited in the source to the range
  0.1 to 2.0.
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

The KWW modes theory is available in the Dielectric application as
``KWW modes`` and is intended for ``.dls`` dielectric spectroscopy files with
columns :math:`\omega`, :math:`\epsilon'`, and :math:`\epsilon''`.

.. warning::
    The theory can only be applied to one file per data set. 
    If more than one file is active in the current data set,
    the theory will be applied to the first one in the list of active files.




