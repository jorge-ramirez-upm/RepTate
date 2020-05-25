#!/bin/bash
# source: https://dzone.com/articles/executable-package-pip-install
# Create pypirc: The Pypirc file stores the PyPi repository information. Create a file in the home directory
# for Windows :  C:\Users\UserName\.pypirc 
# for *nix :   ~/.pypirc 
# And add the following content to it. Replace USERNAME with your username.
#   [distutils] 
#   index-servers=pypi
#   [pypi] 
#   repository = https://upload.pypi.org/legacy/ 
#   username = USERNAME

python -m pip install --upgrade pip setuptools wheel
python -m pip install tqdm
python -m pip install --user --upgrade twine

# remove old stuff
rm -rf *.egg-info

# compile package
python setup.py bdist_wheel

#upload to PyPi
python -m twine upload dist/*.whl