# scripts/no_bom_check.py
from pathlib import Path

p = Path("requirements.txt")
data = p.read_bytes()

if data.startswith(b"\xef\xbb\xbf"):
    print("BOM found in requirements.txt (remove it: Save As UTF-8 w/out BOM).")
    raise SystemExit(1)

print("No BOM present in requirements.txt.")
