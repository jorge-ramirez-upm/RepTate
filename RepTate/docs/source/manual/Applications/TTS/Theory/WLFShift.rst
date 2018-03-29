===============================
Williams-Landel-Ferry TTS Shift
===============================

.. toctree::
   :maxdepth: 2

Summary
-------

.. autoclass:: TheoryTTS.TheoryWLFShift()

Description
-----------
Time-temperature superposition based on a WLF equation with two parameters. Temperature of the data is read from the file. The temperature to which the data is shifted is specified by :math:`T_0`. This theory shifts many samples simultaneously with the same shift factors which follow exactly the WLF equation. Thus, if there is one temperature for which the data is out of line with the others, the theory does not try to hide it by using an arbitrary shifting - instead the shifted data will clearly show that one of the temperatures went  wrong. Also, the vertical shifts are applied according to the density change only, whereas in other rheometer software some loading errors are hidden into the vertical shifts. 

In the **horizontal shift**, the frequency is modified according to:

.. math::
    \omega(T_0) = a_T \omega(T)
    
with

.. math::
    \log_{10} a_T = \frac{-C_1 (T-T_0)}{T+C_2}

where :math:`C_1` and :math:`C_2` are material parameters. Note that in many publications the denominator of this equation contains :math:`T_0` as well - in this case :math:`C_2` depends on :math:`T_0`. The parameter :math:`C_1` depends on the temperature :math:`T_0`. If :math:`T_0` is changed from :math:`T_0^{old}` to :math:`T_0^{new}`, the value of :math:`C_1` changes according to the expression:

.. math::
    C_1^{new} = C_1^{old}\frac{T_0^{old}+C_2}{T_0^{new}+C_2}
    
In the **vertical shift**, the modulus is modified according to the expression:

.. math::
    G(T_0) = G(T)/b_T
    
with

.. math::
    b_T = \frac{\rho(T)T}{\rho(T_0)T_0} = \frac{(\rho_0-T C_3\cdot 10^{-3})(T+273.15)}{(\rho_0-T_0 C_3\cdot 10^{-3})(T_0+273.15)}
    
where :math:`\rho_0` is the density of the polymer at 0 degrees Celsius.

The **molecular weight dependence** of :math:`T_g` must be considered when shift data of very short chains or very broad molecular weight distributions containing a significative fraction of short chains. This change is roughly related to the amount of free ends present in the sample. In order to take the effect into account, we use the following phenomenological expression, which was shown to fit the experimental data:

.. math::
    T_g = T_g^\infty - \frac{C_{T_g}}{M_w}
    
A simple chain ends argument leads to the same expression with :math:`M_n` instead of :math:`M_w` (here, we are assuming that :math:`M_w \approx M_n`). This leads to the following modified expression for the **horizontal shift**:

.. math::
    \log_{10} a_T = \frac{-C_1 (T-T_0+\frac{C_{T_g}}{M_w})}{T+C_2+\frac{C_{T_g}}{M_w}}

In most cases, when shifting the data of well entangled monodisperse polymers, this effect can be discarded by unticking the corresponding check box in the theory window.

.. warning::
    Try to shift simultaneously different samples of the same material, using the suggested values of the fitting parameters from the Materials Database or taking them from the literature.
    
.. warning::
    Load all the *.osc files in the same dataset.
    