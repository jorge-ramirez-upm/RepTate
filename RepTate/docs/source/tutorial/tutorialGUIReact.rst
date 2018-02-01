==========================
Tutorial React Application
==========================

.. toctree::
   :maxdepth: 2

.. |Reactapp| image:: GUI_tutorial_images/icons8-test-tube.png
    :width: 20pt
    :height: 20pt
    :align: bottom
    
.. |TobitaBatchTh| image:: GUI_tutorial_images/TobitaBatchTh.png
    :height: 15pt
    :align: bottom

.. |thparam| image:: GUI_tutorial_images/th_parameters.png
    :width: 40pt
    :align: bottom

.. |einstein| image:: GUI_tutorial_images/icons8-einstein.png
    :width: 20pt
    :height: 20pt
    :align: bottom

.. |bob-hat| image:: GUI_tutorial_images/icons8-bob-hat.png
    :width: 20pt
    :height: 20pt
    :align: bottom

.. |piggy| image:: GUI_tutorial_images/icons8-money-box.png
    :width: 20pt
    :height: 20pt
    :align: bottom

Discretization of a GPC molecular weight distribution
-------------------------------------------------------

#.  Start RepTate and create a new React Application |Reactapp|:
    
    .. image:: GUI_tutorial_images/open_React_app.png
        :width: 400pt
        :align: center
        :alt: New React application

#.  Drag and drop a file with a `.reac` extension, e.g. `out1.reac` in the `data/React/` folder.

    The first column should contain the molecular mass :math:`M`, the second column the 
    relative molecular weight :math:`w(\log(M))`, the third column :math:`g`, 
    and the fourth column the number of branching per 1000 carbon.
   
    .. image:: GUI_tutorial_images/open_react_file.png
        :width: 400pt
        :align: center
        :alt: Load data

#.  Select the "TobitaBatchTh" theory |TobitaBatchTh| and press |einstein| to create it.
    
    .. image:: GUI_tutorial_images/create_tobita_batch_theory.png
        :width: 400pt
        :align: center
        :alt: New TobitaBatch theory


#.  To adjust the BoB binning settings, click the |bob-hat| button.

#.  To save the polymer configuration for BoB, click the |piggy| button.



