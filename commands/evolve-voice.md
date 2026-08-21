---
description: "Run one evolution round: mass-generate the format matrix, adversarial judge panels, master board, empirical A/B tests, human gate, codify. The self-improvement loop for the skill itself."
---

Run one round of the evolution engine (`$SKILL/evolution/` — read its `README.md` first; it holds
the loop diagram and the non-negotiables). This command is the orchestration procedure; all knobs
live in `evolution/hyperparams.yaml` — **read it before every round, change it only with a
`history:` entry**.

```bash
SKILL="${CLAUDE_PLUGIN_ROOT:+$CLAUDE_PLUGIN_ROOT/skills/writer-style}"
[ -d "$SKILL" ] || SKILL=".claude/skills/writer-style"; [ -d "$SKILL" ] || SKILL="skills/writer-style"
EVO="$SKILL/evolution"; ROUND="$EVO/rounds/r<N>"   # N = round_next from hyperparams.yaml
```

## 0. Preflight (sequential, cheap)
Read: `evolution/hyperparams.yaml` · `evolution/EVOLUTION.md` (what previous rounds already
decided — never re-propose settled items) · `profiles/kaue/LESSONS.md` · the freshest file in
`evolution/research/`. If the research file is >90 days old, or the round's focus shifted
platforms, refresh it first (parallel researcher agents by modality: practitioner / measurement /
mechanism / platform-norms → one synthesizer; see the research file's own header for the shape).
Optionally refresh the published-corpus audit (what shipped since last round; AI tells that
survived editing are the highest-value evidence). Save round inputs under `rounds/r<N>/inputs/`.

## 1. Generate (parallel — one writer agent per brief)
For every brief in `evolution/briefs/` (per `generation.briefs`): a writer agent runs the full
skill workflow — reads `SKILL.md`, the pack files it names, `formats/<container>.md` for the
brief's container, and the brief; facts are **imported frozen** (Pass B/C only, no research);
writes the piece to `rounds/r<N>/pieces/<brief-id>.md`. Long-form pieces also save their marker
ledger to `<brief-id>.ledger.md`. Each writer's return includes its **tone manifest**
(`tone[...] · mood · markers · route`) — routing telemetry the board reads. Writers never see each
other's output. Record the generation model in the round report.

## 2. Panel (parallel — pipeline per piece, no cross-piece barrier)
Per piece, one judge agent per lens in `panel.lenses`, each built from its charter in
`evolution/judges/<lens>.md` (the charter names its own required reading). Judges return
structured verdicts: `{score 1-5, takeaways[≤5]: {severity, class: compliance-failure|rule-gap|
judgment-call, quote, lesson, proposed_fix}}`. Independence is hard: no judge sees another's
output. Save all verdicts to `rounds/r<N>/verdicts.json`.

## 3. Mechanical layer (cheap, objective — run while panels finish)
```bash
for f in "$ROUND"/pieces/*.md; do id=$(basename "$f" .md)
  python3 "$SKILL/tools/validate_voice.py" tells   --file "$f" --card "$SKILL/profiles/kaue/kaue.card.yaml"
  python3 "$SKILL/tools/validate_voice.py" density --file "$f" --card "$SKILL/profiles/kaue/kaue.card.yaml" --facts "$EVO/briefs/$id.md"
  python3 "$SKILL/tools/validate_voice.py" diff    --facts "$EVO/briefs/$id.md" --styled "$f"
done > "$ROUND/validator.txt" 2>&1
python3 "$SKILL/testbed/check_round.py" --round "$ROUND/pieces" --briefs "$EVO/briefs" \
  --card "$SKILL/profiles/kaue/kaue.card.yaml" > "$ROUND/check_round.txt" 2>&1
```
`audit --file` additionally for pieces ≥1,200 words. A fact-diff hard fail invalidates that piece
as evidence (note it; judges' takeaways from it still count for slop, not for fidelity).

## 4. Master board (barrier — needs ALL evidence)
`board.members` agents, one stance each (charter: `evolution/judges/master-board.md`), read the
full evidence set independently and propose candidates in the charter's yaml contract. A synthesis
chair dedupes into the slate: mechanical fixes · empirical candidates (≤`candidates_max`, ranked) ·
owner-taste questions · calibration-routed marker items · workflow fixes. Save slate + dissents to
`rounds/r<N>/slate.md`.

## 5. Empirical tests (parallel per candidate)
- **Prose candidates**: for each, pick `probes_per_candidate` briefs where the defect showed;
  regenerate each probe with the candidate's `proposed_diff` injected into the writer's context as
  an additional rule (baseline = the round's piece, same model). Blind pairwise judging per
  `evolution/judges/blind-ab.md`, `votes_per_probe` judges, presentation order alternating by
  probe index. Adopt-eligible when win-rate (wins/non-tie primary votes) ≥ `adopt_threshold` and
  no probe shows a fact divergence.
- **Lexicon candidates**: the false-positive guard — the proposed pattern must flag ZERO lines
  across `empirical.lexicon_guard` dirs (the author's own prose + accepted goldens); then it must
  actually fire on the round evidence that motivated it. Mechanical; no votes needed.
- **Workflow fixes** (compliance failures): no A/B needed — they re-assert existing rules; verify
  by one regeneration showing compliance.

## 6. Human gate (ONE consolidated check-in — never mid-flow pings)
Present: round scoreboard, the slate with win-rates, and the owner-taste questions. Ask exactly
what `human_gate.ask` lists: which adopt-eligible candidates to adopt (multi-select) · the taste
questions (direct either/or) · whether to commit. Anything touching `markers:` is presented as
"routes to a calibration round", never adopted here.

## 7. Codify + close the loop (only after the gate)
- Apply each adopted candidate as ONE mapped change (the closed set in `evolution/README.md` §6);
  respect `governance.lessons_cap` — adding a lesson may mean merging or expiring one.
- Append the round entry to `evolution/EVOLUTION.md`: date, model, scoreboard, slate, test
  results, human decisions, codified diffs (`- [RN][evidence] "quote" → change-type: what — file`),
  deferred items.
- Bump `round_next` in hyperparams.yaml; append any knob changes to `history:` with reasons.
- Re-run the mechanical layer on `testbed/accepted/` if any lexicon/rule changed (regression: the
  goldens must stay green). Run `python3 "$SKILL/tools/test_tools.py"` if any tool changed.
- Update session auto-memory with the round's state and open decisions.

**Two-strike rule**: any stage failing twice on the same cause → stop, present, ask. Rounds are
cheap; silent thrash is not.
