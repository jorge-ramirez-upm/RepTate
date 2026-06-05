---------------------------
Baumgaertel-Winter modes
---------------------------

.. toctree::
   :maxdepth: 2

Summary
-------

.. automodule:: RepTate.theories.TheoryBaumgaertelWinter.TheoryBaumgaertelWinterTime

Description
-----------

Fit of stress-relaxation data with a discrete set of Maxwell modes using the 
Baumgaertel-Winter method to adjust the number of modes. The relaxation modulus is written as:

.. math::
    G(t) = G_e + \sum_i G_i \exp(-t/\tau_i)

where :math:`\tau_i` is the relaxation time and :math:`G_i` is the modulus of
mode :math:`i`. In contrast to the standard ``Maxwell modes`` theory, the
relaxation times are not constrained to be equally spaced in logarithmic scale.
Both :math:`\tau_i` and :math:`G_i` are independent adjustable parameters,
stored as ``logtauXX`` and ``logGXX`` in logarithmic scale. The optional
equilibrium modulus is controlled by ``Ge``.

The number of modes is selected with the spinbox in the theory toolbar. Mode
markers are shown on the current plot when ``View modes`` is active. Dragging a
marker changes both the relaxation time and the modulus of that individual
mode; the neighboring modes are not redistributed.

The modes menu provides tools to load modes from a text file, get modes from
another open RepTate theory, and save the current spectrum. The **broom button**
starts a conservative simplification procedure that merges close modes and can
remove redundant modes only when the residual increase remains within the
configured limits. The adjacent configuration button controls the separation
and residual thresholds used by that procedure.

Right-clicking directly on a Baumgaertel-Winter mode marker opens a small
context menu. Choose ``Delete Mode`` to remove that mode manually. At least one
mode must remain.

.. warning::
    The theory can only be applied to one file per data set.
    If more than one file is active in the current data set,
    the theory will be applied to the first one in the list of active files.

