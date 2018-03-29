==================================
TTS: General description
==================================

.. contents:: Contents
    :local:

..	toctree::
   	:maxdepth: 2
	
----------
Data Files
----------

.. include:: ../datafile_doc.rst


``.osc`` extension
-------------------

Text files with ``.osc`` extension should be organised as follows:

- ``.osc`` files should **at least** the value parameter values for the:

  #. sample molar mass ``Mw``,
  #. temperature ``T``.

- 3 columns separated by **spaces** or **tabs** containing respectively:

  #. frequency, :math:`\omega`,
  #. elastic modulus, :math:`G'`,
  #. loss modulus :math:`G''`.

Other columns will be ingnored. A correct ``.osc`` file looks like:

.. code-block:: none

  T=0;Mw=94.9;chem=PI;origin=LeedsDA;label=PI88k_09_PP-10;PDI=1.03;
  Freq	    G'	        G"	        Temp	    Strain
  rad/s	    Pa	        Pa	        °C	        %	
  100       3.4801E5    70871       -0.0079     0.96734
  68.129    3.328E5     70723       -0.0088     0.96362
  46.416    3.1675E5    71696       -0.0101     0.96238
  ...       ...         ...         ...         ...

-----
Views
-----

:math:`\log(G'(\omega)), \log(G''(\omega))`
-------------------------------------------

:math:`G'(\omega), G''(\omega)`
--------------------------------

:math:`\eta^*(\omega)`
----------------------

:math:`\delta(\omega)`
----------------------

:math:`\tan(\delta(\omega))`
----------------------------
