---
slot: show-the-real-artifact
length_words: 320
topic: solana-transaction-account-and-instruction-model
fk_grade: 11
demonstrates: [front-load-the-takeaway, show-the-real-struct, walk-field-by-field, inline-gloss, anchor-to-the-known, named-actor-worked-example, quantify-with-units, capability-with-its-limit]
source: persona worked micro-example (neutral voice — idiolect already stripped)
---
A Solana transaction is a small bundle of two parts: a list of signatures and a message. The message
holds the work:

    pub struct Message {
        pub header: MessageHeader,      // how many signers / read-only accounts
        pub account_keys: Vec<Pubkey>,  // every account this tx will touch
        pub recent_blockhash: Hash,     // freshness stamp; stale ones are rejected
        pub instructions: Vec<CompiledInstruction>,
    }

If you've used Ethereum, the contrast is the fastest way in: there a transaction targets one contract
and the chain discovers what state it touches as it runs. A Solana transaction instead declares *up
front*, in `account_keys`, every account it will read or write. That declaration is the load-bearing
choice. Because the runtime knows the full access list before executing, it can run non-overlapping
transactions at the same time.

The unit of work inside the message is the instruction, one call to one program:

    pub struct Instruction {
        pub program_id: Pubkey,          // which program runs
        pub accounts: Vec<AccountMeta>,  // accounts it may touch, each flagged signer/writable
        pub data: Vec<u8>,               // opaque bytes the program decodes itself
    }

(What you build is this `Instruction`, with full addresses; once packed into the message it becomes a
`CompiledInstruction`, each account replaced by an index into `account_keys` above, the same data
compacted.)

Concretely: Alice sends Bob 10 SOL → one instruction, `program_id` = System Program, `accounts` = [Alice
(signer, writable), Bob (writable)], `data` = encoded "transfer 10 SOL." A transaction can hold several
instructions, run in order and atomically: all succeed or none do.

Two limits belong next to the capability. The transaction must fit in 1232 bytes, so at 32 bytes per
address you can name only ~35 accounts directly before needing an Address Lookup Table. And `data` is
just bytes: the program, not the runtime, must validate that the accounts it got are the ones it
expected. That is why so many Solana bugs are missing checks.

<!-- MOVE TRACE: front-load the takeaway → show the real Message struct and walk it field by field with inline glosses → anchor to the reader's Ethereum model → show the Instruction struct, annotate the Instruction→CompiledInstruction delta inline → trace one named actor (Alice/Bob) with concrete values → pair the capability (parallelism) with its limits (1232-byte cap → ~35 accounts; attacker-controlled data → missing-check bugs), quantified with units. Neutral voice: no borrowed headers, no "(i.e., …)" tic, no ritual labels. -->
