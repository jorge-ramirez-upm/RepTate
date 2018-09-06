===========================
TTS Tutorial: Command Line
===========================

.. toctree::
   :maxdepth: 2

.. hint::
	.. include:: /manual/Applications/All_Tutorials/tutorialCL_instructions.rst

.. highlight:: none

**Time-Temperature shift**
    
#. Start RepTate and create LVE Application::

    RepTate Version 0.9.3 - 20180719 command processor
    help [command] for instructions
    TAB for completions
    RepTate> new TTS
    RepTate/TTS1/DataSet01>

A new plot window for the new application is opened.

#. Add files to the dataset (small amplitude oscillatory shear files ``.osc``, see :ref:`TTS_Data_Description`)
   and display the data::

    RepTate/TTS1/DataSet01> open data/PI_LINEAR/osc/PI*osc
    RepTate/TTS1/DataSet01> plot

   .. image:: images/plotOSCfiles.png
        :width: 70%
        :align: center
        :alt: osc files

#. Create new WLF theory (the shift is calculated with the default values of the parameters)::

    RepTate/TTS1/DataSet01> theory_new WLF Shift

   The output is::
    
    Mw           Mw2          phi          phi2         Error        # Pts.
    2.4          0            0            0            0.293        192
    5.1          0            0            0            0.0881       82
    13.5         0            0            0            0.0926       168
    23.4         0            0            0            0.038        260
    33.6         0            0            0            0.0225       274
    94.9         0            0            0            0.00315      536
    225.9        0            0            0            0.00311      1070
    483.1        0            0            0            0.00116      436
    634.5        0            0            0            0.00589      324
    1131         0            0            0            0.000427     550

    TOTAL ERROR:      0.02638 (  3892)

    ---Calculated in 0.*** seconds---

   .. image:: images/WLFdefault.png
        :width: 70%
        :align: center
        :alt: WLF shift with default parameters

#. Change the value of a theory parameter, e.g. the reference temperature::

    RepTate/TTS1/DataSet01/WLF Shift01> T0=-35
    
#. Fit the theory to the data files (in this case, shift according to WLF). 
   After the fit is finished, the optimal values of the theory parameters are shown. 
   Only those parameters marked with a ``*`` have been optimized. Also, the error per Mw is 
   shown in a table, along with the number of points that were used for the fit, and the 
   total error of the fit (the objective of the optimization)::

    RepTate/TTS1/DataSet01/WLF Shift01> fit
    
   The output is::

    Parameter Fitting
    131 function evaluations
    Parameter          Value
    C1                 8.716
    C2                 114.3

    Mw           Mw2          phi          phi2         Error        # Pts.
    2.4          0            0            0            0.00304      152
    5.1          0            0            0            0.00164      78
    13.5         0            0            0            0.00171      146
    23.4         0            0            0            0.000648     244
    33.6         0            0            0            0.00025      254
    94.9         0            0            0            7.72e-05     498
    225.9        0            0            0            0.000181     1052
    483.1        0            0            0            5.58e-05     430
    634.5        0            0            0            0.000373     322
    1131         0            0            0            1.82e-05     548

    TOTAL ERROR:   0.00038775 (  3724)

    ---Fitted in *.** seconds---

   .. image:: images/WLFfit.png
      :width: 70%
      :align: center
      :alt: WLF shift with fitted parameters
    
#. Save theory predictions (by default, tts theory files are saved to the same folder 
   as the osc files)::
    
    RepTate/TTS1/DataSet01/WLF Shift01> save
    
   The output is::

    Saving prediction of WLF Shift theory
    File: ***/data/PI_LINEAR/osc/PI_Mw2.4k_Mw20_phi0_phiB0-35.0.tts
    File: ***/data/PI_LINEAR/osc/PI_Mw5.1k_Mw20_phi0_phiB0-35.0.tts
    File: ***/data/PI_LINEAR/osc/PI_Mw13.5k_Mw20_phi0_phiB0-35.0.tts
    File: ***/data/PI_LINEAR/osc/PI_Mw23.4k_Mw20_phi0_phiB0-35.0.tts
    File: ***/data/PI_LINEAR/osc/PI_Mw33.6k_Mw20_phi0_phiB0-35.0.tts
    File: ***/data/PI_LINEAR/osc/PI_Mw94.9k_Mw20_phi0_phiB0-35.0.tts
    File: ***/data/PI_LINEAR/osc/PI_Mw225.9k_Mw20_phi0_phiB0-35.0.tts
    File: ***/data/PI_LINEAR/osc/PI_Mw483.1k_Mw20_phi0_phiB0-35.0.tts
    File: ***/data/PI_LINEAR/osc/PI_Mw634.5k_Mw20_phi0_phiB0-35.0.tts
    File: ***/data/PI_LINEAR/osc/PI_Mw1131.0k_Mw20_phi0_phiB0-35.0.tts
    
#. Exit RepTate (the y answer is needed)::

    RepTate/TTS1/DataSet01/WLF Shift01> quit
