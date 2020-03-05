----------------
Sticky Reptation
----------------

.. toctree::
   :maxdepth: 2

Summary
-------

.. autoclass:: StickyReptation.TheoryStickyReptation()
   

Sticky Reptation model for the linear rheology of linear entangled polymers with a number of stickers that can form reversible intramolecular crosslinks. The key ingredients to this model are sticky Rouse :cite:`SRlve-Leibler1991` and double reptation :cite:`SRlve-desCloizeaux1990` (see Description for more detail). The parameters are

    *   :math:`G_\mathrm{e}`: elastic plateau modulus
    *   :math:`Z_\mathrm{e}`: number of entanglements per chain
    *   :math:`Z_\mathrm{s}`: number of stickers per chain
    *   :math:`\tau_\mathrm{s}`: sticker dissociation time
    *   :math:`\alpha`: dimensionless constant that is in principle universal, but in practice varies between different polymers (see e.g. Ref. :cite:`SRlve-Ruymbeke2002`). Note that :math:`Z_\mathrm{e}/\alpha` is equivalent to the parameter :math:`H` in Ref. :cite:`SRlve-desCloizeaux1990`.

.. warning::
    The high-frequency Rouse modes with time scales shorter than the sticker dissociation time are not included.  This is only valid if the sticker dissociation time is much larger than the Rouse time of those substrands.


Description
-----------

Theory for the linear rheology of linear entangled polymers with a number of stickers that can form reversible intramolecular crosslinks.
The relaxation modulus, :math:`G(t)`, is modeled as the sum of a Sticky-Rouse, :math:`G_\mathrm{SR}(t)` :cite:`SRlve-Leibler1991` and a Double-Reptation, :math:`G_\mathrm{rep}(t)` :cite:`SRlve-desCloizeaux1990` contribution,

.. math::
    G(t) = G_\mathrm{SR}(t) + G_\mathrm{rep}(t)

with 

.. math::
    G_\mathrm{SR}(t) = \dfrac{G_\mathrm{e}}{Z_\mathrm{e}} \sum_{q=1}^{Z_\mathrm{s}} \kappa \exp\left(\dfrac{q^2 t}{\tau_\mathrm{s} (Z_\mathrm{s})^2}\right).

This equation assumes that most stickers are bound, and after sticker dissociation a strand of length :math:`N/Z_\mathrm{s}` can relax, with :math:`N` the number of monomers per chain and :math:`Z_\mathrm{s}` the number of stickers per chain. :math:`\tau_\mathrm{s}` is the dissociation time of a sticker.
(Note that this is approximate: after sticker dissociation a chain with a length twice :math:`N/Z_\mathrm{s}` or more relaxes,  see :cite:`SRlve-Leibler1991` and :cite:`SRlve-Rubinstein2001` )
The truncation of the sum at :math:`Z_\mathrm{s}` implies that we ignore high-frequency (non-sticky) Rouse relaxation of the subchains between stickers.
This is only valid if the sticker dissociation time is much larger than the Rouse time of those substrands.
Finally, the factor  :math:`\kappa` is 0.2 for long wavelengths (i.e., for :math:`q < Z_\mathrm{e}`  and unity for short wavelengths (i.e., for :math:`q \geq Z_\mathrm{e}`) (see Likhtman-McLeish, 2002). 
The factor :math:`Z_\mathrm{e}` is the number of entanglements per chain.
    
The other contribution to the relaxation modulus is the double-reptation model,

.. math::
    G_\mathrm{rep}(t) = G_\mathrm{e} \left( \frac{8}{\pi^2}\sum_{\mathrm{odd}\, q} \frac{1}{q^2}\exp\left(-q^2 U(t)\right) \right)^2,

with

.. math::
    U(t) = \frac{t}{\tau_\mathrm{rep}} + \frac{\alpha}{Z_\mathrm{e}}g\left(\frac{Z_\mathrm{e}}{\alpha} \frac{t}{\tau_\mathrm{rep}}\right)

and with :math:`g(x)=\sum_{m=1}^{\infty}m^{-2}\left[1-\exp(-m^2 x)\right]`.
The sticky reptation time is :math:`\tau_\mathrm{rep} = \tau_\mathrm{s}Z_\mathrm{s}^2Z_\mathrm{e}`.





Recommendations
---------------
To verify the theory, the calculated viscosity :math:`\eta_0 = G_\mathrm{e}\times \tau_\mathrm{s}Z_\mathrm{s}^2 Z_\mathrm{e}/\alpha`: should be close to the experimental value. 
Further, the fitted value of the elastic plateau modulus should be close to

.. math::
    G_\mathrm{e} = \dfrac{4}{5}\dfrac{\phi Z_\mathrm{e}}{\upsilon N} k_\mathrm{B}T

with :math:`\phi` the volume fraction occupied by the polymer, :math:`\upsilon` the volume of a monomer and :math:`N` the number of monomers per chain.
:math:`k_\mathrm{B}` is Boltzmann's constant and :math:`T` is the absolute temperature in Kelvin.

.. rubric:: References

.. bibliography:: ../bibliography.bib
    :style: unsrt
    :keyprefix: SRlve-

