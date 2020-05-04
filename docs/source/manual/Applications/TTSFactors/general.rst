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

.. autoclass:: RepTate.applications.ApplicationTTSFactors.ApplicationTTSFactors()	

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
.. automethod:: RepTate.applications.ApplicationTTSFactors.BaseApplicationTTSFactors.viewLogaT()
   
aT
-------------------------------------------
.. automethod:: RepTate.applications.ApplicationTTSFactors.BaseApplicationTTSFactors.viewaT()
   
Log(bT)
-------------------------------------------
.. automethod:: RepTate.applications.ApplicationTTSFactors.BaseApplicationTTSFactors.viewLogbT()
   
bT
-------------------------------------------
.. automethod:: RepTate.applications.ApplicationTTSFactors.BaseApplicationTTSFactors.viewbT()
   
Log(aT, bT)
-------------------------------------------
.. automethod:: RepTate.applications.ApplicationTTSFactors.BaseApplicationTTSFactors.viewLogaTbT()
   
Log(aT) vs 1/T (Kelvin)
-------------------------------------------
.. automethod:: RepTate.applications.ApplicationTTSFactors.BaseApplicationTTSFactors.viewLogaT_invT()
   
