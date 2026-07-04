---
description: "Run an empirical calibration round: regenerate the 8-brief matrix, measure, collect owner ratings, codify every reaction into a logged pack change"
---

Run one calibration round of the writer-style pack against the fixed test matrix. The loop: **measure →
owner rates → codify → apply → re-measure.** Protocol details: `the calibration protocol (local, gitignored: profiles/kaue/calibration/)`;
matrix + briefs: `$SKILL/testbed/MATRIX.md`; ledger: `profiles/kaue/calibration/ROUNDS.md (local, gitignored)`.

```bash
SKILL="${CLAUDE_PLUGIN_ROOT:+$CLAUDE_PLUGIN_ROOT/skills/writer-style}"
[ -d "$SKILL" ] || SKILL=".claude/skills/writer-style"; [ -d "$SKILL" ] || SKILL="skills/writer-style"
```

## The round (N = next round number in ROUNDS.md)

1. **Regenerate the FULL matrix** — all 8 briefs, one voice-writer run each, into
   `$SKILL/profiles/kaue/calibration/rounds/round-N/<brief-id>.md`. Never partial: repetition is
   emergent; regenerating 3 of 8 hides interactions. Each brief's fact-sheet is FROZEN — Pass B/C only,
   no research. Record the generation model in ROUNDS.md (keep it constant across rounds).
2. **Measure**: per piece, capture `tells` + `density --facts <brief>` + `audit --file` + `diff` output to
   `<brief-id>.validator.txt`, then run the mechanical gate:
   ```bash
   python3 "$SKILL/testbed/check_round.py" --round "$SKILL/profiles/kaue/calibration/rounds/round-N" \
     --card "$SKILL/profiles/kaue/kaue.card.yaml"
   ```
   Append the summary (incl. the cross-piece marker coverage — the STAMP table) to ROUNDS.md.
3. **Owner rates** each piece conversationally; structure the reactions into the RUBRIC.md yaml blocks
   (voice_fit, naturalness, forced_insertions with verbatim quotes, repetitions_noticed, publish y/n).
4. **Blind A/B** on 2-3 briefs (always include the worst-rated baseline cell): frozen Round-0 output vs
   round-N output, shuffled labels; owner picks; record the unblinded mapping AFTER the pick. A new-pack
   loss = regression → must get a mapped change.
5. **Codify** — every feedback item maps to exactly ONE change from the closed set
   `{card-dial, marker-cap/gate, rule-edit, exemplar-add/remove, themes-bank-entry}`, appended to the
   round's Changes list (`- [RN][brief] "quote" → change-type: what — file`). Unmappable feedback logs as
   `unmapped` (a design-gap signal to discuss). Apply confirmed changes to the pack.
6. **Converged?** Check the RUBRIC.md criteria (voice_fit/naturalness ≥4 everywhere, zero forced
   insertions, publish ≥7/8, validator green, A/B new-or-tie — for 2 consecutive rounds). When met:
   promote owner-confirmed tic caps to `enforce: hard` in the card, freeze the accepted round as
   `testbed/accepted/ (in-repo golden outputs)`, and the matrix becomes the permanent regression gate (re-run
   check_round on any pack/tool change).

Round 0 (the pre-redesign baseline) is frozen forever — it is the A/B "old pack" arm and the proof line.
