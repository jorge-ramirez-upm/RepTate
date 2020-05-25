REM source: https://dzone.com/articles/executable-package-pip-install
REM Create pypirc: The Pypirc file stores the PyPi repository information. Create a file in the home directory
REM for Windows :  C:\Users\UserName\.pypirc 
REM for *nix :   ~/.pypirc 
REM And add the following content to it. Replace USERNAME with your username.
REM   [distutils] 
REM   index-servers=pypi
REM   [pypi] 
REM   repository = https://upload.pypi.org/legacy/ 
REM   username = USERNAME

REM install needed packages first
python -m pip install --upgrade pip setuptools wheel
python -m pip install tqdm
python -m pip install --user --upgrade twine

REM remove old stuff
rmdir /Q/S RepTate_test.egg-info

REM compile package
python setup.py bdist_wheel

REM upload to PyPi
python -m twine upload dist/*.whl

REM Create conda stuff (to be done...)
REM conda install conda-build
REM conda update conda
REM conda update conda-build
REM conda skeleton pypi click
