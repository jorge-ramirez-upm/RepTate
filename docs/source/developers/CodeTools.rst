Tools
=====

.. toctree::
   :maxdepth: 2

ToolBounds
----------

.. automodule:: RepTate.tools.ToolBounds
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

ToolEvaluate
------------

.. automodule:: RepTate.tools.ToolEvaluate
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

ToolFindPeaks
-------------

.. automodule:: RepTate.tools.ToolFindPeaks
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

ToolGradient
------------

.. automodule:: RepTate.tools.ToolGradient
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

ToolIntegral
------------

.. automodule:: RepTate.tools.ToolIntegral
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

ToolInterpolate
---------------

.. automodule:: RepTate.tools.ToolInterpolate
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

ToolMaterialsDatabase
---------------------

.. automodule:: RepTate.tools.ToolMaterialsDatabase
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

Unit-aware material parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Material unit metadata is defined in ``RepTate.tools.polymer_data``. The
Materials Database stores canonical internal values and marks converted
``polymer`` objects with ``MATERIAL_DATABASE_UNIT_SYSTEM``. Existing user
databases without that marker are migrated on load.

When applying material parameters to a theory, use
``ToolMaterialsDatabase.get_all_parameters()`` or the same conversion path:
database value in database internal units, then
``polymer_data.convert_database_value_to_parameter()`` for the target
``Parameter``. This is required for theories that intentionally keep a
different legacy internal unit.

ToolPowerLaw
------------

.. automodule:: RepTate.tools.ToolPowerLaw
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

ToolSmooth
----------

.. automodule:: RepTate.tools.ToolSmooth
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:
