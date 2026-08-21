# Master board — charter

The board turns a round's raw evidence into a small slate of *testable* improvement candidates.
Members read everything, independently, through an assigned stance; a synthesis chair dedupes.
The board proposes; the empirical stage measures; the human gate disposes. The board never edits
skill files.

## Inputs (every member reads all of it)
1. All panel takeaways + scores (the round's verdicts file).
2. The mechanical layer: per-piece validator output, `check_round` results — STAMP table, batch
   twins, expect-block failures.
3. `evolution/research/deslop-2026-08.md` and the course-audit inventory.
4. `profiles/kaue/LESSONS.md` + `evolution/EVOLUTION.md` — what is already settled. A candidate
   that restates a codified lesson is a **compliance failure finding**, not a candidate.
5. `evolution/hyperparams.yaml` — the loop's own knobs are candidates too (panel composition,
   thresholds, matrix gaps).

## Stances (one per member — argue it, don't perform it)
- **detector**: what still clocks as AI, and what single change kills the most of it.
- **owner-advocate**: where output drifts from the owner's actual voice/interests; what he'd veto.
- **reader-advocate**: where pieces fail the audience (useless, padded, condescending, unclear) —
  slop-free but empty is still a failure.
- **minimalist**: which findings existing rules already cover (workflow fix, not rule fix); what
  to DELETE or merge; the cost of every added instruction (each rule dilutes attention on the rest).
- **contrarian**: which panel takeaways are wrong, over-fitted to one piece, or over-corrections
  that would push output toward performed humanity. Attack the round's own methodology too.

## Candidate contract (each member proposes ≤6, ranked by expected-impact × generality)
```yaml
- claim: one sentence — the defect and the change
  evidence: [piece-ids / STAMP lines / research citations / audit refs]
  class: compliance-failure | rule-gap | spec-bug | over-correction-repair | harness-gap
  type: rule-edit | workflow-edit | format-spec-edit | lexicon-add | card-dial |
        marker-change(route-to-calibration) | exemplar-gap | themes-gap | hyperparam-change
  proposed_diff: the concrete text/lines to add-change-remove (real words, not "improve X")
  test: how the empirical stage falsifies it (probe briefs + what a win looks like), or
        "mechanical" (lexicon guard), or "owner-taste" (goes to the human as a question)
  risk: what this could break — especially over-correction and rule-bloat
```

## Synthesis chair
Dedupe across members (same defect, different words = one candidate; keep the sharpest diff).
Split the slate into: **mechanical fixes** (objective, guard-tested) · **empirical candidates**
(≤ hyperparams `candidates_max`, ranked) · **owner-taste questions** (preference, not correctness
— phrase each as a direct either/or the operator can answer in seconds) · **calibration-routed**
(anything touching `markers:`) · **workflow fixes** (compliance failures — generation-side).
Record dissent: a stance that lost an argument gets one line saying why it lost.
