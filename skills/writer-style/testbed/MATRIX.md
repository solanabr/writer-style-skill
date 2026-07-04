# Calibration test matrix

Fixed 8-brief eval set covering the failure surface of the kaue pack. Regenerated in full each
calibration round; never edited after Round 0 (the fact-sheets are FROZEN so round-over-round diffs
isolate pack changes from research variance). Owner ratings live in
the local calibration ledger (gitignored).

## The matrix

| # | Brief | Words | Job → route | What it tests |
|---|-------|-------|-------------|----------------|
| 01 | How-to: priority fees | 1200 | how-to → helius | **LATAM must NOT appear** (no gate keyword in facts); tic caps in neutral register |
| 02 | Macro: stablecoins + FX in emerging markets | 1500 | macro → hayes | LATAM **legitimately allowed** (topic IS the region) — present but not saturated |
| 03 | Course-opener / motivation | 800 | motivation → primary-only | Catchphrase pileup, double sign-offs, even-enthusiasm; global audience → no identity beat |
| 04 | Security: missing signer checks | 1200 | security → helius/vitalik | Serious register: no LATAM, no "game-changer", no jokes at the exploit |
| 05 | Deep-dive: SVM transaction lifecycle | 2500–3000 | derivation → vitalik | **The compounder**: long-form marker budgets, seam rotation, intra-doc repetition |
| 06 | Short post: Anchor 1.0 shipped | 400 | announcement → any | Control: caps scale down sanely, no forced marker to "prove" voice |
| 07 | Tutorial: Anchor init → devnet deploy | 1800 | how-to → helius | Analogy cap (≤1), triadic-list looping, step-register terseness |
| 08 | Thesis: AI agents × crypto rails | 2000 | thesis → balaji | LATAM **boundary** case: facts mention emerging markets once → ≤1 beat, never themed |

02 and 08 are deliberate: a harness that only proves "LATAM never appears" would teach the writer to
amputate the marker. The owner's complaint is *wrong contexts*, not existence.

## Brief file format

Each brief = line-oriented frontmatter (parsed by `check_round.py` without a YAML dep) + the
assignment + a **frozen fact-sheet** (Pass-A'd once against solana-dev / context7 MCPs on the date
stamped in the file; rounds only redo Pass B/C — never re-derive the facts).

`expect:` keys consumed by `check_round.py`:
- `<marker-id>: 0` — exact count assertion (any lexeme hit fails). Used on gate-MISS briefs.
- `<marker-id>_max: N` — count must be ≤ N.
- `<marker-id>_sections_max: N` — marker lexemes confined to ≤ N sections (the "not themed
  throughout" proxy for boundary briefs).
- `<marker-id>: allow` — no mechanical assertion; human-rated cell. Used on gate-PASS briefs whose
  TOPIC is the region (lexeme counts measure substance there, not identity beats — brief 02).
- `hard_fails: 0` — the piece must exit the validator with no hard failure.

## Running a round

```bash
SKILL=skills/writer-style
PACK=$SKILL/profiles/kaue
ROUND=$PACK/calibration/rounds/round-N

# per piece (generation happens via the /write-in-voice workflow; briefs supply the frozen facts)
python3 $SKILL/tools/validate_voice.py tells   --file $ROUND/<id>.md --card $PACK/kaue.card.yaml
python3 $SKILL/tools/validate_voice.py density --file $ROUND/<id>.md --card $PACK/kaue.card.yaml --facts $SKILL/testbed/briefs/<id>.md
python3 $SKILL/tools/validate_voice.py audit   --file $ROUND/<id>.md
python3 $SKILL/tools/validate_voice.py diff    --facts $SKILL/testbed/briefs/<id>.md --styled $ROUND/<id>.md

# whole round, mechanical expectations
python3 $SKILL/testbed/check_round.py --round $ROUND --card $PACK/kaue.card.yaml
```

Until the `markers:` block lands in `kaue.card.yaml`, pass `--markers $SKILL/testbed/draft-markers.yaml`
to `density` and `check_round.py` (Round 0 runs against the draft markers).

Round protocol, rubric, codification rule, A/B, and convergence criteria:
the local calibration dir (gitignored); golden outputs: `accepted/`.
