==================================
LVE: General Description
==================================

.. contents:: Contents
    :local:

..	toctree::
   	:maxdepth: 2
	
	
----------
Data Files
----------

.. include:: ../datafile_doc.rst

``.tts`` extension
-------------------

Text files with ``.tts`` extension should be organised as follows:

- ``.tts`` files should **at least** the value parameter values for the:

  #. sample molar mass ``Mw``,
  #. temperature ``T``.

- 3 columns separated by **spaces** or **tabs** containing respectively:

  #. frequency, :math:`\omega`,
  #. elastic modulus, :math:`G'`,
  #. loss modulus :math:`G''`.

A correct ``.tts`` file looks like:

.. code-block:: none
  
  T=-35;CTg=14.65;dx12=0;isof=true;Mw=13.5;chem=PI;PDI=1.04;
  1.90165521264016E+0000      7.38023647054321E+0001      1.35152457625702E+0004     -2.99910000000000E+0001
  3.01392554124040E+0000      1.99063258930248E+0002      2.14834778959042E+0004     -2.99900000000000E+0001
  4.51700049635957E+0000      3.72861375546198E+0002      3.17756716623334E+0004     -3.99960000000000E+0001
  ...                         ...                         ...                        ...

-----
Views
-----

:math:`G'(\omega), G''(\omega)`
--------------------------------

:math:`\log(G'(\omega)), \log(G''(\omega))`
-------------------------------------------

:math:`\eta^*(\omega)`
----------------------

:math:`\log(\eta^*(\omega))`
----------------------------

:math:`\delta(\omega)`
----------------------

:math:`\tan(\delta(\omega))`
----------------------------
