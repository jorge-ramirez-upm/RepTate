========================
Tobita CSTR
========================

.. toctree::
   :maxdepth: 2


The LDPE CSTR reaction theory uses an algorithm based on the one described in
the paper by H. Tobita 
(`J. Pol. Sci. Part B, 39, 391-403 (2001)
<https://doi.org/10.1002/1099-0488(20010115)39:4\<391::AID-POLB1011\>3.0.CO;2-3>`_) 
for batch reactions. 
The algorithm is based upon a set of processes occuring in the
reactor during free-radical polymerisation. 
These processes are: 

*   initiation of free radicals (rate :math:`R_\text{I}` per unit volume); 
*   propagation or polymerisation (rate :math:`R_\text{p}`); 
*   chain transfer to small molecules (rate :math:`R_\text{f}`); 
*   termination by disproportionation (rate :math:`R_\text{td}`); 
*   termination by combination (rate :math:`R_\text{tc}`);
*   chain transfer reactions leading to long-chain branching (rate :math:`R_\text{b}`);
*   chain transfer reactions leading to scission (rate :math:`R_\text{s}`). 

The rates of each of these processes can be related, 
via standard reaction kinetics theory, to the reaction rate constants and 
the concentrations of various species in the reactor. 
In a CSTR, the rates of each of these processes are fixed. 
Tobita makes the further assumption that the timescale over which a single (linear)
chain strand is formed within a molecule is much shorter than the reactor
timescale. 
This is the "stationary state hypothesis", and under these
conditions, we balance the rate of creation of free radicals with the rate at
which they are "terminated" and write

.. math::
    R_{\mathrm{I}}=R_{\mathrm{td}}+R_{\mathrm{tc}}.

Hence, there are four parameters which control the results of the reaction:

.. math::
    \tau &= \dfrac{R_{\mathrm{td}} + R_{\mathrm{f}}}{R_{\mathrm{p}}},\\
    \beta &= \dfrac{R_{\mathrm{tc}}}{R_{\mathrm{p}}},\\
    \lambda &= \dfrac{R_{\mathrm{b}}}{R_{\mathrm{p}}},\\
    \sigma &= \dfrac{R_{\mathrm{s}}}{R_{\mathrm{p}}}.

.. include:: BoB_polymer_storage_and_memory.rst
