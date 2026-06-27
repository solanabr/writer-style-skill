---
slot: forces-as-actors
length_words: 138
topic: solana-priority-fees-local-fee-markets
fk_grade: 9
demonstrates: [forces-as-actors, socratic-beat, kinetic-verbs, define-as-you-go, falsifiable-actionable-close]
source: neutral-voice demo
---
Think of a toll road where the busy lane prices itself, and only that lane. That's a local fee market — and Solana runs one per account, not one for the whole chain.

So who sets the price? The traffic does. When a popular account gets hot, every transaction that wants to *write* to it competes, and the bid that wins is the compute-unit price — the small tip, in micro-lamports per unit of work, you attach to jump the queue. The validator collects that tip in full; it doesn't burn. And here's the kind part: a transaction touching a *quiet* account pays nothing extra and still lands in the same block. Congestion stays in its lane.

What to watch: pull recent fees for the *exact* accounts your transaction locks, not the whole network — that's your real floor.

<!-- MOVE TRACE: organizing image introduced and DEFINED in one clause ("a local fee market — Solana runs one per account") → Socratic question-then-answer beat ("So who sets the price? The traffic does.") → force-as-actor with a motive ("every transaction that wants to write… competes"; "the validator collects that tip") → kinetic verbs for invisible events ("jump the queue," "still lands," "stays in its lane") → falsifiable + actionable close ("pull recent fees for the EXACT accounts your transaction locks… your real floor"). Builder-optimist tone: "here's the kind part" frames the local design as a FEATURE, not a tollbooth shaking you down. No villain, no doom. Facts: priority fee = compute_unit_price × CU limit / 1e6; 100% to validator (SIMD-0096); per-account write contention. -->
