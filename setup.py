import os
from setuptools import setup, find_packages
import sys

sys.path.append('RepTate/core')

import Version

base_dir = os.path.dirname(os.path.abspath(__file__))
requirements_file = open(os.path.join(base_dir, 'requirements.txt'))
requirements = requirements_file.read().splitlines()

setup(
    name="RepTate",
	version=Version.VERSION,
    description="Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiment",
    author="Jorge Ramirez <jorge.ramirez@upm.es>, Victor Boudara <V.A.Boudara@leeds.ac.uk>",
    author_email="jorge.ramirez@upm.es",
	url='http://github.com/jorge-ramirez-upm/RepTate',
	packages=find_packages(),
    package_data={'': ['*.ui', '*.qrc', '*.npy', '*.so']},
	install_requires=requirements,
	entry_points={
        'console_scripts': [
            'RepTate = RepTate.RepTate:main',
            'RepTateCL = RepTate.RepTateCL:main'
        ]
    },
	license='GPL License',
	classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
		'Topic :: Scientific/Engineering',
		'Intended Audience :: Science/Research'
    ]
)
