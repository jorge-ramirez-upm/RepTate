============
Installation
============

RepTate can be installed in two ways: 

    #. the "shortcut", which will allow you to run RepTate in a couple of clicks;
    #. the "scenic route", which require more steps and the use of the command-line interface. 

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
as well as a Python interpreter), can be downloaded here:

`RepTate v0.9.1 for Windows (Windows 7 64-bit or later) <https://upm365-my.sharepoint.com/:u:/g/personal/jorge_ramirez_upm_es/EWV3803YS2NOuD5oRae3y9YBYEQqSUNkgZr_A4JMFDHElA?download=1>`_
    Download size: 305 MB. 
    Unzip the dowloaded file and look for the RepTate executable ``RepTate.exe``.

`RepTate v0.9.1 for Mac (OS X 10.10 or later) <https://upm365-my.sharepoint.com/:u:/g/personal/jorge_ramirez_upm_es/EQV6JjH4p7ZMn-TOvQ8ze8ABR-9vXRGT1QtektModMbGmg?download=1>`_ 
    Download size: 82 MB.
    Drag-and-drop the RepTate application in your Application folder. 

Linux users are supposed to follow the instruction below.

The "scenic route"
==================

This option will take you through the installation of Python 3, RepTate dependancies, 
and the "cloning" of RepTate's repository.

Install Python 3 in your computer. Any 64-bit distribution is fine. We recommend `miniconda 
<https://conda.io/miniconda.html>`_.

Windows
-------

After installing miniconda with Python 3.6, 64-bit, open a terminal and run::

    > conda install pyqt 
    > conda install matplotlib 
    > conda install scipy
    > conda install pyreadline
    > conda install openpyxl

If necessary, install the git CVS system. Then, clone the RepTate source code distribution 
from `GitHub website <https://github.com/jorge-ramirez-upm/RepTate>`_::

    > git clone https://github.com/jorge-ramirez-upm/RepTate.git

Alternatively, download the zip package containing the RepTate source code and uncompress it.    
After that, it should be possible to run RepTate in the RepTate folder with the command::

    > python RepTate.py

Linux
-----

After installing miniconda with Python 3.6, 64-bit, open a terminal and run::

    > conda install pyqt 
    > conda install matplotlib 
    > conda install scipy
    > conda install openpyxl

If necessary, install the git CVS system. Then, clone the RepTate source code distribution 
from `GitHub website <https://github.com/jorge-ramirez-upm/RepTate>`_::

    > git clone https://github.com/jorge-ramirez-upm/RepTate.git

Alternatively, download the zip package containing the RepTate source code and uncompress it.    
After that, it should be possible to run RepTate in the RepTate folder with the command::

    > python RepTate.py
    
Mac
---

After installing miniconda with Python 3.6, 64-bit, open a terminal and run::
    
    > conda install pyqt 
    > conda install matplotlib 
    > conda install scipy
    > conda install openpyxl
    
Install MacOS developer tools (in order to use git). Then, from a terminal, clone the 
RepTate source code distribution from `GitHub website <https://github.com/jorge-ramirez-upm/RepTate>`_::

    > git clone https://github.com/jorge-ramirez-upm/RepTate.git

Alternatively, download the zip package containing the RepTate source code and uncompress it. 
After that, it should be possible to run RepTate in the RepTate folder with the command::

    > python RepTate.py

    
    
    