# Authoring a Voice — the build method (index)

How the voices in a pack are actually built: an **adversarial, multi-pass, evidence-bound process**, not a
one-shot "describe the style." Follow it to add or rebuild a voice at the same quality bar. The process is
deliberately heavy because the alternative (a shallow, vibes-based style sketch) is exactly what produces
generic, forgeable output. Compute spent here pays off on every future generation.

This is read by the **persona-builder** agent (and by you, when adding a voice). For *using* an existing pack
to write, you don't need any of this — see `SKILL.md`.

## First, know which of TWO voice types you're building — they invert one rule

| | **SECONDARY voice** (a borrowed-craft "author") | **PRIMARY voice** (the target author's own) |
|---|---|---|
| Goal | borrow an author's *transferable craft* to write **original** work | reproduce *the target's* voice so output sounds authentically like them |
| Idiolect (punctuation tics, signature phrases, rituals, coined terms, persona) | **STRIP it**: capturing fingerprints makes output a pastiche; keep only *how they think/teach/structure* ("quality, not quirks") | **REPRODUCE it**: the quirks are the asset; they're what make it *them* |
| Ends with | a "What this deliberately EXCLUDES" note + a worked example in **neutral** voice | a naturalness floor (uneven texture + human seam) + a worked example in **the target's** voice |

Getting this inversion wrong is the single most common failure. A secondary voice that keeps idiolect produces
impersonation; a primary voice that strips it produces a "well-behaved impostor." Decide the type first.

## The workflow (each phase has a reference — read it when you reach that phase)

1. **Corpus → gather & clean.** Collect a real, sufficient corpus; clean it hard (strip boilerplate, dedupe,
   separate registers, language-filter, drop non-prose, **drop guest reposts by other authors**). Garbage
   corpus → garbage voice; the loudest "signal" in a dirty corpus is often scrape chrome. The profiler
   (`tools/profile_corpus.py`) does the cleaning and emits a builder-internal `evidence/<voice>.profile.json`
   plus `card_suggestions`. → `method/process-playbook.md` (Phase 1)
2. **Mine: multiple lenses, in parallel.** Spawn several expert "miner" agents, each a different lens
   (pedagogy, rhetoric, prose, technical-comms, genre, or for a primary: idiolect, cognitive-patterns,
   register, personality). Each reads the *real* corpus and returns **evidence-bound** findings (quotes +
   counts), not adjectives. → `method/agent-prompts.md` (Miners)
3. **Synthesize a draft** against the right schema. → `method/craft-profile.md` (secondary) *or*
   `method/primary-profile.md` (primary). Derive the **style-card** dials from `card_suggestions` +
   judgment; curate the **exemplar bank**. → `style-card-schema.md`
4. **Adversarial judging.** Never ship a first draft.
   - *Secondary:* a **ruthless cutter** vs a **fidelity advocate**; reconcile (cut bloat, fold in the gaps).
   - *Primary:* a **fidelity hawk** (find missed/over-fit/generic against the corpus) **and** a
     **generate-and-blind-compare** pass (write a sample from the draft alone, diff it against the real
     corpus — catches what critique misses). → `method/agent-prompts.md` (Judges)
5. **Refine to final**: apply the reconciled fixes; enforce the quality bar. → `method/quality-bar.md`
6. **(Re)design & validate the router**: which voice leads for which job, how they stack, the cap. Design it
   adversarially, then **validate empirically** by routing real topics through it. → `method/routing-design.md`

## The non-negotiables (full list + checklists in `method/quality-bar.md`)
- **Evidence-bound, not vibes**: every claim ties to a corpus quote or a count.
- **Strip-idiolect (secondary) / reproduce-idiolect (primary)**: the inversion above.
- **Actionable, not forensic**: the style-card exposes only dials a writer can act on; raw stylometry stays
  in `evidence/` for the builder and validator, never the writer.
- **Adversarial, multi-pass** — miners → judges → (for primary) generate-and-blind-compare. One pass is not enough.
- **Worked example + exemplar bank**: prove the voice *generates*, not just *describes*.
- **Protect naturalness** (primary): uneven texture, a human seam per passage; even-tidiness is the tell.

## Output location & shape
- **Primary:** `profiles/<pack>/<name>.md` + `<name>.card.yaml` + `exemplars/<name>/` (7 slots).
- **Secondary:** `profiles/<pack>/secondary/<name>.md` + `<name>.card.yaml` + `exemplars/<name>/` (~3 move-demos).
- Raw numbers: `profiles/<pack>/evidence/<name>.profile.json` (builder-internal).
Match the section shape of the existing profiles. If you added/changed a secondary, update the pack's
`ROUTING.md` and the lane table in `SKILL.md`, then run the router validation (Phase 6).

> Reference files are detailed; read the one for your current phase rather than all of them up front.
