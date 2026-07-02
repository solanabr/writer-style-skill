# Calibration ledger — kaue pack

Append-only. One block per round: mechanical summary → owner rubric blocks → mapped changes.
Format + codification rule: `RUBRIC.md`. Matrix + briefs: `../../../testbed/MATRIX.md`.

---

## Round 0 — baseline (current pack, pre-redesign)

- date: 2026-07-02
- pack state: commit 37f4941 (pre-redesign — LATAM uncapped in favor.moves, no markers: block)
- generator: claude-fable-5, one writer subagent per brief following the skill verbatim
- facts: frozen per-brief fact-sheets in testbed/briefs/ (verified 2026-07-02 vs solana-dev MCP)
- outputs: `rounds/round-0/<brief-id>.md` + `<brief-id>.validator.txt`

### Mechanical summary

`check_round.py --round rounds/round-0 --markers testbed/draft-markers.yaml`: all 8 briefs PASS
within-piece expectations; 0 hard fails. Per-piece validator output: `rounds/round-0/*.validator.txt`.

**The portfolio-level stamp (the headline finding):**

| marker | pieces containing it | verdict |
|---|---|---|
| sign-off ("Happy building" family) | **7/8** | STAMP — every piece closes the same way; rotation pools exist in index.yaml but are never used |
| game-changer/godsend | **5/8** | STAMP — within-piece cap holds, portfolio loops it |
| latam-framing | 2/8 | contextually correct this run (02 topic-legit; 08 boundary) |

**Within-piece:** the worst-case forced insertion ("this is latam" in a pure-tech piece) did NOT
reproduce in this run — 0 identity lexemes in briefs 01/03/04/05/06/07. But brief 08 shows the
mechanism live: **"Superteam" and "Brazil" appear in the piece though neither is in the fact-sheet**
(facts say only "emerging markets") — the writer pulled them from the voice profile. Flagged
advisory: `latam-framing 2x vs budget 1`. Brief 02 (topic-legit): latam lexemes 10x across 4/6
sections — "themed through the piece" advisory for the owner to judge saturation vs substance.

**Interpretation:** the repetition problem is primarily CROSS-PIECE (the stamp), the forced-insertion
problem is REAL but stochastic (08 reproduced it mildly; the owner hit it harder in real usage,
plausibly on briefs without frozen fact-sheets). Both now have mechanical detectors. Current
validator (tells/diff) passed everything — the measurement gap is confirmed.

- generation model: claude-fable-5 (record for round-over-round consistency)
- routes taken: 01 helius · 02 hayes+helius · 03 primary-only · 04 helius+vitalik · 05 vitalik+helius · 06 helius · 07 helius · 08 balaji+helius

### Owner rubric

_(pending — owner rates each piece per RUBRIC.md)_

### Changes

_(mapped from owner feedback after rating)_
