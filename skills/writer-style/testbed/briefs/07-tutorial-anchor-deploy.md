---
id: 07-tutorial-anchor-deploy
title: "From anchor init to devnet: your first program, deployed"
words_target: 1800
audience: developer new to Anchor, comfortable with a terminal
dominant_job: how-to
route_expected: helius
context: course-mid (series "Solana Development Fundamentals", lesson 3 of 6; previous lesson: "Rust for Solana" — assume it's done, a continuation open is available; next lesson: "Client development (TypeScript + wallet adapter)"; closer contract: point to the actual next lesson or plain-close — NO teasers/comments-invites)
expect:
  latam-framing: 0
  civilizational-analogy_max: 1
  game-changer_max: 1
  sign-off_max: 1
  hard_fails: 0
---

## Brief

A hands-on tutorial: initialize an Anchor project, understand the generated structure, build, test,
and deploy to devnet, then verify it's live. Exact commands for the interesting steps, terse on the
routine ones. Reader follows along in a terminal.

## Fact-sheet (FROZEN — verified 2026-07-02; Anchor 1.0 behavior per this repo's rules)

- Prereqs: Rust toolchain + Anchor installed. Anchor 1.0 bundles the Solana toolchain (no separate
  `solana` CLI install needed).
- `anchor init my_program` generates: `programs/my_program/src/lib.rs` (the program),
  `tests/`, `migrations/`, `Anchor.toml` (cluster + wallet config), and on first build
  `target/deploy/my_program-keypair.json` (the program's identity).
- The program ID in `declare_id!()` must match the deploy keypair. After cloning or regenerating
  keys, `anchor keys sync` fixes the mismatch — the #1 first-deploy failure.
- `anchor build` → compiled `.so` in `target/deploy/` + IDL in `target/idl/`.
- `anchor test` (Anchor 1.0): runs against Surfpool, not `solana-test-validator`; the default test
  template is LiteSVM (Rust, in-process).
- Devnet config: `Anchor.toml` `[provider] cluster = "devnet"`, wallet points at a local keypair.
- Funding: devnet SOL is free but rate-limited — `solana airdrop 2` style requests (typically ≤2
  SOL per request) or faucet.solana.com when the CLI faucet is limited.
- Deploy cost: the program account must be rent-exempt for roughly 2× the binary size (a typical
  starter program costs a few SOL of devnet balance to deploy).
- `anchor deploy --provider.cluster devnet` deploys via the upgradeable loader; the deploying
  wallet becomes the upgrade authority; later changes ship with `anchor upgrade`.
- Verify: `solana program show <PROGRAM_ID> --url devnet`, then call the program from the generated
  TS test/client via the IDL.
- Common failures to pre-empt: insufficient devnet balance, `declare_id!` mismatch, wrong cluster
  in `Anchor.toml`.
