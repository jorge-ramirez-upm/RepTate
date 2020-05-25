-------------------
Automatic TTS Shift
-------------------

.. toctree::
   :maxdepth: 2

Summary
-------

.. autoclass:: RepTate.theories.TheoryTTS_Automatic.TheoryTTSShiftAutomatic()
   
Description
-----------
This theory attempts to perform an automatic Time-temperature superposition shift of experimental data without assuming any preconceived behaviour.

When a dataset is loaded, the program creates a database of the datafiles according the molecular weight :math:`M_w` and the volume fraction :math:`\phi` of the samples in the file. Then, it allows the user to select the temperature to which he or she wants to shift the data (from a dropdown box). The list of allowed values of temperature is limited to those values of :math:`T` that are present in all the different samples loaded in the datafile. 

The fitting procedure goes sample by sample, starting from the file that is at the selected reference temperature. Then, it walks over the other files of the same sample, in ascending order of the difference between their temperature and the reference temperature, and finds the right horizontal and vertical shift factors so that the overlap between each file and the previously shifted files is optimal. For each file, the program stores the optimal shift factors.

Once the procedure is over, the theory output window will show a list of the samples and, for each one, will output the temperature of each file and the corresponding optimal shift factors. For the time being, the user will have to copy this data and use it externally in order to extract the temperature dependence of the shift factors (WLF, Arrhenius or any other). In the future, we may implement a new application within RepTate to interpret and fit those data.

.. warning::
    Try to shift simultaneously different samples of the same material.
    
.. warning::
    Load all the *.osc files in the same dataset.
    
.. warning::
    The theory is in **beta** state. It may fail if there is a large number of files to shift. If that happens, inspect the data files and search for files that contain corrupt data or data that is impossible to fit to the data in other files of the same sample. If the error persists, try to fit a reduced number of files. 