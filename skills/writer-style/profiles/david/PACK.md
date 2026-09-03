# PACK — david

> Voice pack for original long-form content in **David Potolski Lafetá's** voice.
> Headline use case: **online course material for Solana** — code-bearing technical lessons, with `helius`
> supplying the evidence layer the corpus does not have. Also: Medium-style long-form posts, 800–2,500 words
> (the corpus's own container), and PM / delivery artifacts — estimation write-ups, scoping worksheets,
> project retrospectives, team-process notes.

- **name:** david
- **license:** MIT — David Potolski Lafetá (the repo owner; this is their own voice)
- **entry:** `../../SKILL.md` (the engine) · **router:** `ROUTING.md`
- **primary:** `david.md` (+ `david.card.yaml`): always-on; reproduces idiolect; **not** counted toward the cap
- **secondary voices:** **one — `helius`** (borrowed from `../kaue/secondary/`), licensed for its **evidence
  layer only** and switched on for technical pieces. Its **structural** layer — numbered step lists,
  procedures — is **banned**: that import measured −4.2 FK grades in validation. Weight ≈ **85 / 15**.
  See `ROUTING.md` §1.

## Primary voice (always on, free)

- **`david.md`** — the tone, rhythm, brain-patterns, and the uneven-human seam. Owns the naturalness floor.
  Register: the **2020 Medium personal-practical post** (FK 8–10, mean sentence ~17 words, paragraphs of one
  or two sentences). Identity beats (Brazil/Portuguese, employer names, the named anecdotes) are
  **context-gated** (§5b) — a value, not a quota.
- **`david.card.yaml` `markers:`** — every countable signature marker with a budget and, where it matters, a
  hard context gate. Enforced by `validate_voice.py density`. **Three gates are `enforce: hard` because they
  guard against fabrication or disclosure, not against style drift:** `fabricated-instance-guard`,
  `book-handoff`, and `employer-client-beat`.
- **`themes.md`** — the substance bank: his real stances, anecdotes, numbers, and named references with
  receipts, topic tags, and burn rates, mined from all 8 posts (off-register files are substance-only
  sources). **Owner-reviewed and signed off 2026-09-03** — all 44 stances are live. The four that were
  previously flagged are now `owner-confirmed`: usable, but they carry no verbatim receipt, so argue them
  as his position and never as a quotation. The banner at the top of that file remains binding.
- **`exemplars/david/`** — 7 verbatim on-register passages, one per rhetorical slot.

## The register tension — read this before writing a PM artifact

This pack has a real, deliberate split, and it will confuse you if nobody says it out loud:

**All of the PM and delivery substance lives in the two 2025 posts, which are excluded as style sources.**

Profiling the eras separately showed a five-grade readability gap on the same author: **2020 = FK 9.0** (5
posts; 3,707 body words, re-measured FK 9.1 after chrome removal) versus **2025 = FK 14.0** (2 posts, 3,497
words). Median sentence length is nearly
identical (16 vs 18 words), so the drift is **vocabulary and abstraction, not rhythm**. Merging the eras
would average across that gap and produce a voice matching neither. **The owner chose the 2020 register.**

So the estimation content exists but the estimation *prose style* does not. Writing a PM artifact in this
pack means: pull the substance from `themes.md` (tagged `[2025-offreg]`), then run it through the
**translation table in `david.md` §7** — a word-level transform whose one-line rule is *if the subject of a
sentence is an abstract noun, rewrite it so the subject is `you`, `I`, or a thing you can point at.*

If a draft still contains an abstract-noun subject, a `However`, or a nominalization stack, you pasted
instead of translating.

*(A related finding, documented in `david.md` §7 and the card's `notes.register_drift`: the 2025 posts'
smoothness is probably **not** the author's acquired polish. Non-native-English seam density collapses ~4.5×
there — except inside the two short first-person anecdotes, which still carry the 2020 seams at a high local
rate — alongside typographic artefacts a browser-typed draft does not produce. Do not model that fluency.)*

## What makes this voice unusual (and where it inverts the engine's defaults)

| Engine default | This voice |
|---|---|
| Enthusiasm at the **edges** (hot open, calm middle, hot close) | **Tail-loaded.** Zero `!` in any of the five openings; the heat is at the end. The body is flat in its *argument* but carries steady low warmth in its *adjectives*, always aimed at someone else's work. |
| A `verdict` exemplar slot | **`question-hinge`** — he never renders a verdict. He asks the reader's worried question and answers it flat, then hands off. |
| An `analogy` exemplar slot | **`worked-example`** — measured analogy rate **0.0/1k**. He instantiates; he does not map. The ban extends to figurative verbs. |
| Em-dash cap as a generic safety guardrail | A **measured signal**: 4 em-dashes in 3,710 words, **none in body prose**. |
| "Calm ≠ clean" as a general looseness rule | A specific, tabulated set of **non-native English seam classes** at 8–10 per 1k of his own prose — with five rules (position, kind, no misspellings, never inside a fact, per-class caps) that matter more than the rate. |
| A `false-antithesis` cap of 1–2 per 800w | **0.** "Not X, it's Y" has no instance in the target register. |

## Invariants

1. **Primary always on, uncounted.** With no secondaries, it carries every piece alone.
2. **Facts first, voice last:** verify before styling; voice never alters a number, a date, or a book title.
3. **Never fabricate to complete a ritual.** The book handoff and any dated first-person instance are gated
   on the **fact-sheet**, hard. An invented book title or an invented "last week we…" is the worst failure
   this pack can produce — and the blind-compare pass proved it is the easiest one to make.
4. **Seams ≠ markers.** A seam (structural humanity, plus the grammar residue of §5.2) is required
   everywhere; a marker (a refrain, an identity beat, a named anecdote) is budgeted and gated. At least 1 in
   3 sections carries zero markers. Boosters are **not** markers.
5. **Reproduce the grammar, never the spelling.** The corpus's `sallet` / `achieving` / `ETAS` are typing
   artifacts, not voice, and are off-limits.
6. **Don't build a clean arc.** No post in the corpus is well-shaped; leave one section that doesn't pull
   its weight.
7. **One named anecdote per piece**, and respect the `burn:` rates in `themes.md`.

## Corpus provenance (raw stylometry in `evidence/`, builder-internal)

| Role | Source | Corpus |
|---|---|---|
| **Style** (idiolect, dials, exemplars) | `davidpotolskilafeta.medium.com` + DataDrivenInvestor, **2020 only** | 5 posts / 3,927 words as profiled (~3,710 body, ~3,150 excluding block-quoted book material) |
| **Substance only** (`themes.md`) | the same Medium, 2022 + 2025 | 3 posts / ~6.4k words |

Pulled via RSS (`content:encoded` full bodies); all 8 items verified `dc:creator = David Potolski Lafeta` —
**no guest reposts to drop.** Corpus directories are gitignored.

## Scope note (honest)

This pack produces content **in David's 2020 register, with AI tells engineered out and facts verified
first** — not an indistinguishable clone. The primary is calibrated from a **small on-register sample: 5
posts, ~3.9k words, one platform, one year, one genre.** There is **no** corpus for long-form beyond ~950
words, for anything code-bearing (0 fenced blocks in the whole target register), for threads, or for video
scripts — a piece in those containers is an extrapolation, and should be treated as one. The voice also
carries a **documented register drift** the pack deliberately does not follow. Lean on the exemplar bank and
the naturalness floor; don't over-promise "it's exactly him." Fidelity grows only as more real on-register
writing is added — never by stretching what is here.

## Build provenance

Built by the persona-builder via the full adversarial method: 5 parallel lens-miners (idiolect · cognition ·
register · personality · substance) → synthesis → **fidelity hawk + generate-and-blind-compare** → refine.
Both judges changed the shipped artifact. The hawk re-verified the draft's counts with Python and corrected
several (the closer recipe is 3/5, not 5/5; the piece ends on `!` in 2/5, not 5/5; 4 em-dashes, not 2) and
demoted six single-post tics that the draft had generalized. The blind-compare found the body was being
written **colder than any real post** (the missing booster warmth), that the seams were arriving decorative
and metronomic rather than structural and clumped, and it **fabricated an anecdote** — which is why
`fabricated-instance-guard` exists. One judge recommendation was **rejected**: a deliberate typo budget.
Reproducing the corpus's misspellings would read as a broken model and can silently corrupt a product name;
the pack reproduces the *grammar*, never the *spelling*.

## Changelog

- **1.0:** Initial build. Primary-only pack (`david.md` + card + `themes.md` + 7 exemplars). 2020 register
  pinned as the voice; 2022/2025 posts admitted as substance-only sources with a translation table for PM
  content. No secondary voices; router documents the deferral.
