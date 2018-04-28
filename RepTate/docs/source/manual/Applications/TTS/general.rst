==================================
TTS: General description
==================================

.. contents:: Contents
    :local:

..	toctree::
   	:maxdepth: 2

-------
Purpose
-------

.. autoclass:: ApplicationTTS.ApplicationTTS()	
	
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

log(G',G''(w))
-------------------------------------------
Logarithm of the storage modulus :math:`\log(G'(\omega))` and loss modulus :math:`\log(G''(\omega))` vs :math:`\log(\omega)`

.. image:: images/TTS_logG1G2.png
    :width: 45%
    :align: center


G',G''(w)
--------------------------------
Storage modulus :math:`G'(\omega)` and loss modulus :math:`G''(\omega)` (in logarithmic scale) vs :math:`\omega`(in logarithmic scale)

.. image:: images/TTS_G1G2.png
    :width: 45%
    :align: center

etastar
----------------------
Complex viscosity :math:`\eta^*(\omega) = \sqrt{G'^2 + G''^2}/\omega` (in logarithmic scale) vs :math:`\omega` (in logarithmic scale)

.. image:: images/TTS_etastar.png
    :width: 45%
    :align: center

logetastar
----------------------
Logarithm of the complex viscosity :math:`\eta^*(\omega) = \sqrt{G'^2 + G''^2}/\omega` vs :math:`\log(\omega)` 

.. image:: images/TTS_logetastar.png
    :width: 45%
    :align: center

delta    
----------------------
Loss or phase angle :math:`\delta(\omega)=\atan(G''/G')\cdot 180/\pi` (in degrees, in logarithmic scale) vs :math:`\omega` (in logarithmic scale)

.. image:: images/TTS_delta.png
    :width: 45%
    :align: center

tan(delta)
----------------------------
Tangent of the phase angle :math:`\tan(\delta(\omega))=G''/G'` (in logarithmic scale) vs :math:`\omega` (in logarithmic scale)

.. image:: images/TTS_tandelta.png
    :width: 45%
    :align: center

log(tan(delta))
----------------------------
:math:`\log(\tan(\delta(\omega)))=\log(G''/G')` vs :math:`\log(\omega)` 

.. image:: images/TTS_logtandelta.png
    :width: 45%
    :align: center
    
log(G*)
----------------------------
Logarithm of the modulus of the complex viscosity :math:`|G*(\omega)|=\sqrt(G'^2+G''^2)` vs :math:`\log(\omega)` 

.. image:: images/TTS_logGstar.png
    :width: 45%
    :align: center

log(tan(delta),G*)
----------------------------
Logarithm of the tangent of the loss angle :math:`\tan(\delta(\omega))=G''/G'` vs logarithm of the modulus of the complex viscosity :math:`|G*(\omega)|=\sqrt(G'^2+G''^2)`

.. image:: images/TTS_logtandeltaGstar.png
    :width: 45%
    :align: center

delta(G*)
----------------------------
Loss angle :math:`\delta(\omega)=\atan(G''/G')` vs logarithm of the modulus of the complex viscosity :math:`|G*(\omega)|=\sqrt(G'^2+G''^2)`

.. image:: images/TTS_deltaGstar.png
    :width: 45%
    :align: center

J',J''(w)
----------------------------
Storage compliance :math:`J'(\omega)=G'/(G'^2+G''^2)` and loss compliance :math:`J''(\omega)=G''/(G'^2+G''^2)` (in logarithmic scale) vs :math:`\omega` (in logarithmic scale)

.. image:: images/TTS_J1J2.png
    :width: 45%
    :align: center

Cole-Cole
----------------------------
Cole-Cole plot: out of phase viscosity :math:`\eta''(\omega)=G'(\omega)/\omega` vs dynamic viscosity :math:`\eta'(\omega)=G''(\omega)/\omega`

.. image:: images/TTS_ColeCole.png
    :width: 45%
    :align: center

log(G')
-------------------------------------------
Logarithm of the storage modulus :math:`\log(G'(\omega))` vs :math:`\log(\omega)`

.. image:: images/TTS_logG1.png
    :width: 45%
    :align: center


G'
--------------------------------
Storage modulus :math:`G'(\omega)` (in logarithmic scale) vs :math:`\omega`(in logarithmic scale)

.. image:: images/TTS_G1.png
    :width: 45%
    :align: center

log(G'')
-------------------------------------------
Logarithm of the loss modulus :math:`\log(G''(\omega))` vs :math:`\log(\omega)`

.. image:: images/TTS_logG2.png
    :width: 45%
    :align: center


G''
--------------------------------
Loss modulus :math:`G''(\omega)` (in logarithmic scale) vs :math:`\omega`(in logarithmic scale)

.. image:: images/TTS_G2.png
    :width: 45%
    :align: center

log(G',G''(w),tan(delta))
--------------------------------
Logarithm of the storage modulus :math:`\log(G'(\omega))`, loss modulus :math:`\log(G''(\omega))` and tangent of the loss angle :math:`\log(\tan(\delta(\omega)))=\log(G''/G')`vs :math:`\log(\omega)`

.. image:: images/TTS_logG1G2tandelta.png
    :width: 45%
    :align: center
