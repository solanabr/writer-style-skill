# How to Land Transactions During Congestion (Priority Fees)

People love talking about Solana congestion like it's weather. The network is "busy," your transactions are dropping, nothing to be done except add a retry loop and wait for the front to pass. I've read that diagnosis in a dozen Discord threads, and honestly I've shipped it myself, and most of the time the real story is far more fixable: blockspace under load is an auction, and a transaction with default settings shows up bidding zero.

The silver bullet? Two instructions from the Compute Budget Program, plus one simulation call most dApps skip. Let's follow the money first, then wire up the code.

## What a transaction actually pays

Every transaction pays a base fee of 5,000 lamports per signature: 50% burned, 50% to the block producer. The base fee buys validity, not placement: every other transaction in the queue paid it too, so it does nothing to move you up the line when blocks are contested.

The priority fee is the optional layer on top, and its economics are different in a way that matters: 100% of it goes to the validator (SIMD-0096), which is exactly why it works — you're paying the specific machine currently deciding what makes it into the next block, and it raises your transaction's scheduling priority with that leader.

The amount comes from one formula worth memorizing:

```
priority fee (lamports) = ceil(compute_unit_price × compute_unit_limit / 1,000,000)
```

The price is quoted in micro-lamports per compute unit, and 1 lamport = 1,000,000 micro-lamports, so the raw numbers look much scarier than the money. A 300,000 CU limit at 10,000 micro-lamports per CU works out to 3,000 lamports of priority fee (0.000003 SOL) on top of the 5,000-lamport base.

## The two instructions

Both knobs live in the Compute Budget Program. `SetComputeUnitLimit` takes a u32 and caps how much compute your transaction may consume; `SetComputeUnitPrice` takes a u64 in micro-lamports and sets your bid per unit. You get one of each per transaction — a duplicate fails the whole thing with a `DuplicateInstruction` error, which I only know because half the transaction-builder helpers out there try to quietly add their own.

Leave them out and you get the defaults: 200,000 CU per non-builtin instruction, 3,000 per builtin, with a hard maximum of 1,400,000 CU per transaction. And this is where the money leaks, because the fee is charged on the CU limit you REQUEST, not on what you actually consume. I learned that the annoying way: an early sender of mine requested the 1,400,000 maximum on every transaction because a forum post said headroom was free, and if your instruction really consumes 300,000 CU, that configuration pays priority fee on more than four times the compute you used, on every send, forever, quietly, because each individual overpayment still rounds to nothing on a receipt. Headroom is not free — it multiplies every bid you will ever make.

## Simulate before you bid

So you don't guess the limit — you measure it. The workflow is four steps, and none of them are clever: simulate the transaction, read `unitsConsumed` from the result, set the CU limit to that value plus a 10–20% margin, then set the CU price from recent fee data.

```ts
// 1) simulate to measure the real compute cost
const sim = await connection.simulateTransaction(tx);
if (sim.value.err) throw new Error(`sim failed: ${JSON.stringify(sim.value.err)}`);
const used = sim.value.unitsConsumed;

// 2) request that + margin; bid from recent fee data (next section)
tx.add(
  ComputeBudgetProgram.setComputeUnitLimit({ units: Math.ceil(used * 1.2) }),
  ComputeBudgetProgram.setComputeUnitPrice({ microLamports: price }),
);
```

Honestly, the simulation step is the godsend here. Everyone fixates on the price knob because the price feels like the bid, but the limit is what that price gets multiplied by, and a simulation is the only way to set it from a measurement instead of a guess. The margin earns its keep too: consumption can drift between simulation and execution when the accounts you touch change state underneath you, so the extra 10–20% is there to absorb drift you can't see coming.

## Where the fee numbers come from

Next up, the price. The RPC method is `getRecentPrioritizationFees`, which returns per-slot minimum fees over the last 150 blocks; when people say "set the price from recent fee data," this is the data they mean. Two mistakes show up in almost every integration I've reviewed. One: passing program IDs. Pass the WRITABLE accounts your transaction locks instead: programs are read-only, and querying them returns near-empty data that will cheerfully convince you fees are zero everywhere. Two: averaging the response. It's full of zeros from quiet slots, so take a high percentile of the non-zero values if the goal is landing during a spike rather than describing an average Tuesday. Both mistakes produce the same symptom, a fee that looks perfectly reasonable in your dashboard and does nothing at the exact moment your users care.

If you'd rather not run your own percentile plumbing, Helius exposes `getPriorityFeeEstimate`: hand it a serialized transaction and it returns estimates at percentile levels, which is what I reach for on anything user-facing (my hand-rolled version survives in a scratch file of launch-night fee curves that started as debugging notes and has slowly become more of a hobby than an input to any actual decision).

## Local fee markets

Now, one correction to the mental model before you go tune numbers: fees on Solana are local. Contention is priced per writable account, so a transaction writing to a hot account (the pool everyone is swapping through, a mint everyone wants) competes in one small expensive auction while the rest of the network stays cheap. During a hyped launch this is exactly what you watch happen in real time: the handful of accounts everyone is writing to get pricey for a stretch, and an unrelated transfer two tabs over keeps landing at the base fee like nothing is going on. The corollary cuts both ways: your estimate should follow the specific accounts your transaction locks, and a huge fee attached to an uncongested account buys you nothing you weren't already getting; it's a tip, not a fast lane.

One caveat, though: a priority fee raises your odds with the current leader without ever guaranteeing inclusion, so in a genuine saturation event some well-priced transactions will still drop, and your retry logic keeps its job. What changes is your baseline. Run it with your own numbers, your simulated CU, your accounts' recent percentile, through the formula above: for most flows the fee that lands reliably costs fractions of a cent, while the default configuration was somehow managing to overpay for compute and still lose the one auction that mattered.

If you wire it up and things still vanish during rush hour, reach out; I've debugged enough of these to genuinely enjoy them at this point. Happy shipping! 🚀
