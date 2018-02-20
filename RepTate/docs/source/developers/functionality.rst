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
    
   - without transformation, :math:`x` vs :math:`y`
   - :math:`x` vs :math:`\sqrt{y}`

#. has a theory [...]


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
       :lineno-start: 46

        class ApplicationTemplate(CmdBase):
    
    becomes

    .. code-block:: python
       :lineno-start: 46

        class ApplicationXY(CmdBase):


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

Edit RepTate's ``ApplicationManager``
-------------------------------------

We need to add a reference to this new application into 
RepTate's ``ApplicationManager``, so it knows it exists. To do so:

#.  Insert this line in the top part of the file ``core/ApplicationManager.py``,
    e.g.

    .. code-block:: python
       :lineno-start: 51

       from ApplicationXY import ApplicationXY

#.  Insert the following line to add an entry to the ``ApplicationManager`` dictionary

    .. code-block:: python
       :lineno-start: 104

       self.available_applications[ApplicationXY.name] = ApplicationXY

.. note::
    Our new application is ready to be used in Command Line RepTate!

Edit RepTate's ``QApplicationManager``
--------------------------------------

In order to have our new application available in the Graphical 
User Interface (GUI) version of RepTate (and not just available in the
Command-Line version of RepTate), we need to create a new "button"
that will launch our new application when clicked.
We will edit the file ``gui/QApplicationManager.py`` in this purpose.

#.  Add a button in the main RepTate tool-bar by inserting these lines in 
    ``gui/QApplicationManager.py``. The icon we choose is 
    "icons8-scatter-plot.png" which is readily part of RepTate icons database.
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

#.  The new button has been successfully inserted into the application tool bar.
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

    .. warning::
        The ``app_name`` must be identical to the ``name`` defined
        in the file ``applications/ApplicationXY.py``, i.e., it should match

        .. code-block:: python
            :lineno-start: 46

            class ApplicationXY(CmdBase):
                """[summary]
                
                [description]
                """
                name = 'XY'

.. note:: 
    Our new application is ready to be used in GUI RepTate!


--------------
New file types
--------------

RepTate applications are designed to accept a only a 
predefined file extension. As defined in the :ref:`goals_section` section,
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
            description='XY data from XY-experiment',
            col_names=['X', 'Y'],  # name the variables for legend
            basic_file_parameters=['date', 'T'],  # parameter in file header
            col_units=['-', '-'])  # units of X and Y (here none)


---------
New views
---------

About the "old" view
--------------------

At the moment, only one view is allowed in our ``ApplicationXY``. 
It can be seen in ``applications/ApplicationXY.py``:

    .. code-block:: python
       :lineno-start: 96

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
- ``self.viewyx`` is the function that defines what operations
  are done on the data before plotting them (see below),
- ``n`` defines the number of series the view is plotting.

The definition of the function ``self.viewyx`` is 

    .. code-block:: python
       :lineno-start: 138
        
        def viewyx(self, dt, file_parameters):
            """[summary]
            
            [description]
            
            Arguments:
                dt {[type]} -- [description]
                file_parameters {[type]} -- [description]
            
            Returns:
                [type] -- [description]
            """
            x = np.zeros((dt.num_rows, 1))
            y = np.zeros((dt.num_rows, 1))
            x[:, 0] = dt.data[:, 0]
            y[:, 0] = dt.data[:, 1]
            return x, y, True

The two lines ``x[:, 0] = dt.data[:, 0]`` and ``y[:, 0] = dt.data[:, 1]``
tell us that this function does not perform any operations on the data.
It simply copies the input data into ``x`` and ``y`` arrays. It means that 
we already have one of the views required from the :ref:`goals_section` section.

Definition of a new view
------------------------

To define a new view that shows :math:`x` vs :math:`\sqrt{y}`, as 
requested in the :ref:`goals_section` section, we add a view to
``self.views`` dictionary. The new view is called "sqrt(y)"

    .. code-block:: python
       :lineno-start: 111

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

We also need to define the function ``self.view_sqrt_y``
    
    .. code-block:: python
       :lineno-start: 169
        
        def view_sqrt_y(self, dt, file_parameters):
            """[summary]
            
            [description]
            
            Arguments:
                dt {[type]} -- [description]
                file_parameters {[type]} -- [description]
            
            Returns:
                [type] -- [description]
            """
            x = np.zeros((dt.num_rows, 1))
            y = np.zeros((dt.num_rows, 1))
            x[:, 0] = dt.data[:, 0]
            y[:, 0] = (dt.data[:, 1])**0.5
            return x, y, True

.. note::
    The new view is ready!

------------
New theories
------------



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
    ``gui/MainWindow_rc.py`` by running the following command in a
    terminal (assuming the current working directory is ``gui/``)
    
    ..  code-block:: bash
        
        pyrcc5 MainWindow.qrc -o MainWindow_rc.py

.. note::
    Your new icon ``my_favourite_icon.png`` is now ready to be used
    by Qt:

    ::
    
      icon = QIcon(':/Icons/Images/new_icons/my_favourite_icon.png')
