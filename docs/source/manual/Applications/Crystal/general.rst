=================================================
Flow Induced Crystallization: General description
=================================================

.. contents:: Contents
    :local:

..	toctree::
   	:maxdepth: 2

-------
Purpose
-------

.. automodule:: RepTate.applications.ApplicationCrystal.ApplicationCrystal	

.. _Crystal_Data_Description:

----------
Data Files
----------

.. include:: ../datafile_doc.rst


``.shearxs`` extension
----------------------

Text files with ``.shearxs`` extension should be organised as follows:

- ``.shearxs`` files should contaion **at least** the parameter values for the:

  #. shear rate, :math:`\dot\gamma`
  #. shear end time, :math:`t`-stop
  #. temperature, :math:`T`

- 5 columns separated by **spaces** or **tabs** containing respectively:

  #. time, :math:`t`,
  #. shear stress growth function, :math:`\sigma^+(t)`,
  #. nucleation rate, :math:`\dot N(t)`,
  #. crystal fraction, :math:`\phi_X(t)`,
  #. nucleation density, :math:`N(t)`,

Other columns will be ignored. A correct ``.shearxs`` file looks like:

.. code-block:: none

  gdot=0.1;tstop=50.0;T=0.0;
  t	          sigma_xy	  Ndot	      phi_X	      N
  1.437E+00	  1.411E+02	  5.103E-09	  3.227E-08	  1.001E-05
  1.751E+00	  1.709E+02	  1.358E-08	  5.772E-08	  1.001E-05
  2.134E+00	  2.065E+02	  4.283E-08	  1.034E-07	  1.002E-05
  2.600E+00	  2.486E+02	  1.623E-07	  1.858E-07	  1.006E-05
  3.168E+00	  2.978E+02	  7.418E-07	  3.349E-07	  1.028E-05
  ...         ...         ...         ...         ...

-----
Views
-----

log(eta(t))
---------------------
.. automethod:: RepTate.applications.ApplicationCrystal.ApplicationCrystal.viewLogeta()
Ndot(t) [log-log]
---------------------
.. automethod:: RepTate.applications.ApplicationCrystal.ApplicationCrystal.viewNdot

N(t) [log-log]
---------------------
.. automethod:: RepTate.applications.ApplicationCrystal.ApplicationCrystal.viewNt

phiX(t) [log-log]
---------------------
.. automethod:: RepTate.applications.ApplicationCrystal.ApplicationCrystal.viewphiX

Ndot(t) [log-lin]
---------------------
Nucleation rate as a function of time on log axis :math:`\dot{N}(t)` vs time :math:`t`


N(t) [log-lin]
---------------------
Nucleation density as a function of time on log axis :math:`N(t)` vs
time :math:`t`

phiX(t) [log-lin]
---------------------
Crystal fraction as a function of time on log axis :math:`\\phi_X(t)`
vs time :math:`t`


eta(t))
---------------------
.. automethod:: RepTate.applications.ApplicationCrystal.ApplicationCrystal.vieweta()


log(sigma(gamma))
---------------------
.. automethod:: RepTate.applications.ApplicationCrystal.ApplicationCrystal.viewLogSigmaGamma()
    
sigma(gamma)
---------------------
.. automethod:: RepTate.applications.ApplicationCrystal.ApplicationCrystal.viewSigmaGamma()

log(sigma(t))
---------------------
.. automethod:: RepTate.applications.ApplicationCrystal.ApplicationCrystal.viewLogSigmaTime()

    
sigma(t)
---------------------
.. automethod:: RepTate.applications.ApplicationCrystal.ApplicationCrystal.viewSigmaTime()


Flow Curve
---------------------
.. automethod:: RepTate.applications.ApplicationCrystal.ApplicationCrystal.view_flowcurve()

Steady Nucleation
---------------------
.. automethod:: RepTate.applications.ApplicationCrystal.ApplicationCrystal.view_steadyNuc

The Crystal application views use the columns of the loaded crystallisation
file. For the ``.shearxs`` files described above, the columns are time,
transient stress, nucleation rate, crystal fraction, and nucleation density. The
flow rate is taken from the file parameters and is used to calculate transient
viscosity and strain.

Use ``log(eta(t))`` or ``eta(t)`` to inspect the transient viscosity,
:math:`\eta^+(t)=\sigma^+(t)/\dot\gamma`. The logarithmic view calculates
:math:`\log_{10}(t)` and :math:`\log_{10}(\eta^+)` explicitly; the ``eta(t)``
view plots the same quantity using logarithmic axes by default.

Use the ``Ndot(t)``, ``N(t)``, and ``phiX(t)`` views to follow the crystallisation
quantities as functions of time. ``Ndot(t)`` shows the nucleation rate,
``N(t)`` shows the nucleation density, and ``phiX(t)`` shows the crystal
fraction. Each quantity is available with log-log and log-lin scaling so that
early-time and late-time behaviour can be inspected without changing the data.

Use ``sigma(t)`` and ``log(sigma(t))`` to inspect the transient stress as a
function of time. ``sigma(t) [log-lin]`` keeps the stress on a linear axis while
using a logarithmic time axis. Use ``sigma(gamma)`` and ``log(sigma(gamma))`` to
plot the same transient stress against strain, where the strain is computed from
time multiplied by the flow rate.

``Flow Curve`` and ``Steady Nucleation`` provide one point per file. ``Flow
Curve`` plots the final stress value against the flow rate, and ``Steady
Nucleation`` plots the final nucleation-rate value against the flow rate. These
views are useful when several files at different flow rates are loaded in the
same dataset.

Logarithmic views require positive time and positive values of the plotted
quantity. The steady views use the last row of each file as the steady-state
estimate, so they assume that the imported data extend far enough in time for
the final value to be representative.
