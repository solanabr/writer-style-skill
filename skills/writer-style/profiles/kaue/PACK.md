# PACK — kaue

> Voice pack for original educational Solana/blockchain content in **Kaue's** (Superteam Brazil) voice.
> Headline use case: long-form technical Solana explainers and course material.

- **name:** kaue
- **license:** MIT — Superteam Brazil / Kaue.
- **entry:** `../../SKILL.md` (the engine) · **router:** `ROUTING.md`
- **primary:** `kaue.md` (+ `kaue.card.yaml`): always-on; reproduces idiolect; **not** counted toward the cap

## Primary voice (always on, free)
- **kaue.md:** Kaue, Superteam Brazil. The tone, rhythm, brain-patterns, and the uneven-human seam. Owns the
  naturalness floor; protected above all secondary craft. Register: Medium technical-guide.

## Secondary voices (selected by the piece's dominant job; cap = backbone 1 + guest ≤1)

| voice | lane (axis) | leads | scope header (top of profile) |
|---|---|---|---|
| **helius** | structure & evidence | practical how-to / integration / reference; universal guest | "Show how the documented thing works: the real struct/number, every claim checkable." |
| **vitalik** | derivation, sustained | deep tech / protocol internals / mechanism design | "Derive from first principles AND keep going: tradeoffs, failure modes; never stop at the one-liner." |
| **balaji** | framing & scope | broad / interconnected theses; also opener-guest | "Frame the whole domain: anchor analogy, auditable pillars, historical lineage." |
| **hayes** | engagement & stamina | macro / markets / geopolitics / tokenomics / crowd-psychology | "Carry length on one organizing metaphor: forces-as-actors, stakes, falsifiable close." |
| **hotz** | compression & collapse | demystification (honest "X is just Y") | "Collapse to one clean honest model, then STOP — if it needs an asterisk, it's Vitalik's." |

Each voice is a **full backbone in its lane** — none is positionally restricted. The lanes self-differentiate;
there are **no author-vs-author special-case rules**. Full triggers/anti-triggers in `ROUTING.md`.

## Invariants (the non-negotiables)
1. **Primary always on, uncounted.**
2. **Cap = 2 secondary layers** (backbone + ≤1 guest); 3 only for 3,000+ words, segregated; else split.
3. **Stack only across different lanes;** never two voices on one axis (esp. vitalik + hotz).
4. **Original, never impersonation:** secondary idiolect stripped; only Kaue's idiolect reproduced.
5. **Helius is the universal guest;** security routes to helius/vitalik, **never hotz**.
6. **Facts first, voice last:** verify technical content before styling; voice never alters a number/code.
7. **Protect the uneven human seam above all craft** — dosage, not saturation.

## Corpus provenance (per voice; raw stylometry in `evidence/`, builder-internal)
| voice | source | corpus (after cleaning) |
|---|---|---|
| kaue | Superteam/Medium technical guides, **on-register only** | 4 pieces / ~6.5k words |
| helius | Lostin + 0xIchigo (Helius blog) | 93 pieces / ~358k words |
| vitalik | vitalik.eth.limo essays | 390 pieces / ~738k words |
| balaji | Balaji long-form (19 guest-reposts excluded) | 87 pieces / ~167k words |
| hayes | Arthur Hayes essays | 76 pieces / ~318k words |
| hotz | George Hotz writing | 128 pieces / ~91k words |

Corpus was re-cleaned before profiling: HTML artifacts, newsletter/footer chrome, and guest-reposts by other
authors removed. Secondary idiolect is **stripped** in the profiles (only transferable craft is kept).

## Scope note (honest)
This pack produces content **in Kaue's register, with AI tells engineered out and facts verified first** — not
an indistinguishable clone. The primary voice is calibrated from a **small on-register sample (4 posts)**;
fidelity is corpus-bounded and grows as more of Kaue's on-register technical writing is added. Lean on the
exemplar bank (`exemplars/kaue/`) and the naturalness floor; don't over-promise "it's exactly him."

## Changelog
- **2.0:** Generalized engine + `kaue` default pack. Renamed spine→primary (`kaue.md`), craft→secondary.
  Subject-lane roster with scope headers (each a full backbone, Balaji no longer opener-only; Hayes spans
  macro/geopolitics/psychology, not just economics). Removed the Vitalik-vs-Hotz special rule (now inherent to
  the lanes). Data layer rebuilt: writer-facing **style-cards** + **exemplar banks**; raw stylometry walled
  off to `evidence/`. Facts-first workflow added. LoRA lane dropped.
