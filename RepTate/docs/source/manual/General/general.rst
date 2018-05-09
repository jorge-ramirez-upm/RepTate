==============================
General Description of RepTate
==============================

.. toctree::
   :maxdepth: 2
    
RepTate (Rheology of Entangled Polymers: Toolkit for Analysis of Theory & Experiment) is a software package for viewing, exchanging and analysing experimental data. Several of the classical and latest theories of polymer dynamics are included in RepTate, so they can be tested and fitted to the experimental data.

The software is designed in a modular way, so it is easy to extend to analyze new types of data and fit with new theories. 

The main Reptate window is called the *Application Manager* and is a multiple document interface (MDI). All the applications can be opened from the Application Manager and will reside inside it. At the top of the Application Manager there is a toolbar that allows to open different applications, load and save projects, read the help and exit RepTate.

Applications have three separate areas:

- The plot, in the center, is where the experimental data files and theoretical fits are shown. 
- A vertical region at the right of the window, that allows to:
    
  - Select the current *View* (way of representing the data)
  - Open data *Files* and arrange them into different *Datasets*
  - Create a *Theory* associated to a given Dataset and fit it (minimize the error with respect to the Files within that Dataset).

- A vertical region at the left of the window, where the user can inspect the contents of the data of the selected File in the current Dataset. This region is hidden by default.

RepTate makes extensive use of the following packages and libraries:

- Matplotlib: Text :cite:`General-Hunter_2007`.

- Scipy: Text :cite:`General-Jones_2018`.

- Numpy: Text :cite:`General-Oliphant_2006`.

- Qt and Pyqt: Text :cite:`General-Pyqt_2018`, Text :cite:`General-Qt_2018`.

.. rubric:: References

.. bibliography:: bibliography.bib
    :style: unsrt
    :keyprefix: General-
