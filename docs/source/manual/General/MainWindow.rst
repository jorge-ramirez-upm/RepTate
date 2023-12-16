-----------------------
Main RepTate Window 
-----------------------

.. |inspection| image:: /gui_icons/icons8-microscope.png
    :width: 15pt
    :height: 15pt
    :align: bottom

.. |openmain| image:: /gui_icons/icons8-open-view-in-new-tab.png
    :width: 15pt
    :height: 15pt
    :align: bottom


The main RepTate window is called the *Application Manager* and is a multiple document interface (MDI) (see :numref:`figmainwindow`). All the applications can be opened from the Application Manager and will reside inside it. At the top of the Application Manager there is a toolbar that allows to open different applications (label **1** in :numref:`figmainwindow`), load and save RepTate projects, read the help and exit RepTate. Currently open applications can are shown as tabs below the toolbar (label **2** in :numref:`figmainwindow`). By default, tabs are named after the application name and a number. The name can be changed by double-clicking on the tab.

.. _figmainwindow:
.. figure:: images/RepTate_Window.png
    :width: 75%
    :align: center
    	
    Main RepTate window showing the most important elements in the user interface.

Applications have three main separate areas:

- The plot, in the center, is where the experimental data files and theoretical fits are shown (label **4** in :numref:`figmainwindow`). 
- A vertical region at the right of the window, that allows to:
    
  - Select the current *View* (way of representing the data, label **3** in :numref:`figmainwindow`)
  - Open data *Files* and arrange them into different *Datasets* (label **5** in :numref:`figmainwindow`). Different *Datasets* are shown as tabs, named by default as "Set" + number. The name of a *Dataset* can be changed by double-clicking on the tab.
  - Create a *Theory* associated to a given Dataset and fit it (minimize the error with respect to the Files within that Dataset, label **7** in :numref:`figmainwindow`). Currently open theories are named after the theory name + a number. The name can be changed by double-clicking on the tab.
  
Files in the current *DataSet* are shown in a table, along with the main parameters that describe each file (label **6** in :numref:`figmainwindow`). Files can be added to a *Dataset* with the "Open Data File" button |openmain| (Ctrl+O) or by dragging them from the file explorer and dropping them on the RepTate window. In the *Theory* area, the parameters of the current theory are shown in a table, with their current value and error. A blue box below the table shows information during the calculation and fitting procedure (label **8** in :numref:`figmainwindow`)

By clicling on the "Data Inspection" button |inspection| (label **1** in :numref:`figextendedwindow`), a new region on the left of the plot area is shown where the user can inspect the contents of a file, shift data and use the Tools. Two separate areas are shown:

.. _figextendedwindow:
.. figure:: images/RepTate_Extended_Window.png
    :width: 75%
    :align: center
    	
    Extended RepTate window showing file data and Tools.

- A region (label **3** in :numref:`figextendedwindow`) where the file contents are shown in a table. Above the table (label **2** in :numref:`figextendedwindow`) there is a toolbar that allows the user to do some operations on the data (copy, paste, shift, etc). 
- A region (label **4** in :numref:`figextendedwindow`) that lets the user apply different Tools to the current Dataset.

The data inspection and Tools region is hidden by default.
