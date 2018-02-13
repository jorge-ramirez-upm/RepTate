========================
Metallocene CSTR
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


The multiple metallocene CSTR reaction theory uses an algorithm based on the
reaction scheme given by Read and Soares (`Macromolecules 36,
10037-10051 (2003) <https://doi.org/10.1021/ma030354l>`_). 
That paper presented some analytical and semi-analytical
derivations of molecular weight distributions for the case of two metallocene
catalysts. The present algorithm is a Monte Carlo algorithm for simulating the
case multiple catalysts. Note that some catalysts behave non-ideally,
giving broad molecular weight distributions. These will need to be modelled as
a combination of several catalysts with different rate parameters.

On opening the theory, one is presented with (apparently) only four
parameters, which are:

.. include:: simulation_parameters.rst

The remaining parameters are shown when you press the |calculate| button, which
opens a form looking like:

    .. image:: images/metalloceneCSTR_form.png
        :width: 400pt
        :align: center
        :alt: metalloceneCSTR_form

Here, one can set the total number of catalyst sites to be used in the
calculation, the reactor time constant (the mean residence time in the CSTR),
and the reactor monomer concentration. Then, for each catalyst site, there are
five parameters to be fixed, as described by `Read and Soares <https://doi.org/10.1021/ma030354l>`_:

*   The active catalyst site concentration (if catalyst deactivation is
    significant, one should account for this by reducing this parameter).
*   The polymerisation rate constant, :math:`K_\text{p}`.
*   The rate constant for chain transfer to macromonomer, :math:`K^=`.
    Some chain transfer reactions result in the creation of a macromonomer, which can
    then subsequently be incorporated into a growing chain, forming a
    long-chain-branch. This chain transfer rate constant describes a reaction of
    form

    .. math::
        P\rightarrow D^{=}+C,
    
    where :math:`P` is a macromonomer and :math:`C` is a free
    catalyst site (or short growing chain). 
    Thus, :math:`K^=` is the total rate
    constant for all such processes, and the concentration of any chain transfer
    agents should be included within this rate constant.
*   The rate constant for chain transfer to dead chains, :math:`K^\text{s}`.
    Some chain transfer reactions result in the creation of a dead chain, which plays no
    further part in the reaction. Similar comments apply as for the constant :math:`K^=`
*   The polymerisation rate constant for incorporation of macromonomers to
    form long-chain-branches, :math:`K_\text{p,LCB}`.

.. include:: gfactor_BoB_polymer_storage_and_memory.rst
