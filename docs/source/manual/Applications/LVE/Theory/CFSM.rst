----
CFSM
----

.. toctree::
   :maxdepth: 2

Summary
-------

.. automodule:: RepTate.theories.TheoryDSMLinear.TheoryDSMLinear

Parameters and units
--------------------

``CFSM+Rouse`` can initialise ``MK`` and ``rho0`` from the Materials Database
when the first file in the dataset contains a recognised ``chem`` value.

The parameter table is unit-aware:

* ``MK`` is stored internally as a molar mass but displayed by default in
  ``Da``.
* ``rho0`` is displayed in ``g/cc``.
* ``Mc`` is displayed by default in ``Da``.
* ``tau_c`` is displayed in ``s``.

The underlying DSM formulas use the traditional molar-mass convention in
``Da``. RepTate therefore converts the unit-aware ``MK`` and ``Mc`` parameters
to ``Da`` inside the calculation. This preserves the legacy numerical behavior
while still allowing the parameter table and the Materials Database to use
explicit unit metadata.

For example, a Materials Database value ``MK = 140.5 Da`` is stored internally
as ``0.1405 kg/mol`` but displayed as ``140.5 Da`` in this theory. If the
initial crossover estimate computes ``Mc = 2146 Da``, the stored internal value
is ``2.146 kg/mol`` and the displayed value remains ``2146 Da``.
