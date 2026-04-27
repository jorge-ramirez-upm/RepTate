- The first line of the file should contain the sample parameters separated by semi-colons (``;``). 
  It may contain any number of parameters which will be read and saved as file-parameter in RepTate.
  In unit-aware applications, a file parameter value may also include an
  explicit unit, for example ``Mw=1131 Da;T=25 ºC;gdot=0.1 1/s;``.

- Then the data columns should appear, separated by **spaces** or **tabs**.

- In unit-aware applications, column headers may include units in square
  brackets or parentheses, for example ``t [min]`` or ``G' [kPa]``. See
  :ref:`Units <units>` for the supported units and current
  limitations.
