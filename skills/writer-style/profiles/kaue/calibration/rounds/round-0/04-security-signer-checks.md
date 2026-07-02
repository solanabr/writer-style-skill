# The missing signer check: Solana's most boring $50M bug

Picture the post-mortem you never want to write. The vault is empty, and the attacker didn't steal a private key, didn't break any cryptography, didn't find some exotic edge case in the runtime. They read your program, noticed the withdraw instruction takes an "authority" account, and put your admin's pubkey in that slot of a transaction they assembled themselves. Your program checked that the pubkey matched the one stored in the vault. It did match. It always will — pubkeys are public. Then it paid out.

That's the missing signer check: the most boring exploit class on Solana, and among the most expensive. One absent line of code, and the attack is just a well-formed transaction any stranger can build.

## The shape of the bug

The class is exactly this: an instruction handler treats an account as the authority without verifying that the account actually *signed* the transaction. Once that check is missing, any caller can pass any pubkey as the authority and act on its behalf.

Why is that even possible? Because accounts arrive at your program as a list the caller assembled, and being on that list proves nothing: the caller picked every entry, the same way they picked the instruction data. Comparing a passed-in pubkey against the one you stored at initialization only proves the caller can read public account data and copy a pubkey into a transaction, which, on a public ledger, anyone can do. The one thing a transaction actually proves is which keys signed it. If your handler never asks that question, controlling the authority key is not required for acting as the authority.

So the vulnerable handler reads completely reasonably. Load the vault state, confirm the passed account's pubkey equals the stored authority, mutate. Every test goes green, because your tests pass the real authority and sign with it. You wrote both sides of the conversation; of course they agree.

## Why this keeps happening

Partly because the happy path hides it. Localnet: green. Devnet: green. The demo: flawless. A missing signer check produces zero failures until an adversary shows up, and adversaries show up where the money is, which tends to be mainnet, months after anyone last stared hard at the accounts logic.

And partly because of where Solana places the responsibility: nothing outside your program knows which accounts an instruction needs consent from. That judgment belongs to your handler, so every account it touches is an unauthenticated input until your code says otherwise.

I've shipped this bug, for what it's worth. An early escrow of mine had a cancel instruction that checked the authority by pubkey comparison alone; a teammate caught it reading the accounts code, not running it. Nothing was lost except a little confidence. The uncomfortable part was realizing every test I'd written was structurally incapable of catching it.

## The fix, in native Rust

One line:

```rust
if !authority.is_signer { return Err(...) }
```

Fill in whatever unauthorized error your program defines. Forgetting this one line IS the bug. There's no subtle variant underneath, no deeper mechanism to study; the check is explicit, and it has to appear for every account whose consent the instruction implies.

## Anchor: you need both constraints

So Anchor makes this impossible? Not quite. Anchor gives you `Signer<'info>`, which enforces the signature at deserialization: if the account didn't sign, your handler never runs. Declaring the type declares the check, which beats remembering a line every single time.

But look at what each constraint proves on its own, because either check alone is incomplete:

- **`Signer` without `has_one`**: any signer passes, not the right one. An attacker signs with their own key, and your program greets them as the authority.
- **`has_one` without `Signer`**: the right account, but nobody proved they control it. You're back to pubkey matching, the exact bug from the top of this piece.

Pair them and the hole closes: `has_one = authority` on the state account means the signer must also *match* the stored authority.

```rust
#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(mut, has_one = authority)]
    pub vault: Account<'info, Vault>,

    pub authority: Signer<'info>,
}
```

One honest caveat before you relax. Anchor moved the check from a line you can forget into a type you must choose, and the choosing is still on you: type that account as anything other than `Signer` and the program compiles without complaint. Better odds. Same responsibility.

## One leg of three

The signer check is one leg of the account-validation trio that belongs on every state-mutating instruction: the signer check, the owner check (the account is owned by the expected program), and the address or PDA check (this is the exact account you meant, derived the way you meant). Three questions, roughly: did the right party consent, can this data be trusted, is this even the right account. Skip any one and you've left a different door open. Attackers need one.

This family is where the real losses live. Cashio, March 2022: roughly $52M minted against fake collateral accounts that passed an incomplete validation chain. The root cause wasn't a cryptographic break; it was a missing link in account validation. That's the pattern worth sitting with, honestly — the expensive failures in this class aren't clever. They're a chain of checks with one link absent, found by someone patient enough to go looking.

## How to audit for it

The heuristic I'd hand any reviewer, including you reviewing your own work: for every instruction that mutates state, write one sentence naming WHO may call it. Then find the line of code that enforces exactly that. Not approximately that; exactly that. If the sentence says "only the vault authority" and the constraint says "any signer", the gap between those two is your finding. And if you can't write the sentence at all, that's also a finding, arguably a worse one. One sentence, one constraint, they either match or they don't. That's the sentence test.

Then go work through `coral-xyz/sealevel-attacks`. It's the canonical teaching catalog for this whole family, and signer authorization sits right at the front as example `0-signer-authorization`. Somebody already built the training ground; run the drills there instead of rediscovering them on mainnet.

## Go run it

You could read five more posts about this, or you could open your program today and run the sentence test on every mutating instruction. It's an hour of work, maybe less, and this entire class is preventable with checks you already know how to write, which is about the best offer security ever makes. DMs open if you run it and something doesn't look right. Happy auditing.
