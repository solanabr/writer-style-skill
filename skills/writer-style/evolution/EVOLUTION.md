# Evolution ledger — append-only round history

One entry per round: what ran, what the board proposed, what the tests measured, what the human
decided, what was codified where. Raw working data lives in `rounds/` (gitignored); this file is
the durable memory.

---

## Round 1 — 2026-08-20 · model: claude-fable-5 (generation, panels, board, probes)

**Scope.** First run of the engine, full 16-brief format matrix (x-post ×3, x-thread ×2, linkedin
×2, blog ×2, course-lesson ×2, video-script ×2, newsletter, community-announcement ×2), frozen
fact-sheets imported from the calibration testbed + repo rules. Inputs: fresh deslop research
(`research/deslop-2026-08.md`, incl. the Hassid template catalog, WP:AISIGNS era tiers, slop-score
regexes, PNAS grammar tells) + a full audit of the shipped btc-to-sol course corpus (81k words —
key finding: its tells are variable-slot templates repeated across the batch, invisible to n-gram
and lexicon checks).

**Scoreboard.** 16/16 pieces gate-green mechanically; 48-verdict panel (3 lenses × 16) mean ~3.9/5
(41 of 48 verdicts scored 4). The lexical war is won — zero era-tier vocabulary batch-wide. What
remains: contrast-frame monoculture (the lint saw ~15% of the family), fabricated first-person
receipts in 5 pieces (the seam mandate manufacturing counterfeit humanity under receipt
starvation), 12 cross-piece twin families shipped under a PASS (no de-twin phase existed), a
cold-tilted batch partly mismeasured by a broken warmth thermometer, and reader-model gaps
(known-fact posts in lead slots, buried lead facts).

**Board.** 5 stances (detector, owner-advocate, reader-advocate, minimalist, contrarian) →
synthesis chair: 8 empirical candidates, 7 mechanical fixes, 3 workflow fixes, 2 taste questions,
2 calibration-routed items, 9 dissents (mostly rejecting quota-fication: per-piece warmth floors,
hard cadence bands, pooled hard caps — all would re-create measured failure modes R2-03 / Rule 0).

**Empirical (blind A/B, 8 candidates × 2 probes × 3 votes = 48 votes).**
- `cand-lesson-contract` (course-lesson: fix-first time-to-value bound + method-claims-are-promises)
  — **6W-0L (1.00) → ADOPTED**, codified in `formats/course-lesson.md`.
- `cand-xpost-antithesis-license` (merge x-post's blanket antithesis ban with the card's budgeted
  license; scope the fail to payload-free mirrors) — **4W-2L (0.667) → ADOPTED**, codified in
  `formats/x-post.md`.
- `cand-receipt-provenance` — **0W-6L → rejected by blind preference**: judges structurally cannot
  see fabrication and consistently preferred fabricated lived-receipts over honest observation.
  The vote QUANTIFIES the warmth cost of integrity; fabrication is barred via the workflow fix
  below, and the UX question (placeholder vs silent degrade) went to the owner.
- Five candidates split 3W-3L with opposite unanimous probes (sheet-prose-restyle, thread-
  completion, audience-weighting, mood-job-license, scope-qualifiers) — each rule helped exactly
  where its defect showed and hurt elsewhere (e.g. scope-qualifiers fixed xp-02's "no Rust needed /
  Rust is hardest" self-contradiction but pushed jargon onto li-01's non-crypto audience).
  **Deferred to R2 with per-probe analyses**; refinement direction: add audience-translation and
  register clauses before re-probing.

**Codified this round** (`- [R1][evidence] change → file`):
- [R1][6-0 A/B sweep] lesson-contract: fix-first bound + method-claims-cashed → format-spec-edit —
  `formats/course-lesson.md`
- [R1][4-2 A/B] payload-free-mirror scoping of the antithesis fail, dealt-contrast license → 
  format-spec-edit — `formats/x-post.md`
- [R1][board W1; 12 twin families under PASS] de-twin pass as a mandatory batch phase + ≥3-piece
  twin gate (`FAIL(twins)`, `--allow-twins`) → workflow-edit + tool-fix — `writing-workflow.md`,
  `testbed/check_round.py`, `evolution/README.md`
- [R1][board W2; 5 fabricated receipts] attested-receipts annex: themes scan survives frozen
  sheets; first-person incidents only from annex/sheet/own-practice; batch deals different
  receipts → workflow-edit — `writing-workflow.md`
- [R1][board W3; bp-02 9/11 snap paragraphs] paragraph-close census in Pass B.5 → workflow-edit —
  `writing-workflow.md`
- [R1][course-audit B5 + panel ~20 vs lint 3] contrast-frame family pooled under the card's
  existing cap (6 variants, checkable-slot exemption) + announced-candor + manufactured-insider
  advisories → lexicon-add — `tools/style_lexicons.py`, `tools/validate_voice.py`. Guards: zero
  false positives on 16 exemplars + 8 accepted goldens; true-positives land on the panel-flagged
  spans (nl-01, xp-02, xt-01); selftests extended.
- [R1][every piece's diff noise] atomic `[PLACEHOLDER]` tokens + fact-sheet-section scoping +
  "absent (scope-cut?)" labeling → tool-fix — `tools/validate_voice.py`
- [R1][thermometer misread: 0 warm closers reported, ≥5 real] warmth telemetry fix + 
  `closer_family` expect key + zero-warm-batch advisory → tool-fix — `testbed/check_round.py`
- [R1][xp-02 shipped unpostable at 295/280 effective] t.co 23-char link budget in spec + effective-
  length gates for x-post/x-thread → format-spec-edit + tool-fix — `formats/x-post.md`,
  `testbed/check_round.py`
- [R1][user request mid-round] tone override + tone manifest (`tone[helius 0.8, hayes 0.2] · mood ·
  markers · route: auto|requested`) → workflow-edit — `SKILL.md`, `commands/write-in-voice.md`,
  `agents/voice-writer.md`; manifests observed flowing in probe regens same-day.

**Routed to calibration** (markers are owner-territory): any tightening of the false-antithesis
cap below 2/800w; whether batch-level marker/personality coverage gets a FLOOR (seed with the
owner's launch-warmth answer).

**R2 backlog** (board-specced, not yet implemented): closer-shape census in `audit` (snap-share
tables), batch lemma-tic detector with domain exemptions, round-harness gates (input manifest ·
words_target×6-vs-char-cap brief lint · spec-example topic-collision), the five split candidates
refined + re-probed, cross-repo: dedash.py syntactic-role replacement + nonzero em-dash policy for
the course pipeline.

**Harness lessons** (encoded in hyperparams history): probe count binds before vote count;
adopt_threshold precision (2/3 passes); course-audit must land before panels (input-manifest gate
specced); x-post briefs carried an impossible words_target (55w > 280 chars — brief lint specced);
`formats/newsletter.md`'s worked example shared the live brief's topic (regenerate on a foreign
topic — R2).

**Session-limit note.** Generation/panels/probes were cut by account session-limit windows three
times mid-round; all gaps were retried to completion (48/48 verdicts, 48/48 votes). Workflow
`args` did not deliver on this runtime — scripts now inline their data (research out_path defaulted
to scratchpad and was copied into the repo by hand).

**Human gate (2026-08-20, owner).** _(R1)_ (1) Both empirical adoptions KEPT. (2) Receipt no-fit policy:
HYBRID — `[RECEIPT — confirm: …]` placeholder (publish-blocking) on teaching/motivation pieces
where the receipt is load-bearing; silent degrade to practice/stance seams elsewhere; never
fabricate → codified `rules/facts-first.md` §7. (3) Launch-post warmth: BATCH-DEALT ~1/3 — the
coordinator deals the warm edge; cold launches stay licensed → codified `writing-workflow.md`
course/batch mode. (4) Round committed to `feat/voice-evolution-engine-20-08-2026`. (LESSONS.md
deliberately not extended — both rulings live in their binding homes; rule-bloat is the failure
mode the minimalist stance exists to stop.)

---

## Round 2 — 2026-08-21 · absorption round (owner-accepted courses as inspiration) · model: claude-fable-5

**Scope + owner steer.** Owner clarified the two shipped courses (btc-to-sol-evolution, 81k words;
solana-speedrun, 1.7k PT-BR prose words) are ITERATED AND ACCEPTED output — feed them as
inspiration, and explicitly: "avoid overfitting or giving them too much attention." Shape: 1
reframed speedrun audit + 3 miners (craft / voice / reclassification) + chair over btc-to-sol +
mechanical sweeps. No generation, no probes. ~1.5M tokens.

**Key findings.**
- *The frame is stable, the string is not*: the same tells re-emerge translated into PT
  ("aren't magic"→"Não é mágica"; "is the whole point"→"É pra isso que") — lexicons cannot catch
  this class; only positional/functional checks transfer. Markedness is language-relative (the PT
  cleft is near-neutral where the EN epigram is marked).
- *Acceptance has a visibility horizon*: per-lesson-visible patterns are licensed by review, but
  cross-lesson clones (the confession skeleton ×5, a superlative-ladder contradiction) are exactly
  what per-lesson review cannot see — so accepted-corpus guarding applies to HARD fails and
  lexicon bans only; advisory detectors stay free to fire (governance note in hyperparams).
- Two live tool bugs surfaced by the corpus: batch_twin_scan counted fenced-block boilerplate as
  prose (12/12 raw "twin families" on the corpus were fence noise), and Tier-1 "underscore" fired
  on literal Rust-identifier teaching.
- Contrast-frame family survived contact with ground truth unchanged (2-7 content-bearing hits
  per accepted lesson, all under the scaled cap).
- Process correction (honesty note): the first "collision sweep clean" claim was VACUOUS — a cwd
  drift made the tool path silently unresolvable; the real sweep ran 2026-08-21 post-fix.

**Codified (focus-filtered — contradiction fixes + bugs + one mechanism, nothing corpus-shaped):**
- [R2][14/14 accepted lessons violated the spec] closer contract redrawn: content-bridge to the
  ACTUAL next lesson licensed (accuracy-verified against the next brief); marketing energy,
  beyond-next teasing, comments-invites still banned; final lesson points outward → format-spec-edit
  — `formats/course-lesson.md`
- [R2][recap function lives in next-opener/checkpoints] no recap closers; series uniformity is
  measured at the SURFACE, not the beat → format-spec-edit — `formats/course-lesson.md`
- [R2][confession skeleton ×5, survives translation] seam shape-cloning line (type may ritualize,
  skeleton may not; the tell lives in the frame) → rule-edit — `rules/naturalness.md`
- [R2][12/12 fence-noise twins] `_prose_only()` fence/inline-code stripping in batch_twin_scan →
  tool-fix — `testbed/check_round.py`
- [R2][×2 FP on accepted Rust lesson] literal-identifier "underscore(s)" exemption (incl.
  hyphenated "leading-underscore") → tool-fix — `tools/validate_voice.py`
- [R2][R1 receipt starvation] durable owner-shipped substance into the bank: stances 26-27 +
  anecdotes A26-A27 (Superteam community cases + own-org receipts, identity-gated, numbers
  re-verify at use) → themes-bank-entry — `profiles/kaue/themes.md`
- [R2][guard governance] lexicon_guard scoped (hard/Tier-1 only; advisories exempt; PT-BR
  tokenizer caveat) → hyperparam-change — `hyperparams.yaml`

**Parked (anti-overfit — n=1 corpus; revisit only with a second corroborating course or owner
appetite):** machine-drafted exemplar adoption (5 candidates with payloads in rounds/r2/slate.json);
confession-anecdote biography confirmation for themes.md; course-register card overlay (zero
exclamation/emoji/verdict-tokens, aphorism-pair verdicts); kaue.md move-set + "Tuesday"/"wearing-X"
marker minting; formats/course-series.md; the full course-lesson enrichment set (two-gate
checkpoints, fading tiers, code-register block); all 16 detector-decision rescopes for unbuilt
detectors (thresholds recorded in slate.json).

**Cross-repo handoff** (course-creator-skill's bugs, not ours): rounds/r2/HANDOFF-course-creator.md
— quiz-layer em-dash hole (97 shipped), dedash comma-splice mapping, cover template leakage,
mandatory fact-check pass, fanout dialect normalization, incomplete-fix sweeps, audience-model
contradiction.

**PT-BR note.** The toolchain is English-calibrated (WORD_RE splits accented tokens; contrast
regexes are EN-shaped). Multilingual support = separate project, not incremental tuning; logged,
not attempted.
