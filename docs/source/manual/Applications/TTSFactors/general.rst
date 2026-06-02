=======================================
TTS Shift Factors: General description
=======================================

.. contents:: Contents
    :local:

..	toctree::
   	:maxdepth: 2

-------
Purpose
-------

.. automodule:: RepTate.applications.ApplicationTTSFactors.ApplicationTTSFactors

The TTS Factors application provides views for checking horizontal and vertical
shift factors as functions of temperature. The input data are the three columns
of a ``.ttsf`` file: temperature, :math:`a_T`, and :math:`b_T`. The temperature
column is read in degrees Celsius; views that use inverse temperature convert it
internally to Kelvin before calculating :math:`1/T`.


----------
Data Files
----------

.. include:: ../datafile_doc.rst


``.ttsf`` extension
-------------------

Text files with ``.ttsf`` extension should be organised as follows:

- ``.ttsf`` files should contaion **at least** the parameter value for the:

  #. sample molar mass ``Mw``,

- 3 columns separated by **spaces** or **tabs** containing respectively:

  #. Temperature in degree Celcius
  #. Horizontal shift factor, aT
  #. Vertical shift factor, bT

Other columns will be ingnored. A correct ``.ttsf`` file looks like:

.. code-block:: none

    Mw=1131.0;chem=PI;origin=LeedsDA;label=PI1000k-02_FS_PP10;PDI=1.05;
    T            aT           bT         
    [°C]         [-]          [-]     
    -40          1936.91      1.14298
    -30          146.777      1.10282
    -20          19.4248      1.06584
    ...          ...          ...

-----
Views
-----

Log(aT)
-------------------------------------------
.. automethod:: RepTate.applications.ApplicationTTSFactors.ApplicationTTSFactors.viewLogaT()
   
aT
-------------------------------------------
.. automethod:: RepTate.applications.ApplicationTTSFactors.ApplicationTTSFactors.viewaT()
   
Use ``Log(aT)`` or ``aT`` to inspect the horizontal shift factor alone. The
``Log(aT)`` view plots :math:`\log_{10}(a_T)` against temperature on linear
axes, while ``aT`` plots :math:`a_T` against temperature with a logarithmic
vertical axis.


Log(bT)
-------------------------------------------
.. automethod:: RepTate.applications.ApplicationTTSFactors.ApplicationTTSFactors.viewLogbT()
   
bT
-------------------------------------------
.. automethod:: RepTate.applications.ApplicationTTSFactors.ApplicationTTSFactors.viewbT()

Use ``Log(bT)`` or ``bT`` to inspect the vertical shift factor alone. These
views follow the same convention as the horizontal shift-factor views:
``Log(bT)`` plots :math:`\log_{10}(b_T)` on linear axes, and ``bT`` plots
:math:`b_T` with a logarithmic vertical axis.


Log(aT, bT)
-------------------------------------------
.. automethod:: RepTate.applications.ApplicationTTSFactors.ApplicationTTSFactors.viewLogaTbT()

Use ``Log(aT, bT)`` when both shift factors need to be compared in the same
plot. It displays :math:`\log_{10}(a_T)` and :math:`\log_{10}(b_T)` against the
same temperature values.

Log(aT) vs 1/T (Kelvin)
-------------------------------------------
.. automethod:: RepTate.applications.ApplicationTTSFactors.ApplicationTTSFactors.viewLogaT_invT()
   
Use ``Log(aT) vs 1/T`` for Arrhenius-type checks of the horizontal shift factor.
This view plots :math:`\log_{10}(a_T)` against :math:`1/(T+273.15)`, with
:math:`T` taken from the temperature column in degrees Celsius.

Because the logarithmic views calculate base-10 logarithms of the shift factors,
the corresponding :math:`a_T` or :math:`b_T` values must be positive.
