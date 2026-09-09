======================
RepTate for developers
======================

Contents:

Native theory libraries
------------------------

Source developers can rebuild the RepTate-owned native theory libraries with::

   python scripts/build_native_libraries.py

Release CI uses this same entry point for native macOS builds. Ordinary users
installing a binary release do not need to compile these libraries.

.. toctree::
   :maxdepth: 2

   functionality
   python_c_interface
   units
   code
   callgraphGUI
   workflow_map
   todo
