---
id: ca-02-anchor-migration
title: "Community post: Anchor 1.0 heads-up for our repos"
container: community-announcement
words_target: 170
audience: community devs with active Anchor projects
dominant_job: announcement
route_expected: any
context: standalone (dev channel of the community; readers maintain real projects)
expect:
  latam-framing: 0
  sign-off_max: 1
  game-changer_max: 1
  hard_fails: 0
---

## Brief

A dev-channel heads-up (~150–200 words): Anchor 1.0 is out, here's what breaks and what the
community's own project repos should do about it. Practical, calm, zero release-notes-copypaste
energy — the value is the triage (what to do this week vs what can wait). Format rules in
`formats/community-announcement.md`.

## Fact-sheet (FROZEN — imported from testbed/briefs/06-short-post-anchor1.md; do not re-derive)

- Anchor 1.0 targets Solana 3.x / Agave and bundles its own toolchain — no external `solana` CLI
  dependency.
- TS client package renamed: `@coral-xyz/anchor` → `@anchor-lang/core`.
- `CpiContext::new(...)` / `new_with_signer(...)` now take the program `Pubkey` (`.key()`) — 
  touches every CPI call site.
- SPL token CPIs use `transfer_checked`; plain `transfer` is deprecated.
- Space calc: `T::DISCRIMINATOR.len() + T::INIT_SPACE` — no more magic `8`.
- `anchor test` now runs against Surfpool; default test template is LiteSVM (Rust).
- Verdict space: changes are mechanical but broad. New projects: start on 1.0. Existing
  production programs: migrate behind a branch, not in place.
