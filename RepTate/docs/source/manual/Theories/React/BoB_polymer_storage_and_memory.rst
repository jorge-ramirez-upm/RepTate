**Simulation parameters**

In addition to these parameters, there are four more which control the
generation of molecules, the way that the data are displayed, and the output
to a BoB polymer configuration file. There are:

`num_to_make`: 
    controls the number of molecules made in the
    simulation - more molecules mean better statistics, but take up more memory
    and take longer to simulate! It is a good idea, when trying to match data, to
    start with just a few molecules - say 1000 to 10000 - and then increase this
    number when you are satisfied the parameters are close to where you want them.
`mon_mass`: 
    this is the mass, in a.m.u., of a monomer (usually set to
    28 for LDPE).
`Me`:
    the entanglement molecular weight - needed for output to a BoB
    polymer configuration file, but has no effect on the display within the React module.
`nbins`:
    this is the number of bins - equally spaced in :math:`\log_{10}\text{MW}`
    - used for analysis of the molecules. More bins means more resolution in the 
    :math:`\log_{10}\text{MW}` axis, but also more noise because there are fewer molecules per
    bin. Thus, the quality of the curves produced is a compromise between these
    two factors. Usually 50 bins is quite adequate for a reasonable number of molecules.


When a molecule is generated, it is straightforward to assess its molecular
weight and number of branches. The `g`-factor is calculated based on the
assumption of ideal random walk statistics (as opposed to self-avoiding walk
statistics). Ideal chain radius of gyration is fast to calculate:
self-avoiding walk radius is not. It is often found that the `g`-factor
calculated in these two ways is (somewhat surprisingly) similar, but it is
still a possible source of error!


**Polymer storage and saving to BoB**

When a molecule is generated using the algorithm, the theory makes a decision
as to whether to "save" the molecule (that is, to store a complete record of
the molecule, including the connectivity of all the arms) or not (for an
unsaved molecule, the theory still retains a record of the total molecular
weight, number of branches and `g`-factor).

"Saved" molecules are retained for
possible output into a BoB polymer configuration file. The decision as to
whether to save a molecule, or not, is based upon whether there have been a
given number of molecules of similar molecular weight already generated. 
The :math:`\log_{10}\text{MW}` axis is split into a set of evenly-spaced bins, 
and each bin keeps track of how many polymers have been made with molecular
weight in the range of that bin.
Once the number made exceeds a given maximum, polymers of
that molecular weight are no longer saved. 
However, the algorithm still keeps
track of the number of polymers made in a given bin - when saving a polymer
configuration file for BoB, the weights of the saved molecules are adjusted
accordingly, to account for the unsaved molecules.

You can modify the parameters used for saving molecules by clicking on the
|bob-hat|
button. This opens a form with four parameters:

*   the maximum molecular weight of the bins,
*   the minimum molecular weight of the bins (it is wise to make sure
    these span the MW range of the polymers you are making),
*   the number of bins,
*   the maximum number of polymers stored per bin.

In particular, increasing either of the last two parameters 
increases the number of polymers saved.

Clicking the |piggy|
button opens a save dialogue box which allows you to save a polymer
configuration file containing the connectivity for the saved polymer. The
format of this file, and the use of it within a BoB calculation, is given in
the BoB documentation.


**Memory issues**

React stores polymer information (total molecular weight, number of branches
and `g`-factor) in a polymer record, and connectivity information in arm
records. There is a fixed amount of computer memory allocated for this. React is designed to
cope smoothly with running out of memory - it should kindly ask you to allocate more memory!
The dialog will propose you to increase the amount of computer memory allocated to React
and give you an estimate the extra amount or RAM needed.

There are some things that contribute to using a lot of memory:

*   Some choices of reaction parameters lead to extremely large molecules,
    with lots of arms being generated on each molecule. For non-zero values of the
    parameter :math:`\beta`, gelation (i.e. infinite molecules) is possible. If a
    molecule looks like being particularly large, you will get a warning message!
*   If you make too many molecules, you will run out of memory.
*   If you save too many molecules, you will run out of arm records (adjust
    the parameters by clicking on the |bob-hat| button.
*   If you have other theories open which are already using a lot of
    storage, there might not be enough memory left for your current calculation
    (close un-needed theories, or adjust their parameters so they don't use as
    much storage). 

You will get brief hints along these lines in the theory log if you run out of parameters.
