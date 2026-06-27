---
slot: scaling-ladder
length_words: 135
topic: solana-parallel-execution
fk_grade: 9.3
demonstrates: [scaling-ladder, thesis-earned-rung-by-rung, named-pillar-bounded, peer-altitude]
source: neutral-voice move-demo
---
Start somewhere uncontroversial: most transactions in a block never touch the same accounts. A swap on one pair and a transfer between two strangers have nothing in common to fight over. So if you knew, ahead of time, exactly which accounts each transaction would read and write, you could sort them into groups that don't overlap. Solana asks every transaction to declare those accounts up front. Grant that, and the next rung follows: groups that share no account can run at the same time without corrupting each other, because there is nothing to race over. Climb one more, and the busy ones — the popular market everyone wants — fall back to running in line, exactly where ordering still matters. The throughput isn't magic; it's the share of work that happened to be independent, run in parallel.

<!-- MOVE TRACE: the scaling ladder — earn a bold claim ("Solana runs transactions in parallel") one agreeable rung at a time. Base case nobody disputes (most transactions don't share accounts) → rung (if accounts are declared up front, you can group the non-overlapping ones) → the load-bearing fact (Solana requires that declaration) → rung (disjoint groups can run simultaneously, because there's nothing to race over) → bound it honestly (contended accounts fall back to serial — the gain is only the independent share). Peer altitude; the closing line is a portable restatement, not a slogan. -->
