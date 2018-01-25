========================
Tutorial MWD Application
========================

.. toctree::
   :maxdepth: 2

.. |MWDapp| image:: GUI_tutorial_images/icons8-MWD.png
    :width: 20pt
    :height: 20pt
    :align: bottom

.. |einstein| image:: GUI_tutorial_images/icons8-einstein.png
    :width: 20pt
    :height: 20pt
    :align: bottom
    
.. |MWDiscr| image:: GUI_tutorial_images/MWDiscr.png
    :height: 15pt
    :align: bottom
.. |fileparam| image:: GUI_tutorial_images/file_parameters.png
    :height: 20pt
    :align: bottom

.. |thparam| image:: GUI_tutorial_images/th_parameters.png
    :width: 45pt
    :align: bottom

.. |piggy| image:: GUI_tutorial_images/icons8-money-box.png
    :width: 20pt
    :height: 20pt
    :align: bottom

Discretization of a GPC molecular weight distribution
------------------------------------------------------

#.  Start RepTate and create a new MWD Application |MWDapp|:
    
    .. image:: GUI_tutorial_images/open_MWD_app.png
        :width: 400pt
        :align: center
        :alt: New MWD application

#.  Drag and drop a file with a `.gpc` extension, e.g. `ps2.gpc` in the `data/PS_Linear_Polydisperse/` folder.

    The first column should contain the molecular mass :math:`M`, and the second column the relative molecular weight :math:`w(\log(M))`.
   
    .. image:: GUI_tutorial_images/open_gpc_file.png
        :width: 400pt
        :align: center
        :alt: Load data

#.  Select the "Molecular Weight Discretization" theory |MWDiscr| and press |einstein| to create it.
    
    .. image:: GUI_tutorial_images/create_MWDiscr_theory.png
        :width: 400pt
        :align: center
        :alt: New MWD theory
    
    The number average, weight average and polydispersity index, :math:`M_n` , :math:`M_w` and `PDI`, respectively, of the original data are calculated and
    reported into the file parameters panel: |fileparam|.
    
    The theory parameters panel shows these values for the discretized distribution: |thparam|.

    The area of each bin corresponds to the area under the data curve delimited by the bin edges.

#.  Adjust the number of molecular weight bins by changing the value in the theory panel.
    By default they are equally spaced on a logarithmic scale:

    .. image:: GUI_tutorial_images/change_bin_number.png
        :width: 400pt
        :align: center
        :alt: Adjust bin number

#.  In the bottom of the plot, the grey tick marks indicate the bin molecular weight.
    For each bin :math:`i`, it is taken as the weight-average molecular mass value across the bin width

    .. math::
        M_{w,i} = \frac{\sum w_j M_j}{\sum w_j}.

    The yellow markers indicate the bin edges, they can be dragged around:

    .. image:: GUI_tutorial_images/move_bin_edge.png
        :width: 400pt
        :align: center
        :alt: Move bin edge

#.  To save the discretized molecular weight. Click the |piggy| button.

    The output file contains a header with the moments  :math:`M_n`, :math:`M_w` and the `PDI`, and two columns.
    The first column is the molecular weight :math:`M_{w,i}` as indicated by the grey tick marks, 
    the second column is the value of the area of the covered by the bin, :math:`\phi_i`. 

    The sum of the areas should equal 1:

    .. math::
       \sum \phi_i = 1.



