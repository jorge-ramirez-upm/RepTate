import importlib.util
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "build_native_libraries.py"
SPEC = importlib.util.spec_from_file_location("build_native_libraries", SCRIPT)
assert SPEC and SPEC.loader
build_native_libraries = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = build_native_libraries
SPEC.loader.exec_module(build_native_libraries)


def test_platform_detection():
    assert build_native_libraries.detect_platform("darwin") == "darwin"
    assert build_native_libraries.detect_platform("linux") == "linux"
    assert build_native_libraries.detect_platform("win32") == "windows"


def test_inventory_and_outputs():
    names = {library.name for library in build_native_libraries.NATIVE_LIBRARIES}
    outputs = {library.output_name for library in build_native_libraries.NATIVE_LIBRARIES}
    assert names == {"bob", "dtd", "kww", "landscape", "react", "rouse", "rp_blend", "sccr", "schwarzl"}
    assert "bob2p5_lib_darwin.so" in outputs
    assert len(outputs) == len(names)


def test_command_construction():
    library = next(item for item in build_native_libraries.NATIVE_LIBRARIES if item.name == "rouse")
    assert build_native_libraries.direct_command(library) == [
        "cc", "-dynamiclib", "-fPIC", "-O2", "rouse.c", "-o", "../rouse_lib_darwin.so"
    ]
    landscape = next(item for item in build_native_libraries.NATIVE_LIBRARIES if item.name == "landscape")
    assert "-I./" in build_native_libraries.direct_command(landscape)


def test_architecture_parsing():
    assert build_native_libraries.parse_architectures("arm64\n") == ("arm64",)
    assert build_native_libraries.parse_architectures("arm64 x86_64\n") == ("arm64", "x86_64")
