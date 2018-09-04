======================================
MWD Tutorial: Graphical User Interface
======================================

.. |logo| image:: /app_logo/MWD.png
    :width: 20pt
    :height: 20pt
    :align: bottom

.. |einstein| image:: /gui_icons/icons8-einstein.png
    :width: 20pt
    :height: 20pt
    :align: bottom

.. |th_save| image:: /gui_icons/icons8-save_TH.png
    :width: 20pt
    :height: 20pt
    :align: bottom
    
.. |MWDiscr| image:: images/MWDiscr.png
    :height: 15pt
    :align: bottom
	
.. |fileparam| image:: images/file_parameters.png
    :height: 20pt
    :align: bottom

.. |thparam| image:: images/th_parameters.png
    :width: 45pt
    :align: bottom


**Discretization of a GPC molecular weight distribution**

#.  Start RepTate and create a new MWD Application |logo|:
    
    .. image:: images/open_MWD_app.png
        :width: 75%
        :align: center
        :alt: New MWD application

#.  Drag and drop a file with a ``.gpc`` extension, e.g. ``ps2.gpc`` in the ``data/PS_Linear_Polydisperse/`` folder.

    The first column of the file should contain the molecular mass :math:`M`, and the second column the weight associated, :math:`\dfrac{\text d w(\log M)}{\text d \log M}`.
   
    .. image:: images/open_gpc_file.png
        :width: 75%
        :align: center
        :alt: Load data

#.  Select the "Molecular Weight Discretization" theory |MWDiscr| and press |einstein| to create it.
    
    .. image:: images/create_MWDiscr_theory.png
        :width: 75%
        :align: center
        :alt: New MWD theory
    
    The area of each bin corresponds to the area under the data curve delimited by the bin edges.
    The number- and weight-average molecular weight, together with the higher order moments 
    of the distribution, are calculated and reported in the theory text-box for both the input data and the discretized MW:
    
    .. image:: images/MWD_characteristics.png
        :width: 40%
        :align: center
        :alt: New MWD theory

#.  Adjust the number of molecular weight bins by changing the value in the theory panel.
    By default they are equally spaced on a logarithmic scale:

    .. image:: images/change_bin_number.png
        :width: 75%
        :align: center
        :alt: Adjust bin number

#.  In the bottom of the plot, the grey tick marks indicate the bin molecular weight.
    For each bin :math:`i`, it is taken as the weight-average molecular mass value across the bin width

    .. math::
        M_{w,i} = \frac{\sum w_j M_j}{\sum w_j}.

    The yellow markers indicate the bin edges, they can be dragged around:

    .. image:: images/move_bin_edge.png
        :width: 75%
        :align: center
        :alt: Move bin edge

    .. hint::
       To increase density of bins in an region, say the high M, we can set the number of bins to 1,
       then move the bin edges to the region of interest and increase the number of bins. This will increase the number of bins between the
       :math:`M_\mathrm{min}` and :math:`M_\mathrm{max}`.

#.  To save the discretized molecular weight, click the |th_save| button.

    The output file contains a header with the moments  :math:`M_n`, :math:`M_w` and the `PDI`, and two columns.
    The first column is the molecular weight :math:`M_{w,i}` as indicated by the grey tick marks, 
    the second column is the value of the area of the covered by the bin, :math:`\phi_i`. 

    The sum of the areas should equal 1:

    .. math::
       \sum \phi_i = 1.



