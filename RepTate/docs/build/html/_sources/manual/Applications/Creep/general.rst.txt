==========================
Creep: General description
==========================

.. contents:: Contents
    :local:

..	toctree::
   	:maxdepth: 2
	
-------
Purpose
-------

.. autoclass:: ApplicationCreep.ApplicationCreep()	

----------
Data Files
----------

.. include:: ../datafile_doc.rst

``.creep`` extension
--------------------

Text files with ``.creep`` extension should be organised as follows:

- ``.creep`` files should **at least** the value parameter values for the:

  #. Applied stress ``stress``

- 2 columns separated by **spaces** or **tabs** containing respectively:

  #. time, :math:`t`,
  #. strain, :math:`\gamma`,

A correct ``.creep`` file looks like:

.. code-block:: none

  chem=PE;label=CM3;T=150;stress=10;
  t	    strain	    stress	T 
  s	    -	        Pa	    C
  1E-3	1.413E-5	10	    149.9
  1E-3	-9.419E-6	10	    149.9
  1E-3	-2.826E-5	10	    149.9
  ...   ...         ...     ...

-----
Views
-----

log(gamma(t))
--------------------------------
.. automethod:: ApplicationCreep.BaseApplicationCreep.viewLogStraint()

.. image:: images/Creep_LogGammat.png
    :width: 45%
    :align: center

gamma(t)
-------------------------------------------
.. automethod:: ApplicationCreep.BaseApplicationCreep.viewStraint()

.. image:: images/Creep_Gammat.png
    :width: 45%
    :align: center

log(J(t))
----------------------
.. automethod:: ApplicationCreep.BaseApplicationCreep.viewLogJt()

.. image:: images/Creep_LogJt.png
    :width: 45%
    :align: center

J(t)
----------------------------
.. automethod:: ApplicationCreep.BaseApplicationCreep.viewJt()

.. image:: images/Creep_Jt.png
    :width: 45%
    :align: center

t/J(t)
----------------------
.. automethod:: ApplicationCreep.BaseApplicationCreep.viewt_Jt()

.. image:: images/Creep_t_Jt.png
    :width: 45%
    :align: center

