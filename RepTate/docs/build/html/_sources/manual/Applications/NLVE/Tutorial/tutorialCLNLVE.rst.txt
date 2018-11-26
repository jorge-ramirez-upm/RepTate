===========================
NLVE Tutorial: Command Line
===========================

.. toctree::
   :maxdepth: 2


.. hint::
    .. include:: /manual/Applications/All_Tutorials/tutorialCL_instructions.rst

.. highlight:: none

**Rolie-Poly start-up flow**

    
#. First create LVE application to fit Maxwell Modes::
    
    RepTate> new LVE

#. Open the LVE data and plot::

    RepTate/LVE1/DataSet01> open data/DOW/Linear_Rheology_TTS\DOWLDPEL150R_160C.tts
    RepTate/LVE1/DataSet01> plot

#. Open new Maxwell mode theory, set the number of modes to 8 and minimize the error::

    RepTate/LVE1/DataSet01> theory_new Maxwell Modes
    RepTate/LVE1/DataSet01/Maxwell Modes01> nmodes=8
    RepTate/LVE1/DataSet01/Maxwell Modes01> fit

   The output is::

    Parameter Fitting
    Initial Error      Final Error
    8.72273            0.0103711

    288 function evaluations
    Parameter          Value ± Error
    logG00             2.196 ± 0.03803
    logG01             2.996 ± 0.01574
    logG02             3.547 ± 0.01288
    logG03             3.938 ± 0.0119
    logG04             4.247 ± 0.01391
    logG05             4.508 ± 0.01319
    logG06             4.687 ± 0.02296
    logG07             5.054 ± 0.01338
    logwmax            2.561 ± 0.04225
    logwmin            -2.913 ± 0.02537
    nmodes             8

    File               Error (RSS)        # Pts
    DOWLDPEL150R_160C  4.051e-05          256

    TOTAL ERROR:   4.0512e-05 (256 Pts)
    Bayesian IC:      -2533.7

    ---Fitted in 0.*** seconds---

#. Return to the *Application Manager*::
    
    RepTate/LVE1/DataSet01/Maxwell Modes01> up
    RepTate/LVE1> up
    RepTate/>
    
    
#. Create a new NLVE Application::
    
    RepTate/> new NLVE

    
#. Add files to the dataset (master curve tts files)::

    RepTate/NLVE2/DataSet01> open data/DOW/Non-Linear_Rheology/Start-up_Shear/My_dow150-160-*shear.shear
    
#. Plot the files using the default LVE Application view::

    RepTate/NLVE2/DataSet01> plot
    
#. Create new theory::
    
    RepTate/NLVE2/DataSet01> theory_new Rolie-Poly
    

#. Copy the Maxwell modes previously calculated::

    RepTate/NLVE2/DataSet01/Rolie-Poly01> copy_modes
    Found 1 theories that provide modes
    0: LVE1.DataSet01.Maxwell Modes01
    Select theory (number between 0 and 0> 0
    
#. Calculate the theory with the new modes::

    RepTate/NLVE2/DataSet01/Rolie-Poly01> calculate
    
#. Save theory predictions::

    RepTate/NLVE2/DataSet01/Rolie-Poly01> save
    
#. Exit RepTate (the y answer is needed)::

    RepTate/NLVE2/DataSet01/Rolie-Poly01> quit
