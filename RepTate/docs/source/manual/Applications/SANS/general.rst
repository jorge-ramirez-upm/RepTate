==================================
SANS: General description
==================================

.. contents:: Contents
    :local:

..  toctree::
   	:maxdepth: 2
	

----------
Data Files
----------

.. include:: ../datafile_doc.rst

``.sans`` extension
-------------------

Text files with ``.sans`` extension should be organised as follows:

- ``.sans`` files should **at least** the value parameter values for the:

  #. Sample molecular weight ``Mw``,
  #. Volume fraction of deuterated chains ``Phi``.

- 2 columns separated by **spaces** or **tabs** containing respectively:

  #. scattering vector, :math:`q`,
  #. scattered intensity, :math:`I(q)`,

A correct ``.sans`` file looks like:

.. code-block:: none
  
  Mw=407;Phi=0.964;
  0.0098083         24.9121
  0.010647          22.9176
  0.011486          21.7702
  0.012325          20.0757
  0.013164          18.6836
  ...               ...

-----
Views
-----

:math:`\log (I) \ \mathrm{vs} \ \log(q)`
--------------------------------

:math:`I \ \mathrm{vs} \ q`
-------------------------------------------

:math:`I^{-1} \ \mathrm{vs} \ q^2`   (Zimm plot)
----------------------

:math:`q^2\cdot I \ \mathrm{vs} \ q`  (Kratky plot)
----------------------------
