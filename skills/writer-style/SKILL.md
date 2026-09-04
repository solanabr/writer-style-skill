---
name: writer-style
description: "Write original educational and long-form technical content in a specific author's authentic voice — courses, lessons, explainers, deep-dives, threads — using a two-layer voice pack (an always-on PRIMARY voice that reproduces the author's idiolect + SECONDARY craft borrowed from master writers, applied not impersonated, routed by the piece's job) and a facts-first workflow that verifies technical content BEFORE styling. Ships two packs: kaue (Kaue / Superteam Brazil, tuned for Solana/Web3 education) as the default, and david (David Potolski Lafetá — Solana online-course lessons, plus Medium long-form and PM/delivery artifacts like estimation write-ups, scoping docs and retrospectives; one guest voice, helius, scoped to its evidence layer). Use whenever drafting or editing content that should sound like a specific person rather than generic AI — 'write this lesson in my voice', 'in Kaue's voice', 'in David's voice', 'draft a thread the way <author> would', or 'a Superteam-style explainer'. Also builds new voice packs via the persona-builder agent. Do NOT use for brand-neutral/generic copy, or content that should sound house-styled rather than like a person."
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

## The packs

| Pack | Voice | Use it when | Shape |
|---|---|---|---|
| **`kaue`** (default) | Kaue / Superteam Brazil — Solana & Web3 education | "in **Kaue's** voice", "a Superteam-style explainer", Solana lessons/courses/threads | primary + **5 secondary** craft voices, routed by job |
| **`david`** | David Potolski Lafetá — Solana online-course material; also Medium long-form (800–2,500w) + PM/delivery artifacts | "in **David's** voice", course lessons, estimation write-ups, scoping docs, retrospectives, practical how-to posts | **one guest: `helius`**, evidence layer only (structure banned), ≈85/15 |

An unqualified "write this **in my voice**" defaults to **`kaue`**. For another author/domain, load that pack
instead; to create one, use the persona-builder. Everything below is the engine; the pack supplies the voices.

> **`david` routes differently.** Its router (`profiles/david/ROUTING.md`) picks a **register mode** first,
> then decides whether its one guest is on. That guest is **`helius`, licensed for its evidence layer only** —
> its *structural* layer (numbered step lists, procedures) is banned, because importing it measured
> **−4.2 FK grades and −5 words of median sentence length** against the corpus. Weight ≈ 85/15; primary-only
> for non-technical pieces. The pack also **inverts two engine defaults**: enthusiasm is *tail-loaded* (cold
> open, hot close, not hot edges), and its measured analogy rate is 0.0/1k, so its exemplar bank swaps the
> `analogy` and `verdict` slots for `worked-example` and `question-hinge`. Its main container
> (`course-lesson`) and anything code-bearing are **extrapolations** — the corpus has neither. Read
> `profiles/david/PACK.md` before writing in it.

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
| **B: Voice** | Load `kaue.md` + `kaue.card.yaml` + ~4 exemplars + the routed secondary. **Check the card's `markers:` gates** (identity beats need their gate keywords in the fact-sheet — write the marker budget ledger first) and scan `themes.md` for fitting substance. **Restyle the frozen facts**: "every number, code line, and named API is frozen; rephrase around them, never change them." Apply the naturalness floor (incl. the plainness quota). Long-form (≥1,200w): section-by-section with the ledger. | **ON** |
| **B.5: Blind-compare** | Re-read the draft against the **loaded exemplars** (seam + opener) — *"him, or a rule-follower?"* If it's even/polished/definition-led, regenerate toward a felt-pain opener + uneven rhythm + rotating seams. Run the FIT test on every marker: *does it land on a genuine payoff, in this piece's mood, within budget?* Keep what fits; never necessity-test personality. **Loaded exemplars only, never the corpus** (at write-time the corpus is token-waste). | **ON** |
| **C: Lint** | AI-tell scan + **fact-preservation diff** (no number/identifier mutated A→C) + **marker density/gates** (an identity beat with no gate keyword in the fact-sheet or a doubled sign-off is a **hard fail**) + repetition audit (intra-doc for long pieces). A changed `0.002 SOL` or renamed instruction is a **hard fail**. | — |

`tools/validate_voice.py` runs the Pass-C checks (`tells`, `density`, `diff`, `audit`); the **voice-validator**
agent wraps them.

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

**Explicit tone override.** The requester may pin the blend — `tone: hayes`, `tone: helius 0.7 / hotz 0.3`,
"a touch of vitalik", or `primary-only`. An explicit request **outranks the router**: apply it within the cap
(backbone + ≤1 guest; rough weights set which is which). If the request crosses a lane guardrail (e.g. hotz
on security), still honor it, but say so in the tone manifest instead of silently re-routing.

**Tone manifest (always).** Every delivery ends with ONE metadata line in the chat/report — **never inside
the piece itself**:
`tone[helius 0.8, hayes 0.2] · mood: dry-competent · markers: sign-off 1 · route: auto`
Weights are the writer's honest estimate of each secondary's share of the craft (backbone-heavy by
construction; the always-on primary is not weighted — it owns the floor). `route: auto` vs `route: requested`
records whether the blend was router-chosen or user-pinned, so the requester can iterate ("same piece,
hayes 0.5").

## The naturalness floor (protect above all craft — `rules/naturalness.md`)

The body of every craft, applied thoroughly, *smooths* prose into something that sounds like nobody. Counter it:
**write unevenly**: long calm stretches, enthusiasm only at the edges (open / seams / verdicts / close), and
**real human seams that CLUMP** (a confession, a real number from your own use, a named credit, a "this ran
long" — several per long piece, in floods and droughts, never one-per-section on schedule; a met quota is
itself the tell). Even enthusiasm + even polish is the #1 AI tell. Always load the **seam** exemplar.


## What you load at generation time (Pass B)

`profiles/kaue/kaue.md` (primary prose) · `kaue.card.yaml` (dials + `markers:` budgets/gates) ·
`profiles/kaue/themes.md` (the substance bank — pull FITTING stances/anecdotes instead of recycling
exemplar content) · ~4 exemplars from `exemplars/kaue/` (always the **seam** + opener + close + 1 body slot
by job; exemplars are rhythm donors, never content donors) · the **one** routed secondary
(`secondary/<v>.md` + card + its move-demos) · **if the piece targets a specific container** (X
post/thread, LinkedIn, blog, course lesson, video script, newsletter, community announcement), the
one matching contract in `formats/` — container is orthogonal to job; it constrains the vessel, not
the routing. **Never** read `evidence/*.profile.json`, `calibration/`, or `evolution/` —
builder/validator-only.

*Substitute the pack directory for another pack (`profiles/david/david.md` + card + `themes.md` + ~4
exemplars). For a **primary-only** pack there is no routed secondary to load — the router hands you a
register mode instead.*

## Self-check before returning (Pass C)
- **Burstiness:** sentence lengths vary hard (≥1 short punch & ≥1 long run per section); stdev clears the
  card's `burstiness_min`. *Uniform cadence is the top tell.*
- **AI tells:** run `python3 "$SKILL/tools/validate_voice.py" tells --card "$SKILL/profiles/kaue/kaue.card.yaml"`. It enforces *this voice's*
  burstiness floor, em-dash cap, false-antithesis cap, avoid lists, AND a **deslop scan** (gated cliché tiers
  with plain-word swaps, crypto-boilerplate, copula/gloss, machine-paste fingerprints, Markdown hygiene).
- **Deslop judgment** (`rules/deslop.md`): clear cliché *clusters*, run the paragraph-reshuffle /
  "what's-new" / read-aloud tests, but keep the specific detail, mixed feelings, and asides that read human.
- **Naturalness:** seams present and CLUMPED (droughts allowed — never one per section on schedule);
  enthusiasm spiked at edges, flat in the body; ≥1 in 3 sections marker-free (the plainness quota).
- **Markers:** run `python3 "$SKILL/tools/validate_voice.py" density --file <draft> --card "$SKILL/profiles/kaue/kaue.card.yaml" --facts <fact-sheet>`.
  An identity beat with no gate keyword in the fact-sheet, or a doubled sign-off, is a **hard fail**; for
  ≥1,200w also run `audit --file <draft>` (section-to-section repetition).
- **Facts:** every number/identifier from the fact-sheet survived styling unchanged (run `python3 "$SKILL/tools/validate_voice.py" diff`).
- **In-voice:** reads like the primary against `kaue.md` + the loaded exemplars.

## Progressive disclosure (read when needed)

| Topic | File |
|---|---|
| The two-layer model, the inversion, the cap, how packs plug in | [two-layer-model.md](two-layer-model.md) |
| The facts-first Pass A/Gate/B/C workflow + MCP grounding | [writing-workflow.md](writing-workflow.md) |
| Container contracts (X post/thread, LinkedIn, video script, newsletter…) | [formats/README.md](formats/README.md) |
| The style-card schema, exemplar convention, builder/writer/validator boundary | [style-card-schema.md](style-card-schema.md) |
| The full router (per-lane triggers, stacking, failure modes) | [profiles/kaue/ROUTING.md](profiles/kaue/ROUTING.md) |
| The primary voice (Kaue) | [profiles/kaue/kaue.md](profiles/kaue/kaue.md) |
| The substance bank (stances/anecdotes/analogies with receipts) | [profiles/kaue/themes.md](profiles/kaue/themes.md) |
| **The `david` pack** (Solana courses; 2020 register, PM substance, `helius` evidence-layer guest) | [profiles/david/PACK.md](profiles/david/PACK.md) → [david.md](profiles/david/david.md) · [ROUTING.md](profiles/david/ROUTING.md) · [themes.md](profiles/david/themes.md) |
| A secondary voice's craft | `profiles/kaue/secondary/<voice>.md` |
| **Building/refreshing a voice** (the adversarial method) | [authoring-personas.md](authoring-personas.md) → `method/` |
| **Empirical calibration** (the 8-brief testbed + owner-feedback rounds) | [testbed/MATRIX.md](testbed/MATRIX.md) + `profiles/kaue/LESSONS.md` (calibration working data is local-only) |

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
| [/validate-voice](../../commands/validate-voice.md) | Run audit / tells / density / diff on generated output |
| [/calibrate-voice](../../commands/calibrate-voice.md) | Run a calibration round: regenerate the 8-brief matrix, collect owner ratings, codify changes |
| [/evolve-voice](../../commands/evolve-voice.md) | Run an evolution round: format-matrix mass-generation → adversarial panels → master board → empirical A/B → human gate |
