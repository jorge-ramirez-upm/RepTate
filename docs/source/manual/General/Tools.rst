-----------------------
Using the Tools
-----------------------

Tools are opened from the tools area of an application window. Select the tool
from the tool drop-down list and press the ``New Tool`` button. A new tab is
added to the tools panel, and the plot is updated immediately using the new
tool.

Tools operate on the data shown in the current application views. For each
visible file, RepTate first calculates the selected view and then applies the
active tools in the order shown by the tool tabs. The transformed data are then
plotted. If theories are visible, the same tool sequence is also applied to the
theory curves when the tool's ``Apply to Theory`` toggle is enabled.

Each tool tab contains its own parameter table and output text area. Changing a
parameter value updates the plots. The ``Active`` toggle enables or disables the
tool without deleting it. Closing the tab removes the tool from the application.

When several tools are open, their order matters. For example, applying
``Bounds`` before ``Integral`` restricts the data range before the integral is
calculated, while applying the tools in the opposite order integrates first and
then filters the plotted result. Tool tabs can be dragged to reorder the tool
sequence; RepTate recalculates the plots after the order is changed.

Tools work on the coordinates of the current view, not necessarily on the raw
columns stored in the data file. If the selected view uses logarithms,
converted units, or derived quantities, the tool receives those displayed-view
coordinates.

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
