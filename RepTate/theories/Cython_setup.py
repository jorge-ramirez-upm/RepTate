#Setup file for Cython: pre-compile functions
#py Cython_setup.py build_ext --inplace
from distutils.core import setup
from Cython.Build import cythonize

setup(
	ext_modules = cythonize(["scilength.pyx", "brlength.pyx", "request_arm.pyx"])
)
