#!/usr/bin/env python3
"""Build the header-free style corpus the profiler should actually see.

    python3 corpus/david/mkstyle.py

extract.py prefixes each post with a 4-line provenance header (# title / author /
date / url). That is useful for a human reader and poison for a stylometric
profiler: it put scrape chrome into the signature trigrams and inflated word and
sentence counts by roughly 5%. This writes corpus/david/style_clean/ containing
body prose only, and drops Medium's cross-post footer.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "style"
DEST = ROOT / "style_clean"

HEADER = re.compile(r"^(author|date|url):\s|^#\s")
FOOTER = re.compile(
    r"was originally published in .* on Medium, where people are continuing the conversation",
    re.I,
)


def words(text: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", text))


def main() -> int:
    if not SRC.is_dir():
        print(f"missing {SRC}")
        return 1
    DEST.mkdir(exist_ok=True)
    rows = []
    for src in sorted(SRC.glob("*.txt")):
        keep = []
        for para in src.read_text(encoding="utf-8", errors="replace").split("\n\n"):
            p = para.strip()
            if not p or HEADER.match(p) or FOOTER.search(p):
                continue
            keep.append(p)
        body = "\n\n".join(keep) + "\n"
        dest = DEST / src.name
        dest.write_text(body, encoding="utf-8")
        rows.append((src.name[5:42], words(src.read_text(encoding='utf-8')), words(body)))

    w = max(len(n) for n, _, _ in rows)
    print(f"\nwrote -> {DEST}\n")
    print(f"  {'post':<{w}}  {'was':>7}  {'now':>7}")
    tb = tn = 0
    for n, b, a in rows:
        print(f"  {n:<{w}}  {b:>7,}  {a:>7,}")
        tb += b
        tn += a
    print(f"\n  {'TOTAL':<{w}}  {tb:>7,}  {tn:>7,}   ({tn - tb:+d} words of chrome removed)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
