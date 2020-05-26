=========================
LAOS: General Description
=========================

.. contents:: Contents
    :local:

..	toctree::
   	:maxdepth: 2

-------
Purpose
-------

.. automodule:: RepTate.applications.ApplicationLAOS.ApplicationLAOS()	
	
----------
Data Files
----------

.. include:: ../datafile_doc.rst

``.laos`` extension
-------------------

Text files with ``.laos`` extension should be organised as follows:

- ``.laos`` files should contaion **at least** the parameter values for the:

  #. Frequency ``omega``,
  #. Amplitude ``gamma``.

- 3 columns separated by **spaces** or **tabs** containing respectively:

  #. time, :math:`t`,
  #. strain, :math:`\gamma`,
  #. stress :math:`\sigma`.

Other columns will be ignored. The top of a correct ``.laos`` file looks like:

.. code-block:: none
  
	omega=0.3;gamma=3.16;
	#time 	Strain(-) 	Stress(Pa)
	0.082	0.07802		8.5946
	0.445	0.42041		10.804
	0.814	0.7637		11.736
	1.187	1.1018		11.959
	1.559	1.4245		11.807
	1.924	1.7241		11.419
	2.292	2.0053		10.893
	2.659	2.262		10.246
	...     ...         ...

-----
Views
-----

.. todo::
    Need to report the views available in LAOS

