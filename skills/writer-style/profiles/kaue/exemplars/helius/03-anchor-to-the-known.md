---
slot: anchor-to-the-known
length_words: 96
topic: solana-address-lookup-tables
fk_grade: 12
demonstrates: [anchor-to-the-known, map-part-for-part, quantify-with-units, capability-with-its-limit, inline-gloss]
source: neutral-voice demo (idiolect stripped)
---
Start from the model you already have. A legacy transaction lists every account inline at 32 bytes each, and must fit in 1232 bytes — which caps you near 35 accounts. An Address Lookup Table (an on-chain account holding up to 256 public keys) changes that: store the addresses once, then a versioned (v0) transaction names each by a 1-byte index instead of the 32-byte key, lifting the ceiling to 256.

One limit rides along: signers cannot be loaded through a table. Each signer's full address still appears in the transaction, so signature checks stay verifiable.

<!-- MOVE TRACE: anchor the new mechanism (ALTs) to the reader's known model (the inline-account legacy transaction), mapped part-for-part — 32-byte inline key → 1-byte table index → quantify the delta with units (1232-byte cap; ~35 → 256 accounts; 31 bytes saved each) → gloss the term inline on first use (ALT = on-chain account holding up to 256 keys) → pair the capability with its limit (signers can't be table-loaded). Neutral voice: no borrowed headers or sign-offs. -->
