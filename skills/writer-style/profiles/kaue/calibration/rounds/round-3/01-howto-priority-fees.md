# Landing Transactions When the Network Gets Busy (Priority Fees, Done Right)

People love treating priority fees like a tip jar. The network gets busy, transactions start dropping, so you throw more lamports at the problem and hope a validator likes you better this time. I understand the instinct, because that's roughly how gas works in most people's mental model of a blockchain, but on Solana it's wrong in a way that costs you twice: you overpay on every transaction that lands, and the ones that matter still drop, because the fee you attach isn't a tip to one global queue. It's a bid in a very local auction, and most dApps I've reviewed are bidding blind.

So let's do this properly: what a transaction actually pays, the two instructions that control it, and the simulate-first loop that ends the guessing, in that order, because the fix makes more sense once you've seen what the fee is charged on.

## What you're actually paying for

Let's start with the part you can't opt out of. Every transaction pays a base fee of 5,000 lamports per signature, congestion or not; half of that gets burned, half goes to the block producer, and none of it buys you any scheduling priority at all.

The priority fee (the docs call it a prioritization fee) is the optional part on top, and it behaves differently: 100% of it goes to the validator, per SIMD-0096, which is exactly why it works. You're paying the one entity that decides whether your transaction makes this block, and what you're buying is scheduling priority with the current leader.

You control it through two instructions from the Compute Budget Program:

```
SetComputeUnitLimit(units: u32)    // how much compute you reserve
SetComputeUnitPrice(price: u64)    // micro-lamports per compute unit
```

One of each per transaction, maximum. A duplicate doesn't get silently ignored; it fails with a `DuplicateInstruction` error, which is worth checking before you bolt these on, because if anything else in your stack is already appending compute budget instructions, your own copy is the duplicate.

The math connecting them:

```
priority fee (lamports) = ceil(compute_unit_price × compute_unit_limit / 1,000,000)
```

Price is in micro-lamports per CU, and 1 lamport = 1,000,000 micro-lamports, so the raw numbers look scarier than they are.

Now the detail that quietly drains wallets: the fee is charged on the CU limit you REQUEST, not on what your transaction actually consumes. Skip `SetComputeUnitLimit` entirely and the runtime assumes 200,000 CU for every non-builtin instruction (3,000 for builtins), up to the hard maximum of 1,400,000 CU per transaction, and your priority fee gets priced on all of it whether you use it or not.

## The part I did wrong for months

When I first hit dropped transactions in production, my playbook was exactly the tip-jar move from the first paragraph: crank `compute_unit_price`, re-send, repeat until it lands. No limit instruction, no simulation, just a multiplier and some faith. I even had a retry wrapper that doubled the price on every attempt, very sophisticated stuff. It mostly worked too, which is the worst kind of feedback, because it hid what the habit was costing me, and I wasn't about to go digging into transactions that landed fine.

The number that finally made me look: a swap in one of my bots simulated at 118,000 compute units. It carried three non-builtin instructions, so with no limit set the runtime budgeted 600,000 CU, and every priority fee I attached got priced on all 600,000. Roughly five times the compute I consumed. Five times the fee I needed. On every single send, for months, and I only noticed while debugging something unrelated. Not ruinous at Solana prices, sure, but it compounds, and during a hot launch it's the difference between fees you shrug at and fees your users screenshot.

The correct loop is four steps, none of them hard:

1. **Simulate the transaction first.**
2. **Read `unitsConsumed` from the result.** That's your real compute cost, measured instead of guessed.
3. **Set the CU limit to that value plus 10–20% margin.** Enough headroom that state changes between simulation and execution don't kill you, not so much that you're paying for air.
4. **Set the CU price from recent fee data.** The next section covers where that number actually comes from.

Worked through with round numbers: a 300,000 CU limit at 10,000 micro-lamports per CU comes out to 3,000 lamports of priority fee, 0.000003 SOL, on top of the 5,000-lamport base. That's the entire cost of jumping the line, and notice it lands below the base fee you were paying anyway.

## Where the price number comes from

Step 4 up there said "recent fee data," and that phrase was doing a lot of quiet work, so let's unpack it. Two sources worth knowing.

The vanilla one is the `getRecentPrioritizationFees` RPC method, which returns per-slot minimum fees over the last 150 blocks. It ships with two gotchas that bite almost everyone once. First: pass it the WRITABLE accounts your transaction locks, not the program IDs — programs are read-only, so querying them returns near-empty data, and I've watched devs conclude "fees are basically zero right now" from exactly that mistake. Second: these are per-slot minimums, so don't average them; take a high percentile of the non-zero values if you want to land while an account is contested. Where you sit in that distribution is your urgency dial, because a user clicking swap on a hot pool mid-launch deserves a higher percentile than a cron job sweeping dust at 4am, and pricing each transaction on its own contention is the whole point of the exercise.

If you'd rather not roll your own percentile logic, Helius exposes `getPriorityFeeEstimate`, which takes your serialized transaction and hands back estimates at different percentile levels, so the urgency dial becomes one parameter instead of a data pipeline you maintain.

Why writable accounts specifically? Because this is the design choice that makes the whole tip-jar model wrong: fee contention on Solana is per-writable-account, not network-wide. Writing to a hot account, a popular pool, a mint everyone wants a piece of, needs a higher fee while the rest of the network stays cheap. This is also why copying some "current Solana priority fee" number off a dashboard misleads you — there is no single number, there's one per contested account, and yours is probably not the one trending. Local fee markets are the real game-changer here, and they cut both ways: your quiet transfer never pays for someone else's memecoin frenzy, but no fee, however large, buys you anything on an account nobody is contesting. If your transactions are dropping on a quiet account, the problem lives somewhere else, and more lamports won't fix it, however satisfying it feels to crank the knob.

## Wrapping up

Simulate, read `unitsConsumed`, set the limit with a small margin, price it from the writable accounts you're actually touching. Your transactions land during the chaos and your fee bill stops subsidizing compute you never used.

Happy landing! 🚀
