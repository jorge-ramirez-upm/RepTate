import os
from importlib import import_module
from pathlib import Path
from typing import Any

from setuptools import Extension, setup

try:
    pybind11: Any = import_module("pybind11")
except ImportError as exc:
    raise SystemExit(
        "pybind11 is required to build RepTate.theories._lp2r. "
        "Install it with `python -m pip install pybind11`."
    ) from exc


ROOT = Path(__file__).resolve().parent
LP2R_DIR = ROOT / "RepTate" / "theories" / "modified_LP2R1.1"
LP2R_PYBIND_DIR = LP2R_DIR / "pybind"

lp2r_extension = Extension(
    "RepTate.theories._lp2r",
    sources=[
        str(LP2R_PYBIND_DIR / "lp2r_bindings.cpp"),
        str(LP2R_PYBIND_DIR / "lp2r_solver.cpp"),
        str(LP2R_PYBIND_DIR / "kww_adapter.cpp"),
        str(LP2R_PYBIND_DIR / "kww_cpp.cpp"),
    ],
    include_dirs=[
        pybind11.get_include(),
        str(LP2R_PYBIND_DIR),
    ],
    language="c++",
    extra_compile_args=["/std:c++17"] if os.name == "nt" else ["-std=c++17"],
)


setup(ext_modules=[lp2r_extension])
