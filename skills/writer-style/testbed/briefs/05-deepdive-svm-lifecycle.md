---
id: 05-deepdive-svm-lifecycle
title: "What actually happens to your transaction: the Solana lifecycle, end to end"
words_target: 2800
audience: developers who use Solana daily but have never traced a tx below the RPC
dominant_job: derivation
route_expected: vitalik
context: standalone
expect:
  latam-framing: 0
  game-changer_max: 1
  civilizational-analogy_max: 1
  sign-off_max: 1
  hard_fails: 0
---

## Brief

A long-form deep-dive: follow one transaction from `sendTransaction` to finality. Derive WHY each
stage exists (why blockhash expiry, why no mempool, why account locks) rather than just naming the
stages. This is the repetition stress test — 2,800 words, multiple sections, the marker budget must
hold across the whole piece.

## Fact-sheet (FROZEN — verified 2026-07-02 against solana-dev MCP / Anza docs; do not re-derive)

- Transaction anatomy: signatures + message (header, account keys list, recent blockhash,
  instructions). Every account an instruction touches is declared up front, marked writable or
  read-only — this declaration is what makes parallel execution possible.
- The recent blockhash is a recent Proof-of-History hash and acts as a timestamp. A transaction is
  accepted while its blockhash is within the last 150 blocks (`MAX_PROCESSING_AGE = 150`);
  `lastValidBlockHeight` = current block height + 150 (blocks, not slots). In wall-clock terms
  roughly 60–120 seconds. Durable nonces exist for offline/delayed signing.
- Submission: the RPC node does not hold a public global mempool. It forwards the transaction
  directly to the current and next scheduled leaders (Gulf Stream) — the leader schedule is known
  an epoch in advance.
- Leader pipeline (TPU): Fetch → SigVerify → Banking stage → PoH → broadcast.
- Banking stage: the scheduler assigns non-conflicting transactions to executor threads using
  account locks — writable account = exclusive lock, read-only = shared. Transactions touching
  disjoint accounts execute in parallel (Sealevel); transactions contending on the same writable
  account serialize. This is why "hot account" congestion is local, not global (local fee markets).
- Execution: programs are SBF (eBPF-derived) bytecode run by the Solana Virtual Machine, metered in
  compute units. Per-transaction ceiling: 1.4M CU. Block-level ceilings also exist and have been
  raised repeatedly via SIMDs (48M → 50M → 60M CU through 2025).
- The leader stamps entries into the PoH stream and broadcasts the block as erasure-coded shreds
  through Turbine — a stake-weighted fan-out tree, so no single node uploads the block to everyone.
- Other validators replay the block (Replay stage) and vote; votes are themselves transactions.
- Commitment levels: `processed` (the leader's bank saw it) → `confirmed` (optimistic
  confirmation: ≥2/3 of stake voted on the block) → `finalized` (rooted: 31+ confirmed blocks built
  on top). Rollback of an optimistically confirmed block requires ≥1/3 of stake to be slashable.
- The dominant failure modes developers actually hit: (1) blockhash expired before inclusion,
  (2) fee too low for a contended writable account, (3) account-lock contention serializing what
  they assumed was parallel.
