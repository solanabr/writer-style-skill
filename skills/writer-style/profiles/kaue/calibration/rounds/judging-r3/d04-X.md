# The missing signer check

A Solana program never sees a signature. By the time your instruction handler runs, the runtime has already verified every signature on the transaction and reduced each one to a boolean on the account it belongs to: `is_signer`. Reading that boolean is the program's job. The most expensive recurring bug class on Solana is the handler that never reads it.

The shape is always the same. An instruction handler treats some account as the authority (the vault owner, the admin, the position holder) and mutates state on that account's behalf without verifying that the account actually signed the transaction. From the attacker's side the consequence is total: they pass your pubkey as the authority, the handler never asks for proof of control, and now they are withdrawing your funds on your behalf, with your address sitting in the transaction logs as if everything were fine. No key was stolen. Nothing was cracked. The program simply never asked.

## Native Rust: the one line

Start in native Rust, where nothing is hidden from you. The check is explicit, one conditional you write yourself:

```rust
if !authority.is_signer {
    return Err(ProgramError::MissingRequiredSignature);
}
```

Forgetting this one line is the bug. The entire class reduces to that omission, and what makes the class durable is that the vulnerable version usually still contains something that resembles a security check:

```rust
// looks like a security check; it isn't one
if vault.authority != *authority.key {
    return Err(ProgramError::InvalidArgument);
}
```

This comparison verifies that the caller knows which pubkey the authority is. Every pubkey on Solana is public information, so it passes for anyone who can read your account state, which is everyone. A reviewer skimming the handler sees a conditional guarding the mutation, pattern-matches it as the auth check, and moves on. The check that's present hides the check that's missing.

I know how the line goes missing because I've shipped the vulnerable version myself. The comparison was there, it looked like the check, my tests were green — and they were green because every test I'd written signed with the correct keypair, which is precisely the case the missing check doesn't guard. Nothing failed. Nothing ever would have. The exploit is a transaction no honest client would ever construct, and a test suite is honest clients all the way down.

## Anchor: the pair

Anchor moves the check into the type system. Declare the account as `Signer<'info>` and the signature requirement is enforced at deserialization: if that account didn't sign, the instruction fails before your handler runs. The line you used to forget is now a type you can't skip.

It's tempting to stop there, and stopping there is the second version of the bug. `Signer` alone proves that somebody signed. Any signer clears it, including a keypair the attacker generated a second ago, so you've verified control of a key without verifying it's the right key. The mirror-image mistake is `has_one = authority` alone on the state account: now the passed account must match the authority stored in your state, but nobody proved they control it. An attacker reads the stored pubkey out of your account data, passes it in unsigned, and walks through. Each constraint alone answers half the question, and half an answer here rounds down to zero. The complete check is the pair:

```rust
#[derive(Accounts)]
pub struct Withdraw<'info> {
    pub authority: Signer<'info>,

    #[account(mut, has_one = authority)]
    pub vault: Account<'info, Vault>,
}
```

`Signer` proves the caller controls the key. `has_one` proves the key is the one your state says may act. Only together do they enforce the sentence you actually mean: the specific account this vault answers to signed this transaction.

## The trio

The signer check is one leg of a trio that belongs on every state-mutating instruction. The signer check asks: did the caller prove control of the key? The owner check asks: is this account's data owned by the program I expect, or is it a lookalike the attacker allocated and filled with convenient values? The address or PDA check asks: is this the exact account I derived, from the seeds I meant? Three checks, three different questions. An instruction that answers two of them is not two-thirds safe, because the attacker only needs the one that's missing.

Cashio, in March 2022, is what incomplete validation costs at scale: roughly $52M minted against fake collateral accounts that passed an incomplete validation chain. The chain had a missing link, and the attacker manufactured accounts that satisfied every check that existed and walked through the one that didn't. That is what "incomplete" means in practice: all the checks you wrote can pass, and it doesn't matter.

The canonical teaching catalog for this family is `coral-xyz/sealevel-attacks`. Signer authorization is example `0-signer-authorization`: the first entry in the catalog, with the vulnerable and patched versions side by side. Read it before the exotic entries.

## Auditing for it

So how do you find this in a program you already shipped? The audit procedure is plain enough to feel like it can't be the real technique. It is. For every instruction that mutates state, write one sentence naming who may call it: only the vault authority may withdraw. Only the admin stored in config may change the fee. Anyone may crank this. Then find the line of code that enforces exactly that sentence — not approximately that sentence, exactly it. If the sentence says "the vault authority" and the constraints prove "some signer," or "the stored pubkey, unsigned," the distance between the sentence and the code is the finding.

Tooling makes the sweep cheap now. I've run ten rounds of agentic security audits over a single release and pulled 150+ pertinent findings out of one weekend, work that used to take weeks by hand. That ratio changed how often I'm willing to re-run the sweep, honestly. But tooling produces candidates, and the sentence test is what turns a candidate into a finding, because it forces you to state what the constraint was supposed to mean before you check what it actually enforces.

None of this requires a security team to start. If you have a program deployed anywhere right now, the exercise costs an evening: the one-sentence caller statement for each state-mutating instruction, then the hunt for each enforcing line. Most evenings you'll find every line and sleep better for having looked. If one is missing, you found it before someone else did.
