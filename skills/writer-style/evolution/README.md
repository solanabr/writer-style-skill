# Evolution engine — adversarial self-improvement for the writer-style skill

Maintainer-only infrastructure (never loaded by the writer; npm-excluded like `testbed/`). The engine
mass-produces content across **real-case containers** (X posts/threads, LinkedIn, blogs, course
lessons, video scripts, newsletters, community announcements), puts every piece in front of an
**adversarial judge panel**, aggregates panel takeaways through a **master board**, **empirically
tests** the surviving improvement candidates, and — only after a **human gate** — codifies them into
the pack/rules with a logged trail. Run it via `/evolve-voice`.

## How this differs from `/calibrate-voice`

| | Calibration (`testbed/`) | Evolution (this dir) |
|---|---|---|
| Question | *Does the output sound like the owner?* | *What should the skill change next?* |
| Judge | The owner (Kaue) rates every cell | Adversarial agent panels + blind A/B |
| Matrix | Fixed 8 briefs, frozen forever | Format-stress matrix (`briefs/`), extensible |
| Output | Card dials, marker caps, LESSONS.md | Rule/workflow/format-spec/lexicon candidates |
| Authority | Owner ratings are ground truth | Empirical win-rates propose; **human gate disposes** |

They share the mechanical layer (`tools/validate_voice.py`, `testbed/check_round.py --briefs
evolution/briefs`) and the governance spine: **marker caps and gates change ONLY through a logged
calibration round with owner ratings** — when an evolution round implicates a marker, the candidate
is routed to calibration, never adopted here.

## The loop (one round)

```
inputs refresh ──► generate (all briefs, parallel) ──► adversarial panels (3 lenses/piece, parallel)
                                                                │
   mechanical layer: tells · density · diff · audit · check_round (STAMP + batch twins + gates)
                                                                │
        DE-TWIN PASS (mandatory when check_round reports twins — writing-workflow.md batch mode)
                                                                │
                                     master board (N independent members ──► synthesis chair)
                                                                │
              slate: {compliance failures · empirical candidates · mechanical fixes ·
                      owner-taste questions · calibration-routed marker items}
                                                                │
        empirical tests: blind A/B probes per candidate · lexicon false-positive guard
                                                                │
                          HUMAN GATE (adopt / reject / defer, taste answers)
                                                                │
        codify (one mapped change per adoption) ──► EVOLUTION.md entry ──► hyperparams history
```

Every stage fans out in parallel; the only barriers are the board (needs all takeaways) and the gate
(needs a human).

## Files

- `hyperparams.yaml` — every tunable knob of the loop + an append-only `history:` of knob changes.
  Read it before running a round; change knobs only with a history entry.
- `briefs/` — the format-stress matrix. Same frontmatter schema as `testbed/briefs/` (so
  `check_round.py --briefs` runs unmodified). Fact-sheets are **imported frozen** from testbed
  briefs or this repo's rules — evolution rounds never re-derive facts, so round-over-round diffs
  isolate skill changes from research variance.
- `judges/` — lens charters (`slop-hunter`, `voice-fidelity`, `format-native`), the
  `master-board` charter, and the `blind-ab` protocol. Judge prompts are built FROM these files;
  edit the charter, not the prompt.
- `research/` — refreshed external evidence (deslop/humanization findings, platform norms). Judges
  cite it; candidates reference it.
- `rounds/` — working data (pieces, validator output, verdicts, reports). **Gitignored**; durable
  knowledge lives in `EVOLUTION.md`, `profiles/kaue/LESSONS.md`, and the codified diffs themselves.
- `EVOLUTION.md` — the append-only round ledger: what ran, what the board proposed, what the tests
  measured, what the human decided, what was codified where.

## Non-negotiables

1. **Facts frozen.** Generation is Pass B/C over imported fact-sheets. A mutated number is a round
   invalidator for that piece, not a style note.
2. **Compliance failure ≠ rule gap.** If a piece violates an *existing* rule, the fix is the
   generation workflow/prompting, never a new rule. Boards must classify before proposing — rule
   bloat is how skills rot.
3. **Empirical or it didn't happen.** No candidate is adopted on argument alone: prose candidates
   need blind A/B win-rate ≥ `empirical.adopt_threshold`; lexicon candidates must flag **zero**
   lines of `profiles/kaue/exemplars/kaue/` and `testbed/accepted/` (the false-positive guard —
   the author's own prose is the ground truth a tell-list must never fire on).
4. **The human gate is real.** Adoption, taste questions, and anything touching the owner's
   identity markers stop and ask. Present evidence, recommend, wait.
5. **Anti-over-correction.** Every round the board must answer: *did any prior adoption push output
   toward performed humanity?* (fake typos, quota'd seams, uniform quirkiness). De-adoption is a
   first-class candidate type.
6. **One mapped change per adoption**, same closed set as calibration
   (`{rule-edit, workflow-edit, format-spec-edit, lexicon-add, card-dial, exemplar-add/remove,
   themes-bank-entry}` — marker-cap/gate routes to calibration), logged in `EVOLUTION.md` as
   `- [RN][evidence] "quote/measurement" → change-type: what — file`.
