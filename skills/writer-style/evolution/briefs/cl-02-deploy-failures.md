---
id: cl-02-deploy-failures
title: "Course lesson: your deploy failed — the three usual suspects"
container: course-lesson
words_target: 1300
audience: course students who just attempted their first devnet deploy
dominant_job: how-to
route_expected: helius
context: course-mid (series "Solana Development Fundamentals", lesson 3.5 of 6, a troubleshooting interlude after the deploy lesson; previous lesson: "From anchor init to devnet" — assume it's done; next lesson: "Client development (TypeScript + wallet adapter)"; closer contract: point to the actual next lesson or plain-close — NO teasers/comments-invites)
expect:
  latam-framing: 0
  game-changer_max: 1
  sign-off_max: 1
  hard_fails: 0
---

## Brief

A course lesson (~1,300 words) that exists because half the class just hit a failed deploy: the
three first-deploy failures (`declare_id!` mismatch, insufficient devnet balance, wrong cluster),
how to recognize each from its error, the exact fix, and how to verify you're actually live.
Troubleshooting register: the student is mildly frustrated; be the calm senior next to them.
Exact commands for the interesting steps, terse on routine ones. Load `formats/course-lesson.md`.

## Fact-sheet (FROZEN — imported subset of testbed/briefs/07-tutorial-anchor-deploy.md; do not
re-derive)

- The program ID in `declare_id!()` must match the deploy keypair
  (`target/deploy/my_program-keypair.json`). After cloning or regenerating keys,
  `anchor keys sync` fixes the mismatch — the #1 first-deploy failure.
- Funding: devnet SOL is free but rate-limited — `solana airdrop 2` style requests (typically ≤2
  SOL per request) or faucet.solana.com when the CLI faucet is limited.
- Deploy cost: the program account must be rent-exempt for roughly 2× the binary size (a typical
  starter program costs a few SOL of devnet balance).
- Cluster config: `Anchor.toml` `[provider] cluster = "devnet"`; wallet points at a local keypair.
- `anchor deploy --provider.cluster devnet` deploys via the upgradeable loader; the deploying
  wallet becomes the upgrade authority; later changes ship with `anchor upgrade`.
- Verify: `solana program show <PROGRAM_ID> --url devnet`, then call the program from the
  generated TS test/client via the IDL.
- Anchor 1.0 bundles the Solana toolchain — no separate `solana` CLI install needed for the
  standard flow.
