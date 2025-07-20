# scripts/make_full_audit.py
"""
Generate a consolidated audit markdown containing:
 - File tree
 - Per-file SHA256 + size
 - Full source listings (safe set)
Usage:
    python scripts/make_full_audit.py
    python scripts/make_full_audit.py --include-secrets
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_EXCLUDES = {
    ".git",
    ".ruff_cache",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    "eventbus.db",
    "test.db",
    "pgdata",
    "mosquitto_data",
    "alembic/versions/__pycache__",
}

# Secrets you normally do NOT embed
SECRET_FILES = {
    ".env",
    "mosquitto/certs/ca.key",
    "mosquitto/certs/server.key",
    "tls.key",
    "tls.crt",
    "ca.key",
}

SAFE_EXTENSIONS = {
    ".py",
    ".toml",
    ".yml",
    ".yaml",
    ".ini",
    ".md",
    ".txt",
    ".conf",
    ".sh",
    ".sql",
    ".dockerfile",
    "dockerfile",
}

OUTPUT = ROOT / "audit_report.md"


def iter_files() -> Iterable[Path]:
    for p in ROOT.rglob("*"):
        if p.is_dir():
            continue
        rel = p.relative_to(ROOT)
        # Skip excludes
        if any(str(rel).startswith(ex) for ex in DEFAULT_EXCLUDES):
            continue
        yield rel


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def is_source_file(rel: Path) -> bool:
    if rel.name in SECRET_FILES:
        return False
    ext = rel.suffix.lower()
    if ext in SAFE_EXTENSIONS:
        return True
    # allow Dockerfile (no ext)
    if rel.name.lower() == "dockerfile":
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--include-secrets", action="store_true", help="Include secret files"
    )
    args = ap.parse_args()

    all_files = sorted(iter_files(), key=lambda p: str(p).lower())

    # Build file metadata table
    lines = []
    lines.append("# Aegis Event Bus – Full Audit Report\n")
    lines.append(f"Generated (UTC): {dt.datetime.utcnow():%Y-%m-%d %H:%M:%S}\n")
    lines.append("## File Inventory\n")
    lines.append("| Path | Size (bytes) | SHA256 |")
    lines.append("|------|--------------|--------|")

    for rel in all_files:
        path = ROOT / rel
        size = path.stat().st_size
        digest = sha256_file(path)
        lines.append(f"| `{rel}` | {size} | `{digest[:16]}...` |")

    lines.append("\n## Source Listings\n")
    for rel in all_files:
        path = ROOT / rel
        if rel.name in SECRET_FILES and not args.include_secrets:
            continue
        if not is_source_file(rel):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        lines.append(f"\n### `{rel}`\n")
        lines.append("```")
        lines.append(text.rstrip())
        lines.append("```")

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
