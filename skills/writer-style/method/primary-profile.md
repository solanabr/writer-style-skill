# Spine Profile schema (the primary / "your own voice" persona)

The spine is the always-on voice the whole system writes in. **Inversion from craft profiles: here you
REPRODUCE the idiolect** — the quirks, rhythm, and brain-patterns are the asset that makes output sound
like the person and not generic. The craft layer rides *on top* of this voice.

## The two things that make or break a spine

**1. Reproduce idiolect — but at the right dose, in the right register.**
Capture the surface fingerprints (sentence rhythm, punctuation habits, signature words/openers/closers,
formatting, emoji/slang) *and* mark their **dosage by context**. The dosage lesson is hard-won: a
person's *tweets* are far denser in slang/emoji than their *guides*; calibrating a course to tweet-density
produces cosplay. Pin the **target register** (e.g., their technical-guide voice), put enthusiasm/slang at
the **edges** (intros, transitions, sign-offs), and keep the explanatory **body calm and clean of
chrome**.

**2. The naturalness floor — this is what separates "is them" from "studied them."**
A rules-following model defaults to uniform, tidy, evenly-enthusiastic prose. Real voices aren't like
that. The spine MUST encode:
- **Write unevenly.** Bimodal texture: calm, almost-flat technical stretches *punctuated* by hype spikes,
  a zoom-out, a verdict. Do not distribute enthusiasm evenly.
- **Calm ≠ clean.** The body prose is *loose*: run-ons, the occasional hedge mid-sentence, a clause that
  starts as one thought and lands as another. Don't smooth it. Perfectly groomed prose is a *bigger* tell
  than over-enthusiasm. Vary *cleanliness*, not just enthusiasm.
- **A human seam in every passage**: a first-person confession, a real number from experience, a
  collaborator credited, a mid-flow aside ("this is running long, let me wrap"). Its absence is the
  single fastest way output reads "studied them." This was discovered via the generate-and-blind-compare
  test. Critique alone won't surface it, so always run that test (see `agent-prompts.md`).

## Section schema (match `personas/_spine-*.md`)

1. **Header**: this is the voice; idiolect is reproduced (not stripped). State the **target register**
   and what's off-register (e.g., the institutional "we", the tweet-slang body).
2. **The essence / prompt-primer**: one tight paragraph capturing the *stance* (e.g., "a build-in-public
   engineer narrating his own decisions; pain-first; always names the trade-off"). This is what to prime a
   model with; the rest elaborates.
3. **How you teach (the cognitive engine)**: the load-bearing brain-patterns as a numbered list: the
   hook style, how they build/structure, how they motivate, analogy instinct, the recurring "thinking
   tics," the close.
4. **How you sound (idiolect, reproduce)**: surface fingerprints with examples: openers, the
   sentence/question rhythm, parentheticals, list habits, signature phrases, sentence-length whiplash,
   verdict lines. Mark which are core (cross-register) vs edge-only.
5. **Surface, formatting & dosage**: concrete dosages calibrated to the **target register** (exclamation/
   parentheses/colon rates; emoji and slang budgets and *where* they're allowed; ALL-CAPS rate excluding
   acronyms; signature openers/closers).
6. **Naturalness floor**: the uneven-texture / calm≠clean / human-seam rules above. Mark this as the
   layer that decides authenticity.
7. **Register dial + standardization**: the target register; how to dial up/down by context; what
   off-register voice to avoid; language notes (e.g., writes in fluent English by choice — keep it
   English, don't insert their L1).
8. **Values & worldview**: the convictions that color framing and examples (delivered as their specific
   behaviors, not the adjective "warm").
9. **Author-overlap calibration**: where the spine overlaps each craft persona (lean that craft heavier —
   it's congruent) and the **guardrail** at each divergence (what keeps blended output *theirs*, e.g.
   "stay a peer, not a prophet"). This is what makes the router's blends harmonize with the voice.
10. **The distinguishing fingerprint**: the combination that is unmistakably them (no single craft author
    has all of it).
11. **A worked example IN THEIR VOICE**: short, demonstrating the uneven texture + a human seam +
    edge-concentrated enthusiasm. Annotate the moves.

## Quality checks specific to spine profiles
- Run the **generate-and-blind-compare** test (write a fresh sample from the spec alone, diff vs corpus).
  If the sample reads as a "well-behaved impostor" — tidy, even, seamless — the naturalness floor is too
  weak. Strengthen §6 (especially calm≠clean and the per-passage seam) and re-test.
- Are dosages calibrated to the **target register** (the guides), not the tweets? Slang/emoji should be
  near-zero in the body.
- Are signature words/phrases *real content*, not scrape chrome? (Re-profile the cleaned corpus to be sure.)
- Did the fidelity hawk's over-fit flags get demoted/capped? (A tic inflated by an off-register era is a
  trap: e.g., a college-essay relic that's rare in the target register.)
- Does §9 (author-overlap) exist? Without it the craft layer won't harmonize with the voice.

## Anti-patterns
- Stripping idiolect (that's the craft-profile rule, wrong here).
- Tweet-calibrated dosage in a guide register (cosplay).
- A clean, even, polished spec with no naturalness floor → "well-behaved impostor" output.
- Describing voice with "warm/authentic/engaging" instead of the specific behaviors that create it.
