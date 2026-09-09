======================
RepTate for developers
======================

Contents:

Native theory libraries
------------------------

Source developers can rebuild the RepTate-owned native theory libraries on
macOS, Linux, or Windows with::

   python scripts/build_native_libraries.py

Use ``--library bob`` to build one logical library or ``--check`` to verify
existing outputs without rebuilding. Release CI uses this same entry point on
all three platforms. Ordinary users installing a binary release do not need
to compile these libraries.

.. toctree::
   :maxdepth: 2

   functionality
   python_c_interface
   units
   code
   callgraphGUI
   workflow_map
   todo
