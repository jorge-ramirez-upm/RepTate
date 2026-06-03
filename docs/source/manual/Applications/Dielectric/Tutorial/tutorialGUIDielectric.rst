===============================
Tutorial Dielectric Application
===============================

.. toctree::
   :maxdepth: 2

This tutorial shows how to load a dielectric spectroscopy data file, inspect the
available views, and create a simple Debye modes theory.


Load a dielectric data file
---------------------------

Start RepTate and create a new ``Dielectric`` application. Open the example file
``data/Dielectric_Spectroscopy/Debye.dls`` from the RepTate source tree.

Dielectric spectroscopy files use the ``.dls`` extension. A file should define
the file parameters ``Mw`` and ``T`` and provide three data columns:

* ``w``: angular frequency, in ``rad/s``.
* ``e'``: elastic dielectric permittivity.
* ``e''``: loss dielectric permittivity.

The file is loaded as a normal RepTate data set, so it can be selected in the
data set tree, shown or hidden, and combined with theories and tools.


Inspect the views
-----------------

Use the view selector to change how the data are displayed. The combined views
``log(e',e''(w))``, ``semilog(e',e''(w))``, and ``e',e''(w)`` plot both
components against angular frequency. The single-component views show either
``e'`` or ``e''`` only.

The ``Cole-Cole`` view plots ``e''`` as a function of ``e'``. This is useful for
checking the shape of the dielectric response without using frequency as the
horizontal axis.

The logarithmic views use base-10 logarithms, so they require positive
frequencies and positive dielectric values in the displayed columns.


Fit Debye modes
---------------

Select the loaded file, choose ``Debye modes`` in the theory selector, and click
``Create Selected Theory``. The theory initializes a set of discrete Debye modes
between the minimum positive frequency and the maximum frequency of the selected
data.

Use the number-of-modes control in the theory toolbar to change the number of
modes. The ``View modes`` button toggles the markers used to inspect and adjust
the modes on the plot. ``Calculate`` evaluates the theory with the current
parameters, while ``Minimize Error`` fits the adjustable parameters to the data.

The Debye modes theory is a single-file theory. If more than one active file is
present in the current data set, RepTate applies the theory to the first active
file.
