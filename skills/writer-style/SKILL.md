---
name: writer-style
description: "Write original educational and long-form technical content in a specific author's authentic voice — courses, lessons, explainers, deep-dives, threads — using a two-layer voice pack (an always-on PRIMARY voice that reproduces the author's idiolect + SECONDARY craft borrowed from master writers, applied not impersonated, routed by the piece's job) and a facts-first workflow that verifies technical content BEFORE styling. Ships the kaue pack (Kaue / Superteam Brazil, tuned for Solana/Web3 education) as the default. Use whenever drafting or editing content that should sound like a specific person rather than generic AI — 'write this lesson in my voice', 'in Kaue's voice', 'draft a thread the way <author> would', or 'a Superteam-style explainer'. Also builds new voice packs via the persona-builder agent. Do NOT use for brand-neutral/generic copy, or content that should sound house-styled rather than like a person."
license: "MIT — Superteam Brazil / Kaue"
user-invocable: true
---

# Writer-Style

Write **original** content that sounds like a **specific person**, not generic AI. And, for technical
topics, that is **factually correct first and styled second**. The engine is voice-agnostic; it ships with
the **`kaue` pack** (Kaue / Superteam Brazil, tuned for Solana/Web3 education) as the default.

## What this skill is for

Use it whenever the output should read like a named author:
- **Educational Solana/Web3 content**: courses, lessons, modules, explainers, tutorials, deep-dives, threads.
- **Long-form technical writing** in general, in a target voice.
- Drafting *or* editing/restyling existing copy into the voice.
- **Building a new voice pack** (add an author, build someone's voice, design a router) → the **persona-builder** agent.

**Do NOT use for:** brand-neutral/house-style copy; content that should sound generic; one-off "summarize this"
where voice doesn't matter.

> **Honest scope.** This produces content **in the author's register, with AI tells engineered out and facts
> verified first**, not an indistinguishable clone. Voice fidelity is corpus-bounded and improves as more of
> the author's on-register writing is added. (The default Kaue pack is calibrated from a small on-register
> sample; lean on the **exemplars** and the **naturalness floor**, and don't over-promise "it's exactly him.")

## The default pack

Requests like "write this lesson **in my voice**", "in **Kaue's** voice", or "a Superteam-style explainer"
→ use the **`kaue` pack** (`profiles/kaue/`). For another author/domain, load that pack instead; to create
one, use the persona-builder. Everything below is the engine; the pack supplies the actual voices.

## The two-layer model (summary — full detail in `two-layer-model.md`)

- **Primary voice** (`profiles/kaue/kaue.md` + `kaue.card.yaml`), the target author's own voice, **always on**,
  **reproduced** (idiolect is the asset). It owns the tone, the seams, and the naturalness floor. **Free**,
  not counted toward the layer budget.
- **Secondary voices** (`profiles/kaue/secondary/*.md` + cards), transferable **craft** borrowed from master
  writers, **idiolect stripped** (applied in Kaue's voice, never impersonation). One leads (backbone), at most
  one guests. Chosen by the piece's **job**, not its topic.

> The inversion is the whole trick: **reproduce** the primary's idiolect, **strip** the secondaries'. Keep the
> primary's quirks; borrow only the secondaries' *craft*.

## The workflow — facts first, voice last (full detail in `writing-workflow.md`)

Persona prompting boosts voice **but degrades factual accuracy** — fatal for technical content. So **voice is
the last transform over verified facts, never the medium facts are discovered in.** Five steps:

| Step | What | Voice |
|---|---|---|
| **A: Facts** | Outline + every claim, number, code line, version-sensitive API, in plain neutral prose. Ground against the Solana doc MCPs (`solana-dev`, `context7`, Helius), **not** model memory. Output: a fact-sheet. | **OFF** |
| **Gate: Verify** | Fact-check the terse fact-sheet before any styling. (Cheap: facts aren't buried in warm prose.) Nothing proceeds until facts are frozen. | — |
| **B: Voice** | Load `kaue.md` + `kaue.card.yaml` + ~4 exemplars + the routed secondary. **Restyle the frozen facts**: "every number, code line, and named API is frozen; rephrase around them, never change them." Apply the naturalness floor. | **ON** |
| **B.5: Blind-compare** | Re-read the draft against the **loaded exemplars** (seam + opener) — *"him, or a rule-follower?"* If it's even/polished/definition-led, regenerate toward a felt-pain opener + uneven rhythm + rotating seams. **Loaded exemplars only, never the corpus** (at write-time the corpus is token-waste). | **ON** |
| **C: Lint** | AI-tell scan + **fact-preservation diff** (no number/identifier mutated A→C) + repetition audit. A changed `0.002 SOL` or renamed instruction is a **hard fail**. | — |

`tools/validate_voice.py` runs the Pass-C checks (`tells`, `diff`, `audit`); the **voice-validator** agent
wraps them.

> **Running the bundled tools (any install).** The validator and data live inside this skill's own directory,
> so call them with **absolute paths**. Resolve the directory once and let **`$SKILL`** stand for it below
> (`$CLAUDE_PLUGIN_ROOT/skills/writer-style` in a plugin, `.claude/skills/writer-style` in an npm/project
> install run from the project root, or `skills/writer-style` in a clone run from the repo root):
> ```bash
> SKILL="${CLAUDE_PLUGIN_ROOT:+$CLAUDE_PLUGIN_ROOT/skills/writer-style}"
> [ -d "$SKILL" ] || SKILL=".claude/skills/writer-style"; [ -d "$SKILL" ] || SKILL="skills/writer-style"
> python3 "$SKILL/tools/validate_voice.py" tells --file <draft> --card "$SKILL/profiles/kaue/kaue.card.yaml"
> ```

## Routing — which secondary voice (full router in `profiles/kaue/ROUTING.md`)

Route on the piece's **dominant job, not its topic.** Each voice is a full backbone in its lane:

| The piece's dominant job | Lead voice |
|---|---|
| Show how a documented Solana system works: tutorial, integration, the runtime, the real artifact | **helius** |
| Derive why a deep / non-obvious design is right: protocol internals, cryptoeconomics, mechanism design | **vitalik** |
| Frame a broad, interconnected thesis: connect tech/history/economics/society, the big picture & trajectory | **balaji** |
| Make macro / market forces legible: economics, tokenomics, geopolitics, incentives, crowd-psychology | **hayes** |
| Demystify a hyped / over-complicated thing: collapse it to its true simple model (honest "X is just Y") | **hotz** |
| Security / exploit classes | **helius** (vulnerable→patched) or **vitalik** (why the check is necessary), never **hotz** |
| Pure motivation / "why this matters" / course-opener | **primary only** + ≤1 light guest |

**Rules:** primary always on & uncounted; **cap = backbone (1) + guest (≤1) = 2 secondary layers** (3 only for
3,000+ words, segregated; else split the piece); stack only across **different lanes**; helius is the safe
universal guest; hold each voice's guardrail (Hayes builder-optimist not cynical · Balaji peer not oracular ·
Hotz inviting not dismissive · Vitalik warm not flat). The lanes self-differentiate: **no author-vs-author
special rules.**

## The naturalness floor (protect above all craft — `rules/naturalness.md`)

The body of every craft, applied thoroughly, *smooths* prose into something that sounds like nobody. Counter it:
**write unevenly**: long calm stretches, enthusiasm only at the edges (open / seams / verdicts / close), **a
human seam in every passage** (a confession, a real number from your own use, a named credit, a "this ran
long"). Even enthusiasm + even polish is the #1 AI tell. Always load the **seam** exemplar.


## What you load at generation time (Pass B)

`profiles/kaue/kaue.md` (primary prose) · `kaue.card.yaml` (dials) · ~4 exemplars from `exemplars/kaue/`
(always the **seam** + opener + close + 1 body slot by job) · the **one** routed secondary (`secondary/<v>.md`
+ card + its move-demos). **Never** read `evidence/*.profile.json`. That is builder/validator-only.

## Self-check before returning (Pass C)
- **Burstiness:** sentence lengths vary hard (≥1 short punch & ≥1 long run per section); stdev clears the
  card's `burstiness_min`. *Uniform cadence is the top tell.*
- **AI tells:** run `python3 "$SKILL/tools/validate_voice.py" tells --card "$SKILL/profiles/kaue/kaue.card.yaml"`. It enforces *this voice's*
  burstiness floor, em-dash cap, false-antithesis cap, avoid lists, AND a **deslop scan** (gated cliché tiers
  with plain-word swaps, crypto-boilerplate, copula/gloss, machine-paste fingerprints, Markdown hygiene).
- **Deslop judgment** (`rules/deslop.md`): clear cliché *clusters*, run the paragraph-reshuffle /
  "what's-new" / read-aloud tests, but keep the specific detail, mixed feelings, and asides that read human.
- **Naturalness:** a human seam in every passage; enthusiasm spiked at edges, flat in the body.
- **Facts:** every number/identifier from the fact-sheet survived styling unchanged (run `python3 "$SKILL/tools/validate_voice.py" diff`).
- **In-voice:** reads like the primary against `kaue.md` + the loaded exemplars.

## Progressive disclosure (read when needed)

| Topic | File |
|---|---|
| The two-layer model, the inversion, the cap, how packs plug in | [two-layer-model.md](two-layer-model.md) |
| The facts-first Pass A/Gate/B/C workflow + MCP grounding | [writing-workflow.md](writing-workflow.md) |
| The style-card schema, exemplar convention, builder/writer/validator boundary | [style-card-schema.md](style-card-schema.md) |
| The full router (per-lane triggers, stacking, failure modes) | [profiles/kaue/ROUTING.md](profiles/kaue/ROUTING.md) |
| The primary voice (Kaue) | [profiles/kaue/kaue.md](profiles/kaue/kaue.md) |
| A secondary voice's craft | `profiles/kaue/secondary/<voice>.md` |
| **Building/refreshing a voice** (the adversarial method) | [authoring-personas.md](authoring-personas.md) → `method/` |

## Agents & commands

| Agent | Purpose | Model |
|---|---|---|
| [voice-writer](../../agents/voice-writer.md) | Run the facts-first 3-pass workflow to draft/restyle a piece | opus |
| [persona-builder](../../agents/persona-builder.md) | Build/refresh a voice pack (adversarial, evidence-bound) | opus |
| [voice-validator](../../agents/voice-validator.md) | Repetition audit + AI-tell lint + fact-preservation diff | sonnet |

| Command | Purpose |
|---|---|
| [/write-in-voice](../../commands/write-in-voice.md) | Draft a piece in a pack's voice (facts-first) |
| [/new-persona](../../commands/new-persona.md) | Build a new voice via the persona-builder |
| [/profile-corpus](../../commands/profile-corpus.md) | Regenerate builder-internal evidence + card dials |
| [/validate-voice](../../commands/validate-voice.md) | Run audit / tells / diff on generated output |
