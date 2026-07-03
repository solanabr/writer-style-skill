# Landing transactions during congestion (without overpaying for it)

You shipped the dApp, it held up fine for weeks, and then some mint goes viral, blockspace gets scarce, and suddenly your support channel fills with users watching spinners while their transactions quietly evaporate. Nothing errors. It just never lands. So you resend, it drops again, and you start refreshing the explorer like that's going to help (took me an embarrassing number of retries to accept that resending harder is not a strategy).

What's actually happening: the leader (the validator currently producing blocks) has more transactions than it can schedule, and yours gives it no reason to jump the queue. The unlock is the priority fee: an optional tip that raises your transaction's scheduling priority with the current leader — raises, not guarantees, but it's the lever you actually have. Two instructions, one simulation, one formula. Let's wire it in properly, because the naive version of this fix overpays on every single transaction you send.

## What you're actually paying for

Every transaction pays a base fee: 5,000 lamports per signature. 50% is burned, 50% goes to the block producer. You can't negotiate that. The priority fee sits on top, optional, and under SIMD-0096 it goes 100% to the validator. That's the economic reason tipping works at all: the leader keeps the whole tip, so the leader has a direct incentive to schedule you first.

What you're tipping on is compute. Two Compute Budget Program instructions control it:

- **SetComputeUnitLimit (u32)**: how many compute units (CU) your transaction is allowed to use
- **SetComputeUnitPrice (u64)**: what you pay for each of those units, in micro-lamports (1 lamport = 1,000,000 micro-lamports)

Both are plain instructions, they ride inside the very transaction they're budgeting for, no separate setup step. Only one of each per transaction; include a duplicate and the whole thing fails with a `DuplicateInstruction` error. The fee itself:

```
priority fee (lamports) = ceil(compute_unit_price × compute_unit_limit / 1,000,000)
```

Read that twice, because the catch here is: you're charged on the REQUESTED limit, not on what you actually consume. Over-allocate and you are paying, on every send, for units you never touch. And if you skip `SetComputeUnitLimit` entirely, the runtime assumes 200,000 CU per non-builtin instruction (3,000 per builtin), against a hard maximum of 1,400,000 CU per transaction. For a transaction that uses a sliver of that, the default is padding, and now you're paying rent on padding. Put the two mistakes together and the leak writes itself: a limit nobody measured, multiplied by a price nobody checked. Both numbers are yours to set.

## Simulate first, then size

So what's the right limit? You don't guess, you measure. Confession: my first congestion fix was cranking the price up and praying. It landed. It also meant every transaction was tipping on compute it never used, the kind of quiet leak you only notice once you multiply it across all your production traffic.

The workflow that holds up:

1. Simulate the transaction.
2. Read `unitsConsumed` from the result.
3. Set the CU limit to that value plus a 10–20% margin.
4. Set the CU price from recent fee data (next section).

The margin exists because a simulation is a snapshot, not a guarantee; give execution some headroom, just not the default's worth of it. And notice what the limit is doing in the formula: it multiplies the price. Sizing it down doesn't just cap what your transaction can burn, it shrinks every tip you will ever pay at a given price level.

Numbers, so this stays concrete: a 300,000 CU limit at 10,000 micro-lamports per CU works out to 3,000 lamports of priority fee. That's 0.000003 SOL, on top of the 5,000-lamport base — in this example the tip is smaller than the base fee it rides on! Landing here is cheap. Guessing is what gets expensive.

## Where does the price number come from?

Ask the chain, because the chain keeps receipts: the `getRecentPrioritizationFees` RPC returns per-slot minimum fees over the last 150 blocks, which is exactly "what has inclusion been costing lately." The price half is the half people get wrong, and it's usually one of two details:

- **Query the writable accounts your transaction locks, not program IDs.** Programs are read-only. Ask about a program and you get near-empty data back, which will cheerfully report that the network is free while the pool you're actually writing to is on fire.
- **Take a high percentile of the non-zero values.** These are per-slot minimums; average them and a few quiet slots drag your number below what actually lands.

Writable accounts, non-zero values, high percentile. That's the whole recipe. If you'd rather not maintain that aggregation yourself, Helius exposes `getPriorityFeeEstimate`: hand it your serialized transaction and it returns estimates at percentile levels, so your checkout flow can pay a higher percentile than a background sync does. (Credit where due, this replaced a percentile script I was babysitting.)

## Fees are local (that's where the overpay hides)

The instinct, once you know tips exist, is to treat congestion as one global weather system and pay storm rates everywhere. It isn't one. Contention on Solana is per-writable-account: your transaction competes for the specific accounts it writes to, not for the network as a whole. A popular pool, a mint in demand, those are hot accounts and need a real fee; a transaction touching neither stays cheap (well, "cheap" meaning whatever the quiet lane's recent fees show, which is exactly why you query your own accounts) while the frenzy happens next door.

Supermarket picture: one register mobbed because of a coupon deal, the others idle. Paying to skip the line only means something at the mobbed register. On-chain, same thing: a high fee does not help on an uncongested account. It buys you nothing. Save the aggressive percentile for the sends that are genuinely contested and let everything else ride cheap.

Which is the entire overpaying story in one line: teams benchmark against the hottest account on the network and apply that price to everything they send. Price the writable accounts you actually lock, and most of your transactions turn out to be standing in the empty lane.

## 200,000 is a default, not a plan

That default is my bet for what your dApp is requesting right now, sitting on transactions that use a fraction of it. Go check, I'll wait. Then simulate, size, send.

With this in your send path, congestion stops being a reliability incident and becomes a pricing decision, and usually a small one. It's an afternoon of work, honestly, and your users stop meeting spinners the next time an account they care about gets hot. If the fee spend still looks off after you wire it up, check which accounts you're locking before you touch anything else, that's where the answer usually lives.

Want a part two on fee strategy for hot mints specifically? Say the word. cya 👋
