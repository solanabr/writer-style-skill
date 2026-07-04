---
description: "The naturalness floor — write unevenly with a human seam, so output reads like a person not AI. Always applies when writing in-voice."
---

# Naturalness floor (protect above ALL craft)

Every craft, applied thoroughly, **smooths** prose into something that sounds like nobody. Even enthusiasm +
even polish is the **#1 tell** that a machine wrote it. Counter it on every piece.

**Seams are not markers.** A *seam* is structural humanity — a real number from your own use, a named
credit, a confession, a loose run-on. A *marker* is surface idiolect — a catchphrase, a refrain, an
identity beat (see the card's `markers:` budgets). The floor requires a seam in every passage; it never
requires a marker anywhere. A plain section still has a seam; it has **zero markers**. Saturating markers
to "sound human" is the failure mode this file exists to prevent — humanity is the seam and the rhythm,
never the catchphrase.

## The rules

> **Rule 0 — one MOOD per piece.** Declare it before drafting (confessional / dry-competent / mentor-warm
> / hyped-launch / builder-pragmatic…). The mood scales every rule below: seam density, heat topology,
> marker appetite. Humans vary BETWEEN pieces and stay coherent within one; a piece that samples every
> register is uniformity one level up. **A quota met identically in every section is itself the tell** —
> calibration measured a ≤4-word punch in 43/45 generated sections while the real author's punches CLUMP
> (a burst of four, then 800 flat words). Distributions, not metronomes.

1. **Write UNEVENLY.** Long calm, near-documentation-flat stretches, *punctuated* by a hype spike, a zoom-out,
   a verdict, one self-aware seam. Personality lives at the **open, the seams, the verdicts, and the close** —
   not every sentence.
2. **Vary sentence length hard — at PIECE level, with per-section variance.** The piece needs short punches
   (≤4 words) and long runs (≥38 words — numbers live in the card), but they should CLUMP like a human's:
   some sections carry several punches, some carry none and run documentation-flat. Whole-piece stdev must
   clear the card's `burstiness_min`; a couple of individually-flat sections are correct, not a violation.
   Watch the mean too — this voice's sentences run LONG (median ~18, real pieces average 20–40); a piece
   averaging 14-word sentences is clipped, not him.
3. **Calm ≠ clean.** The body is *loose*: run-ons, the occasional comma splice, a dropped article, a clause
   that starts as one thought and lands as another, a mid-sentence hedge ("at least for me," "honestly"). Do
   **not** smooth these out. Over-tidy prose is a bigger tell than over-enthusiasm. In a long piece, real
   damage is allowed: ~one unfixed agreement slip or one list that derails mid-flight per ~1k body words —
   never in code, commands, numbers, or claims. And license **one genuinely off-argument aside per long
   piece** (a personal intrusion that serves nothing) — instrumental-only asides are a tell. But the
   license is not a template: never LABEL the aside ("Complete aside:", "Completely unrelated:"), never
   reuse a flavor across a batch (calibration measured a "domestic quirk" aside cloned into 4/8 pieces),
   and in batch mode only the pieces dealt one get one.
4. **Seams are real, not rationed.** A human seam = a confession, a real number from your own use, a named
   credit, a tool-credit, a "this is running long." Long pieces carry several, SHORT pieces may carry one.
   Don't fill a seam slot per section on schedule — calibration measured a confession in 8/8 pieces, 5/8
   front-loaded, which reads as a quota, because it was one. Zero-confession pieces are allowed. Let "I"
   clump the way humans self-refer — floods and droughts, usually at the edges — not one ration per section.
   Rotate seam TYPES across the piece; never open every section the same way. (Always load the primary's
   `seam` exemplar.)
5. **Spike, then cool — topology by JOB, not one law.** After a spike (caps/emoji/exclamation/vowel-stretch),
   flat competence before the next; two adjacent spikes = the over-enthusiasm tell. For **explainers**:
   edges hot, middle calm. For **teaching/motivation**: mid-piece warmth IS the payload — the instructor
   stays in the room throughout; don't refrigerate the middle of a course opener. One goofy, unguarded
   spike per piece (fan-burst, vowel-stretch, "!" that means it) is licensed — ironized-only enthusiasm is
   a tell.
6. **Vary section SHAPE across the piece.** A near-flat mechanics stretch (zero markers) → a warm-reasoning
   cluster → a short hype/zoom-out seam → flat again — as the piece's mood dictates, not as a fixed cycle.
   Evenness of shape is as much a tell as evenness of enthusiasm; so is a fixed alternation.
7. **The plainness quota.** In a multi-section piece, at least **1 in 3 sections (round up) contains ZERO
   signature markers** — no catchphrases, refrains, identity beats, coined handles, or civilizational
   analogies. Its seam is structural: a real number, a credit, a loose run-on. If every section carries
   markers, the voice is a stamp, not a person. (Serious registers may run marker-free end to end — the
   voice at rest is also the voice.)

## Why
This is the one instruction that fights the model's own pull toward uniform polish. It is what separates
"authentic voice" from "competent AI." When the routed craft and this floor conflict, **the floor wins** —
dosage, not saturation. Pull craft at the positions that need it; leave routine stretches plain and a little
loose.

## How it's enforced
Four checks, not vibes:
- **Pass B.5 blind-compare** (write-time): re-read the draft against the loaded humane exemplars and ask
  "him, or a rule-follower?"; regenerate toward felt-pain + uneven rhythm + rotating seams if it reads even.
- **The marker ledger** (write-time, long-form): the writer keeps a per-section ledger of seam types and
  marker spends against the card's `markers:` budgets — see the long-form mode in `../writing-workflow.md`.
  Rotation and the plainness quota are checked on the ledger, not on memory.
- **Deslop pass**: `../rules/deslop.md`: strip AI-cliché *clusters* (the lint flags them with plain-word
  swaps) and run the paragraph-reshuffle / "what's new here" / read-aloud tests, without sanding off the
  specific detail, mixed feelings, and asides that read as human.
- **The validator**: `validate_voice.py tells --card <voice>.card.yaml` fails any output whose
  sentence-length stdev is below the card's `burstiness_min` (the quantitative form of "write unevenly");
  `density --card <voice>.card.yaml --facts <sheet>` enforces the marker budgets + context gates;
  `audit --file <doc>` catches section-to-section repetition in one long piece. The em-dash cap is a
  *guardrail*, not a voice signal — burstiness is the real target.
