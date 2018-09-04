==========================
MWD Tutorial: Command Line
==========================

.. hint::
	.. include:: /manual/Applications/All_Tutorials/tutorialCL_instructions.rst

Start RepTate and open a new MWD application::
	
	new MWD

Open a data file containing a GPC data and display the data::

	open data/PS_Linear_Polydisperse/ps1_header.gpc
	plot

Open a new "Discretize MWD" theory::

	theory_new Discretize MWD

Change the number of bins to 15::

	nbin=15
