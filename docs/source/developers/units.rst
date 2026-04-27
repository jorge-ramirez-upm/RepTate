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
* deformation rate: ``1/s``
* inverse distance: ``1/A``
* nucleation rate: ``1/s/m3``
* rate: ``m/s``
* unit density: ``1/m3``
* angular frequency: ``rad/s``
* frequency: ``Hz``
* stress, modulus, pressure: ``Pa``
* compliance: ``1/Pa``
* viscosity: ``Pa.s``
* angle: ``rad``
* density: ``kg/m3``
* inverse temperature: ``1/K``
* temperature: ``K``
* molar mass: ``kg/mol``

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

View Axis Metadata
------------------

Views can now carry explicit axis metadata through ``AxisSpec`` in
``RepTate.core.View``. This should be preferred over relying only on the
legacy ``x_units`` and ``y_units`` strings when a view is meant to be
unit-aware.

.. code-block:: python

   self.views["G(t)"] = View(
       name="G(t)",
       description="Relaxation modulus",
       x_label="t",
       y_label="G",
       x_units="s",
       y_units="Pa",
       log_x=True,
       log_y=True,
       view_proc=self.viewGt,
       n=1,
       snames=["G"],
       x_axis=AxisSpec(label="t", internal_unit="s"),
       y_axis=AxisSpec(label="G", internal_unit="Pa"),
   )

``AxisSpec`` stores:

* ``label``: axis label text
* ``internal_unit``: canonical unit used by calculations and stored view data
* ``display_unit``: currently selected GUI unit
* ``quantity``: inferred from the unit registry unless set explicitly
* ``transform``: currently ``identity`` or ``log10``
* ``unit_choices``: optional restricted list of units to offer in the GUI

Two-way conversion helpers are available on both ``AxisSpec`` and ``View``:

* ``AxisSpec.convert_from_internal()``
* ``AxisSpec.convert_to_internal()``
* ``View.convert_xy_to_display()``
* ``View.convert_xy_to_internal()``

Plotting boundary
-----------------

``view_proc()`` should continue to return x and y arrays in canonical internal
units. Conversion to the currently selected display units should happen only at
the plotting boundary.

Ordinary data and theory curves are converted in ``QDataSet.do_plot()``. Do not
move display-unit conversion into numerical theory code.

The same rule applies to theory-generated ``DataTable`` objects. If a theory
fills ``self.tables[...]`` directly, the stored arrays must already be in the
canonical internal units expected by the active application views. Do not store
legacy display-unit values in theory tables and rely on the view layer to
"correct" them later, because that will produce inconsistent scaling between
experimental data and theory curves once view axes become unit-aware.

Theory helper graphics
----------------------

Theory-side helper artists that live in data coordinates, such as mode markers,
LVE envelopes, helper spectra, or editable bin boundaries, must also go through
the current view conversion path.

Recommended pattern inside a theory:

.. code-block:: python

   view = self.current_view()
   x, y, success = view.view_proc(data_table_tmp, file_parameters)
   x, y = self.convert_view_data_to_display(x, y, view)
   self.helper_artist.set_data(x, y)

If the helper artist is draggable, convert its dragged coordinates back before
using them to update theory parameters:

.. code-block:: python

   dx, dy = self.convert_view_data_to_internal(dx, dy)

This keeps helper graphics visually aligned with the selected display units
while preserving the theory's canonical internal parameterization.

Logarithmic theory parameters
-----------------------------

Parameters such as ``logwmin`` or ``logG00`` remain dimensionless and tied to
canonical internal units. RepTate currently does not change their displayed
numeric values when plot-axis units change.

If their interpretation depends on a reference unit, document that in the
parameter description or tooltip, for example "decimal logarithm of angular
frequency referenced to rad/s".
