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

.. autoclass:: RepTate.tools.ToolBounds.ToolBounds()

-------------------
Evaluate Expression
-------------------

.. autoclass:: RepTate.tools.ToolEvaluate.ToolEvaluate()

-------------------
Find Peaks
-------------------

.. autoclass:: RepTate.tools.ToolFindPeaks.ToolFindPeaks()

-------------------
Gradient
-------------------

.. autoclass:: RepTate.tools.ToolGradient.ToolGradient()

-------------------
Integral
-------------------

.. autoclass:: RepTate.tools.ToolIntegral.ToolIntegral()

-------------------
Smooth
-------------------

.. autoclass:: RepTate.tools.ToolSmooth.ToolSmooth()


-------------------
Power Law
-------------------

.. autoclass:: RepTate.tools.ToolPowerLaw.ToolPowerLaw()

------------------
Materials Database
------------------

.. autoclass:: RepTate.tools.ToolMaterialsDatabase.ToolMaterialsDatabase()
