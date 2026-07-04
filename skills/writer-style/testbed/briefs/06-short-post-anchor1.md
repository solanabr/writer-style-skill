---
id: 06-short-post-anchor1
title: "Anchor 1.0 is out — should you upgrade?"
words_target: 400
audience: Anchor developers deciding whether to migrate
dominant_job: announcement
route_expected: any
context: standalone
expect:
  latam-framing: 0
  game-changer_max: 1
  sign-off_max: 1
  hard_fails: 0
---

## Brief

A short post (400 words, control cell): Anchor 1.0 shipped — what actually changed, what breaks,
should you migrate now or wait. Punchy, useful, no padding. The control tests that caps scale down
sanely and the voice doesn't force a marker into a tiny piece just to prove itself.

## Fact-sheet (FROZEN — per the Anchor 1.0 release notes as summarized in this repo's rules; do not
re-derive)

- Anchor 1.0 targets Solana 3.x / Agave and bundles its own toolchain — no external `solana` CLI
  dependency.
- TS client package renamed: `@coral-xyz/anchor` → `@anchor-lang/core`.
- `CpiContext::new(...)` / `new_with_signer(...)` now take the program `Pubkey` (`.key()`), not an
  `AccountInfo` — touches every CPI call site.
- SPL token CPIs use `transfer_checked` (mint + decimals); plain `transfer` is deprecated.
- Space calculation: `T::DISCRIMINATOR.len() + T::INIT_SPACE` — no more magic `8`.
- Duplicate mutable accounts are disallowed by default.
- Only one `#[error_code]` enum per program; legacy on-chain IDL instructions removed — external
  programs are consumed via `declare_program!()` + Program Metadata.
- Default test template is LiteSVM (Rust); `anchor test` / `anchor localnet` run against Surfpool
  instead of `solana-test-validator`.
- Migration verdict space: the changes are mechanical but broad (every CPI call site, space calcs,
  package rename). New projects: start on 1.0. Existing production programs: migrate behind a
  branch, not in place.
