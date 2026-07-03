---
id: 04-security-signer-checks
title: "The missing signer check: Solana's most boring $50M bug"
words_target: 1200
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

A security explainer on the missing-signer-check vulnerability class: what it is, why it keeps
happening, how to write the check correctly in native Rust and in Anchor, and how to audit for it.
Serious register — a real exploit class with real losses; no jokes at the exploit, no hype
vocabulary ("game-changer" would be tone-deaf here), no geography.

## Fact-sheet (FROZEN — verified 2026-07-02; incident figures per public post-mortems)

- The vulnerability: an instruction handler treats an account as the "authority" without verifying
  that account actually SIGNED the transaction. Any caller can then pass any pubkey as the
  authority and act on its behalf.
- Native Rust: the check is explicit — `if !authority.is_signer { return Err(...) }`. Forgetting
  this one line IS the bug.
- Anchor: `Signer<'info>` enforces the signature at deserialization. Pair it with
  `has_one = authority` on the state account so the signer must also MATCH the stored authority —
  either check alone is incomplete:
  - `Signer` without `has_one`: any signer passes, not the right one.
  - `has_one` without `Signer`: the right account, but nobody proved they control it.
- The full account-validation trio on every state-mutating instruction: signer check + owner check
  (account owned by the expected program) + address/PDA check.
- Canonical teaching catalog: `coral-xyz/sealevel-attacks`, example `0-signer-authorization`.
- Real incident in the missing-validation family: Cashio (March 2022) — ~$52M minted against fake
  collateral accounts that passed an incomplete validation chain (the root cause was a missing link
  in account validation, not a cryptographic break).
- Audit heuristic: for every instruction that mutates state, name in one sentence WHO may call it —
  then find the line of code that enforces exactly that. If the sentence and the constraint don't
  match, that's the finding.
