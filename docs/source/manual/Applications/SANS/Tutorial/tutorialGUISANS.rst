=========================
Tutorial SANS Application
=========================

.. toctree::
   :maxdepth: 2

This short tutorial shows how to load the bundled SANS examples, inspect the
standard scattering views, and create a simple Debye theory calculation.

Load SANS Data
--------------

#.  Start RepTate and create a new SANS application.

#.  Open the example files in ``data/PS_SANS``:

    * ``100k.sans``
    * ``250k.sans``
    * ``400k.sans``

    The SANS application reads text files with the ``.sans`` extension. Each
    file should contain the molecular weight ``Mw`` and deuterated-chain volume
    fraction ``phi`` (or ``Phi``) as file parameters, followed by columns for the
    scattering vector ``q`` and intensity ``I(q)``.

Inspect Views
-------------

Use the ``View`` selector to switch between the SANS representations:

* ``log(I(q))`` plots ``log10(q)`` against ``log10(abs(I(q)))``.
* ``I(q)`` plots the measured intensity as a function of scattering vector.
* ``Zimm`` plots ``1/I(q)`` against ``q^2``.
* ``Kratky`` plots ``q^2 I(q)`` against ``q``.

Add a Debye Theory
------------------

#.  In the theory selector, choose ``Debye`` and create the theory.

#.  Click ``Calculate`` to evaluate the Debye function for the loaded files.
    The theory uses ``Mw`` and ``phi``/``Phi`` from each file and the theory
    parameters ``Contrast``, ``C_gyr``, ``M_mono``, and ``Bckgrnd``.

#.  Use ``Minimize Error`` only when you want to fit the adjustable parameters.
    The optional ``Stretched`` and ``Non-Ideal Mix`` buttons enable the
    corresponding ``lambda`` and ``chi`` terms described in the Debye theory
    documentation.
