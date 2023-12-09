===================
Code Class Diagrams
===================

Inheritance Diagrams
====================

Basic Classes
-------------

The following scheme shows the class inheritance diagram of the most imporatant classes in RepTate. Most of them are children of the CmdBase class. In the diagram:

   - Empty ellipses represent **core classes**. Their source code can be found in the ``core`` folder and are they provide the basic functionality.

   - Grey filled rounded boxes represent the RepTate central **GUI classes**. Each GUI class is derived from a PyQt object (either QWidget or QMainWindow).

   - Green filled boxes represent **PySide6** classes. Many PySide6 classes are used within the RepTate code. In the diagram, only two of the most important are shown.

   - Green arrows represent inheritance. The arrow goes **from the parent class to the child class**.

   - Red arrows represent **composition**. The arrow goes **from the container class to the contained class**.

.. graphviz::

   digraph foo {
      "QApplicationWindow" [href="../developers/CodeCoreGUI.html#qapplicationwindow", target="_top", shape="box", style="rounded,filled"]
      "QApplicationManager" [href="../developers/CodeCoreGUI.html#qapplicationmanager", target="_top", shape="box", style="rounded,filled"]
      "QDataSet" [href="../developers/CodeCoreGUI.html#qdataset", target="_top", shape="box", style="rounded,filled"]
      "QTheory" [href="../developers/CodeCoreGUI.html#qtheory", target="_top", shape="box", style="rounded,filled"]
      "QTool" [href="../developers/CodeCoreGUI.html#qtool", target="_top", shape="box", style="rounded,filled"]
      "QWidget" [shape=box,fillcolor=palegreen,href="https://doc.qt.io/qt-5/qwidget.html", target="_top", style="filled"]
      "QMainWindow" [shape=box,fillcolor=palegreen,href="https://doc.qt.io/qt-5/qmainwindow.html", target="_top", style="filled"]
      "QWidget" -> "QApplicationWindow" [color=green];
      "QWidget" -> "QDataSet" [color=green];
      "QWidget" -> "QTheory" [color=green];
      "QWidget" -> "QTool" [color=green];
      "QMainWindow" -> "QApplicationManager" [color=green];
      "QApplicationManager" -> "QApplicationWindow" [color=red];
      "QApplicationWindow" -> "QDataSet" [color=red];
      "QApplicationWindow" -> "QTool" [color=red];
      "QDataSet" -> "QTheory" [color=red];
      "View" [href="../developers/CodeCoreCL.html#view", target="_top"]
      "FileType" [href="../developers/CodeCoreCL.html#filetype", target="_top"]
      "QApplicationWindow" -> "View" [color=red];
      "QApplicationWindow" -> "FileType" [color=red];
      "File" [href="../developers/CodeCoreCL.html#file", target="_top"]
      "QDataSet" -> "File" [color=red];
      "DataTable" [href="../developers/CodeCoreCL.html#datatable", target="_top"]
      "File" -> "DataTable" [color=red];
      "Parameter" [href="../developers/CodeCoreCL.html#parameter", target="_top"]
      "QTheory" -> "Parameter" [color=red];
      "QTool" -> "Parameter" [color=red];
      "QTheory" -> "DataTable" [color=red];
   }

Container Diagrams
==================

The structure RepTate, which can be clearly seen when running a session, is also reflected in the code. Essentially:

   - A RepTate session may contain one or more open applications of the same or different type (*i.e.* LVE, NLVE, LAOS, etc).

   - Each application can have one or more open datasets (*i.e.* Set1, Set2, etc). Datasets are intended to group experimental data that are related in some way. For example:
   
      - SAOS measurements of samples of the same material, measured at same temperature, but having different molecular weight.

      - Start-up of shear flow measurements of samples of the same material and same molecular weight, measured at the same temperature, but with different shear rates. 

   - Each Dataset may contain one or several Data files, which are typically loaded from disk.

   - Inside each dataset, there may be one or more open theories of the same or different kind (*i.e.* Maxwell, Rouse, etc). Each theory is **only applied to the files in the same Dataset that contains the theory**.

   - Finally, each Application may have open tools of the same or different type (*i.e.* Find Peaks, Materials Database, etc). The tools are applied to **all the files in all the Datasets** contained in the same Application as the Tool. 

The following diagram shows a typical example of use of RepTate, representing the above structure in a schematic way. In the diagram:

   - The green box represents a RepTate session. 
   - In the session, there are three open applications (TTS1, LVE2 and NLVE3), represented by red rounded boxes.
   - Each application contains one or more datasets, represented by yellow folders. Some applications also have a tool, represented by a cyan arrow. 
   - Each dataset contains data files, represented in grey. In addition, some datasets have opened one or more theories, which are shown as purple boxes.

.. graphviz::

   digraph foo {
	  rankdir=LR
	  "RepTate" [shape="box",style="filled",fillcolor=mediumseagreen]
	  "TTS1" [shape="box",style="rounded,filled",fillcolor=indianred1]
	  "LVE2" [shape="box",style="rounded,filled",fillcolor=indianred1]
	  "NLVE3" [shape="box",style="rounded,filled",fillcolor=indianred1]
	  "Set1" [shape="folder",style="filled",fillcolor=khaki]
	  "Set2" [shape="folder",style="filled",fillcolor=khaki]
	  "Set3" [shape="folder",style="filled",fillcolor=khaki]
	  "Set4" [shape="folder",style="filled",fillcolor=khaki]
	  "WLF Shift" [shape="signature",style="filled",fillcolor=magenta1]
	  "Maxwell Modes" [shape="signature",style="filled",fillcolor=magenta1]
	  "Likhtman-McLeish" [shape="signature",style="filled",fillcolor=magenta1]
	  "PI88K 25C.osc" [shape="note",style="filled"]
	  "PI88K 10C.osc" [shape="note",style="filled"]
	  "PI94_T25.tts" [shape="note",style="filled"]
	  "PI225_T25.tts" [shape="note",style="filled"]
	  "dow150.shear" [shape="note",style="filled"]
	  "dow170.shear" [shape="note",style="filled"]
	  "hdpe320.shear" [shape="note",style="filled"]
	  "hdpe270.shear" [shape="note",style="filled"]
	  "Materials Database" [shape="cds",style="filled", fillcolor=cyan]
	  "Find Peaks" [shape="cds",style="filled", fillcolor=cyan]
      "RepTate" -> "TTS1";
      "RepTate" -> "LVE2";
      "RepTate" -> "NLVE3";
      "TTS1" -> "Set1";
      "Set1" -> "PI88K 25C.osc";
      "Set1" -> "PI88K 10C.osc";
      "Set1" -> "WLF Shift";
      "LVE2" -> "Set2";
      "Set2" -> "PI94_T25.tts";
      "Set2" -> "PI225_T25.tts";
      "Set2" -> "Maxwell Modes";
      "Set2" -> "Likhtman-McLeish";
      "LVE2" -> "Materials Database";
      "NLVE3" -> "Set3";
      "Set3" -> "dow150.shear";
      "Set3" -> "dow170.shear";
      "NLVE3" -> "Set4";
      "Set4" -> "hdpe320.shear";
      "Set4" -> "hdpe270.shear";
      "NLVE3" -> "Find Peaks"
   }

