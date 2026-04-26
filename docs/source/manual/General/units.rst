.. _units:

-----
Units
-----

RepTate can read, display, and convert units for the parts of the program that
have been made unit-aware. This page describes the user-visible behavior and the
current coverage.

Supported units
---------------

The supported unit quantities are:

.. list-table::
   :header-rows: 1

   * - Quantity
     - Supported input/display units
     - Internal unit used by RepTate
   * - Time
     - ``ns``, ``μs``, ``ms``, ``s``, ``min``, ``h``
     - ``s``
   * - Angular frequency
     - ``rad/s``
     - ``rad/s``
   * - Frequency
     - ``Hz``
     - ``Hz`` when used as frequency, or converted to ``rad/s`` for angular-frequency data
   * - Stress or modulus
     - ``Pa``, ``kPa``, ``MPa``, ``bar``, ``atm``
     - ``Pa``
   * - Viscosity
     - ``Pa.s``, ``kPa.s``
     - ``Pa.s``
   * - Temperature
     - ``K``, ``ºC``, ``°C``
     - ``K`` for unit-aware calculations
   * - Molecular mass
     - ``kg/mol``, ``g/mol``
     - ``kg/mol``
   * - Dimensionless
     - ``-``
     - ``-``

In practice, this means that a data file may contain, for example, time in
``s`` or ``min``, modulus in ``Pa``, ``kPa``, or ``MPa``, pressure in ``Pa``,
``bar``, or ``atm``, molecular mass in ``kg/mol`` or ``g/mol``, and temperature
in ``K`` or ``ºC`` where the corresponding importer or parameter is unit-aware.

Specifying units in data files
------------------------------

For unit-aware text files, units can be written in the column header using
square brackets or parentheses:

.. code-block:: text

   Mw=100;T=25;
   w [Hz] G' [kPa] G'' [kPa]
   0.1 12.0 3.0
   1.0 25.0 8.0

If the file header does not include units, RepTate uses the default units
declared by the selected application file type. For example, LVE files expect
angular frequency and moduli, while MWD files expect molecular mass and
distribution columns.

Unknown unit strings are kept as legacy labels and the numbers are not
converted. This preserves old files, but it also means that only the supported
units listed above are converted automatically.

How units appear in RepTate
---------------------------

Unit-aware data columns are converted when the file is imported. Plot axes show
the internal unit when a view axis directly corresponds to a data column. For
example, a column loaded as ``time [min]`` is plotted as ``time [s]`` after
conversion.

Unit-aware file parameters, such as selected ``T`` and ``Mw`` parameters, are
stored internally in RepTate's internal units and displayed in their configured
display units. Unit-aware theory parameters show the unit in the parameter
table, and the theory parameter dialog lets users choose among compatible
display units.

Saved or exported data should currently be treated with care. Some exported
tables contain converted internal values but do not yet consistently write unit
annotations in the output header. This is listed below as a current limitation.

Frequency and angular frequency
-------------------------------

Frequency in ``Hz`` and angular frequency in ``rad/s`` are not treated as
interchangeable units. When an application expects angular frequency but the
input column is declared as ``Hz``, RepTate converts using

.. math::

   \omega = 2\pi f

The reverse relation is used only at explicit conversion boundaries. Generic
unit conversion does not silently treat ``Hz`` and ``rad/s`` as the same
quantity.

Temperature
-----------

Temperature conversion is affine. For example, ``25 ºC`` is converted to
``298.15 K`` for unit-aware calculations. Legacy rheology applications that have
historically used Celsius file parameters still display those file parameters in
``ºC`` where the corresponding file parameter is unit-aware.

Logarithmic quantities
----------------------

Parameters such as ``logwmin``, ``logwmax``, ``logG01``, or ``logM0`` should be
read as dimensionless decimal logarithms of an underlying dimensional quantity,
not as quantities that have units themselves.

For example, ``logG01`` represents :math:`\log_{10}(G_{01}/G_\mathrm{unit})`.
Changing the display unit of the underlying dimensional quantity changes the
displayed logarithmic value by an additive shift. For example, changing a
stress scale from ``Pa`` to ``kPa`` subtracts 3 from the displayed
:math:`\log_{10}` value. Changing molecular mass from ``kg/mol`` to ``g/mol``
adds 3.

Current legacy logarithmic theory parameters are not yet all unit-aware. When no
unit metadata is attached to a logarithmic parameter, RepTate displays and saves
the stored dimensionless logarithmic value without unit conversion.

Current unit-awareness coverage and limitations
-----------------------------------------------

The tables below are based on the current code. An application or theory is
listed as unit-aware only when it contains explicit unit metadata or uses a
unit-aware importer with supported units.

Unit-aware applications
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Application
     - Unit-aware items
   * - Creep
     - Text data columns; file parameter ``T``
   * - Crystal
     - Text data columns where units are supported; file parameter ``T``
   * - Dielectric
     - Text data columns; file parameter ``T``
   * - FRS
     - Text data columns with supported units
   * - Gt
     - Text data columns with supported units
   * - LAOS
     - Text data columns; file parameters ``omega`` and ``gamma``
   * - LVE
     - Text data columns; file parameters ``Mw`` and ``T``
   * - MWD
     - Text data columns for molecular mass distributions
   * - NLVE
     - Text data columns; file parameter ``T``
   * - React
     - Text data columns for molecular mass distributions
   * - TTS
     - Text data columns; file parameter ``T``
   * - TTS Factors
     - Text data columns with supported units

Partially unit-aware or unknown applications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Application
     - Current limitation
   * - SANS
     - Uses legacy scattering-vector labels such as ``1/A``; those units are not registered for conversion
   * - Universal Viewer
     - Units come from the user configuration file; conversion coverage depends on whether those strings match supported units

Applications not yet unit-aware
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Application
     - Current limitation
   * - Template
     - Placeholder units are not registered and are not converted

Unit-aware theories
^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Theory
     - Coverage
   * - Carreau-Yasuda
     - All detected parameters include unit metadata
   * - DTD Stars
     - All detected parameters include unit metadata
   * - PETS
     - All detected parameters include unit metadata
   * - Rouse
     - All detected parameters include unit metadata
   * - Sticky Reptation
     - All detected parameters include unit metadata

Partially unit-aware theories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Theory
     - Coverage
   * - Diene CSTR
     - Some parameters include unit metadata
   * - Giesekus
     - Some parameters include unit metadata
   * - GO PolySTRAND
     - Some parameters include unit metadata
   * - LDPE Batch
     - Some parameters include unit metadata
   * - Likhtman-McLeish 2002
     - Some parameters include unit metadata
   * - Multi Metallocene CSTR
     - Some parameters include unit metadata
   * - Pom-Pom
     - Some parameters include unit metadata
   * - RDP LVE
     - Some parameters include unit metadata
   * - Rolie Double Poly
     - Some parameters include unit metadata
   * - Rolie-Poly
     - Some parameters include unit metadata
   * - SCCR
     - Some parameters include unit metadata
   * - Smooth PolySTRAND
     - Some parameters include unit metadata
   * - Tobita CSTR
     - Some parameters include unit metadata
   * - UCM
     - Some parameters include unit metadata

Theories not yet unit-aware
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Theory
   * - Arrhenius
   * - Basic theories
   * - BoB LVE
   * - BoB NLVE
   * - Create Polyconf
   * - Debye
   * - Debye Modes
   * - Discretize MWD
   * - DSM Linear
   * - GEX
   * - Havriliak-Negami Modes
   * - KWW Modes
   * - Log-Normal
   * - Maxwell Modes
   * - React Mix
   * - Retardation Modes
   * - Shanbhag Maxwell Modes
   * - Template theory
   * - TTS
   * - TTS Automatic
   * - WLF

Other current limitations
^^^^^^^^^^^^^^^^^^^^^^^^^

* Unit conversion is implemented for text column files. Excel import is not yet
  unit-aware.
* Plot axis labels use column metadata only when the view axis label directly
  matches an imported data column. Derived views may still show the view's
  legacy unit string.
* Compound units outside the registered list, such as SANS ``1/A`` and several
  inverse or mixed units, are not converted.
* File parameters are unit-aware only when the application declares explicit
  metadata for that parameter.
* Theory parameters are unit-aware only when that theory declares explicit
  metadata for that parameter.
* Saved datasets, saved views, and some theory-specific exports do not yet
  consistently include unit annotations or convert values back to display units.
