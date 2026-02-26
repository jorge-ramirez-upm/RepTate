import os
from setuptools import setup, find_packages

# import versioneer
import functools
import glob

base_dir = os.path.dirname(os.path.abspath(__file__))
requirements_file = open(os.path.join(base_dir, "requirements.txt"))
requirements = requirements_file.read().splitlines()


def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    data_file_tree = {}

    def build_tree(dic, dir_tree):
        for key in dic:
            if dic[key] is not None:
                if dir_tree != "":
                    dir = build_tree(dic[key], dir_tree + os.sep + key)
                else:
                    dir = build_tree(dic[key], key)
            else:
                data_file_tree[dir_tree + os.sep] = glob.glob(dir_tree + os.sep + "*.*")
        return [(k, data_file_tree[k]) for k in data_file_tree]

    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = functools.reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir

    return build_tree(dir, "")


list_data_files = get_directory_structure("data")
list_doc_files = get_directory_structure("docs")


with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="RepTate",
    # version=versioneer.get_version(),
    # cmdclass=versioneer.get_cmdclass(),
    description="Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiment",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Jorge Ramirez, Victor Boudara",
    author_email="reptate.rheology@gmail.com",
    url="http://github.com/jorge-ramirez-upm/RepTate",
    packages=find_packages(),
    package_data={"": ["*.ui", "*.qrc", "*.npy", "*.so", "*.npz"]},
    data_files=list_data_files,
    install_requires=requirements,
    entry_points={
        "gui_scripts": [
            "RepTate = RepTate.__main__:main",
            "MatDB = RepTate.MatDB:main",
            "UV = RepTate.UV:main",
        ],
    },
    license="GNU General Public License v3 or later (GPLv3+)",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
    ],
)
