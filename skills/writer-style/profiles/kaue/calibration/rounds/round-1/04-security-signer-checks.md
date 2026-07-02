# The missing signer check: Solana's most boring $50M bug

You write an instruction that changes something valuable. A config owner, a vault's authority, who's allowed to withdraw. You pass in the account that's *supposed* to be the owner, you read its key, you update state. It works in your tests. You ship it.

Here's what you didn't do: check that the account actually signed the transaction.

That's the bug. Not a clever bug. Not a cryptographic break. It's the most boring missing line in the whole program, and this class of mistake has drained tens of millions of dollars out of Solana. An instruction treats an account as "the authority" without verifying that account actually signed the transaction, so any caller can hand your program any pubkey they like as the authority and act on its behalf. No key, no permission, nothing. Your admin function is now everyone's admin function.

I've shipped an instruction that trusted an account it never checked. Caught it in review, not in production, which is the only reason I'm typing this instead of writing a post-mortem. It's easy to miss precisely because the happy path looks identical whether the check is there or not. Your own tests, where you pass the real owner, pass either way.

## The bug, in one line

Say you're in native Rust, where nothing's enforced for you. You read the account, and it's on you to verify it:

```rust
// Vulnerable: `authority` is trusted but never verified to have signed
let authority = next_account_info(accounts_iter)?;
// ...code that treats `authority` as the config owner...
```

There's no signature there. The account is just bytes someone handed you, and until you check the signer flag your program has no idea whether the caller invoking it owns that key or simply typed it into a transaction. The fix is a single line:

```rust
if !authority.is_signer { return Err(...) }
```

That's it. Forgetting that one line *is* the vulnerability. There's no subtler version of it. A signature is the only thing that proves the caller actually controls the key they're claiming to be — anyone can address an envelope with your name on it; the signature is the part only you can produce.

If you want the canonical teaching version, it's already catalogued: `coral-xyz/sealevel-attacks`, example `0-signer-authorization`. Read it before you write your next handler. It's the cheapest security education on Solana and it costs you an afternoon.

## Anchor gives you two guards, and you need both

So does the framework save you? Half. Type an account as `Signer<'info>` and Anchor enforces the signature at deserialization; the instruction won't even run if that account didn't sign. That's genuinely good. It's also only half the check, and half a check on an authority is exactly how the second version of this bug ships. You reach for `Signer`, the compiler's happy, the tests stay green, and it *feels* handled. That feeling is the whole trap.

Because "someone signed" is not the same as "the *right* someone signed." Walk the two failure cases:

- `Signer` without `has_one`: *any* signer passes. I sign with my own keypair, I'm a valid signer as far as the runtime cares, and your instruction happily lets me act as the authority — because you never checked that I'm *the* authority stored on the account.
- `has_one` without `Signer`: now you're checking the account matches the stored authority, but nobody proved they control it. Right account, no proof of possession.

Either check alone is incomplete. You want both, and in Anchor that's two small pieces on the same struct:

```rust
#[derive(Accounts)]
pub struct UpdateConfig<'info> {
    #[account(mut, has_one = authority)]
    pub config: Account<'info, Config>,
    pub authority: Signer<'info>,
}
```

`has_one = authority` checks the key stored on `config` matches the account you passed. `Signer<'info>` proves that account signed. Together they say the one thing you actually mean: the account that owns this config authorized this call. Neither half says it alone.

## It's never just the signer

One check is never the whole job. The signer check is a single leg of a tripod, and on every state-mutating instruction you want all three legs, not one:

1. **Signer:** the authority actually signed.
2. **Owner:** the account is owned by the program you expect, not a look-alike someone else created.
3. **Address / PDA:** the account sits at the address it's supposed to, derived from the seeds you expect.

Skip any leg and the stool tips. Cashio, March 2022, is the expensive lesson here: roughly $52M minted against fake collateral accounts that passed an incomplete validation chain. The root cause wasn't a broken signature or cracked crypto, it was a missing link in account validation. The attacker fed in accounts that looked right on the axis the program happened to check and were fake on the axis it didn't, and that single gap was enough to mint tens of millions out of nothing. That's the whole genre. Not exotic. A gap in the checklist.

## How to audit for it

I hunt these the same low-tech way every time, and it isn't a fuzzer. You don't need one to find most of them; you need one sentence per instruction.

For every instruction that mutates state, say it out loud in one plain sentence: *who* is allowed to call this? "Only the config's stored authority may change the fee." Then go find the line of code that enforces exactly that sentence. The `Signer`. The `has_one`. The explicit `is_signer` check.

If your sentence says "only the stored authority" and the code only checks `is_signer` with no `has_one` — the sentence and the constraint don't match. That mismatch is your finding. Every time.

Do it for the whole program, one instruction at a time, and then again on every diff that adds or touches one, because the check that was there last month is one careless refactor away from gone. It's tedious. It's also the first move a paid auditor runs, and it catches the bug class that has cost Solana programs more than any clever exploit ever has.

None of this is hard. That's the uncomfortable part. The missing signer check isn't a hard bug, it's a boring one, and boring is exactly why it keeps slipping through. Nobody feels heroic writing the check, and nobody notices it's gone until someone else does. Write the sentence for every handler you have. If one of them doesn't have a line that matches it, you just found something worth a lot more than the weekend it'll take to fix. DMs open if you want a second pair of eyes on a handler you're not sure about.
