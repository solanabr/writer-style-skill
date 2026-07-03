# The 150-block life of a Solana transaction

Quick trivia question: when you call `sendTransaction`, where does your transaction wait in line?

Take a second with that one. On most chains the answer is the mempool, that big public waiting room where pending transactions get gossiped around the network, inspected by strangers, and eventually scooped up into a block. Explorers have a tab for it, entire industries live inside it. So where's Solana's?

Trick question. There isn't one. Your transaction never waits in a public line because there is no line, and once you see why, a whole family of Solana behaviors that look like quirks (the expiring blockhash, the account list you have to declare, the fee spikes that hit one app and nothing else) turn out to be consequences of a handful of early decisions. So that's the plan today: one transaction, followed from the moment your code signs it to the moment nobody can take it back, with the why derived at every stop. You push transactions through this machine every day. Let's actually open it up.

## The envelope you're actually signing

A transaction is two things stapled together: a set of signatures, and the message those signatures commit to. The message itself carries four parts, a compact header, the list of account keys the transaction will touch, a recent blockhash, and the instructions to execute.

One item in that list is quietly the boldest design decision in the whole system: every account an instruction touches is declared up front, before anything runs, and each one is marked writable or read-only. Most execution environments let code wander wherever it likes and figure out what it touched afterwards; Solana demands the complete guest list, with permissions, before the party starts. The writable flag is you promising you might change that account, the read-only flag is you promising you won't, and the network is going to take both promises far more seriously than you'd expect.

The reason is worth spelling out, because it pays for everything else: that declaration is what makes parallel execution possible. If the runtime knows ahead of time which transactions touch which accounts, it can run the non-overlapping ones simultaneously instead of forcing all of them into a single line. We'll watch that payoff land in a few sections, inside the leader. For now, write the principle on a sticky note, because it's the spine of this entire piece: **the runtime hates surprises.** Solana keeps asking you to state things up front, which accounts, how fresh, how much compute, so that nothing has to be discovered mid-flight. Keep the sticky note handy. We'll need it at least twice more.

## Born with an expiry date

The third field in that message, the recent blockhash, is your transaction's timestamp. It is also its death clock.

The hash you attach is a recent Proof-of-History hash, and it tells the network roughly when your transaction was built. A transaction stays acceptable while its blockhash sits within the last 150 blocks (the constant in the codebase is literally `MAX_PROCESSING_AGE = 150`), and the `lastValidBlockHeight` your RPC hands back is simply the current block height plus 150. That's blocks, mind you, not slots, a distinction that will bite you exactly once in your life and then never again, at least that's how it went for me. In wall-clock terms the window works out to roughly 60 to 120 seconds, which sounds generous until you're submitting during congestion and the clock is eating your retries one by one.

Now the derivation. Why would a chain make transactions perishable at all? Go back to the trivia question: there's no mempool, so there is no waiting room where an old transaction can sit until conditions improve. A transaction either reaches a leader while it's fresh or it never lands, which means freshness can't be a property of some queue that doesn't exist, it has to live inside the transaction itself. The recent blockhash is exactly that: a printed expiry date on the envelope. And my honest read is that the expiry is the design doing you a favor, because a signed transaction that stays valid forever is a thing you have to worry about forever, while one that dies within 150 blocks is a thing you can safely forget.

I'll confess how I actually learned this. My first retry loop just re-sent the same signed bytes over and over, well past the window, while I sat there wondering why the network had stopped caring. It hadn't stopped caring. It had read the expiry date I was ignoring.

And when you genuinely can't sign fresh, offline signing, say, or a multisig ceremony that takes days to gather signatures, durable nonces exist for exactly that case.

## The line that doesn't exist

So if there's no mempool, what does your RPC node actually do with the transaction you hand it?

It checks the leader schedule, which is public and known a full epoch in advance, and forwards your transaction directly to the current leader and the next scheduled ones. That forwarding path is Gulf Stream, and honestly the name makes it sound fancier than it is: your RPC node is a courier with the delivery route taped to the dashboard, nothing more mystical than that. A mempool is the thing you build when you don't know who will produce the next block: since anyone might, everyone must hold the pending set. Solana always knows. When the producer's identity is public ahead of time, broadcasting your transaction to the whole town square is pure waste; you mail it to the one machine that can actually include it, plus the next in line in case the first misses its turn.

It's the sticky note again. The runtime hates surprises, and the network layer turns out to share the allergy: the leader schedule is declared an epoch ahead so that delivery can be a straight line instead of a flood.

The trade-off is real, though, and worth naming. With no public pool, your transaction's fate depends on reaching one specific machine inside one specific slice of time, which is exactly why the expiry stamp from the last section has to exist. Fresh or dead. There is no third state to wait in.

## Inside the leader

Picture the machine whose turn it is. Your transaction has just arrived at it, and here I want to slow way down, because almost everything people find confusing about Solana performance lives inside this one building.

The leader runs a pipeline called the TPU: Fetch → SigVerify → Banking stage → PoH → broadcast. Fetch pulls packets off the wire. SigVerify checks signatures and does nothing else. Those are the routine floors of the building and the elevator doesn't stop long. The Banking stage is where your sticky note finally pays for itself.

Picture the scheduler's problem. It is holding a pile of verified transactions and a bank of executor threads, and it wants to keep every thread busy at once. The naive answer, just run everything simultaneously, dies on contact: two transactions writing the same account at the same time is corrupted state, full stop. The next answer up, run everything and catch collisions as they happen, is better but still bad, because by the time you notice the conflict you've already burned the compute and have to throw the work away. What the scheduler actually needs is a way to know, before executing anything, which transactions can safely share a moment. Sound familiar? It's exactly the information you were forced to declare back in section one.

The account list you signed becomes the scheduler's lock table. A writable account is an exclusive lock: one transaction at a time, no exceptions. A read-only account is a shared lock: everyone can read together, nobody blocks anybody. Transactions whose account sets don't overlap get dealt out to separate executor threads and run in parallel, which is the runtime people call Sealevel, while transactions that contend on the same writable account get serialized behind each other, one at a time, exactly like they would on a single-threaded chain.

The consequence is the most useful fact in this piece: congestion on Solana is local, not global. When a hyped mint or one hot trading pool gets slammed, the fight is over that account's exclusive lock, and transactions touching anything else keep sailing through untouched threads. Fees spike where the contention is and stay flat everywhere else. That's local fee markets, and for anyone who has watched an entire chain's fees go vertical because one NFT collection dropped at noon, it is a genuine godsend.

The paired cost lands on you, though, and it deserves to be said out loud. You have to know your complete account list before you send, which gets genuinely awkward when the account you need next depends on data you haven't read yet, and if you over-declare accounts as writable just to be safe, you hand the scheduler exclusive locks you never needed and serialize yourself against neighbors you were never actually fighting. The whole parallel machine was bought with the honesty of that list, so a sloppy declaration doesn't crash anything, it just quietly costs you the thing you came here for. Hold that thought; it comes back at the end of the piece as one of the classic ways a transaction dies.

Once your transaction is scheduled onto a thread, the programs it calls actually execute. Program code on Solana is SBF bytecode, an eBPF-derived format, running inside the Solana Virtual Machine, and every operation is metered in compute units. Your transaction gets a hard ceiling of 1.4M CU. Blocks carry their own ceilings on top of that, and those have been raised repeatedly through SIMDs, 48M to 50M to 60M CU through 2025, as the runtime squeezed more out of the hardware. The meter is the same philosophy one more time, if you squint: state your compute appetite up front, get scheduled accordingly, and nobody discovers at execution time that your transaction was secretly enormous.

As results come off the threads, the leader stamps the entries into the PoH stream, the same hash chain your blockhash came from, which is a tidy bit of symmetry I didn't appreciate for an embarrassingly long time, and hands the finished material to the broadcast stage. Which brings us to the part of the pipeline almost nobody talks about.

## How a block leaves the building

Here's a bottleneck that's easy to miss: the leader just built a block, and thousands of validators need it. If the leader uploaded the full block to every one of them directly, its bandwidth would become the ceiling on the entire chain, no matter how fast the Banking stage got.

So it doesn't. The block leaves as erasure-coded shreds pushed through Turbine, a stake-weighted fan-out tree: the leader sends shreds to a small first layer of validators, each of those forwards to a layer below it, and so on down the tree, so no single node ever bears the full upload alone. The whole network shares the distribution work, layer by layer, the same way a rumor crosses a stadium faster than any one person with a megaphone could manage. And the erasure coding is what makes the tree safe to lean on, since receivers can reconstruct the block without catching every individual shred, so a few packets lost between layers don't force anyone to start over.

## Replay

Every other validator now re-executes the block's transactions in its own Replay stage, checking the leader's work rather than taking it on faith. The validators that agree with the result vote on the block. And the votes are themselves transactions, riding the exact same pipeline you've been reading about this whole time.

## Three flavors of done

Your wallet says the transaction landed. The real question, the one payment apps and bridges and exchanges genuinely disagree on, is what "landed" should mean, and Solana's answer is that it means three different things at three different prices.

`processed` means the leader's bank saw your transaction: it executed on one machine's view of the world, and that view could still get skipped, so treat it as a progress indicator, nothing more. `confirmed` means optimistic confirmation: at least 2/3 of stake has voted on the block containing it. `finalized` means the block is rooted, with 31+ confirmed blocks built on top of it, and at that point it is, for every practical purpose, carved in.

The interesting one is the middle. What does "optimistic" confirmation actually buy you, concretely? An economic guarantee with a price tag on it: rolling back an optimistically confirmed block requires at least 1/3 of stake to be slashable, so anyone who wants to unwind your transaction has to put a third of everything staked on the network somewhere it can be burned. For a coffee purchase that is the same thing as impossible. For a bridge moving nine figures, it's a number you sit down and actually think about, which is why serious infrastructure waits for `finalized` while your wallet UI happily shows `confirmed`. Choosing a commitment level is just choosing whose risk model you're borrowing. (Complete aside: the same chipped mug has been on my desk through this entire write-up, its third deep-dive now, which is more longevity than most of my drafts get.)

## The three ways your transaction dies

I've met all three of the classic deaths in my own logs, some of them many more times than I'd like to put in writing, and the useful thing about having just walked the pipeline is that each one now has an address.

Death one: the blockhash expired before inclusion. The envelope outlived its stamp. Never re-send the stale bytes; re-sign with a fresh blockhash and you've got a new perishable good.

Death two: your fee was too low for a contended writable account. You joined a local auction, one hot account, one exclusive lock, and bid as if the whole chain were quiet. The rest of the chain WAS quiet. Your auction wasn't.

Death three: account-lock contention serialized what you assumed was parallel. Maybe you declared an account writable when you only needed to read it, maybe your design funnels every user through one shared account. Either way the scheduler did exactly what your account list told it to do.

Line them up and it's the same lesson in three costumes: each death is a surprise, delivered to a runtime that, say it with me, hates surprises. Declare accurately, sign fresh, bid for the lock you're actually fighting over, and this machine turns out to be almost boringly cooperative.

## Trace one of your own

Once you can see the pipeline, declared accounts in, Gulf Stream to a known leader, locks and threads in the Banking stage, shreds down the Turbine tree, replay, votes, root, error messages stop being noise and start being coordinates. An expired blockhash points at one stage. A fee spike points at one specific lock. Next time one of yours dies, don't just retry it, go find the stage that killed it, because the stage names the fix.

ps: when you build retry logic, track `lastValidBlockHeight` and re-sign once the chain passes it, and remember it counts blocks, not slots. Muscle memory from other chains will fight you on that one. Let it lose.
