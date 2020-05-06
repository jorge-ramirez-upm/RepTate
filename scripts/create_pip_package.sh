#!/bin/bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install tqdm
python -m pip install --user --upgrade twine

# remove old stuff
rm -rf *.egg-info

# compile package
python setup.py bdist_wheel

#upload to PyPi
python -m twine upload dist/*.whl