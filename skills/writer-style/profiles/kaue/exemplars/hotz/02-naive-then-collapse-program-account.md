---
slot: naive-then-collapse
length_words: 98
topic: solana-program-account
fk_grade: 7
demonstrates: [naive-then-collapse, mechanistic-reframe, unhedged-opener, discriminating-question, portable-close]
source: neutral-voice demo (idiolect stripped — inviting, not dismissive)
---
The tempting mental model: a Solana program is a living object that owns its state and guards it. Build that
out and you expect the program to hold balances, remember who called it, protect its own data.

It doesn't. A program account is just a file the runtime runs — its owner is a loader, its `executable` flag
is on, and its data is code, not state. Here's the test: can it remember anything between calls? No. It reads
and writes *other* accounts; it keeps nothing itself.

So the program is the verb. The accounts are the nouns.
<!-- MOVE TRACE: build the naive wrong model fully and in earnest (a program as a stateful, self-guarding object) → collapse it in one move with a mechanistic reframe ("just a file the runtime runs") anchored to three loader-independent facts: owned by a loader, executable flag on, data is code → hand the reader a discriminating question that settles it ("can it remember anything between calls? No") → portable close ("program is the verb, accounts are the nouns"). Honest collapse: true across all BPF loaders — it claims data is *code*, not that the ELF bytes sit in the program account (that's loader-v3 detail), so no edge case is dropped. Neutral voice: inviting, no posture, no tics. -->
