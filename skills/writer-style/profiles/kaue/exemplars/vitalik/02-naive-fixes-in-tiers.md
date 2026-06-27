---
slot: naive-fixes-in-tiers
length_words: 121
topic: solana-proof-of-history
fk_grade: 12
demonstrates: [status-quo-limit, motivating-question, naive-fixes-in-tiers, just-in-time-definition, build-to-conclusion-through-steps]
source: neutral-voice (new demo)
---
A blockchain has to agree on the order of events, but the network has no shared clock. So how do nodes agree on what happened first?

The naive fix — trust the leader's wall-clock timestamp — fails, because the leader can lie about time to reorder transactions in its favor. The next fix — have every node gossip and vote on timestamps — fails differently: that negotiation is exactly the slow consensus you were trying to speed up. So the requirement is sharper: produce *verifiable* elapsed time without asking anyone.

That forces a delay function. Proof of History hashes each output into the next input, sequentially; the chain's length is itself a clock no one can fake or fast-forward.

<!-- MOVE TRACE: status-quo + concrete limit (no shared clock) → motivating question (how to agree what happened first?) → naive fixes ruled out IN TIERS (trust leader's clock → it can lie; gossip+vote on timestamps → that IS the slow consensus you were avoiding) → sharpened requirement (verifiable elapsed time without asking anyone) → just-in-time definition (PoH as a sequential hash chain = an unfakeable clock). Different move-lead than 01: tiers-forward, no analogy, builds to the conclusion through visible steps. Idiolect stripped. -->
