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

.. automodule:: RepTate.applications.ApplicationLAOS.ApplicationLAOS
	

The LAOS application provides views for the raw time signal, Lissajous plots,
Fourier-based reconstructions, and Chebyshev analysis. The views use the three
columns of a ``.laos`` file: time, strain, and stress. The file parameters
``omega`` and ``gamma`` are also required; ``omega`` is used when the view needs
the strain-rate or harmonic frequencies.


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

``sigma,gamma(t)`` displays the raw stress and raw strain as functions of time.
Use it as a first check that the loaded signal has the expected oscillatory
shape. ``sigma SCA,gamma(t)`` shows the same raw strain together with the raw
stress scaled by its maximum absolute value, which is useful when comparing the
phase of stress and strain on the same plot. ``sigma(t)`` and ``gamma(t)`` show
the raw stress or raw strain separately.

``sigma(gamma)`` plots the raw stress against the raw strain. This is the direct
stress-strain Lissajous curve from the imported data. ``sigma(gamma) FILT`` uses
the Fourier reconstruction of the signal before plotting stress against strain.

``FFT spectrum`` plots the normalized magnitude of the stress harmonics as a
function of angular frequency. The spectrum is normalized by the fundamental
harmonic and is shown on a logarithmic vertical axis. To keep the plot readable,
the view displays at most the first 25 harmonics.

``sigma(gdot) FILT`` plots the reconstructed stress against the reconstructed
strain-rate. The strain-rate is calculated from the reconstructed strain and the
file parameter ``omega``.

``sigma(gamma) ANLS`` and ``sigma(gdot) ANLS`` compare the filtered stress with
elastic or viscous contributions reconstructed from selected odd harmonics. They
also include the contribution reconstructed from the first and third harmonics.

``Cheb elastic`` and ``Cheb viscous`` display the elastic and viscous Chebyshev
coefficients obtained from the Fourier coefficients of the stress signal. These
views are intended for harmonic analysis after checking that the raw signal is
suitable for Fourier processing.

The filtered, FFT, analysis, and Chebyshev views show two additional controls in
the view toolbar. ``HHSR`` is the highest harmonic considered in the stress
reconstruction. ``PPQC`` is the number of points per quarter cycle used in the
Fourier reconstruction; it can be set between 20 and 500.

The Fourier-based views interpolate the signal onto an evenly spaced time grid
and identify cycles from zero crossings of the strain signal. They are therefore
most appropriate for periodic LAOS data with a clear oscillatory strain signal.
