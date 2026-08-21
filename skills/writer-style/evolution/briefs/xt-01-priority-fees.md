---
id: xt-01-priority-fees
title: "X thread: stop overpaying priority fees"
container: x-thread
words_target: 450
audience: Solana dApp developers who've had transactions dropped
dominant_job: how-to
route_expected: helius
context: standalone
expect:
  latam-framing: 0
  sign-off_max: 1
  game-changer_max: 1
  civilizational-analogy_max: 1
  hard_fails: 0
---

## Brief

An X thread (6–9 posts): why transactions drop during congestion, how priority fees actually
price, and the simulate-first workflow that stops overpaying. Each post must stand alone when
screenshotted; the first post must earn the tap on its own. Number formatting, line breaks, and
per-post length per `formats/x-thread.md`. Write posts separated by `---` on its own line.

## Fact-sheet (FROZEN — imported from testbed/briefs/01-howto-priority-fees.md; do not re-derive)

- Base fee: 5,000 lamports per signature; 50% burned, 50% to the block producer.
- The priority fee is optional, goes 100% to the validator (SIMD-0096), and raises scheduling
  priority with the current leader.
- Formula: `priority fee (lamports) = ceil(compute_unit_price × compute_unit_limit / 1,000,000)`;
  price is micro-lamports per CU.
- The fee is charged on the REQUESTED CU limit, not actual usage — over-allocating compute is
  paying for units never consumed.
- Defaults without `SetComputeUnitLimit`: 200,000 CU per non-builtin instruction; hard max
  1,400,000 CU per transaction.
- One `SetComputeUnitLimit` + one `SetComputeUnitPrice` per transaction; duplicates error.
- Correct workflow: simulate → read `unitsConsumed` → set limit to that +10–20% → set price from
  recent fee data.
- Fee data: `getRecentPrioritizationFees` (pass the WRITABLE accounts your tx locks, not program
  IDs; take a high percentile of non-zero values). Helius: `getPriorityFeeEstimate`.
- Local fee markets: contention is per-writable-account — a hot account needs a higher fee while
  the rest of the network stays cheap.
- Worked example: 300,000 CU × 10,000 micro-lamports/CU = 3,000 lamports (0.000003 SOL) on top of
  the 5,000-lamport base.
