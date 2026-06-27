# The quality bar

The non-negotiable principles, plus ready-to-use checklists and a catalog of the failure modes this
process exists to prevent. A persona that meets this bar will produce content that sounds like a real
person and reads as original; one that doesn't will produce generic, forgeable, or pastiche output.

## The principles (why each matters)
1. **Evidence-bound, not vibes.** Every claim ties to a verbatim quote or a frequency count from the real
   corpus. Adjectives ("punchy", "rigorous") are unactionable and usually wrong; mechanisms and numbers
   are reproducible. If you can't cite it, you're guessing.
2. **The idiolect inversion, applied correctly.** Craft → strip idiolect, keep transferable craft.
   Spine → reproduce idiolect. Getting this backwards is the #1 failure (pastiche, or an impostor voice).
3. **Adversarial & multi-pass.** Mine with several lenses → judge with opposed critics → (spine) prove it
   with a generate-and-blind-compare. A single synthesis pass overfits, over-claims, and misses gaps. The
   judges routinely catch things the synthesis can't see — inflated tics, generic filler, naturalness
   failures.
4. **Reconcile, don't rubber-stamp.** The orchestrator decides; agents propose. The right outcome of the
   craft cut is *leaner AND sharper* (remove bloat, add the gaps the advocate found). Don't let a
   generator grade its own work.
5. **Worked example, always.** A persona must *generate*, not just *describe*. The example proves it — and
   in the right voice (craft → neutral, to prove separability; spine → their voice, to prove fidelity).
6. **Protect naturalness (spine).** Uneven texture, calm≠clean, a human seam per passage. Even-tidiness is
   the tell that betrays AI authorship faster than over-enthusiasm.
7. **Lean where lean works, deep where depth changes output.** Don't pad; don't over-specify into
   formulaic rules. Cut shared/generic craft hard; spend the words on the distinctive, output-changing moves.
8. **Compute is not the blocker; fidelity is.** A persona is written once, used thousands of times. Spend
   the passes.

## Checklist — CRAFT profile
- [ ] Leads with the author's distinctive **signature strengths** (not "explains clearly").
- [ ] Every section is a **mechanism or a number**, not an adjective.
- [ ] **No idiolect** kept; a "What this EXCLUDES" note lists the fingerprints to avoid.
- [ ] A **worked example in neutral voice** that a fan of the author could NOT attribute to them.
- [ ] Survived the **cutter + advocate** pass: leaner than the draft *and* the advocate's gap-examples folded in.
- [ ] Any frequency claims **verified against the corpus**.
- [ ] Distinctive vs the other personas (over-cut the shared craft).

## Checklist — SPINE profile
- [ ] **Idiolect reproduced** (not stripped); dosages calibrated to the **target register** (not the
      densest register).
- [ ] A tight **essence/prompt-primer** paragraph capturing the stance.
- [ ] **Naturalness floor** present and strong: write-unevenly, calm≠clean, **human seam per passage**.
- [ ] **Author-overlap calibration** section (congruence + guardrails) so the craft layer harmonizes.
- [ ] Signature words/phrases are **real content**, not scrape chrome (re-profiled the cleaned corpus).
- [ ] Fidelity hawk's **over-fit flags demoted/capped** (no off-register relics elevated to fingerprints).
- [ ] Passed the **generate-and-blind-compare** test — the sample doesn't read as a "well-behaved impostor."
- [ ] A **worked example in their voice** showing the uneven texture + a seam.

## Checklist — ROUTER (multi-persona)
- [ ] Routes on **dominant job, not topic**.
- [ ] Each persona mapped to an **axis**; stacking only across axes; **2-layer cap** stated.
- [ ] A **disambiguation rule** for any two similar personas (+ tie-break).
- [ ] Jobs the **spine should own alone** identified (e.g. pure motivation).
- [ ] **Empirically validated** on ~14 real topics; breakages patched.
- [ ] **SKILL.md and the routing doc agree** (no read-alone mis-route).
- [ ] Failure modes listed, ranked by damage.

## Failure-mode catalog (what goes wrong without this process)
- **Pastiche**: a craft profile kept the author's idiolect → output is recognizably "them," not original.
- **Well-behaved impostor**: a spine that's too clean/even/seamless → competent but obviously AI.
- **Scrape-chrome voice**: a dirty corpus made UI scaffolding ("Reply", "UTC") the loudest "signature."
- **Cosplay**: tweet-density slang/emoji applied to a guide register.
- **Adjective soup**: "witty, clear, engaging", describes nothing an agent can act on.
- **Inflated tic**: a relic of one corpus era/genre elevated to a fingerprint (caught by the hawk).
- **Over-fit caricature**: rigid per-section quotas ("one joke per section") → parody.
- **Bloat**: a profile so long the model skims it; or so comprehensive it's indistinguishable from others.
- **Lumped personas**: two similar craft profiles with no disambiguation rule → arbitrary routing.
- **Topic-routing**: routing on subject instead of the piece's job → wrong craft for the goal.
- **Guardrail leak**: a persona's edge (cynicism, grandiosity, dismissiveness) bleeds into the voice.
- **Over-stacking**: 3+ craft layers crowd out the spine's human seam.
- **Single-pass**: no adversary, no generation test → all of the above ship undetected.

## The one test that catches the most
For a **spine**, the generate-and-blind-compare is the highest-value check — it tests the spec *in use*
and exposes naturalness failures critique misses. For a **craft** profile, the "could a fan attribute the
neutral worked example to the author?" test catches retained idiolect. For a **router**, routing ~14 real
topics catches the gaps. When in doubt, run the test, not another read.
