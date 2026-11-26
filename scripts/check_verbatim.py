#!/usr/bin/env python3
"""Check that a rebuilt deck still has every word of the original, slide by slide.

Usage: check_verbatim.py ORIGINAL NEW

ORIGINAL and NEW are PDFs rendered from the decks (one page per slide), or text files
with pages separated by form feeds or by a line "===== PAGE =====".
Needs pdftotext (poppler) for PDFs.

Prints, per slide, the original words missing from the new version, and exits 1 if any are missing.
Expected misses: hyphenation at line breaks in the original ("pré-" + "treinada") and approved
wording changes. Extra words in the new deck (labels and captions you added) are not reported.
"""
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


def pages(path: Path) -> list[str]:
    if path.suffix.lower() == ".pdf":
        text = subprocess.run(["pdftotext", "-layout", str(path), "-"], check=True,
                              capture_output=True, text=True).stdout
    else:
        text = path.read_text(encoding="utf-8")
    text = text.replace(" ", " ").replace("‑", "-")
    parts = re.split(r"\f|^=+ ?PAGE ?=+$", text, flags=re.M)
    return [p for p in parts if p.strip()] if "=====" in text else parts


def words(page: str) -> Counter:
    page = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1-\2", page)        # hyphen split across lines
    tokens = re.findall(r"[\w@,.%±→×<=/()-]+", page)
    return Counter(t for t in tokens if not re.fullmatch(r"\d{1,2}", t))   # skip slide numbers


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    orig, new = pages(Path(sys.argv[1])), pages(Path(sys.argv[2]))
    if len([p for p in orig if p.strip()]) != len([p for p in new if p.strip()]):
        print(f"warning: {len(orig)} pages in the original, {len(new)} in the new deck")
    bad = 0
    for i, (o, n) in enumerate(zip(orig, new), 1):
        if not o.strip():
            continue
        wn = words(n)
        missing = words(o) - wn
        # "pré-" + "treinada" split by a line break in the original, "pré-treinada" whole in the new deck
        for part in [w for w in missing if w.endswith("-")]:
            for joined in wn:
                rest = joined[len(part):]
                if joined.startswith(part) and rest and missing.get(rest):
                    missing[part] -= 1
                    missing[rest] -= 1
                    break
        missing = +missing
        if missing:
            bad += 1
            print(f"slide {i}: missing " + ", ".join(f"{w}" + (f" ×{c}" if c > 1 else "") for w, c in missing.items()))
        else:
            print(f"slide {i}: ok")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
