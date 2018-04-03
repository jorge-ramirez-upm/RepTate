==================================
React: General description
==================================


.. contents:: Contents
    :local:

..	toctree::
   	:maxdepth: 2
	
	
-------
Purpose
-------

.. autoclass:: ApplicationReact.ApplicationReact()	

----------
Data Files
----------

.. include:: ../datafile_doc.rst

``.reac`` extension
-------------------

Text files with ``.reac`` extension should be organised as follows:

- Any parameters in the first line. ``.reac`` files are not expected
  to provide any specific parameter values.

- 4 columns separated by **spaces** or **tabs** containing respectively:

  #. molar mass, :math:`M`,
  #. weight associated, :math:`w(M)`,
  #. the `g`-factor, :math:`g(M)` 
  #. number of branch per 1000 carbon, :math:`\log_{10}(g(M))`.

A correct ``.reac`` file looks like:

.. code-block:: none
  
  0.1148E+03 0.5000E-03 0.1000E+01 0.0000E+00
  0.1514E+03 0.1500E-02 0.1000E+01 0.0000E+00
  0.1995E+03 0.1667E-02 0.1000E+01 0.0000E+00
  0.2630E+03 0.1750E-02 0.1000E+01 0.0000E+00
  0.3467E+03 0.5250E-02 0.1000E+01 0.0000E+00
  0.4571E+03 0.6750E-02 0.9977E+00 0.3765E+00
  ...        ...        ...        ...


-----
Views
-----

:math:`w(M)` (log-linear)
-------------------------

:math:`\log_{10}(w(M))` (log-linear)
------------------------------------

:math:`g(M)` (log-linear)
-------------------------

:math:`\log_{10}(g(M))` (log-linear)
------------------------------------

:math:`\text{br/1000C}` (log-linear)
------------------------------------
