# What actually happens to your transaction: the Solana lifecycle, end to end

You call `sendTransaction`, you get a signature back, and then: silence. The explorer has never heard of it. A minute or two later your app surfaces an expired-blockhash failure to a user who just wanted to send somebody a token, and you do what most of us do. Retry, shrug, move on. I shipped on Solana for a long time treating everything below the RPC as weather: rain happens, transactions drop, you carry an umbrella and a retry loop. Not proud of it.

Here's the thing though: it isn't weather. Every stage between your `sendTransaction` call and finality exists because a specific naive design fails in a specific way, and once you can see those failures, a vanished transaction stops being a mystery and becomes a diagnosis. So let's trace one transaction all the way down, and instead of just naming the stages (you've seen that diagram a hundred times) let's derive why each one has to exist: why your transaction expires, why there is no mempool for it to wait in, why you're forced to declare every account before you send. By the end, "my transaction disappeared" turns into a question with three likely answers, and you'll know how to tell which one you're staring at.

Tag along.

## The envelope you're actually sending

Strip the client libraries away and a transaction is a small, rigid envelope: a list of signatures, then a message. The message holds a header, the list of account keys, a recent blockhash, and the instructions. That's the whole artifact.

Two of those fields should bother you.

First, the account list. Every account an instruction will touch gets declared up front, each one marked writable or read-only. Coming from other chains this feels like pointless bureaucracy, your code already knows what it touches, so why would the runtime need the guest list in advance, in writing, before a single instruction is allowed to run? Hold that thought. It turns out to be the most consequential design decision in the whole pipeline, and we'll earn it properly when we reach the banking stage.

Second, the recent blockhash. A hash of recent history, sitting inside your transaction. It looks like a checksum. It's actually a timestamp, and the reason it exists answers one of the oldest problems in this field.

Both fields are your transaction pre-answering questions the runtime would otherwise have to ask at the worst possible moment. Keep that framing; most of what follows is machinery built to cash in those two pre-answers.

## Why your transaction expires

So, why would a transaction need a timestamp at all?

Start from the wall every chain hits: replay. A signed transaction is just bytes, and anyone who sees those bytes can submit them again. Your payment must execute exactly once, so the network needs some way to recognize the second copy of it, forever, or your one coffee becomes eleven.

The naive fix is a global memory: remember every transaction ever seen, reject repeats. That means an unbounded, forever-growing set that every validator must consult on every incoming transaction until the end of time. Dead on arrival. The classic fix is the per-account counter: each transaction carries the next number in your account's sequence, and a replay gets rejected because its number was already spent. It works, and you pay for it with strict ordering: nothing you sign can land until everything you signed before it lands, one stuck transaction dams the whole queue behind it, and pre-signing things for later gets awkward.

Solana picks a third option: make transactions perishable. Stamp each one with a recent reading from a clock the whole network shares, and only accept it while that reading is fresh. The clock is Proof of History; the reading is the recent blockhash your transaction carries. A transaction is accepted while its blockhash sits within the last 150 blocks (the constant is literally `MAX_PROCESSING_AGE = 150`), which is why your client computes `lastValidBlockHeight` as the current block height plus 150. Blocks, not slots! Everyone misreads that at least once, me included. In wall-clock terms you get roughly 60–120 seconds of life.

Now the impossible memory problem is small. A validator only has to remember what it saw inside a 150-block window, because anything older is invalid by construction.

It's the same trick that cracked navigation in the age of sail. To know your longitude you need to know the time at a reference point far away, and once ships carried an accurate clock on board, position stopped being a conversation with the shore and became a local calculation. A shared clock turns a coordination problem into a comparison. Solana's clock is the chain itself: your transaction quotes a tick of it, and any validator can check that quote against history it already holds.

The cost is real, and you pay it weekly: a signed transaction is milk, not wine. Let it sit past the window and it dies, which is precisely failure mode number one, the expired blockhash. For the cases where fresh signing is impossible (offline signing, or a signature set that takes days to collect) the protocol ships durable nonces, the deliberate escape hatch from perishability.

## There is no mempool

I lied a little earlier, when I said your RPC submits the transaction to the network. There is no "the network" to submit to: no shared, public waiting room where transactions pool until a block producer picks through them. On most chains that room, the mempool, exists for one honest reason: nobody knows who will produce the next block, so a pending transaction has to be everywhere at once, just in case.

Solana deletes the premise. The leader schedule is known an epoch in advance, so at any given moment every node can tell you who the current leader is and who's up next. And once you know who's next, broadcasting to thousands of nodes is pure waste. Your RPC node forwards the transaction directly to the current leader and the next scheduled ones. That's Gulf Stream: submission as a courier with an address instead of a message in a bottle.

The consequences fall out fast once you hold that picture. Your pending transaction has no public existence, it isn't sitting "in the network," it's sitting in the queues of a handful of specific machines, so when a leader under load sheds it, there is no pool somewhere keeping a copy alive for the next block — that's why a dropped Solana transaction is silent. Second consequence: combined with the expiry window, you get an unusually clean contract, either the transaction lands within its 150 blocks or it provably never will. What reads as flakiness is a crisp, checkable promise. Third: with no global lobby to out-bid, the fee market has to live somewhere else, and it moves down into the leader's scheduler. Which is where we're going next.

## Inside the leader: one pipeline, one scheduler

While it's the leader's turn, transactions pour into its TPU, the transaction processing unit, which is a pipeline: Fetch pulls packets off the wire, SigVerify checks signatures, the Banking stage executes, PoH stamps what happened into the stream, broadcast ships it out. Fetch and SigVerify are what they sound like, plumbing for throughput, nothing to derive. Banking is where the design lives.

The banking stage wants something that sounds contradictory: execute as many transactions at once as physically possible, while producing a result identical to running them one at a time. Run everything in parallel blindly and two writes to the same account corrupt each other. Detect the conflict mid-execution and roll back? You already paid for work you're now throwing away. So the honest question is narrower: how can a scheduler know which transactions are safe to run together before executing a single one of them?

It can't. Not unless somebody tells it. Guess who tells it.

The guest list from section two, the account list every transaction declares, is the answer to a question you didn't know the runtime was asking. The scheduler reads each transaction's declared accounts and takes locks: writable account, exclusive lock; read-only account, shared lock. Transactions touching disjoint accounts get assigned to different executor threads and run in parallel (this is Sealevel), while transactions contending on the same writable account get serialized behind each other. It's a reader-writer lock, the same one from every systems codebase you've ever touched, promoted into the consensus layer. That up-front declaration is the entire reason parallel execution is possible here.

Execution itself is metered. Your program is SBF bytecode (an eBPF derivative) running inside the Solana Virtual Machine, and every step costs compute units: a single transaction gets a ceiling of 1.4M CU, and the block has its own ceiling too, one that has kept climbing by governance, 48M to 50M to 60M CU through 2025, raised SIMD by SIMD.

Now the consequence you feel in production. Locks are per-account, so contention is per-account. A thousand people hammering one hyped mint (ok fine, one memecoin pool) are fighting over one exclusive lock, while your unrelated transfer, touching none of those accounts, doesn't even notice the war. Congestion on Solana is local, not global, and fees inherit the same shape: a fee is effectively a bid for specific locks rather than for the block as a whole, which is what people mean by local fee markets. So when your transaction "won't land," the productive question is not "is Solana congested," it's "is my writable account congested." Different question, different fix.

And the trade-off, named, because there's always one: all this parallelism is bought with your inconvenience. You must know every account before you send, which gets awkward when the address you need depends on data you haven't read yet. And if you get lazy and over-declare accounts as writable, you serialize yourself against strangers for no benefit at all. The guest list is a contract: the tighter you write it, the more parallelism the scheduler pays back.

## Turbine, or how to ship a block without a firehose

The leader has executed, stamped the entries into the PoH stream, and now owes the network a block. The naive version: upload the full block to every validator, one by one. Count the recipients and it collapses immediately, the leader's uplink becomes the whole network's ceiling, and every validator that joins makes the leader's day strictly worse. Decentralizing would literally slow the network down. It doesn't scale.

So the block travels as a relay instead. The leader slices it into shreds, erasure-codes them (a receiver can rebuild the whole from a subset, so lost packets don't trigger rounds of please-resend), and pushes different shreds to different validators, who forward them onward through a fan-out tree weighted by stake. Turbine is basically a phone tree for blocks: no single node, leader included, ever uploads the whole thing to everyone; the network distributes the block to itself, reach multiplying at every hop.

ps: when you want full depth on any stage here, the Anza docs are the real reference (this piece is the why, they're the what), and they've gotten genuinely readable.

## Processed, confirmed, finalized: three different promises

Every other validator now replays the block. The Replay stage re-executes what the leader executed and checks the results match, and then validators vote, and the votes aren't whispers in some committee, they're transactions, on-chain like everything else. Notice the pattern across the whole pipeline: SigVerify didn't take your word for the signatures, Replay doesn't take the leader's word for the execution. Don't trust, verify, industrialized.

Which is why "is my transaction done?" is really three different questions with three different price tags:

**Processed** means the leader's bank saw it. One machine's view. Fine for optimistic UI and nothing else.

**Confirmed** means optimistic confirmation: at least 2/3 of stake has voted on the block. And here the economics are the guarantee — rolling back an optimistically confirmed block requires at least 1/3 of stake to be slashable. Read that carefully: the guarantee is economic, a third of all the stake securing the network would become provably destroyable. The promise: undoing this costs someone a fortune.

**Finalized** means rooted: 31+ confirmed blocks built on top. The chain has moved on so far that reversal stops being a live consideration.

So choose by blast radius. A balance display updating is a `confirmed` decision. Anything irreversible on your side of the boundary (you ship a product, you release funds, you hand over the thing) deserves `finalized`. If undoing it would hurt you, wait for the root.

And if you've made it this far, notice we quietly finished the map. Born in your client, stamped with a clock reading, couriered straight to a known leader, lock-scheduled, executed and metered, stamped into PoH, shredded through a stake-weighted tree, replayed by everyone, voted into confirmation, buried into finality. Every stage is a wall somebody hit; every wall became a design.

## Where transactions actually go to die

Back to the transaction that vanished at the top of this piece, because it now has three likely graves, and they're the same three that dominate real-world debugging.

One, it expired. It never reached a leader's banking stage inside its 150-block window, slow forwarding, a shedding leader, plain bad luck, and past `lastValidBlockHeight` it is dead by definition. The signature you keep searching for will never appear. Silence, then certainty. The fix lives at submission time: a fresher blockhash, or a durable nonce when fresh signing isn't an option.

Two, it lost the auction for a lock. It arrived fine, but the writable account it needed was hot and the fee didn't justify a place in that account's line. The tell: everything else you send lands, this one category doesn't. The fix is a fee aimed at that specific market, not a global panic about "congestion."

Three, it serialized. It even landed, but your throughput cratered, because transactions you assumed were parallel all declared the same writable account and the scheduler did exactly what you told it to. Nobody dropped you. Your own guest list queued you. The fix is architectural: shrink the write set, stop making everything touch the same account.

I once spent two hours debugging a deploy, completely certain the bug was in our code, before realizing we had managed to break the Goerli testnet itself. The lesson traveled with me: when something dies silently, the layer you're staring at is usually not the layer that killed it. Which is the whole reason to own this map.

So next time a transaction vanishes, interrogate it. Did it expire before any leader saw it? Did it lose the fee auction for one hot lock? Did its own write set serialize it? Three questions, three graves, three completely different fixes, and not one of them is weather.

The bigger point, and then I'll let you go: a chain stops being intimidating the moment you stop treating it as climate and start reading it as a machine, one deliberate decision at a time. You don't need to be a validator engineer for that. You just traced a transaction end to end in one sitting, walls, trade-offs and all! Design with the machine from now on: tight guest lists, fees aimed at the lock you need, a durable nonce when signing runs slow. And if you trace one of yours and something down there still refuses to add up, tell me about it. Genuinely. I collect these.

cya 👋
