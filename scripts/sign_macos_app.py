"""Ad-hoc sign a macOS app bundle and package it in a DMG.

This deliberately does not use ``codesign --deep`` for signing. Mach-O files
are signed individually from the inside out, followed by nested code bundles
and the outer application bundle.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable, Sequence


class SigningError(RuntimeError):
    """An actionable signing or DMG creation error."""


def _run(command: Sequence[str], *, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, check=True, text=True, capture_output=capture_output)
    except FileNotFoundError as exc:
        raise SigningError(f"required macOS tool was not found: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        raise SigningError(f"command failed with exit status {exc.returncode}: {' '.join(command)}") from exc


def is_macho(file_output: str) -> bool:
    """Return whether ``file`` output identifies Mach-O code."""
    return "Mach-O" in file_output


def discover_macho_files(contents_dir: Path) -> list[Path]:
    """Find real Mach-O files below Contents, excluding symlinks."""
    found: list[Path] = []
    for root, directories, filenames in os.walk(contents_dir, followlinks=False):
        directories[:] = sorted(directory for directory in directories if not (Path(root) / directory).is_symlink())
        for filename in sorted(filenames):
            candidate = Path(root) / filename
            if candidate.is_symlink() or not candidate.is_file():
                continue
            result = _run(["file", "-b", str(candidate)], capture_output=True)
            if is_macho(result.stdout):
                found.append(candidate)
    return sorted(found, key=lambda path: (len(path.relative_to(contents_dir).parts), str(path)))


_BUNDLE_SUFFIXES = {".app", ".appex", ".bundle", ".framework", ".plugin", ".xpc"}


def discover_code_bundles(app_path: Path, macho_files: Iterable[Path]) -> list[Path]:
    """Find nested code bundles that contain discovered Mach-O files."""
    macho_files = list(macho_files)
    bundles: set[Path] = set()
    for macho in macho_files:
        current = macho.parent
        while current != app_path and app_path in current.parents:
            if current.suffix in _BUNDLE_SUFFIXES and not current.is_symlink():
                bundles.add(current)
            current = current.parent
    return sorted(bundles, key=lambda path: (-len(path.relative_to(app_path).parts), str(path)))


def adhoc_sign(path: Path) -> None:
    print(f"Ad-hoc signing: {path}")
    _run(["codesign", "--force", "--sign", "-", str(path)])


def sign_app(app_path: Path) -> list[Path]:
    """Sign nested Mach-O code and bundles, then sign the outer app last."""
    if not app_path.is_dir() or app_path.suffix != ".app":
        raise SigningError(f"application bundle does not exist: {app_path}")
    contents_dir = app_path / "Contents"
    if not contents_dir.is_dir():
        raise SigningError(f"application bundle has no Contents directory: {app_path}")

    macho_files = discover_macho_files(contents_dir)
    if not macho_files:
        raise SigningError(f"no Mach-O files found below {contents_dir}")
    print(f"Found {len(macho_files)} Mach-O file(s) under {contents_dir}")
    for macho in sorted(macho_files, key=lambda path: (-len(path.relative_to(contents_dir).parts), str(path))):
        adhoc_sign(macho)
    for bundle in discover_code_bundles(app_path, macho_files):
        adhoc_sign(bundle)

    # Keep this explicit and last: no app contents may be changed afterwards.
    print(f"Ad-hoc signing outer application: {app_path}")
    _run(["codesign", "--force", "--sign", "-", str(app_path)])
    return macho_files


def verify_app(app_path: Path) -> None:
    print("Verifying ad-hoc signature (adhoc)")
    _run(["codesign", "--verify", "--deep", "--strict", "--verbose=4", str(app_path)])
    _run(["codesign", "-dv", "--verbose=4", str(app_path)])


def create_dmg(app_path: Path, dmg_path: Path) -> None:
    """Create a simple compressed DMG with an Applications shortcut."""
    with tempfile.TemporaryDirectory(prefix="reptate-dmg-") as temporary_directory:
        staging = Path(temporary_directory)
        shutil.copytree(app_path, staging / app_path.name, symlinks=True)
        (staging / "Applications").symlink_to("/Applications", target_is_directory=True)
        print(f"Creating DMG: {dmg_path}")
        _run([
            "hdiutil", "create", "-volname", "RepTate", "-srcfolder", str(staging),
            "-ov", "-format", "UDZO", str(dmg_path),
        ])
    verify_dmg(dmg_path, app_path.name)
    print("DMG contains the ad-hoc signed app; the DMG itself is unsigned.")


def verify_dmg(dmg_path: Path, app_name: str) -> None:
    """Mount the image read-only and verify its simple drag-and-drop layout."""
    with tempfile.TemporaryDirectory(prefix="reptate-dmg-mount-") as temporary_directory:
        mountpoint = Path(temporary_directory)
        _run(["hdiutil", "attach", "-readonly", "-nobrowse", "-mountpoint", str(mountpoint), str(dmg_path)])
        try:
            if not (mountpoint / app_name).is_dir():
                raise SigningError(f"DMG is missing {app_name}")
            if not (mountpoint / "Applications").is_dir():
                raise SigningError("DMG is missing the Applications shortcut")
            print(f"Verified DMG contents: {app_name}, Applications")
        finally:
            _run(["hdiutil", "detach", str(mountpoint)])


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("app", type=Path, help="assembled .app bundle to sign")
    parser.add_argument("dmg", type=Path, help="output DMG path")
    args = parser.parse_args(argv)
    if sys.platform != "darwin":
        raise SigningError("macOS app signing and DMG creation require macOS")
    sign_app(args.app)
    verify_app(args.app)
    create_dmg(args.app, args.dmg)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SigningError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
