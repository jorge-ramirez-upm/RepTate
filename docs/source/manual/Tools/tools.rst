=============
RepTate tools
=============

.. contents:: Contents
    :local:

.. toctree::
   :maxdepth: 2

The following tools are available in all applications. In general, the aim of the tools is to manipulate (filter, smooth, apply operations, integrate, differentiate, etc) or get information (statistics, peaks, etc) from the data as it is being represented in the current application and view. The tools can be applied to both the experimental data and the theory, or just to the experimental data. Several tools can be applied, and they are applied in sequence (in the same order as they are shown in the tool tab widget), to all the datasets and theories that are visible in the current application. If the user wants to apply the tools in a different order, he/she can drag the corresponding tab and drop it in the right position. 

------
Bounds
------

.. automodule:: RepTate.tools.ToolBounds.ToolBounds

The Bounds tool keeps only the points of the current view that fall within a
selected rectangular range. It is useful when a later tool or visual comparison
should use only part of the plotted data, for example before applying
``Integral`` or when excluding a low- or high-range region from the displayed
curve.

The tool acts on the coordinates produced by the selected view. If the view
plots logarithms, shifted variables, converted units, or derived quantities, the
limits are applied to those view coordinates rather than to the raw columns in
the original file.

The Bounds parameters are:

.. list-table::
   :header-rows: 1

   * - Parameter
     - Meaning
   * - ``xmin``
     - Minimum accepted x value
   * - ``xmax``
     - Maximum accepted x value
   * - ``ymin``
     - Minimum accepted y value
   * - ``ymax``
     - Maximum accepted y value

Only points with ``xmin < x < xmax`` and ``ymin < y < ymax`` are kept. The
default bounds are unbounded, so opening the tool does not remove points until
one or more limits are changed. RepTate checks that ``xmin`` is smaller than
``xmax`` and that ``ymin`` is smaller than ``ymax`` when the parameters are
edited.

-------------------
Evaluate Expression
-------------------

.. automodule:: RepTate.tools.ToolEvaluate.ToolEvaluate

The Evaluate Expression tool replaces the x- and y-values of the current view
with values computed from user-defined algebraic expressions. It is useful for
quick derived-coordinate checks, rescaling a plotted curve, comparing a
normalized quantity, or applying a simple transformation without changing the
original data file.

The tool acts on the coordinates produced by the selected view. In the
expressions, ``x`` is the current-view abscissa array and ``y`` is the
current-view ordinate array. If the view already plots logarithms, shifted
variables, converted units, or derived quantities, the expressions operate on
those displayed coordinates rather than on the raw file columns.

The Evaluate Expression parameters are:

.. list-table::
   :header-rows: 1

   * - Parameter
     - Meaning
   * - ``x``
     - Expression used to compute the output x-values
   * - ``y``
     - Expression used to compute the output y-values

The default expressions are ``x`` and ``y``, which leave the plotted data
unchanged. For example, set ``y = y/x`` to plot the current-view ordinate
divided by the current-view abscissa, or set ``x = log10(x)`` and ``y = y`` to
show the same y-values against :math:`\log_{10}(x)`.

Expressions may use numeric constants, the operators ``+``, ``-``, ``*``, ``/``,
``**``, and ``%``, unary signs, and the functions ``sin``, ``cos``, ``tan``,
``arcsin``, ``arccos``, ``arctan``, ``arctan2``, ``sinh``, ``cosh``, ``tanh``,
``arcsinh``, ``arccosh``, ``arctanh``, ``deg2rad``, ``rad2deg``, ``round``,
``around``, ``rint``, ``floor``, ``ceil``, ``trunc``, ``exp``, ``log``,
``log10``, ``fabs``, ``abs``, ``mod``, ``power``, and ``sqrt``. The constants
``pi`` and ``e`` are available. The helper functions ``randu(x)`` and
``randn(x)`` generate random arrays with the same shape as ``x``.

File parameters can be referenced with square brackets, for example
``[Mw]`` or ``[T]``. If a named file parameter is not present in a file, RepTate
uses ``0.0`` for that parameter in the expression.

The expression syntax is intentionally restricted. Function calls must be
direct calls to the supported functions, keyword arguments are not accepted, and
unknown names or unsupported syntax are rejected. If evaluating either
expression fails, RepTate prints the error in the tool output area and leaves
the input x- and y-values unchanged.

-------------------
Find Peaks
-------------------

.. automodule:: RepTate.tools.ToolFindPeaks.ToolFindPeaks

The Find Peaks tool identifies local maxima or minima. It acts on current-view
ordinate values and marks peaks on the plot. It is useful for quickly locating
peak positions, comparing peak shifts between files, or reading approximate
peak coordinates from the tool output area.

The tool acts on the coordinates produced by the selected view. The peak search
uses the displayed x- and y-values, so logarithms, shifted variables, converted
units, or derived quantities from the active view affect both the detected peak
positions and the reported coordinates. The original curve is kept unchanged;
the tool adds peak markers and prints the peak coordinates.

The Find Peaks parameters are:

.. list-table::
   :header-rows: 1

   * - Parameter
     - Meaning
   * - ``threshold``
     - Relative y-level used to reject small peaks
   * - ``minimum_distance``
     - Minimum separation between accepted peaks, in data points

By default, the tool searches for maxima. The toolbar ``Minimum peaks`` toggle
switches the search to minima by applying the same peak-detection logic to
``-y``. The ``Fit Parabola`` toggle optionally fits a parabola around each
detected peak and reports the analytical maximum or minimum of that fitted
parabola instead of the raw data point.

The threshold is interpreted relative to the current y-range. RepTate computes
``threshold * (max(y) - min(y)) + min(y)`` and keeps only maxima above that
level. For minima, the same calculation is applied after changing the sign of
``y``. For example, with the default ``threshold = 0.3``, maxima must be above
30 percent of the displayed y-span measured from the lowest displayed y-value.

The algorithm looks for sign changes in the first difference of the y-values.
Flat neighboring values are handled by borrowing nearby non-zero differences.
When several candidate peaks are closer than ``minimum_distance`` points, the
stronger peak is kept and nearby weaker candidates are rejected. If ``Fit
Parabola`` is enabled, ``minimum_distance`` also controls the number of points
around the detected data point used for the local parabolic fit.

The output area reports how many maxima or minima were found and, when at least
one is found, prints a table of ``x`` and ``y`` peak coordinates. The plot shows
the peaks as large diamond markers with the same face color as the processed
curve and a black edge.

Noisy data can produce many local extrema, and the
method can be inaccurate and slow in that case. Use ``Smooth`` before ``Find
Peaks`` when noise creates too many spurious peaks, or ``Bounds`` first when
only a restricted x or y range should be searched. The parabolic refinement is a
local numerical fit around each detected point; it can fail or give unreliable
coordinates if there are too few suitable neighboring points, repeated x-values,
or a poorly shaped local peak.

-------------------
Gradient
-------------------

.. automodule:: RepTate.tools.ToolGradient.ToolGradient

The Gradient tool replaces the y-values of the current view with the numerical
derivative :math:`dy/dx`. It is useful for inspecting local slopes, checking
power-law regions, or highlighting changes in a curve that are difficult to see
from the original plotted data.

The tool acts on the coordinates produced by the selected view. If the current
view uses logarithms, converted units, shifted data, or derived quantities, the
derivative is calculated with respect to those view coordinates. The x-values
are kept unchanged, and the plotted y-values become the numerical derivative.

The Gradient tool has no user parameters. It uses NumPy's gradient calculation:
central differences are used for interior points, and one-sided differences are
used at the boundaries. For noisy data, use ``Smooth`` before ``Gradient`` if a
smoother derivative is needed. For a derivative over a restricted range, apply
``Bounds`` before ``Gradient``.

The x-values should be ordered and should not contain problematic repeated
values. If the derivative calculation fails, the tool leaves the input data
unchanged.

-------------------
Integral
-------------------

.. automodule:: RepTate.tools.ToolIntegral.ToolIntegral

The Integral tool replaces the y-values of the current view with the cumulative
integral of y with respect to x. It is useful when the area under the displayed
curve is the quantity of interest, or when the integrated curve should be
compared between files or against a theory.

The tool acts on the coordinates produced by the selected view. If the current
view uses logarithms, converted units, shifted data, or derived quantities, the
integral is taken over those view coordinates. To integrate only part of a
curve, apply ``Bounds`` before ``Integral`` and set the desired x and y limits.

The Integral tool has no user parameters. Before integrating, repeated x-values
are removed. The remaining points are interpolated with a cubic spline, and the
cumulative integral is calculated over the x-values of the current view. The
plotted x-values are the unique x-values, and the plotted y-values are the
cumulative integral from the first retained x-value.

The final value of the cumulative integral is printed in the tool output area
as ``I``. If the interpolation or integration fails, the tool reports the error
and leaves the input data unchanged.

-----------------------
Interpolate/Extrapolate
-----------------------

.. automodule:: RepTate.tools.ToolInterpolate.ToolInterpolateExtrapolate

The Interpolate/Extrapolate tool evaluates the current-view curve at one
user-selected x-value and prints the corresponding y-value in the tool output
area. It is useful for reading an interpolated value from a curve without
manually estimating it from the plot.

The tool acts on the coordinates produced by the selected view. If the current
view uses logarithms, shifted variables, converted units, or derived
quantities, the interpolation is performed on those view coordinates. The tool
does not replace the plotted data; it returns the original x- and y-values
unchanged after printing the result.

The Interpolate/Extrapolate parameter is:

.. list-table::
   :header-rows: 1

   * - Parameter
     - Meaning
   * - ``x``
     - Current-view x-value at which y should be evaluated

Before interpolation, repeated x-values are removed by keeping the first
occurrence. The remaining points are passed to SciPy's ``interp1d`` with
``kind = "cubic"``, ``assume_sorted = True``, and
``fill_value = "extrapolate"``. This means values outside the data range are
extrapolated rather than rejected.

For example, set ``x = 10`` to print the interpolated or extrapolated y-value
at the displayed x-coordinate 10. The output area shows a small table with the
selected ``x`` and calculated ``y``.

The source data should be ordered by increasing x for the selected view. Cubic
interpolation can fail or give unreliable extrapolated values if there are too
few points, unsuitable repeated values, non-finite values, or if the requested
x-value is far outside the data range. If the calculation fails, RepTate prints
the error in the tool output area and leaves the plotted data unchanged.

-------------------
Smooth
-------------------

.. automodule:: RepTate.tools.ToolSmooth.ToolSmooth

The Smooth tool replaces the y-values of the current view with a
Savitzky-Golay smoothed curve. It is useful for reducing point-to-point noise
before visual comparison or before applying another tool that is sensitive to
noise, such as ``Gradient``.

The tool acts on the data produced by the selected view. The x-values are kept
unchanged, and only the y-values are filtered. If the view plots a logarithm,
converted unit, or derived quantity, the smoothing is applied to that
current-view y-coordinate.

The Smooth parameters are:

.. list-table::
   :header-rows: 1

   * - Parameter
     - Meaning
   * - ``window``
     - Number of points in the smoothing window
   * - ``order``
     - Polynomial order used inside the smoothing window

For example, the default values ``window = 11`` and ``order = 3`` smooth each
series using an 11-point window and a cubic polynomial. Increasing ``window``
gives stronger smoothing, while increasing ``order`` allows more curvature to
be preserved locally.

The ``window`` parameter must be a positive odd integer, must be larger than
``order``, and must be smaller than the number of y-values in the series. The
``order`` parameter must be non-negative and smaller than ``window``. If these
conditions are not satisfied, the tool reports the invalid setting and leaves
the data unchanged.

-------------------
Power Law
-------------------

.. automodule:: RepTate.tools.ToolPowerLaw.ToolPowerLaw

The Power Law tool divides the y-values of the current view by
:math:`x^n`. It is useful for checking whether a curve follows an approximate
power law. If the selected exponent is appropriate, a region where
:math:`y \propto x^n` appears approximately horizontal after the transformation.

The tool acts on the coordinates produced by the selected view. If the current
view uses logarithms, converted units, shifted data, or derived quantities, the
power-law division is applied to those view coordinates. The x-values are kept
unchanged, and the plotted y-values become :math:`y/x^n`.

The Power Law parameter is:

.. list-table::
   :header-rows: 1

   * - Parameter
     - Meaning
   * - ``n``
     - Power-law exponent used in :math:`y/x^n`

For example, set ``n = 2`` to check whether a selected range behaves as
:math:`y \propto x^2`. This tool does not fit ``n`` automatically; the user
chooses the exponent and inspects the transformed curve. Use ``Bounds`` before
``Power Law`` if the check should focus on a restricted x or y range.

Because the calculation divides by :math:`x^n`, zero or otherwise unsuitable
x-values can produce undefined or non-finite results. The tool does not apply
extra validity checks beyond the numerical calculation.

-------------
Resample Data
-------------

.. automodule:: RepTate.tools.ToolResampleData.ToolResampleData

The Resample Data tool replaces the current-view curve with an interpolated
curve on a new x-grid. It is useful for comparing curves on a common number of
points, preparing smoother-looking interpolated data, or placing several
displayed series on the same x-grid.

The tool acts on the coordinates produced by the selected view. For
multi-series views, RepTate converts the displayed coordinates to the view's
display representation before constructing the common resampling grid, and then
converts the resampled result back to the view's internal representation for
plotting. For single-series processing, the tool works directly on the x- and
y-values passed to the tool.

The Resample Data parameters and toolbar controls are:

.. list-table::
   :header-rows: 1

   * - Control
     - Meaning
   * - ``npoints``
     - Number of output points
   * - ``Method``
     - Interpolation method: ``PCHIP`` or ``Cubic spline``
   * - ``Scale``
     - Interpolation scale: ``Linear`` or ``Logarithmic``

The output x-grid is uniformly spaced in the selected scale. ``Linear`` uses
``linspace`` between the valid x-range limits. ``Logarithmic`` uses
``logspace`` and requires positive x-values. The default interpolation method
is ``PCHIP``. ``Cubic spline`` is also available, but it requires at least four
finite points with distinct x-values in each processed series.

Before interpolation, RepTate removes ``NaN`` and infinite points, sorts data by
x, and consolidates repeated x-values by averaging the corresponding y-values.
The tool reports how many invalid points were ignored and how many repeated
x-values were consolidated. It also reports the number of output points, the
interpolation method, and the scale.

For multi-series views, all displayed y-series must cover the common x-range
that RepTate constructs from the valid series ranges. The tool does not
extrapolate outside the valid x-range. For logarithmic interpolation, x-values,
y-values, and output x-values must all be positive. If any requirement is not
met, RepTate prints the error in the tool output area and leaves the input data
unchanged.

------------------
Materials Database
------------------

.. automodule:: RepTate.tools.ToolMaterialsDatabase.ToolMaterialsDatabase

The Materials Database tool lets the user inspect RepTate's polymer material
database and manage a personal material database. It is useful when a theory or
workflow needs standard polymer parameters such as WLF shift parameters,
entanglement time, entanglement modulus, entanglement molar mass, density, or
repeat-unit information.

This tool is not a current-view coordinate transformation like ``Bounds``,
``Smooth``, or ``Gradient``. Applying the tool to plotted data leaves the x- and
y-values unchanged. Its main output is the selected material information and
derived material calculations printed in the tool output area. Some theories
also use the same database helpers to initialize matching theory parameters
from a file's ``chem`` parameter.

The material selector lists the built-in RepTate material database followed by
materials from the user's database. User materials are shown in red. When the
tool opens, it tries to select the ``chem`` value from the first file in the
first dataset, if such a file parameter is available. Selecting a material
loads its parameters into the tool parameter table and shows the material's long
name above the tool controls.

The toolbar actions are:

.. list-table::
   :header-rows: 1

   * - Control
     - Meaning
   * - ``Calculate stuff with selected Mw/T``
     - Print derived WLF and tube-theory quantities for the selected material
   * - ``New Material``
     - Create a new user material from default values
   * - ``Edit/View Material Properties``
     - Edit the selected material, if it belongs to the user database
   * - ``Duplicate Material``
     - Copy the selected material into the user database under a new name
   * - ``Delete Material``
     - Delete the selected material, if it belongs to the user database
   * - ``Save User Material Database``
     - Save the user database to ``user_database.npy`` in the application data folder

Built-in materials can be viewed and duplicated, but they cannot be edited or
deleted. Editing and deleting are restricted to user materials. New and copied
materials are stored in memory until ``Save User Material Database`` is used.
RepTate also reads an older ``user_database.npy`` from the user's home folder
when present and merges it with the application-data user database.

The ``Mw (kDa)`` and ``T (°C)`` fields provide the molar mass and temperature
used by the calculation action. The calculation prints the selected chemistry,
``Mw``, ``T``, WLF quantities ``C1`` and ``C2``, adjusted ``tau_e`` and ``Ge``,
and the derived quantities ``Z``, ``tau_R``, and ``tau_D``. The
``Shift to isofrictional state`` and ``Vertical shift`` toggles affect these
calculations.

The ``Shift all Files in the current Application`` action asks for confirmation
and then shifts all files in the current dataset to the selected target
temperature using the selected material's WLF parameters. It updates file data
columns whose names are recognized by the source code: ``t`` or ``time`` are
divided by the horizontal shift factor, ``w`` is multiplied by it, and stress or
modulus columns such as ``G'``, ``G''``, ``Gt``, ``sigma_xy``, ``N1``,
``sigma``, are multiplied by the vertical shift factor when vertical shifting is
enabled. The file parameter ``T`` is then set to the target temperature.

Use care with the shift action because it modifies the data tables in the
current dataset. It expects the files to contain suitable ``T`` and ``Mw`` file
parameters and only shifts columns with the names listed above. Materials or
parameters that are not present in the selected material cannot be supplied
automatically to theories.
