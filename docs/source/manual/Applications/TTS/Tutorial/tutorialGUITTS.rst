======================================
TTS Tutorial: Graphical User Interface
======================================

.. contents:: Contents
    :local:

.. toctree::
   :maxdepth: 2

.. |logo| image:: /app_logo/TTS.png
    :width: 20pt
    :height: 20pt
    :align: bottom

.. |einstein| image:: /gui_icons/icons8-einstein.png
    :width: 20pt
    :height: 20pt
    :align: bottom

.. |fit| image:: /gui_icons/icons8-minimum-value.png
    :width: 20pt
    :height: 20pt
    :align: bottom

.. |th_save| image:: /gui_icons/icons8-save_TH.png
    :width: 20pt
    :height: 20pt
    :align: bottom

.. |theory| image:: images/TTS_theoryWLF.png
    :height: 20pt
    :align: bottom

.. |arrow_up| image:: /gui_icons/icons8-vertical-shift.png
    :height: 20pt
    :align: bottom

.. |iso| image:: /gui_icons/icons8-iso.png
    :height: 20pt
    :align: bottom

#.  Start RepTate and create a new LVE Application |logo|:

    .. image:: images/TTS_app.png
        :width: 75%
        :align: center
        :alt: New application

#.  Drag and drop files with ``.osc`` extension, e.g. the set of ``PI_*.osc`` files in the ``data/PI_LINEAR/osc/`` 
    folder. See :ref:`TTS_Data_Description` for a description of the data file organization.
   
    .. image:: images/TTS_data.png
        :width: 75%
        :align: center
        :alt: Load data

#.  Select a theory, e.g. "WLF Shift" |theory|, and press |einstein| to create it (calculation is done with default parameter values).
    Press "Minimize Error" |fit|.
    
    .. image:: images/TTS_shift.png
        :width: 75%
        :align: center
        :alt: New theory

#.  Change a parameter, e.g. set the reference temperature to :math:`T_0=-40^\circ`\ C, and press "Minimize Error" |fit|.

    .. image:: images/TTS_T-40.png
        :width: 75%
        :align: center
        :alt: New theory

#.  To save the theory line(s), click the |th_save| button.
    A dialog will ask for a folder where the theory files will be saved.

.. note:: 
    When the "Vertical Shift" button |arrow_up| is checked, 
    vertical shift of the data is allowed.

.. todo::
    When the "Shift to Isofrictional State" button |iso| is checked ...
