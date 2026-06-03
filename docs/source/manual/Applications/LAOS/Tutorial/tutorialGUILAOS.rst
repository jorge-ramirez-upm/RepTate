=========================
Tutorial LAOS Application
=========================

.. toctree::
   :maxdepth: 2

This short tutorial shows how to load the bundled LAOS examples and inspect raw,
filtered, and harmonic-analysis views. It does not require fitting a theory.

Load LAOS Data
--------------

#.  Start RepTate and create a new LAOS application.

#.  Open one of the example files in ``data/LAOS``:

    * ``CPyCL-omega00p30-gam03p1600.laos``
    * ``GiesekusSimulation-omega01p00-gam05p000.laos``
    * ``SlugSlime-omega03p00-Run31.laos``

    The LAOS application reads text files with the ``.laos`` extension. Each
    file should contain the angular frequency ``omega`` and strain amplitude
    ``gamma`` as file parameters, followed by columns for time, strain, and
    stress. Extra columns are ignored by the file reader.

Check the Raw Signal
--------------------

Use the ``View`` selector to inspect the raw imported data before using the
Fourier-based views:

* ``sigma,gamma(t)`` shows raw stress and raw strain as functions of time.
* ``sigma SCA,gamma(t)`` scales the raw stress by its maximum absolute value so
  the stress and strain phase can be compared on the same plot.
* ``sigma(t)`` and ``gamma(t)`` show each raw signal separately.
* ``sigma(gamma)`` plots the raw stress-strain Lissajous curve.

Use Fourier-Based Views
-----------------------

After checking that the signal is periodic and has a clear oscillatory strain,
switch to the Fourier-based views:

* ``sigma(gamma) FILT`` plots reconstructed stress against reconstructed strain.
* ``FFT spectrum`` shows the normalized stress-harmonic spectrum.
* ``sigma(gdot) FILT`` plots reconstructed stress against reconstructed
  strain-rate, using the file parameter ``omega``.
* ``sigma(gamma) ANLS`` and ``sigma(gdot) ANLS`` compare the filtered stress
  with elastic or viscous harmonic contributions.
* ``Cheb elastic`` and ``Cheb viscous`` show the elastic and viscous Chebyshev
  coefficients from the Fourier coefficients.

When one of these Fourier-based views is selected, RepTate shows two extra view
controls. ``HHSR`` is the highest harmonic used in stress reconstruction.
``PPQC`` is the number of points per quarter cycle used for the Fourier
reconstruction; the source code limits it to the range 20 to 500.

