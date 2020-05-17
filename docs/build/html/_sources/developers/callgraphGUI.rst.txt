Code Class Diagrams
===================

Basic Classes
-------------

The most important basic classes in RepTate are children of the CmdBase class. 

.. graphviz::

   digraph foo {
      "CmdBase" [href="CodeCoreCL.html#cmdbase"]
      "Application" [href="CodeCoreCL.html#application"]
      "ApplicationManager" [href="CodeCoreCL.html#applicationmanager"]
      "DataSet" [href="CodeCoreCL.html#dataset"]
      "Theory" [href="CodeCoreCL.html#theory"]
      "Tool" [href="CodeCoreCL.html#tool"]
      "CmdBase" -> "Application";
      "CmdBase" -> "ApplicationManager";
      "CmdBase" -> "DataSet";
      "CmdBase" -> "Theory";
      "CmdBase" -> "Tool";
      "QApplicationWindow" [href="CodeCoreGUI.html#qapplicationwindow"]
      "QTheory" [href="CodeCoreGUI.html#qtheory"]
      "QTool" [href="CodeCoreGUI.html#qtool"]
      "Application" -> "QApplicationWindow";
      "ApplicationManager" -> "QApplicationManager";
      "DataSet" -> "QDataSet";
      "Theory" -> "QTheory";
      "Tool" -> "QTool";
      "QWidget" [shape=box,color=red]
      "QMainWindow" [shape=box,color=red]
      "QWidget" -> "QApplicationWindow" [color=red];
      "QWidget" -> "QDataSet" [color=red];
      "QWidget" -> "QTheory" [color=red];
      "QWidget" -> "QTool" [color=red];
      "QMainWindow" -> "QApplicationManager" [color=red];
   }

``CmdBase`` provides the basic functionality to operate on the command line (CL). RepTate was built first as a CL application and this hierarchical class structure is a reminder of that. The Graphic User Interface (GUI) version of the classes are children of the corresponding CL versions and QWidget class from PyQt (except the QApplicationManager, which is derived from QMainWindow).

Applications
------------

Example diagram of the class inheritance of one of the Theories

.. graphviz::

   digraph foo {
      "CmdBase" -> "Application";
      "Application" -> "QApplicationWindow";
      "QApplicationWindow" -> "GUIApplicationLVE";
      "Application" -> "CLApplicationLVE";
      "BaseApplicationLVE" -> "GUIApplicationLVE";
      "BaseApplicationLVE" -> "CLApplicationLVE";
      "ApplicationLVE" [shape=box,color=red];
      "CmdBase" -> "ApplicationLVE"
      "ApplicationLVE" -> "CLApplicationLVE" [style=dotted, label="CL", color=red];
      "ApplicationLVE" -> "GUIApplicationLVE" [style=dotted, label="GUI", color=red];
   }

The new inheritance relation that I suggest:

.. graphviz::

   digraph foo {
      "CmdBase" [href="CodeCoreCL.html#cmdbase"]
      "Application" [href="CodeCoreCL.html#application"]
      "QApplicationWindow" [href="CodeCoreGUI.html#qapplicationwindow"]
      "BaseApplicationLVE" [href="CodeApplications.html#RepTate.applications.ApplicationLVE.BaseApplicationLVE"]
      "ApplicationLVE" [shape=box,color=red,href="CodeApplications.html#RepTate.applications.ApplicationLVE.ApplicationLVE"]
      "CLApplicationLVE" [href="CodeApplications.html#RepTate.applications.ApplicationLVE.CLApplicationLVE"]
      "GUIApplicationLVE" [href="CodeApplications.html#RepTate.applications.ApplicationLVE.GUIApplicationLVE"]
      "CmdBase" -> "Application";
      "Application" -> "QApplicationWindow";
      "QApplicationWindow" -> "GUIApplicationLVE";
      "Application" -> "BaseApplicationLVE";
      "BaseApplicationLVE" -> "CLApplicationLVE";
      "BaseApplicationLVE" -> "GUIApplicationLVE";
      "ApplicationLVE" -> "CLApplicationLVE" [style=dotted, label="CL", color=red];
      "ApplicationLVE" -> "GUIApplicationLVE" [style=dotted, label="GUI", color=red];
   }



Theories
--------

Example diagram of the class inheritance of one of the Theories

.. graphviz::

   digraph foo {
      "CmdBase" -> "Theory";
      "Theory" -> "QTheory";
      "QTheory" -> "GUITheoryPolynomial";
      "Theory" -> "CLTheoryPolynomial";
      "BaseTheoryPolynomial" -> "GUITheoryPolynomial";
      "BaseTheoryPolynomial" -> "CLTheoryPolynomial";
      "TheoryPolynomial" [shape=box,color=red];
      "CmdBase" -> "TheoryPolynomial"
      "TheoryPolynomial" -> "CLTheoryPolynomial" [style=dotted, label="CL", color=red];
      "TheoryPolynomial" -> "GUITheoryPolynomial" [style=dotted, label="GUI", color=red];
   }

The new inheritance relation that I suggest:

.. graphviz::

   digraph foo {
      "CmdBase" [href="CodeCoreCL.html#cmdbase"]
      "Theory" [href="CodeCoreCL.html#theory"]
      "QTheory" [href="CodeCoreGUI.html#qtheory"]
      "BaseTheoryPolynomial" [href="CodeTheories.html#RepTate.theories.TheoryBasic.BaseTheoryPolynomial"]
      "TheoryPolynomial" [shape=box,color=red,href="CodeTheories.html#RepTate.theories.TheoryBasic.TheoryPolynomial"]
      "CLTheoryPolynomial" [href="CodeTheories.html#RepTate.theories.TheoryBasic.CLTheoryPolynomial"]
      "GUITheoryPolynomial" [href="CodeTheories.html#RepTate.theories.TheoryBasic.CLTheoryPolynomial"]
      "CmdBase" -> "Theory";
      "Theory" -> "QTheory";
      "QTheory" -> "GUITheoryPolynomial";
      "Theory" -> "BaseTheoryPolynomial";
      "BaseTheoryPolynomial" -> "CLTheoryPolynomial";
      "BaseTheoryPolynomial" -> "GUITheoryPolynomial";
      "TheoryPolynomial" -> "CLTheoryPolynomial" [style=dotted, label="CL", color=red];
      "TheoryPolynomial" -> "GUITheoryPolynomial" [style=dotted, label="GUI", color=red];
   }



Tools
-----

Example diagram of the class inheritance relation for one of the Tools:

.. graphviz::

   digraph foo {
      "CmdBase" -> "Tool";
      "Tool" -> "QTool";
      "QTool" -> "GUIToolBounds";
      "Tool" -> "CLToolBounds";
      "BaseToolBounds" -> "GUIToolBounds";
      "BaseToolBounds" -> "CLToolBounds";
      "ToolBounds" [shape=box,color=red];
      "CmdBase" -> "ToolBounds"
      "ToolBounds" -> "CLToolBounds" [style=dotted, label="CL", color=red];
      "ToolBounds" -> "GUIToolBounds" [style=dotted, label="GUI", color=red];
   }

The new inheritance relation that I suggest:

.. graphviz::

   digraph foo {
      "CmdBase" [href="CodeCoreCL.html#cmdbase"]
      "Tool" [href="CodeCoreCL.html#tool"]
      "QTool" [href="CodeCoreGUI.html#qtool"]
      "BaseToolBounds" [href="CodeTools.html#RepTate.tools.ToolBounds.BaseToolBounds"]
      "ToolBounds" [shape=box,color=red,href="CodeTools.html#RepTate.tools.ToolBounds.ToolBounds"]
      "CLToolBounds" [href="CodeTools.html#RepTate.tools.ToolBounds.CLToolBounds"]
      "GUIToolBounds" [href="CodeTools.html#RepTate.tools.ToolBounds.GUIToolBounds"]
      "CmdBase" -> "Tool";
      "Tool" -> "QTool";
      "QTool" -> "GUIToolBounds";
      "Tool" -> "BaseToolBounds";
      "BaseToolBounds" -> "CLToolBounds";
      "BaseToolBounds" -> "GUIToolBounds";
      "ToolBounds" -> "CLToolBounds" [style=dotted, label="CL", color=red];
      "ToolBounds" -> "GUIToolBounds" [style=dotted, label="GUI", color=red];
   }

