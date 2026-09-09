import importlib.util
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "sign_macos_app.py"
SPEC = importlib.util.spec_from_file_location("sign_macos_app", SCRIPT)
assert SPEC and SPEC.loader
sign_macos_app = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sign_macos_app
SPEC.loader.exec_module(sign_macos_app)


def test_macho_detection():
    assert sign_macos_app.is_macho("Mach-O 64-bit dynamically linked shared library arm64")
    assert not sign_macos_app.is_macho("ELF 64-bit LSB shared object")


def test_nested_bundles_are_inside_out():
    app = Path("dist/RepTate.app")
    framework = app / "Contents/Frameworks/Example.framework"
    nested = framework / "Versions/A/PlugIns/Inner.plugin"
    macho = nested / "Inner"
    bundles = sign_macos_app.discover_code_bundles(app, [macho])
    assert bundles == [nested, framework]
