---
slot: named-taxonomy
length_words: 126
topic: solana-commitment-levels
fk_grade: 13
demonstrates: [named-taxonomy, reason-inside-the-frame, paired-cost-tradeoff, compared-to-what, average-vs-worst-case]
source: neutral-voice (new demo)
---
"Is the transaction done?" has no single answer on Solana; it has three, and naming them is the explanation. Confirmation comes in tiers: *processed* (the leader ran it), *confirmed* (a supermajority of validators voted for its block), and *finalized* (that block is buried deep enough that reverting it would cost the network its own stake).

Place a use case in the frame and the tradeoff names itself. A balance refresh in a wallet UI can read *processed* — fast, but on a discarded fork it silently rolls back. An exchange crediting a deposit must wait for *finalized*: seconds slower, yet safe against the worst case, a reorg, not just the average one. The cost you pay for certainty is latency, measured against exactly how expensive a mistaken reversal would be.

<!-- MOVE TRACE: build a NAMED TAXONOMY (processed / confirmed / finalized) and make coining it the explanation → reason INSIDE the frame by placing examples in it (wallet UI → processed; exchange deposit → finalized) → paired-cost tradeoff (speed bought with rollback risk; safety bought with latency) → average-vs-worst-case named explicitly (a reorg is the worst case, not the average) → "compared to what?" (latency judged against the cost of a mistaken reversal). Different move-lead than 01/02: taxonomy-first, no naive-fix ladder. Idiolect stripped — no Alice/Bob, no asides. -->
