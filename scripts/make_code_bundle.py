#!/usr/bin/env python
"""
Generate a single markdown bundle (code_bundle.md) containing:
- Metadata (timestamp UTC, git commit if available)
- File manifest (name, size, lines, sha256)
- Global integrity hash (sha256 of all per-file hashes concatenated in
  sorted order)
- Full contents of each file in fenced code blocks (language guessed
  by extension)

Intended for: offline audit sharing, reproducibility, integrity
verification.
"""

from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys
from typing import Iterable, List, Tuple

from app.utils.time import utcnow

# ---- Configuration ---------------------------------------------------------

ROOT = pathlib.Path(__file__).resolve().parent.parent

ALLOW_EXT = {
    ".py",
    ".yml",
    ".yaml",
    ".md",
    ".toml",
    ".ini",
    ".txt",
    ".conf",
    ".sh",
    ".sql",
    ".env",  # only template / sanitized; actual .env skipped below
}

ALLOW_NAMED = {
    "Dockerfile",
    ".gitignore",
    ".env.example",
    "Makefile",
}

EXCLUDE_DIRS = {
    ".git",
    ".ruff_cache",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    "projects_data",
    "mosquitto/certs",  # exclude certs / binary secrets
    "pgdata",
}

EXCLUDE_FILES = {
    "eventbus.db",
    "test.db",
    "tls.crt",
    "tls.key",
    "audit_report.md",
    "code_bundle.md",
}

OUTPUT_FILE = ROOT / "code_bundle.md"


# ---- Helpers ---------------------------------------------------------------


def is_allowed(path: pathlib.Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel in EXCLUDE_FILES:
        return False
    for d in EXCLUDE_DIRS:
        if rel == d or rel.startswith(d + "/"):
            return False
    if path.name in ALLOW_NAMED:
        return True
    if path.suffix.lower() in ALLOW_EXT:
        # Skip *real* .env to avoid leaking secrets (allow only example)
        if path.name == ".env":
            return False
        return True
    return False


def iter_files() -> Iterable[pathlib.Path]:
    for p in ROOT.rglob("*"):
        if p.is_file() and is_allowed(p):
            yield p


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def detect_language(path: pathlib.Path) -> str:
    ext = path.suffix.lower()
    return {
        ".py": "python",
        ".yml": "yaml",
        ".yaml": "yaml",
        ".toml": "toml",
        ".ini": "ini",
        ".md": "markdown",
        ".txt": "text",
        ".conf": "conf",
        ".sh": "bash",
        ".sql": "sql",
        ".env": "bash",
        "": "",
    }.get(ext, "")


def get_git_commit() -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=ROOT,
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
    except Exception:
        return "N/A"


def read_text_preserve(path: pathlib.Path) -> str:
    """
    Read file as UTF-8; fall back to latin-1 if necessary (rare).
    Avoid altering raw content (no newline normalization here).
    """
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


# ---- Main ------------------------------------------------------------------


def main() -> None:
    files: List[pathlib.Path] = sorted(
        iter_files(),
        key=lambda p: p.as_posix(),
    )
    if not files:
        print(
            "No files matched configuration. Adjust ALLOW lists.",
            file=sys.stderr,
        )
        sys.exit(1)

    manifest_rows: List[Tuple[str, int, int, str]] = []
    lines_out: List[str] = []

    utc_now = utcnow().replace(microsecond=0)
    git_commit = get_git_commit()

    lines_out.append("# Consolidated Code Bundle\n")
    lines_out.append(f"Generated (UTC): {utc_now.isoformat()}  \n")
    lines_out.append(f"Git commit: `{git_commit}`\n")
    lines_out.append(f"Total files: {len(files)}\n\n")

    for f in files:
        data = f.read_bytes()
        text = read_text_preserve(f)
        line_count = text.count("\n") + (
            0 if text.endswith("\n") else (1 if text else 0)
        )
        file_hash = sha256_bytes(data)
        manifest_rows.append((f.as_posix(), len(data), line_count, file_hash))

    concat_hash_source = "".join(row[3] for row in manifest_rows).encode()
    global_hash = sha256_bytes(concat_hash_source)

    lines_out.append("## Integrity\n")
    lines_out.append(f"- Global concatenated file-hash SHA256: **{global_hash}**\n")
    lines_out.append(
        "  (Computed by concatenating each file's SHA256 (sorted by path) "
        "and hashing that string.)\n\n"
    )

    lines_out.append("## Manifest\n\n")
    lines_out.append("| File | Bytes | Lines | SHA256 |\n")
    lines_out.append("|------|-------|-------|--------|\n")
    for path_str, size_b, lc, h in manifest_rows:
        lines_out.append(f"| `{path_str}` | {size_b} | {lc} | `{h}` |\n")
    lines_out.append("\n---\n\n")

    for f, size_b, lc, h in manifest_rows:
        lang = detect_language(pathlib.Path(f))
        lines_out.append(f"### `{f}`\n\n")
        lines_out.append(f"- Size: {size_b} bytes  \n")
        lines_out.append(f"- Lines: {lc}  \n")
        lines_out.append(f"- SHA256: `{h}`\n\n")
        lines_out.append(f"```{lang}\n")
        file_text = read_text_preserve(ROOT / f)
        lines_out.append(file_text)
        if not file_text.endswith("\n"):
            lines_out.append("\n")
        lines_out.append("```\n\n")

    OUTPUT_FILE.write_text(
        "".join(lines_out),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {OUTPUT_FILE}")
    print(f"Global integrity hash: {global_hash}")


if __name__ == "__main__":
    main()
