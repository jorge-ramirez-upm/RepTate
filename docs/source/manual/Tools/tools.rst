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

-------------------
Find Peaks
-------------------

.. automodule:: RepTate.tools.ToolFindPeaks.ToolFindPeaks

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

------------------
Materials Database
------------------

.. automodule:: RepTate.tools.ToolMaterialsDatabase.ToolMaterialsDatabase

.. todo:: Give a short example of use of all the Tools
