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

Tool Parameter Metadata
-----------------------

Tool parameters use the same ``Parameter`` class and unit metadata as theory
parameters. ``QTool`` displays ``Parameter.display_label()`` and
``Parameter.display_value()`` in the tool parameter table, and converts values
entered by the user through ``Parameter.value_from_display()``.

Double-clicking a tool parameter name opens the tool-parameter properties
dialog. If a parameter defines ``quantity``, ``internal_unit`` and
``display_unit``, compatible display units are populated from the unit registry.

When adding a unit-aware tool parameter, follow the same rule used for
theories: numerical tool calculations must use ``Parameter.value`` in
``internal_unit`` and conversion must remain at the GUI boundary.

Materials Database
------------------

The Materials Database is unit-aware through metadata in
``RepTate.tools.polymer_data``. Built-in and user material databases are
canonicalized on load with ``canonicalize_database()``. New material database
files should be saved with values already converted to internal units and with
``polymer.unit_system`` set to ``MATERIAL_DATABASE_UNIT_SYSTEM``.

Current unit-aware material fields are:

.. list-table::
   :header-rows: 1

   * - Field
     - Internal unit
     - Legacy/display unit
   * - ``tau_e``
     - ``s``
     - ``s``
   * - ``Ge``
     - ``Pa``
     - ``Pa``
   * - ``Me``
     - ``kg/mol``
     - ``kg/mol`` or legacy ``kDa``
   * - ``rho0``
     - ``kg/m3``
     - ``g/cm3``
   * - ``M0``
     - ``kg/mol``
     - ``g/mol``
   * - ``MK``
     - ``kg/mol``
     - ``Da``
   * - ``B2``
     - ``°C``
     - ``°C``
   * - ``Te``
     - ``°C``
     - ``°C``

``ToolMaterialsDatabase.get_all_parameters()`` applies
``convert_database_value_to_parameter()`` before assigning a database value to a
theory parameter. This lets a database field stored in canonical units feed a
legacy theory whose parameter intentionally declares a different internal unit.

Do not bypass this conversion when importing material parameters into a theory.
If a theory needs a derived material parameter, obtain the database value in
internal database units and explicitly convert it to the target theory
parameter's internal unit before assignment.

Temperature caveat
^^^^^^^^^^^^^^^^^^

The canonical registry unit for temperature is ``K``, but WLF-style material
parameters ``B2`` and ``Te`` are stored as ``°C`` because the existing WLF shift
equations are written in Celsius differences and Celsius offsets. Do not change
those fields to Kelvin unless all WLF formulas that use them are migrated at
the same time.

Legacy theory formulas
^^^^^^^^^^^^^^^^^^^^^^

Some theories still use historical numerical conventions internally even though
their parameters are unit-aware. Keep conversions local and explicit. For
example, ``TheoryDSMLinear`` declares ``MK`` and ``Mc`` as molar masses stored
in ``kg/mol`` but converts them to ``Da`` inside the DSM formulas, because the
legacy equations also convert file ``Mw`` to ``Da``.

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
