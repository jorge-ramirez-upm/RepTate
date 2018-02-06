========================
React mixture
========================

.. toctree::
   :maxdepth: 2

.. |piggy| image:: images/icons8-money-box.png
    :width: 20pt
    :height: 20pt
    :align: bottom

.. |calculate| image:: images/icons8-abacus.png
    :width: 20pt
    :height: 20pt
    :align: bottom

The "mixture" theory allows you to combine the molecules and molecular
weight distributions from other active React theories, and to output the
combined mixture into a BoB polymer configuration file. It does not perform
new Monte Carlo simulations but uses those already made.

On opening the theory, one is presented with (apparently) just one parameter,
which is

`nbin`:
    this is the number of bins - equally spaced in :math:`\log_{10}\text{MW}`
    - used for analysis of the molecules. More bins means more resolution in the
    :math:`\log_{10}\text{MW}` axis, but also more noise because there are fewer molecules per
    bin. Thus, the quality of the curves produced is a compromise between these
    two factors. Usually 50 bins is quite adequate for a reasonable number of molecules.

The remaining parameters are shown when you press the |calculate| button, which
opens a form looking like:

    .. image:: images/mixform.png
        :width: 400pt
        :align: center
        :alt: mixform

Whenever React creates a new Monte Carlo simulation, using one of the other
theories, it stores the information for that simulation in one of 10 initially available
memory locations. These memory locations are listed on the far left of this
form - it might be that not all of them are currently active. Also, when React
creates a new theory, it gives that theory a unique name (e.g. "LDPE batch
1") which is shown on the control panel for that theory. This corresponds to
the name listed on the second column of the above mixture form. This should be
sufficient information for the user to identify which row of the form
corresponds to which theory. The form also gives additional information about
how many polymers were generated within that theory, and how many polymers are
"saved" for output into a BoB polymer configuration file (a saved molecule
stores a complete record of the molecule, including the connectivity of all
the arms, an unsaved molecule still retains a record of the total molecular
weight, number of branches and `g`-factor).

In order to create a mixture, the user needs to decide which theories to
"include" in the mixture (by clicking on the relevant check-boxes). Then the
user needs to decide with what weight ratio to combine these theories. 

.. note:: 
    The values in the ratio boxes need not add up to one - the form calculates the
    effective weight fractions from the ratios (clicking the "Update weights"
    button shows the result of this - although it is not necessary to do this).

.. warning:: 
    Inputting negative numbers in the ratio boxes, or inputting all zeros, will
    result in an error message. It isn't advisable to enter non-numeric values!

Clicking "OK" results in calculation of the MWDs.


**Saving to BoB**

To save a BoB polymer configuration file corresponding to the mixture, click
the |piggy| button.
The mixture theory first checks to see whether any of the other
theories have been modified since the mixture MWD was last calculated - if so,
you are prompted to recalculate the mixture MWD (this ensures you don't save a
polymer configuration file which doesn't correspond to the displayed MWD).
Then, a form is displayed which asks you to check that the monomer mass and
entanglement molecular weights from the different theories in the mixture are
consistent. 

.. warning:: 
    Currently, BoB is not designed to cope with mixtures of molecules
    having different entanglement molecular weights - performing calculations on
    such mixtures is at your own risk! 

On clicking "OK", a save dialogue box is
openned, which allows you to save the polymer configuration file. All
"saved" polymers, in all theories included in the mixture, are saved into
the file, with weight fractions adjusted to reflect the weight fractions in
the mixture.
