=====================================
Flow-Induced Crystallization Tutorial
=====================================

.. contents:: Contents
    :local:

.. toctree::
   :maxdepth: 2

.. |logo| image:: /app_logo/Crystal.png
    :width: 20pt
    :height: 20pt
    :align: bottom

.. |einstein| image:: /gui_icons/icons8-einstein.png
    :width: 20pt
    :height: 20pt
    :align: bottom

.. |calculate| image:: /gui_icons/icons8-abacus.png
    :width: 20pt
    :height: 20pt
    :align: bottom

.. |fit| image:: /gui_icons/icons8-minimum-value.png
    :width: 20pt
    :height: 20pt
    :align: bottom

.. |th_save| image:: /gui_icons/icons8-save_TH.png
    :width: 20pt
    :height: 20pt
    :align: bottom

This first tutorial checks that the Crystal application runs and shows how the
``GO-polySTRAND`` theory responds to a simple synthetic data set. The files used
here are theory-generated data, so the calculation is intended as a reproducible
sanity check before working with experimental crystallization data.

Load Synthetic Data
-------------------

#.  Start RepTate and create a new Flow Induced Crystallization Application |logo|.

#.  Open the three synthetic files in ``data/Crystal``:

    * ``InitialTest_gdot0.05.shearxs``
    * ``InitialTest_gdot0.1.shearxs``
    * ``InitialTest_gdot0.2.shearxs``

    These files use the ``.shearxs`` format handled by the Crystal application:
    each file stores ``gdot``, ``T``, and ``tstop`` parameters and the columns
    ``t``, ``sigma_xy``, ``Ndot``, ``phi_X``, and ``N``.

#.  Use the plot tabs on the left of the application window to inspect the
    individual plots. Use the ``View`` selector near the upper-right corner of
    the application window to switch between stress, viscosity, nucleation rate,
    nucleation density, and crystal-fraction views.

Run GO-polySTRAND
-----------------

#.  In the theory selector, choose ``GO-polySTRAND`` and create the theory
    |einstein|.

#.  Calculate the theory |calculate| once with the default settings to confirm that
    the model runs on the loaded files.

#.  For the synthetic data check, set both ``G_C`` and ``N_0`` to ``1e-3`` and
    calculate again. The tutorial data were generated from theory output, and
    these values are the documented settings for reproducing the crystal-fraction
    and nucleation-density curves.

Things To Try
-------------

After the initial calculation, explore the model response by changing one setting
at a time:

* Change ``Gamma`` to adjust the sensitivity to shear.
* Make small changes to ``epsilonB`` to adjust the quiescent crystallization
  barrier. In the original tutorial notes this is described as analogous to
  changing temperature.
* Adjust ``tau0`` to scale the nucleation rates.
* Adjust ``G_C`` to change the crystal growth rate.
* Use the theory's modes menu to edit the number of modes, relaxation times, and
  mode fractions. The mode fractions should add up to ``1``.
* Double-click a data set and edit file parameters such as ``gdot`` and
  ``tstop`` to see how the plotted quantities respond. The ``T`` parameter is
  stored by the ``.shearxs`` file type; the initial tutorial notes state that it
  has no effect in this synthetic check.

Steady Nucleation View
----------------------

#.  Open the data files in
    ``data/Crystal/CoccorulloMacromolecules2008/Steady_Shear_Nucleation_Data``.

#.  Reduce the application to one view if you want a compact plot, then select
    the ``Steady Nucleation`` view. This view gives one point per loaded file,
    using the flow rate from the file parameters on the x-axis and the final
    nucleation-rate value on the y-axis.

#.  Use ``View All`` to show the loaded files together.
