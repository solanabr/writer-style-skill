#!/usr/bin/env python3
"""Split an owner-pasted Medium dump (medium.txt) into clean per-article text.

    python3 corpus/david/split_paste.py

Articles are delimited by a bare URL on its own line. Everything after the URL up
to the next URL is that article's page text, including Medium's UI chrome, which
this strips. Writes corpus/david/paste/<slug>.txt and prints a word-count
comparison against the RSS-derived files in corpus/david/clean/ so it is obvious
whether the feed truncated any post.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "medium.txt"
OUT = ROOT / "paste"
RSS = ROOT / "clean"

# Lines that are Medium furniture, not authored prose.
CHROME_EXACT = {
    "follow", "following", "share", "listen", "sign up", "sign in", "open in app",
    "--", "—", "·", "member-only story", "get an email whenever david potolski lafeta publishes.",
    "subscribe", "more from david potolski lafeta", "recommended from medium",
}
CHROME_RE = re.compile(
    r"^("
    r"\d+\s*min read|"
    r"\d+(\.\d+)?[km]?$|"                      # clap / response counters
    r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2},\s*\d{4}$|"
    r"get .*stories in your inbox|"
    r"join medium for free|"
    r"published in|"
    r"written by|"
    r"responses? \(\d+\)|"
    r"text to speech|"
    r"david potolski lafeta$"
    r")",
    re.I,
)


def slugify(url: str) -> str:
    tail = url.rstrip("/").rsplit("/", 1)[-1]
    tail = re.sub(r"-[0-9a-f]{8,}$", "", tail)   # drop Medium's hash suffix
    return tail or "untitled"


def words(text: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", text))


def clean(lines: list[str]) -> str:
    out: list[str] = []
    for ln in lines:
        s = re.sub(r"[ \t\xa0]+", " ", ln).strip()
        if not s:
            continue
        if s.lower() in CHROME_EXACT or CHROME_RE.match(s):
            continue
        # Collapse the duplicated byline Medium renders twice in a row.
        if out and s == out[-1]:
            continue
        out.append(s)
    return "\n\n".join(out).strip() + "\n"


def main() -> int:
    if not SRC.is_file():
        print(f"missing {SRC}")
        return 1

    raw = SRC.read_text(encoding="utf-8", errors="replace").splitlines()
    marks = [i for i, ln in enumerate(raw) if ln.strip().startswith("http")]
    if not marks:
        print("no URL delimiters found in medium.txt")
        return 1

    OUT.mkdir(exist_ok=True)
    marks.append(len(raw))
    rows = []
    for a, b in zip(marks, marks[1:]):
        url = raw[a].strip()
        slug = slugify(url)
        body = clean(raw[a + 1 : b])
        dest = OUT / f"{slug}.txt"
        dest.write_text(f"url: {url}\n\n{body}", encoding="utf-8")

        # find the RSS counterpart by fuzzy slug match
        rss_n = 0
        key = slug.replace("-", "")
        for cand in RSS.glob("*.txt"):
            if key[:24] in cand.stem.replace("-", "").replace("feed", ""):
                rss_n = words(cand.read_text(encoding="utf-8", errors="replace"))
                break
        rows.append((slug, words(body), rss_n))

    w = max(len(s) for s, _, _ in rows)
    print(f"\nwrote -> {OUT}\n")
    print(f"  {'article':<{w}}  {'paste':>7}  {'rss':>7}  delta")
    for slug, p, r in rows:
        d = "—" if not r else f"{p - r:+d}"
        print(f"  {slug:<{w}}  {p:>7,}  {r:>7,}  {d}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
