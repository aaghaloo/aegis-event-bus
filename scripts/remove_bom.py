from pathlib import Path


def strip_bom(path: str = "requirements.txt") -> None:
    p = Path(path)
    raw = p.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        p.write_bytes(raw[3:])
        print(f"{path}: BOM removed.")
    else:
        print(f"{path}: no BOM found.")


if __name__ == "__main__":
    strip_bom()
