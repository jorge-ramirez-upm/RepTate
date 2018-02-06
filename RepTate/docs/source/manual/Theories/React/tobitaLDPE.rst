========================
Tobita LDPE
========================

.. toctree::
   :maxdepth: 2


The LDPE batch reaction theory uses an algorithm described in the paper by H.
Tobita 
(`J. Pol. Sci. Part B, 39, 391-403 (2001)
<https://doi.org/10.1002/1099-0488(20010115)39:4\<391::AID-POLB1011\>3.0.CO;2-3>`_).
It is designed for a batch
reaction - in which the reagents are well mixed at the beginning and monomer
is consumed as the reaction proceeds. It is equivalent to the "plug-flow"
approximation for a tubular reactor. One possibility when modelling a real
tubular reactor is to mix several batch reactions with different conversions.

The algorithm is based upon a set of processes occuring in the reactor during
free-radical polymerisation. These processes are: 

*   initiation of free radicals (rate :math:`R_{\mathrm{I}}` per unit volume);
*   propagation or polymerisation (rate :math:`R_{\mathrm{p}}`);
*   chain transfer to small molecules (rate :math:`R_{\mathrm{f}}`);
*   termination by disproportionation (rate :math:`R_{\mathrm{td}}`);
*   termination by combination (rate :math:`R_{\mathrm{tc}}`);
*   chain transfer reactions leading to long-chain branching (rate :math:`R_{\mathrm{b}}`);
*   chain transfer reactions leading to scission (rate :math:`R_{\mathrm{s}}`).

The rates of each of these processes can be related, via
standard reaction kinetics theory, to the reaction rate constants and the
concentrations of various species in the reactor. In a batch reactor, the
rates of each of these processes vary with reaction time, as monomers are
consumed and polymers are made (this algorithm assumes that the monomer
concentration decreases with reaction - i.e. it is batch rather than semi-batch).

Tobita makes the further assumption that the timescale over which a single
(linear) chain strand is formed within a molecule is much shorter than the
reactor timescale. This is the "stationary state hypothesis", and under
these conditions, we balance the rate of creation of free radicals with the
rate at which they are "terminated" and write

.. math::
    R_{\mathrm{I}}=R_{\mathrm{td}}+R_{\mathrm{tc}}.

Hence, there are five parameters which control the results of the reaction:

.. math::
    \tau &= \dfrac{R_{\mathrm{td}}+R_{\mathrm{f}}}{R_{\mathrm{p}}},\\
    \beta &= \dfrac{R_{\mathrm{tc}}}{R_{\mathrm{p}}},\\
    C_\text{b} &= \dfrac{k_{\mathrm{b}}}{k_{\mathrm{p}}},\\
    C_\text{s} &= \dfrac{k_{\mathrm{s}}}{k_{\mathrm{p}}},

where :math:`C_\text{b}` is the ratio of the
branching and polymerisation rate constants and 
:math:`C_\text{s}` the ratio of the
scission and polymerisation rate constants.
The fifth parameter is the monomer conversion at the end of the reaction.

.. include:: BoB_polymer_storage_and_memory.rst