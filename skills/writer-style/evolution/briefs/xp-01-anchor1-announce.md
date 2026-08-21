---
id: xp-01-anchor1-announce
title: "X post: Anchor 1.0 is out"
container: x-post
words_target: 55
audience: Solana developers scrolling the feed
dominant_job: announcement
route_expected: any
context: standalone
expect:
  latam-framing: 0
  sign-off_max: 1
  game-changer_max: 1
  hard_fails: 0
---

## Brief

A single X post (≤280 characters, one post, no thread) announcing that Anchor 1.0 shipped and
telling a working Anchor dev the one thing they must know before upgrading. Pick ONE angle — a
tweet that tries to carry three release notes carries none. Load `formats/x-post.md`.

## Fact-sheet (FROZEN — imported from testbed/briefs/06-short-post-anchor1.md; do not re-derive)

- Anchor 1.0 targets Solana 3.x / Agave and bundles its own toolchain — no external `solana` CLI
  dependency.
- TS client package renamed: `@coral-xyz/anchor` → `@anchor-lang/core`.
- `CpiContext::new(...)` / `new_with_signer(...)` now take the program `Pubkey` (`.key()`), not an
  `AccountInfo` — touches every CPI call site.
- SPL token CPIs use `transfer_checked`; plain `transfer` is deprecated.
- Migration verdict space: changes are mechanical but broad. New projects: start on 1.0. Existing
  production programs: migrate behind a branch, not in place.
