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

_(pending — owner rates each piece per RUBRIC.md; can be rated together with Round 1 via the blind A/B)_

### Changes

_(mapped from owner feedback after rating)_

---

## Round 1 — first post-redesign round

- date: 2026-07-02
- pack state: commit c20ba99 (markers gates + §5b + themes.md + expanded pools) + in-round fixes below
- generator: claude-fable-5, one writer subagent per brief, same neutral prompt as Round 0 (only the pack changed)
- outputs: `rounds/round-1/<brief-id>.md` + `<brief-id>.validator.txt`

### Mechanical summary — Round 0 → Round 1

| metric | Round 0 | Round 1 |
|---|---|---|
| hard fails | 0 | 0 |
| within-piece `expect:` | 8/8 PASS | 8/8 PASS |
| **sign-off stamp** | **"Happy building" 7/8** | rotated: cya 4 · what-a-time 2 · lfb 1 · **none 1** — residual: 'cya' 4/8 (see below) |
| **game-changer/godsend** | **5/8 pieces** | **0/8** — full pendulum swing (watch item: is a whole batch with zero too sterile? ~1/2500w is authentically him) |
| **latam-framing** | 2/8 — incl. **unearned** Superteam/Brazil in 08 (not in facts) | 2/8 — **both earned**: 02 (topic IS the region, substance) + 08 (exactly 1 beat, 1 section, "I live on one end of those corridors", gate keyword in facts) |
| identity gates decided | n/a (no gates existed) | 6× FAIL→0 markers (01/03/04/05/06/07) · 2× PASS→budgeted (02/08) — all 8 correct |
| themes.md substance used | n/a | 03: Arduino origin (A23) + theory-vs-practice + abandonment stances · 05: Goerli confession (A18) · no forced items reported |
| plainness quota | not tracked | ledgers report 3/8 plain sections (05), 2/8 (08); serious-register 04 ran marker-free end to end |

### Findings

1. **The gate architecture works.** All six pure-tech briefs got the fallback (reader's-own-numbers
   stakes) instead of a geography beat; 08's single beat is subtle and opportunity-framed. The failure
   mode Round 0 demonstrated (profile-sourced Superteam/Brazil with no basis in facts) did not recur.
2. **Residual stamp: 'cya' 4/8.** Parallel writers can't see each other's closer picks; each rotated off
   the burned "Happy building" and several landed on the same alternative. Proposed change (pending owner
   confirmation): seed the sign-off/verdict rotation by piece (e.g. rotate by brief position, or batch
   mode passes the previous piece's closer into the next writer's context).
3. **game-changer 0/8 is a possible over-correction** — the card's Round-0 stamp note may now read as a
   ban. Owner judgment wanted: if 0 feels sterile, soften the fallback note ("rotate", not "avoid").
4. Tool fixes shipped mid-round (all selftested): opener-classifier heading-glue artifact (agents found
   it — headings glued to section bodies capped detectable opener variety at 2 types); per-lexeme stamp
   metric (marker-family coverage could not distinguish "same token 7×" from "rotated"); hyphenated
   "emerging-market" added to latam patterns/gate (08's beat was invisible to density).

### Changes (codified this round — mechanical; owner-feedback changes pending rating)

- [R1][tooling] opener-variety advisory was structural noise on headed markdown → tool-fix: strip the glued heading before opener classification — `tools/validate_voice.py`
- [R1][tooling] stamp metric blind to per-lexeme domination → tool-fix: `pattern_hits` in density + per-lexeme coverage/stamp in `check_round.py`
- [R1][08-thesis] "emerging-market" (hyphenated) invisible to the identity marker → marker-cap/gate: pattern + gate keyword added — `kaue.card.yaml`
- [R1][cross-piece] 'cya' 4/8 residual stamp → **proposed** (unmapped until owner confirms): piece-seeded closer rotation for batch generation

### Owner rubric

_(pending — rate per RUBRIC.md)_

### Blind A/B — RESULTS (owner picked 2026-07-03, before unsealing)

Owner picked **B on all three**. Unblinded:

| brief | owner's pick | winner |
|---|---|---|
| 03-course-opener | B | **round-0 (OLD pack)** — new pack LOSS |
| 05-deepdive-svm-lifecycle | B | **round-1 (new pack)** — win |
| 08-thesis-ai-agents | B | **round-0 (OLD pack)** — new pack LOSS |

**Reading:** the new pack won the long-form compounder (where the redesign aimed) and lost the
course-opener + thesis cells. 2 losses = regression per protocol. n=1 rater, one critique given —
diagnosis delegated to the adversarial analysis session (2026-07-03) before any change is applied.

### Owner feedback (Round 1)

- **Critique:** the follow-up endings — "want me to do X up next?" — are wrong for course generation:
  the curriculum already exists, so a piece must not tease/ask about a next part that is already
  scheduled. (The sequel-teaser/comments-invite closers entered the rotation pool from the corpus
  mining — real Kaue moves from STANDALONE posts, misapplied to course context. Same error class as
  LATAM-in-tech: right move, wrong context.)

### Changes — PROPOSED, not applied (held for the joint analysis session)

- [R1][owner][closers] sequel-teaser / "part 2?" / comments-invite closers forced into course context →
  PROPOSED rule-edit + marker-gate: context-gate the closer family on "does a known curriculum/next
  lesson exist?" — course mode points to the actual next lesson or just closes; standalone posts keep
  the teaser family.
- [R1][owner][A/B] new pack lost 03 + 08 to the old pack → PROPOSED: hold all further restraint-side
  changes until the loss is diagnosed (hypotheses: over-sterilization — game-changer 0/8, energy delta,
  closer family — under adversarial analysis).
