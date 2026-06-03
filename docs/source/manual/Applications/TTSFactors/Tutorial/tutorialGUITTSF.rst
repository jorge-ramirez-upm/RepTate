=========================
Tutorial TTSF Application
=========================

.. toctree::
   :maxdepth: 2

This short tutorial shows how to inspect time-temperature superposition shift
factors and compare them with the built-in WLF or Arrhenius theories.

Load Shift-Factor Data
----------------------

#.  Start RepTate and create a new TTS Factors application.

#.  Open a ``.ttsf`` file containing shift factors. The file should include the
    sample molar mass ``Mw`` as a file parameter and three data columns:
    temperature ``T`` in degrees Celsius, horizontal shift factor ``aT``, and
    vertical shift factor ``bT``.

Inspect Views
-------------

Use the ``View`` selector to switch between the shift-factor representations:

* ``log(aT)`` plots :math:`\log_{10}(a_T)` against temperature.
* ``aT`` plots the horizontal shift factor against temperature with a
  logarithmic vertical axis.
* ``log(bT)`` and ``bT`` show the corresponding vertical shift factor.
* ``log(aT, bT)`` displays both logarithmic shift factors in the same plot.
* ``log(aT) vs 1/T`` plots :math:`\log_{10}(a_T)` against
  :math:`1/(T+273.15)`, which is useful when checking Arrhenius-like behavior.

The logarithmic views require positive ``aT`` or ``bT`` values.

Add a Shift-Factor Theory
-------------------------

#.  In the theory selector, choose ``WLF`` to compare the data with a
    Williams-Landel-Ferry shift law. The WLF calculation uses the file parameter
    ``Mw`` and theory parameters such as ``Tr``, ``B1``, ``B2``, ``logalpha``,
    and ``CTg``.

#.  Click ``Calculate`` to evaluate the current theory parameters. Use
    ``Minimize Error`` only when you want RepTate to fit the adjustable WLF
    parameters to the loaded shift-factor data.

#.  For a single-file Arrhenius check, choose ``ArrheniusTheory`` instead. This
    theory calculates ``aT`` from the reference temperature ``Tref`` and
    activation energy ``Ea``.
