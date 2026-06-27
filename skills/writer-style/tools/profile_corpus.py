#!/usr/bin/env python3
"""
profile_corpus.py — the builder-internal stylometric pass (writer-style v2).

Reads a source's raw corpus, CLEANS the chrome that polluted v1 (HTML
<center>/<br> tags, Substack/template footers, meta headers), and emits
`<out>/<name>.profile.json` with two blocks:

  meta + raw   — the full forensic numbers (sentence-length distribution,
                 punctuation, openers, signature n-grams, …). BUILDER-INTERNAL —
                 the writer agent never reads these.
  card_suggestions — the GENERATION-ACTIONABLE dials, already distilled to the
                 values a `<voice>.card.yaml` exposes (median/burstiness,
                 FK grade, lexical-density / example / code / question enums,
                 hedge-vs-boost lean, person-perspective). The card author drops
                 these in and hand-curates the favor/avoid/move/ai-tell lists.

    python profile_corpus.py --paths kaue=../../../tone-lora/corpus/you/raw \
        --include 'self-host|hackathon|defis-core|mcp-services' --out ../profiles/kaue/evidence
    python profile_corpus.py --corpus ../../../tone-lora/corpus --authors helius,vitalik,balaji,hayes,hotz \
        --out ../profiles/kaue/evidence
    python profile_corpus.py --selftest

Pure-Python, no network. --selftest validates the logic + the cleaning + the
card-derivation invariants.
"""
from __future__ import annotations
import argparse, json, re, sys, statistics as st
from collections import Counter
from pathlib import Path

from style_lexicons import (
    WORD_RE, SENT_RE, FUNCTION_WORDS,
    HEDGES, BOOSTERS, CAUSAL, CONTRASTIVE, ADDITIVE,
    DEFINITION_MARKERS, ANALOGY_MARKERS, EXAMPLE_MARKERS,
    flesch_kincaid_grade, count_markers,
)

LOG = lambda *a: print(*a, file=sys.stderr, flush=True)

# ── corpus cleaning ───────────────────────────────────────────────────────────
_META = re.compile(r"^<!--.*?-->\s*", re.S)                 # our raw/ url header
_LEAD_TITLE = re.compile(r"^#\s+.*\n")                       # leading markdown title
_HTML = re.compile(r"<[^>\n]{1,40}>")                       # <center>, <br>, <br/> …
_FENCE = re.compile(r"```.*?```", re.S)                      # fenced code blocks
_INLINE_CODE = re.compile(r"`[^`\n]+`")
# boilerplate / scrape-chrome lines (case-insensitive, whole-line contains).
# NB: be specific — "stay up to date with new developments" is genuine advice in
# the corpus; only the newsletter-CTA form ("up-to-date with the latest in Solana
# development") is chrome.
_CHROME = re.compile(
    r"^.*(this post was originally|originally published at|subscribe|"
    r"share this post|related articles|up.?to.?date with the latest|"
    r"the latest in solana development|further resources|thanks for reading|"
    r"thanks for reviewing|if you'?ve read this far|many thanks to|"
    r"special thanks to|follow the author|read more|leave a comment).*$",
    re.I | re.M,
)
# guest reposts (essays by OTHER authors republished on the source's site) — skip
# the whole file; they are not the target author's voice.
_GUESTPOST = re.compile(r"this post was originally written by", re.I)


def clean_prose(text: str) -> tuple[str, int, int]:
    """Return (prose_without_code_or_chrome, fenced_block_count, inline_code_count)."""
    t = _META.sub("", text)
    t = _LEAD_TITLE.sub("", t, count=1)
    fenced = len(_FENCE.findall(t))
    inline = len(_INLINE_CODE.findall(t))
    t = _FENCE.sub(" ", t)            # drop code from prose stats (counted separately)
    t = _INLINE_CODE.sub(" ", t)
    t = _HTML.sub(" ", t)             # kill <center>/<br> artifacts
    t = _CHROME.sub("", t)            # kill footer/template lines
    return t.strip(), fenced, inline


def sentences(text: str) -> list[str]:
    return [s.strip() for s in SENT_RE.split(text) if s.strip()]


_FIRST_SENT = re.compile(r"^\s*(.+?[.!?])(\s|$)", re.S)


def first_sentence(text: str) -> str:
    m = _FIRST_SENT.match(text.strip())
    return m.group(1).strip() if m else text.strip().split("\n", 1)[0].strip()


def classify_opener(sent: str) -> str:
    s = sent.strip()
    low = s.lower()
    if s.endswith("?"):
        return "question"
    if re.match(r"^(who|what|when|where|why|how|which)\b", low) and len(s.split()) <= 14:
        return "question"
    if re.match(r"^[\"“']", s):
        return "quote"
    if re.match(r"^(\d|\$|€|£)", s) or re.search(r"^\D{0,12}\d+%", s):
        return "data"
    if re.match(r"^(imagine|picture|suppose|when |in \d{4}|back in|consider |say you|let's say)", low):
        return "scenario"
    if re.match(r"^(i |we |my |our |i've|we've|i'm|when i|years ago)", low):
        return "story"
    return "claim"


def _pct(data, q):
    data = sorted(data)
    if not data:
        return 0
    k = max(0, min(len(data) - 1, int(round(q * (len(data) - 1)))))
    return data[k]


def _enum(value, low, high):
    return "low" if value < low else ("high" if value > high else "medium")


def profile(texts: list[str]) -> dict:
    cleaned = [clean_prose(t) for t in texts]
    prose = [c[0] for c in cleaned if c[0]]
    fenced = sum(c[1] for c in cleaned)
    inline = sum(c[2] for c in cleaned)
    full = "\n\n".join(prose)
    low = full.lower()

    words = WORD_RE.findall(low)
    n = max(1, len(words))
    per1k = lambda c: round(1000 * c / n, 1)
    sents = sentences(full)
    slens = [len(WORD_RE.findall(s)) for s in sents] or [0]
    mean_sl = round(st.mean(slens), 1)
    stdev_sl = round(st.pstdev(slens), 1) if len(slens) > 1 else 0.0

    # paragraphs: re-split on real blank lines; flag if a single "paragraph" is a whole doc
    paras = [p for t in prose for p in re.split(r"\n\s*\n", t) if p.strip()]
    plens = [len(sentences(p)) for p in paras] or [0]
    para_median = st.median(plens)
    para_valid = para_median <= 12  # >12 sentences/para ⇒ blank lines were lost upstream

    # punctuation
    punct = {p: per1k(full.count(p)) for p in [",", ";", ":", "—", "(", "?", "!", "..."]}

    # openers
    openers = Counter(classify_opener(first_sentence(p)) for p in paras if p.strip())
    op_total = max(1, sum(openers.values()))
    opener_pct = {k: round(100 * v / op_total) for k, v in openers.items()}

    # lexical
    content = [w for w in words if w not in FUNCTION_WORDS and len(w) > 2]
    lex_density = round(len(content) / n, 3)
    ttr = round(len(set(words)) / n, 3)
    long_frac = round(sum(1 for w in words if len(w) >= 7) / n, 3)
    fk = flesch_kincaid_grade(words, len(sents))

    # stance
    hedges = count_markers(low, HEDGES)
    boosters = count_markers(low, BOOSTERS)
    lean_raw = (boosters - hedges) / (n / 1000.0) if n else 0
    hedge_boost_lean = max(-2, min(2, round(lean_raw / 3)))

    # person perspective (pronoun-share) — tokenized (counts sentence-initial &
    # possessive pronouns the old space-padded scan missed)
    _FIRST = {"i", "me", "my", "mine", "we", "us", "our", "ours",
              "i'm", "i've", "i'd", "i'll", "we're", "we've", "we'd", "we'll"}
    _SECOND = {"you", "your", "yours", "you're", "you've", "you'd", "you'll"}
    _THIRD = {"he", "she", "it", "they", "them", "him", "his", "her", "hers",
              "its", "their", "theirs", "he's", "she's", "they're"}
    fp = sum(1 for w in words if w in _FIRST)
    sp = sum(1 for w in words if w in _SECOND)
    tp = sum(1 for w in words if w in _THIRD)
    ptot = max(1, fp + sp + tp)
    perspective = {"first": round(100 * fp / ptot), "second": round(100 * sp / ptot),
                   "third": round(100 * tp / ptot)}

    # teaching-craft + connective rates (per 1k words)
    def_rate = per1k(count_markers(low, DEFINITION_MARKERS))
    ana_rate = per1k(count_markers(low, ANALOGY_MARKERS))
    ex_rate = per1k(count_markers(low, EXAMPLE_MARKERS))
    num_rate = per1k(len(re.findall(r"\b\d[\d,.]*\b", full)))
    code_rate = per1k(fenced)
    q_rate = per1k(full.count("?"))   # count '?' directly — SENT_RE.split() drops the delimiter, so the old
    #                                   `s.endswith("?")` was always False and this metric was dead-zero.
    causal = per1k(count_markers(low, CAUSAL))
    contrastive = per1k(count_markers(low, CONTRASTIVE))
    additive = per1k(count_markers(low, ADDITIVE))

    # signature n-grams (builder-internal; chrome already stripped)
    sig_words = Counter(content).most_common(15)
    bg = Counter(zip(words, words[1:]))
    tg = Counter(zip(words, words[1:], words[2:]))

    return {
        "meta": {
            "n_pieces": len(prose), "n_words": n, "n_sentences": len(sents),
            "n_paragraphs": len(paras), "fenced_code_blocks": fenced, "inline_code_spans": inline,
            "corpus_cleaned": True,
            "paragraph_metric_valid": para_valid,
            "warnings": ([] if para_valid else ["paragraph_metric_suspect: blank lines lost upstream"]),
        },
        "raw": {  # BUILDER-INTERNAL — not for the writer
            "sentence_len": {
                "median": st.median(slens), "mean": mean_sl,
                "p10": _pct(slens, .1), "p90": _pct(slens, .9),
                "min": min(slens), "max": max(slens), "stdev": stdev_sl,
                "cv": round(stdev_sl / mean_sl, 2) if mean_sl else 0.0,
            },
            "paragraph_sentences": {"median": para_median, "p90": _pct(plens, .9), "valid": para_valid},
            "punct_per_1k_words": punct,
            "openers": {"counts": dict(openers), "pct": opener_pct, "n": op_total},
            "lexical": {"content_word_ratio": lex_density, "type_token_ratio": ttr,
                        "long_word_frac": long_frac, "flesch_kincaid_grade": fk},
            "stance": {"hedges_per_1k": per1k(hedges), "boosters_per_1k": per1k(boosters),
                       "perspective": perspective},
            "teaching": {"definition_per_1k": def_rate, "analogy_per_1k": ana_rate,
                         "example_per_1k": ex_rate, "numeric_per_1k": num_rate,
                         "code_blocks_per_1k": code_rate, "question_per_1k": q_rate},
            "connectives": {"causal_per_1k": causal, "contrastive_per_1k": contrastive,
                            "additive_per_1k": additive},
            "signature_content_words": sig_words,
            "signature_bigrams": [(" ".join(k), c) for k, c in bg.most_common(12)],
            "signature_trigrams": [(" ".join(k), c) for k, c in tg.most_common(10)],
        },
        "card_suggestions": {  # WRITER-FACING dials, ready to drop into <voice>.card.yaml
            "sentence_length": {
                "median": int(st.median(slens)),
                "short_punch_floor": max(3, _pct(slens, .1)),
                "long_reach": _pct(slens, .9),
                "burstiness_min": max(7, round(stdev_sl * 0.6)),   # realistic floor a full lesson clears
            },
            "readability_grade": {"min": max(5, int(fk - 2)), "max": int(fk + 2)},
            "lexical_density": _enum(lex_density, 0.48, 0.55),
            "hedge_boost_lean": hedge_boost_lean,
            "person_perspective": perspective,
            "example_density": _enum(ex_rate, 2, 5),
            "code_density": ("none" if code_rate == 0 else _enum(code_rate, 1, 4)),
            "rhetorical_question_rate": ("none" if q_rate == 0 else _enum(q_rate, 3, 8)),
            "definition_marker_rate_per_1k": def_rate,   # hint; author sets the positional enum
            "analogy_per_1k": ana_rate,
            "top_connectives_seen": _top_connectives(low),
        },
    }


def _top_connectives(low: str) -> list[str]:
    cand = CAUSAL + CONTRASTIVE + ADDITIVE
    seen = [(c.strip(", "), low.count(c)) for c in cand]
    return [c for c, n in sorted(seen, key=lambda x: -x[1]) if n > 0][:6]


def read_texts(path: Path, include: re.Pattern | None) -> list[str]:
    texts, skipped = [], 0
    if path.is_dir():
        for fp in sorted(list(path.glob("*.md")) + list(path.glob("*.txt"))):
            if include and not include.search(fp.name):
                continue
            t = fp.read_text("utf-8", "replace")
            if _GUESTPOST.search(t):                  # essay by another author — skip
                skipped += 1
                continue
            texts.append(t)
    if skipped:
        LOG(f"  (skipped {skipped} guest-repost file(s) — not the target author's voice)")
    return [t for t in texts if t.strip()]


def run(sources: dict[str, Path], out: Path, include: re.Pattern | None):
    out.mkdir(parents=True, exist_ok=True)
    for name, path in sources.items():
        texts = read_texts(path, include)
        if not texts:
            LOG(f"[{name}] no texts at {path} (skip)"); continue
        p = profile(texts)
        (out / f"{name}.profile.json").write_text(json.dumps(p, indent=2), encoding="utf-8")
        m, cs = p["meta"], p["card_suggestions"]
        LOG(f"[{name}] {m['n_pieces']} pcs, {m['n_words']} words -> {out}/{name}.profile.json "
            f"(median {cs['sentence_length']['median']}w, FK {p['raw']['lexical']['flesch_kincaid_grade']}, "
            f"para_valid={m['paragraph_metric_valid']})")


def selftest() -> int:
    ok = True
    def check(c, m):
        nonlocal ok; print(("PASS" if c else "FAIL") + " - " + m); ok = ok and c

    # cleaning strips HTML artifacts and chrome
    dirty = ["<center><br>Real prose here. It has two sentences.<br></center>\n\n"
             "This post was originally published at example.com\nSubscribe now!"]
    pr, fenced, inline = clean_prose(dirty[0])
    check("center" not in pr and "<br>" not in pr, "HTML <center>/<br> stripped")
    check("originally published" not in pr.lower() and "subscribe" not in pr.lower(), "chrome lines stripped")

    # bursty vs uniform
    bursty = ["Ship it. No excuses. " + ("a fairly long winding sentence that keeps going for a while " * 2) +
              "Done."]
    uniform = ["word word word word word. " * 8]
    pb, pu = profile(bursty), profile(uniform)
    check(pb["raw"]["sentence_len"]["stdev"] > pu["raw"]["sentence_len"]["stdev"],
          "bursty text has higher sentence-length stdev")

    # card_suggestions never leak a forensic field; every suggested dial is present
    cs = pb["card_suggestions"]
    for key in ["sentence_length", "readability_grade", "lexical_density", "hedge_boost_lean",
                "person_perspective", "example_density", "code_density", "rhetorical_question_rate"]:
        check(key in cs, f"card_suggestions has '{key}'")
    check("function_word" not in json.dumps(cs) and "type_token" not in json.dumps(cs),
          "no forensic field leaks into card_suggestions")

    # paragraph validity flag fires on a single blob
    blob = [("Sentence one. " * 20).strip()]  # one paragraph, 20 sentences
    check(profile(blob)["meta"]["paragraph_metric_valid"] is False, "paragraph_metric_valid flags a blob")

    # openers + perspective compute
    qa = ["Why does this matter? Because it does.\n\nYou should care. I tested it."]
    pq = profile(qa)
    check(pq["raw"]["openers"]["counts"].get("question", 0) >= 1, "detects a question opener")
    check(pq["card_suggestions"]["person_perspective"]["first"] >= 0, "perspective computed")
    check(pq["raw"]["teaching"]["question_per_1k"] > 0, "question_per_1k counts '?' (was dead-zero before)")

    print("\n" + ("PROFILER SELFTESTS PASSED" if ok else "FAILURES ABOVE"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="Builder-internal stylometric profiler (writer-style v2).")
    ap.add_argument("--corpus", default=None, help="<corpus>/<author>/raw layout")
    ap.add_argument("--authors", default="all", help="comma list or 'all'")
    ap.add_argument("--paths", default=None, help="name=dir,name=dir (overrides --corpus)")
    ap.add_argument("--include", default=None, help="regex; only files whose name matches are read")
    ap.add_argument("--out", default="evidence", help="output dir for <name>.profile.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    include = re.compile(a.include) if a.include else None
    sources: dict[str, Path] = {}
    if a.paths:
        for part in a.paths.split(","):
            if "=" not in part:
                ap.error(f"--paths expects name=dir pairs, got: {part!r}")
            k, v = part.split("=", 1); sources[k.strip()] = Path(v.strip())
    elif a.corpus:
        root = Path(a.corpus)
        names = ([d.name for d in root.iterdir() if d.is_dir() and not d.name.startswith("_")]
                 if a.authors == "all" else [x.strip() for x in a.authors.split(",")])
        for nm in names:
            sources[nm] = root / nm / "raw"
    else:
        ap.error("need --paths or --corpus")
    run(sources, Path(a.out), include)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
