# Landing transactions when Solana gets busy (without overpaying for it)

Your dApp works. It worked on devnet, it worked on mainnet for weeks, and then some hyped mint goes live (you know the day), the network gets busy, and suddenly your users are staring at spinners while their transactions quietly expire. No error to catch, nothing to log. Just gone. If you've shipped anything real on Solana, you've felt this one, probably at the worst possible hour.

The fix has a name: priority fees. The problem is that most of the fixes I see in the wild are either a hardcoded magic number somebody copied from a gist, or a panic-sized fee chosen precisely because nobody knew what the right one was. So this guide covers both halves: how to land transactions when the network is busy, and how to stop overpaying the second it isn't.

The route: what you're actually paying → the two Compute Budget instructions → the simulate-first workflow → where the price number comes from → why Solana fees are local, not global. By the end you'll have a small fee pipeline instead of a magic number.

## What you're actually paying

Two separate things hide inside "fees" on Solana, and mixing them up is where most of the confusion starts.

The base fee is fixed: 5,000 lamports per signature, whether the network is empty or on fire. 50% of it is burned, 50% goes to the block producer. You pay it either way, and it buys you nothing extra during congestion.

The priority fee is the optional one, and since SIMD-0096 it goes 100% to the validator. What it buys is exactly one thing: it raises your transaction's scheduling priority with the current leader. A better spot in line. That's the whole product.

The math: `priority fee (lamports) = ceil(compute_unit_price × compute_unit_limit / 1,000,000)`.

The price is in micro-lamports per compute unit (CU), and 1 lamport = 1,000,000 micro-lamports. Deliberately tiny units, so sub-cent pricing stays possible.

So why not set a giant limit and a fat price and call it solved? Because the fee is charged on the REQUESTED CU limit, not on what your transaction actually consumes. Over-allocate and you pay, on every send, for compute you never touch (ask me how I know). Skipping the limit doesn't save you either: with no `SetComputeUnitLimit` in the transaction, the runtime assumes 200,000 CU per non-builtin instruction (3,000 per builtin), and the hard maximum is 1,400,000 CU per transaction. If your instruction needs a fraction of 200,000, the default quietly prices you for all of it.

## The two dials

Both values are set with Compute Budget Program instructions, added to your transaction like any other:

- **SetComputeUnitLimit** — takes a u32, caps the compute your transaction may use.
- **SetComputeUnitPrice** — takes a u64, the price in micro-lamports per CU.

Only one of each per transaction. Include a duplicate and the whole thing fails with a `DuplicateInstruction` error, which is, honestly, a fun one to meet in production when two layers of your stack each add a compute budget on your behalf. Check what your wallet adapter or SDK already injects before adding your own.

## Simulate first

I'll confess how I handled this the first time: grabbed a compute-budget snippet from someone's repo, hardcoded both numbers, shipped it, moved on. Guilty, big time. It "worked", in the sense that transactions landed, and it overpaid on every single one of them for months.

The correct workflow is boring and takes four steps:

1. Simulate the transaction.
2. Read `unitsConsumed` from the result.
3. Set the CU limit to that value plus a 10–20% margin.
4. Set the CU price from recent fee data (next section).

That's it. The simulation tells you what the transaction actually costs in compute, so you stop renting the 200,000-CU default when the real number is a fraction of that, and the 10–20% margin absorbs the small variance between simulation and live execution so an exact-cut limit doesn't fail you at the worst moment. Simulate-first isn't a nice-to-have, it's the difference between pricing a transaction and guessing at it.

## Where the price comes from

The limit came from simulation. The price comes from the market, and this is where two well-hidden traps live.

The RPC method `getRecentPrioritizationFees` returns per-slot minimum fees over the last 150 blocks. Trap one: pass it the writable accounts your transaction will lock, not program IDs. Programs are read-only, and querying read-only addresses returns near-empty data, which looks exactly like "fees are basically zero right now". I have watched that one mistake produce a very confident, very wrong fee estimator.

Trap two: these are per-slot minimums, so take a high percentile of the non-zero values. An average across a pile of empty slots and one spike tells you nothing about landing inside the spike.

If you'd rather not hand-roll percentile logic, Helius exposes `getPriorityFeeEstimate`: hand it a serialized transaction, pick a percentile level, get a number back. Don't reinvent this wheel; wire the estimate in and spend the saved hours on your actual product.

## Local fee markets, or why your fee didn't help

Here's the mental model that makes everything above click: fee contention on Solana is per-writable-account. Your transaction is bidding against the other transactions trying to lock the same accounts, not against the whole network.

Writing to a hot account (a popular pool, a mint in demand) is expensive right now. Writing to your own quiet PDA in the same slot stays cheap. And the inverse is the part people skip: a high fee does not help on an uncongested account. There is no line to jump. Paying a mint-rush fee on a Tuesday-afternoon transfer is pure donation.

Think toll bridge, not citywide curfew. One bridge into the stadium fills up on game night and gets priced accordingly, while every other road stays free-flowing and free. The analogy is bounded (the scheduler is more complicated than a toll booth), but it carries the right instinct: you're pricing the specific account you write to, at the specific moment you write to it.

Which is why the hardcoded fee is wrong in both directions at once: too low for the pool during a frenzy, too high for everything else, forever.

## What it costs, concretely

One realistic transaction, priced end to end: a 300,000 CU limit at 10,000 micro-lamports per CU comes to 3,000 lamports of priority fee (0.000003 SOL) on top of the 5,000-lamport base. Landing reliably during congestion costs less than the base fee itself. The entire game is paying it only when the account you're touching is actually hot.

Your fee logic is now four steps and one data source instead of a magic number, and it moves with the market instead of guessing at it. Want to see the payoff in your own numbers? Log requested vs consumed CU for a week; the gap is what you've been overpaying, and watching it shrink is weirdly satisfying. Happy building! 🚀
