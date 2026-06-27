# The two-layer model (engine — pack-neutral)

Every voice pack has the same shape: **one primary voice + N secondary voices + a router.** This file explains
the model; a pack (e.g. `profiles/kaue/`) supplies the actual content.

## Primary vs secondary — the inversion

| | **PRIMARY voice** | **SECONDARY voices** |
|---|---|---|
| What | the target author's own voice (e.g. Kaue) | transferable *craft* borrowed from master writers |
| Idiolect (tics, signature phrases, rituals, coined terms) | **REPRODUCE it**: the quirks are the asset; they make it *them* | **STRIP it**: keeping fingerprints makes output a pastiche; keep only *how they think/teach/structure* |
| On | **always** (every piece) | **routed**: one leads, ≤1 guests, by the piece's job |
| Counted toward the cap | **no** (free) | **yes** |
| Goal | output sounds authentically like the author | borrow craft to write **original** work, in the author's voice |

**Getting the inversion backwards is the #1 failure.** Strip the primary's idiolect → a "well-behaved
impostor" (correct, generic, not them). Keep a secondary's idiolect → impersonation (the piece reads like a
George Hotz impression instead of Kaue using Hotz's compression). Every secondary profile ends with a "What
this deliberately EXCLUDES" note — that is the firewall; honor it.

## Original, never impersonation

The secondaries are **craft, not costume.** You apply Vitalik's *derivation method* or Hayes's *stamina
engineering*, not their punctuation, slogans, or persona. The output is the author's own writing that happens
to be well-structured/well-argued/well-paced, not a blend of other people's voices. See
`rules/original-not-impersonation.md`.

## The cap (why it exists)

```
budget = primary (free, always on, NOT counted)
       + backbone (1)
       + guest   (≤1, on a DIFFERENT lane)
       = at most 2 secondary layers
```

3 layers only for 3,000+ word pieces with physically segregated sections; a wish for a third usually means
**split the piece.** Past two layers, the primary's human seam and uneven texture get crowded out — and that
uneven, seam-bearing texture is exactly what makes it sound like a person. The cap protects the naturalness
floor under combination. Never co-lead two voices on the **same** lane (e.g. Vitalik's sustained derivation +
Hotz's abrupt collapse on the same point = incoherence).

## How a pack plugs in

A pack is a directory under `profiles/<pack>/`:

```
profiles/<pack>/
  PACK.md                 # manifest: primary, roster, lanes, routing, invariants, provenance, scope
  <primary>.md            # the primary voice (reproduced idiolect) — always on
  <primary>.card.yaml     # its actionable dials
  ROUTING.md              # the full router for this pack
  secondary/<v>.md        # each secondary's craft (idiolect stripped) + <v>.card.yaml
  exemplars/<v>/          # few-shot move-demos (primary: 14 files / 7 slots; secondary: ~3)
  evidence/<v>.profile.json   # builder-internal raw stylometry (writer never reads)
```

The **engine** (`skills/writer-style/`) is pack-agnostic: it knows about primary/secondary, the cap, the workflow, and the
data-layer schema, never about a specific author. Swap the pack to write in a different voice; build a new
pack with the **persona-builder** (`authoring-personas.md`). The default pack is `kaue`.

## What each artifact is for (no duplication)

- **`<voice>.md`**: register-grounded craft prose. The *why* and *how* of the moves. No numbers.
- **`<voice>.card.yaml`**: the actionable dials (ranges/enums) + favor/avoid lists + AI-tell caps. The
  writer/validator membrane. No prose, no passages.
- **`exemplars/<voice>/`**: the actual annotated passages. The *show*, not the *tell*. The strongest signal.
- **`evidence/<voice>.profile.json`**: raw stylometry, **builder/validator-only**, never the writer.

See `style-card-schema.md` for the schemas and the builder/writer/validator boundary.
