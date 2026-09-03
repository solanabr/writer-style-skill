#!/usr/bin/env python3
"""Turn fetched Medium HTML / RSS into clean corpus text.

    python3 corpus/david/extract.py

Reads  corpus/david/raw/*.html + feed.xml
Writes corpus/david/clean/<slug>.txt   (one blank-line-separated block per paragraph)
Prints a per-file word count so corpus thinness is visible before any mining starts.

Pure stdlib. Deliberately conservative: it drops anything it cannot confidently
attribute to the article body, because a dirty corpus profiles the scrape chrome
rather than the author.
"""

from __future__ import annotations

import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
CLEAN = ROOT / "clean"

# Block-level tags whose text we keep, in article order.
BLOCKS = {"p", "h1", "h2", "h3", "h4", "blockquote", "li", "pre", "figcaption"}
SKIP_CONTENT = {"script", "style", "noscript", "svg", "button", "nav", "footer"}

# Medium page furniture that lives inside <article> and is not authored prose.
CHROME = re.compile(
    r"^("
    r"sign up|sign in|follow|following|share|listen|more from|written by|"
    r"published in|responses? \(\d+\)|\d+ min read|open in app|member-only|"
    r"help|status|about|careers|press|blog|privacy|terms|text to speech|teams|"
    r"recommended from medium|see all from|see more recommendations"
    r")\b",
    re.I,
)


class ArticleParser(HTMLParser):
    """Collect block-level text found inside the first <article> element."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth_article = 0
        self.seen_article = False
        self.skip_depth = 0
        self.stack: list[str] = []
        self.buf: list[str] = []
        self.blocks: list[tuple[str, str]] = []

    # -- helpers ---------------------------------------------------------
    def _in_article(self) -> bool:
        return self.depth_article > 0 and self.skip_depth == 0

    def _flush(self, tag: str) -> None:
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        self.buf.clear()
        if text:
            self.blocks.append((tag, text))

    # -- parser hooks ----------------------------------------------------
    def handle_starttag(self, tag, attrs):
        if tag == "article":
            self.depth_article += 1
            self.seen_article = True
            return
        if self.depth_article and tag in SKIP_CONTENT:
            self.skip_depth += 1
            return
        if self._in_article() and tag in BLOCKS:
            self.buf.clear()
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "article" and self.depth_article:
            self.depth_article -= 1
            return
        if self.depth_article and tag in SKIP_CONTENT and self.skip_depth:
            self.skip_depth -= 1
            return
        if self.stack and tag == self.stack[-1]:
            self._flush(self.stack.pop())

    def handle_data(self, data):
        if self._in_article() and self.stack:
            self.buf.append(data)


def render(blocks: list[tuple[str, str]]) -> str:
    """Format blocks as plain prose, keeping heading + list structure."""
    out: list[str] = []
    seen: set[str] = set()
    for tag, text in blocks:
        if CHROME.match(text):
            continue
        # Medium repeats the title/subtitle in header and body; keep first only.
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        if tag in {"h1", "h2", "h3", "h4"}:
            out.append(f"## {text}")
        elif tag == "li":
            out.append(f"- {text}")
        elif tag == "blockquote":
            out.append(f"> {text}")
        else:
            out.append(text)
    return "\n\n".join(out).strip() + "\n"


def from_html(path: Path) -> str:
    parser = ArticleParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    if not parser.seen_article:
        return ""
    return render(parser.blocks)


TAGS = re.compile(r"<[^>]+>")
# Only these end a paragraph. Inline tags (<a>, <em>, <strong>, <code>) must be
# stripped WITHOUT a break, or mid-sentence links split one sentence into three
# and every sentence-length statistic downstream is garbage.
BLOCK_BREAK = re.compile(
    r"</(?:p|h[1-6]|li|blockquote|pre|figure|figcaption|div)\s*>|<br\s*/?>", re.I
)
ITEM = re.compile(r"<item>(.*?)</item>", re.S)
FIELD = {
    name: re.compile(rf"<{name}>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</{name}>", re.S)
    for name in ("title", "link", "pubDate", "dc:creator")
}
ENCODED = re.compile(r"<content:encoded>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</content:encoded>", re.S)


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] or "untitled"


def from_feed(path: Path) -> list[tuple[str, str, str]]:
    """-> [(slug, meta, body)] for every <item> carrying full content."""
    xml = path.read_text(encoding="utf-8", errors="replace")
    items = []
    for chunk in ITEM.findall(xml):
        def field(name: str) -> str:
            m = FIELD[name].search(chunk)
            return html.unescape(m.group(1)).strip() if m else ""

        title = field("title")
        body_html = ENCODED.search(chunk)
        if not body_html:
            continue
        raw_body = BLOCK_BREAK.sub("\n", body_html.group(1))
        raw_body = html.unescape(TAGS.sub("", raw_body))
        paras = []
        for ln in raw_body.split("\n"):
            ln = re.sub(r"[ \t\xa0]+", " ", ln).strip()
            if ln and not CHROME.match(ln):
                paras.append(ln)
        body = "\n\n".join(paras)
        meta = f"# {title}\nauthor: {field('dc:creator')}\ndate: {field('pubDate')}\nurl: {field('link')}"
        items.append((slugify(title), meta, body))
    return items


def words(text: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", text))


def main() -> int:
    if not RAW.is_dir() or not any(RAW.iterdir()):
        print(f"nothing in {RAW} — run: zsh corpus/david/fetch.sh", file=sys.stderr)
        return 1

    CLEAN.mkdir(exist_ok=True)
    written: list[tuple[str, int]] = []

    for src in sorted(RAW.glob("*.html")):
        body = from_html(src)
        if not body.strip():
            print(f"  !! {src.name}: no <article> body found (JS-rendered?)", file=sys.stderr)
            continue
        dest = CLEAN / f"{src.stem}.txt"
        dest.write_text(body, encoding="utf-8")
        written.append((dest.name, words(body)))

    feed = RAW / "feed.xml"
    if feed.is_file():
        for slug, meta, body in from_feed(feed):
            dest = CLEAN / f"feed-{slug}.txt"
            dest.write_text(f"{meta}\n\n{body}\n", encoding="utf-8")
            written.append((dest.name, words(body)))

    if not written:
        print("no usable text extracted", file=sys.stderr)
        return 1

    width = max(len(n) for n, _ in written)
    total = 0
    print(f"\nextracted -> {CLEAN}\n")
    for name, n in sorted(written):
        print(f"  {name:<{width}}  {n:>6,} words")
        total += n
    print(f"\n  {'TOTAL':<{width}}  {total:>6,} words across {len(written)} files\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
