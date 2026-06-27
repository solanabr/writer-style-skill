# The data layer — style-cards, exemplars, and the builder/writer/validator boundary

Each voice ships **three artifacts**, each owning one job, no duplication:

| Artifact | Owns | Never contains |
|---|---|---|
| `<voice>.md` | register-grounded **craft prose**, for the primary, reproduced idiolect; for a secondary, transferable craft + EXCLUDES | numbers, stat dumps, banned-word lists-as-data |
| `<voice>.card.yaml` | the **actionable dials** (ranges/enums) + favor/avoid lists + AI-tell caps, the writer/validator membrane | prose explanation of *why* a move works (that's the persona); example passages (that's the bank) |
| `exemplars/<voice>/` | the actual **annotated passages**, one per rhetorical slot, with move-traces, the few-shot | abstract rules; dials |

The raw stylometry (`evidence/<voice>.profile.json`) is **builder-internal and validator-internal only**.
The writer never reads it. The card is the membrane: only the subset of numbers a writer can *act on* crosses
into generation, transformed into ranges/enums and favor/avoid lists.

## The style-card schema (`<voice>.card.yaml`)

Numbers are **ranges/enums**, never point targets — a writer can aim at a band and a direction, not `0.48`.
Every field states how the writer uses it; the `card_suggestions` block of `evidence/<voice>.profile.json`
gives derived starting values, which the author hand-curates against the persona.

```yaml
voice: kaue
role: primary                 # primary = reproduce idiolect | secondary = transferable craft
register: medium-technical-guide
persona_ref: kaue.md
exemplars_ref: exemplars/kaue/
dials:
  sentence_length: {median, short_punch_floor, long_reach, burstiness_min}
    # WRITER: aim typical sentence at median; force ≥1 short punch & ≥1 long reach per section.
    # VALIDATOR: generated sentence-length stdev must be ≥ burstiness_min (the #1 human-vs-AI signal).
  readability_grade: {min, max}     # WRITER: keep the body in this FK band.  VALIDATOR: compute FK.
  lexical_density: low|medium|high  # WRITER: how dense with content words ("don't pack every sentence").
  hedge_boost_lean: -2..+2          # WRITER: -=hedged/qualified, +=assertive. (Kaue +1: confident verdicts, named tradeoffs.)
  person_perspective: {first, second, third}   # the narrative stance; VALIDATOR flags large 3rd-person drift.
  example_density: none|low|medium|high        # concrete instances/numbers per abstract claim.
  definition_density: {enum: front-loaded|just-in-time|sparse, per_1k: <rate>}  # WHEN terms get defined +
    # the measured marker rate (e.g. helius 4.9/1k defines ~2.7× more than kaue 1.8/1k).
  code_density: none|low|medium|high           # fenced snippets per section, for technical guides.
  rhetorical_question_rate: none|low|medium|high
favor:
  connectives: [...]   # WRITER: reach for THESE transition words — they sound like this voice.
  moves: [...]         # the load-bearing rhetorical moves (pointers; expanded in the persona + tagged in exemplars).
avoid:
  words: [...]         # never emit.  VALIDATOR: substring scan, hard fail on a hit.
  connectives: [...]   # essay-bot connectives banned (use the FAVOR set).
ai_tells:              # structural tells; the validator enforces these (defaults in validate_voice.py).
  - {id: false-antithesis, cap_per_800w: 1}   # "not X, it's Y" — at most one per ~800 words, as a real verdict.
  - {id: em-dash-overuse, max: 4, kind: guardrail}  # a SAFETY ceiling, not a corpus-measured voice signal (every voice <2.2/1k).
  - {id: uniform-cadence, min: <burstiness_min>}  # even prose IS the tell.
  - {id: delve-class, cap: 0}                 # delve/intricate/realm/tapestry/multifaceted/underscores.
  - {id: even-enthusiasm, rule: spike-then-cool}  # hype at edges; ~100-200 flat words between spikes.
```

Forensic fields (function-word rates, n-gram frequencies, type-token ratio, full punctuation table) are
**absent by construction**. They live only in `evidence/`.

**Two honesty conventions.** (1) A scalar dial is **measured** from the corpus; a dial written as a mapping
with `source: persona_override` was set from the persona because the small sample under-measured it (it
carries `measured:` + `why:` so the override is auditable, not hidden). (2) `em-dash-overuse` is a **safety
guardrail**, not a voice signal. Every author measures <2.2/1k, so the cap never reproduces an authentic
trait; only `uniform-cadence`/`burstiness_min` is a real, enforced per-voice target.

The validator (`validate_voice.py tells --card <voice>.card.yaml`) enforces the per-voice `burstiness_min`,
`em-dash-overuse.max`, `false-antithesis.cap_per_800w`, and the `avoid` word/connective lists; without a card
it falls back to universal defaults.

**Tiered deslop baseline.** On top of each voice's `avoid` list, the validator applies a shared, *gated*
AI-cliché baseline (in `tools/style_lexicons.py`) so it catches machine slop without over-suppressing
legitimate technical prose: **Tier-1** clichés always flag (with a plain-word swap surfaced inline); **Tier-2**
buzzwords flag only as a cluster (≥3 distinct in a paragraph); **Tier-3** high-frequency technical words
(`robust`, `scalable`, `ecosystem`…) flag only at density (≥3 distinct *and* ≥5/1k). A few scattered across a
long post is fine. Plus crypto-boilerplate, copula/symbolic-gloss clusters, machine-paste fingerprints (a hard
fail), and Markdown hygiene. See `rules/deslop.md` for the write-time judgment that complements the lint.

## The exemplar bank (`exemplars/<voice>/`)

Curated few-shot passages are the **single strongest voice conveyor** — so this is first-class. One annotated
`.md` per **rhetorical slot** + an `index.yaml`.

- **Primary (14 files / 7 slots):** `opener` · `derivation` · `transition` · `seam` · `verdict` · `close` · `analogy`
  (the kaue bank ships two `opener` registers), sourced from the target's real on-register writing. The writer
  **always loads the `seam`** (the naturalness floor is non-negotiable) + `opener` + `close` + 1 body slot matched to the job (~4 of 14).
- **Secondary (~3 move-demos):** the author's signature moves, in **neutral voice** (idiolect stripped). They
  show how to *apply* the move in Kaue's voice, not copy the author. Slots are the author's key moves.

Each exemplar file:

```markdown
---
slot: opener            # which rhetorical position / move it demonstrates
length_words: 95
topic: solana-local-fee-markets
fk_grade: 9.4           # measured — lets the writer see a dial in the flesh
demonstrates: [pain-first-hook, calm-mechanics, parenthetical-seam, named-tradeoff]
---
<the passage>

<!-- MOVE TRACE: pain-first hook → calm mechanics → first-person seam → named trade-off → … -->
```

`demonstrates` tags share one vocabulary with the card's `favor.moves` and the persona's craft headings.
`index.yaml` lists the slots and which the writer should default-load.

## How the writer selects exemplars (at generation time)
1. Always load the **seam** exemplar (primary), the human-seam floor.
2. Load **opener** + **close** (every piece has both).
3. Load **1–2 body** exemplars matched to the routed job (derivation-heavy → `derivation`+`verdict`; long →
   `transition`). For a secondary backbone, load its move-demos.
4. For a multi-lesson course, keep a **used-exemplar ledger** and rotate body slots so lesson 2 ≠ lesson 1.

## The boundary (who reads what)

```
BUILDER  (tools/profile_corpus.py, persona-builder agent)
  reads:  cleaned corpus
  writes: evidence/<voice>.profile.json (raw + card_suggestions)  →  derives <voice>.card.yaml + curates exemplars
WRITER   (voice-writer agent, at generation time)
  reads:  <voice>.md  +  <voice>.card.yaml  +  ~4 exemplars       ←  NEVER evidence/ or raw numbers
VALIDATOR (tools/validate_voice.py, voice-validator agent)
  reads:  the generated output (+ may read evidence/ for forensic context)
  checks: repetition audit · AI-tell lint · fact-preservation diff
```

The hard line: **`evidence/` is builder-and-validator-visible, writer-invisible.** Every field the writer
sees answers "how do I change a sentence with this?"
