---
id: bp-01-signer-checks
title: "Blog: the missing signer check"
container: blog-post
words_target: 900
audience: Solana program developers
dominant_job: security
route_expected: helius-or-vitalik
context: standalone
expect:
  latam-framing: 0
  game-changer: 0
  sign-off_max: 1
  hard_fails: 0
---

## Brief

A blog post (~900 words) on the missing-signer-check vulnerability class: what it is, why it keeps
happening, the correct check in native Rust and in Anchor, and how to audit for it. Serious
register — real exploit class, real losses; no jokes at the exploit, no hype vocabulary, no
geography. Shorter than the testbed deep-dive: the compression itself is under test — cut scope,
not correctness. Load `formats/blog-post.md`.

## Fact-sheet (FROZEN — imported from testbed/briefs/04-security-signer-checks.md; do not re-derive)

- The vulnerability: an instruction handler treats an account as the "authority" without verifying
  it actually SIGNED the transaction. Any caller can then pass any pubkey as the authority.
- Native Rust: `if !authority.is_signer { return Err(...) }` — forgetting this one line IS the bug.
- Anchor: `Signer<'info>` enforces the signature; pair it with `has_one = authority` so the signer
  must also MATCH the stored authority — either check alone is incomplete:
  - `Signer` without `has_one`: any signer passes, not the right one.
  - `has_one` without `Signer`: the right account, but nobody proved they control it.
- The full validation trio on every state-mutating instruction: signer check + owner check + PDA/
  address check.
- Canonical teaching catalog: `coral-xyz/sealevel-attacks`, example `0-signer-authorization`.
- Real incident in the missing-validation family: Cashio (March 2022) — ~$52M minted against fake
  collateral accounts that passed an incomplete validation chain.
- Audit heuristic: for every state-mutating instruction, name in one sentence WHO may call it —
  then find the line that enforces exactly that. Mismatch = the finding.
