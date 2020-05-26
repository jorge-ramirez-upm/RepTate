==========================
React: General description
==========================


.. contents:: Contents
    :local:

..	toctree::
   	:maxdepth: 2
	
	
-------
Purpose
-------

.. automodule:: RepTate.applications.ApplicationReact.ApplicationReact()	

----------
Data Files
----------

.. include:: ../datafile_doc.rst

``.reac`` extension
-------------------

Text files with ``.reac`` extension should be organised as follows:

- ``.reac`` files are not expected to provide any specific parameter values. 

- 4 columns separated by **spaces** or **tabs** containing respectively:

  #. molar mass, :math:`M`,
  #. weight associated, :math:`\dfrac{\text d w(\log M)}{\text d \log M}`,
  #. the `g`-factor, :math:`g(M)=\dfrac{\langle R^2_g \rangle_\text{branched}}{\langle R^2_g \rangle_\text{linear}}` 
  #. number of branching points per 1000 carbon.

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

w(M)
----

.. automethod:: RepTate.applications.ApplicationReact.BaseApplicationReact.view_wM()

.. image:: images/React_wM.png
    :width: 45%
    :align: center

log(w(M))
---------
:math:`\log_{10}(w(M))` (log-linear)

.. automethod:: RepTate.applications.ApplicationReact.BaseApplicationReact.view_logwM()

.. image:: images/React_logwM.png
    :width: 45%
    :align: center

g(M)
----
:math:`g(M)` (log-linear)

.. automethod:: RepTate.applications.ApplicationReact.BaseApplicationReact.view_gM()

.. image:: images/React_gM.png
    :width: 45%
    :align: center

log(g(M))
---------
:math:`\log_{10}(g(M))` (log-linear)

.. automethod:: RepTate.applications.ApplicationReact.BaseApplicationReact.view_loggM()

.. image:: images/React_LoggM.png
    :width: 45%
    :align: center

br/1000C
--------
:math:`\text{br/1000C}` (log-linear)

.. automethod:: RepTate.applications.ApplicationReact.BaseApplicationReact.view_br_1000C()

.. image:: images/React_br_1000C.png
    :width: 45%
    :align: center
