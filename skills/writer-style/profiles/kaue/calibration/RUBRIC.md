# Calibration rubric — per piece, ≤1 minute

The owner rates every piece of every round with this fixed block (captured as fenced yaml in
`ROUNDS.md`). Conversational reactions are fine — Claude structures them into this format and
confirms before logging.

```yaml
piece: 05-deepdive-svm-lifecycle
voice_fit: 1-5        # "sounds like me"
naturalness: 1-5      # "a reader would NOT clock this as AI"
forced_insertions:    # count + verbatim quotes — each quote MUST map to a change
  - "<quote the offending sentence>"
repetitions_noticed:
  - "<e.g. 'godsend twice in 800 words'>"
publish: y|n          # "would you publish this as-is?"
note: <one line, free text>
```

## The codification rule

Every feedback item maps to **exactly one** logged change, from a closed set:

| Change type | Lands in |
|---|---|
| `card-dial` | `kaue.card.yaml` dials |
| `marker-cap/gate` | `kaue.card.yaml` markers: |
| `rule-edit` | `kaue.md` / `rules/*.md` |
| `exemplar-add/remove` | `exemplars/kaue/` |
| `themes-bank-entry` | `themes.md` |

Logged in ROUNDS.md as:
`- [R1][04-security] "this is latam" forced → marker-gate: tightened gate_when — kaue.card.yaml`

Feedback that fits none of these is logged as `unmapped` — that's a design-gap signal, discussed
before the next round.

## Blind A/B (regression + placebo guard)

Each round, 2–3 briefs (always including the worst-rated baseline cell): Round-0 output vs Round-N
output on the same brief, presented as shuffled A/B; owner picks; the unblinded mapping is recorded
in ROUNDS.md **after** the pick. A new-pack loss = regression → gets a mapped change before the next
round.

## Convergence (stop when ALL hold for 2 consecutive rounds)

1. `voice_fit ≥ 4` AND `naturalness ≥ 4` on every matrix cell
2. zero `forced_insertions` reports across the matrix
3. `publish: y` on ≥ 7/8 briefs
4. validator green: 0 hard fails, 0 identity/signoff advisories, ≤ 2 tic advisories total
5. blind A/B: new pack picked or tied on every cell

Then: promote owner-confirmed tic caps to `enforce: hard`, freeze the last accepted round as
`rounds/accepted/` (golden outputs, the permanent regression arm).
