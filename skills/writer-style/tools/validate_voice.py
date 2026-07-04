#!/usr/bin/env python3
"""
validate_voice.py — the writer-style validator (post-generation checks).

Four checks, all pure-Python and deterministic:

  audit   — REPETITION audit. Batch mode (--lessons <dir>): opener-type diversity,
            repeated opening phrases, transition tics, cross-lesson 4-gram overlap.
            Single-doc mode (--file <doc>): the same checks BETWEEN THE SECTIONS of
            one long document (the long-form repetition compounder).
  tells   — AI-TELL lint on generated prose: banned words, false-antithesis
            ("not X, it's Y"), em-dash overuse, and the burstiness floor. Pass
            --card <voice>.card.yaml to enforce THAT voice's per-voice targets
            (burstiness_min, em-dash max, false-antithesis cap, avoid lists);
            without a card it uses universal defaults.
  density — SIGNATURE-MARKER dosage vs the card's `markers:` block: per-marker
            counts vs caps (per piece or per-words budget), windowed clustering,
            section spread, and the context GATE (an identity marker firing with
            no gate keyword in the fact-sheet = likely forced insertion). Pass
            --facts <fact-sheet> so gates can be checked; --markers <yaml> overrides
            the card's block (used while a card pre-dates the markers schema).
  diff    — FACT-PRESERVATION diff between the Pass-A fact-sheet and the Pass-C
            styled output: every number / code identifier in A must survive into C.

No cosine `match`/`ab` style-distance — that manufactured false confidence. Voice
fidelity is judged by a human blind read.

    python validate_voice.py audit   --lessons out_lessons/
    python validate_voice.py audit   --file long-piece.md
    python validate_voice.py tells   --file lesson.md --card ../profiles/kaue/kaue.card.yaml
    python validate_voice.py density --file lesson.md --card ../profiles/kaue/kaue.card.yaml --facts factsheet.md
    python validate_voice.py diff    --facts factsheet.md --styled lesson.md
    python validate_voice.py --selftest
"""
from __future__ import annotations
import argparse, difflib, re, sys
from collections import Counter
from pathlib import Path

from style_lexicons import (
    WORD_RE, AI_TELL_WORDS, AI_TELL_CONNECTIVES, FALSE_ANTITHESIS_RE,
    AI_TELL_TIER2, AI_TELL_TIER3, REPLACEMENTS, CRYPTO_CLICHES,
    COPULA_SUBSTITUTES, SYMBOLIC_GLOSS, AI_FINGERPRINTS, HEDGE_STACK_RE,
    SUMMARY_CLOSER_RE, META_HEDGE_RE, AT_ITS_CORE_RE,
)
from profile_corpus import classify_opener, sentences, first_sentence

LOG = lambda *a: print(*a, file=sys.stderr, flush=True)

TRANSITION_TICS = ["in today's", "in this lesson", "let's dive", "let's explore",
                   "at its core", "in conclusion", "it's important to", "as we'll see",
                   "now that we", "in the world of", "when it comes to"]

# universal defaults — used only when no <voice>.card.yaml is supplied
_QA_PUNCH_RE = re.compile(r"\?\s+([A-Z][^.!?\n]{0,30}[.!])")
DEFAULT_EMDASH_MAX_PER_1K = 4
DEFAULT_BURSTINESS_MIN_STDEV = 9
DEFAULT_FALSE_ANTITHESIS_PER_800W = 1
# below this absolute stdev a passage is machine-even regardless of voice (a HARD tell); the per-voice
# burstiness_min above it is an ADVISORY target (terse human authors legitimately sit in the 4-9 band).
HARD_UNIFORM_STDEV = 4


def ngrams(text: str, n: int) -> set:
    w = WORD_RE.findall(text.lower())
    return set(tuple(w[i:i + n]) for i in range(len(w) - n + 1))


def jaccard(a: set, b: set) -> float:
    return 0.0 if not a and not b else len(a & b) / max(1, len(a | b))


# ── audit ─────────────────────────────────────────────────────────────────────
def repetition_audit(lessons: list[str]) -> dict:
    first_sents = [first_sentence(t) for t in lessons]
    opener_types = [classify_opener(s) for s in first_sents if s]
    opener_hist = Counter(opener_types)
    heads = [" ".join(WORD_RE.findall(s.lower())[:6]) for s in first_sents if s]
    head_dups = sum(c - 1 for c in Counter(heads).values() if c > 1)
    joined = "\n".join(lessons).lower()
    tics = {t: joined.count(t) for t in TRANSITION_TICS if joined.count(t) > 0}
    grams = [ngrams(t, 4) for t in lessons]
    pairs = [(i, j) for i in range(len(grams)) for j in range(i + 1, len(grams))]
    overlap = round(sum(jaccard(grams[i], grams[j]) for i, j in pairs) / max(1, len(pairs)), 4)
    n = max(1, len(lessons))
    flags = []
    if n >= 5 and len(opener_hist) < 3:
        flags.append("LOW opener-type variety (<3) — repetitive openings")
    if head_dups > 0:
        flags.append(f"{head_dups} lessons share a near-identical opening phrase")
    if overlap > 0.18:
        flags.append(f"HIGH cross-lesson 4-gram overlap ({overlap}) — boilerplate")
    return {"lessons": len(lessons), "distinct_opener_types": len(opener_hist),
            "opener_histogram": dict(opener_hist), "duplicate_opening_phrases": head_dups,
            "transition_tics": tics, "mean_pairwise_4gram_overlap": overlap,
            "flags": flags or ["ok: no repetition red flags"]}


def intra_doc_audit(text: str) -> dict:
    """The repetition audit BETWEEN THE SECTIONS of one long document — the long-form
    compounder the batch audit can't see. Reuses repetition_audit's metrics with
    intra-doc thresholds (adjacent sections legitimately share terms of art, so the
    mean-overlap bar is 0.22 vs the 0.18 cross-lesson bar), plus two intra-doc-only
    checks: adjacent-pair overlap (copy-paste-restyled sections) and duplicate
    paragraph openers across the whole doc."""
    bodies = [b for _, b in split_sections(text) if len(WORD_RE.findall(b)) >= 50]
    if len(bodies) < 2:
        return {"sections": len(bodies),
                "flags": ["ok: too few sections for an intra-doc audit (needs 2+ of 50w+)"]}
    # split_sections glues the heading line into the body (density wants markers-in-headings counted),
    # but the opener classifier must see the PROSE's first sentence, not "## Title" — strip it here,
    # or every headed section classifies as "claim" and the variety check caps at 2 types structurally.
    prose = [re.sub(r"\A#{1,6}\s+[^\n]*\n+", "", b) for b in bodies]
    base = repetition_audit(prose)
    grams = [ngrams(p, 4) for p in prose]
    adj = [round(jaccard(grams[i], grams[i + 1]), 4) for i in range(len(grams) - 1)]
    adj_max = max(adj) if adj else 0.0
    heads = [" ".join(WORD_RE.findall(p.lower())[:6]) for p in _paragraphs(text)
             if len(WORD_RE.findall(p)) >= 6]
    dup_heads = {h: c for h, c in Counter(heads).items() if c > 1}
    flags = []
    if len(bodies) >= 4 and base["distinct_opener_types"] < 3:
        flags.append(f"LOW section-opener variety ({base['distinct_opener_types']} types over "
                     f"{len(bodies)} sections) — every section starts the same way")
    if base["duplicate_opening_phrases"] > 0:
        flags.append(f"{base['duplicate_opening_phrases']} sections share a near-identical opening phrase")
    if base["mean_pairwise_4gram_overlap"] > 0.22:
        flags.append(f"HIGH intra-doc 4-gram overlap ({base['mean_pairwise_4gram_overlap']}) — "
                     f"sections repeat themselves")
    if adj_max > 0.30:
        flags.append(f"adjacent sections nearly duplicated (max pair overlap {adj_max})")
    if dup_heads:
        flags.append(f"duplicate paragraph openers (first 6 words): {dup_heads}")
    if base["transition_tics"]:
        flags.append(f"transition tics: {base['transition_tics']}")
    return {"sections": len(bodies), "distinct_opener_types": base["distinct_opener_types"],
            "opener_histogram": base["opener_histogram"],
            "mean_4gram_overlap": base["mean_pairwise_4gram_overlap"],
            "adjacent_max_overlap": adj_max,
            "flags": flags or ["ok: no intra-doc repetition red flags"]}


# ── card reader (dependency-free: pulls only the validator targets) ────────────
def read_card_targets(path: str | None) -> dict:
    """Extract per-voice validator targets from a <voice>.card.yaml with a small
    regex reader (no YAML dependency). Falls back to universal defaults."""
    t = {"burstiness_min": DEFAULT_BURSTINESS_MIN_STDEV,
         "emdash_max": DEFAULT_EMDASH_MAX_PER_1K,
         "false_antithesis_cap": DEFAULT_FALSE_ANTITHESIS_PER_800W,
         "sentence_median": None,
         "avoid_words": [], "avoid_connectives": [], "voice": None}
    if not path or not Path(path).is_file():   # a dir or missing path -> universal defaults, not a crash
        return t
    text = Path(path).read_text("utf-8", "replace")

    def num(pat, key):
        m = re.search(pat, text, re.S)
        if m:
            t[key] = int(m.group(1))

    mv = re.search(r"^voice:\s*(\S+)", text, re.M)
    if mv:
        t["voice"] = mv.group(1)
    num(r"\bburstiness_min:\s*(\d+)", "burstiness_min")          # \b avoids meta_burstiness_min hijack
    num(r"sentence_length:[^\n]*\bmedian:\s*(\d+)", "sentence_median")
    num(r"\bem-?dash-overuse[^}\n]*max:\s*(\d+)", "emdash_max")
    num(r"\bfalse-antithesis[^}\n]*cap_per_800w:\s*(\d+)", "false_antithesis_cap")

    def items(block_key):
        m = re.search(r"\navoid:\s*(.*?)(?:\nai_tells:|\nnotes:|\Z)", text, re.S)
        block = m.group(1) if m else ""
        # allow one level of nesting so a token like "array[0]" or "[date]" doesn't truncate the list
        m2 = re.search(block_key + r":\s*\[((?:[^\[\]]|\[[^\]]*\])*)\]", block, re.S)
        if not m2:
            return []
        out = []
        # tokens: a "double"/'single' quoted string (may contain commas) OR a bareword.
        # the bareword class excludes quotes so it can't bleed into a quoted token after a separator.
        for a, b, c in re.findall(r'"([^"]*)"|\'([^\']*)\'|([^,\[\]"\'\n]+)', m2.group(1)):
            s = (a or b or c).strip()
            if s:
                out.append(s.lower())
        return out

    t["avoid_words"] = items("words")
    t["avoid_connectives"] = items("connectives")
    return t


# ── markers: dosage + context-gate engine ──────────────────────────────────────
# Card contract (line-oriented block style; single-line bracket lists — the same
# no-YAML-dep parser conventions as read_card_targets):
#
#   markers:
#     - id: latam-framing
#       class: identity          # identity | refrain | verdict-token | tic | analogy | structural | signoff
#       patterns: [latam, brazil, "emerging market"]
#       cap: 1
#       per_words: 0             # 0 = per piece; N = budget scales cap*round(words/N), floor cap
#       gate: [latam, brazil]    # OPTIONAL: keywords that must appear in the FACT-SHEET to earn the marker
#       enforce: hard            # OPTIONAL override; default hard for identity/signoff, advisory otherwise
#
# Hard/advisory policy (the calibration contract):
#   identity + gate MISS + any hit      -> HARD  (the "forced insertion" case — the reported bug)
#   identity + gate PASS + over budget  -> advisory (topic-legit lexemes may be substance, not beats)
#   identity + gate UNCHECKED           -> advisory (can't tell substance from beat without --facts)
#   signoff over budget                 -> HARD  (two sign-offs is objectively wrong)
#   tic/analogy/etc over budget         -> advisory until the card promotes them (enforce: hard)
#   clustering / section-spread         -> always advisory (heuristics)

_MARKER_TOKEN_RE = re.compile(r'"([^"]*)"|\'([^\']*)\'|([^,\[\]"\'\n]+)')


def _parse_bracket_list(s: str) -> list[str]:
    out = []
    for a, b, c in _MARKER_TOKEN_RE.findall(s):
        tok = (a or b or c).strip()
        if tok:
            out.append(tok.lower())
    return out


def read_card_markers(path: str | None) -> list[dict]:
    """Parse the `markers:` block from a card (or a standalone markers yaml).
    Missing file or missing block -> [] (density then has nothing to check —
    tolerant of cards that pre-date the markers schema)."""
    if not path or not Path(path).is_file():
        return []
    text = Path(path).read_text("utf-8", "replace")
    m = re.search(r"^markers:\s*\n(.*?)(?=^\S|\Z)", text, re.M | re.S)
    if not m:
        return []
    out = []
    for entry in re.split(r"^\s*-\s+(?=id:)", m.group(1), flags=re.M):
        if "id:" not in entry:
            continue
        mk: dict = {}
        for key in ("id", "class", "enforce"):
            km = re.search(rf"^\s*{key}:\s*([^\n#]+)", entry, re.M)
            if km:
                mk[key] = km.group(1).strip().strip("\"'").lower()
        for key in ("cap", "per_words"):
            km = re.search(rf"^\s*{key}:\s*(\d+)", entry, re.M)
            if km:
                mk[key] = int(km.group(1))
        for key in ("patterns", "gate"):
            km = re.search(rf"^\s*{key}:\s*\[((?:[^\[\]]|\[[^\]]*\])*)\]", entry, re.M)
            if km:
                mk[key] = _parse_bracket_list(km.group(1))
        if mk.get("id") and mk.get("patterns"):
            mk.setdefault("class", "tic")
            mk.setdefault("cap", 1)
            mk.setdefault("per_words", 0)
            out.append(mk)
    return out


def _compile_marker(p: str) -> re.Pattern:
    """Single tokens are boundary-guarded ('lfb' must not match inside a word);
    multiword/punctuated phrases match as substrings ('emerging market' catches
    'emerging markets')."""
    if re.fullmatch(r"[\w-]+", p):
        return re.compile(r"(?<!\w)" + re.escape(p) + r"(?!\w)", re.I)
    return re.compile(re.escape(p), re.I)


def split_sections(text: str) -> list[tuple[str, str]]:
    """Split on markdown headings; text before the first heading is '(intro)'.
    Sections under 50 words merge into the previous one (stub headings aren't
    sections). Heading text is kept inside the section body — a marker in a
    heading is still a marker."""
    parts = re.split(r"(?m)^(#{1,6}\s+.*)$", text)
    sections: list[tuple[str, str]] = []
    if parts[0].strip():
        sections.append(("(intro)", parts[0].strip()))
    for i in range(1, len(parts) - 1, 2):
        head = parts[i].lstrip("#").strip()
        sections.append((head, (parts[i] + "\n" + parts[i + 1]).strip()))
    merged: list[tuple[str, str]] = []
    for name, body in sections:
        if merged and len(WORD_RE.findall(body)) < 50:
            pn, pb = merged[-1]
            merged[-1] = (pn, pb + "\n\n" + body)
        else:
            merged.append((name, body))
    return merged or [("(all)", text)]


def _marker_enforce(mk: dict) -> str:
    e = mk.get("enforce")
    if e in ("hard", "advisory"):
        return e
    return "hard" if mk.get("class") in ("identity", "signoff") else "advisory"


def marker_density(text: str, markers: list[dict], gate_text: str | None = None) -> dict:
    """Count each marker's lexeme hits against its budget; check windows, section
    spread, and the context gate. gate_text is the FACT-SHEET, never the draft —
    a forced insertion contains its own lexemes, so self-checking would self-license."""
    import bisect
    nw = max(1, len(WORD_RE.findall(text.lower())))
    secs = split_sections(text)
    starts = [m.start() for m in WORD_RE.finditer(text)]
    glow = gate_text.lower() if gate_text is not None else None
    results, flags, hard = [], [], False
    for mk in markers:
        raw = mk.get("patterns", [])
        pats = [_compile_marker(p) for p in raw]
        pos = sorted(max(0, bisect.bisect_right(starts, m.start()) - 1)
                     for rx in pats for m in rx.finditer(text))
        count = len(pos)
        # per-lexeme hits — the STAMP signal needs to distinguish "same token every piece"
        # from "rotated tokens" (marker-level coverage alone can't)
        pattern_hits = {p: n for p, n in ((p, len(rx.findall(text))) for p, rx in zip(raw, pats)) if n}
        cap, per = mk.get("cap", 1), mk.get("per_words", 0)
        allowed = cap if per == 0 else max(cap, cap * round(nw / per))
        hit_secs = [i for i, (_, body) in enumerate(secs, 1) if any(rx.search(body) for rx in pats)]
        win_over = 0
        if per > 0 and count > cap:
            w = 0
            while w < nw:
                if sum(1 for p in pos if w <= p < w + per) > cap:
                    win_over += 1
                w += 250
        gate = mk.get("gate")
        if not gate:
            gate_status = "-"
        elif glow is None:
            gate_status = "UNCHECKED"
        else:
            gate_status = "pass" if any(kw in glow for kw in gate) else "MISS"
        enforce = _marker_enforce(mk)
        mid, mcls = mk["id"], mk.get("class", "tic")
        mflags, mhard = [], False
        if mcls == "identity" and gate_status == "MISS" and count > 0:
            mhard = enforce == "hard"
            tag = "[HARD]" if mhard else "[advisory]"
            mflags.append(f"{tag}[gate] identity '{mid}' fires {count}x but NO gate keyword in the "
                          f"fact-sheet — likely forced insertion; human gate must confirm")
        elif count > allowed:
            budget = f"{allowed}/piece" if per == 0 else f"{allowed} per {per}w"
            if mcls == "identity" and gate_status == "pass":
                mflags.append(f"[advisory] identity '{mid}' {count}x vs budget {budget} — gate passes "
                              f"(topic-legit); confirm it's substance, not saturation")
            elif mcls == "identity" and gate_status == "UNCHECKED":
                mflags.append(f"[advisory] identity '{mid}' {count}x over budget {budget} "
                              f"(gate UNCHECKED — pass --facts to check it)")
            elif enforce == "hard":
                mhard = True
                mflags.append(f"[HARD] {mcls} '{mid}' {count}x over budget {budget}")
            else:
                mflags.append(f"[advisory] {mcls} '{mid}' {count}x over budget {budget}")
        if win_over:
            mflags.append(f"[advisory] '{mid}' bunched — {win_over} window(s) of {per}w exceed cap {cap}; spread or cut")
        if len(secs) >= 3 and count >= 2 and len(hit_secs) > len(secs) / 2:
            mflags.append(f"[advisory] '{mid}' appears in {len(hit_secs)}/{len(secs)} sections — "
                          f"themed through the piece; thin it out")
        hard = hard or mhard
        flags.extend(mflags)
        results.append({"id": mid, "class": mcls, "count": count, "allowed": allowed,
                        "windows_over_cap": win_over, "sections_hit": hit_secs,
                        "gate_status": gate_status, "hard": mhard, "flags": mflags,
                        "pattern_hits": pattern_hits})
    return {"words": nw, "sections": len(secs), "markers": results, "hard": hard,
            "flags": flags or ["ok: all markers within budget"]}


# ── tells ─────────────────────────────────────────────────────────────────────
def ai_tell_lint(text: str, card: dict | None = None) -> dict:
    c = card if card is not None else read_card_targets(None)
    low = text.lower()
    words = WORD_RE.findall(low)
    nw = max(1, len(words))
    sents = sentences(text)
    slens = [len(WORD_RE.findall(s)) for s in sents] or [0]
    import statistics as st
    stdev = round(st.pstdev(slens), 1) if len(slens) > 1 else 0.0

    banlist = set(AI_TELL_WORDS) | set(c.get("avoid_words", []))
    banned = {w: low.count(w) for w in banlist if low.count(w) > 0}
    banconn = set(AI_TELL_CONNECTIVES) | set(c.get("avoid_connectives", []))
    banned_conn = {cc: low.count(cc) for cc in banconn if low.count(cc) > 0}
    antithesis = len(FALSE_ANTITHESIS_RE.findall(text))
    # em + en + the SPACED double-hyphen evasion (" -- "). Plain "--" is NOT counted: it false-flagged
    # CLI flags (--features, --no-bip39) at 250/1k on docs with zero real em-dashes.
    emdash_count = text.count("—") + text.count("–") + text.count(" -- ")
    emdash_per_1k = round(1000 * emdash_count / nw, 1)

    emdash_max = c.get("emdash_max", DEFAULT_EMDASH_MAX_PER_1K)
    burst_min = c.get("burstiness_min", DEFAULT_BURSTINESS_MIN_STDEV)
    fa_cap = c.get("false_antithesis_cap", DEFAULT_FALSE_ANTITHESIS_PER_800W)

    flags = []
    if banned:
        shown = {w: (f"{n}→'{REPLACEMENTS[w]}'" if w in REPLACEMENTS else n) for w, n in banned.items()}
        flags.append(f"banned AI-tell words (Tier-1, with swaps): {shown}")
    if banned_conn:
        flags.append(f"essay-bot connectives: {banned_conn}")
    if antithesis > max(1, round(fa_cap * nw / 800)):
        flags.append(f"false-antithesis 'not X, it's Y' overused ({antithesis} > cap {fa_cap}/800w)")
    # em-dash: rate-AND-count so a single dash in a short passage doesn't trip the /1k metric
    if emdash_count >= 3 and emdash_per_1k > emdash_max:
        flags.append(f"em-dash overuse ({emdash_count}×, {emdash_per_1k}/1k > {emdash_max})")
    # the "Question? Punch-answer." rhetorical machine — a real human move at ~1/piece; calibration
    # measured it industrialized 9x/batch. Count Q followed by a ≤4-word answer sentence.
    qa_hits = sum(1 for m in _QA_PUNCH_RE.finditer(text) if len(WORD_RE.findall(m.group(1))) <= 4)
    if qa_hits > 1:
        flags.append(f"self-answered-question machine used {qa_hits}× (human rate ~1/piece) — vary the pivot")
    # clipped-sentence drift: this voice runs LONG (card median); a piece averaging well under it is
    # machine-clipped even when burstiness passes (R1 measured means 13.6-17.1 vs corpus 20.5-40.3)
    mean_len = round(sum(slens) / max(1, len(slens)), 1)
    smed = c.get("sentence_median")
    if smed and nw >= 250 and mean_len < smed - 3:
        flags.append(f"sentences run short for this voice (mean {mean_len}w < card median {smed}-3) — let clauses breathe")
    # verdict-fragment headers: crafted antithesis headlines ("X is a default, not a plan") stamped
    # across a piece read as machine section-titling; humans title plainly
    vheads = [h for h in re.findall(r"(?m)^#{1,6}\s+(.+)$", text)
              if ", not " in h.lower() or "isn't" in h.lower() or "aren't" in h.lower()]
    if len(vheads) >= 2:
        flags.append(f"verdict-fragment headers ×{len(vheads)} ({vheads[:2]}…) — title sections plainly")
    # burstiness: judge cadence once there are enough sentences (≥8) in a real passage (≥150w) — short
    # snippets/exemplars stay exempt. Below the ROBOTIC floor it's a HARD tell (machine-even at any voice);
    # below the voice's own target but above robotic is ADVISORY (terse authors live there — don't clip them).
    if nw >= 150 and len(slens) >= 8:
        if stdev < HARD_UNIFORM_STDEV:
            flags.append(f"uniform cadence (sentence stdev {stdev} < {HARD_UNIFORM_STDEV}) — robotic, the #1 AI tell")
        elif stdev < burst_min:
            flags.append(f"burstiness below the voice target (stdev {stdev} < {burst_min}) — vary sentence length more")
    return {"words": nw, "sentence_stdev": stdev, "emdash_per_1k": emdash_per_1k,
            "false_antithesis": antithesis, "banned_words": banned, "burstiness_min": burst_min,
            "voice": c.get("voice"), "flags": flags or ["ok: no AI tells detected"]}


# ── deslop: tiered cliché + structural + machine-paste scan (voice-agnostic) ───
_BOLD_RE = re.compile(r"\*\*[^*\n]{1,60}\*\*")
_INLINE_HEADER_RE = re.compile(r"^\s*[-*]\s+\*\*[^*\n]+:\*\*", re.M)
_TITLECASE_HEAD_RE = re.compile(r"^#{1,6}\s+(?:[A-Z][a-z0-9]+\s+){2,}[A-Z][a-z0-9]+\s*$", re.M)


def _paragraphs(text: str) -> list[str]:
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def _markdown_hygiene(text: str, nw: int) -> list[str]:
    flags = []
    bold = len(_BOLD_RE.findall(text))
    if nw >= 120 and bold > 3 * nw / 100:
        flags.append(f"boldface overuse ({bold} spans / {nw}w) — earn emphasis, don't sprinkle it")
    if len(_INLINE_HEADER_RE.findall(text)) >= 3:
        flags.append("inline-header bullet lists (**Label:** …) — an AI list tic; fold into prose")
    if len(_TITLECASE_HEAD_RE.findall(text)) >= 2:
        flags.append("Title-Case headings — use sentence case")
    return flags


def deslop_flags(text: str) -> dict:
    """Voice-agnostic deslop scan. Tier-1 cliches are handled by ai_tell_lint (always-flag
    + swaps); this covers the GATED tiers + structural tells. `hard` = a near-dispositive
    machine-paste fingerprint fired (a real fail); the rest are advisory."""
    low = text.lower()
    nw = max(1, len(WORD_RE.findall(low)))
    flags, hard = [], False

    # Tier 2 — distinct-cluster gated per paragraph: ≥3 DISTINCT buzzwords sharing a
    # paragraph (humans use 1-2; AI piles them). A mix is the tell, not repetition.
    t2 = set()
    for p in _paragraphs(text):
        present = [w for w in AI_TELL_TIER2 if w in p.lower()]
        if len(present) >= 3:
            t2.update(present)
    if t2:
        flags.append(f"Tier-2 buzzword cluster (≥3 distinct/para): {sorted(t2)}")

    # Tier 3 — density gated: these are LEGIT in technical prose, so flag only as soup
    # (≥3 distinct AND ≥5 occurrences/1k). A few scattered across a long post is fine.
    t3 = sorted(w for w in AI_TELL_TIER3 if w in low)
    t3_per1k = 1000 * sum(low.count(w) for w in AI_TELL_TIER3) / nw
    if len(t3) >= 3 and t3_per1k >= 5:
        flags.append(f"Tier-3 buzzword density ({t3_per1k:.1f}/1k, {len(t3)} distinct): {t3}")

    # crypto/web3 boilerplate — cluster
    cc = [p for p in CRYPTO_CLICHES if p in low]
    if len(cc) >= 2:
        flags.append(f"crypto-boilerplate cluster: {cc}")

    # copula-avoidance — flag only as a cluster (one 'serves as' is fine)
    cop = [c for c in COPULA_SUBSTITUTES if c in low]
    if len(cop) >= 3:
        flags.append(f"copula-avoidance cluster {cop} — prefer is/are/has")

    # symbolic gloss — advisory (state the concrete fact instead)
    sg = [g for g in SYMBOLIC_GLOSS if g in low]
    if sg:
        flags.append(f"symbolic-gloss {sg} — state the fact, cut the gloss")

    # stacked hedging — advisory (one modal + one adverb is fine; two adverbs in a row is the tell)
    if HEDGE_STACK_RE.search(text):
        flags.append("stacked hedging (e.g. 'potentially eventually') — commit or cut one")

    # discourse scaffolding — the "essay frame" fluent BARE LLM output leaves even when it dodges the word-lists
    # (this is what bare ChatGPT/Claude prose trips that the lexical checks miss). All ~0% on the human corpus.
    paras = _paragraphs(text)
    if paras and any(SUMMARY_CLOSER_RE.match(s) for s in re.split(r"(?<=[.!?])\s+", paras[-1].strip())[-2:]):
        flags.append("summary-restatement closer ('In summary/In conclusion …') — the LLM essay-frame tell; cut it")
    mh = 1000 * len(META_HEDGE_RE.findall(text)) / nw
    if mh >= 2:
        flags.append(f"meta-hedge pile-up ({mh:.1f}/1k of 'it's worth noting'-class) — assert it or cut it")
    if 1000 * len(AT_ITS_CORE_RE.findall(text)) / nw >= 2:
        flags.append("'at its core / think of it as / in essence' framing — a default-LLM explainer tell")

    # machine-paste fingerprints — HARD (near-dispositive, voice-neutral)
    for fid, rx in AI_FINGERPRINTS:
        if rx.search(text):
            flags.append(f"machine-paste fingerprint: {fid}"); hard = True

    flags += _markdown_hygiene(text, nw)
    return {"hard": hard, "flags": flags or ["ok: no deslop flags"]}


# ── diff (fact preservation) ───────────────────────────────────────────────────
# a number with its OPTIONAL trailing unit, so "1232 bytes" != "1232 KB" (a 1024x error).
# (?<![\w.]) keeps us off mid-token digits (the "2" in v1.2); the .\d+ branch keeps a leading-dot ".002";
# (?:\.\d+)* keeps ALL version octets ("1.14.18", not just "1.14") so a patch-version bump is caught.
_NUMUNIT = re.compile(
    r"(?<![\w.])(\.\d+|\d[\d,]*(?:\.\d+)*)\s?"
    r"(%|bytes?|kb|mb|gb|tb|sol|lamports?|eth|btc|usdc?|usdt|ms|sec|secs|x)?\b", re.I)
_CODEISH = re.compile(
    r"`[^`\n]+`"                                  # inline code span
    r"|\b0x[0-9a-fA-F]+\b"                         # hex literal (discriminators, bitmasks)
    r"|\bv\d+(?:\.\d+)+\b"                         # v-prefixed version (v1.2, v1.2.3)
    r"|\b[A-Za-z_]\w*(?:::[A-Za-z_]\w*)+(?:\(\))?"  # Rust/Cpp path (Foo::bar, Clock::get()) — eats trailing ()
    r"|\b[A-Za-z_]\w*\(\)"                         # bare fn() call
    r"|\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b"         # SCREAMING_SNAKE const (TOKEN_PROGRAM_ID, MAX_RETRIES)
    r"|\b[a-z]+(?:_[a-z0-9]+)+\b"                  # snake_case
    r"|\b[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)+\b"      # CamelCase
)   # The SCREAMING rule needs an underscore on purpose: SCREAMING_SNAKE consts are real identifiers that must
    # survive, but bare acronyms (CU, ALT, RPC) get expanded in prose ("compute units") — faithful, not a drop —
    # so they're left out. Ticker/unit swaps (SOL->ETH, bytes->KB) stay caught by _NUMUNIT when a number is attached.
_LISTMARK = re.compile(r"(?m)^\s{0,3}\d+\.\s")    # markdown ordered-list markers are not facts
_PLAINNUM = re.compile(r"\d[\d,]*(?:\.\d+)?")      # a single int/decimal — _NUMUNIT already owns these


def _norm_num(s: str) -> str:
    s = s.replace(",", "").strip()
    s = re.sub(r"^\.(\d)", r"0.\1", s)         # .002 -> 0.002 (no false fail on leading-zero styling)
    if "." not in s:
        s = s.lstrip("0") or "0"               # 007 -> 7
    return s


def _norm_code(s: str) -> str:
    s = s.strip("`").strip().lower()
    return re.sub(r"^v(\d)", r"\1", s)         # version sigil: `v1.2` == "version 1.2"


def facts_in(text: str) -> set[str]:
    body = _LISTMARK.sub("   ", text)
    out = set()
    for m in _NUMUNIT.finditer(body):
        unit = (m.group(2) or "").lower().rstrip("s")
        out.add(_norm_num(m.group(1)) + (" " + unit if unit else ""))   # count/unit mutations now fail
    for m in _CODEISH.findall(text):
        raw = m.strip("`").strip()
        if _PLAINNUM.fullmatch(raw):           # a bare number — _NUMUNIT owns it; but v1.2/0xFF/IDs survive
            continue
        if m.startswith("`") and raw.isalpha() and raw.islower():
            continue   # a single backticked plain word (`bump`, `seeds`) is emphasis, not a must-survive id —
            #            it legitimately becomes prose ("the stored bump") and must not read as a dropped fact
        f = _norm_code(m)
        if f:
            out.add(f)
    return {f for f in out if f}


# a fact like "0.002 sol" / "1232 byte" / "5000" — split into (value, unit) so we can pair a value change.
_NUMFACT = re.compile(r"^(0x[0-9a-f]+|\.\d+|\d[\d,]*(?:\.\d+)*)(?: (\w+))?$")


def _num_unit(f: str):
    m = _NUMFACT.match(f)
    return (m.group(1), (m.group(2) or "")) if m else None


def _is_mutation(dropped_fact: str, introduced: list[str]) -> bool:
    """A dropped sheet-fact is a MUTATION (the dangerous case), not a mere omission, when the styled output
    introduced a SIBLING: a number with the same non-empty unit but a CHANGED value (0.002 SOL -> 0.005 SOL),
    or a near-identical identifier (a swapped/typo'd name: transfer_checked -> transfer_unchecked). A faithful
    restyle that simply leaves a fact out, or paraphrases it, has no sibling -> advisory, never a hard fail.
    This makes the gate enforce fact-PRESERVATION, not verbatim transcription (the old set-difference hard-
    failed correct output the moment the fact-sheet listed more than the piece chose to assert)."""
    nd = _num_unit(dropped_fact)
    for i in introduced:
        ni = _num_unit(i)
        if nd and ni:
            (v, u), (v2, u2) = nd, ni
            if u and u == u2 and v != v2:                     # same unit, value changed (0.002 SOL -> 0.005 SOL)
                return True
            if u and u2 and u != u2 and v == v2:              # same value, unit changed (1232 bytes -> 1232 KB)
                return True
        elif not nd and not ni:                               # two identifiers -> swap if near-identical
            if difflib.SequenceMatcher(None, dropped_fact, i).ratio() >= 0.6:
                return True
    return False


def fact_diff(facts_sheet: str, styled: str) -> dict:
    a, c = facts_in(facts_sheet), facts_in(styled)
    dropped, introduced = sorted(a - c), sorted(c - a)
    mutated = [d for d in dropped if _is_mutation(d, introduced)]
    omitted = [d for d in dropped if d not in mutated]
    flags = []
    if mutated:                                               # the one HARD case: a value actually changed
        flags.append(f"HARD FAIL: {len(mutated)} verified fact(s) MUTATED by styling (value changed): {mutated}")
    if omitted:
        flags.append(f"advisory: {len(omitted)} sheet fact(s) absent from the output — confirm a deliberate "
                     f"omission/paraphrase, not a silent drop: {omitted}")
    if introduced:
        flags.append(f"advisory: {len(introduced)} number/identifier in the output but not the fact-sheet — "
                     f"confirm each is grounded, not invented: {introduced}")
    return {"facts_in_sheet": len(a), "facts_in_styled": len(c), "dropped": dropped, "introduced": introduced,
            "mutated": mutated, "omitted": omitted, "hard": bool(mutated),
            "flags": flags or ["ok: every verified fact survived styling"]}


# ── io + commands ──────────────────────────────────────────────────────────────
def _strip_meta(text: str) -> str:
    """Drop YAML frontmatter + HTML comments so the prose metrics see PROSE, not annotation.
    Exemplar files carry a `---` front-matter block and a trailing <!-- MOVE TRACE --> note;
    neither is the prose under test, and both are em-dash/arrow heavy — left in, they'd inflate
    the em-dash count and skew burstiness against the very canon the skill ships."""
    text = re.sub(r"\A﻿?\s*---\n.*?\n---[ \t]*\n", "", text, count=1, flags=re.S)  # leading YAML
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)                                   # HTML comments anywhere
    return text.strip()


def read_dir(path: str) -> list[str]:
    p = Path(path)
    out = [_strip_meta(fp.read_text("utf-8", "replace"))
           for fp in list(p.glob("*.md")) + list(p.glob("*.txt"))]
    return [t for t in out if t]


def read_one(path: str) -> str:
    p = Path(path)
    if not p.is_file():
        raise SystemExit(f"validate_voice: not a readable file: {path}")
    return _strip_meta(p.read_text("utf-8", "replace"))


def cmd_audit(a):
    if bool(a.lessons) == bool(getattr(a, "file", None)):
        LOG("audit: pass exactly one of --lessons <dir> (batch) or --file <doc> (intra-doc)"); return 2
    if getattr(a, "file", None):
        r = intra_doc_audit(read_one(a.file))
        print(f"Intra-doc repetition audit over {r['sections']} sections:")
        if "opener_histogram" in r:
            print(f"  opener types : {r['distinct_opener_types']}  {r['opener_histogram']}")
            print(f"  4-gram overlap: mean {r['mean_4gram_overlap']}  adjacent-max {r['adjacent_max_overlap']}")
        for f in r["flags"]:
            print("   - " + f)
        return 0
    lessons = read_dir(a.lessons)
    if not lessons:
        LOG(f"no lessons in {a.lessons}"); return 2
    r = repetition_audit(lessons)
    print(f"Repetition audit over {r['lessons']} lessons:")
    print(f"  opener types : {r['distinct_opener_types']}  {r['opener_histogram']}")
    print(f"  dup openings : {r['duplicate_opening_phrases']}")
    print(f"  4-gram overlap: {r['mean_pairwise_4gram_overlap']}")
    if r["transition_tics"]:
        print(f"  transition tics: {r['transition_tics']}")
    for f in r["flags"]:
        print("   - " + f)
    return 0


def cmd_density(a):
    text = read_one(a.file)
    markers = read_card_markers(a.markers) if a.markers else read_card_markers(a.card)
    if not markers:
        print("Marker density: no markers: block found (card pre-dates the markers schema; "
              "pass --markers <yaml>) — nothing to check")
        return 0
    gate_text = read_one(a.facts) if a.facts else None
    card = read_card_targets(a.card)
    r = marker_density(text, markers, gate_text)
    voice = f"voice={card['voice']}, " if card.get("voice") else ""
    print(f"Marker density ({voice}{r['words']} prose words, {r['sections']} sections):")
    print(f"  {'id':<24}{'class':<10}{'count':>5}{'budget':>7}  {'windows>cap':>11}  {'sections':<12}gate")
    for m in r["markers"]:
        secs = ",".join(map(str, m["sections_hit"])) or "-"
        print(f"  {m['id']:<24}{m['class']:<10}{m['count']:>5}{m['allowed']:>7}  "
              f"{m['windows_over_cap']:>11}  {secs:<12}{m['gate_status']}")
    n_adv = sum(1 for f in r["flags"] if "[advisory]" in f)
    for f in r["flags"]:
        print("   - " + f)
    if gate_text is None and any(m["gate_status"] == "UNCHECKED" for m in r["markers"]):
        print("   - note: gates UNCHECKED — pass --facts <fact-sheet> so gated markers can be checked")
    print(f"GATE: {'FAIL (hard)' if r['hard'] else 'PASS'}" + (f" — {n_adv} advisory" if n_adv else ""))
    return 1 if r["hard"] else 0


def _is_hard(flag: str) -> bool:
    """Only two things hard-fail the tells gate (see rules/deslop.md): a machine-paste fingerprint,
    and true uniform cadence (the burstiness floor). Banned words, em-dash, false-antithesis, and the
    gated deslop tiers are ADVISORY — surfaced for the writer to weigh, never an automatic regenerate.
    Sanding every flagged word out is itself what makes text read like AI."""
    return "uniform cadence" in flag or "machine-paste fingerprint" in flag


def cmd_tells(a):
    text = read_one(a.file)
    card = read_card_targets(a.card)
    r = ai_tell_lint(text, card)
    d = deslop_flags(text)
    voice = f"voice={r['voice']} " if r["voice"] else ""
    print(f"AI-tell lint ({voice}{r['words']} words; burstiness_min={r['burstiness_min']}): "
          f"stdev={r['sentence_stdev']} emdash/1k={r['emdash_per_1k']} false-antithesis={r['false_antithesis']}")
    n_adv = 0
    def show(flag):
        nonlocal n_adv
        if "ok:" in flag:
            print("   - " + flag)
        elif _is_hard(flag):
            print("   - [HARD] " + flag)
        else:
            n_adv += 1
            print("   - [advisory] " + flag)
    for f in r["flags"]:
        show(f)
    print("Deslop scan (gated tiers + structural; only machine-paste fingerprints are hard):")
    for f in d["flags"]:
        show(f)
    hard_fail = d["hard"] or any("uniform cadence" in f for f in r["flags"])
    print(f"GATE: {'FAIL (hard tell)' if hard_fail else 'PASS'}" + (f" — {n_adv} advisory" if n_adv else ""))
    return 1 if hard_fail else 0


def cmd_diff(a):
    r = fact_diff(read_one(a.facts), read_one(a.styled))
    print(f"Fact-preservation diff: {r['facts_in_sheet']} facts in sheet, "
          f"{r['facts_in_styled']} in styled output")
    for f in r["flags"]:
        print("   - " + f)
    return 1 if r["hard"] else 0   # hard-fail only on a real MUTATION; omissions/additions are advisory


def selftest() -> int:
    ok = True
    def check(c, m):
        nonlocal ok; print(("PASS" if c else "FAIL") + " - " + m); ok = ok and c

    rep = ["In today's fast-paced world, Solana is fast. " + ("detail " * 40)] * 6
    ar = repetition_audit(rep)
    check(ar["distinct_opener_types"] == 1, "repetitive batch -> 1 opener type")
    check(ar["duplicate_opening_phrases"] >= 5, "repetitive batch -> dup openings flagged")

    varied = ["Why do validators exist? " + " ".join(f"p{i} a" for i in range(40)),
              "Imagine a global clock. " + " ".join(f"b{i} c" for i in range(40)),
              "40% of fees burn. " + " ".join(f"g{i} f" for i in range(40)),
              "I once watched a halt. " + " ".join(f"d{i} h" for i in range(40)),
              "Stake replaces work here. " + " ".join(f"e{i} s" for i in range(40))]
    av = repetition_audit(varied)
    check(av["distinct_opener_types"] >= 4, "varied batch -> many opener types")

    # tells: catch delve + false-antithesis (>1 to exceed ≤1/800w cap) + uniform cadence
    bad = ("We delve into this. It's not a fee, it's a deposit. This is not slow, it's fast. "
           "Not hard, but easy. " + ("word word word word word. " * 8))
    rt = ai_tell_lint(bad)
    check(any("delve" in str(f) for f in rt["flags"]), "lint flags 'delve'")
    check(any("false-antithesis" in f for f in rt["flags"]), "lint flags repeated 'not X, it's Y'")
    single = "It's not a fee, it's a deposit. " + ("calm steady prose here for a while. " * 6)
    check(not any("false-antithesis" in f for f in ai_tell_lint(single)["flags"]),
          "a single 'not X, it's Y' is within cap (not flagged)")
    # the CONTRACTED form ("isn't X, it's Y") must be caught too — it's Kaue's real exemplar-01 form,
    # which the old \bnot\b regex silently missed; and 'cannot' must not false-match.
    contracted = ("This isn't regulation, it's a wall. These aren't shares, it's dilution. "
                  "It wasn't cheap, but worth it. " + ("calm steady prose here. " * 6))
    check(any("false-antithesis" in f for f in ai_tell_lint(contracted)["flags"]),
          "contracted 'isn't/aren't X, it's Y' is caught (was silently missed before)")
    check(not FALSE_ANTITHESIS_RE.search("I cannot, however, agree."), "'cannot' is not a false-match")

    # advisory-vs-hard gate (rules/deslop.md contract): ONLY fingerprints + uniform cadence hard-fail
    check(_is_hard("uniform cadence (sentence stdev 3.0 < card's 9) — reads even/AI"), "uniform cadence is HARD")
    check(_is_hard("machine-paste fingerprint: chatgpt-utm"), "machine-paste fingerprint is HARD")
    check(not _is_hard("banned AI-tell words (Tier-1, with swaps): {'leverage': \"use\"}"), "a banned word is advisory")
    check(not _is_hard("em-dash overuse (5x, 12.0/1k > 4)"), "em-dash overuse is advisory")
    check(not _is_hard("false-antithesis 'not X, it's Y' overused (3 > cap 2/800w)"), "false-antithesis is advisory")
    good = ("You stake SOL and the network mints fresh tokens. Short punch. Then a much longer, "
            "winding clause that runs on for a while to vary the rhythm and keep it human. Done.")
    check("ok:" in ai_tell_lint(good)["flags"][0] or len(ai_tell_lint(good)["flags"]) <= 1,
          "clean prose passes (or only minor)")

    # em-dash: rate-AND-count — one dash in a short passage is fine; many over the cap is the tell
    check(not any("em-dash" in f for f in ai_tell_lint("A short line — with one aside.")["flags"]),
          "single em-dash in short text is NOT flagged")
    check(any("em-dash" in f for f in ai_tell_lint("a — b — c — d — e — f. " * 3)["flags"]),
          "many em-dashes (count≥3 over the cap) flagged")
    check(any("em-dash" in f for f in ai_tell_lint("a -- b -- c -- d -- e. " * 2)["flags"]),
          "double-hyphen em-dash evasion is caught")

    # _strip_meta: prose metrics run on PROSE, not the front-matter / MOVE-TRACE annotation (dash/arrow heavy)
    meta_doc = "---\nslot: x\nsource: a — b — c\n---\nClean prose, no dash here at all.\n\n<!-- TRACE: x — y — z — w -->\n"
    sm = _strip_meta(meta_doc)
    check("slot:" not in sm and "TRACE" not in sm, "_strip_meta drops YAML frontmatter and HTML comments")
    check("—" not in sm, "_strip_meta leaves none of the annotation's em-dashes in the prose")
    check(not any("em-dash" in f for f in ai_tell_lint(sm)["flags"]),
          "stripped exemplar prose clears the em-dash gate (annotation no longer inflates the count)")

    # burstiness: HARD only when robotically even (stdev < 4); terse-but-varied below the voice target is
    # ADVISORY, not hard; short snippets/exemplars stay exempt; sub-250w robotic no longer slips through.
    uniform_long = "word word word word word. " * 60   # 300 words, stdev ≈ 0
    strict = {"burstiness_min": 9, "emdash_max": 4, "false_antithesis_cap": 1,
              "avoid_words": ["banana"], "avoid_connectives": []}
    rr = ai_tell_lint(uniform_long + " banana.", strict)
    check(any("uniform cadence" in f for f in rr["flags"]), "robotic-even text HARD-fails (uniform cadence)")
    check(any("banana" in str(f) for f in rr["flags"]), "card avoid_words enforced")
    robotic_short = "word word word word word word. " * 32   # ~192 words, 32 sentences, stdev ≈ 0
    check(any("uniform cadence" in f for f in ai_tell_lint(robotic_short)["flags"]),
          "sub-250w robotic text is now caught (the closed exemption hole)")
    s3, s13 = "alpha beta gamma. ", "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu. "
    terse = (s3 + s13) * 10                              # 160 words, 20 sentences, stdev 5.0 (4 < 5 < floor 9)
    tf = ai_tell_lint(terse)["flags"]
    check(not any("uniform cadence" in f for f in tf), "terse-but-varied text is NOT a HARD uniform-cadence fail")
    check(any("burstiness below the voice target" in f for f in tf), "...but it IS flagged ADVISORY (below floor)")
    check(not any("uniform" in f or "burstiness" in f for f in ai_tell_lint("word word word. " * 5, strict)["flags"]),
          "short snippet is EXEMPT from the burstiness check")

    # card reader parses the real kaue card (resolve relative to THIS file, not cwd)
    _card = Path(__file__).resolve().parent.parent / "profiles/kaue/kaue.card.yaml"
    kt = read_card_targets(str(_card))
    if kt["voice"] == "kaue":  # only assert when the card is reachable
        check(kt["burstiness_min"] == 9, "reads kaue burstiness_min=9 from card")
        check("delve" in kt["avoid_words"], "reads kaue avoid_words from card")
    # card parser survives a ']'-bearing token (no silent truncation)
    import tempfile, os
    ctxt = ('voice: t\navoid:\n  words: [delve, "x[0]", utilize, last]\n'
            '  connectives: ["Moreover,"]\nai_tells:\n')
    tf = os.path.join(tempfile.gettempdir(), "wsx_card_test.yaml"); open(tf, "w").write(ctxt)
    kc = read_card_targets(tf); os.remove(tf)
    check("last" in kc["avoid_words"] and "utilize" in kc["avoid_words"],
          "card avoid-list survives a ']'-bearing token")

    # deslop: gated tiers + fingerprints + markdown hygiene + Tier-1 swaps + hedge-stack
    soup = "We foster a nuanced approach to streamline the result and empower the team."
    check(any("Tier-2" in f for f in deslop_flags(soup)["flags"]),
          "tier-2 cluster flagged (≥3 distinct buzzwords in a paragraph)")
    check(not any("Tier-2" in f for f in deslop_flags("We foster and streamline this. Plain line. Done.")["flags"]),
          "two tier-2 words is NOT flagged (needs ≥3)")
    dense = "It is significant, innovative, scalable, robust, and compelling work overall."
    check(any("Tier-3" in f for f in deslop_flags(dense)["flags"]), "tier-3 density (≥3 distinct + ≥5/1k) flagged")
    check(not any("Tier-3" in f for f in deslop_flags("A robust retry loop.")["flags"]),
          "a single technical 'robust' is NOT flagged (density carve-out)")
    dfp = deslop_flags("More at example.com/?utm_source=chatgpt.com here.")
    check(dfp["hard"] and any("fingerprint" in f for f in dfp["flags"]), "machine-paste fingerprint = hard fail")
    check(not deslop_flags("We may eventually ship this feature.")["hard"], "modal+adverb is NOT a hard fingerprint")
    check(not deslop_flags("[date]: <> (2025/07/10)\n[title]: <> (My post)\n\nReal prose.")["hard"],
          "Markdown [date]: ref-link header is NOT a fingerprint (was a 168-file false positive)")
    check(deslop_flags("Published 2024-XX-XX by the team.")["hard"], "real 20XX-XX-XX template residue IS a fingerprint")
    check(any("hedging" in f for f in deslop_flags("This could potentially eventually work somehow.")["flags"]),
          "stacked hedges flagged (advisory, not hard)")
    md = "- **Intro:** hi\n- **Setup:** go\n- **Done:** end\n"
    check(any("inline-header" in f for f in deslop_flags(md)["flags"]), "inline-header bullet lists flagged")
    check("ok:" in deslop_flags("You stake SOL and the network mints tokens. Short. A longer clause to vary.")["flags"][0],
          "clean prose -> no deslop flags")
    # discourse-scaffolding tells of fluent bare-LLM output (the gap that bare ChatGPT/Claude prose trips):
    check(any("summary-restatement" in f for f in deslop_flags("PDAs are derived addresses. They have no key.\n\nIt does a lot. In summary, PDAs are a foundational building block.")["flags"]),
          "summary-restatement closer flagged")
    check(not any("summary-restatement" in f for f in deslop_flags("We shipped it.\n\nOverall it was a good week. Happy hacking!")["flags"]),
          "'Overall' sign-off is NOT a summary-restatement (human form)")
    check(any("meta-hedge" in f for f in deslop_flags("It's worth noting the cap. It's important to note the floor.")["flags"]),
          "meta-hedge pile-up flagged")
    check(not any("meta-hedge" in f or "summary" in f for f in deslop_flags("Keep in mind this is from an engineering view, but it applies broadly.")["flags"]),
          "'keep in mind' (a real Kaue-ism) does NOT fire the scaffolding tells")
    check(any("at its core" in f for f in deslop_flags("At its core it is a queue. Think of it as a ledger you append to.")["flags"]),
          "'at its core / think of it as' framing flagged")
    t1 = ai_tell_lint("Let's delve into this and leverage the result.")
    check(any("delve" in str(f) and "dig into" in str(f) for f in t1["flags"]), "Tier-1 flag surfaces the plain-word swap")

    # diff: mutations fail (number, unit, count, ALL-CAPS id); legit number styling does NOT false-fail
    facts = "Rent is 0.002 SOL. The tx limit is 1232 bytes. Program is transfer_checked."
    styled_ok = "It locks about 0.002 SOL, fits in 1232 bytes, and calls transfer_checked."
    styled_bad = "It locks about 0.005 SOL and fits in 1232 bytes."
    check(not fact_diff(facts, styled_ok)["dropped"], "faithful styling -> no dropped facts")
    # MUTATIONS (a value/identifier actually changed) — the only HARD case:
    check(fact_diff(facts, styled_bad)["hard"], "a mutated number (0.002->0.005 SOL) is a HARD fail")
    check(fact_diff("limit is 1232 bytes", "limit is 1232 KB")["hard"], "unit change bytes->KB is a hard mutation (1024x)")
    check(fact_diff("rent is 0.002 SOL", "rent is 0.002 ETH")["hard"], "ticker swap SOL->ETH (same number) is a hard mutation")
    check(fact_diff("owner is TOKEN_PROGRAM_ID", "owner is SYSTEM_PROGRAM_ID")["hard"], "SCREAMING_SNAKE id swap is a hard mutation")
    check(fact_diff("call Foo::bar today", "call Foo::baz today")["hard"], "Rust path Foo::bar->baz is a hard mutation")
    check(fact_diff("use transfer_checked", "use transfer_unchecked")["hard"], "near-identical identifier swap is a hard mutation")
    # OMISSIONS / PARAPHRASE / FALSE-POSITIVE GUARDS — must NOT hard-fail (the gate preserves facts, not transcription):
    check(not fact_diff("the CU cap", "the compute-unit cap")["hard"], "acronym expansion (CU) is not a mutation")
    check(not fact_diff("rent is 0.002 SOL", "rent is .002 SOL")["hard"], "leading-zero styling is not a mutation")
    check(not fact_diff("call `v1.2`", "call version 1.2")["hard"], "v1.2 == version 1.2 is not a mutation")
    check(not fact_diff("emit the ALT account", "emit the Address Lookup Table account")["hard"], "ALT->expansion is not a mutation")
    check(not fact_diff("store the `bump` here", "store the stored bump here")["hard"], "single backticked word -> prose is not a mutation")
    check(not fact_diff("call `Clock::get()` now", "then Clock::get() runs")["hard"], "backtick `Clock::get()` == bare Clock::get() (no false mutation)")
    bigsheet = "Rent 0.002 SOL. Tx 1232 bytes. 32 per pubkey. SIMD-0123. instruction.rs. CreateAccount, Transfer."
    sel = fact_diff(bigsheet, "A token account locks ~0.002 SOL of rent; close it to reclaim the lamports.")
    check(not sel["hard"] and sel["omitted"], "a faithful SELECTIVE lesson is advisory (omissions), never a hard fail")

    # markers: parsing + the density/gate policy (the calibration contract)
    mtxt = ('markers:\n'
            '  - id: latam-framing\n    class: identity\n'
            '    patterns: [latam, brazil, "emerging market"]\n'
            '    cap: 1\n    per_words: 0\n'
            '    gate: [latam, brazil, "emerging market"]\n'
            '  - id: game-changer\n    class: tic\n'
            '    patterns: ["game-changer", godsend]\n    cap: 1\n    per_words: 2500\n'
            '  - id: sign-off\n    class: signoff\n'
            '    patterns: ["happy building", lfb]\n    cap: 1\n    per_words: 0\n')
    mf = os.path.join(tempfile.gettempdir(), "wsx_markers_test.yaml"); open(mf, "w").write(mtxt)
    mks = read_card_markers(mf); os.remove(mf)
    check(len(mks) == 3 and mks[0]["id"] == "latam-framing" and mks[0]["gate"],
          "read_card_markers parses ids + bracket lists + gate")
    check(mks[1]["per_words"] == 2500 and mks[1]["cap"] == 1, "read_card_markers reads per_words budgets")
    check(read_card_markers(None) == [], "missing markers file -> [] (tolerant)")

    filler = "Plain sentence about fees goes here with several words. "
    tech = ("## Setup\n" + filler * 12 +
            "\n## Deep part\n" + filler * 12 + " This tool is such a godsend for brazil builders in LatAm.\n"
            "## Close\n" + filler * 12 + " Happy building! lfb")
    dm = marker_density(tech, mks, gate_text="How to set priority fees. Compute units. Simulation workflow.")
    lat = next(m for m in dm["markers"] if m["id"] == "latam-framing")
    sig = next(m for m in dm["markers"] if m["id"] == "sign-off")
    check(lat["count"] == 2 and lat["gate_status"] == "MISS" and lat["hard"],
          "identity marker + gate MISS -> HARD forced-insertion flag")
    check(sig["count"] == 2 and sig["hard"], "double sign-off over cap -> HARD")
    check(dm["hard"], "density result carries the hard fail")
    dm2 = marker_density(tech, mks, gate_text="stablecoin adoption across brazil and latam economies")
    lat2 = next(m for m in dm2["markers"] if m["id"] == "latam-framing")
    check(lat2["gate_status"] == "pass" and not lat2["hard"],
          "same text, gate keywords in facts -> identity over-budget is advisory, not hard")
    dm3 = marker_density(tech, mks)
    lat3 = next(m for m in dm3["markers"] if m["id"] == "latam-framing")
    check(lat3["gate_status"] == "UNCHECKED" and not lat3["hard"],
          "no --facts -> gate UNCHECKED, identity downgrades to advisory")
    clean = "## Setup\n" + filler * 12 + "\n## Close\n" + filler * 12 + " Happy building!"
    check(not marker_density(clean, mks, gate_text="fees only")["hard"],
          "one sign-off, zero identity hits -> density passes")

    # split_sections: intro naming + sub-50w merge
    ss = split_sections("intro words here " * 20 + "\n## A\n" + "aaa bbb ccc " * 20 +
                        "\n## Tiny\nfew words only\n## B\n" + "ddd eee fff " * 20)
    check(ss[0][0] == "(intro)" and len(ss) == 3, "split_sections: intro kept, <50w section merged into previous")

    # intra-doc audit: identical sections flagged, varied sections pass
    same_sec = "So here's the thing. " + "fee market detail words flow onward " * 12
    ia = intra_doc_audit("## S1\n" + same_sec + "\n## S2\n" + same_sec + "\n## S3\n" + same_sec)
    check(any("opening phrase" in f or "overlap" in f or "duplicate paragraph" in f for f in ia["flags"]),
          "identical sections -> intra-doc repetition flags fire")
    varied_doc = ("## S1\nWhy do fees exist? " + " ".join(f"alpha{i} beta{i}" for i in range(30)) +
                  "\n## S2\nImagine a queue forming. " + " ".join(f"gamma{i} delta{i}" for i in range(30)) +
                  "\n## S3\n40% of it burns. " + " ".join(f"eps{i} zeta{i}" for i in range(30)))
    check(intra_doc_audit(varied_doc)["flags"][0].startswith("ok:"),
          "varied sections -> no intra-doc flags")
    check(intra_doc_audit("one short paragraph only")["flags"][0].startswith("ok:"),
          "short single-section doc is exempt from the intra-doc audit")
    # warmth-side + machine checks added after R1 (temperature-unmeasured gap)
    qa_text = ("Does it cost you? Nope. Is it fast? Rent. Why bother at all? Half. "
               + "Calm filler sentence goes here to pad the passage nicely. " * 40)
    check(any("self-answered-question" in f for f in ai_tell_lint(qa_text)["flags"]),
          "Q?-punch-answer machine >1 is flagged")
    check(not any("self-answered-question" in f for f in ai_tell_lint(
        "Why bother? Rent. " + "Calm filler sentence goes here to pad things. " * 40)["flags"]),
          "a single Q?-punch-answer is fine (human rate)")
    clipped = {"burstiness_min": 9, "emdash_max": 4, "false_antithesis_cap": 2,
               "sentence_median": 18, "avoid_words": [], "avoid_connectives": [], "voice": "t"}
    short_doc = ("Fees rise fast. You pay more. It hurts a lot. Nobody enjoys that at all. "
                 "Set a limit now. Simulate the transaction first, then send it, then confirm it. ") * 12
    check(any("run short" in f for f in ai_tell_lint(short_doc, clipped)["flags"]),
          "clipped-sentence drift vs card median is flagged")
    vh = "## 200,000 is a default, not a plan\ntext here\n## It isn't the signer\nmore text\n"
    check(any("verdict-fragment headers" in f for f in ai_tell_lint(vh + ("calm words " * 60))["flags"]),
          "2+ antithesis headers flagged")

    # heading-glue must not mask real opener variety (agents found this: '## Title' glued to the body
    # made every headed section classify as 'claim', capping detectable variety at 2 types)
    headed = ("## A\nWhy do fees exist at all? " + " ".join(f"a{i} b{i}" for i in range(30)) +
              "\n## B\nImagine a queue forming fast. " + " ".join(f"c{i} d{i}" for i in range(30)) +
              "\n## C\n40% of it burns away. " + " ".join(f"e{i} f{i}" for i in range(30)) +
              "\n## D\nI once watched a leader stall. " + " ".join(f"g{i} h{i}" for i in range(30)))
    hv = intra_doc_audit(headed)
    check(hv["distinct_opener_types"] >= 3, "headed sections: opener classifier sees the PROSE opener, not '## Title'")

    print("\n" + ("VALIDATOR SELFTESTS PASSED" if ok else "FAILURES ABOVE"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="writer-style validator")
    sub = ap.add_subparsers(dest="cmd")
    pa = sub.add_parser("audit")
    pa.add_argument("--lessons", default=None, help="batch mode: a dir of lessons")
    pa.add_argument("--file", default=None, help="intra-doc mode: one long document")
    pt = sub.add_parser("tells"); pt.add_argument("--file", required=True)
    pt.add_argument("--card", default=None, help="<voice>.card.yaml — enforce per-voice targets")
    pn = sub.add_parser("density"); pn.add_argument("--file", required=True)
    pn.add_argument("--card", default=None, help="<voice>.card.yaml with a markers: block")
    pn.add_argument("--markers", default=None, help="standalone markers yaml (overrides the card's block)")
    pn.add_argument("--facts", default=None, help="the Pass-A fact-sheet — enables the context-gate check")
    pd = sub.add_parser("diff"); pd.add_argument("--facts", required=True); pd.add_argument("--styled", required=True)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.cmd == "audit":
        return cmd_audit(a)
    if a.cmd == "tells":
        return cmd_tells(a)
    if a.cmd == "density":
        return cmd_density(a)
    if a.cmd == "diff":
        return cmd_diff(a)
    ap.print_help(); return 1


if __name__ == "__main__":
    raise SystemExit(main())
