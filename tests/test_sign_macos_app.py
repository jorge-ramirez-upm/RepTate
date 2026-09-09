import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).parents[1] / "scripts" / "sign_macos_app.py"
SPEC = importlib.util.spec_from_file_location("sign_macos_app", SCRIPT)
assert SPEC and SPEC.loader
sign_macos_app = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sign_macos_app
SPEC.loader.exec_module(sign_macos_app)


def test_macho_detection():
    assert sign_macos_app.is_macho("Mach-O 64-bit dynamically linked shared library arm64")
    assert not sign_macos_app.is_macho("ELF 64-bit LSB shared object")


def test_reptate_owned_classification():
    app = Path("dist/RepTate.app")
    assert sign_macos_app.is_reptate_owned(app / "Contents/MacOS/RepTate.bin", app)
    assert sign_macos_app.is_reptate_owned(app / "Contents/MacOS/RepTate/theories/rouse_lib_darwin.so", app)
    assert sign_macos_app.is_reptate_owned(app / "Contents/Resources/RepTate/foo.so", app)
    assert not sign_macos_app.is_reptate_owned(app / "Contents/MacOS/scipy/foo.so", app)


def test_signature_decision():
    def runner(command):
        if str(command[-1]).endswith("invalid.so"):
            raise sign_macos_app.SigningError("invalid")

    assert sign_macos_app.has_valid_signature(Path("valid.so"), runner)
    assert not sign_macos_app.has_valid_signature(Path("invalid.so"), runner)


def test_nested_bundles_are_inside_out():
    app = Path("dist/RepTate.app")
    framework = app / "Contents/Frameworks/Example.framework"
    nested = framework / "Versions/A/PlugIns/Inner.plugin"
    macho = nested / "Inner"
    bundles = sign_macos_app.discover_code_bundles(app, [macho])
    assert bundles == [nested, framework]


def test_symlink_is_excluded_from_macho_discovery(tmp_path, monkeypatch):
    target = tmp_path / "real"
    target.write_text("binary")
    link = tmp_path / "link"
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        return

    def fake_run(command, **kwargs):
        return subprocess.CompletedProcess(command, 0, stdout="Mach-O 64-bit", stderr="")

    monkeypatch.setattr(sign_macos_app, "_run", fake_run)
    assert sign_macos_app.discover_macho_files(tmp_path) == [target]


def test_signing_summary_and_outer_order(tmp_path, monkeypatch):
    app = tmp_path / "RepTate.app"
    contents = app / "Contents/MacOS"
    contents.mkdir(parents=True)
    owned = contents / "RepTate.bin"
    valid = contents / "scipy/valid.so"
    invalid = contents / "scipy/invalid.so"
    valid.parent.mkdir()
    owned.touch()
    valid.touch()
    invalid.touch()
    bundle = app / "Contents/Frameworks/Third.framework"
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        if command[:3] == ["codesign", "--verify", "--strict"] and str(command[-1]).endswith(("invalid.so", "Third.framework")):
            raise sign_macos_app.SigningError("invalid")
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(sign_macos_app, "_run", fake_run)
    monkeypatch.setattr(sign_macos_app, "discover_macho_files", lambda _: [owned, valid, invalid])
    monkeypatch.setattr(sign_macos_app, "discover_code_bundles", lambda *_: [bundle])
    summary = sign_macos_app.sign_app(app)

    assert summary.reptate_owned_signed == 1
    assert summary.third_party_signed == 1
    assert summary.third_party_preserved == 1
    assert summary.nested_bundles_signed == 1
    assert summary.outer_signed
    force_signs = [call[-1] for call in calls if call[:3] == ["codesign", "--force", "--sign"]]
    assert force_signs[-1] == str(app)


def test_dmg_creation_retries_and_removes_partial_output(tmp_path, monkeypatch):
    app = tmp_path / "RepTate.app"
    (app / "Contents").mkdir(parents=True)
    (app / "Contents" / "resource.txt").write_text("ready")
    dmg = tmp_path / "RepTate.dmg"
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        if command[:2] == ["hdiutil", "create"]:
            create_count = len([call for call in calls if call[:2] == ["hdiutil", "create"]])
            if create_count == 1:
                dmg.touch()
                raise sign_macos_app.SigningError("Resource busy")
            assert not dmg.exists()
            dmg.touch()
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(sign_macos_app, "_run", fake_run)
    monkeypatch.setattr(sign_macos_app, "verify_dmg", lambda *_: None)
    monkeypatch.setattr(sign_macos_app.time, "sleep", lambda _: None)
    sign_macos_app.create_dmg(app, dmg)

    creates = [call for call in calls if call[:2] == ["hdiutil", "create"]]
    assert len(creates) == 2
    assert dmg.is_file()


def test_dmg_creation_propagates_after_three_failures(tmp_path, monkeypatch):
    app = tmp_path / "RepTate.app"
    (app / "Contents").mkdir(parents=True)
    dmg = tmp_path / "RepTate.dmg"
    attempts = []

    def fake_run(command, **kwargs):
        if command[:2] == ["hdiutil", "create"]:
            attempts.append(command)
            dmg.touch()
            raise sign_macos_app.SigningError("Resource busy")
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(sign_macos_app, "_run", fake_run)
    monkeypatch.setattr(sign_macos_app.time, "sleep", lambda _: None)
    with pytest.raises(sign_macos_app.SigningError, match="Resource busy"):
        sign_macos_app.create_dmg(app, dmg)
    assert len(attempts) == 3
    assert not dmg.exists()
