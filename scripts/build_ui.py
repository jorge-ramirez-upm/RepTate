#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GUI_DIR = REPO_ROOT / "RepTate" / "gui"


def run(cmd: list[str]) -> None:
    print(" ".join(cmd))
    subprocess.check_call(cmd)


def compile_ui(ui_path: Path, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    run(["pyside6-uic", str(ui_path), "-o", str(out_path)])


def compile_qrc(qrc_path: Path, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    run(["pyside6-rcc", str(qrc_path), "-o", str(out_path)])


# Patch patterns in generated Ui_*.py
_IMPORT_RC_RE = re.compile(r"^(import\s+(\w+_rc)\s*)$", re.M)
_FROM_IMPORT_RC_RE = re.compile(r"^(from\s+(\w+_rc)\s+import\s+)", re.M)


def patch_rc_imports(py_path: Path) -> bool:
    """
    Replace in generated Ui_*.py:
      import Tool_rc
    with:
      from . import Tool_rc

    Also handles:
      from Tool_rc import X
    -> from .Tool_rc import X
    """
    txt = py_path.read_text(encoding="utf-8", errors="replace")
    txt2 = _IMPORT_RC_RE.sub(r"from . import \2", txt)
    txt2 = _FROM_IMPORT_RC_RE.sub(r"from .\2 import ", txt2)

    if txt2 != txt:
        py_path.write_text(txt2, encoding="utf-8")
        return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Compile RepTate UI (.ui) and resources (.qrc), patch *_rc imports."
    )
    ap.add_argument("--no-qrc", action="store_true", help="Do not compile .qrc files.")
    ap.add_argument(
        "--ui-glob", default="*.ui", help="UI glob inside RepTate/gui (default: *.ui)"
    )
    ap.add_argument(
        "--qrc-glob",
        default="*.qrc",
        help="QRC glob inside RepTate/gui (default: *.qrc)",
    )
    args = ap.parse_args()

    if not GUI_DIR.is_dir():
        print(f"ERROR: GUI folder not found: {GUI_DIR}", file=sys.stderr)
        return 2

    # 1) Compile QRC -> *_rc.py
    if not args.no_qrc:
        qrc_files = sorted(GUI_DIR.glob(args.qrc_glob))
        for qrc in qrc_files:
            out = GUI_DIR / f"{qrc.stem}_rc.py"
            print(f"[QRC] {qrc.name} -> {out.name}")
            compile_qrc(qrc, out)

    # 2) Compile UI -> Ui_<name>.py
    ui_files = sorted(GUI_DIR.glob(args.ui_glob))
    for ui in ui_files:
        out = GUI_DIR / f"Ui_{ui.stem}.py"
        print(f"[UI ] {ui.name} -> {out.name}")
        compile_ui(ui, out)

    # 3) Patch imports in Ui_*.py
    patched = 0
    for py in sorted(GUI_DIR.glob("Ui_*.py")):
        if patch_rc_imports(py):
            patched += 1
            print(f"[PATCH] {py.name}")

    print(f"Done. Patched {patched} Ui_*.py file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
