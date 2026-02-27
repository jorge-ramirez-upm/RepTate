============
Installation
============

RepTate can be installed in three ways: 

    #. the "shortcut", allows you to run RepTate in a couple of clicks, but only provides access to the latest stable release of RepTate.;
    #. the "scenic route", requires more steps and the use of the command-line interface. 

.. note::
    RepTate is frequenty updated by the developers and contributors . Option-2 will get you the latest version, while Option 1 provides a well tested "snapshot" of the software. 

.. hint::
    Ultimately, the "scenic route" is faster than the "shortcut":
    To update your version of RepTate in the future, the "scenic route" offers
    the powerful ``git pull`` command.

The "shortcut"
==============

Binary packages (containing all the needed files and libraries), for the latest version (|release|) can be downloaded from the **Releases** section of the RepTate GitHub repository: `here <https://github.com/jorge-ramirez-upm/RepTate/releases>`_. Unzip the downloaded file and look for the RepTate executable.

Previous versions of the binary packages can be downloaded from the following `folder 
<https://upm365-my.sharepoint.com/:f:/g/personal/jorge_ramirez_upm_es/EmVwGD9TFo1BhgRlBahS3NwB98txob9v_e3CUJSVYITKYg?e=9QB5vz>`_.

The "scenic route"
==================

This option will take you through the installation of Python 3.11, RepTate dependencies, 
and the "cloning" of RepTate's repository.

Executive summary
-----------------

#. Install Python 3.11. 
#. Install Git (version control system)  via ``conda install git`` (or a native implementation of git for your operating system).
#. Clone RepTate's repository via ``git clone https://github.com/jorge-ramirez-upm/RepTate.git``
#. Install RepTate's package dependencies (pyqt, matplotlib, scipy, (py)readline, openpyxl, xlrd, psutil) via ``conda install <package>`` (or via ``pip install <package>`` if you are using a different Python distribution). Alternatively, you can go to the RepTate code tree and run ``pip install -r requirements.txt``. This will take care of installing all the packages that RepTate needs.
#. Compile the user interface resources via ``python scripts/build_ui.py`` (or ``python3 scripts/build_ui.py`` depending on your system).
#. Try launching RepTate application: ``cd RepTate`` then again ``cd RepTate`` then ``python RepTate.py``
#. From time to time, check for updates via ``git pull``

Should anything go wrong, please read the detailed explanations below. 

Detailed explanations
----------------------

Install Python 3.11
~~~~~~~~~~~~~~~~~~~

To install Python 3.11, you can either install `Minconda <https://conda.io/miniconda.html>`_ (requires 300 MB of disk space)
or install the full `Anaconda <https://www.anaconda.com/download/>`_ Python (requires 3 GB of disk space). Note that depending on your
operating system, other methods, not covered here, are available. Another convenient distribution for Windows is `WinPython <https://winpython.github.io/>`_. WinPython can be installed locally in a folder and does not modify the Windows system in any way. 

We recommend you to install the former, `Minconda <https://conda.io/miniconda.html>`_, that contains Python only (and a small number of useful packages) and to 
install "manually" the extra packages that RepTate needs, as explained below.  
The latter contains Python and 100+ automatically installed open source scientific 
packages and their dependencies, not *all* used by RepTate.
In either case you want to install **Python 3.11** (the code may not work properly in other versions of Python). 

Once the installation is completed, open the command line interface "Anaconda prompt" (or equivalent). 
On Windows, this is usually found by clicking the Windows button and looking under 
"All Programmes -> Anaconda3".
Verify that Python 3 has been correctly installed by typing in the command line interface::

    python --version

It should print something like ``Python 3.11.x``. If it prints an error message or something 
like ``Python 2.x.x``, then try::

    python3 --version

If it prints something like ``Python 3.11.x``, you will need to add the "3" 
at the end of ``python`` every time you see it used in this tutorial.


Install extra packages 
~~~~~~~~~~~~~~~~~~~~~~

You need to install some extra packages to be able to run RepTate. 
Open an "Anaconda prompt" (or equivalent). On Windows, this is found by clicking the Windows 
button and looking under All Programmes -> anaconda3.
This will open up a window where you can type commands to install the extra packages::

    conda install PySide6
    conda install matplotlib 
    conda install scipy
    conda install openpyxl
	conda install xlrd

Alternatively, you can change into the RepTate code folder and run ``pip install -r requirements.txt``. The file ``requirements.txt`` contains a list of all the python packages and libraries that RepTate needs in order to run properly.

If a package is missing and you try to run RepTate, Python will print an 
information message in the terminal telling you what went missing. 
For example, something like::

    ModuleNotFoundError: No module named 'openpyxl'

tells you that you need to install the ``openpyxl`` package. Note that, in other Python distributions, the standard command to install packages is ``pip``. 

Incompatibility with other Python packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some users have reported incompatibility between RepTate and other popular packages, such as Spyder. In that case, we recommend to create a separate Python environment to run RepTate. In miniconda, this can be achieved by following the instructions below:

#. Create a Python environnement. In the Anaconda prompt::

	conda create --name Env_Reptate

#. Connection to the environnement::

	conda activate Env_Reptate

#. Install pip::

	conda install pip

#. Install Reptate::

	pip install RepTate

#. Launch Reptate::

	python -m RepTate

#. In this environnement, if Spyder is no longer working we can launch it from the basis environnemet or windows cmd::

	conda deactivate
	spyder

Install Git
~~~~~~~~~~~

Git is a free and open source distributed version control system. We use it 
for the development of RepTate. To install Git, do::

    conda install git

Alternatively, you can install a binary implementation of Git for your Operating System.

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

Compile the user interface resources via ``python scripts/build_ui.py`` (or ``python3 scripts/build_ui.py`` depending on your system).   

Launch RepTate
~~~~~~~~~~~~~~

To launch RepTate, you should change the current working directory of the
command line interface to ``RepTate/``. Type::

	cd RepTate
	python -m RepTate

Wait a little and RepTate should appear on your screen. Note that you may need to use 
``python3 -m RepTate`` depending on your system.

Take a moment to read the `User Manual <http://reptate.readthedocs.io/manual/manual.html>`_.

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
