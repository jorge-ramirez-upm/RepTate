Units
=====

RepTate keeps numerical values internally in canonical units. Unit conversion
should happen only at input/output boundaries: when reading files, displaying
values, formatting labels, or accepting user-entered values from the GUI.

Numerical theory code should continue to receive plain Python floats and NumPy
arrays. Do not pass unit-bearing objects into theory calculations.

Canonical Units
---------------

The unit registry is in ``RepTate.core.units``. Current canonical units include:

* time: ``s``
* angular frequency: ``rad/s``
* frequency: ``Hz``
* stress, modulus, pressure: ``Pa``
* viscosity: ``Pa.s``
* temperature: ``K``

Frequency and angular frequency are intentionally different quantities.
``Hz`` and ``rad/s`` must not be treated as generally compatible units. If a
specific importer accepts ``Hz`` where an application expects ``rad/s``, that
conversion must be handled explicitly at the file input boundary. This is the 
case for rheological data. 

Adding a Unit
-------------

Add the unit to ``_UNITS`` in ``RepTate.core.units``:

.. code-block:: python

   "ms": Unit("ms", "time", 1.0e-3)

The factor is relative to the canonical internal unit for that quantity. Keep
conversions multiplicative only unless the conversion model is deliberately
extended to support offset units.

Column Metadata
---------------

Data columns use ``ColumnSpec`` metadata:

.. code-block:: python

   ColumnSpec(
       name="w",
       display_unit="Hz",
       internal_unit="rad/s",
       quantity="angular_frequency",
   )

File importers should convert loaded arrays to internal units before storing
them in ``DataTable.data``. Axis-label generation can then use
``ColumnSpec.axis_label()`` or a fallback for legacy data types without unit
metadata.

Theory Parameter Metadata
-------------------------

Theory parameters can carry optional unit metadata:

.. code-block:: python

   Parameter(
       "tau_e",
       2e-6,
       "Rouse time of one Entanglement",
       ParameterType.real,
       quantity="time",
       internal_unit="s",
       display_unit="μs",
   )

The stored ``Parameter.value`` remains in ``internal_unit``. GUI display and
editing may use ``display_unit`` via ``display_value()`` and
``value_from_display()``. Fitting and theory calculations should continue to
use ``Parameter.value`` directly.
