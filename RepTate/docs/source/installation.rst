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

    
    
    
