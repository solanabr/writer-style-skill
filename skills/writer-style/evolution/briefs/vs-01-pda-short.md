---
id: vs-01-pda-short
title: "Video short: what a PDA actually is"
container: video-script-short
words_target: 180
audience: devs scrolling shorts/reels who've cargo-culted PDAs
dominant_job: demystify
route_expected: hotz
context: standalone
expect:
  latam-framing: 0
  sign-off_max: 1
  game-changer_max: 1
  hard_fails: 0
---

## Brief

A script for a 60–90 second vertical video (YouTube Short / Reel), ~150–220 spoken words: "what
is a PDA, actually." One idea, deflated to its true simple model: an address computed from seeds
that has no private key, so the program itself is the only thing that can sign for it. Spoken
words only — if a sentence can't be said in one breath, split it. Visual/beat directions in
brackets per `formats/video-script.md`. Hook lands inside the first 2 seconds.

## Fact-sheet (FROZEN — per this repo's anchor.md rules; do not re-derive)

- A PDA is derived from seeds + the program ID. It is off-curve: no private key exists for it.
- Because no key exists, no user can ever sign as the PDA; the owning program signs for it via
  the seeds (+ bump) in `invoke_signed`.
- `find_program_address` searches bump values (from 255 downward) for the first off-curve
  address; that bump is the canonical bump.
- Store the canonical bump once and reuse it — recalculating costs ~1,500 CU per access.
- The payoff is deterministic addressing: anyone can compute where user X's vault lives from the
  seeds alone — no registry, no lookup table.
