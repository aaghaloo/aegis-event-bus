#!/usr/bin/env python
"""
Generate a comprehensive audit bundle (single markdown file) that inlines
key source, infra, and test files for offline / external review.

Run:
    python scripts/make_full_audit.py
Outputs:
    audit_report_full.md
"""

from __future__ import annotations

import datetime as dt
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PRIMARY_FILES = [
    "Dockerfile",
    "docker-compose.yml",
    "alembic.ini",
    "pyproject.toml",
    "requirements.txt",
    ".pre-commit-config.yaml",
    "README.md",
    "app/main.py",
    "app/db.py",
    "app/endpoints.py",
    "app/security.py",
    "app/schemas.py",
    "app/logging_config.py",
    "app/cli.py",
    "app/archivist.py",
    "app/models.py",
    "migrations/env.py",
    "migrations/versions",
    "tests/conftest.py",
    "tests/test_api.py",
    "tests/test_pagination.py",
    "tests/test_archivist.py",
    "scripts/gen-mqtt-cert.sh",
]

OUTPUT_FILE = REPO_ROOT / "audit_report_full.md"


def list_tree(max_depth: int = 6) -> str:
    """Return a code block listing the repo tree up to max_depth."""
    lines: list[str] = []
    root_depth = len(REPO_ROOT.parts)
    for path in sorted(REPO_ROOT.rglob("*")):
        if any(
            skip in path.parts
            for skip in (
                ".git",
                ".ruff_cache",
                ".mypy_cache",
                "__pycache__",
                ".venv",
            )
        ):
            continue
        depth = len(path.parts) - root_depth
        if depth > max_depth:
            continue
        rel = path.relative_to(REPO_ROOT)
        lines.append(str(rel).replace("\\", "/"))
    return "```\n" + "\n".join(lines) + "\n```"


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return f"[BINARY or NON-UTF8: {path.name}]"
    except FileNotFoundError:
        return "[MISSING]"


def section_for_file(rel: str) -> str:
    """Build a markdown section for a file or directory."""
    path = REPO_ROOT / rel
    header = f"### {rel}\n"
    if path.is_dir():
        child_chunks: list[str] = []
        for child in sorted(path.rglob("*")):
            if child.is_dir():
                continue
            rel_child = child.relative_to(REPO_ROOT)
            content = read_text_file(child)
            child_chunks.append(
                "#### {name}\n\n```\n{body}\n```\n".format(
                    name=rel_child,
                    body=content,
                )
            )
        body = "\n".join(child_chunks) if child_chunks else "_(empty)_\n"
        return header + body
    content = read_text_file(path)
    return header + f"\n```\n{content}\n```\n"


def generate() -> str:
    now = dt.datetime.utcnow().strftime("%a, %b %d, %Y %H:%M:%S UTC")
    out: list[str] = []
    out.append(f"# Full Source Audit Bundle\n\nGenerated: {now}\n")
    out.append("## Repository Tree (truncated)\n")
    out.append(list_tree())
    out.append("\n---\n\n## File Contents\n")
    for rel in PRIMARY_FILES:
        out.append(section_for_file(rel))
        out.append("\n")
    return "\n".join(out)


def write_report() -> Path:
    report = generate()
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    return OUTPUT_FILE


def main() -> None:
    report_path = write_report()
    line_count = sum(1 for _ in report_path.read_text(encoding="utf-8").splitlines())
    msg = f"✅ Audit bundle written to: {report_path}\nLines: {line_count}"
    print(textwrap.dedent(msg).strip())


if __name__ == "__main__":
    main()
