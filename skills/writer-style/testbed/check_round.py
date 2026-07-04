#!/usr/bin/env python3
"""
check_round.py — mechanical regression runner over one calibration round.

Loads every brief in testbed/briefs/, finds the round's piece for each, runs the
validator suite (density with the brief as gate source, tells+deslop, fact diff),
and asserts the brief's `expect:` block. Also prints cross-piece marker coverage —
the "stamp" metric (a marker appearing in nearly every piece is the portfolio-level
repetition the per-piece caps can't see; Round 0 baseline: sign-off in 7/8 pieces).

    python3 check_round.py --round <round-dir> --card <voice>.card.yaml [--markers <yaml>] [--briefs <dir>]

Exit 1 on any expectation violation or hard validator failure. Pure Python, no deps.
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL / "tools"))

from validate_voice import (read_card_markers, read_card_targets, marker_density,   # noqa: E402
                            ai_tell_lint, deslop_flags, fact_diff, intra_doc_audit,
                            read_one, _strip_meta, WORD_RE)


def batch_twin_scan(texts: dict) -> list:
    """Within-batch phrase twinning: distinctive word 4-grams shared by >=2 pieces of ONE batch.
    R3 forensics found writers dedupe coinages against history but not against sibling pieces —
    >=8 fresh collocations minted twice in a single batch. Filter: no digits, >=2 words of >=5
    chars (drops function-word scaffolding); shared by 2-3 pieces (4+ = domain vocabulary)."""
    grams = {}
    for pid, text in texts.items():
        words = [w for w in WORD_RE.findall(text.lower())]
        seen = set()
        for i in range(len(words) - 3):
            g = tuple(words[i:i + 4])
            if any(any(ch.isdigit() for ch in w) for w in g):
                continue
            if sum(1 for w in g if len(w) >= 5) < 2:
                continue
            seen.add(g)
        for g in seen:
            grams.setdefault(g, []).append(pid)
    twins = [(g, pids) for g, pids in grams.items() if 2 <= len(pids) <= 3]
    twins.sort(key=lambda t: (-len(t[1]), t[0]))
    return twins[:12]


def load_brief(path: Path) -> dict:
    raw = path.read_text("utf-8", "replace")
    m = re.match(r"\A﻿?\s*---\n(.*?)\n---", raw, re.S)
    fm = m.group(1) if m else ""
    brief: dict = {"path": path, "expect": {}}
    for key in ("id", "title", "words_target", "dominant_job", "route_expected"):
        km = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
        if km:
            brief[key] = km.group(1).strip().strip('"')
    em = re.search(r"^expect:\s*\n((?:[ \t]+\S.*\n?)*)", fm, re.M)
    if em:
        for line in em.group(1).splitlines():
            lm = re.match(r"\s+([\w][\w-]*(?:_max|_sections_max)?):\s*(\S+)", line)
            if lm:
                k, v = lm.group(1), lm.group(2)
                brief["expect"][k] = int(v) if v.isdigit() else v
    brief["body"] = _strip_meta(raw)   # brief prose + FROZEN fact-sheet = the gate source
    return brief


def check_piece(brief: dict, piece_path: Path, markers: list[dict], card: dict) -> dict:
    text = read_one(str(piece_path))
    dens = marker_density(text, markers, gate_text=brief["body"])
    tl = ai_tell_lint(text, card)
    ds = deslop_flags(text)
    fd = fact_diff(brief["body"], text)
    cadence_hard = any("uniform cadence" in f for f in tl["flags"])
    hard = dens["hard"] or ds["hard"] or fd["hard"] or cadence_hard
    counts = {m["id"]: m for m in dens["markers"]}
    fails, notes = [], []
    for k, v in brief["expect"].items():
        if k == "hard_fails":
            if hard and v == 0:
                srcs = [s for s, h in (("density", dens["hard"]), ("deslop", ds["hard"]),
                                       ("fact-diff", fd["hard"]), ("cadence", cadence_hard)) if h]
                fails.append(f"hard_fails: expected 0, got hard ({'+'.join(srcs)})")
            continue
        if v == "allow":
            notes.append(f"{k}: allow (human-rated cell)")
            continue
        if k.endswith("_sections_max"):
            mid = k[: -len("_sections_max")]
            got = len(counts.get(mid, {}).get("sections_hit", []))
            if got > int(v):
                fails.append(f"{k}: marker in {got} sections > max {v}")
        elif k.endswith("_max"):
            mid = k[: -len("_max")]
            got = counts.get(mid, {}).get("count", 0)
            if got > int(v):
                fails.append(f"{k}: count {got} > max {v}")
        else:
            got = counts.get(k, {}).get("count", 0)
            if got != int(v):
                fails.append(f"{k}: count {got} != {v}")
    advisories = sum(1 for f in dens["flags"] + tl["flags"] + ds["flags"]
                     if not f.startswith("ok:") and "[HARD]" not in f and "HARD" not in f)
    # warmth telemetry (the R1 gap: restraint was measured, temperature wasn't)
    excl_per_1k = round(1000 * text.count("!") / max(1, dens["words"]), 1)
    tail = text[-300:].lower()
    warm = any(t in tail for t in ("happy ", "you've got this", "you got this", "keep build",
                                   "keep shipping", "🚀", "not that hard"))
    cool = any(t in tail for t in ("cya", "lfb", "see you on the next one", "what a time to be alive"))
    closer_family = "warm" if warm else ("cool" if cool else "plain")
    return {"fails": fails, "notes": notes, "hard": hard, "advisories": advisories,
            "marker_counts": {m["id"]: m["count"] for m in dens["markers"]},
            "marker_lexemes": {m["id"]: m["pattern_hits"] for m in dens["markers"] if m["pattern_hits"]},
            "excl_per_1k": excl_per_1k, "closer_family": closer_family,
            "words": dens["words"]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="calibration round regression runner")
    ap.add_argument("--round", required=True, help="round dir with <brief-id>.md pieces")
    ap.add_argument("--card", required=True, help="<voice>.card.yaml (tells targets + markers block)")
    ap.add_argument("--markers", default=None, help="standalone markers yaml (overrides the card's block)")
    ap.add_argument("--briefs", default=str(SKILL / "testbed" / "briefs"))
    a = ap.parse_args(argv)
    markers = read_card_markers(a.markers) if a.markers else read_card_markers(a.card)
    if not markers:
        print("check_round: no markers definition — pass --markers or a card with a markers: block")
        return 2
    card = read_card_targets(a.card)
    briefs = sorted(Path(a.briefs).glob("*.md"))
    if not briefs:
        print(f"check_round: no briefs in {a.briefs}")
        return 2
    rdir = Path(a.round)
    rows, any_fail, portfolio, n_pieces = [], False, {}, 0
    piece_texts = {}
    for bp in briefs:
        b = load_brief(bp)
        piece = rdir / f"{b.get('id', bp.stem)}.md"
        if piece.is_file():
            piece_texts[b.get("id", bp.stem)] = read_one(str(piece))
        if not piece.is_file():
            rows.append((b.get("id", bp.stem), "MISSING", ["piece file not found"]))
            any_fail = True
            continue
        r = check_piece(b, piece, markers, card)
        n_pieces += 1
        for mid, c in r["marker_counts"].items():
            if c > 0:
                portfolio.setdefault(mid, {"pieces": 0, "lexemes": {}})
                portfolio[mid]["pieces"] += 1
                for lex in r["marker_lexemes"].get(mid, {}):
                    lx = portfolio[mid]["lexemes"]
                    lx[lex] = lx.get(lex, 0) + 1   # pieces containing this lexeme
        status = "FAIL" if r["fails"] else "PASS"
        any_fail = any_fail or bool(r["fails"])
        detail = r["fails"] + r["notes"] + [
            f"{r['words']}w, {r['advisories']} advisory · warmth: {r['excl_per_1k']} excl/1k, closer={r['closer_family']}"]
        rows.append((b.get("id", bp.stem), status, detail))
    print(f"check_round: {a.round}  ({len(rows)} briefs)")
    for bid, st, det in rows:
        print(f"  [{st}] {bid}")
        for d in det:
            print(f"        - {d}")
    if portfolio and n_pieces:
        print("  cross-piece marker coverage (pieces containing each marker; the STAMP is a single")
        print("  lexeme dominating, not the marker family being present):")
        for mid, d in sorted(portfolio.items(), key=lambda kv: -kv[1]["pieces"]):
            c = d["pieces"]
            lex = sorted(d["lexemes"].items(), key=lambda kv: -kv[1])
            top = lex[0] if lex else ("", 0)
            stamp = f"   <- STAMP: '{top[0]}' in {top[1]}/{n_pieces} pieces — rotate it" \
                if top[1] >= max(3, round(0.5 * n_pieces)) else ""
            breakdown = ", ".join(f"{l} {n}" for l, n in lex[:4])
            print(f"        {mid}: {c}/{n_pieces} ({breakdown}){stamp}")
    if len(piece_texts) >= 2:
        twins = batch_twin_scan(piece_texts)
        if twins:
            print("  within-batch phrase twins (distinctive 4-grams shared by sibling pieces — de-twin these):")
            for g, pids in twins:
                print(f"        \"{' '.join(g)}\" — {','.join(pids)}")
    if n_pieces and "game-changer" not in portfolio:
        print("  [advisory] verdict-token budget UNSPENT across the whole batch — a cap is not a ban "
              "(~1/2500w is the voice); zero everywhere reads sterile (R1 finding)")
    print("RESULT: " + ("FAIL" if any_fail else "PASS"))
    return 1 if any_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
