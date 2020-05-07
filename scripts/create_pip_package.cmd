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