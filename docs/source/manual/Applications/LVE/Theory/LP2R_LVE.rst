----
LP2R
----

.. toctree::
   :maxdepth: 2

Summary
-------

.. automodule:: RepTate.theories.TheoryLP2RLVE.TheoryLP2RLVE

Polymer components
------------------

The LP2R LVE theory represents the polymer input as a list of components rather
than as a single visible input-mode parameter. Open the ``LP2R components``
dialog from the theory toolbar to add, edit, remove, import, and normalise the
components used in the next calculation.

Each component has a weight fraction and one of two forms:

* ``lognormal``: described by ``npoly``, ``Mw`` and ``PDI``.
* ``mwd``: described by discrete molar masses and weights.

Discrete MWD components can be imported from a RepTate ``Discretize MWD`` theory
or from a ``.gpc`` file. RepTate expects ``.gpc`` files to provide columns
``M`` and ``W(logM)``. The unit declared in the ``M`` header is read when
available; masses are converted to RepTate's internal molar-mass unit
``kg/mol`` before being passed to LP2R.

If no component has been defined, LP2R creates a default lognormal component
from the first file when possible. ``Mw`` and ``PDI`` are taken from the file
parameters if they exist and are positive; otherwise reasonable defaults are
used. The default number of lognormal bins is ``npoly = 8``.

Material and numerical parameters
---------------------------------

The normal parameter table contains the material and numerical controls:
``MK``, ``Me``, ``G0``, ``tau_e``, glass parameters, ``freq_ratio`` and the
advanced numerical controls. The hidden default-component parameters ``Mw``,
``PDI`` and ``n`` are not part of the ordinary fitting workflow.

When the first file contains a recognised ``chem`` value, LP2R imports common
material parameters from the Materials Database. ``MK``, ``Me`` and ``tau_e``
are imported directly when available. ``G0`` is initialised from the shifted
Materials Database value of ``Ge`` using ``G0 = 0.8 Ge``.

Calculation output
------------------

When calculation starts, LP2R prints a table of the current polymer components
in the theory output area. The calculation progress is shown with dashed
markers from 0% to 100%, following the convention used by GLaMM/SCCR.

If the component list is empty or invalid, LP2R stops before starting the
solver and reports the problem in the theory output area.

Numerical robustness
--------------------

The LP2R implementation uses an MSVC-safe KWW implementation for the sake of compatibility
with Windows computers. If a numeric
integration failure occurs, the error is caught and reported in the theory
output area instead of terminating RepTate.

Advanced LP2R Controls
----------------------

The ``Advanced LP2R controls`` dialog exposes numerical controls that are not
normally varied during routine fitting. These parameters are kept separate from
the polymer component list and the main material parameters.
