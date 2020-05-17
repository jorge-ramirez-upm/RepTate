Code Class Diagrams
===================

Basic Classes
-------------

The most important basic classes in RepTate are children of the CmdBase class. 

.. graphviz::

   digraph foo {
      "CmdBase" [href="../developers/CodeCoreCL.html#cmdbase", target="_top"]
      "Application" [href="../developers/CodeCoreCL.html#application", target="_top"]
      "ApplicationManager" [href="../developers/CodeCoreCL.html#applicationmanager", target="_top"]
      "DataSet" [href="../developers/CodeCoreCL.html#dataset", target="_top"]
      "Theory" [href="../developers/CodeCoreCL.html#theory", target="_top"]
      "Tool" [href="../developers/CodeCoreCL.html#tool", target="_top"]
      "CmdBase" -> "Application";
      "CmdBase" -> "ApplicationManager";
      "CmdBase" -> "DataSet";
      "CmdBase" -> "Theory";
      "CmdBase" -> "Tool";
      "QApplicationWindow" [href="../developers/CodeCoreGUI.html#qapplicationwindow", target="_top"]
      "QTheory" [href="../developers/CodeCoreGUI.html#qtheory", target="_top"]
      "QTool" [href="../developers/CodeCoreGUI.html#qtool", target="_top"]
      "Application" -> "QApplicationWindow";
      "ApplicationManager" -> "QApplicationManager";
      "DataSet" -> "QDataSet";
      "Theory" -> "QTheory";
      "Tool" -> "QTool";
      "QWidget" [shape=box,color=red,href="https://doc.qt.io/qt-5/qwidget.html", target="_top"]
      "QMainWindow" [shape=box,color=red,href="https://doc.qt.io/qt-5/qmainwindow.html", target="_top"]
      "QWidget" -> "QApplicationWindow" [color=red];
      "QWidget" -> "QDataSet" [color=red];
      "QWidget" -> "QTheory" [color=red];
      "QWidget" -> "QTool" [color=red];
      "QMainWindow" -> "QApplicationManager" [color=red];
   }

``CmdBase`` provides the basic functionality to operate on the command line (CL). RepTate was built first as a CL application and this hierarchical class structure is a reminder of that. The Graphic User Interface (GUI) version of the classes are children of the corresponding CL versions and QWidget class from PyQt (except the QApplicationManager, which is derived from QMainWindow).

Applications
------------

Example diagram of the class inheritance of one of the Theories (LVE):

.. graphviz::

   digraph foo {
      "CmdBase" [href="../developers/CodeCoreCL.html#cmdbase", target="_top"]
      "Application" [href="../developers/CodeCoreCL.html#application", target="_top"]
      "QApplicationWindow" [href="../developers/CodeCoreGUI.html#qapplicationwindow", target="_top"]
      "ApplicationLVE" [href="../developers/CodeApplications.html#RepTate.applications.ApplicationLVE.ApplicationLVE", target="_top", shape=box,color=red]
	  "BaseApplicationLVE" [href="../developers/CodeApplications.html#RepTate.applications.ApplicationLVE.BaseApplicationLVE", target="_top"]
	  "CLApplicationLVE" [href="../developers/CodeApplications.html#RepTate.applications.ApplicationLVE.CLApplicationLVE", target="_top"]
	  "GUIApplicationLVE" [href="../developers/CodeApplications.html#RepTate.applications.ApplicationLVE.GUIApplicationLVE", target="_top"]
      "CmdBase" -> "Application";
      "Application" -> "QApplicationWindow";
      "QApplicationWindow" -> "GUIApplicationLVE";
      "Application" -> "CLApplicationLVE";
      "BaseApplicationLVE" -> "GUIApplicationLVE";
      "BaseApplicationLVE" -> "CLApplicationLVE";
      "CmdBase" -> "ApplicationLVE"
      "ApplicationLVE" -> "CLApplicationLVE" [style=dotted, label="CL", color=red];
      "ApplicationLVE" -> "GUIApplicationLVE" [style=dotted, label="GUI", color=red];
   }

I don't feel very comfortable with this hieararchy for the following reasons:

   - ApplicationLVE is a child of CmdBase but uses none of its functionality. Application LVE is just a metaclass that decides which is the right instance to create, depending on the case (CL or GUI).
   - BaseApplicationLVE uses functionality of Application but it is not a children of it. In fact, VSCode and other editors complain that some of the members of BaseApplicationLVE do not exist. 
   
I never understood well how this structure could work, but the fact is that it does and it was a brilliant solution at the time. In fact, I consider this to be one of the biggest pillars upon which we built RepTate. It was fully your solution, so I want to discuss it with you before applying any changes to this.

Following the considerations above, I suggest the following new inheritance relation:

.. graphviz::

   digraph foo {
      "CmdBase" [href="../developers/CodeCoreCL.html#cmdbase", target="_top"]
      "Application" [href="../developers/CodeCoreCL.html#application", target="_top"]
      "QApplicationWindow" [href="../developers/CodeCoreGUI.html#qapplicationwindow", target="_top"]
      "ApplicationLVE" [href="../developers/CodeApplications.html#RepTate.applications.ApplicationLVE.ApplicationLVE", target="_top", shape=box,color=red]
	  "BaseApplicationLVE" [href="../developers/CodeApplications.html#RepTate.applications.ApplicationLVE.BaseApplicationLVE", target="_top"]
	  "CLApplicationLVE" [href="../developers/CodeApplications.html#RepTate.applications.ApplicationLVE.CLApplicationLVE", target="_top"]
	  "GUIApplicationLVE" [href="../developers/CodeApplications.html#RepTate.applications.ApplicationLVE.GUIApplicationLVE", target="_top"]
      "CmdBase" -> "Application";
      "Application" -> "QApplicationWindow";
      "QApplicationWindow" -> "GUIApplicationLVE";
      "Application" -> "BaseApplicationLVE";
      "BaseApplicationLVE" -> "CLApplicationLVE";
      "BaseApplicationLVE" -> "GUIApplicationLVE";
      "ApplicationLVE" -> "CLApplicationLVE" [style=dotted, label="CL", color=red];
      "ApplicationLVE" -> "GUIApplicationLVE" [style=dotted, label="GUI", color=red];
   }


Now, the dependencies are clear, and all classes that need to use functionality from another are children of it. ApplicationLVE does not need to be the child of any class because it simply does not use any functionality. It is just a Metaclass. I've tried this implementation for one of the Applications and it seems to work. However, before applying this structure to the overall code, I'd like to know what you think about it. In any case, if I ever try to implement this, I'll do it in a separate branch that we will test thoroughly before merging it to the main.


Theories
--------

Example diagram of the class inheritance of one of the Theories

.. graphviz::

   digraph foo {
      "CmdBase" [href="../developers/CodeCoreCL.html#cmdbase", target="_top"]
      "Theory" [href="../developers/CodeCoreCL.html#theory", target="_top"]
      "QTheory" [href="../developers/CodeCoreGUI.html#qtheory", target="_top"]
      "TheoryPolynomial" [href="../developers/CodeTheories.html#theorybasic", target="_top", shape=box,color=red]
	  "BaseTheoryPolynomial" [href="../developers/CodeTheories.html#theorybasic", target="_top"]
	  "CLTheoryPolynomial" [href="../developers/CodeTheories.html#theorybasic", target="_top"]
	  "GUITheoryPolynomial" [href="../developers/CodeTheories.html#theorybasic"", target="_top"]
      "CmdBase" -> "Theory";
      "Theory" -> "QTheory";
      "QTheory" -> "GUITheoryPolynomial";
      "Theory" -> "CLTheoryPolynomial";
      "BaseTheoryPolynomial" -> "GUITheoryPolynomial";
      "BaseTheoryPolynomial" -> "CLTheoryPolynomial";
      "CmdBase" -> "TheoryPolynomial"
      "TheoryPolynomial" -> "CLTheoryPolynomial" [style=dotted, label="CL", color=red];
      "TheoryPolynomial" -> "GUITheoryPolynomial" [style=dotted, label="GUI", color=red];
   }

Using a similar reasoning as with Applications, I suggest the following new structure:

.. graphviz::

   digraph foo {
      "CmdBase" [href="../developers/CodeCoreCL.html#cmdbase", target="_top"]
      "Theory" [href="../developers/CodeCoreCL.html#theory", target="_top"]
      "QTheory" [href="../developers/CodeCoreGUI.html#qtheory", target="_top"]
      "TheoryPolynomial" [href="../developers/CodeTheories.html#theorybasic", target="_top", shape=box,color=red]
	  "BaseTheoryPolynomial" [href="../developers/CodeTheories.html#theorybasic", target="_top"]
	  "CLTheoryPolynomial" [href="../developers/CodeTheories.html#theorybasic", target="_top"]
	  "GUITheoryPolynomial" [href="../developers/CodeTheories.html#theorybasic"", target="_top"]
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

Using a similar reasoning as with Applications, I suggest the following new structure:

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

