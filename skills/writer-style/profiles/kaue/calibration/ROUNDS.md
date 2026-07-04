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

---

## Round 2 — auto-mode round 1 (coordinator palettes + fresh-eyes revisers)

- date: 2026-07-03 · pack state: b29eec6 + 10d9bc5 · generator: claude-fable-5 via workflow
- judging: 30 blind pairwise judges (3 lenses × 10 cells; 1 failed on 529) + batch forensics; mapping was sealed until scoring

### Panel results (majority of 3)

| cell | vs | winner | votes |
|---|---|---|---|
| 01 how-to | R1 | **R2** | 2-1 |
| 02 macro | R1 | R1 | 2-1 |
| 03 course-opener | R1 | R1 | 3-0 |
| 04 security | R1 | R1 | 3-0 |
| 05 deep-dive | R1 | tie | 1-1 (1 judge 529'd) |
| 06 short | R1 | **R2** | 2-1 |
| 07 tutorial (course-mid) | R1 | **R2** | 3-0 |
| 08 thesis | R1 | **R2** | 3-0 |
| **03 vs ROUND-0 (owner's pick)** | R0 | **R2** | 2-1 |
| **08 vs ROUND-0 (owner's pick)** | R0 | **R2** | 3-0 |

**The regression the owner flagged is recovered**: R2 beats both old-pack pieces he preferred. vs R1: 4/8 (mixed → one targeted round per decision rules).

### Loss diagnosis (unanimous across losing cells' judges)
Every R1-win cited the same thing about R2: "epigram-per-paragraph cadence… designer-tidy… ornamental aphorism" + missing lived receipts. R2-03 mandated warmth ("You've got this\!", ≥2 exclamations) WITHOUT a lived receipt → judges called it performed; R1-03's Arduino/borrow-checker receipts won. **Mandated warmth reads performed; receipts generate real warmth. Stripped markers get replaced by essayist polish — the model's default filler.**

### Forensics (R1 → R2)
improved: closing choreography 8/8→~3/8 (6 distinct endings) · 'Here's' 22→2 · QA-machine 9→6 · punch metronome 43/45→28/47 sections (clumped) · sentence means 13.6-17.1→16.3-24.5 · sign-off tokens 7/8→2/8.
worse: cross-piece phrase stamping 2→5+ ("The silver bullet?" ×2 — coordinator palette error; "I'll admit my bias" ×2; "I'd rather hand you" ×2; godsend 4/8 single-lexeme). NEW tell: labeled domestic aside ("Complete aside: …chipped mug") 4/8 — the aside license became a template. Confession beat still 8/8.

### Changes (applied for R3)
- [R2][all-losses] epigram density → rule: paragraph-final snapped-shut lines ≤1/500w; two consecutive = unsnap one — LESSONS 7 + reviser mandate
- [R2][c03] mandated warmth without receipt → EVERY piece carries ≥1 concrete first-person lived receipt; warmth mandates removed — LESSONS 2
- [R2][forensics] phrase stamping → coordinator deals EXCLUSIVE distinctive constructions + specific tokens (godsend ≤2/batch, silver-bullet 1 owner) — LESSONS 3/6
- [R2][forensics] domestic-aside template → aside license: never labeled, ≤2/batch, coordinator-dealt, flavors must differ — naturalness rule 3 + LESSONS 10
- [R2][forensics] confession 8/8 → confession-flavored seams ≤5/batch, dealt

---

## Round 3 — auto-mode round 2 (receipts mandatory, anti-epigram, exclusive constructions)

- date: 2026-07-03 · pack state: 6507238 + f8209cd · 33 blind judges + forensics, mapping sealed until scoring

### Panel results (majority of 3)

**vs Round 2: 8-0 SWEEP** — d01 3-0 · d02 3-0 · d03 3-0 · d04 3-0 · d05 2-1 · d06 3-0 · d07 3-0 · d08 3-0.
**vs Round 1 on R2's lost cells: all three FLIPPED** — 02: 2-1 · 03: 3-0 (all-high) · 04: 3-0.
Judges' recurring reason for R3: lived receipts with real numbers ("118k simulated vs 600k billed",
"ten days, a few hundred dollars", Arduino/guitar, "153/80/73 bounty queue") + loose comma-chained runs;
recurring reason against R2: "epigram-per-paragraph… designer-tidy… performed cheerleading".

### Forensics (R2 → R3)
improved: sentence means 16.3-24.5 → **20.6-34.9 (fully inside corpus band)** · punch metronome 28/47 →
~10/47 · labeled asides 4/8 → 0 · old phrase-twins purged (silver-bullet/price-of-admission/I'd-rather = 0) ·
exclamations 8→6 · godsend/game-changer 4/0 → 2/1.
flat: choreography 3/8 · QA-fragments 6→7 · confession 7/8.
worse: "Here's" 2→4 · **NEW: within-batch phrase twinning** — ≥8 fresh collocations minted twice in one
batch ("honestly a godsend" 07+08, "earns its keep" 02+07, "sit with it for a second" 02+05, the verbatim
base-fee sentence frame ×3…). Writers dedupe against history, not against sibling pieces.
**Dominant remaining tell: paragraph-final epigram closers ~4.9/piece (39 total)** — reduced in judged
salience (R3 won anyway) but structurally unchanged; prompts+reviser dented, didn't break.

### Decision
Improvement decisive (11/11 cells) → not stagnant. **Round 4 = surgical de-tell EDIT pass on the R3
pieces** (no regeneration — protect the sweep): epigram budget ≤2/piece, de-twin with explicit keep/lose
assignments, "Here's" ≤1/piece, QA-fragments ≤1/piece; facts untouchable; then a confirmation panel
R4-vs-R3. R4 wins/ties → final; loses → revert to R3 (stagnation reached at a winning state).

---

## Round 4 — surgical de-tell polish + confirmation panel → STAGNATION REACHED (program concluded)

- date: 2026-07-04 · R4 = bounded edits on R3 pieces (epigram ≤2/piece, de-twin, trims); facts verified intact post-edit
- panel: 9/21 judges completed (monthly spend limit killed 12 + forensics mid-panel, second occurrence)

### What the 9 verdicts showed — the Pareto frontier

- e03: **R4 wins 3-0** (the single unsnap — "click on and poke at" vs an appended didactic epigram — improved ALL lenses) → cherry-picked into accepted/.
- e01: R3 2-0 — but caused by an **editor overreach bug**: the editor cut "game-changer" as "slop" when it was the piece's DEALT token; owner+fidelity judges correctly called it "the author's genuine tic… sterile restraint."
- e02: R3 2-1, e04: 1-1 — **split along lens lines**: owner/fidelity defend the warm quotable lines; detector wants them flattened. Line-level edits now trade one lens's approval for another's 1:1.

**Stagnation call (per the owner's stopping rule):** R3→R4 editing has hit the trade-off zone — further
"de-telling" costs warmth at parity. The epigram lesson refined: the tell is UNIFORMITY (every paragraph
snapping shut), not existence — R3's level (a few warm, load-bearing snaps; never two consecutive; most
paragraphs ending plain) is the measured optimum.

### FINAL STATE

- **`rounds/accepted/` = the golden outputs**: Round-3 pieces + Round-4's 03 (the 3-0 cell). The permanent
  Tier-1 regression arm (`check_round.py --round rounds/accepted`).
- **The deliverable is the pack + pipeline as of commit b351f2b**: markers gates + §5b (identity: 8/8 correct
  decisions since R1), themes.md substance bank (receipts = the #1 measured win driver), LESSONS.md feedback
  channel, coordinator palettes + fresh-eyes reviser + de-twin scan, warmth telemetry.
- **Program trajectory**: R0 baseline (validator green, owner unhappy) → R1 (gates work, temperature lost;
  owner A/B: lost 2/3 to R0) → R2 (recovered both owner cells vs R0; 4/8 vs R1) → **R3 (8-0 sweep vs R2, all
  R1 losses flipped, sentence rhythm inside corpus band)** → R4 (Pareto frontier found; stagnation declared).
- Open for the owner: read `accepted/`; future rounds are one `/calibrate-voice` away when the spend limit
  resets; his ratings remain the ultimate arbiter above all judge panels.
