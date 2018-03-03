=========================
NLVE: General description
=========================

.. contents:: Contents
    :local:

..	toctree::
   	:maxdepth: 2
	
----------
Data Files
----------

.. include:: ../datafile_doc.rst

``.shear`` extension
--------------------

Text files with ``.shear`` extension should be organised as follows:

- ``.shear`` files should provide parameter values for

  #. shear rate, :math:`\dot\gamma`
  #. temperature, :math:`T`

- 2 columns separated by **spaces** or **tabs** containing respectively:

  #. time, :math:`t`,
  #. shear stress growth coefficient (viscosity), :math:`\eta^+(t) = \dfrac{\sigma_{xy}}{\dot\gamma}`,

A correct ``.shear`` file looks like:

.. code-block:: none
  
  gdot=0.1;T=160;
  2.50E-01 845
  7.50E-01 1830
  1.25E+00 2490
  ...      ...

``.uext`` extension
-------------------

Text files with ``.uext`` extension should be organised as follows:

- ``.uext`` files should provide parameter values for

  #. Hencky strain rate, :math:`\dot\varepsilon`
  #. temperature, :math:`T`

- 2 columns separated by **spaces** or **tabs** containing respectively:

  #. time, :math:`t`,
  #. tensile stress growth coefficient (viscosity), :math:`\eta_E^+(t) = \dfrac{\sigma_{xx} - \sigma_{yy}}{\dot\varepsilon}`,

A correct ``.uext`` file looks like:

.. code-block:: none
  
  gdot=0.1;T=160;
  2.50E-01 845
  7.50E-01 1830
  1.25E+00 2490
  ...      ...

.. warning::
  The first line of the ``.uext`` file provides the flow rate as ``gdot=0.1``, **not** ``edot=0.1``

-----
Views
-----

:math:`\log(eta(t))`
-------------------------
log transient viscosity

:math:`\log(sigma(t))-gamma` (log-linear)
-----------------------------------------

log transient shear stress vs strain

:math:`\log(sigma(t))-t` (log-linear)
-------------------------------------

log transient shear stress vs time
