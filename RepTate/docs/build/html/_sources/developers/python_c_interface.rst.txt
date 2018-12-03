=======================================
Tutorial: Interfacing Python and C code
=======================================

.. contents:: Contents
    :local:
    
-----
Goals
-----

In this section, we will show how to create a new Python function that makes use of C code
for computations and that can be later used in a theory or view.

Python offers rapid application development because it easier to write, to read (and therefore to maintain) than C code.
However, Python code used for number crunching might be 10 to 100 times slower than C
when Python `NumPy <http://www.numpy.org>`_ or `SciPy <https://www.scipy.org/scipylib/index.html>`_ 
libraries (written in C/C++ or Fortran) cannot be used.

Fortunately, there are many solutions available to write code that will run fast in Python. 
We can cite `Cython <http://cython.org>`_ or `Numba <https://numba.pydata.org>`_ that
transform Python code into C executable and require minimal addition to the existing Python 
code. There is also `Ctypes <https://docs.python.org/3.6/library/ctypes.html>`_ that provides 
C compatible data types, and allows calling functions 
from external libraries, e.g. calling pre-compiled C functions. It is a very effective means to communicate with existing C code.

.. note::
    All these solutions require a C compiler installed on your machine.

In RepTate, some theories (most notably the React application theories) are written in C code and interfaced with Python using,
`Ctypes <https://docs.python.org/3.6/library/ctypes.html>`_.

In general, already-written C code will require **no** modifications to be used by Python.
The only work we need to do to integrate C code in Python is on Python's side.

The steps for interfacing Python with C using 
`Ctypes <https://docs.python.org/3.6/library/ctypes.html>`_. are:

#. write C code functions
#. compile the C code as a shared library
#. write some Python lines of code to "extract" the C functions from the library
#. run!

----------
Our C code
----------

As an example of C function, we write a simple function that takes as input
an array of double and return the square. It is evident that such a simple function
(that calculates the square of an array) does not justify the use of C, but it is a good place
to start.

In a new text file, write the code below and save it as ``basic_function.c`` in the folder
``theories/`` for example:

.. code-block:: c

    #include <stdlib.h>

    void c_square(int n, double *array_in, double *array_out)
    { //return the square of array_in of length n in array_out
        int i;

        for (i = 0; i < n; i++)
        {
            array_out[i] = array_in[i] * array_in[i];
        }
    }

---------------------------------
Compile the C code into a library
---------------------------------

First, make sure you have a C compiler installed on you machine.
Mac and Linux machines usually have a C compiler installed by default.
On Windows, we suggest to install `MinGW <https://anaconda.org/anaconda/mingw>`_
via Anaconda.

To compile the above C function into a library that can later be used by Python,
open a terminal and change the working directory to the folder where ``basic_function.c``
is located. Then compile the library.


.. warning::
    This new library can only be used by the same type of machine is was 
    compiled on, i.e., a Windows machine creates libraries that cannot be
    used on Linux or Mac, and vice versa.
    To avoid problem, we name these library differently: we append to the 
    library name
    
    - ``_win32`` for Windows,
    - ``_darwin`` for Max,
    - ``_linux`` for Linux.

Compile the C file using either

.. code-block:: bash

    $ gcc -o basic_function_win32.so -shared -fPIC -O2 basic_function.c # Windows

    $ gcc -o basic_function_darwin.so -shared -fPIC -O2 basic_function.c # Mac
    
    $ gcc -o basic_function_linux.so -shared -fPIC -O2 basic_function.c # Linux

This created a new file ``basic_function_***.so`` containing our C function in the RepTate
folder ``theories/``. 

-------------------------
Use a C library in Python
-------------------------

Read the C library
------------------

We use the ``basic_function.so`` library via 
`Ctypes <https://docs.python.org/3.6/library/ctypes.html>`_.
In a new file, write the following and save it as, for example,
``basic_function_helper.py``

.. code-block:: python
    :lineno-start: 1
    
    """
    Define the C-variables and functions from the C-files that are needed in Python
    """
    from ctypes import c_double, c_int, CDLL
    import sys

    lib_path = 'theories/basic_function_%s.so' % (sys.platform)
    try:
        basic_function_lib = CDLL(lib_path)
    except:
        print('OS %s not recognized' % (sys.platform))

    python_c_square = basic_function_lib.c_square
    python_c_square.restype = None


Some explainations: 
::

    from ctypes import c_double, c_int, CDLL

imports the Python Ctypes object we will be needing.

::

    lib_path = 'theories/basic_function_%s.so' % (sys.platform)

defines the path of our library file, and ``sys.platform`` returns either 
``win32``, ``darwin`` or ``linux``. Note that the path is relative to the path of 
``RepTate.py`` or ``RepTateCL.py``.

::

    basic_function_lib = CDLL(lib_path)

defines the Python object ``square_lib`` where all the functions and variables 
from our C file ``basic_function.c`` are stored. In particular, the function 
``c_square``

::

    python_c_square = basic_function_lib.c_square

defines the Python equivalent of the C function ``c_square``. We name it 
``python_c_square`` for clarity, but using the same name is acceptable.

::

    python_c_square.restype = None

defines what type of variables the C function returns. 
In our case, it is ``void``, which translates in Python to ``None``.
See `fundamental-data-types 
<https://docs.python.org/3.6/library/ctypes.html#fundamental-data-types>`_ for 
a list of equivalence.


Use library functions
---------------------

Our C function ``c_square`` accepts three arguments: an ``int`` and two
``double *``. Hence, our Python function ``python_c_square`` accepts three 
arguments too but they must by of type ``c_int`` and "array of c_double" 
defined by the ``ctypes`` Python library.

Therefore, to use ``python_c_square``, we have to convert Python integer into
``c_int`` type and Python list into an "array of c_double".

The best way to do so is to write a Python function, in the file 
``basic_function_helper.py``

.. code-block:: python
    :lineno-start: 16
    
    def do_square_using_c(list_in):
        """Call C function to calculate squares"""
        n = len(list_in)
        c_arr_in = (c_double * n)(*list_in)
        c_arr_out = (c_double * n)()

        python_c_square(c_int(n), c_arr_in, c_arr_out)
        return c_arr_out[:]

In details::

    c_arr_in = (c_double * n)(*list_in)
    c_arr_out = (c_double * n)()

defines two ``ctypes`` arrays of ``double`` of size ``n``
that can be used by the C function. The first one is initialised with the values of ``list_in``.
It is equivalent to::

    for i in range(n):
        c_arr_in[i] = c_double(list_in[i])

This line::

    python_c_square(c_int(n), c_arr_in, c_arr_out)

calls the C function that does the computation of the square of ``c_arr_in``
and put the result in ``c_arr_out``. Note the conversion ``c_int(n)`` that 
transforms the Python integer into a ``ctypes`` ``int``.

This line::

    return c_arr_out[:]

returns a copy of the results as a Python list.

--------------
Final comments
--------------

Our C function ``c_square`` is now wrapped into a Python function
``do_square_using_c``. To use it in a RepTate module, simply import the 
function by including in the module header.

As an example, the following calculates the square of numbers from 0 to 999::

    from basic_function_helper import do_square_using_c
    ...
    my_list = np.arange(1000)
    squared_list = do_square_using_c(*my_list)

------------------------
Bonus: Callback function
------------------------

We presented above a method to have Python "request something from C", that is,
Python calls a C function and gets an answer. In the previous example, Python requested
C to calculate the square of an array.
Sometimes, it is convenient to do the other way around too. For instance, if the array
is "big", the C function might take some time to finish the calculations, and we may want
to inform Python of the advancement of the computations.

We propose here to modify the above code to include a *callback* function that lets 
the C code call a Python function.
As a simple example, the C code will request Python to print the advancement of the
calculations of the "square" function, previously introduced.
It require more steps than what we have seen before, but it is reasonably simple.

The C function will call a Python function with a ``double`` argument (the advancement in percent)
and Python will return the percentage incremented by 20%.

Modify the C code
-----------------

We need to define:

- A proxy function that will be used to call the corresponding Python function
- A function that Python will initially call to define the proxy function.
    This is similar to what we have done so far.
- A function *type* that defines how the proxy function "look" like, i.e.
    arguments and return types (``int``, ``double``, etc.)

Somewhere before the ``c_square`` function definition, we write:

.. code-block:: c

    typedef double give_and_take_double(double p); // type definition
    give_and_take_double *tell_python;             // pointer to a function of type "give_and_take_double"
    void def_python_callback(give_and_take_double *func)
    {
        // Function called by Python once
        // Defines what "tell_python" is pointing to
        tell_python = func;
    }

The first line defines a new type: a function that takes a single ``double`` as argument and returns a ``double``.
This allows us to define the second line: a pointer to a function of type ``give_and_take_double``.
At this point we do not know that the function will be, but we know it accepts a ``double`` as argument, and 
it returns a ``double``. The last lines consist of the function that Python will have to call to actually define what ``tell_python`` is, 
or rather, define towards what it is pointing to.


Now we can decorate our ``c_square`` function with the ``tell_python`` function:

.. code-block:: c


    void c_square(int n, double *array_in, double *array_out)
    { //return the square of array_in of length n in array_out
        int i;
        double percent = 0.2;
        for (i = 0; i < n; i++)
        {
            if ((double)i / n > percent)
            {
                percent = tell_python(percent);
            }
            array_out[i] = array_in[i] * array_in[i];
        }
    }

That is all we need to do on the C side. 

.. warning::
    Do not forget to recompile the shared library every time you modify the C code.


Modify the Python code
----------------------

Last steps, we need to modify the Python code. 
We make some addition to the file "basic_function_helper.py".
We need to:

- Define a "classic" Python function 
- Define a C callback function that translates that Python function
- Call the C function ``def_python_callback``, defined above to setup the callback function

We add to the bottom of the file "basic_function_helper.py":

.. code-block:: python

    # Callback stuff
    from ctypes import CFUNCTYPE, POINTER

    def get_percent(percent):
        """Print advancement and set the next call when C has advanced a further 20%"""
        self.Qprint("Advancement of C calculations: %f%%" % (percent*100))
        return percent + 0.2

    CB_FTYPE_DOUBLE_DOUBLE = CFUNCTYPE(c_double, c_double) # define C pointer to a function type
    cb_get_percent = CB_FTYPE_DOUBLE_DOUBLE(get_percent) # define a C function equivalent to the python function "get_percent"
    basic_function_lib.def_python_callback(cb_get_percent)  # the the C code about that C function

In these lines::

    def get_percent(percent):
        ...

we define a "classic" Python function that take a ``float`` as argument, and return a ``float``.
It prints the information in the theory text box of RepTate via the Qprint method.

Then, in the line::

    CB_FTYPE_DOUBLE_DOUBLE = CFUNCTYPE(c_double, POINTER(c_double))

the first argument of the ctypes function ``CFUNCTYPE`` defines the return types (here ``double``) and the other arguments
are the function arguments (here only one ``double``). ``CFUNCTYPE`` returns a pointer to a C functions::

The following line defines a C function of type ``CB_FTYPE_DOUBLE_DOUBLE``, which is a proxy for the Python
function ``get_percent``::

    cb_get_percent = CB_FTYPE_DOUBLE_DOUBLE(get_percent)

Then we tell our C code which is our callback function::

    basic_function_lib.def_python_callback(cb_get_percent)


Usage
-----

Now we can calculate the square of a "big" list and follow the advancement of the computations in the theory text box.