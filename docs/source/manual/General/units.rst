.. _units:

-----
Units
-----

RepTate can now read, store, display, and convert units for the parts of the
program that have been made unit-aware. This page describes the current
user-visible behavior and the present coverage in applications and theories.

General behavior
----------------

RepTate keeps numerical values internally in canonical units whenever explicit
unit metadata are available. Conversion happens only at input and output
boundaries:

* when reading text-column data files
* when reading unit-aware file parameters from the first line of a text file
* when displaying file parameters in a Dataset
* when displaying or editing unit-aware theory parameters
* when displaying or editing unit-aware tool parameters
* when applying unit-aware Materials Database values to theory parameters

If no unit metadata exist for a given column, file parameter, or theory
parameter, RepTate preserves the legacy numerical convention and no automatic
conversion is applied.

View axes
---------

RepTate views can also be unit-aware. When a view axis has explicit metadata,
RepTate keeps the numerical data in canonical internal units and converts the
plotted coordinates to the currently selected display unit only at plotting
time.

For unit-aware view axes:

* the default axis unit is the canonical RepTate unit for that quantity
* right-clicking on a plot opens axis-unit menus for the current view when
  compatible alternative units are available
* changing the axis unit affects the plotted coordinates and axis label, but
  does not alter the stored data or theory parameters

This currently works best for axes that represent a single physical quantity.
Mixed axes, such as plots combining stress and dimensionless quantities on the
same axis, remain only partially unit-aware.

Supported quantities and canonical units
----------------------------------------

The current unit registry supports the following quantities.

.. list-table::
   :header-rows: 1

   * - Quantity
     - Registered units
     - Canonical internal unit
   * - Time
     - ``ns``, ``μs``, ``ms``, ``s``, ``min``, ``h``
     - ``s``
   * - Deformation rate
     - ``1/s``, ``s-1``, ``s^-1``, ``s⁻¹``, ``1/min``, ``min-1``, ``1/h``, ``h-1``
     - ``1/s``
   * - Inverse distance
     - ``1/A``, ``1/Å``, ``A-1``, ``Å-1``, ``1/nm``, ``1/um``, ``1/μm``, ``1/mm``, ``1/cm``, ``1/m``
     - ``1/A``
   * - Nucleation rate
     - ``1/s/m3``, ``1/m3/s``, ``1/s/cm3``, ``1/cm3/s``, ``1/s/mm3``, ``1/mm3/s``, ``1/s/μm3``, ``1/μm3/s``, ``1/s/nm3``, ``1/nm3/s``
     - ``1/s/m3``
   * - Linear rate
     - ``m/s``, ``m/min``, ``m/h``, ``cm/s``, ``mm/s``, ``um/s``, ``μm/s``, ``nm/s``
     - ``m/s``
   * - Unit density
     - ``1/m3``, ``1/L``, ``1/cm3``, ``1/mL``, ``1/mm3``, ``1/um3``, ``1/μm3``, ``1/nm3``
     - ``1/m3``
   * - Angular frequency
     - ``rad/s``
     - ``rad/s``
   * - Frequency
     - ``Hz``
     - ``Hz``
   * - Stress or modulus
     - ``Pa``, ``kPa``, ``MPa``, ``bar``, ``atm``
     - ``Pa``
   * - Compliance
     - ``1/Pa``, ``1/kPa``, ``1/MPa``, ``1/bar``, ``1/atm``
     - ``1/Pa``
   * - Viscosity
     - ``Pa.s``, ``kPa.s``
     - ``Pa.s``
   * - Angle
     - ``rad``, ``deg``
     - ``rad``
   * - Density
     - ``kg/m3``, ``kg/m^3``, ``kg/m³``, ``g/cm3``, ``g/cm^3``, ``g/cm³``, ``g/cc``, ``g/mL``, ``kg/L``
     - ``kg/m3``
   * - Inverse temperature
     - ``1/K``, ``K^-1``, ``K⁻¹``
     - ``1/K``
   * - Temperature
     - ``K``, ``ºC``, ``°C``
     - ``K``
   * - Molecular mass
     - ``kg/mol``, ``g/mol``, ``Da``, ``kDa``
     - ``kg/mol``
   * - Dimensionless
     - ``-``
     - ``-``

Many quantities also accept equivalent ASCII, superscript, and Unicode variants
of the same symbol, for example ``1/m^3`` and ``1/m³``.

Specifying units in data files
------------------------------

For unit-aware text files, units can be specified in two places.

Column headers
^^^^^^^^^^^^^^

Column headers may include units in square brackets or parentheses:

.. code-block:: text

   Mw=100 kg/mol;T=25 ºC;
   w [Hz] G' [kPa] G'' [kPa]
   0.1 12.0 3.0
   1.0 25.0 8.0

If the file header does not include units for a column, RepTate uses the
default ``col_units`` declared by the selected application file type.

File parameters on the first line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first line of a text file may also include units on individual file
parameters:

.. code-block:: text

   Mw=1131 Da;T=25 ºC;gdot=0.1 1/s;

If a file parameter is unit-aware in the corresponding application,
RepTate converts that value to the internal canonical unit when the file is
loaded. Legacy unitless headers such as ``Mw=1131;T=25;`` still work.

Unknown unit strings
^^^^^^^^^^^^^^^^^^^^

Unknown unit strings are preserved as legacy labels and the corresponding
numbers are not converted. This preserves old files, but automatic conversion
only applies to registered units.

How units appear in RepTate
---------------------------

Data columns
^^^^^^^^^^^^

Unit-aware data columns are converted to canonical internal units when the file
is imported. When a plotted axis directly corresponds to an imported column,
that axis uses the column metadata. Unit-aware derived views may also declare
their own axis metadata explicitly, so view axes can stay consistent even when
the plotted quantity is not a direct copy of an imported column.

File parameters in a Dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unit-aware file parameters are stored internally in their canonical units and
displayed in the parameter's configured display unit.

When a Dataset column corresponds to a unit-aware file parameter, right-clicking
that column header opens a pop-up menu listing all registered compatible units
for that quantity. Choosing one changes the display unit for that parameter in
that Dataset and updates all file rows in that Dataset.

Theory parameters
^^^^^^^^^^^^^^^^^

Unit-aware theory parameters show their display unit in the theory parameter
table. The theory parameter editor lets users choose among compatible display
units when that theory parameter carries explicit unit metadata.

For logarithmic theory parameters such as ``logwmin`` or ``logG00``, the
stored value remains dimensionless and tied to the canonical internal unit
system used by the theory. RepTate does not currently change those displayed
numbers when plot-axis units are changed. Instead, their meaning should be
documented in the parameter description or tooltip.

Tool parameters
^^^^^^^^^^^^^^^

Unit-aware tool parameters follow the same display/editing convention as theory
parameters. The tool table shows the display unit in the parameter label, stores
the numerical value in the parameter's internal unit, and converts values typed
by the user from the display unit back to the internal unit.

Double-clicking a tool parameter name opens a tool-parameter properties dialog.
For unit-aware parameters, the dialog offers compatible display units from the
unit registry.

Materials Database
^^^^^^^^^^^^^^^^^^

The Materials Database keeps common material parameters in internal units and
converts them when applying them to a theory. This is important because some
legacy theories still use historical internal conventions. For example,
``DSM Linear`` displays ``MK`` and ``Mc`` in ``Da`` and converts those values to
the units expected by its legacy formulas, while the database stores molar
masses internally in ``kg/mol``.

The following Materials Database fields are unit-aware: ``tau_e`` in ``s``,
``Ge`` in ``Pa``, ``Me`` in ``kg/mol``, ``rho0`` in ``kg/m3``, ``M0`` and
``MK`` in ``kg/mol``, and the WLF temperature fields ``B2`` and ``Te`` in
``°C``.

Theory helper graphics
^^^^^^^^^^^^^^^^^^^^^^

Theory-side helper graphics that are plotted in data coordinates, such as
mode markers, LVE envelopes, helper spectra, or discretized-MWD markers, now
follow the current display units of the active view. RepTate converts those
helper coordinates from internal units to display units before plotting them.

When such helper graphics are draggable, the dragged coordinates are converted
back to internal units before theory parameters are updated.

Frequency and angular frequency
-------------------------------

Frequency in ``Hz`` and angular frequency in ``rad/s`` are intentionally
different quantities.

When an application expects angular frequency but an imported column is declared
as ``Hz``, RepTate performs the explicit boundary conversion

.. math::

   \omega = 2\pi f

The reverse relation is only used at explicit import/export boundaries.
Generic unit conversion does not treat ``Hz`` and ``rad/s`` as the same
quantity.

Temperature
-----------

Temperature conversion is affine rather than purely multiplicative. For
example, ``25 ºC`` is converted to ``298.15 K`` in the canonical temperature
system.

Some legacy rheology applications and theories still keep temperature parameters
internally in ``ºC`` because their numerical code has not yet been migrated to
canonical ``K``. The tables below reflect the code as it currently exists.

Logarithmic quantities
----------------------

Parameters such as ``logwmin``, ``logwmax``, ``logG01``, or ``logM0`` should be
read as dimensionless decimal logarithms of an underlying dimensional quantity,
not as dimensional quantities themselves.

For example, ``logG01`` represents :math:`\log_{10}(G_{01}/G_\mathrm{unit})`.
RepTate currently keeps these displayed parameter values fixed and tied to the
canonical internal unit system rather than shifting them when plot-axis units
change.

Current use in applications
---------------------------

The table below summarizes the current state of the application layer.

.. list-table::
   :header-rows: 1

   * - Application
     - Current unit-aware coverage
   * - FRS
     - Text columns use declared ``col_units``; file parameters remain legacy
   * - Creep
     - Text columns; file parameters ``Mw``, ``stress``, and ``T``; unit-aware view axes for time, compliance, viscosity, frequency, and stress
   * - Crystal
     - Text columns; file parameters ``gdot``, ``T``, and ``tstop``; unit-aware view axes for time, viscosity, stress, deformation rate, nucleation rate, and number density
   * - Dielectric
     - Text columns; file parameters ``Mw`` and ``T``
   * - Gt
     - Text columns; file parameters ``Mw`` and ``gamma``; unit-aware view axes for time, frequency, and modulus
   * - LAOS
     - Text columns; file parameters ``omega`` and ``gamma``; unit-aware view axes for time, stress, deformation rate, viscosity, and FFT frequency where the plotted quantity is unambiguous
   * - LVE
     - Text columns in ``tts`` and ``osc`` files; file parameters ``Mw`` and ``T``; unit-aware view axes for frequency, stress, viscosity, and compliance. The Excel importer remains separate from the unit-aware text-column path
   * - MWD
     - Text columns; file parameters ``Mn`` and ``Mw``; unit-aware view axes for molar mass
   * - NLVE
     - Text columns; file parameter ``T``. The flow-rate file parameter is still legacy, but main view axes are unit-aware for time, viscosity, stress, and deformation rate
   * - React
     - Text columns use declared units; file parameters remain legacy; unit-aware view axes for molar mass and branch-segment molar mass
   * - SANS
     - Text columns, including inverse-distance units such as ``Å⁻¹``; file parameters ``Mw`` and ``phi``; unit-aware inverse-distance axes for ``I(q)``, ``log(I(q))``, and ``Kratky``
   * - TTS
     - Text columns; file parameters ``Mw`` and ``T``; unit-aware view axes for frequency, stress, viscosity, and compliance
   * - TTS Factors
     - Text columns; file parameter ``Mw``; unit-aware view axes for temperature and inverse temperature
   * - Universal Viewer
     - Text columns can participate when the configured unit strings match the registry
   * - Template
     - Placeholder example only; its default unit strings are not intended for conversion

Current use in theories
-----------------------

Theory coverage is heterogeneous. Many theories now attach unit metadata to
some or all user-editable parameters, but this is not yet universal.

Theories with explicit unit metadata on at least one parameter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Theory
     - Notes
   * - Arrhenius
     - Temperature metadata present
   * - Carreau-Yasuda
     - Explicit metadata on main fit parameters
   * - Debye
     - Explicit metadata on selected parameters
   * - Diene CSTR
     - Explicit metadata on selected parameters
   * - DSM Linear
     - Explicit metadata on selected parameters
   * - DTD Stars
     - Explicit metadata on main parameters
   * - Giesekus
     - Explicit metadata on selected parameters
   * - GO PolySTRAND
     - Extensive metadata coverage
   * - LDPE Batch
     - Explicit metadata on selected parameters
   * - Likhtman-McLeish 2002
     - Explicit metadata on selected parameters
   * - Multi Metallocene CSTR
     - Explicit metadata on selected parameters
   * - PETS
     - Explicit metadata on main parameters
   * - Pom-Pom
     - Explicit metadata on selected parameters
   * - RDPLVE
     - Explicit metadata on selected parameters
   * - Rolie Double Poly
     - Explicit metadata on selected parameters
   * - Rolie-Poly
     - Explicit metadata on selected parameters
   * - Rouse
     - Explicit metadata on main parameters
   * - SCCR
     - Explicit metadata on selected parameters
   * - Smooth PolySTRAND
     - Extensive metadata coverage
   * - Sticky Reptation
     - Explicit metadata on main parameters
   * - Tobita CSTR
     - Explicit metadata on selected parameters
   * - TTS
     - Temperature metadata present
   * - TTS Automatic
     - Temperature metadata present
   * - UCM
     - Explicit metadata on selected parameters
   * - WLF
     - Temperature metadata present

Theories without explicit parameter-unit metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Theory
   * - Basic theories
   * - BoB LVE
   * - BoB NLVE
   * - Create Polyconf
   * - Debye Modes
   * - Discretize MWD
   * - GEX
   * - Havriliak-Negami Modes
   * - KWW Modes
   * - Log-Normal
   * - Maxwell Modes
   * - React Mix
   * - Retardation Modes
   * - Shanbhag Maxwell Modes
   * - Template theory

Important limitations
---------------------

* Unit conversion is implemented for text-column importers. Excel import is not
  yet generally unit-aware.
* A theory having explicit parameter metadata does not imply that every
  parameter in that theory has been migrated.
* Many legacy rheology theories still use Celsius internally for temperature
  parameters even though the canonical temperature unit in the registry is
  ``K``.
* File parameters are unit-aware only when the application declares explicit
  ``FileParameterSpec`` metadata for that parameter.
* Theory parameters are unit-aware only when that theory declares explicit
  ``quantity``, ``internal_unit``, and ``display_unit`` metadata.
* Tool parameters are unit-aware only when that tool declares explicit
  ``quantity``, ``internal_unit``, and ``display_unit`` metadata.
* Materials Database values are stored in internal units, but temperature-shift
  formulas for WLF-style parameters still use the established Celsius
  convention.
* Saved datasets, saved views, and some theory-specific exports do not yet
  consistently include unit annotations or convert values back to display
  units.
