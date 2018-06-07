==================================
G(t): General description
==================================

.. contents:: Contents
    :local:

..	toctree::
   	:maxdepth: 2
	
-------
Purpose
-------

.. autoclass:: ApplicationGt.ApplicationGt()	


----------
Data Files
----------

.. include:: ../datafile_doc.rst

``.gt`` extension
--------------------

Text files with ``.gt`` extension should be organised as follows:

- ``.gt`` files should provide at least parameter values for

  #. Molecular weight, :math:`M_w`
  #. Strain applied, :math:`\gamma`. If not present, the experimental data file is supposed to contain the relaxation modulus, not the stress, and the value of :math:`\gamma` is assumed to be equal to 1.

- 2 columns separated by **spaces** or **tabs** containing respectively:

  #. time, :math:`t`,
  #. shear stress, :math:`\sigma_{xy}`,

A correct ``.gt`` file looks like:

.. code-block:: none
  
  ncontri=1;Mw=224;gamma=1;
  t sxy
  0.0E+0      1.28146E+10     
  5.0E-6      1.13402E+10     
  1.0E-5      7.57171E+9     
  ...         ...

-----
Views
-----

log[G(t)]
-------------------------
.. automethod:: ApplicationGt.BaseApplicationGt.viewLogGt()

.. image:: images/Gt_LogGt.png
    :width: 45%
    :align: center

G(t)
--------------
.. automethod:: ApplicationGt.BaseApplicationGt.viewGt()

.. image:: images/Gt_Gt.png
    :width: 45%
    :align: center

Schwarzl G',G''
-----------------------
.. automethod:: ApplicationGt.BaseApplicationGt.viewSchwarzl_Gt()

The time range of the :math:`G(t)` that will be used for the Fourier transformation can be selected by changing the values of the text boxes :math:`\log(t_{min})` and :math:`\log(t_{min})`. For more details, check :cite:`Gt-Schwarzl_1971`.

.. image:: images/Gt_Schwarzl.png
    :width: 45%
    :align: center

i-Rheo G',G''
---------------------
.. automethod:: ApplicationGt.BaseApplicationGt.viewiRheo()

The time range of the :math:`G(t)` that will be used for the Fourier transformation can be selected by changing the values of the text boxes :math:`\log(t_{min})` and :math:`\log(t_{min})`. For more details, check :cite:`Gt-Tassieri_2016`.

.. image:: images/Gt_iRheo.png
    :width: 45%
    :align: center

i-Rheo-Over G',G''
---------------------
.. automethod:: ApplicationGt.BaseApplicationGt.viewiRheoOver()

The time range of the :math:`G(t)` that will be used for the Fourier transformation can be selected by changing the values of the text boxes :math:`\log(t_{min})` and :math:`\log(t_{min})`. For more details, check :cite:`Gt-Tassieri_2016`.

.. image:: images/Gt_iRheoOver.png
    :width: 45%
    :align: center

.. rubric:: References

.. bibliography:: bibliography.bib
    :style: unsrt
    :keyprefix: Gt-
