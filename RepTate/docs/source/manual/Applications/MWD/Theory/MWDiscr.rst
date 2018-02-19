==================
MWD Discretization
==================

.. |piggy| image:: /gui_icons/icons8-money-box.png
    :width: 20pt
    :height: 20pt
    :align: bottom
    
	
.. |fileparam| image:: ../Tutorial/images/file_parameters.png
    :height: 20pt
    :align: bottom

.. |thparam| image:: ../Tutorial/images/th_parameters.png
    :width: 45pt
    :align: bottom


- The number average, weight average and polydispersity index, :math:`M_n` , :math:`M_w` and :math:`\text{PDI}`, respectively, of the original data are calculated and
  reported into the file parameters panel: |fileparam| where

  .. math::

    M_n &= \dfrac{1}{\sum_i w_i/M_i} \\
    M_w &= \sum_i w_i M_i \\
    \text{PDI} &= \dfrac{M_w}{M_n}

  The theory parameters panel shows these values for the discretized distribution: |thparam|.

- The area, :math:`\phi_i`, of each greay bin corresponds to the area under the data curve delimited by the bin edges.
  The height, :math:`h_i` of the bin is the area divided by the bin width (on a :math:`\log_{10}` scale).

  You can change the number of bins and move the bin edges by dragging the yellow markers.

- In the bottom of the plot, the grey tick marks indicate the bin molecular weight
  taken as the weight-average molecular mass value across the bin width

    .. math::
        M_{w,i} = \frac{\sum w_j M_j}{\sum w_j}.

#.  To save the discretized molecular weight, click the |piggy| button.

    The output file contains a header with the moments  :math:`M_n`, :math:`M_w` and the `PDI`, and two columns.
    The first column is the molecular weight :math:`M_{w,i}` as indicated by the grey tick marks, 
    the second column is the value of the area of the covered by the bin, :math:`\phi_i`. 

    The sum of the areas should equal 1:

    .. math::
       \sum \phi_i = 1.
