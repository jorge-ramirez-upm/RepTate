=============================================
Tutorial: Adding new functionality to RepTate
=============================================

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
    
   - without transformation, :math:`x` vs :math:`y`
   - :math:`x` vs :math:`\sqrt{y}`

#. has a theory: a simple line fitting with two parameters :math:`a` and :math:`b` such that
   :math:`y = ax+b`.

.. tip::
    Each time we need to modify or add some line of Python code, the line number is indicated
    on the left hand side for information. 
    This should correspond to the same line numbering for the "template" files, but might
    be different for the files in the ``core/`` or ``gui/`` folders.

---------------
New application
---------------

Create a new application file
-----------------------------

To create a new RepTate application, we will use the template
application file ``ApplicationTemplate.py`` that can be found in the
``applications/`` folder.

#.  Make a copy of this file and rename it with a sensible name that 
    relates to the application purpose. According to the 
    :ref:`goals_section` section, we name it ``ApplicationXY.py``.

#.  Open ``ApplicationXY.py`` with your favourite text editor and
    replace **all** the occurrences of "Template" by "XY". For example, 
    
    .. code-block:: python
       :lineno-start: 44

        class ApplicationTemplate(QApplicationWindow):
    
    becomes

    .. code-block:: python
       :lineno-start: 44

        class ApplicationXY(QApplicationWindow):


#.  Give a brief description of the purpose of the application, 
    e.g. "Application reading XY files".
    The first lines of ``ApplicationXY.py`` should now look like

    .. code-block:: python
       :lineno-start: 33

       """Module ApplicationXY

       Application reading XY files

       """

The file ``ApplicationXY.py`` is ready for the next round of modifications
that are (i) file types accepted by the application, (ii) the views, 
and (iii) the theories, as defined in the :ref:`goals_section` section.
But first, we have to let RepTate know about our new application.

Edit RepTate's ``QApplicationManager``
--------------------------------------

We need to add a reference to this new application into 
RepTate's ``QApplicationManager``, so it knows it exists. To do so:

#.  Insert this line in the top part of the file ``gui/QsApplicationManager.py``,
    e.g.

    .. code-block:: python
       :lineno-start: 77

       from RepTate.applications.ApplicationXY import ApplicationXY

#.  Insert the following line to add an entry to the ``QApplicationManager`` dictionary

    .. code-block:: python
       :lineno-start: 155

       self.available_applications[ApplicationXY.appname] = ApplicationXY

In order to have our new application available in the Graphical 
User Interface (GUI), we need to create a new "button"
that will launch our new application when clicked.

#.  Add a button in the main RepTate tool-bar by inserting the following lines in 
    the ``__init__`` method of ``gui/QApplicationManager.py``. 
    The icon name (filename) should correspond to the ``appname``, here ``XY.png``. See 
    the section :ref:`new_icons` to create and use your onwn icon in RepTate.

    .. code-block:: python
       :lineno-start: 258

        # ApplicationXY button
        #choose the button icon
        icon = QIcon(':/Icon8/Images/new_icons/XY.png')
        tool_tip = 'XY'  # text that appear on hover
        self.actionXY = QAction(icon, tool_tip, self)
        #insert the new button before the "MWD" button
        self.toolBarApps.insertAction(self.actionMWD, self.actionXY)

#.  The new button has been successfully inserted into the application tool bar.
    However, if we click on it, nothing happens because it is not linked to any action.
    We need to "wire" (connect) this new button to a "function".
    In the same file ``gui/QApplicationManager.py``, below the previous lines,
    add

    .. code-block:: python
       :lineno-start: 266
        
        #connect button
        self.actionXY.triggered.connect(lambda: self.handle_new_app('XY'))

    .. warning::
        The application name (``appname``), defined at line 46 of ``ApplicationXY.py``, should then be "XY". 
        Additionally, the icon name defining the logo of the new application should be named "XY.png",
        see the definition of the ``handle_new_app`` method.

.. note:: 
    Our new application is ready to be used in RepTate!


Note on default theories
------------------------

By default, some "basic theories" are included with the application 
(e.g. polynomial, power-law, exponential). To remove all these 
"basic theories" from your new application, comment the following line
in the ``__init__`` method of ``class ApplicationXY``

 .. code-block:: python
    :lineno-start: 135

    self.add_common_theories()  # Add basic theories to the application


.. _file_type:

--------------
New file type
--------------

RepTate applications are designed to accept a only a 
predefined file extension. As defined in the :ref:`goals_section` section,
we want our new application ``ApplicationXY.py`` to accept ``.xy`` files.
To do so, we modify ``ApplicationXY.py`` as follows.

In ``class ApplicationXY``, before ``def __new__``, add

.. code-block:: python
    :lineno-start: 48

    extension = "xy"  # drag and drop this extension automatically opens this application

In the ``__init__`` method of ``class ApplicationXY`` add

.. code-block:: python
    :lineno-start: 86

    # set the type of files that ApplicationTemplate can open
    ftype = TXTColumnFile(
        name='XY data',  # name the type of data
        extension='xy',  # file extension
        description='XY data from XY-experiment',
        col_names=['X', 'Y'],  # name the variables for legend
        basic_file_parameters=['date', 'T'],  # parameter in file header
        col_units=['-', '-'])  # units of X and Y (here none)


---------
New view
---------

About the "old" view
--------------------

At the moment, only one view is allowed in our new ``ApplicationXY``. 
That view is located in the ``__init__`` method of
``class ApplicationXY``:

.. code-block:: python
    :lineno-start: 62

    # VIEWS
    # set the views that can be selected in the view combobox
    self.views['y(x)'] = View(
        name='y(x)',
        description='y as a function of x',
        x_label='x',
        y_label='y(x)',
        x_units='-',
        y_units='-',
        log_x=False,
        log_y=False,
        view_proc=self.viewyx,
        n=1,
        snames=['y(x)'])

The important attributes of the view called "y(x)" are: 

- the x- and y-label to be used in the plot,
- the units that are appended to the x- and y-labels,
- the ``log_x`` and ``log_y`` define whether the axes should be in
  in log-scale (base 10)
- ``self.viewyx`` is the method that defines what operations
  are done on the data before plotting them (see below),
- ``n`` defines the number of series the view is plotting.

In the line below, you can define the default number of view, 
i.e., the number of views that appear when you open the appliction.
In case the new application would benefit from having multiple views
shown at the same time (similar to the React or Stress Relaxation applications),
this number can be increased (up to 4)

.. code-block:: python
    :lineno-start: 75
    
    # set multiviews
    # default view order in multiplot views, set nplots=1 for single view
    self.nplots = 1

The definition of the method ``viewyx`` is 
given by

.. code-block:: python
    :lineno-start: 108
    
    def viewyx(self, dt, file_parameters):
        """Documentation"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True

The two lines ``x[:, 0] = dt.data[:, 0]`` and ``y[:, 0] = dt.data[:, 1]``
tell us that ``viewyx`` does not perform any operations on the data.
It simply copies the input data into ``x`` and ``y`` arrays. It means that 
we already have one of the views required from the :ref:`goals_section` section.

Definition of a new view
------------------------

To define a new view that shows :math:`x` vs :math:`\sqrt{y}`, as 
requested in the :ref:`goals_section` section, we add a view to
``self.views`` dictionary. The new view is called "sqrt(y)".
In the ``__init__`` method of ``class ApplicationXY``, add

.. code-block:: python
    :lineno-start: 74

    self.views['sqrt(y)'] = View(
        name='sqrt(y)',
        description='sqrt(y) as a function of x',
        x_label='x',
        y_label='$y^{1/2}$',
        x_units='-',
        y_units='-',
        log_x=False,
        log_y=False,
        view_proc=self.view_sqrt_y,
        n=1,
        snames=['sqrt(y)'])

.. tip::
    The ``x_label`` and ``y_label`` support LaTeX-like syntax.

We also need to define the new method ``view_sqrt_y``.
In ``class ApplicationXY``, add the definition

.. code-block:: python
    :lineno-start: 118
    
    def view_sqrt_y(self, dt, file_parameters):
        """Documentation"""
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = (dt.data[:, 1])**0.5
        return x, y, True

.. note::
    The new view is ready!

----------
New theory
----------

Create a new theory file
------------------------

To create a new RepTate application, we will use the template
theory file ``TheoryTemplate.py`` that can be found in RepTate
``theories/`` folder.

#.  Make a copy of this file and rename it with a sensible name that 
    relates to the theory purpose. According to the 
    :ref:`goals_section` section, we name it ``TheoryLine.py``.

#.  Open ``TheoryLine.py`` with your favourite text editor and
    replace **all** the occurrences of "Template" by "Line". For example, 
    
    .. code-block:: python
       :lineno-start: 42

        class TheoryTemplate(QTheory):
    
    becomes

    .. code-block:: python
       :lineno-start: 42

        class TheoryLine(QTheory):

#.  Give a brief description of the purpose of the application, 
    e.g. " Theory fitting a line to the data".
    The first lines of ``TheoryLine.py`` should now look like

    .. code-block:: python
       :lineno-start: 33

       """Module TheoryLine

       Theory fitting a line to the data

       """
       import numpy as np

The file ``TheoryLine.py`` is ready for the next round of modifications
that are (i) define the parameters, (ii) define the theory "function".
But first, we have to let ApplicationXY (developed just above) know about 
our new theory.

Edit ``ApplicationXY.py``
-------------------------------------

We need to add a reference to this new theory into 
``ApplicationXY.py``, so it knows it exists. To do so:

#.  Insert the following line in the ``__init__`` method of
    ``class ApplicationXY``, after the "``# IMPORT THEORIES``" comment

    .. code-block:: python
       :lineno-start: 54
        
        # IMPORT THEORIES
        # Import theories specific to the Application e.g.:
        from RepTate.theories.TheoryLine import TheoryLine

    .. hint::
        We choose to place the theories ``import``
        inside the ``__init__`` method of ``class ApplicationXY`` 
        rather than in the very top of the file
        ``ApplicationXY.py`` as this prevents RepTate from loading
        all theories at start. Instead, theories are loaded only when an application
        using them is opened.

#.  Insert the following line, also in the ``__init__`` method of
    ``class ApplicationXY``, after the ``# THEORIES``, and before
    ``self.add_common_theories()``, the line

    .. code-block:: python
       :lineno-start: 102

        self.theories[TheoryLine.thname] = TheoryLine

Edit the theory 
---------------
According to the :ref:`goals_section` section, the theory should define a straight line
:math:`y=ax+b`, hence there are two parameters. We will (i) write a short documentation of
our new theory, (ii) define the parameters, and (iii) write the main function that
calculates the theory values.
  
#.  Add a Python docstring to (auto)-document the theory. Place some description of the goal of the theory
    as well as a description of the parameters. This will help future reader of the file understand
    the purpose of the theory and it will be automatically integrated to the
    online RepTate documentation (`reptate.readthedocs <http://reptate.readthedocs.io/>`_).

    .. code-block:: python
       :lineno-start: 42

        class TheoryLine(QTheory):
            """Fit a straight line. 
            
            * **Function**
                .. math::
                    y = a x + b
            
            * **Parameters**
            - :math:`a`: slope of the line
            - :math:`b`: the :math:`y`:-intercept

            """

#.  To define the theory parameters, :math:`a` and :math:`b`, we modify the
    ``__init__`` method of ``class TheoryLine`` to have only these two
    parameter definitions

    .. code-block:: python
       :lineno-start: 60

        self.parameters['a'] = Parameter(
            name='a',
            value=1,
            description='parameter a',
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters['b'] = Parameter(
            name='b',
            value=0,
            description='parameter b',
            type=ParameterType.real,
            opt_type=OptType.opt)
    
    The important attributes of the parameters are:
    
    - ``value``: the initial value of the parameter
    - ``type``: defines if he parameter is real, integer or discrete
    - ``opt_type``: optimisation type is either ``const`` for constant parameter
      (cannot be optimised),
      ``opt`` if the parameter is optimised by default, 
      ``nopt`` if the parameter can
      be optimised but is not by default.


#.  Modify the method ``calculate`` of ``class TheoryLine``

    .. code-block:: python
       :lineno-start: 89

        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        a = self.parameters['a'].value
        b = self.parameters['b'].value
        tt.data[:, 0] = ft.data[:, 0]  # x values
        tt.data[:, 1] = a * ft.data[:, 0] + b  # y values

    .. hint::
        
        - The file type of ``ApplicationXY`` defined in section :ref:`file_type`
          tells us that there are **two** columns in the data files. Hence, the theory
          data also have two columns to populate. For example of application/theory using
          more than two data columns, see ``class ApplicationLVE`` of ``ApplicationLVE.py`` 
          and ``class TheoryMaxwellModesFrequency``
          of ``TheoryMaxwellModes.py``.
        - The information from the data file header, in our example ``date`` and
          ``T``, can be called via, e.g. ``T = float(f.file_parameters["T"])``.
          Parameters are stored as strings, hence the ``float`` conversion.

.. note::
    The new "Line" theory is ready to be used in our new ApplicationXY!

.. _new_icons:

---------
New Icons
---------

Application icons are stored in a compiled resource file
``gui/MainWindow_rc.py``.
In order to add a new icon to this resource file, that can later be used as
a button icon for instance, we need to

#.  Modify the file ``gui/MainWindow.qrc`` by opening it in a text editor
    and add the relative path of the new image or icon we want to 
    have in the resource file.
    For instance: 
    
    - copy and paste you favourite icon ``my_favourite_icon.png`` 
      in the ``gui/Images/new_icons/`` folder.
    - add the line ``<file>Images/new_icons/my_favourite_icon.png</file>``
      to the file ``gui/MainWindow.qrc``

#.  Re-compile the file ``MainWindow_rc.py`` into a resource file
    ``MainWindow_rc.py`` by running the following command in a
    terminal (assuming the current working directory is ``gui/``)
    
    ..  code-block:: bash
        
        $ rcc MainWindow.qrc -o MainWindow_rc.py

.. note::
    Your new icon ``my_favourite_icon.png`` is now ready to be used
    by Qt:

    ::
    
      icon = QIcon(':/Icons/Images/new_icons/my_favourite_icon.png')
