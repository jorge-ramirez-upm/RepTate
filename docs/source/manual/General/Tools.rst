-----------------------
Using the Tools
-----------------------

- Opening a New Tool
- How the Tooks work
- Shuffling the Tools

.. todo:: Complete this section

Tool parameters
---------------

Tools use the same parameter-table conventions as theories. If a tool
parameter has unit metadata, the parameter table shows the current display unit
next to the parameter name and converts edited values back to the internal unit
used by the calculation.

Double-clicking a tool parameter value edits the value directly. Double-clicking
the parameter name opens the tool-parameter properties dialog. This dialog
allows the user to inspect the parameter type, optimization state, display flag,
bounds, and unit metadata. When compatible units are registered for a
unit-aware parameter, the ``display_unit`` field is shown as a list of allowed
display units.

Materials Database
------------------

The Materials Database stores recommended polymer material parameters and is
used by several theories to initialise parameters from the chemistry name
stored in a data file. If the first file in a dataset contains a ``chem`` file
parameter and the chemistry exists in the user or built-in database, compatible
theory parameters are filled automatically.

The Materials Database is unit-aware for the common material parameters:

.. list-table::
   :header-rows: 1

   * - Parameter
     - Meaning
     - Internal unit
     - Default display unit
   * - ``tau_e``
     - Entanglement time
     - ``s``
     - ``s``
   * - ``Ge``
     - Entanglement modulus
     - ``Pa``
     - ``Pa``
   * - ``Me``
     - Entanglement molar mass
     - ``kg/mol``
     - ``kg/mol``
   * - ``rho0``
     - Melt density at 0 °C
     - ``kg/m3``
     - ``g/cm3``
   * - ``M0``
     - Repeating-unit molar mass
     - ``kg/mol``
     - ``g/mol``
   * - ``MK``
     - Kuhn-step molar mass
     - ``kg/mol``
     - ``Da``
   * - ``B2``
     - WLF temperature parameter
     - ``°C``
     - ``°C``
   * - ``Te``
     - Temperature at which tube parameters were measured
     - ``°C``
     - ``°C``

Older material databases that stored values in legacy display units are
converted when they are loaded. For example, ``MK = 140.5 Da`` is stored
internally as ``0.1405 kg/mol`` and displayed as ``140.5 Da`` when the display
unit is ``Da``. When a theory requests a material parameter, RepTate converts
the database value to the theory parameter's declared internal unit before
setting the theory parameter.

The temperature-dependent parameters ``tau_e``, ``Ge``, and ``rho0`` are shifted
from the database reference temperature using the file temperature ``T`` when
available. If the file has no usable ``T`` parameter, these temperature-shifted
values are not imported.
