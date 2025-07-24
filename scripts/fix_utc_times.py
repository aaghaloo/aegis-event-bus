# scripts/fix_utc_times.py
# Purpose: swap deprecated datetime.utcnow() calls for timezone-aware utcnow().
# Safe to run once, commit the patched files, then delete or keep for history.

from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "app" / "cli.py",
    ROOT / "scripts" / "make_code_bundle.py",
    ROOT / "scripts" / "make_full_audit.py",
]

UTCNOW_RE = re.compile(r"datetime\.utcnow\(\)")
IMPORT_LINE = "from app.utils.time import utcnow"
REPLACEMENT = "utcnow()"


def add_import(text: str) -> str:
    """Ensure IMPORT_LINE is present right after a datetime import or at top."""
    lines = text.splitlines()
    if any(IMPORT_LINE in ln for ln in lines):
        return text

    new_lines = []
    inserted = False
    for ln in lines:
        new_lines.append(ln)
        if not inserted and (
            ln.strip().startswith("import datetime")
            or ln.strip().startswith("from datetime import")
        ):
            new_lines.append(IMPORT_LINE)
            inserted = True

    if not inserted:
        # put after a shebang if present, else at file start
        idx = 1 if lines and lines[0].startswith("#!") else 0
        new_lines = lines[:idx] + [IMPORT_LINE] + lines[idx:]

    return "\n".join(new_lines)


def patch_file(path: pathlib.Path) -> bool:
    original = path.read_text(encoding="utf-8")
    if "utcnow(" not in original and "datetime.utcnow(" not in original:
        return False

    replaced = UTCNOW_RE.sub(REPLACEMENT, original)
    replaced = add_import(replaced)

    if replaced != original:
        path.write_text(replaced, encoding="utf-8")
        print(f"[ok] Patched {path}")
        return True
    return False


def main() -> None:
    changed_any = False
    for p in TARGETS:
        if p.exists():
            changed_any |= patch_file(p)
    if not changed_any:
        print("[info] Nothing to patch.")


if __name__ == "__main__":
    main()
