"""Build RepTate-owned native theory libraries on the current platform.

The direct C recipes follow the platform-specific source README files. Bob
retains its established generated-object makefile as an explicit special case.
Linux and Windows builds use the same source inventory as the working Darwin
build; only compiler flags and output names vary by platform.
"""

from __future__ import annotations

import argparse
import ctypes
import os
import platform as platform_module
import shutil
import struct
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence


PLATFORMS = ("darwin", "linux", "windows")


@dataclass(frozen=True)
class NativeLibrary:
    name: str
    source_dir: str
    source_files: tuple[str, ...]
    output_names: Mapping[str, str]
    special_build: str | None = None
    include_current_directory: bool = False

    def source_path(self, theories_dir: Path) -> Path:
        return theories_dir / self.source_dir

    def output_name(self, platform_name: str) -> str:
        try:
            return self.output_names[platform_name]
        except KeyError as exc:
            raise BuildError(f"{self.name}: no output is defined for platform {platform_name}") from exc

    def output_path(self, theories_dir: Path, platform_name: str) -> Path:
        return theories_dir / self.output_name(platform_name)


def _outputs(stem: str) -> dict[str, str]:
    return {
        "darwin": f"{stem}_darwin.so",
        "linux": f"{stem}_linux.so",
        "windows": f"{stem}_win32.so",
    }


_LANDSCAPE_SOURCES = (
    "brent.c", "c_math.c", "convergence.c", "error.c", "fdfsolver.c",
    "fdiv.c", "fsolver.c", "infnan.c", "landscape.c", "newton.c",
    "pow_int.c", "stream.c",
)

NATIVE_LIBRARIES = (
    NativeLibrary("dtd", "dtd_source_c_code", ("dtd.c", "trapz.c", "qtrap.c"), _outputs("dtd_lib")),
    NativeLibrary("kww", "kww_source_c_code", ("kww.c",), _outputs("kww_lib")),
    NativeLibrary("landscape", "BuildLandscape_Linux", _LANDSCAPE_SOURCES, _outputs("landscape"), include_current_directory=True),
    NativeLibrary(
        "react", "react_source_c_code",
        ("binsandbob.c", "polybits.c", "polycleanup.c", "polymassrg.c", "ran3.c", "tobitabatch.c", "tobitaCSTR.c", "multimetCSTR.c", "dieneCSTR.c", "calc_architecture.c"),
        _outputs("react_lib"),
    ),
    NativeLibrary("rouse", "rouse_source_c_code", ("rouse.c",), _outputs("rouse_lib")),
    NativeLibrary("rp_blend", "rp_blend_source_c_code", ("derivs_rolie_poly_blend.c",), _outputs("rp_blend_lib")),
    NativeLibrary("sccr", "sccr_source_c_code", ("sccr.c",), _outputs("sccr_lib")),
    NativeLibrary("schwarzl", "schwarzl_source_c_code", ("schwarzl.c",), _outputs("schwarzl_lib")),
    NativeLibrary(
        "bob", "modified_bob2.5/code/src/obj", (),
        {platform_name: f"bob2p5_lib_{platform_name if platform_name != 'windows' else 'win32'}.so" for platform_name in PLATFORMS},
        special_build="bob_makefile",
    ),
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


def expected_architecture(platform_name: str | None = None, machine: str | None = None) -> str:
    """Normalize the current runner architecture for diagnostics and checks."""
    platform_name = platform_name or detect_platform()
    value = (machine or platform_module.machine()).lower()
    aliases = {"amd64": "x86_64", "x86-64": "x86_64", "aarch64": "aarch64"}
    normalized = aliases.get(value, value)
    if platform_name == "windows" and normalized in {"x86", "i386", "i686"}:
        return "x86"
    return normalized


def parse_architectures(output: str) -> tuple[str, ...]:
    """Parse the whitespace-separated architecture list printed by lipo."""
    return tuple(part for part in output.split() if part)


def direct_command(library: NativeLibrary, platform_name: str = "darwin", compiler: str | None = None) -> list[str]:
    """Construct the existing direct compiler recipe for one platform."""
    compiler = compiler or {"darwin": "cc", "linux": "cc", "windows": "gcc"}[platform_name]
    flags = ["-dynamiclib", "-fPIC", "-O2"] if platform_name == "darwin" else ["-shared", "-fPIC", "-O2"]
    if platform_name == "windows":
        flags.append("-static-libgcc")
    command = [compiler, *flags, *library.source_files]
    if library.include_current_directory:
        command.append("-I./")
    command.extend(["-o", f"../{library.output_name(platform_name)}"])
    return command


def _run(command: Sequence[str], cwd: Path | None, library: NativeLibrary | None = None, verbose: bool = False, env=None) -> subprocess.CompletedProcess:
    if verbose:
        location = f" (in {cwd})" if cwd else ""
        print("$", " ".join(command) + location)
    try:
        return subprocess.run(command, cwd=cwd, env=env, check=True)
    except FileNotFoundError as exc:
        owner = f" for {library.name}" if library else ""
        raise BuildError(f"command not found{owner}: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        owner = f" ({library.name})" if library else ""
        source = f"; source location: {cwd}" if cwd else ""
        raise BuildError(f"command failed with exit status {exc.returncode}{owner}: {' '.join(command)}{source}") from exc


def _tool(name: str, description: str) -> str:
    path = shutil.which(name)
    if path is None:
        raise BuildError(f"required {description} was not found: {name}")
    return path


def _tool_environment(tool_paths: Sequence[str]) -> dict[str, str]:
    environment = os.environ.copy()
    directories = [str(Path(path).parent) for path in tool_paths]
    environment["PATH"] = os.pathsep.join(dict.fromkeys(directories + [environment.get("PATH", "")]))
    return environment


def _compiler(platform_name: str) -> str:
    default = "gcc" if platform_name == "windows" else "cc"
    configured = os.environ.get("CC")
    if configured:
        return configured
    return _tool(default, f"{platform_name} C compiler")


def _make_command(platform_name: str) -> tuple[str, dict[str, str], str]:
    names = ("mingw32-make", "make") if platform_name == "windows" else ("make",)
    make = next((shutil.which(name) for name in names if shutil.which(name)), None)
    if make is None:
        raise BuildError(f"required {platform_name} make program was not found (tried: {', '.join(names)})")
    cxx = _tool("g++", f"{platform_name} C++ compiler for Bob")
    return make, _tool_environment((make, cxx)), "g++"


def _file_output(path: Path, library: NativeLibrary) -> str:
    file_tool = _tool("file", "file inspection tool")
    try:
        result = subprocess.run([file_tool, "-b", str(path)], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        raise BuildError(f"{library.name}: file inspection failed with exit status {exc.returncode}: {path}") from exc
    description = result.stdout.strip()
    print(f"{path.name}: {description}")
    return description


def _verify_macos(path: Path, library: NativeLibrary, expected: str) -> None:
    try:
        result = subprocess.run(["lipo", "-archs", str(path)], check=True, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise BuildError(f"{library.name}: lipo was not found while checking {path}") from exc
    except subprocess.CalledProcessError as exc:
        raise BuildError(f"{library.name}: lipo failed with exit status {exc.returncode}: {path}") from exc
    architectures = parse_architectures(result.stdout)
    if architectures != (expected,):
        raise BuildError(f"{library.name}: expected macOS architecture {expected}, found {architectures or 'none'} in {path}")
    print(f"{path.name}: verified macOS architecture {expected}")


def _verify_linux(path: Path, library: NativeLibrary, expected: str) -> None:
    description = _file_output(path, library)
    if "ELF" not in description:
        raise BuildError(f"{library.name}: expected an ELF shared library, found {description}")
    architecture_tokens = {
        "x86_64": ("x86-64", "x86_64"),
        "aarch64": ("ARM aarch64", "AArch64", "aarch64"),
    }.get(expected, (expected,))
    if not any(token in description for token in architecture_tokens):
        raise BuildError(f"{library.name}: expected Linux architecture {expected}, found {description}")


def _windows_pe_machine(path: Path, library: NativeLibrary) -> int:
    try:
        with path.open("rb") as binary:
            header = binary.read(64)
            if len(header) < 64 or header[:2] != b"MZ":
                raise BuildError(f"{library.name}: {path} is not a PE executable (missing MZ header)")
            pe_offset = struct.unpack_from("<I", header, 0x3C)[0]
            binary.seek(pe_offset)
            pe_header = binary.read(6)
    except OSError as exc:
        raise BuildError(f"{library.name}: could not inspect Windows binary {path}: {exc}") from exc
    if len(pe_header) < 6 or pe_header[:4] != b"PE\0\0":
        raise BuildError(f"{library.name}: {path} is not a PE executable (missing PE header)")
    return struct.unpack_from("<H", pe_header, 4)[0]


def _verify_windows(path: Path, library: NativeLibrary, expected: str) -> None:
    machine = _windows_pe_machine(path, library)
    expected_machine = 0x8664 if expected == "x86_64" else None
    if expected_machine is None or machine != expected_machine:
        raise BuildError(f"{library.name}: expected x86_64 Windows DLL, found PE machine 0x{machine:04x} in {path}")
    print(f"{path.name}: verified Windows PE x86_64 (machine 0x{machine:04x})")


def _load_windows_library(path: Path, library: NativeLibrary) -> None:
    try:
        ctypes.CDLL(str(path))
    except OSError as exc:
        raise BuildError(f"{library.name}: Windows loader could not load {path}: {exc}") from exc
    print(f"{path.name}: ctypes.CDLL load passed")


def _windows_dependencies(path: Path, library: NativeLibrary) -> tuple[str, ...]:
    objdump = _tool("objdump", "Windows PE dependency inspection tool")
    try:
        result = subprocess.run([objdump, "-p", str(path)], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        raise BuildError(f"{library.name}: objdump dependency audit failed with exit status {exc.returncode}: {path}") from exc
    dependencies = parse_windows_dependencies(result.stdout)
    print(f"{path.name} imports: {', '.join(dependencies) or '(none)'}")
    return dependencies


def parse_windows_dependencies(output: str) -> tuple[str, ...]:
    """Parse DLL Name entries from GNU objdump PE output."""
    return tuple(
        line.split("DLL Name:", 1)[1].strip()
        for line in output.splitlines()
        if "DLL Name:" in line
    )


def verify_output(path: Path, library: NativeLibrary, platform_name: str, expected: str, load_windows: bool = False) -> None:
    if not path.is_file():
        raise BuildError(f"{library.name}: expected output was not created: {path}")
    if platform_name == "darwin":
        _verify_macos(path, library, expected)
    elif platform_name == "linux":
        _verify_linux(path, library, expected)
    elif platform_name == "windows":
        _verify_windows(path, library, expected)
        if load_windows:
            _load_windows_library(path, library)


def _remove_bob_products(source_dir: Path, verbose: bool = False) -> None:
    for product in (source_dir / "bob2p5_lib.so", *source_dir.glob("*.o")):
        if product.exists():
            product.unlink()
            if verbose:
                print(f"Removed {product}")


def bob_build_command(make: str, cxx: str, platform_name: str) -> list[str]:
    """Construct Bob's platform-specific make invocation."""
    command = [make, "-f", "makefile_for_lib"]
    if platform_name == "windows":
        command.append(f"cpp={cxx} -Wall -g -O3 -DNBETA -shared -fPIC -static-libstdc++ -static-libgcc")
        # This is deliberately after $(all_obj) in makefile_for_lib so the
        # static archive is searched after object-file references are known.
        command.append("BOB_LDFLAGS=-Wl,-Bstatic -lwinpthread -Wl,-Bdynamic")
    return command


def _build_bob(library: NativeLibrary, theories_dir: Path, platform_name: str, verbose: bool) -> None:
    source_dir = library.source_path(theories_dir)
    make, environment, cxx = _make_command(platform_name)
    if platform_name != "windows":
        _run([make, "-f", "makefile_for_lib", "clean"], source_dir, library, verbose, environment)
    else:
        # The makefile's clean recipe uses Unix rm; use the script's narrow
        # product cleanup on Windows while retaining the established build.
        _remove_bob_products(source_dir, verbose)
    _run(bob_build_command(make, cxx, platform_name), source_dir, library, verbose, environment)
    built = source_dir / "bob2p5_lib.so"
    if not built.is_file():
        raise BuildError(f"{library.name}: make completed but did not produce {built} (source: {source_dir})")
    shutil.copy2(built, library.output_path(theories_dir, platform_name))


def build_library(library: NativeLibrary, theories_dir: Path, platform_name: str, expected: str, verbose: bool) -> None:
    print(f"Building {library.name} ({platform_name})...")
    if library.special_build == "bob_makefile":
        _build_bob(library, theories_dir, platform_name, verbose)
    else:
        compiler = _compiler(platform_name)
        environment = _tool_environment((compiler,))
        _run(direct_command(library, platform_name, compiler), library.source_path(theories_dir), library, verbose, environment)
    output = library.output_path(theories_dir, platform_name)
    verify_output(output, library, platform_name, expected)
    print(f"Built {output.name}")


def clean_outputs(theories_dir: Path, platform_name: str) -> None:
    for library in NATIVE_LIBRARIES:
        output = library.output_path(theories_dir, platform_name)
        if output.exists():
            output.unlink()
            print(f"Removed {output.name}")
    _remove_bob_products(theories_dir / "modified_bob2.5/code/src/obj")


def audit_windows_dependencies(theories_dir: Path, selected: Sequence[NativeLibrary]) -> None:
    for library in selected:
        output = library.output_path(theories_dir, "windows")
        if not output.is_file():
            raise BuildError(f"{library.name}: expected output is missing for dependency audit: {output}")
        _windows_dependencies(output, library)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="build all libraries for the current platform")
    parser.add_argument("--library", choices=[library.name for library in NATIVE_LIBRARIES], help="build/check one library")
    parser.add_argument("--clean", action="store_true", help="remove current-platform outputs and Bob build products")
    parser.add_argument("--check", action="store_true", help="check current-platform outputs without rebuilding")
    parser.add_argument("--audit-dependencies", action="store_true", help="audit Windows DLL imports with objdump")
    parser.add_argument("--verbose", action="store_true", help="print compiler commands")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    platform_name = detect_platform()
    if platform_name not in PLATFORMS:
        print(f"Platform: {platform_name}")
        print("Native-library builds are not implemented for this platform.", file=sys.stderr)
        return 2

    theories_dir = Path(__file__).resolve().parents[1] / "RepTate" / "theories"
    expected = expected_architecture(platform_name)
    print(f"Platform: {platform_name}\nArchitecture: {expected}")
    if platform_name == "darwin":
        target = os.environ.get("MACOSX_DEPLOYMENT_TARGET", "")
        print(f"MACOSX_DEPLOYMENT_TARGET: {target or '(not set)'}")

    selected = [library for library in NATIVE_LIBRARIES if args.library is None or library.name == args.library]
    if args.clean:
        clean_outputs(theories_dir, platform_name)
        return 0
    if args.check:
        if args.audit_dependencies:
            if platform_name != "windows":
                raise BuildError("--audit-dependencies is only implemented on Windows")
            audit_windows_dependencies(theories_dir, selected)
        for library in selected:
            output = library.output_path(theories_dir, platform_name)
            verify_output(output, library, platform_name, expected, load_windows=platform_name == "windows")
        return 0
    for library in selected:
        build_library(library, theories_dir, platform_name, expected, args.verbose)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
