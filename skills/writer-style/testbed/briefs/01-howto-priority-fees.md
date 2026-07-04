---
id: 01-howto-priority-fees
title: "How to land transactions during congestion (priority fees)"
words_target: 1200
audience: intermediate Solana developer shipping a dApp
dominant_job: how-to
route_expected: helius
context: standalone
expect:
  latam-framing: 0
  game-changer_max: 1
  sign-off_max: 1
  civilizational-analogy_max: 1
  hard_fails: 0
---

## Brief

A practical guide: my transactions keep getting dropped when the network is busy — what are
priority fees, how do I set them correctly, and how do I stop overpaying? Reader has shipped a dApp
and hit this in production. Show the actual instructions and the simulate-first workflow.

## Fact-sheet (FROZEN — verified 2026-07-02 against solana-dev MCP; do not re-derive)

- Every transaction pays a base fee: 5,000 lamports per signature. 50% is burned, 50% goes to the
  block producer.
- The priority (prioritization) fee is optional and goes 100% to the validator (SIMD-0096). It
  raises the transaction's scheduling priority with the current leader.
- Formula: `priority fee (lamports) = ceil(compute_unit_price × compute_unit_limit / 1,000,000)`.
  Price is in micro-lamports per CU; 1 lamport = 1,000,000 micro-lamports.
- The fee is charged on the REQUESTED CU limit, not actual usage. Over-allocating compute = paying
  for units you never consume.
- Defaults when no `SetComputeUnitLimit` is included: 200,000 CU per non-builtin instruction,
  3,000 per builtin. Hard maximum: 1,400,000 CU per transaction.
- Compute Budget Program instructions: `SetComputeUnitLimit` (u32) and `SetComputeUnitPrice`
  (u64, micro-lamports). Only ONE of each per transaction — a duplicate causes a
  `DuplicateInstruction` error.
- Correct workflow: (1) simulate the transaction, (2) read `unitsConsumed`, (3) set the CU limit to
  that value + 10–20% margin, (4) set the CU price from recent fee data.
- Fee data sources: `getRecentPrioritizationFees` RPC (per-slot minimum fees over the last 150
  blocks; pass the WRITABLE accounts your tx locks, not program IDs — programs are read-only and
  return near-empty data; take a high percentile of non-zero values). Helius exposes
  `getPriorityFeeEstimate` with percentile levels for a serialized transaction.
- Local fee markets: contention is per-writable-account. Writing to a hot account (a popular pool,
  a mint in demand) needs a higher fee while the rest of the network stays cheap. A high fee does
  not help on an uncongested account.
- Worked example: 300,000 CU limit × 10,000 micro-lamports/CU = 3,000 lamports priority fee
  (0.000003 SOL) on top of the 5,000-lamport base.
