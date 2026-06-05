----------------------------------------
Baumgaertel-Winter retardation modes
----------------------------------------

.. toctree::
   :maxdepth: 2

Summary
-------

.. automodule:: RepTate.theories.TheoryBaumgaertelWinter.TheoryBaumgaertelWinterRetardation

Description
-----------

Fit of creep data with a discrete set of retardation modes using a Baumgaertel-Winter-like
method to simplify the spectrum. The creep strain is calculated as:

.. math::
    \gamma(t) = \sigma_0 \left[
        J_0 + \sum_i J_i \left(1-\exp(-t/\tau_i)\right)
        + \frac{t}{\eta_0}
    \right]

where :math:`\sigma_0` is the stress read from the file parameters,
:math:`J_0` is the instantaneous compliance, :math:`\eta_0` is the terminal
viscosity, :math:`\tau_i` is the retardation time, and :math:`J_i` is the
compliance of mode :math:`i`.

In contrast to the standard ``Retardation modes`` theory, the retardation times
are not constrained to be equally spaced in logarithmic scale. Both
:math:`\tau_i` and :math:`J_i` are independent adjustable parameters, stored as
``logtauXX`` and ``logJXX`` in logarithmic scale. The instantaneous compliance
and terminal viscosity are controlled by ``logJini`` and ``logeta0``.

The number of modes is selected with the spinbox in the theory toolbar. Mode
markers are shown on the current plot when ``View modes`` is active. Dragging a
marker changes both the retardation time and the compliance of that individual
mode; the neighboring modes are not redistributed.

The modes menu provides tools to load modes from a text file, get modes from
another open RepTate theory, and save the current spectrum. Saved retardation
mode files are labeled with :math:`J_i`. The **broom button** starts a conservative
simplification procedure that merges close modes only when the residual
increase remains within the configured step and cumulative limits. Because
individual retardation compliances are often very small, amplitude-based
``weak mode`` deletion and general trial deletion are disabled by default for
this theory. They can be adjusted from the simplification configuration dialog.

Right-clicking directly on a Baumgaertel-Winter retardation mode marker opens a
small context menu. Choose ``Delete Mode`` to remove that mode manually. At
least one mode must remain.

.. warning::
    The theory can only be applied to one file per data set.
    If more than one file is active in the current data set,
    the theory will be applied to the first one in the list of active files.

