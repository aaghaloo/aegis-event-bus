#!/usr/bin/env bash
set -e
OUT=audit_report.md

echo "# Aegis Event Bus Audit Bundle" > "$OUT"
echo "Generated (UTC): $(date -u)" >> "$OUT"

echo -e "\n## Repo Tree (depth 4)\n" >> "$OUT"
echo '```' >> "$OUT"
# If 'tree' exists use it; else fallback to find
if command -v tree >/dev/null 2>&1; then
  tree -L 4 -I '.git|.pytest_cache|__pycache__|projects_data|pgdata|.venv|*.pyc' >> "$OUT"
else
  find . -maxdepth 4 -type f | grep -v -E '\.git|__pycache__|\.pytest_cache|projects_data|pgdata|\.venv' >> "$OUT"
fi
echo '```' >> "$OUT"

echo -e "\n## LOC Summary\n" >> "$OUT"
echo '```' >> "$OUT"
if command -v cloc >/dev/null 2>&1; then
  cloc . --exclude-dir=.git,projects_data,pgdata,.pytest_cache,__pycache__,.venv >> "$OUT"
else
  echo "Install cloc for richer stats (pip install cloc)" >> "$OUT"
fi
echo '```' >> "$OUT"

echo -e "\n## Source & Infra Files\n" >> "$OUT"

FILES=$(git ls-files | grep -E '^(app/|tests/|migrations/|Dockerfile|docker-compose.yml|alembic.ini|requirements.txt|pyproject.toml|\.github/workflows/|\.pre-commit-config.yaml|\.env.example)$' || true)

for f in $FILES; do
  echo -e "\n### $f\n" >> "$OUT"
  echo '```' >> "$OUT"
  # Redact secrets if any
  sed -E 's/(SECRET_KEY=).*/\1***REDACTED***/' "$f" >> "$OUT"
  echo '```' >> "$OUT"
done

echo -e "\n## Migration Versions\n" >> "$OUT"
for f in migrations/versions/*.py; do
  [ -f "$f" ] || continue
  echo -e "\n### $f\n" >> "$OUT"
  echo '```' >> "$OUT"
  cat "$f" >> "$OUT"
  echo '```' >> "$OUT"
done

echo "✅ Wrote $OUT"
