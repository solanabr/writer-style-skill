---
id: bp-02-anchor-vs-pinocchio
title: "Blog: Anchor vs Pinocchio — when the macro is worth it"
container: blog-post
words_target: 900
audience: Solana devs who've heard "Pinocchio is faster" and wonder if they're doing it wrong
dominant_job: demystify
route_expected: hotz
context: standalone
expect:
  latam-framing: 0
  sign-off_max: 1
  game-changer_max: 1
  civilizational-analogy_max: 1
  hard_fails: 0
---

## Brief

A blog post (~900 words) demystifying the framework choice: what Anchor's macros actually buy,
what Pinocchio actually is (doing the same checks by hand, without the scaffolding), and the
honest decision rule. Collapse the hype to the true simple model without dismissing either tool —
inviting, not smug. Load `formats/blog-post.md`.

## Fact-sheet (FROZEN — per this repo's anchor.md / pinocchio.md rules; do not re-derive)

- Pinocchio achieves 80–95% CU reduction vs Anchor via zero-copy account access, no external
  dependencies, and minimal binary size.
- Pinocchio is manual: account validation is hand-written `TryFrom` impls (owner check, signer
  check, PDA check), single-byte discriminators (vs Anchor's 8-byte), field-by-field
  serialization or carefully-checked casts.
- Anchor buys: `#[derive(Accounts)]` constraint enforcement, IDL generation (and client
  generation from it), `declare_program!()` for consuming other programs, a bundled toolchain
  (1.0 needs no external `solana` CLI), the LiteSVM default test template.
- Both sides test the same way in-process: LiteSVM / Mollusk — not `solana-test-validator`.
- The security burden inverts: Anchor's constraints make the missing-check bug harder to write;
  Pinocchio makes every check your problem (and every check visible).
- Honest decision space: default Anchor; Pinocchio when CU limits are actually being hit, when
  transaction costs at scale are material, or when binary size must be minimal. "Faster" is not a
  reason if you never measured your CU.
