#!/usr/bin/env python
"""
make_full_audit.py

Generate audit_report.md containing:
  - Timestamp & current git commit (if repo)
  - Python version
  - Tree listing (filtered)
  - Per-file SHA256 + line counts
  - Full contents of source / infra / test files
  - Summary tables

Works on Windows & *nix (no external deps).
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

EXPLICIT_FILES = {
    ".env.example",
    "Dockerfile",
    "docker-compose.yml",
    "alembic.ini",
    "requirements.txt",
    "pyproject.toml",
    "pytest.ini",
    ".pre-commit-config.yaml",
    ".github/workflows/ci.yml",
    "audit_report.md",
}

INCLUDE_DIRS = {
    "app",
    "tests",
    "migrations",
    "scripts",
    "mosquitto/conf",
    "mosquitto/certs",
}

EXTENSIONS = {
    ".py",
    ".yml",
    ".yaml",
    ".ini",
    ".md",
    ".txt",
    ".conf",
    ".crt",
    ".key",
    ".csr",
    ".srl",
}

OUTPUT_FILE = Path("audit_report.md")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def want_file(p: Path) -> bool:
    if p.name == OUTPUT_FILE.name:
        return False
    if p.is_dir():
        return False
    rp = rel(p)
    if rp in EXPLICIT_FILES:
        return True
    if any(rp.startswith(d + os.sep) or rp == d for d in INCLUDE_DIRS):
        if p.suffix.lower() in EXTENSIONS or p.name in EXPLICIT_FILES:
            return True
    return False


def get_git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "N/A"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_read_bytes(p: Path) -> bytes:
    try:
        return p.read_bytes()
    except Exception as e:
        return f"<<ERROR READING FILE: {e}>>".encode()


def detect_eol(data: bytes) -> str:
    if b"\r\n" in data:
        return "CRLF"
    return "LF"


def classify_encoding(data: bytes) -> str:
    if data.startswith(b"\xef\xbb\xbf"):
        return "UTF-8-BOM"
    return "UTF-8/Unknown (no BOM)"


def main() -> None:

    now = datetime.now(timezone.utc).replace(microsecond=0)
    commit = get_git_commit()
    root = Path.cwd()

    files = sorted(
        [p for p in root.rglob("*") if want_file(p)],
        key=lambda x: rel(x),
    )

    meta_rows = []
    total_lines = 0
    for f in files:
        raw = safe_read_bytes(f)
        try:
            text_preview = raw.decode("utf-8", errors="replace")
        except Exception:
            text_preview = ""
        line_count = text_preview.count("\n") + (
            1 if text_preview and not text_preview.endswith("\n") else 0
        )
        total_lines += line_count
        meta_rows.append(
            {
                "path": rel(f),
                "lines": line_count,
                "sha256": sha256_bytes(raw),
                "eol": detect_eol(raw),
                "enc": classify_encoding(raw),
                "size": len(raw),
            }
        )

    out = []
    out.append("# Aegis Event Bus – Full Code Audit\n")
    out.append(f"Generated (UTC): {now.isoformat()}\n")
    out.append(f"Git commit: `{commit}`\n")
    out.append(f"Python: {sys.version.split()[0]}\n")
    out.append("---\n")

    out.append("## Repository Tree (selected)\n")
    for f in files:
        out.append(f"- `{rel(f)}`")
    out.append("")

    out.append("## File Summary\n")
    header = "| File | Lines | Bytes | SHA256 | EOL | Encoding |"
    sep = "|------|-------|-------|--------|-----|----------|"
    out.append(header)
    out.append(sep)
    for r in meta_rows:
        short_hash = r["sha256"][:10]
        out.append(
            "| `{path}` | {lines} | {size} | `{hash}` | {eol} | {enc} |".format(
                path=r["path"],
                lines=r["lines"],
                size=r["size"],
                hash=short_hash,
                eol=r["eol"],
                enc=r["enc"],
            )
        )
    out.append(f"\n**Total lines:** {total_lines}\n")
    out.append("---\n")

    # Full contents
    out.append("## Full File Contents\n")
    for r in meta_rows:
        p = Path(r["path"])
        raw = safe_read_bytes(p)
        try:
            text = raw.decode("utf-8", errors="replace")
        except Exception:
            text = "<<BINARY OR UNREADABLE>>"

        out.append(f"### `{r['path']}`\n")
        out.append(
            "**Lines:** {lines}  |  **SHA256:** `{sha}`  |  **EOL:** {eol}  |  "
            "**Encoding:** {enc}\n".format(
                lines=r["lines"],
                sha=r["sha256"],
                eol=r["eol"],
                enc=r["enc"],
            )
        )

        out.append("```")
        out.append(text)
        if not text.endswith("\n"):
            out.append("")
        out.append("```\n")

    OUTPUT_FILE.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
