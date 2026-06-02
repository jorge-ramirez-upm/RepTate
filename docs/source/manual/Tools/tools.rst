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

-------------------
Integral
-------------------

.. automodule:: RepTate.tools.ToolIntegral.ToolIntegral

-------------------
Smooth
-------------------

.. automodule:: RepTate.tools.ToolSmooth.ToolSmooth


-------------------
Power Law
-------------------

.. automodule:: RepTate.tools.ToolPowerLaw.ToolPowerLaw

------------------
Materials Database
------------------

.. automodule:: RepTate.tools.ToolMaterialsDatabase.ToolMaterialsDatabase

.. todo:: Give a short example of use of all the Tools
