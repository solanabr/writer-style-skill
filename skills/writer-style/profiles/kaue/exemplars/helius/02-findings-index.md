---
slot: front-load-a-findings-index
length_words: 88
topic: solana-compute-budget-and-priority-fees
fk_grade: 12
demonstrates: [front-load-a-findings-index, self-contained-conclusion-bullets, quantify-with-units, capability-with-its-limit, inline-gloss]
source: neutral-voice demo (idiolect stripped)
---
Before the walkthrough, the conclusions, each standalone:

- Instructions are metered in compute units (CUs) — the runtime's gas. A non-builtin instruction gets 200,000 CUs by default; a transaction is capped at 1,400,000.
- The priority fee is `compute_unit_price × compute_unit_limit`, divided by 1,000,000 to reach lamports. It bills the *requested* limit, not the CUs burned, so simulate and set the limit to the measured value plus ~10%.
- This buys priority, not inclusion: it improves your odds in a congested block but does not guarantee the slot.

<!-- MOVE TRACE: front-load a findings index where each bullet is a self-contained conclusion (the number, the formula, the verdict), NOT a table of contents → glossing inline on first use (CU = the runtime's gas; price = micro-lamports per CU) → quantify with exact figures and units (200,000 / 1,400,000 CUs; ÷1,000,000) → pair the capability with its limit (priority ≠ guaranteed inclusion). Neutral voice: no ritual "Key Takeaways" label, no "anon" address. -->
