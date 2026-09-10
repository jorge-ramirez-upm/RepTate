======================
RepTate for developers
======================

Contents:

Native theory libraries
------------------------

RepTate contains several native libraries used by theories through ``ctypes``.
Source developers can rebuild the RepTate-owned libraries on macOS, Linux, or
Windows with the supported build script::

   python scripts/build_native_libraries.py

Use ``--library bob`` to build one logical library or ``--check`` to verify
existing outputs without rebuilding. The script rebuilds the selected libraries
in place, so a developer changing native C or C++ code should rebuild the
affected libraries and validate the change through CI.

Official CI and release packages always rebuild native libraries from source;
those freshly built CI outputs are the authoritative validation path for
releases. Precompiled native binaries remain checked into the repository for
the convenience of source users and developers who do not have a local
compiler. Ordinary users of downloadable binary packages do not need gcc,
g++, MinGW, Xcode, or another compiler.

Local native-library rebuilds require a suitable toolchain: gcc/g++ on Linux,
MinGW-style gcc/g++ on Windows as supported by the script, and Apple Clang
provided by the Xcode command-line tools on macOS.

.. toctree::
   :maxdepth: 2

   functionality
   python_c_interface
   units
   code
   callgraphGUI
   workflow_map
   todo
