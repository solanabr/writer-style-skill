# Process Playbook — building a persona end to end

The full, phase-by-phase process, for both **craft** (secondary/author) and **spine** (primary/your-voice)
personas. Each phase says what to do, what it produces, and how to know it's done. The agent prompts for
the parallel/adversarial steps live in `agent-prompts.md`; the output schemas live in `craft-profile.md`
and `primary-profile.md`.

---

## Phase 0 — Decide the type and the use-case register
- **Type:** craft or spine? (See SKILL.md's inversion table. This decides everything downstream.)
- **Target register:** a writer has *several* registers (formal, casual, technical, personal). Decide
  which one the persona serves. For our skill the target is the **technical-educational** register. The
  spine work proved this matters: the same person's proposal-"we" voice, college-essay voice, and tweet
  voice are different instruments. Pick the one the use-case needs and weight the corpus accordingly.
- Produces: a one-line statement of "persona X, in register Y, for use Z."

## Phase 1 — Corpus: gather & clean (garbage in → garbage out)
1. **Gather** a real, sufficient corpus of first-party writing in the target register. Prefer primary
   sources; weight recent + on-register material; note (and down-weight) off-register or stale material.
   *Thin corpus is the real ceiling.* For a spine, ~dozens of pieces is workable; for a craft author,
   more is better. If an intended source has almost no long-form prose, say so and substitute.
2. **Clean, hard.** This is where most quality is won or lost:
   - Strip boilerplate (nav, subscribe CTAs, legal disclaimers, engagement bars, scrape chrome).
   - Drop non-prose: base64/data-URI images, code blocks (unless code-style is the point), math dumps.
   - **Language-filter** to the target language; mixed-language corpora pollute the voice.
   - **Separate registers**: never blend an author's essays with their tweets in one bucket.
   - Dedupe across mirrors.
   *Why it matters:* in a dirty corpus the loudest "signature" is often the chrome (timestamps, "Reply",
   "Link"), and it will dominate the profile if you don't remove it. Always sanity-check the cleaned
   corpus (e.g. a stylometric profile of signature words). If the top "words" are UI scaffolding, clean again.
- Produces: a clean, register-tagged corpus + a quick numeric profile (sentence-length distribution,
  punctuation rates, signature words/phrases) you'll feed to the miners.

## Phase 2 — Mine: multiple lenses, in parallel, evidence-bound
Spawn several expert "miner" agents at once, each with a *different lens*, each reading the **real corpus**
(not summaries) and returning findings tied to **verbatim quotes and frequency counts**. Never bare
adjectives ("punchy" is useless; "median sentence 12 words; opens 24% of sections with a question" is a
fingerprint).

- **Craft persona, lenses:** (1) learning-science/pedagogy, (2) rhetoric/argumentation, (3) prose craft,
  (4) technical communication, (5) genre/document architecture. Each hunts *transferable craft* and is
  told to **flag idiolect for exclusion**.
- **Spine persona, lenses:** (1) idiolect/stylometric (surface fingerprints **to reproduce**),
  (2) cognitive/brain-patterns (how they think/teach beneath the words), (3) register range + the
  through-line constant across all registers, (4) personality/affect/values. Each is told we **want** the
  quirks.

Prompts for all of these are in `agent-prompts.md`. Run them in parallel; they're independent.
- Produces: several rich, overlapping, evidence-bound findings dumps.

## Phase 3 — Synthesize a draft
Merge the miners, deduping overlaps, into one draft against the right schema (`craft-profile.md` or
`primary-profile.md`). Err on the side of inclusion here. The adversarial phase will cut. Lead with the
signature strength (craft) or the essence prompt-primer (spine). Write the worked example.
- Produces: an "expanded" draft, knowingly over-full.

## Phase 4 — Adversarial judging (never ship a first draft)
This is the heart of the quality. Use the prompts in `agent-prompts.md`.

**Craft persona, two opposed judges, then reconcile:**
- A **ruthless minimalist editor** (cutter): find redundancy, marginal/low-fidelity items, rules that
  would make output formulaic, anything not load-bearing. Targets a leaner doc.
- A **fidelity advocate** (keeper): defend what genuinely changes output; concede its weakest items; and
  crucially **find gaps**: rules stated with no example, high-frequency behaviors under-weighted.
- *Reconcile:* cut what the cutter flags *and* fold in the gaps the advocate finds. The right outcome is
  net-leaner **and** sharper. You both remove bloat and add a few missing concrete exemplars.

**Spine persona, fidelity hawk + a generation test:**
- A **fidelity hawk**: read corpus + draft; report (A) missed/under-weighted authentic features,
  (B) generic/not-them lines to sharpen or cut, (C) over-fit/caricature risks (with dosages), (D)
  naturalness risk, (E) the single most important fix. The hawk often catches over-fit a synthesis can't
  see (e.g., a "tic" that's really a relic of one corpus era).
- A **generate-and-blind-compare** pass: have an agent write a sample piece **from the draft spec alone**
  (a *different* topic than any embedded example), then read the real corpus and diff its own output:
  what rang false/generic/too-tidy, what trait the spec failed to make it reproduce, what dosage was off.
  This is the most powerful validator because it tests the spec *in use*; it surfaces failures (e.g.,
  "calm body" being read as "clean body") that pure critique misses.

- Produces: a reconciled fix list (and, for the spine, a verified "does it generate authentically" verdict).

## Phase 5 — Refine to final
Apply the reconciled fixes. Enforce the quality bar (`quality-bar.md`): evidence-bound, the right
idiolect stance, a worked example, the "what we exclude" note (craft) / naturalness floor (spine). Correct
any over-claimed counts against the corpus. Write the final to `../personas/<name>.md`.
- Done when: a fresh read passes the quality-bar checklist and (spine) the generation test no longer
  reads as a forgery.

## Phase 6 — Router (only when multiple craft personas exist)
A new/changed craft persona changes how content should be routed. (Re)design and **empirically validate**
the router. See `routing-design.md`. Then update `../profiles/kaue/ROUTING.md` and `../SKILL.md`'s backbone table.

---

## Notes on running the agents
- **Parallelize** the independent miners (one message, multiple agent calls). Judges that depend on a
  draft run after it's written.
- **Give agents absolute paths** to the corpus and (for judges) the draft file, and tell them to read the
  *real* files, not work from your summary.
- **Reconcile yourself.** The agents propose; you (the orchestrator) decide and write. Don't let an agent
  grade its own output leniently. That's why the spine uses a *separate* generate step and blind diff.
- **Compute is not the blocker; fidelity is.** Use enough passes. A persona is written once and used
  thousands of times.
