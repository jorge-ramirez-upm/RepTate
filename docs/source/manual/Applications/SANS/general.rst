==================================
SANS: General description
==================================

.. contents:: Contents
    :local:

..  toctree::
   	:maxdepth: 2
	
-------
Purpose
-------

.. autoclass:: RepTate.applications.ApplicationSANS.ApplicationSANS()	

----------
Data Files
----------

.. include:: ../datafile_doc.rst

``.sans`` extension
-------------------

Text files with ``.sans`` extension should be organised as follows:

- ``.sans`` files should contaion **at least** the parameter values for the:

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
log(I(q))
----------------------------------------

.. automethod:: RepTate.applications.ApplicationSANS.BaseApplicationSANS.viewLogSANS()

.. image:: images/SANS_LogIq.png
    :width: 45%
    :align: center


I(q)
---------------------------

.. automethod:: RepTate.applications.ApplicationSANS.BaseApplicationSANS.viewSANS()

.. image:: images/SANS_Iq.png
    :width: 45%
    :align: center

Zimm
------------------------------------------------

.. automethod:: RepTate.applications.ApplicationSANS.BaseApplicationSANS.viewZimm()

.. image:: images/SANS_Zimm.png
    :width: 45%
    :align: center

Kratky
---------------------------------------------------

.. automethod:: RepTate.applications.ApplicationSANS.BaseApplicationSANS.viewKratky()

.. image:: images/SANS_Kratky.png
    :width: 45%
    :align: center
