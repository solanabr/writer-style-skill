---
description: "The naturalness floor — write unevenly with a human seam, so output reads like a person not AI. Always applies when writing in-voice."
---

# Naturalness floor (protect above ALL craft)

Every craft, applied thoroughly, **smooths** prose into something that sounds like nobody. Even enthusiasm +
even polish is the **#1 tell** that a machine wrote it. Counter it on every piece:

## The rules
1. **Write UNEVENLY.** Long calm, near-documentation-flat stretches, *punctuated* by a hype spike, a zoom-out,
   a verdict, one self-aware seam. Personality lives at the **open, the seams, the verdicts, and the close** —
   not every sentence.
2. **Vary sentence length hard.** ≥1 short punch (≤~5 words) and ≥1 long run (≥~35 words) per section. The
   spread is the signal. The validator's `uniform-cadence` check fails prose whose sentence-length stdev is
   too low.
3. **Calm ≠ clean.** The body is *loose*: run-ons, the occasional comma splice, a dropped article, a clause
   that starts as one thought and lands as another, a mid-sentence hedge ("at least for me," "honestly"). Do
   **not** smooth these out. Over-tidy prose is a bigger tell than over-enthusiasm.
4. **A human seam in EVERY passage, and rotate the TYPE.** A confession → a real number from your own use → a
   collaborator credited by first name → a tool-credit → a mid-flow "this is running long, let me wrap." Never
   open every section the same way. (Always load the primary's `seam` exemplar.)
5. **Spike, then cool.** Spike (caps/emoji/slang/exclamation/a vowel-stretch) **only** at the edges; after a
   spike, ~100–200 words of flat competence before the next. Two adjacent spikes = the over-enthusiasm tell;
   the *contrast* is the voice.
6. **Vary section SHAPE, not just enthusiasm.** Alternate a near-flat mechanics stretch (zero markers) → a
   warm-reasoning cluster → a short hype/zoom-out seam → flat again. Evenness of shape is as much a tell as
   evenness of enthusiasm.

## Why
This is the one instruction that fights the model's own pull toward uniform polish. It is what separates
"authentic voice" from "competent AI." When the routed craft and this floor conflict, **the floor wins** —
dosage, not saturation. Pull craft at the positions that need it; leave routine stretches plain and a little
loose.

## How it's enforced
Three checks, not vibes:
- **Pass B.5 blind-compare** (write-time): re-read the draft against the loaded humane exemplars and ask
  "him, or a rule-follower?"; regenerate toward felt-pain + uneven rhythm + rotating seams if it reads even.
- **Deslop pass**: `../rules/deslop.md`: strip AI-cliché *clusters* (the lint flags them with plain-word
  swaps) and run the paragraph-reshuffle / "what's new here" / read-aloud tests, without sanding off the
  specific detail, mixed feelings, and asides that read as human.
- **The validator's `uniform-cadence` floor**: `validate_voice.py tells --card <voice>.card.yaml` fails any
  output whose sentence-length stdev is below the card's `burstiness_min` (the quantitative form of "write
  unevenly"). The em-dash cap there is a *guardrail*, not a voice signal — burstiness is the real target.
