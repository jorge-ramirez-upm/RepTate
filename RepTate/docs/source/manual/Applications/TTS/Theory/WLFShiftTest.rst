------------------------------------
Williams-Landel-Ferry TTS Shift Test
------------------------------------

.. toctree::
   :maxdepth: 2

Summary
-------

.. autoclass:: TheoryTTS_Test.TheoryWLFShiftTest()

Description
-----------
Time-temperature superposition based on a WLF equation with two parameters. Temperature :math:`T` of the data is read from the file. The temperature to which the data is shifted is specified by :math:`T_r`. This theory shifts many samples simultaneously with the same shift factors which follow exactly the WLF equation. Thus, if there is one temperature for which the data is out of line with the others, the theory does not try to hide it by using an arbitrary shifting - instead the shifted data will clearly show that one of the temperatures went  wrong. Also, the vertical shifts are applied according to the density change only, whereas in other rheometer software some loading errors are hidden into the vertical shifts. 

In the **horizontal shift**, the frequency is modified according to:

.. math::
    \omega(T_r) = a_T \omega(T)
    
with

.. math::
    \log_{10} a_T = \frac{-B_1 (T-T_r)}{(B_2+T_r)(B_2+T)} 

where :math:`B_1` and :math:`B_2` are material parameters. 

.. warning::
    * The equation and parameters are different with respect to the standard WLF definition. In the WLF equation, the values of the parameters :math:`C_1` and :math:`C_2` depend on the reference temperature :math:`T_r` to which the data is being shifted.
    * The parameters :math:`B_1` and :math:`B_2` do not depend on the choice of :math:`T_r` and thus are true material parameters.
    * The values the standard parameters :math:`C_1` and :math:`C_2` can be easily calculated from the values of :math:`B_1` and :math:`B_2` using the following expressions:
    .. math::
        \begin{eqnarray}
        C_1 & = \frac{B_1}{B_2+T_r} \\
        C_2 & = B_2 + T_r
        \end{eqnarray}
    * Similarly, the values of the parameters :math:`B_1` and :math:`B_2` can be easily calculated from the values of :math:`C_1` and :math:`C_2` from the literature using the following expressions:
    .. math::
        \begin{eqnarray}
        B_1 & = C_1C_2 \\
        B_2 & = C_2 - T_r
        \end{eqnarray}
    * Everytime RepTate calculates or fits the theory to a set of experimental data, it will output the values of the standard WLF parameters :math:`C_1` and :math:`C_2` at the temperature :math:`T_r` in the theory window.
    
In the **vertical shift**, the modulus is modified according to the expression:

.. math::
    G(T_r) = b_T G(T)
    
with

.. math::
    b_T = \frac{\rho(T_r)T_r}{\rho(T)T} = \frac{(1+\alpha T)(T_r+273.15)}{(1+\alpha T_r)(T+273.15)}
    
where :math:`\alpha` thermal expansion coefficient of the polymer at 0 °C.

The **molecular weight dependence** of :math:`T_g` must be considered when shift data of very short chains or very broad molecular weight distributions containing a significative fraction of short chains. This change is roughly related to the amount of free ends present in the sample. In order to take the effect into account, we use the following phenomenological expression, which was shown to fit the experimental data:

.. math::
    T_g = T_g^\infty - \frac{C_{T_g}}{M_w}
    
A simple chain ends argument leads to the same expression with :math:`M_n` instead of :math:`M_w` (here, we are assuming that :math:`M_w \approx M_n`). This leads to the following modified expression for the **horizontal shift**:

.. math::
    \log_{10} a_T = \frac{-B_1 (T-T_r+\frac{C_{T_g}}{M_w})}{(B_2+T_r)(B_2+\frac{C_{T_g}}{M_w}+T)} 

In most cases, when shifting the data of well entangled monodisperse polymers, this effect can be discarded by unticking the corresponding check box in the theory window.

.. warning::
    Try to shift simultaneously different samples of the same material, using the suggested values of the fitting parameters from the Materials Database or taking them from the literature.
    
.. warning::
    Load all the *.osc files in the same dataset.
    
.. warning::
    It is important to start the fit from reasonable values of the parameters :math:`B_1` and :math:`B_2`. Otherwise, the minisation procedure will produce wrong results.
    