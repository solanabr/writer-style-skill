---
description: "Run the Pass-C checks on generated output (facts, AI tells, repetition)"
---

Gate generated content before shipping. Spawn the **voice-validator** agent, or run the checks directly:

```bash
# Resolve the writer-style skill dir (plugin / project / clone), then call the tools with absolute paths:
SKILL="${CLAUDE_PLUGIN_ROOT:+$CLAUDE_PLUGIN_ROOT/skills/writer-style}"
[ -d "$SKILL" ] || SKILL=".claude/skills/writer-style"; [ -d "$SKILL" ] || SKILL="skills/writer-style"

# fact preservation — every verified number/identifier must survive styling (HARD gate):
python3 "$SKILL/tools/validate_voice.py" diff  --facts factsheet.md --styled lesson.md
# AI-tell lint + deslop scan — pass --card to enforce THIS voice's targets (burstiness_min, em-dash, avoid)
# AND a gated cliché scan (Tier-1 with plain-word swaps / Tier-2 cluster / Tier-3 density), crypto-boilerplate,
# copula/gloss, machine-paste fingerprints (hard fail), and Markdown hygiene:
python3 "$SKILL/tools/validate_voice.py" tells --file lesson.md --card "$SKILL/profiles/kaue/kaue.card.yaml"
# marker density + context gates — budgets from the card's markers: block; pass --facts so identity
# gates can be checked (an identity beat with NO gate keyword in the fact-sheet = the forced-insertion
# hard fail; a doubled sign-off = hard fail; over-budget tics/clustering/spread = advisory):
python3 "$SKILL/tools/validate_voice.py" density --file lesson.md --card "$SKILL/profiles/kaue/kaue.card.yaml" --facts factsheet.md
# repetition audit — one long document (section-to-section) or a course/batch:
python3 "$SKILL/tools/validate_voice.py" audit --file long-piece.md
python3 "$SKILL/tools/validate_voice.py" audit --lessons out_lessons/
```

Interpret:
- **`diff` reports dropped/mutated facts → HARD FAIL.** Send those exact sentences back to the voice-writer.
- **`tells` fires on uniform cadence** → the prose is too even (the #1 AI tell); vary sentence length until the
  stdev clears the card's `burstiness_min`.
- **`density` hard-fails on a gate-missed identity marker** → quote the offending sentence to the writer/owner
  (the gate is a lexical heuristic — a human confirms); a doubled sign-off just gets cut. Advisories
  (over-budget tics, clustering, "themed through the piece" spread) are weighed, not auto-fixed.
- **`audit` flags low opener variety / high overlap** → the piece/lessons are formulaic; rotate openers/seams.

There is intentionally **no style-distance score** — judge voice fidelity by a human blind read against
`$SKILL/profiles/kaue/kaue.md` + the exemplars. A number there would be false confidence.
