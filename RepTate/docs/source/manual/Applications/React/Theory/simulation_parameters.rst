``num_to_make``: 
    controls the number of molecules made in the
    simulation - more molecules mean better statistics, but take up more memory
    and take longer to simulate! It is a good idea, when trying to match data, to
    start with just a few molecules - say 1000 to 10000 - and then increase this
    number when you are satisfied the parameters are close to where you want them.
``mon_mass``: 
    this is the mass, in a.m.u., of a monomer (usually set to
    28).
``Me``:
    the entanglement molecular weight - needed for output to a BoB
    polymer configuration file, but has no effect on the display within the React module.
``nbins``:
    this is the number of bins - equally spaced in :math:`\log_{10}\text{MW}`
    - used for analysis of the molecules. More bins means more resolution in the 
    :math:`\log_{10}\text{MW}` axis, but also more noise because there are fewer molecules per
    bin. Thus, the quality of the curves produced is a compromise between these
    two factors. Usually 50 bins is quite adequate for a reasonable number of molecules.
