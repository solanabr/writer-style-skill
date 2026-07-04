# The missing signer check: Solana's most boring $50M bug

The bug that has taken the most money out of Solana programs is not a clever one. An instruction handler treats some account as the authority (the vault owner, the admin, the position holder) and moves funds or rewrites state on that account's behalf, without ever verifying that the account actually signed the transaction. Once that check is missing, any caller can pass any pubkey as the authority and act in its name, because your program asked who the authority is but never asked the caller to prove they control it.

To see why the runtime even lets this happen, you need one fact about how Solana hands accounts to your program. Every signature on a transaction is verified before your handler runs; after that, what your code receives is a list of accounts, each carrying an `is_signer` flag recording whether the holder of that key signed. The runtime will never reject an instruction because an "authority" didn't sign, since it has no idea which of your accounts is supposed to be one. Reading the flag is your job, and it stays your job on every instruction you ever add, including the ones you write later, when signer checks are the last thing on your mind.

## The check, in native Rust

In native Rust the check is a single explicit conditional, and forgetting it is the entire vulnerability:

```rust
if !authority.is_signer {
    return Err(ProgramError::MissingRequiredSignature);
}
```

What lets the omission survive review is that the vulnerable handler usually still contains something that resembles an authorization check:

```rust
// proves the caller knows the address, not that they control it
if vault.authority != *authority.key {
    return Err(ProgramError::InvalidArgument);
}
```

That comparison verifies the caller knows which pubkey the authority is. Every pubkey on chain is public, so anyone who can read your account state passes it, and everyone can read your account state. A reviewer sees a conditional standing guard in front of the mutation, files it as the authorization logic, and keeps reading.

So why does a one-line check keep going missing in programs written by people who know exactly what it's for? Because nothing in a normal development loop ever exercises its absence. Your tests sign with the correct keypair, they were always going to, that's what an honest client does, and a transaction signed by the right key is precisely the case the missing check doesn't guard. The exploiting transaction is one no honest client will ever build, so unless you sit down and write the dishonest one yourself, every light stays green.

I shipped the vulnerable version once. A small vault program, early on: the withdraw handler compared the stored authority against the passed account, I read that comparison as the auth check, tests passed, deployed, moved on to the frontend. I found it about ten days later, not through an audit, just re-reading the handler while wiring up a second instruction, and I can tell you what that week was like. Before I let myself touch anything I pulled the program's full transaction history and went through it one withdraw at a time, checking each against the list of people who had deposited. The money was small, a few hundred dollars from people in my own community who had put it there because I asked them to test, but the checking did not feel small. Nobody had found it. I paused deposits, patched the one line, redeployed, and then told the depositors what had been sitting underneath their funds for ten days, which was the hardest part and the part I'd repeat first. The only reason it held is that nobody had gone looking, and I don't get to take credit for that.

## What Anchor changes, and what it doesn't

Anchor moves the signer check into the account types. Declare the account as `Signer<'info>` and the signature requirement is enforced at deserialization: if that account didn't sign the transaction, your handler never runs at all. The check I once forgot now executes before my handler logic gets any chance to be wrong.

The trap is stopping there, because `Signer` alone answers only half the question. `Signer` without `has_one` means any signer passes, not the right one; an attacker signs with a keypair generated a second ago and clears the constraint. And `has_one = authority` without `Signer` means the right account arrives, the one your state actually names, but nobody proved they control it: the attacker reads the stored pubkey straight out of your account data and passes that account in unsigned. Either check alone is incomplete. The correct form is the pair:

```rust
#[derive(Accounts)]
pub struct Withdraw<'info> {
    pub authority: Signer<'info>,

    #[account(mut, has_one = authority)]
    pub vault: Account<'info, Vault>,
}
```

`Signer` proves the caller controls the key. `has_one` proves the key matches the authority your state has on record. Together they enforce the sentence you actually meant: the specific account this vault answers to signed this transaction.

## The other two checks

Don't stop at the signer check either, because it is only one leg of a trio that belongs on every state-mutating instruction. The owner check confirms the account is owned by the program you expect, because an attacker can create an account of their own, fill it with whatever bytes make your deserialization happy, and hand it to your instruction as if it were yours. The address check, or PDA check, confirms this is the exact account you meant, derived from the seeds you meant. Each answers a question the other two can't, and skipping any one of the three leaves the same kind of door open.

Cashio, in March 2022, is what this family costs at scale: roughly $52M minted against fake collateral accounts that passed an incomplete validation chain. The root cause was a missing link in account validation, not a cryptographic break — nobody touched the signatures. The attacker manufactured accounts that satisfied every check the program actually made, and the check that would have rejected them was simply never written.

The canonical catalog for this family is `coral-xyz/sealevel-attacks`, with signer authorization at the very top as example `0-signer-authorization`, vulnerable and patched side by side. If you came from the EVM world and reach for OpenZeppelin by reflex, this repo is the nearest thing Solana has for attack patterns; read the zeroth entry before any of the exotic ones.

## Finding it in a program you already shipped

Auditing for this in code that is already live is a plain procedure, and it works. For every instruction that mutates state, write one sentence naming who may call it: only the vault authority may withdraw, only the admin stored in config may change the fee, anyone may crank this. Then find the line of code that enforces exactly that sentence — not roughly, exactly. If your sentence says "the vault authority" and the constraints prove "some signer," or "the stored pubkey, unproven," the gap between the sentence and the code is the finding. It would have caught my vault bug on the first pass: my sentence was "only the depositor's chosen authority may withdraw," and the code enforced "anyone who knows that authority's address," which was everyone with an RPC connection.

If a handler of yours came to mind anywhere in the last thousand words, run the sentence exercise on it tonight — it costs an evening, and you will spend most of that evening confirming lines that are already there. And if you find one that isn't, and you're sitting with that specific cold feeling I described, write to me before you do anything loud. I've been on the wrong side of this exact line.
