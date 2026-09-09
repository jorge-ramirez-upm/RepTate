import importlib.util
import struct
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
    outputs = {library.output_name(platform) for library in build_native_libraries.NATIVE_LIBRARIES for platform in ("darwin", "linux", "windows")}
    assert names == {"bob", "dtd", "kww", "landscape", "react", "rouse", "rp_blend", "sccr", "schwarzl"}
    assert "bob2p5_lib_darwin.so" in outputs
    assert "bob2p5_lib_linux.so" in outputs
    assert "bob2p5_lib_win32.so" in outputs
    assert len(outputs) == len(names) * 3


def test_command_construction():
    library = next(item for item in build_native_libraries.NATIVE_LIBRARIES if item.name == "rouse")
    assert build_native_libraries.direct_command(library, "darwin") == [
        "cc", "-dynamiclib", "-fPIC", "-O2", "rouse.c", "-o", "../rouse_lib_darwin.so"
    ]
    assert build_native_libraries.direct_command(library, "linux") == [
        "cc", "-shared", "-fPIC", "-O2", "rouse.c", "-o", "../rouse_lib_linux.so"
    ]
    assert build_native_libraries.direct_command(library, "windows") == [
        "gcc", "-shared", "-fPIC", "-O2", "-static-libgcc", "rouse.c", "-o", "../rouse_lib_win32.so"
    ]
    landscape = next(item for item in build_native_libraries.NATIVE_LIBRARIES if item.name == "landscape")
    assert "-I./" in build_native_libraries.direct_command(landscape)


def test_architecture_parsing():
    assert build_native_libraries.parse_architectures("arm64\n") == ("arm64",)
    assert build_native_libraries.parse_architectures("arm64 x86_64\n") == ("arm64", "x86_64")
    assert build_native_libraries.expected_architecture("windows", "AMD64") == "x86_64"


def test_platform_output_resolution():
    library = next(item for item in build_native_libraries.NATIVE_LIBRARIES if item.name == "landscape")
    assert library.output_name("darwin") == "landscape_darwin.so"
    assert library.output_name("linux") == "landscape_linux.so"
    assert library.output_name("windows") == "landscape_win32.so"


def test_special_case_dispatch():
    bob = next(item for item in build_native_libraries.NATIVE_LIBRARIES if item.name == "bob")
    assert bob.special_build == "bob_makefile"


def test_windows_pe_architecture(tmp_path):
    binary = bytearray(70)
    binary[:2] = b"MZ"
    struct.pack_into("<I", binary, 0x3C, 64)
    binary[64:68] = b"PE\0\0"
    struct.pack_into("<H", binary, 68, 0x8664)
    path = tmp_path / "native_win32.so"
    path.write_bytes(binary)
    library = build_native_libraries.NATIVE_LIBRARIES[0]
    assert build_native_libraries._windows_pe_machine(path, library) == 0x8664
