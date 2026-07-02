# What actually happens to your transaction: the Solana lifecycle, end to end

You call `sendTransaction`, the spinner spins, and eventually your app throws some flavor of "transaction expired." So you do what everyone does: resend. It lands, the demo goes on, and you learn exactly nothing about what just happened.

I shipped like that for longer than I want to admit — retry-and-pray was my entire mental model of the chain below the RPC, and I've been guilty of teaching it too, wrapping sends in loops without once asking what the loop was actually racing against.

Let's fix that properly. We're going to take ONE transaction and follow it all the way down: from the bytes you sign, through the leader that executes them, out to the validators that vote, until the network is willing to call the thing final. And at every stop we ask the only question that makes internals stick: why does this stage exist at all? Anyone can recite the stage names. The reasons are where the debugging superpowers live.

Fair warning, this covers a lot of ground. I'll keep each stop tight.

## The transaction you signed is weirder than you think

Start with the artifact itself. A Solana transaction is two things: a list of signatures, and a message. The message is where everything lives: a small header, the list of account keys the transaction will touch, a recent blockhash, and the instructions themselves.

Two of those should bother you.

First, the account keys list. Every account an instruction touches must be declared up front, and each one is marked writable or read-only. Most chains ask nothing of the sort; you send a call and it touches whatever state it ends up touching. Solana makes you announce your entire footprint before anything runs, and it is strict about it.

Second, the "recent blockhash." Your transaction embeds a reference to a specific recent moment in chain history, and that reference expires in minutes, killing the transaction with it.

An up-front confession of everything you'll touch, plus a built-in death clock. Neither is an accident, and neither makes sense in isolation: the declaration pays off inside the leader's scheduler, and the death clock pays off the moment you ask how the network avoids processing you twice. Clock first.

## Why your transaction ships with an expiry date

The motivating problem: the network sees the same signed bytes twice, maybe because a flaky RPC re-forwarded them, maybe because you retried. How does it know not to execute you twice?

The naive answer is memory. Keep a record of every transaction signature ever processed, check every new arrival against it. That record grows forever, and every validator pays the lookup on every single incoming transaction, forever. Dead on cost alone.

The next answer is the one several chains actually use: give each account a counter and require every transaction to carry the next number. Dedupe becomes trivial. But now everything one wallet does is strictly ordered: transaction seven cannot land before transaction six, one stuck transaction dams everything queued behind it, and firing ten independent transfers in parallel from a single wallet turns into an exercise in frustration. For a chain whose entire personality is parallelism, that's a self-inflicted wound.

Solana's answer is to bound the problem in time. The recent blockhash your transaction carries is a recent Proof-of-History hash, and it acts as a timestamp — the chain has its own clock, so "recent" is something a validator can check without trusting anyone's wall time. A transaction is accepted only while its blockhash sits within the last 150 blocks; the constant in the codebase is literally `MAX_PROCESSING_AGE = 150`. When your RPC hands you a `lastValidBlockHeight`, that's simply current block height + 150. Blocks, mind you, not slots: a slot can pass without producing a block, so the two counts drift apart. In wall-clock terms you get roughly 60–120 seconds of life.

With the window bounded, deduplication gets cheap: a validator only needs to remember what landed within the last 150 blocks to reject a replay, because anything older is invalid by definition. Bounded memory, bounded check, problem closed.

The trade-off is real and you should know it: you cannot sign a transaction today and broadcast it next week. That exact pain is why durable nonces exist, a separate mechanism built for offline and delayed signing. Niche, but when you need it, nothing else works.

And the expiry quietly buys you something it took me an embarrassing debugging night to appreciate: safe retries. I once had a script so terrified of double-paying that I kept "protecting" it with sleeps between resends of the same signed bytes. Pointless. Within the window, dedupe rejects the copy; past `lastValidBlockHeight`, the old transaction is dead everywhere, and re-signing with a fresh blockhash is guaranteed safe. The death clock protects the network, sure. It also makes your retry loop sound.

## The mempool that isn't there

The transaction now leaves your machine for an RPC node. On most chains you know the next scene: it enters the mempool, a public waiting room of pending transactions gossiped to every node, held by everyone because nobody knows who will produce the next block, so everybody keeps everything just in case.

That whole structure exists to solve one problem: not knowing who's next. Solana doesn't have that problem. The leader schedule is known an epoch in advance. If you know exactly who is producing this block and who's up next, what is the waiting room for?

Nothing. So it's gone. Your RPC node forwards the transaction directly to the current and next scheduled leaders, a protocol called Gulf Stream, which is less a feature than a deletion: the mempool isn't missing, it's obsolete.

Doesn't the transaction still wait somewhere? Yup, just not in public. It queues at the leader itself.

Worth being honest about the trade here, because there is one. Deleted: the global gossip of pending transactions, plus the hops between you and inclusion. The cost: for a moment, your transaction's fate is concentrated in a couple of known machines, and if the current leader is saturated and drops you, no one else in the network is holding a copy on your behalf. You, or your RPC, resend. The expiry window from the last section is what keeps that sane: you always know the exact block height after which a dropped transaction is safely dead and a fresh signature is safe to send.

## Five stages inside the leader

The leader ingests transactions through a pipeline called the TPU: Fetch → SigVerify → Banking stage → PoH → broadcast.

Fetch pulls packets off the wire. SigVerify checks signatures and discards garbage. Banking executes transactions against state. PoH stamps what happened into a sequence. Broadcast ships the block out to the network.

Three of those are plumbing. Two of them, banking and PoH, carry the ideas the whole design leans on, and the banking stage is where your weird up-front account list finally earns its keep.

## Account locks: the payoff for all that up-front honesty

Time to cash in the question from the top: why did your transaction have to declare every account it touches?

Because the scheduler wants to run transactions in parallel, and parallelism is only safe between transactions that don't touch each other's state. The naive route, run everything at once and detect collisions as they happen, means throwing away completed work every time two transactions clash mid-flight; you paid to execute both, and one gets rolled back. If you want to know which transactions conflict BEFORE running anything, there is exactly one way: each transaction has to hand over its footprint in advance. The account keys list is not bureaucratic ceremony. It's the entry fee for pre-scheduled parallelism.

What the banking stage does with it: the scheduler converts each declared account into a lock. A writable account is an exclusive lock; a read-only account is a shared one, so any number of transactions can read the same account side by side. Transactions whose locks don't collide get assigned to different executor threads and run simultaneously — the parallel runtime is called Sealevel. Transactions contending on the same writable account serialize, one after another, no exceptions.

Think of it as a city's road grid. Two cars on different streets never negotiate; two cars arriving at the same intersection take turns. Pricing follows the same shape: the toll rises at the congested intersection, not across the whole city. (The analogy breaks in one honest place: drivers pick routes as they go, while your transaction files its full route before leaving the garage. That filing is exactly the entry fee from the previous paragraph.)

The toll behavior is Solana's local fee markets, and it falls straight out of the locks. A hyped mint hammering one writable account turns that account into a bidding war, while your unrelated transfer two streets over stays cheap, because congestion on this chain is local, not global. For consumer apps, where fees basically are the UX, local fee markets are a godsend.

One warning before we move on, since it plants a failure mode we'll harvest later: the scheduler takes your declaration literally. Mark an account writable when you only read it, or funnel every user through one shared account, and you have serialized yourself. Nobody attacked you. You told the scheduler to route all your users through the same intersection, and it obeyed.

## Metered execution: the 1.4M CU leash

Inside those executor threads, your program finally runs. Programs on Solana are SBF bytecode, an eBPF-derived format, executed by the Solana Virtual Machine, and every step of that execution is metered in compute units.

The meter isn't optional, and deriving why is quick: this block will be re-executed by every validator in the network. A transaction allowed to run arbitrarily long makes verifying a block arbitrarily slow, and one hostile infinite loop would stall everyone. Bounded work per transaction is what keeps replay predictable, so each transaction gets a hard ceiling of 1.4M CU.

Blocks carry ceilings of their own, and those have been climbing, raised repeatedly through SIMDs, the chain's improvement proposals: 48M → 50M → 60M CU through 2025. I read that sequence as a speed limit under permanent renegotiation, moving up as validator hardware and client software improve. The per-transaction cap bounds the worst single offender; the block cap bounds the total replay bill.

If compute units have only ever been the number that killed your transaction, this is all they are: a meter and two ceilings, protecting everyone else's ability to check your work.

## Getting the block to everyone, without uploading it to everyone

The banking stage executed your transaction, and the leader stamps the results as entries into the PoH stream (the same hash chain your blockhash came from, the clock closing its own loop). Now the block has to reach every other validator, fast, before the leader's turn is over.

The naive design has the leader upload the full block to each validator, point to point. Follow that to its end and the leader's upstream bandwidth becomes the throughput ceiling for the entire network, and it gets worse with every validator that joins. Broadcast-by-brute-force punishes exactly the growth you want.

Solana's answer is Turbine. The block is erasure-coded and sliced into shreds, and the shreds travel down a stake-weighted fan-out tree: the leader sends to one layer of nodes, each of those forwards to its own children, and so on, so no single node ever uploads the block to everyone. If that sounds like the trick torrents use to move big files, same family, here applied to a block on a deadline. The erasure coding is the underrated half: it adds redundancy so a validator can reconstruct the block even when some shreds never arrive, and on real networks, some shreds never arrive.

## Three words for "done"

Your transaction is now executed, stamped, shredded, and scattered. Done? Depends entirely on what you mean by done, and Solana makes you pick between three meanings instead of pretending there's one.

The receiving validators reassemble the block and replay it (the Replay stage), re-executing everything to verify the leader's work, and then they vote. One detail here is too clean to skip: votes are themselves transactions. The ballots ride the same rails as your transfer, through the same pipeline, into the same blocks.

Those votes are what your RPC commitment setting is actually reading:

- **`processed`**: the leader's bank saw your transaction. One machine's word. Fine for showing a "pending" spinner, and for nothing else.
- **`confirmed`**: optimistic confirmation, meaning at least 2/3 of stake has voted on the block.
- **`finalized`**: the block is rooted, with 31+ confirmed blocks built on top of it.

The interesting question is why anyone treats `confirmed` as trustworthy when it isn't final. The answer is a price tag: rolling back an optimistically confirmed block requires at least 1/3 of stake to be slashable. Not impossible, and anyone who tells you it's impossible is selling something. It's a rollback whose cost is explicit, enormous, and provable, which for most product decisions lands close enough to never.

So why three levels instead of one? Because "done" is really a risk question, and different actions price risk differently. A balance display, a swap confirmation screen, and a bridge withdrawal should not wait for the same guarantee. What do I actually use? Honestly: `confirmed` for anything user-facing, `finalized` for anything I can't take back, crediting a deposit, releasing goods, unlocking something off-chain. Waiting for `finalized` when `confirmed` is sitting right there feels slow every single time, and I do it anyway, because the rare case where they differ is precisely the case you cannot undo.

## The three ways transactions actually die

Back to the error from the first paragraph, because it finally has anatomy. Nearly every failed transaction you will ever debug on this chain is one of three stories:

- **The blockhash expired.** Your transaction didn't land within its 150-block window. Resending the same signed bytes past `lastValidBlockHeight` does nothing; the transaction is dead everywhere. Watch the height, and once the window passes, re-sign with a fresh blockhash. That's the retry semantics the expiry was designed to hand you.
- **The fee lost a local auction.** You touched a writable account everyone else wanted in the same moment, and your priority fee didn't clear that account's going rate. The chain wasn't congested; one intersection was. Bid for the account you're actually contending on, or restructure so you stop touching it.
- **Lock contention serialized you.** The work you assumed was parallel wasn't, because your declarations said otherwise: a writable flag on something you only read, or one hot account every code path funnels through. The scheduler did exactly what you asked.

Notice what's missing from that list: mystery. Each failure is a specific stage doing its declared job, which means each one is debuggable from first principles instead of from vibes.

This ran longer than I planned, so let me land it.

## One refusal, five layers

Strip away the vocabulary and the whole lifecycle derives from a single refusal: never make everyone wait for anyone. The expiry window refuses unbounded dedupe memory. Gulf Stream refuses to make the entire network babysit pending transactions. Account locks refuse to serialize strangers. The compute meter refuses unbounded replay. Turbine refuses to choke on one uploader's bandwidth. Same decision, five layers deep.

Next time a transaction dies on you, don't retry and pray. Name the stage that killed it. You know all five now, and honestly, that puts you ahead of a lot of people shipping on this chain every day. It's not that hard once you've walked the pipe. If you trace one end to end and something surprises you, my DMs are open. Happy building! 🚀
