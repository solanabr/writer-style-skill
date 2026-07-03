# From `anchor init` to devnet: your first program, deployed

We put you through Rust last lesson: ownership, borrowing, the borrow checker arguing with you about things you were sure were fine. That was the price of admission. Today you collect. We're going to initialize an Anchor project, walk through what it actually generates, build it, test it locally, and then deploy it to devnet, a real public cluster where anyone with an RPC connection can call your code. By the end of this lesson you'll have a program ID that resolves on a network you don't run, and you'll know how to verify that claim yourself instead of taking my word for it. Tag along with a terminal open, because every command here is one you run yourself.

Prereqs are exactly what lesson 2 left you with, the Rust toolchain and Anchor installed, and honestly nothing else. Anchor 1.0 bundles the Solana toolchain, so there's no separate `solana` CLI to install and keep version-matched with everything else on your machine. One whole category of setup pain, gone before you ever meet it.

## Scaffold the project

```bash
anchor init my_program
cd my_program
```

That one `anchor init my_program` generates more than you need today, the folder looks bigger than it is, most of it is scenery for now. The load-bearing parts:

- **`programs/my_program/src/lib.rs`**: the program itself. This is where your Rust lives, and where you'll spend most of your time from here on out.
- **`tests/`**: the generated test template, which we'll come back to in a minute.
- **`migrations/`**: deploy scripts, which are scenery today and will stay scenery for a while.
- **`Anchor.toml`**: cluster and wallet config. A small file that decides a lot, and the one you'll come back to most in this lesson: which cluster you're talking to, and which wallet pays for it.

And one file that is NOT there yet: `target/deploy/my_program-keypair.json`. It appears on your first build, and it matters more than its filename suggests, because it's the program's identity. On Solana a program lives at an address like everything else on the chain, and that keypair is where the address comes from. Which has a strange consequence: you know your program's address before it exists anywhere. The address isn't assigned to you at deploy time by some registrar, it falls out of a keypair sitting in your own `target/` folder.

Now open `lib.rs` and look near the top: `declare_id!()`. That macro declares, in source, the address your program claims to live at, and it has to match the deploy keypair, or your deploy dies confused about who it is. Keep that in your pocket, because it's the #1 first-deploy failure and we'll defuse it before it happens to you.

## Build it

```bash
anchor build
```

`anchor build` is the routine step of this lesson, so run it and let it finish while we talk about what comes out the other end.

Two artifacts, and they map cleanly onto the two halves of everything you'll build in this course. The compiled program, a `.so` file, lands in `target/deploy/`; that binary is the thing that will actually live on-chain and execute. The IDL lands in `target/idl/`, and this one deserves a beat, because everything client-side hangs off it: the IDL is a machine-readable description of your program's instructions and accounts, and it's how a TypeScript client will know what it can call, with what arguments, against which accounts, without ever reading a line of your Rust. Program goes on-chain, IDL goes to whoever wants to talk to it. When we build the client next lesson, this file is the contract between the two.

Oh, and your first build is also the moment `my_program-keypair.json` shows up in `target/deploy/`. After this command, your program officially has an identity.

## Test it before it leaves your machine

```bash
anchor test
```

If you've read older Anchor tutorials (you will, they're everywhere, and most of them predate 1.0), this step behaves differently than they describe. As of Anchor 1.0, `anchor test` runs against Surfpool, not `solana-test-validator`, and the default test template is LiteSVM: Rust tests that run in-process. In-process means the runtime gets loaded inside the test binary itself, so there's no separate validator process to boot, wait for, and tear down every time you want to know whether your change works. The older workflow made you pay a startup tax on every run; the new default makes the feedback loop tight enough that testing stops feeling like a chore and starts feeling like hitting save.

The generated template ships with a passing test, so run it, watch it go green, and move on — we'll write real tests later in the course, once there's real logic to break.

## Point it at devnet

Why not stay on localhost until you're ready for mainnet? Because localhost only ever proves that your code works where you control every variable, and that's a much weaker claim than it sounds. Devnet proves it works on a public cluster, with other people's validators, real network latency, and real (if worthless) tokens — a place where the deployment mechanics are what you'll face on mainnet and the mistakes cost nothing but time. The switch is one edit in `Anchor.toml`:

```toml
[provider]
cluster = "devnet"
```

Make sure `wallet` in that same `[provider]` block points at a keypair that actually exists on your machine, because that wallet is about to pay for the deploy. Which brings us to funding. Devnet SOL is free but rate-limited:

```bash
solana airdrop 2
```

Requests are typically capped around 2 SOL each, and you'll want more than one request's worth. Deploying isn't a dusting of lamports like a normal transaction: the program account has to be rent-exempt for roughly 2× the binary size, rent-exempt meaning it holds enough SOL that the network considers it paid up and keeps it around indefinitely. For a typical starter program that adds up to a few SOL of devnet balance, so budget two or three airdrop rounds before you start. When the CLI faucet starts telling you no, and it eventually will, faucet.solana.com is the fallback. Ask, wait, ask again. Free money is slow money.

## Deploy

```bash
anchor deploy --provider.cluster devnet
```

This deploys through the upgradeable loader, and the wallet that deploys becomes the upgrade authority. That's a real decision hiding inside a default, so let's name both sides of it. The upside: you can ship changes later with `anchor upgrade`, same address, updated logic, and nobody who integrated with your program has to migrate anything. The downside is the same sentence read from the other end, because whoever holds that wallet's key can rewrite your program in place. Convenience and liability, one key. On devnet, don't sweat it; on mainnet, custody of that key becomes a conversation your future team will have more than once.

Plenty of first deploys fail, and they fail in three boring ways, so let's pre-empt all three:

1. **Insufficient balance.** The error says so in its own vocabulary, so airdrop again or go stand in line at the faucet — annoying precisely because it's the easiest one to fix and the slowest one to notice mid-command.
2. **`declare_id!` mismatch.** You cloned a repo, or regenerated your keys, and now the address in the source disagrees with the deploy keypair. The silver bullet? `anchor keys sync`. One command, and the ID in your source and the keypair agree again, honestly a tiny fix for how much confusion it clears up.
3. **Wrong cluster.** You deployed successfully, to localnet, and are now staring at a devnet explorer wondering where your program went. Re-check `cluster` in `Anchor.toml` before doubting anything else about your setup.

Small confession before an error message sends you spiraling: my team once spent two hours debugging a deploy, checked all of the above twice, and it turned out we had actually managed to break the testnet itself. You will, statistically, not manage that. Check the three things first.

## Verify it's live

Don't just trust the success message — the whole point of this ecosystem is that you never have to. Your deploy printed a program ID, so ask the cluster itself whether that address is real:

```bash
solana program show <PROGRAM_ID> --url devnet
```

Swap in your program ID, the same address sitting in `declare_id!()`. If this command prints the program's on-chain record back at you, you're live. That address now answers queries on a cluster you don't run, from any machine on the planet, whether yours is on or not.

But "the account exists" is a low bar, and passing it doesn't prove the program does anything. The real verification is calling it: the generated TS test/client already speaks to your program through the IDL, so point it at devnet and invoke the instruction for real. When that transaction lands, it wasn't a simulation and it wasn't localhost — someone else's validator just executed code you wrote!

## Where this goes

In lesson 1 a cluster was vocabulary; today you have a program ID that resolves on one, deployed from your own terminal, upgradeable with your own key. Two lessons of groundwork, and the gap between "I read about Solana" and "my code runs on it" is already closed — the rest of the course is about making what runs there worth calling.

Next lesson we build the half your users will actually touch: client development, meaning TypeScript and the wallet adapter, so calling your program stops requiring a terminal and starts looking like an app. And here's the part I like: everything client-side rides on the IDL you generated today, so you've already laid the rail for it.

Happy deploying! 🚀
