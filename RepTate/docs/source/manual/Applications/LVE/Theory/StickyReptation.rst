----------------
Sticky Reptation
----------------

.. toctree::
   :maxdepth: 2

Summary
-------

.. autoclass:: StickyReptation.TheoryStickyReptation()
   
Description
-----------

Theory for the linear rheology of linear entangled polymers with a number of stickers that can form reversible intramolecular crosslinks.
The relaxation modulus, :math:`G(t)`, is modeled as the sum of a Sticky-Rouse, :math:`G_\mathrm{SR}(t)`, (Leibler-Rubinstein-Colby, 1991 :cite:`Leibler1991`) and a Double-Reptation, :math:`G_\mathrm{rep}(t)`, (des Cloizeaux, 1990 :cite:`desCloizeaux1990`) contribution,

.. math::
    G(t) = G_\mathrm{SR}(t) + G_\mathrm{rep}(t)

with 

.. math::
    G_\mathrm{SR}(t) = \frac{G_\mathrm{e}}{Z_\mathrm{e}} \sum_{q=1}^{Z_\mathrm{s}/2} \kappa \exp\left(\dfrac{q^2 t}{\tau_\mathrm{s} (Z_\mathrm{s}/2)^2}.

This equation assumes that most stickers are bound, and after sticker dissociation a strand of length :math:`2N/Z_\mathrm{s}` can relax, with :math:`N` the number of monomers per chain and :math:`Z_\mathrm{s}` the number of stickers per chain. :math:`\tau_\mathrm{s}` is the dissociation time of a sticker.
The truncation :math:`Z_\mathrm{s}/2` implies that we ignore high-frequency (non-sticky) Rouse relaxation of the subchains between stickers.

.. warning::
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


Parameters
----------
:math:`G_\mathrm{e}`: elastic plateau modulus
:math:`Z_\mathrm{e}`: number of entanglements per chain
:math:`Z_\mathrm{s}`: number of stickers per chain
:math:`\tau_\mathrm{s}`: sticker dissociation time
:math:`\alpha`: dimensionless constant (value around 10) that is in principle universal.


.. rubric:: References

.. bibliography:: ../bibliography.bib
    :style: unsrt
    :keyprefix: boblve-

