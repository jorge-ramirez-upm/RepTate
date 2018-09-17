========================
Diene CSTR
========================

.. contents:: Contents
  :local:


Reaction theory
---------------

The diene CSTR reaction theory uses an algorithm based on the reaction described in
the paper by Das et al. :cite:`CSTR-Das2014` for batch reactions. 
The algorithm is based upon a set of processes occuring in the
reactor during free-radical polymerisation. 
These processes are: 

*   initiation; 
*   polymerisation (rate :math:`k_\text{p}`); 
*   free-diene incorporation (rate :math:`k_\text{pD}`); 
*   once-reacted diene incorporation leading to long-chain-branching (rate :math:`k_\text{DLCB}`); 
*   termination (rate :math:`k_\text{t}`); 
*   catalyst deactivation (rate :math:`k_\text{d}`);

The rates of each of these processes can be related, 
via standard reaction kinetics theory, to the reaction rate constants and 
the concentrations of various species in the reactor. 
In a CSTR, the rates of each of these processes are fixed. 
We make the further assumption that the timescale over which a single (linear)
chain strand is formed within a molecule is much shorter than the reactor
timescale. 

There are eight parameters which control the results of the reaction:
    
- ``tau``: the reactor time
- ``kpM``: the polimarisation rate times the monomer concentration
- ``kpD``: the free-diene incorporation rate
- ``kDLCB``: the once-reacted diene incorporation rate (leading to long-chain-branching)
- ``kd``: the catalyst deactivation rate
- ``kt``: the catalyst termination rate
- ``D0``: the concentation of diene in the reactor feed
- ``C0``: the concentation of catalyst in the reactor feed

Simulation parameters
---------------------

In addition to these parameters, there are four more which control the
generation of molecules, the way that the data are displayed, and the output
to a BoB polymer configuration file. There are:

.. include:: simulation_parameters.rst

.. include:: gfactor_BoB_polymer_storage_and_memory.rst


.. rubric:: References

.. bibliography:: ../bibliography.bib
    :style: unsrt
    :keyprefix: CSTR-
