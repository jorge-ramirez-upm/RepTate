"""Build RepTate-owned native theory libraries.

The Darwin path is used by the release workflow and is also useful for source
developers. Linux and Windows entries are intentionally not activated yet.
"""

from __future__ import annotations

import argparse
import os
import platform as platform_module
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class NativeLibrary:
    name: str
    source_dir: str
    source_files: tuple[str, ...]
    output_name: str
    special_build: str | None = None
    include_current_directory: bool = False

    def source_path(self, theories_dir: Path) -> Path:
        return theories_dir / self.source_dir

    def output_path(self, theories_dir: Path) -> Path:
        return theories_dir / self.output_name


_LANDSCAPE_SOURCES = (
    "brent.c", "c_math.c", "convergence.c", "error.c", "fdfsolver.c",
    "fdiv.c", "fsolver.c", "infnan.c", "landscape.c", "newton.c",
    "pow_int.c", "stream.c",
)

NATIVE_LIBRARIES = (
    NativeLibrary("dtd", "dtd_source_c_code", ("dtd.c", "trapz.c", "qtrap.c"), "dtd_lib_darwin.so"),
    NativeLibrary("kww", "kww_source_c_code", ("kww.c",), "kww_lib_darwin.so"),
    NativeLibrary("landscape", "BuildLandscape_Linux", _LANDSCAPE_SOURCES, "landscape_darwin.so", include_current_directory=True),
    NativeLibrary(
        "react", "react_source_c_code",
        ("binsandbob.c", "polybits.c", "polycleanup.c", "polymassrg.c", "ran3.c", "tobitabatch.c", "tobitaCSTR.c", "multimetCSTR.c", "dieneCSTR.c", "calc_architecture.c"),
        "react_lib_darwin.so",
    ),
    NativeLibrary("rouse", "rouse_source_c_code", ("rouse.c",), "rouse_lib_darwin.so"),
    NativeLibrary("rp_blend", "rp_blend_source_c_code", ("derivs_rolie_poly_blend.c",), "rp_blend_lib_darwin.so"),
    NativeLibrary("sccr", "sccr_source_c_code", ("sccr.c",), "sccr_lib_darwin.so"),
    NativeLibrary("schwarzl", "schwarzl_source_c_code", ("schwarzl.c",), "schwarzl_lib_darwin.so"),
    NativeLibrary("bob", "modified_bob2.5/code/src/obj", (), "bob2p5_lib_darwin.so", special_build="bob_makefile"),
)


class BuildError(RuntimeError):
    """An actionable native-library build or validation error."""


def detect_platform(sys_platform: str | None = None) -> str:
    """Return the repository's normalized platform identity."""
    value = sys_platform if sys_platform is not None else sys.platform
    if value == "darwin":
        return "darwin"
    if value.startswith("linux"):
        return "linux"
    if value.startswith("win"):
        return "windows"
    return value


def expected_architecture() -> str:
    value = platform_module.machine().lower()
    return {"amd64": "x86_64", "x86-64": "x86_64"}.get(value, value)


def parse_architectures(output: str) -> tuple[str, ...]:
    """Parse the whitespace-separated architecture list printed by lipo."""
    return tuple(part for part in output.split() if part)


def direct_command(library: NativeLibrary, compiler: str = "cc") -> list[str]:
    command = [compiler, "-dynamiclib", "-fPIC", "-O2", *library.source_files]
    if library.include_current_directory:
        command.extend(["-I./"])
    command.extend(["-o", f"../{library.output_name}"])
    return command


def _run(command: Sequence[str], cwd: Path, library: NativeLibrary, verbose: bool) -> None:
    if verbose:
        print("$", " ".join(command), f"(in {cwd})")
    try:
        subprocess.run(command, cwd=cwd, check=True)
    except FileNotFoundError as exc:
        raise BuildError(f"{library.name}: command not found: {command[0]} (source: {cwd})") from exc
    except subprocess.CalledProcessError as exc:
        raise BuildError(
            f"{library.name}: command failed with exit status {exc.returncode}: "
            f"{' '.join(command)} (source: {cwd})"
        ) from exc


def verify_architecture(path: Path, expected: str) -> None:
    try:
        result = subprocess.run(["lipo", "-archs", str(path)], check=True, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise BuildError(f"architecture check for {path.name}: lipo was not found") from exc
    except subprocess.CalledProcessError as exc:
        raise BuildError(f"architecture check for {path.name}: lipo failed with exit status {exc.returncode}") from exc
    architectures = parse_architectures(result.stdout)
    if architectures != (expected,):
        raise BuildError(f"architecture check for {path.name}: built {architectures or 'none'}, expected {expected}")
    print(f"Verified {path.name}: {expected}")


def _build_bob(library: NativeLibrary, theories_dir: Path, verbose: bool) -> None:
    source_dir = library.source_path(theories_dir)
    _run(["make", "-f", "makefile_for_lib", "clean"], source_dir, library, verbose)
    _run(["make", "-f", "makefile_for_lib"], source_dir, library, verbose)
    built = source_dir / "bob2p5_lib.so"
    if not built.is_file():
        raise BuildError(f"{library.name}: make completed but did not produce {built} (source: {source_dir})")
    shutil.copy2(built, library.output_path(theories_dir))


def build_library(library: NativeLibrary, theories_dir: Path, expected: str, verbose: bool) -> None:
    print(f"Building {library.name}...")
    if library.special_build == "bob_makefile":
        _build_bob(library, theories_dir, verbose)
    else:
        _run(direct_command(library), library.source_path(theories_dir), library, verbose)
    output = library.output_path(theories_dir)
    if not output.is_file():
        raise BuildError(f"{library.name}: expected output was not created: {output}")
    verify_architecture(output, expected)
    print(f"Built {output.name}")


def clean_outputs(theories_dir: Path) -> None:
    for library in NATIVE_LIBRARIES:
        output = library.output_path(theories_dir)
        if output.exists():
            output.unlink()
            print(f"Removed {output.name}")
    bob_dir = theories_dir / "modified_bob2.5/code/src/obj"
    bob_output = bob_dir / "bob2p5_lib.so"
    if bob_output.exists():
        bob_output.unlink()
        print(f"Removed {bob_output}")
    for object_file in bob_dir.glob("*.o"):
        object_file.unlink()
        print(f"Removed {object_file}")


def _parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description=__doc__)


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    parser.add_argument("--all", action="store_true", help="build all libraries for the current implemented platform")
    parser.add_argument("--library", choices=[library.name for library in NATIVE_LIBRARIES], help="build/check one library")
    parser.add_argument("--clean", action="store_true", help="remove Darwin outputs and Bob build products")
    parser.add_argument("--check", action="store_true", help="check existing Darwin outputs without rebuilding")
    parser.add_argument("--verbose", action="store_true", help="print compiler commands")
    args = parser.parse_args(argv)

    current_platform = detect_platform()
    if current_platform != "darwin":
        print(f"Platform: {current_platform}")
        print("Native-library builds for this platform are not implemented in this first pass.", file=sys.stderr)
        return 2

    theories_dir = Path(__file__).resolve().parents[1] / "RepTate" / "theories"
    target = os.environ.get("MACOSX_DEPLOYMENT_TARGET", "")
    print(f"Platform: macOS\nArchitecture: {expected_architecture()}\nMACOSX_DEPLOYMENT_TARGET: {target or '(not set)'}")
    selected = [library for library in NATIVE_LIBRARIES if args.library is None or library.name == args.library]
    if args.clean:
        clean_outputs(theories_dir)
        return 0
    expected = expected_architecture()
    if args.check:
        for library in selected:
            output = library.output_path(theories_dir)
            if not output.is_file():
                raise BuildError(f"{library.name}: expected output is missing: {output}")
            verify_architecture(output, expected)
        return 0
    for library in selected:
        build_library(library, theories_dir, expected, args.verbose)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
