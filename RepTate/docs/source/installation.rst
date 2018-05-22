============
Installation
============

RepTate can be installed in two ways: 

    #. the "shortcut", allows you to run RepTate in a couple of clicks;
    #. the "scenic route", requires more steps and the use of the command-line interface. 

.. note::
    RepTate is continuously updated by the developers. Option-2 will get you the latest version, 
    while Option-1 is a "snapshot" in time of the software. 

.. hint::
    Ultimately, the "scenic route" is faster than the "shortcut":
    To update your version of RepTate in the future, the "scenic route" offers
    the powerful ``git pull`` command.

The "shortcut"
==============

Binary packages (containing all the needed files and libraries, 
as well as a Python interpreter), for the latest version (|release|) can be downloaded here: 

`RepTate for Windows (Windows 7 64-bit or later) <https://upm365-my.sharepoint.com/:u:/g/personal/jorge_ramirez_upm_es/EVPmrLpqiwJJgYJVCjlVHmYB_huq8_D9UtHIcZc-zDC6aw?download=1>`_
    Unzip and uncompress the dowloaded file and look for the RepTate executable ``RepTate.exe``.

`RepTate for Mac (OS X 10.10 or later) <https://upm365-my.sharepoint.com/:u:/g/personal/jorge_ramirez_upm_es/EZrT61uCzZdKsXRe167rwrkB519j1aSaAcRh8cGb4_zrMw?download=1>`_ 
    Drag-and-drop the RepTate application in your Applications folder. 
    
Linux users are supposed to follow the instruction below.

Previous versions of the code can be downloaded from the following `folder 
<https://upm365-my.sharepoint.com/:f:/g/personal/jorge_ramirez_upm_es/EmVwGD9TFo1BhgRlBahS3NwB98txob9v_e3CUJSVYITKYg?e=9QB5vz>`_.

The "scenic route"
==================

This option will take you through the installation of Python 3, RepTate dependancies, 
and the "cloning" of RepTate's repository.

Executive summary
-----------------

#. Install Python 3.6 or later via `Minconda <https://conda.io/miniconda.html>`_ (or your favourite method)
#. Install RepTate's package dependencies (pyqt, matplotlib, scipy, (py)readline, openpyxl) via ``conda install <package>``
#. Install Git (version control system)  via ``conda install git``
#. Clone RepTate's repository via ``git clone https://github.com/jorge-ramirez-upm/RepTate.git``
#. Try launching RepTate application: ``cd RepTate`` then again ``cd RepTate`` then ``python RepTate.py``
#. From time to time, check for updates via ``git pull``

Should anything go wrong, please read the detailed explanations below. 

Detailed explanations
----------------------

Install Python 3
~~~~~~~~~~~~~~~~

To install Python 3, you can either install `Minconda <https://conda.io/miniconda.html>`_ (requires 300 MB of disk space)
or install the full `Anaconda <https://www.anaconda.com/download/>`_ Python (requires 3 GB of disk space). Note that depending on your
operating system, other methods, not covered here, are available.

We recommend you to install the former, `Minconda <https://conda.io/miniconda.html>`_, that contains Python only (and a small number of useful packages) and to 
install "manually" the extra packages that RepTate needs, as explained below.  
The latter contains Python and 100+ automatically installed open source scientific 
packages and their dependencies, not *all* used by RepTate.
In either case you want to install **Python 3.6 or a later version** (not Python 2!). 

Once the installation is completed, open the command line interface "Anaconda prompt" (or equivalent). 
On Windows, this is usually found by clicking the Windows button and looking under 
"All Programmes -> Anaconda3".
Verify that Python 3 has been correctly installed by typing in the command line interface::

    python --version

It should print something like ``Python 3.x.x``. If it prints something 
like ``Python 2.x.x`` instead, then try::

    python3 --version

and if that print something like ``Python 3.x.x``, you will need to add the "3" 
at the end of ``python`` every time you see it in the "Anaconda prompt".


Install extra packages 
~~~~~~~~~~~~~~~~~~~~~~

You need to install some extra packages to be able to run RepTate. 
Open an "Anaconda prompt" (or equivalent). On Windows, this is found by clicking the Windows 
button and looking under All Programmes -> anaconda3.
This will open up a window where you can type commands to install the extra packages::

    conda install pyqt 
    conda install matplotlib 
    conda install scipy
    conda install openpyxl

Additionally, on Windows::
    
    conda install pyreadline

On  Mac or Linux::

    conda install readline

If a package is missing and you try to run RepTate, Python will print an 
information message in the terminal telling you what went missing. 
For example, something like::

    ModuleNotFoundError: No module named 'openpyxl'

tells you that you need to install the ``openpyxl`` package.


Install Git
~~~~~~~~~~~

Git is a free and open source distributed version control system. We use it 
for the development of RepTate. To install Git, do::

    conda install git

"Clone" RepTate repository
~~~~~~~~~~~~~~~~~~~~~~~~~~

RepTate developers keep track of the changes they make to the RepTate project 
using git as a version control system. 
When a developer make a change or bug-fix to RepTate, it is uploaded to an online
repository, hosted by GitHub.
The source code of RepTate is open access (see RepTate's Licence) and can be found
`here <https://github.com/jorge-ramirez-upm/RepTate>`_.
To download the full repository to your computer, type in the command line interface::

    git clone https://github.com/jorge-ramirez-upm/RepTate.git

This will create a new folder called ``RepTate`` by default.

.. Alternatively, download the zip package containing the RepTate source code and uncompress it.    
.. After that, it should be possible to run RepTate in the RepTate folder with the command::

Launch RepTate
~~~~~~~~~~~~~~

To launch RepTate, you should change the current working directory of the
command line interface to ``RepTate/RepTate/``. Type::

    cd RepTate
    cd RepTate
    python RepTate.py

Wait a little, and RepTate should appear on your screen!

Take a moment to read the `User Manual <http://reptate.readthedocs.io/en/latest/manual/manual.html>`_.

Update RepTate
~~~~~~~~~~~~~~

If you successfully went through this tutorial, you have the latest version of RepTate.
However, from time to time, you can check for additions or bug-fix uploaded by RepTate's developers.
While you are in the ``RepTate`` folder (say ``RepTate/RepTate/``), type::

    git pull

If there is no update available, it will print someting like ``Already up to date.``, otherwise you will the full list of changes printed on your screen.

Once this is done, you can launch RepTate as usual.

.. note::
    If anything go wrong during the installation, please contact the developers 
    using the contact details given on the `documentation's main page <http://reptate.readthedocs.io>`_.
