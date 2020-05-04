Tutorial command line (CL) files can be found in the `tests/` folder. They can be run in batch mode or in interactive mode. 

- To run them in *interactive* mode, introduce the lines in the file (except the comments, which start with ``#`` and the line ``console batch``) one by one and wait for the results.

- To run them in *batch* mode, you can execute the tutorial of your choice, e.g.::

	RepTateCL.py -b < tutorial/TEST_WLFShift.txt # Linux or Mac

  or::

  	RepTateCL.py -b < tutorial\TEST_WLFShift.txt # Windows

(the difference is the use of backslash ``\`` instead of slash ``/``) and the output will be shown in the command line. In batch mode, no graphs or plots are shown.
