===================================
Adding new functionality to RepTate
===================================

.. contents:: Contents
    :local:

.. role:: python(code)
    :language: python

.. _goals_section:

-----
Goals
-----

In this section, we will present how to create a new RepTate application.
We will show the important steps needed to build a new RepTate application.
To do so, we will need to modify some already existing RepTate code, as well
as writing new custom code.

As an example, let us say that we want to create a new RepTate application that:
  
#. accepts text files (``.xy``) which are supposed to be composed of:
   
   - a first line (header) containing the ``date`` and temperature ``T``
   - two columns containing data :math:`x` and :math:`y`

#. allows to view the data:
    
   - without transformation
   - without transformation in log-log scale
   - :math:`x` vs :math:`\sqrt{y}`

#. has a theory [...]



----------------
New applications
----------------

Create a new application file
-----------------------------

To create a new RepTate application, we will use the template
application file ``ApplicationTemplate.py`` that can be found in the
``applications/`` folder.

#.  Make a copy of this file and rename it with a sensible name that 
    relates to the application purpose. According to the 
    :ref:`goals_section` section, we name it ``ApplicationXY.py``.

#.  Open ``ApplicationXY.py`` with your favourite text editor and
    replace **all** the occurences of "Template" by "XY". For example, 
    
    .. code-block:: python
       :lineno-start: 46

        class ApplicationTemplate(CmdBase):
    
    becomes

    .. code-block:: python
       :lineno-start: 46

        class ApplicationXY(CmdBase):


#.  Give a brief description of the purpose of the application, 
    e.g. "Application reading general text files".
    The first lines of ``ApplicationXY.py`` should now look like

    .. code-block:: python
       :lineno-start: 33

       """Module ApplicationXY

       Application reading general text files

       """

The file ``ApplicationXY.py`` is ready for the next round of modifications
that are (i) file types accepted by the application, (ii) the views, 
and (iii) the theories, as defined in the :ref:`goals_section` section.
But first, we have to let RepTate know about our new application.

Edit RepTate's ``ApplicationManager``
-------------------------------------

We need to add a reference to this new application into 
RepTate's ``ApplicationManager``, so it knows it exists. To do so:

#.  Insert this line in the top part of the file ``core/ApplicationManager.py``,
    e.g.

    .. code-block:: python
       :lineno-start: 51

       from ApplicationXY import ApplicationXY

    and add this line to add an entry to the ``ApplicationManager`` dictionary

    .. code-block:: python
       :lineno-start: 104

       self.available_applications[ApplicationXY.name] = ApplicationXY

Our new application is ready to be used in Command Line RepTate!

Edit RepTate's ``QApplicationManager``
--------------------------------------

In order to have our new application available in the Graphical 
User Interface (GUI) version of RepTate (and not just available in the
Command-Line version of RepTate), we need to create a new "button"
that will launch our new application when clicked.
We will edit the file ``gui/QApplicationManager.py`` in this purpose.

#.  Add a button in the main RepTate tool-bar by inserting these line in 
    ``gui/QApplicationManager.py``. The icon we choose is 
    "icons8-scatter-plot.png" which is readily part of RepTate.
    To add a new custom icon to RepTate icon database, see 
    the section  :ref:`new_icons`.

    .. code-block:: python
       :lineno-start: 100

        # ApplicationXY button
        #choose the button icon
        icon = QIcon(':/Icon8/Images/new_icons/icons8-scatter-plot.png')
        tool_tip = 'XY'  # text that appear on hover
        self.actionXY = QAction(icon, tool_tip, self)
        #insert the new button before the "MWD" button
        self.toolBar.insertAction(self.actionMWD, self.actionXY)

#.  The new button has been succefuly inserted into the application tool bar.
    However, if we click on it, nothing happens because it is not linked to any action.
    We need to "wire" (connect) this new button to a "function".
    In the same file ``gui/QApplicationManager.py``, below the previous lines,
    add

    .. code-block:: python
       :lineno-start: 107
        
        #connect button
        self.actionXY.triggered.connect(self.new_xy_window)

#.  We need to define the function ``new_xy_window`` as it does not exist yet:

    .. code-block:: python
       :lineno-start: 352

        def new_xy_window(self):
        """Open a new XY application window
        
        [description]
        """
        app_name = "XY" 
        return self.Qopen_app(app_name,
                                ':/Icons/Images/new_icons/icons8-scatter-plot.png')

    .. note::
        The ``app_name`` must be identical to the ``name`` defined
        in the file ``applications/ApplicationXY.py``, i.e., it should match

        .. code-block:: python
            :lineno-start: 46

            class ApplicationXY(CmdBase):
                """[summary]
                
                [description]
                """
                name = 'XY'

Our new application is ready to be used in GUI RepTate!


--------------
New file types
--------------

RepTate applications are designed to accept a only a 
predifine file extension. As defined in the :ref:`goals_section` section,
we want our new application ``ApplicationXY.py`` to accept ``.xy`` files.
To do so, we modify ``class BaseApplicationXY`` of ``ApplicationXY.py`` 
as follows:


    .. code-block:: python
       :lineno-start: 53

       extension = "xy"  # drag and drop this extension automatically opens this application

    .. code-block:: python
       :lineno-start: 116

        ftype = TXTColumnFile(
            name='XY data',  # name the type of data
            extension='xy',  # file extension
            description='XY data from XY-experimemt',
            col_names=['X', 'Y'],  # name the variables for legend
            basic_file_parameters=['date', 'T'],  # parameter in file header
            col_units=['-', '-'])  # units of X and Y (here none)

---------
New views
---------

------------
New theories
------------


.. _new_icons:

---------
New Icons
---------


